import os
from flask import blueprints, render_template, request, flash, redirect
from web_app import loaded_images_temporary_storage_path
from .utils.utils_func import get_image_tags, upload_image, save_image_information_in_database, \
    get_image_caption, get_all_images, get_images_from_string, get_tags_image_sql, delete_image_and_its_tags

routes = blueprints.Blueprint("routes", "routes")


@routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@routes.route('/add_images', methods=['GET'])
def add_images():
    return render_template('add_images.html')


@routes.route('/upload_images', methods=['POST'])
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
    for image in os.listdir(loaded_images_temporary_storage_path):
        # Store image
        if upload_image("image", f"{loaded_images_temporary_storage_path}/{image}", image):
            # Get image tags
            tags = get_image_tags(f"{loaded_images_temporary_storage_path}/{image}", end_point=os.environ["END_POINT_VISION"], key=os.environ["KEY_VISION"])
            if not len(tags.keys()):
                continue
            # Get image caption
            caption = get_image_caption(f"{loaded_images_temporary_storage_path}/{image}",
                                        end_point=os.environ["END_POINT_VISION"], key=os.environ["KEY_VISION"])
            description = ""
            if len(caption.keys()):
                description = list(caption.keys())[0]
                # Save image information in the database
            save_image_information_in_database(image, description, 'image', tags)
        # Remove image
        os.remove(f"{loaded_images_temporary_storage_path}/{image}")
    return render_template('add_images.html')


@routes.route('/get_images', methods=['GET'])
def get_images():
    data = get_all_images()
    for index, row in enumerate(data):
        tags = get_tags_image_sql(row['name'])
        tags = ", ".join(tags)
        data[index]['url'] = str(data[index]['url']).replace("https//", "https://")
        data[index]['tags'] = tags
    return render_template('get_images.html', data=data)


@routes.route('/get_images/search', methods=['POST'])
def get_images_by_searching():
    if request.form["search"] == "":
        return render_template('index.html')
    data = get_images_from_string(request.form['search'])
    for index, row in enumerate(data):
        tags = get_tags_image_sql(row['name'])
        tags = ", ".join(tags)
        data[index]['tags'] = tags
    return render_template('get_images.html', data=data)


@routes.route('/delete', methods=['GET'])
def delete_image_by_id():
    if "id" not in request.args.keys() or request.args["id"] == "":
        return render_template('get_images.html')
    delete_image_and_its_tags(request.args["id"])
    # flash(f"L'image avec {request.args['id']} a été supprimée de la base de données et de son contenair", "Terminé")
    return redirect("/get_images")
