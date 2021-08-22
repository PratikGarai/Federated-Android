import pickle
import time
import numpy
import threading
import nn

from server import GANN_instance, model, data_inputs, data_outputs

class SocketThread(threading.Thread):

    def __init__(
        self, 
        connection, 
        client_info, 
        kivy_app, 
        buffer_size=1024, 
        recv_timeout=5
    ):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client_info = client_info
        self.buffer_size = buffer_size
        self.recv_timeout = recv_timeout
        self.kivy_app = kivy_app


    def recv(self):
        received_data = b""
        while True:
            try:
                
                data = self.connection.recv(self.buffer_size)
                received_data += data

                # Nothing received from the client.
                if data == b'': 
                    received_data = b""
                    # If still nothing received for a number of seconds specified by the recv_timeout 
                    # attribute, return with status 0 to close the connection.
                    if (time.time() - self.recv_start_time) > self.recv_timeout:
                        return None, 0 # 0 means the connection is no longer active and it should be closed.

                elif str(data)[-2] == '.':
                    log = f"All data ({len(received_data)} bytes) Received from {self.client_info}."
                    print(log)
                    self.kivy_app.label.text = log

                    if len(received_data) > 0:
                        try:
                            # Decoding the data (bytes).
                            received_data = pickle.loads(received_data)
                            # Returning the decoded data.
                            return received_data, 1

                        except BaseException as e:
                            print(f"Error Decoding the Client's Data: {e}.\n")
                            self.kivy_app.label.text = "Error Decoding the Client's Data"
                            return None, 0

                else:
                    # In case data are received from the client, update the 
                    # recv_start_time to the current time to reset the timeout counter.
                    self.recv_start_time = time.time()

            except BaseException as e:
                print(f"Error Receiving Data from the Client: {e}.\n")
                self.kivy_app.label.text = "Error Receiving Data from the Client"
                return None, 0


    def model_averaging(
        self, 
        model, 
        other_model
    ):
        model_weights = nn.layers_weights(last_layer=model, initial=False)
        other_model_weights = nn.layers_weights(last_layer=other_model, initial=False)
        new_weights = numpy.array(model_weights + other_model_weights)/2
        nn.update_layers_trained_weights(last_layer=model, final_weights=new_weights)


    def reply(
        self, 
        received_data
    ):
        global GANN_instance, data_inputs, data_outputs, model

        if (type(received_data) is dict):

            if (("data" in received_data.keys()) and ("subject" in received_data.keys())):

                subject = received_data["subject"]
                print(f"Client's Message Subject is {subject}.")
                self.kivy_app.label.text = f"Client's Message Subject is {subject}"
                print("Replying to the Client.")
                self.kivy_app.label.text = "Replying to the Client"

                if subject == "echo":
                    if model is None:
                        data = {"subject": "model", "data": GANN_instance}
                    else:
                        predictions = nn.predict(last_layer=model, data_inputs=data_inputs)
                        error = numpy.sum(numpy.abs(predictions - data_outputs))
                        # In case a client sent a model to the server despite that the model error is 
                        # 0.0. In this case, no need to make changes in the model.
                        if error == 0:
                            data = {"subject": "done", "data": None}
                        else:
                            data = {"subject": "model", "data": GANN_instance}

                    try:
                        response = pickle.dumps(data)
                    except BaseException as e:
                        print(f"Error Encoding the Message: {e}.\n")
                        self.kivy_app.label.text = "Error Encoding the Message"

                elif subject == "model":
                    try:
                        GANN_instance = received_data["data"]
                        best_model_idx = received_data["best_solution_idx"]

                        best_model = GANN_instance.population_networks[best_model_idx]
                        if model is None:
                            model = best_model
                        else:
                            predictions = nn.predict(last_layer=model, data_inputs=data_inputs)
                            error = numpy.sum(numpy.abs(predictions - data_outputs))
                            # In case a client sent a model to the server despite that the model error is 0.0. 
                            # In this case, no need to make changes in the model.
                            if error == 0:
                                data = {"subject": "done", "data": None}
                                response = pickle.dumps(data)
                                return

                            self.model_averaging(model, best_model)
                        # print(best_model.trained_weights)
                        # print(model.trained_weights)

                        predictions = nn.predict(last_layer=model, data_inputs=data_inputs)
                        print(f"Model Predictions: {predictions}")

                        error = numpy.sum(numpy.abs(predictions - data_outputs))
                        print(f"Prediction Error = {error}")
                        self.kivy_app.label.text = f"Prediction Error = {error}"

                        if error != 0:
                            data = {"subject": "model", "data": GANN_instance}
                            response = pickle.dumps(data)
                        else:
                            data = {"subject": "done", "data": None}
                            response = pickle.dumps(data)

                    except BaseException as e:
                        print("Error Decoding the Client's Data: {e}.\n")
                        self.kivy_app.label.text = "Error Decoding the Client's Data"
                else:
                    response = pickle.dumps("Response from the Server")
                            
                try:
                    self.connection.sendall(response)
                except BaseException as e:
                    log = f"Error Sending Data to the Client: {e}.\n"
                    print(log)
                    self.kivy_app.label.text = log

            else:
                print("The received dictionary from the client must have the 'subject' and 'data'\
                     keys available. The existing keys are {received_data.keys()}.")
                self.kivy_app.label.text = "Error Parsing Received Dictionary"
        else:
            log = f"A dictionary is expected to be received from the \
                client but {type(received_data)} received."
            print(log)
            self.kivy_app.label.text = log


    def run(self):
        log = f"Running a Thread for the Connection with {self.client_info}."
        print(log)
        self.kivy_app.label.text = log

        # This while loop allows the server to wait for the client 
        # to send data more than once within the same connection.
        while True:
            self.recv_start_time = time.time()
            time_struct = time.gmtime()
            date_time = "Waiting to Receive Data Starting from {day}/{month}/{year} {hour}:{minute}:{second} GMT"\
            .format(year=time_struct.tm_year, month=time_struct.tm_mon, day=time_struct.tm_mday, 
            hour=time_struct.tm_hour, minute=time_struct.tm_min, second=time_struct.tm_sec)

            print(date_time)
            received_data, status = self.recv()
            if status == 0:
                self.connection.close()
                log = f"Connection Closed with {self.client_info}"
                self.kivy_app.label.text = log
                print(f"Connection Closed with {self.client_info} either due to inactivity \
                    for {self.recv_timeout} seconds or due to an error.", end="\n\n")
                break

            # print(received_data)
            self.reply(received_data)