
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
                sh 'echo "Checking out code..."'
                sh 'ls -la'
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'echo "=== Building Backend ==="'
                    sh 'pwd'
                    sh 'ls -la'
                    sh '''
                        echo "Building Docker image..."
                        docker build -t ${BACKEND_IMAGE}:latest .
                        docker images | grep todo-backend || echo "No images found"
                    '''
                }
            }
        }
    }
}

