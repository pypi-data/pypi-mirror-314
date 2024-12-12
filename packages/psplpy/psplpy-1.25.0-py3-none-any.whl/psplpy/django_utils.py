import os
import re
import django
from django.conf import settings
from django.db import models, connections
from psplpy.image_det import TxtProc
from pathlib import Path


class DbBackend:
    SQLITE3 = 'django.db.backends.sqlite3'
    POSTGRESQL = 'django.db.backends.postgresql'
    MYSQL = 'django.db.backends.mysql'


class Database:
    def __init__(self, engine: str = DbBackend.SQLITE3, name=None, user=None, password=None,
                 host='localhost', port=None, app_label: str = '', **django_settings):
        databases = {
            'default': {
                'ENGINE': engine,
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
                'APP_LABEL': app_label,
            }
        }

        # Update the settings with the custom DATABASES dictionary
        settings_dict = {'DATABASES': databases}
        settings_dict.update(django_settings)
        settings.configure(**settings_dict)
        # Initialize Django
        django.setup()

        # Create the custom base model
        class CustomBaseModel(models.Model):
            class Meta:
                app_label = databases['default']['APP_LABEL']
                abstract = True

            @classmethod
            def init(cls, new_name=None) -> None:
                Database.change_table_name(cls, new_name)
                Database.create_table(cls)
                Database.update_table(cls)

        self.Model = CustomBaseModel

    @staticmethod
    def change_table_name(model, new_name=None) -> None:
        if new_name is None:
            new_name = TxtProc.camel_to_snake(model.__name__)
        model._meta.db_table = new_name

    @staticmethod
    # Create a table if it doesn't exist
    def create_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                schema_editor.create_model(model)

    @staticmethod
    # Update table if you added fields (doesn't drop fields as far as i know, which i was too afraid to implement)
    def update_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                raise ValueError(f'Table "{model._meta.db_table}" not found.')
            else:
                # Get the database columns
                database_columns = connections['default'].introspection.get_table_description(
                    connections['default'].cursor(), model._meta.db_table)
                database_column_names = [column.name for column in database_columns]
                # Check if each field in the model exists in the database table
                for field in model._meta.fields:
                    if field.column not in database_column_names:
                        # Add the new column to the table
                        schema_editor.add_field(model, field)


class DjangoInit:
    def __init__(self, project_dir: str | Path = None, database: str = None):
        self.project_dir = Path(project_dir) if project_dir else os.getcwd()
        self.database = database
        self.manage_py_path = self._find_manage_py()
        self.project_name = self._extract_project_name()
        self.settings_py_path = self.project_dir / self.project_name / 'settings.py'
        self.settings_str = self.settings_py_path.read_text(encoding='utf-8')

    def _find_manage_py(self) -> Path:
        manage_py_path = self.project_dir / 'manage.py'
        if manage_py_path.exists():
            return manage_py_path
        raise FileNotFoundError(f'manage.py not found at {manage_py_path}')

    def _extract_project_name(self) -> str:
        content = self.manage_py_path.read_text(encoding='utf-8')
        match = re.search(r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '([^']+)'\)", content)
        if match:
            return match.group(1).split('.')[0]
        raise ValueError("Cannot extract project name from manage.py")

    def _mkdir(self, dir_path: Path) -> None:
        if dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f'Make dir: {dir_path}')

    def _replace_settings(self, old: str, new: str) -> None:
        if old in self.settings_str:
            self.settings_str = self.settings_str.replace(old, new)
            print(f'Change: {old}')
            print(f'To: {new}')

    def _replace_file(self, file_path: Path, old: str, new: str) -> None:
        if not file_path.exists():
            raise ValueError(f'File does not exist: {file_path}')
        content = file_path.read_text(encoding='utf-8')
        if old in content:
            file_path.write_text(content.replace(old, new), encoding='utf-8')
            print(f'Change: {old}')
            print(f'To: {new}')

    def _set_asgi(self):
        new = f"""'django.contrib.staticfiles',
            'channels',
        ]

        ASGI_APPLICATION = '{self.project_name}.asgi.application'

        CHANNEL_LAYERS = {{
            'default': {{
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {{
                    "hosts": [(get_env('REDIS_HOST'), get_env('REDIS_PORT'))],
                }},
            }},
        }}"""
        self._replace_settings("'django.contrib.staticfiles',\n]", new)
        old = f"""\nfrom django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')

application = get_asgi_application()"""
        new = f"""from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings')

application = ProtocolTypeRouter({{
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
}})
"""
        self._replace_file(self.project_dir / self.project_name / 'asgi.py', old, new)

    def init(self) -> None:
        # make global templates dir
        self._mkdir(self.project_dir / 'templates')
        self._replace_settings("'DIRS': [],", "'DIRS': [BASE_DIR / 'templates'],")
        # make global static dir
        self._mkdir(self.project_dir / 'static')
        new = "STATIC_URL = 'static/'\nSTATICFILES_DIRS = [BASE_DIR / 'static',]"
        self._replace_settings("STATIC_URL = 'static/'", new)
        # modify allowed hosts
        self._replace_settings("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")
        # set_asgi
        self._set_asgi()
        # set database
        if self.database and self.database != DbBackend.SQLITE3:
            db_setting = f"""DATABASES = {{
    'default': {{
        'ENGINE': '{self.database}',
        'NAME': get_env("DB_NAME"),
        'USER': get_env("DB_USER"),
        'PASSWORD': get_env("DB_PASSWORD"),
        'HOST': get_env("DB_HOST"),
        'PORT': get_env("DB_PORT"),
    }}
}}"""
            old = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
            self._replace_settings(old, db_setting)
            old = ("from pathlib import Path\n\n"
                   "# Build paths inside the project like this: BASE_DIR / 'subdir'.")
            new = ('from pathlib import Path\n'
                   'from psplpy.other_utils import get_env\n'
                   'get_env.env_file = Path(__file__).resolve().parent.parent.parent / ".env"\n\n'
                   "# Build paths inside the project like this: BASE_DIR / 'subdir'.")
            self._replace_settings(old, new)
        # write settings
        self.settings_py_path.write_text(self.settings_str, encoding='utf-8')
