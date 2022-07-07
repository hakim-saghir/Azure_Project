import configparser
import logging
from pathlib import Path

from flask import Flask

# Logs
logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s : [%(asctime)s] : %(message)s'",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = Flask(__name__)

# Configs
config = configparser.ConfigParser()
config.read("application.properties")
app.secret_key = config.get("application_parameters", "SECRET_KEY")


# Constants
loaded_images_temporary_storage_path = config.get("application_parameters", "LOADED_IMAGES_TEMPORARY_STORAGE_PATH")
loaded_images_temporary_storage_path = Path(loaded_images_temporary_storage_path).absolute().as_posix()
print(loaded_images_temporary_storage_path)

# Routes
from web_app.src.routes.index import index_blueprint
app.register_blueprint(index_blueprint)



