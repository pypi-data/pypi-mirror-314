import os
import shutil
import sys
from pathlib import Path


class UploadToPypi:
    def __init__(self, project_dir: str | Path, username: str = '__token__', passwd: str = None,
                 upload_to_pypi_test: bool = False, emit_tips: bool = True, python_path: str = None):
        self.project_dir = Path(project_dir).resolve()
        self.username = username
        self.passwd = passwd
        self.upload_to_pypi_test = upload_to_pypi_test
        self.emit_tips = emit_tips
        self.python_path = python_path or sys.executable

        os.chdir(self.project_dir)

    def build(self):
        try:
            shutil.rmtree(self.project_dir / 'dist')    # delete all old dist versions
        except FileNotFoundError:
            if self.emit_tips:
                print(f"Dist doesn't exist or failed to delete.")
        os.system(f'{self.python_path} -m build')

    def upload(self):
        command = f'{self.python_path} -m twine upload dist/* -u {self.username} -p {self.passwd}'
        if self.upload_to_pypi_test:
            command += ' --repository testpypi'
        os.system(command)

    def build_and_upload(self):
        self.build()
        self.upload()
