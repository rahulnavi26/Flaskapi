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

    stage('Debug Workspace') {
        steps {
            echo 'Checking workspace contents...'
            sh '''
            pwd
            ls -la
            find . -name "*.py"
            '''
        }
    }

    stage('Install Dependencies') {
        steps {
            echo 'Setting up Python virtual environment and installing packages...'
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
            sh '''
            export PYTHONPATH=$WORKSPACE
            ./venv/bin/pytest \
            --cov=app \
            --cov-report=xml \
            --cov-report=term \
            --junitxml=test-results.xml \
            tests/
            '''
        }
        post {
            always {
                junit 'test-results.xml'
            }
        }
    }

    stage('Docker Build & Tag') {
        steps {
            echo 'Building Docker image...'
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
