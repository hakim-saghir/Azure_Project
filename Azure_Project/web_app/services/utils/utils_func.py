import html
import logging
import os
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision  import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
from web_app.services.utils.db_interactions import connect_database, execute_request
from web_app.services.utils.sql_requests import CHECK_IF_TAG_EXIST, INSERT_NEW_TAG, INSERT_NEW_IMAGE, INSERT_LINK, \
    GET_IMAGES_BY_TAGS, \
    GET_IMAGE_TAGS, GET_ALL_IMAGES


def check_if_file_is_an_image(image_fullpath: str) -> bool:
    try:
        Image.open(image_fullpath)
    except IOError:
        logging.error(f"upload_image : {image_fullpath} is not a valid image")
        return False
    return True


def check_if_blob_exist_in_container(container_name: str, blob_name: str) -> bool:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Instantiate a ContainerClient
    blob_service_client.get_container_client(container_name)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    # Check if bloc already exist
    if blob_client.exists():
        logging.debug(f"upload_image : {blob_name} already exist in container")
        return False
    return True


def upload_image(container_name: str, image_fullpath: str, image_name: str) -> bool:
    """
    Check that the specified image is a valid image and that the image_name does
    not already exist in the container and if so, load the image into the container
    :param container_name:
    :param image_fullpath:
    :param image_name:
    :return: True if the operation was successful else False
    """
    if not check_if_file_is_an_image(image_fullpath):
        return False
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Instantiate a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)
        # If container doesn't exist, create it
        if not container_client.exists():
            blob_service_client.create_container(container_name)
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name)
        # Check if bloc already exist
        if blob_client.exists():
            logging.debug(f"upload_image : {image_name} already exist in container")
            return False
        # Upload the image
        with open(image_fullpath, "rb") as data:
            blob_client.upload_blob(data)
        logging.debug(f"upload_image : {image_fullpath} uploaded")
    except Exception:
        logging.error("upload_image : error while uploading image,"
                      "please check your inputs and your credentials")
        return False
    return True


def delete_uploaded_image(container_name: str, images_name: list[str]):
    """
    Remove existing blobs in specified container
    :param container_name:
    :param images_name:
    :return: True if the operation was successful else False
    """
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Instantiate a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)
        # If container doesn't exist, create it
        if not container_client.exists():
            logging.error("delete_uploaded_image : error while deleting images, "
                          "container doesn't exist")
            return False
        # Create a blob client using the local file name as the name for the blob
        # Check if blobs exist else do not delete them
        images_name_copy = images_name.copy()
        for image_name in images_name_copy:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name)
            if not blob_client.exists():
                images_name.remove(image_name)
        if len(images_name):
            container_client.delete_blobs(*images_name)
    except Exception:
        logging.error("delete_uploaded_image : error while deleting "
                      "images, please check your inputs")
        return False
    return True


def get_container_blobs_names(container_name: str) -> list[str]:
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Instantiate a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)
    except Exception:
        logging.error("get_container_blobs_name : error while getting "
                      f"container : {container_name} blobs names list")
        return []
    # List the blobs in the container
    return container_client.list_blobs()


def download_blob_from_container(container_name: str, download_path: str, download_name: str, blob) -> bool:
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Instantiate a ContainerClient
        blob_client = blob_service_client.get_container_client(container=container_name)
        download_file_path = os.path.join(download_path, download_name)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob(blob).readall())
    except Exception:
        logging.error("download_blob_from_container : error while downloading blob, "
                      "please check your inputs")
        return False
    return True


def check_if_tag_exist(tag: str) -> bool:
    tag = html.escape(tag)
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, CHECK_IF_TAG_EXIST, tag)
        connection.close()
        if result_count:
            return True
        return False
    return None


def insert_new_tag_if_not_exist(tag: str) -> bool:
    if check_if_tag_exist(tag):
        return True
    tag = html.escape(tag)
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, INSERT_NEW_TAG, tag)
        connection.close()
        if result_count:
            return True
        return False
    return None


def insert_link_image_tag(image_id: str, tag:str) -> bool:
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, INSERT_LINK, (image_id, tag))
        connection.close()
        if result_count:
            return True
        return False
    return None


def save_image_information_in_database(name, description, container, tags):
    for tag in tags:
        insert_new_tag_if_not_exist(tag)
    connection = connect_database()
    if connection:
        url = f"https://{os.getenv('STORAGE_LINK')}.blob.core.windows.net/{container}/{name}"
        result_count, result = execute_request(connection, INSERT_NEW_IMAGE, (name, description, container, url))
        connection.close()
        if result_count:
            image_id = str(connection.insert_id())
            for tag in tags:
                insert_link_image_tag(image_id, tag)
            return True
        return False
    return None


def get_image_tags(image_path, end_point, key):
    features = ['Description', 'Tags', 'Adult', 'Objects', 'Faces']
    computer_vision_client = ComputerVisionClient(end_point, CognitiveServicesCredentials(key))
    image_stream = open(image_path, "rb")
    result = computer_vision_client.analyze_image_in_stream(image_stream, visual_features=features)
    dico = {}
    for i in result.tags:
        dico[i.name] = i.confidence
    return dico


def get_image_caption(image_path, end_point, key):
    features = ['Description']
    computer_vision_client = ComputerVisionClient(end_point, CognitiveServicesCredentials(key))
    image_stream = open(image_path, "rb")
    result = computer_vision_client.analyze_image_in_stream(image_stream, visual_features=features)
    dico = {}
    if len(result.description.captions) == 0:
        return {}
    for i in result.description.captions:
        dico[i.text] = i.confidence
    return dico


def get_tags_image_sql(image):
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, GET_IMAGE_TAGS, image)
        connection.close()
        if result_count:
            tags = []
            for row in result:
                tags.append(row['tag'])
            return tags
        return []
    return None


def get_images_from_string(sentence: str):
    tags_array = sentence.split(' ')
    if not len(tags_array):
        return []
    tags_string_for_sql = tuple(tags_array)
    s_for_sql = ', '.join(["%s" for tag in tags_array])
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, GET_IMAGES_BY_TAGS
                                               .format(s_for_sql, s_for_sql), (tags_string_for_sql, tags_string_for_sql))
        connection.close()
        if result_count:
            return result
    return []


def get_all_images():
    connection = connect_database()
    if connection:
        result_count, result = execute_request(connection, GET_ALL_IMAGES)
        connection.close()
        if result_count:
            return result
    return []
