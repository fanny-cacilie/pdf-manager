from ma import MA
from app.modules.files.models_files import FileModel


class FileSchema(MA.SQLAlchemyAutoSchema):
    class Meta:
        model = FileModel
        # load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
