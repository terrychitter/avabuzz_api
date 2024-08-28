# Flask Application

This is a Flask-based web application with a structured project layout. The application includes API endpoints, database models, and various utilities to support its functionality.

## Table of Contents

- [Flask Application](#flask-application)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory and add the necessary environment variables. Refer to the `Config` class in [`config.py`](config.py) for required variables.

    ```env
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URI=your_database_uri
    ```

5. **Run the database migrations:**

    ```sh
    flask db upgrade
    ```

## Configuration

The application configuration is managed through the [`Config`](config.py) class. Environment variables are loaded from a `.env` file using `python-dotenv`.

## Usage

1. **Run the application:**

    ```sh
    flask run
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000`.
