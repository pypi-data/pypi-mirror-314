import os
import subprocess
from flask import Flask, render_template_string

class FlaskApp:
    def __init__(self):
        self.html_file_path = "index.html"  # Default HTML file
        self.requirements_file_path = "requirements.txt"  # Default dependencies file
        self.app = Flask(__name__)

        # Define the route for the Flask app
        @self.app.route("/")
        def home():
            html_content = self.load_html_content()
            return render_template_string(html_content)
        

    def load_html_content(self):
        """Load HTML content from the specified file."""
        try:
            with open(self.html_file_path, "r", encoding="utf-8") as html_file:
                return html_file.read()
        except FileNotFoundError:
            return "<h1>Error: HTML file not found.</h1>"
        
    def html(self, path):
        """Set a custom path for the HTML file."""
        self.html_file_path = path
        return self.html_file_path

    def dependency(self, path):
        """Set a custom path for the requirements file."""
        self.requirements_file_path = path
        return self.requirements_file_path

    def install_dependencies(self):
        """Install dependencies listed in the specified requirements file."""
        try:
            if os.path.exists(self.requirements_file_path):
                with open(self.requirements_file_path, "r", encoding="utf-8") as file:
                    dependencies = file.read().splitlines()

                for dependency in dependencies:
                    subprocess.check_call(["pip", "install", dependency])
                print("All dependencies installed successfully!")
            else:
                print(f"Error: {self.requirements_file_path} not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing a package: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        """Install dependencies and start the Flask app."""
        self.install_dependencies()
        self.load_html_content()
        self.app.run(debug=True, host="0.0.0.0", port=5000)
