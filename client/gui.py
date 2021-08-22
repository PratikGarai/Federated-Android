import kivy.app
import kivy.uix.button
import kivy.uix.label
import kivy.uix.textinput
import kivy.uix.boxlayout
import socket

class ClientApp(kivy.app.App):

    def __init__(self):
        super().__init__()


    def create_socket(self, *args):
        self.soc = socket.socket(
            family=socket.AF_INET, 
            type=socket.SOCK_STREAM
        )
        self.label.text = "Socket Created"

        self.create_socket_btn.disabled = True
        self.connect_btn.disabled = False
        self.close_socket_btn.disabled = False


    def connect(self, *args):
        try:
            self.soc.connect((
                self.server_ip.text, 
                int(self.server_port.text)
            ))
            self.label.text = "Successful Connection to the Server"
    
            self.connect_btn.disabled = True
            self.recv_train_model_btn.disabled = False

        except BaseException as e:
            self.label.text = "Error Connecting to the Server"
            print(f"Error Connecting to the Server: {e}")

            self.connect_btn.disabled = False
            self.recv_train_model_btn.disabled = True


    def recv_train_model(self, *args):
        global GANN_instance

        self.recv_train_model_btn.disabled = True
        recvThread = RecvThread(
            kivy_app=self, 
            buffer_size=1024, 
            recv_timeout=10
        )
        recvThread.start()


    def close_socket(self, *args):
        self.soc.close()
        self.label.text = "Socket Closed"

        self.create_socket_btn.disabled = False
        self.connect_btn.disabled = True
        self.recv_train_model_btn.disabled = True
        self.close_socket_btn.disabled = True


    def build(self):
        self.create_socket_btn = kivy.uix.button.Button(
            text="Create Socket"
        )
        self.create_socket_btn.bind(on_press=self.create_socket)

        self.server_ip = kivy.uix.textinput.TextInput(
            hint_text="Server IPv4 Address", 
            text="localhost"
        )
        self.server_port = kivy.uix.textinput.TextInput(
            hint_text="Server Port Number", 
            text="10000"
        )

        self.server_info_boxlayout = kivy.uix.boxlayout.BoxLayout(
            orientation="horizontal"
        )

        self.server_info_boxlayout.add_widget(self.server_ip)
        self.server_info_boxlayout.add_widget(self.server_port)

        self.connect_btn = kivy.uix.button.Button(
            text="Connect to Server", 
            disabled=True
        )
        self.connect_btn.bind(on_press=self.connect)

        self.recv_train_model_btn = kivy.uix.button.Button(
            text="Receive & Train Model", 
            disabled=True
        )
        self.recv_train_model_btn.bind(on_press=self.recv_train_model)

        self.close_socket_btn = kivy.uix.button.Button(
            text="Close Socket", 
            disabled=True
        )
        self.close_socket_btn.bind(on_press=self.close_socket)

        self.label = kivy.uix.label.Label(
            text="Socket Status"
        )

        self.box_layout = kivy.uix.boxlayout.BoxLayout(
            orientation="vertical"
        )
        self.box_layout.add_widget(self.create_socket_btn)
        self.box_layout.add_widget(self.server_info_boxlayout)
        self.box_layout.add_widget(self.connect_btn)
        self.box_layout.add_widget(self.recv_train_model_btn)
        self.box_layout.add_widget(self.close_socket_btn)
        self.box_layout.add_widget(self.label)

        return self.box_layout