from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Zippy Form: Generate Celery setup script in the project root directory.'

    def handle(self, *args, **options):
        # Get the project name from the Django settings
        project_name = settings.SETTINGS_MODULE.split('.')[0]

        # Define the content of the Python script
        script_content = f"""import os
import django
from celery import Celery
from dotenv import load_dotenv

project_name = '{project_name}'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_name + '.settings')
django.setup()

app = Celery(project_name, include=['zippy_form.celery_tasks'])
load_dotenv()

try:
    is_webhook_enabled = os.getenv('ZF_ENABLE_WEBHOOK')
    broker_url = os.getenv('ZF_WEBHOOK_BROKER_URL')
    result_backend = os.getenv('ZF_WEBHOOK_BACKEND')

    if is_webhook_enabled:
        app.conf.broker_url = broker_url
        app.conf.result_backend = result_backend

        app.conf.broker_connection_retry_on_startup = True
        app.autodiscover_tasks()

        if __name__ == '__main__':
            app.worker_main(argv=['worker', '--loglevel=info', '--logfile=celery.log'])
except Exception as e:
    print("Celery Setup Error: " + str(e))
"""

        # Specify the file name and path where the script will be created
        file_name = 'celery_init.py'

        # Create the Python script file with the specified content
        with open(file_name, 'w') as script_file:
            script_file.write(script_content)

        self.stdout.write(self.style.SUCCESS(
            f'Zippy Form: Python script "{file_name}" created with Celery setup for project: {project_name}.'))
