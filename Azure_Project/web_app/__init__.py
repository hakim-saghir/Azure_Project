import configparser
import logging
import os
from pathlib import Path
from flask import Flask
from .services.utils.utils_func import check_if_tag_exist

# Logs
logging.basicConfig(level=logging.NOTSET,
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
if not Path(loaded_images_temporary_storage_path).exists():
    os.mkdir(loaded_images_temporary_storage_path)


print(loaded_images_temporary_storage_path)

# Routes
from .services.routes import routes
app.register_blueprint(routes)
