import kivy.app
import kivy.uix.button
import kivy.uix.label
import kivy.uix.textinput
import kivy.uix.boxlayout

class ServerApp(kivy.app.App):

    def build(self):
        self.create_socket_btn = kivy.uix.button.Button(
            text="Create Socket", 
            disabled=False
        )

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

        self.listen_btn = kivy.uix.button.Button(
            text="Listen to Connections", 
            disabled=True
        )

        self.close_socket_btn = kivy.uix.button.Button(
            text="Close Socket", 
            disabled=True
        )

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