from .flask_app import FlaskApp

# Default class instance to allow simple calls like PyO.run()
_app = FlaskApp()

# User-facing functions
def html(file_path):
    _app.html_file_path = file_path

def dependency(file_path):
    _app.requirements_file_path = file_path

def run():
    _app.run()

# Allow PyO() syntax for direct initialization
def PyO(html_file="index.html", requirements_file="requirements.txt"):
    html(html_file)
    dependency(requirements_file)
    run()
