from server import app
from server.models import db

if __name__ == "__main__":
    db.create_all()
    db.init_app(app)
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
