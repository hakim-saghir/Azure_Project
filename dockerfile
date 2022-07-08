FROM ubuntu:22.04
WORKDIR /azure_project
COPY Azure_Project/ .
RUN apt -y update
RUN apt install -y python3-pip
RUN pip3 install -r  requirements.txt
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=52800
ENV FLASK_APP=web_app
ENV DATABASE_HOST=azure-mysql-projet.mysql.database.azure.com
ENV DATABASE_PORT=3306
ENV DATABASE_NAME=azure_project_db
ENV DATABASE_USER=azure
ENV DATABASE_PASSWORD=Projet-admin
ENV STORAGE_LINK=csb10032000e07f0bc1
ENV AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=csb10032000e07f0bc1;AccountKey=505FvWV+4RieYdWii+4GoSoXeM246GNrwnWuwAqMStepKXeIgoec4E+EW1vN1x7y6uJO0dklPHhY2cJXNUobbw==;EndpointSuffix=core.windows.net
ENV END_POINT_VISION=https://azureprojectcomputervision.cognitiveservices.azure.com/
ENV KEY_VISION=b55a82921ead4d62912806d40e9560ad
ENTRYPOINT ["flask", "run"]
EXPOSE 52800