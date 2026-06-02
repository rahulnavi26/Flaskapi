# Flask API Starter Project

A production-ready, containerized Python Flask API project complete with health checks, unit tests, custom error handlers, and a Jenkins CI/CD pipeline.

## Project Structure

```text
├── app.py              # Main Flask application with API endpoints
├── requirements.txt    # Python package dependencies
├── Dockerfile          # Multi-stage production-ready Dockerfile
├── Jenkinsfile         # Declarative Jenkins CI/CD pipeline
├── tests/
│   └── test_app.py     # Automated unit tests using pytest
└── README.md           # Setup and running instructions
```

---

## 1. Running Locally (in Terminal)

To run this application locally on your host machine:

### Step A: Set up a Python Virtual Environment
Creating a virtual environment ensures dependencies do not conflict with system-wide python packages.

**On Windows (PowerShell/CMD):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step B: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step C: Run the Flask Server
By default, the application runs on port `5000`. You can configure the port using the `PORT` environment variable.

```bash
python app.py
```

### Step D: Test the API Endpoints
You can now access the endpoints in your browser, or via tools like `curl` or Postman:

- **Welcome Info:** `http://localhost:5000/`
- **Health Check:** `http://localhost:5000/health`
- **Get Tasks List:** `http://localhost:5000/api/tasks`
- **Get Specific Task:** `http://localhost:5000/api/tasks/1`
- **Create a Task (POST):**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Demonstrating POST request"}' http://localhost:5000/api/tasks
  ```

---

## 2. Running Automated Tests

We use `pytest` for unit testing. Make sure your virtual environment is active.

### Run Tests:
To avoid `ModuleNotFoundError` issues with imports, run pytest via the python module interface:
```bash
python -m pytest
```

### Run Tests with Coverage Report:
```bash
python -m pytest --cov=app --cov-report=term
```

---

## 3. Running with Docker

This project includes a multi-stage Dockerfile that builds the application securely under a non-root user.

### Step A: Build the Docker Image
```bash
docker build -t flask-api-demo .
```

### Step B: Run the Docker Container
Map container port `5000` to host port `5000`:
```bash
docker run -d -p 5000:5000 --name my-flask-app flask-api-demo
```

### Step C: Verify Running Container
Check the status of the container:
```bash
docker ps
```
Or check the logs:
```bash
docker logs my-flask-app
```

---

## 4. Running with Jenkins

The provided `Jenkinsfile` outlines a declarative pipeline matching modern CI/CD practices.

### Stages:
1. **Checkout**: Pulls the repository code.
2. **Install Dependencies**: Creates a virtual environment and installs packages in `requirements.txt`.
3. **Run Tests**: Runs `pytest` and generates a JUnit XML file containing the test reports.
4. **Docker Build & Tag**: Builds the production Docker image and tags it as `latest` and `build-${BUILD_NUMBER}`.

### Setup in Jenkins:
1. Create a new job in Jenkins and select **Pipeline**.
2. Under **Pipeline Definition**, select **Pipeline script from SCM**.
3. Choose **Git** and input your repository URL.
4. Set the **Script Path** to `Jenkinsfile` and save.
5. Click **Build Now** to execute the pipeline.
