from flask import blueprints, render_template, request, flash
from web_app import loaded_images_temporary_storage_path

index_blueprint = blueprints.Blueprint("index_blueprint", "index_blueprint")


@index_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@index_blueprint.route('/add_images', methods=['GET'])
def add_images():
    return render_template('add_images.html')


@index_blueprint.route('/upload_images', methods=['POST'])
def upload_images():
    uploaded_files = request.files.getlist("files")
    valid_files = []
    invalid_files = []
    for file in uploaded_files:
        if file.filename == "":
            continue
        if not file.content_type.startswith("image/"):
            invalid_files.append(file.filename)
        else:
            valid_files.append(file.filename)
            file.save(f"{loaded_images_temporary_storage_path}/{file.filename}")
    if not len(valid_files) and not len(invalid_files):
        flash("Aucun fichier séléctionné", "Attention !")
    elif len(invalid_files):
        flash(f"Les fichiers suivants : {', '.join(invalid_files)} n'ont "
              "pas été chargés car ce ne sont pas des images.",
              f"({len(valid_files)}/{len(valid_files) + len(invalid_files)}) "
              "fichier(s) chargé(s)")
    else:
        flash("Tous les fichiers séléctionnés ont été chargés.",
              f"({len(valid_files)}/{len(valid_files) + len(invalid_files)}) "
              "fichier(s) chargé(s)")

    # file.content_type
    # TODO : Call processing function

    # TODO : Store images

    # TODO : Remove processed images from tmp repository

    return render_template('add_images.html')