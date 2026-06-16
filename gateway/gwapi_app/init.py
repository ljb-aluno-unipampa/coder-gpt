from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .logging_config import configure_logging

def create_app():

```
load_dotenv()

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config.from_object(Config)

configure_logging(app)

from .auth import auth_bp
from .web import web_bp
from .api import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(web_bp)
app.register_blueprint(api_bp)

return app
```
