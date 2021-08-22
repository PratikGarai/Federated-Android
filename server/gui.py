import kivy.app
import kivy.uix.button
import kivy.uix.label
import kivy.uix.textinput
import kivy.uix.boxlayout
import socket

from thread_handler import ListenThread

class ServerApp(kivy.app.App):

    def __init__(self):
        super().__init__()
        

    def create_socket(self, *args):
        self.soc = socket.socket(
            family=socket.AF_INET, 
            type=socket.SOCK_STREAM
        )
        self.label.text = "Socket Created"

        self.create_socket_btn.disabled = True
        self.bind_btn.disabled = False
        self.close_socket_btn.disabled = False


    def bind_socket(self, *args):
        ipv4_address = self.server_ip.text
        port_number = self.server_port.text
        self.soc.bind((ipv4_address, int(port_number)))
        self.label.text = "Socket Bound to IPv4 & Port Number"

        self.bind_btn.disabled = True
        self.listen_btn.disabled = False


    def listen_accept(self, *args):
        self.soc.listen(1)
        self.label.text = "Socket is Listening for Connections"

        self.listen_btn.disabled = True

        self.listenThread = ListenThread(kivy_app=self)
        self.listenThread.start()


    def close_socket(self, *args):
        self.soc.close()
        self.label.text = "Socket Closed"

        self.create_socket_btn.disabled = False
        self.bind_btn.disabled = True
        self.listen_btn.disabled = True
        self.close_socket_btn.disabled = True


    def build(self):

        self.create_socket_btn = kivy.uix.button.Button(
            text="Create Socket", 
            disabled=False
        )
        self.create_socket_btn.bind(on_press=self.create_socket)

        self.server_ip = kivy.uix.textinput.TextInput(
            hint_text="IPv4 Address", 
            text="localhost"
        )
        self.server_port = kivy.uix.textinput.TextInput(
            hint_text="Port Number", 
            text="10000"
        )

        self.server_socket_box_layout = kivy.uix.boxlayout.BoxLayout(
            orientation="horizontal"
        )
        self.server_socket_box_layout.add_widget(self.server_ip)
        self.server_socket_box_layout.add_widget(self.server_port)

        self.bind_btn = kivy.uix.button.Button(
            text="Bind Socket", 
            disabled=True
        )
        self.bind_btn.bind(on_press=self.bind_socket)

        self.listen_btn = kivy.uix.button.Button(
            text="Listen to Connections", 
            disabled=True
        )
        self.listen_btn.bind(on_press=self.listen_accept)

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
        self.box_layout.add_widget(self.server_socket_box_layout)
        self.box_layout.add_widget(self.bind_btn)
        self.box_layout.add_widget(self.listen_btn)
        self.box_layout.add_widget(self.close_socket_btn)
        self.box_layout.add_widget(self.label)

        return self.box_layout