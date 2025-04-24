from doc_app import VoteApp


def init_app(app: VoteApp):
    # register blueprint routers
    from flask_cors import CORS

    from controllers.service_api import bp as service_api_bp

    CORS(
        service_api_bp,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-App-Code",
            "X-Session-ID",
            "X-Is-End",
        ],
        methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    )
    app.register_blueprint(service_api_bp)
