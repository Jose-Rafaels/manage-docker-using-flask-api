# Flask Docker Manager

This Flask application provides a web interface and API endpoints to manage Docker containers. It includes features like user authentication, container listing, and container control (start, stop, restart).

## Features

- User authentication with Flask-Login
- Docker container management (list, start, stop, restart)
- Rate limiting for login attempts
- API documentation

## Requirements

- Python 3.10
- Docker

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/flask-docker-manager.git
   cd flask-docker-manager
   ```

2. Create and activate a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:

   ```sh
   python app.py
   ```

   The application will be available at `http://localhost:5050`.

## Usage

### Login

Open the browser and go to `http://localhost:5050/login`. Enter the username and password. Default credentials are:

- **Username:** `your-username`
- **Password:** `your-password`

### API Endpoints

#### List Containers

- **Endpoint:** `/containers`
- **Method:** `GET`
- **Description:** List all Docker containers.

  ```sh
  curl http://localhost:5050/containers
  ```

#### Start Container

- **Endpoint:** `/containers/<name>/start`
- **Method:** `GET`
- **Description:** Start a Docker container by name.

  ```sh
  curl http://localhost:5050/containers/<name>/start
  ```

#### Stop Container

- **Endpoint:** `/containers/<name>/stop`
- **Method:** `GET`
- **Description:** Stop a Docker container by name.

  ```sh
  curl http://localhost:5050/containers/<name>/stop
  ```

#### Restart Container

- **Endpoint:** `/containers/<name>/restart`
- **Method:** `GET`
- **Description:** Restart a Docker container by name.

  ```sh
  curl http://localhost:5050/containers/<name>/restart
  ```

### API Documentation

Open the browser and go to `http://localhost:5050/docs` to view the API documentation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
