pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-api-demo'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing packages...'
                // Create virtualenv and install dependencies
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests with pytest...'
                // Run pytest, outputting junit XML and test coverage reports
                sh './venv/bin/pytest --cov=app --cov-report=xml --cov-report=term --junitxml=test-results.xml tests/'
            }
            post {
                always {
                    // Archive test results in Jenkins
                    junit 'test-results.xml'
                }
            }
        }

        stage('Docker Build & Tag') {
            steps {
                echo 'Building production Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline succeeded. Built Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "CI/CD Pipeline failed. Check build logs for details."
        }
    }
}
