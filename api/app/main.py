from app import create_app, db
from app.routes import bp

app = create_app()
app.register_blueprint(bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
