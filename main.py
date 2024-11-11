from website import create_app
from website.chat import socketio  # Import socketio to run the app
from config import Config

app = create_app()

if __name__ == "__main__":
    # Use socketio.run to handle both HTTP and WebSocket connections
    socketio.run(app, debug=True, host=Config.Host, port=Config.PORT)
