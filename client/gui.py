import kivy.app
import kivy.uix.button
import kivy.uix.label
import kivy.uix.textinput
import kivy.uix.boxlayout

class ClientApp(kivy.app.App):

    def build(self):
        self.create_socket_btn = kivy.uix.button.Button(
            text="Create Socket"
        )

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

        self.recv_train_model_btn = kivy.uix.button.Button(
            text="Receive & Train Model", 
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
        self.box_layout.add_widget(self.server_info_boxlayout)
        self.box_layout.add_widget(self.connect_btn)
        self.box_layout.add_widget(self.recv_train_model_btn)
        self.box_layout.add_widget(self.close_socket_btn)
        self.box_layout.add_widget(self.label)

        return self.box_layout