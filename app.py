from app_factory import create_app

app = create_app()


@app.route("/")
def index():
    return {
        "version": "0.1.0",
        "description": "This is the backend for project",
        "authors": [{"name": "csy100", "email": "csiyu100@gmail.com"}],
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
