import socket
import pickle
import threading
import numpy

from libs import gann, nn, pygad

from config import data_inputs, data_outputs

def fitness_func(solution, sol_idx):
    global GANN_instance, data_inputs, data_outputs
    predictions = nn.predict(last_layer=GANN_instance.population_networks[sol_idx],
                                           data_inputs=data_inputs)
    correct_predictions = numpy.where(predictions == data_outputs)[0].size
    solution_fitness = (correct_predictions/data_outputs.size)*100
    return solution_fitness

def callback_generation(ga_instance):
    global GANN_instance, last_fitness
    population_matrices = gann.population_as_matrices(population_networks=GANN_instance.population_networks, 
                                                            population_vectors=ga_instance.population)
    GANN_instance.update_population_trained_weights(population_trained_weights=population_matrices)

def prepare_GA(GANN_instance):
    population_vectors = gann.population_as_vectors(population_networks=GANN_instance.population_networks)
    initial_population = population_vectors.copy()
    num_parents_mating = 4 # Number of solutions to be selected as parents in the mating pool.
    num_generations = 500 # Number of generations.
    mutation_percent_genes = 5 # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists.
    parent_selection_type = "sss" # Type of parent selection.
    crossover_type = "single_point" # Type of the crossover operator.
    mutation_type = "random" # Type of the mutation operator.
    keep_parents = 1 # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.
    init_range_low = -2
    init_range_high = 5
    
    ga_instance = pygad.GA(num_generations=num_generations, 
                           num_parents_mating=num_parents_mating, 
                           initial_population=initial_population,
                           fitness_func=fitness_func,
                           mutation_percent_genes=mutation_percent_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           keep_parents=keep_parents,
                           callback_generation=callback_generation)

    return ga_instance

class RecvThread(threading.Thread):

    def __init__(self, kivy_app, buffer_size, recv_timeout):
        threading.Thread.__init__(self)
        self.kivy_app = kivy_app
        self.buffer_size = buffer_size
        self.recv_timeout = recv_timeout

    def recv(self):
        received_data = b""
        while str(received_data)[-2] != '.':
            try:
                self.kivy_app.soc.settimeout(self.recv_timeout)
                received_data += self.kivy_app.soc.recv(self.buffer_size)

            except socket.timeout:
                print(f"A socket.timeout exception occurred because the server \
                    did not send any data for {self.recv_timeout} seconds.")
                self.kivy_app.label.text = "{self.recv_timeout} Seconds of Inactivity. \
                    socket.timeout Exception Occurred"
                return None, 0

            except BaseException as e:
                print("Error While Receiving Data from the Server: {e}.")
                self.kivy_app.label.text = "Error While Receiving Data from the Server"
                return None, 0

        try:
            received_data = pickle.loads(received_data)
        except BaseException as e:
            print("Error Decoding the Client's Data: {e}.\n")
            self.kivy_app.label.text = "Error Decoding the Client's Data"
            return None, 0
    
        return received_data, 1

    def run(self):
        global GANN_instance

        subject = "echo"
        GANN_instance = None
        best_sol_idx = -1

        while True:
            data = {
                "subject": subject, 
                "data": GANN_instance, 
                "best_solution_idx": best_sol_idx
            }
            data_byte = pickle.dumps(data)

            self.kivy_app.label.text = f"Sending a Message of Type {subject} to the Server"

            try:
                self.kivy_app.soc.sendall(data_byte)
            except BaseException as e:
                self.kivy_app.label.text = "Error Connecting to the Server. The server might has been closed."
                print("Error Connecting to the Server: {e}")
                break

            self.kivy_app.label.text = "Receiving Reply from the Server"
            received_data, status = self.recv()
            if status == 0:
                self.kivy_app.label.text = "Nothing Received from the Server"
                break
            else:
                self.kivy_app.label.text = "New Message from the Server"

            subject = received_data["subject"]
            if subject == "model":
                GANN_instance = received_data["data"]
            elif subject == "done":
                self.kivy_app.label.text = "Model is Trained"
                break
            else:
                self.kivy_app.label.text = f"Unrecognized Message Type: {subject}"
                break

            ga_instance = prepare_GA(GANN_instance)

            ga_instance.run()

            subject = "model"
            best_sol_idx = ga_instance.best_solution()[2]