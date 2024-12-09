import websocket
import threading
import time

class ReverseWebSocketClient:
    """

    """

    def __init__(self, server_url: str):
        """


.
        """
        self.server_url = server_url
        self.ws = None

    def on_message(self, message):
        """


        """
        print(f"[Message reçu] : {message}")

    def on_error(self, error):
        


        print(f"[Erreur] : {error}")

    def on_close(self):
        """
        """
        print("[Connexion fermée]")

    def on_open(self):
        """
        """
        print("[Connexion établie]")
        self.ws.send("Client connecté !")

    def start(self):
        """
        """
        def run():
            self.ws = websocket.WebSocketApp(
                self.server_url,
                on_message=lambda ws, msg: self.on_message(msg),
                on_error=lambda ws, err: self.on_error(err),
                on_close=lambda ws: self.on_close(),
            )
            self.ws.on_open = lambda ws: self.on_open()
            self.ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    client = ReverseWebSocketClient("ws://votre_serveur:port")
    client.start()

    while True:
        time.sleep(1)
