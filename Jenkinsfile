
pipeline {
    agent any
    
    environment {
        DOCKER_NAMESPACE = 'hermimoh'
        BACKEND_IMAGE = "${DOCKER_NAMESPACE}/todo-backend"
        FRONTEND_IMAGE = "${DOCKER_NAMESPACE}/todo-frontend"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "=== Environment Variables ==="'
                sh 'echo "DOCKER_NAMESPACE: ${DOCKER_NAMESPACE}"'
                sh 'echo "BACKEND_IMAGE: ${BACKEND_IMAGE}"'
                sh 'echo "FRONTEND_IMAGE: ${FRONTEND_IMAGE}"'
                sh 'ls -la'
            }
        }
    }
}


