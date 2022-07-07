import configparser
import logging
import os
import pymysql
from pymysql.cursors import DictCursor


def connect_database():
    """ Database connection
    """
    config = configparser.ConfigParser()
    config.read("application.properties")
    database_cert_path = config.get("application_parameters", "DATABASE_CERT_PATH")
    try:
        connection = pymysql.connect(host=os.environ["DATABASE_HOST"],
                                     port=3306,
                                     database=os.environ["DATABASE_NAME"],
                                     user=os.environ["DATABASE_USER"],
                                     password=os.environ["DATABASE_PASSWORD"],
                                     ssl={"ca": database_cert_path},
                                     ssl_disabled=False,
                                     autocommit=True,
                                     cursorclass=DictCursor)
        return connection
    except Exception as e:
        logging.debug(f"Database connection failed, error code : {e}")
        return None


def execute_request(connection: pymysql.connections.Connection,
                    sql_request: str,
                    parameters_tuple: tuple = None) -> (int, pymysql.cursors):
    """ Execute the request in parameters
    :param
        connection: connection to use
        parameters_tuple: parameters (tuple)
    :return
        (result count, result lines) or (-1, None) if error
    """
    try:
        cursor = connection.cursor()
        result_count = cursor.execute(sql_request, parameters_tuple)
        return result_count, cursor.fetchall()
    except Exception as e:
        logging.error(f"execute_request : Database operation failed, error code : {e}")
        return -1, None
