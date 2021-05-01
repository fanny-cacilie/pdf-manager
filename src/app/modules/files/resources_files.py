from flask import request
from flask_restful import Resource

from marshmallow import ValidationError

from app.libs.strings import gettext
from app.modules.files.models_files import FileModel
from app.modules.files.schema_files import FileSchema


file_schema = FileSchema()
file_list_schema = FileSchema(many=True)


class Files(Resource):
    @classmethod
    def get(cls):
        """
        Retrieve all files stored in database.
        """
        try:
            files = file_list_schema.dump(FileModel.find_all())
        
        except Exception as err:
            raise err
        
        return {"files": files}, 200
        
    @classmethod
    def post(cls):
        """
        Upload and store a file in database.
        """
        try:
            file = request.files["inputFile"]

            new_file = FileModel(name=file.filename, uploaded_file=file.read())

            if FileModel.find_by_name(new_file.name):
                return {"message": gettext("file_name_exists")}, 400

            new_file.save_to_db()
            
        except Exception as err:
            raise err

        return {"message": gettext("file_uploaded")}, 201


class File(Resource):
    @classmethod
    def get(cls, file_id):
        """
        Retrieve a file stored in database by its ID.
        """
        try:
            file = FileModel.find_by_id(file_id)
            if file:
                return file_schema.dump(file), 200
            return {"message": gettext("file_not_found")}, 404
        
        except Exception as err:
            raise err


    @classmethod
    def put(cls, file_id):
        """
        Update and save a file name by its ID.
        """
        try:
            file_json = request.get_json()
            file = FileModel.find_by_id(file_id)

            if file:
                file.name = file_json["name"]
            else:
                return {"message": gettext("file_not_found")}, 404

            file.save_to_db()

        except Exception as err:
            raise err

        return file_schema.dump(file), 200


    @classmethod
    def delete(cls, file_id):
        """
        Delete a file by its ID.
        """
        try:
            file = FileModel.find_by_id(file_id)
            if file:
                file.delete_from_db()
                return {"message": gettext("file_deleted")}, 200
            return {"message": gettext("file_not_found")}, 404
        
        except Exception as err:
            raise err


