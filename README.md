# Project Overview

This project consists of multiple microservices, right now only authentication service (`auth-service`) is implemented. Each microservice is responsible for handling specific operations and is built using the FastAPI web framework in Python.

## Directory Structure

The project directory structure is as follows:

```plaintext
/music-microservice-backend
|-- auth-service
|-- music-service       -> [WIP]
|-- user-service        -> [WIP]
|-- generate-service-template.sh
|-- README.md
```

## Running the Project

### Prerequisites

- Python 3.9 or later
- Docker

### Setting Up the Environment

1. **Clone the repository:** Clone the repository to your local machine.

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up environment variables:** Set the necessary environment variables in the shell.
3. **Navigate to required service directory:**

    ```sh
    cd <service-directory>
    ```

4. **Create a virtual environment:**

    ```sh
    python -m venv venv-<service-name>
    source venv-<service-name>/bin/activate
    ```

5. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

### Running the Services for Development

1. Navigate to the src directory inside the service directory:

    ```sh
    cd src
    ```

2. Run the service:

    ```sh
    uvicorn <serivce_name>.main:app --reload
    ```

3. The service will be running on `http://localhost:8000`.

### Creating a New Service

Use the `create_service.sh` script to create a new microservice:
  
  ```sh
  . generate-service-template.sh <service-name>
  ```

This script will generate the necessary directory structure and files for the new microservice.
