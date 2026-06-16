import logging

def configure_logging(app):
    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"]),
        format="%(asctime)s %(levelname)s %(message)s"
    )
