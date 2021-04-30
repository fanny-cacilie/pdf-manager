import json

from app.modules.files.models_files import FileModel
from app.tests.base_test import BaseTest


class FileTest(BaseTest):
    def setUp(self):
        super(FileTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/upload",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "name": "file.pdf",
                            "uploaded_file": "1598903175_file.pdf",
                        }
                    ),
                )

    def test_upload_file(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    "/upload",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "name": "file.pdf",
                            "uploaded_file": "1598903175_file.pdf",
                        }
                    ),
                )

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(FileModel.find_by_filename("fcs"))


    def test_get_file(self):
        with self.app() as client:
            with self.app_context():

                token = self.access_token

                response = client.get(
                    "/file/1",
                    headers={
                        "Content-Type": "application/json",
                    },
                )
                self.assertEqual(response.status_code, 200)

                
    def test_upload_duplicate_file(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/upload",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "name": "file.pdf",
                            "uploaded_file": "1598903175_file.pdf",
                        }
                    ),
                )

                response = client.post(
                    "/upload",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "name": "file.pdf",
                            "uploaded_file": "1598903175_file.pdf",,
                        }
                    ),
                )

                self.assertEqual(response.status_code, 400)
