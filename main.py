import logging
from app import app, init_app

# Configure logging for easier debugging
logging.basicConfig(level=logging.DEBUG)

# Inicializa a aplicação (rotas, banco etc.)
init_app(app)

# Executa o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
