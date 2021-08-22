import threading
from socket_handler import SocketThread

class ListenThread(threading.Thread):

    def __init__(self, kivy_app):
        threading.Thread.__init__(self)
        self.kivy_app = kivy_app

    def run(self):
        while True:
            try:
                connection, client_info = self.kivy_app.soc.accept()
                self.kivy_app.label.text = "New Connection from {client_info}".format(client_info=client_info)
                socket_thread = SocketThread(connection=connection,
                                             client_info=client_info, 
                                             kivy_app=self.kivy_app,
                                             buffer_size=1024,
                                             recv_timeout=10)
                socket_thread.start()
            except BaseException as e:
                self.kivy_app.soc.close()
                print(e)
                self.kivy_app.label.text = "Socket is No Longer Accepting Connections"
                self.kivy_app.create_socket_btn.disabled = False
                self.kivy_app.close_socket_btn.disabled = True
                break