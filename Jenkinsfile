
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
                sh 'echo "✅ Checkout complete"'
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'echo "🔨 Building backend..."'
                    sh 'docker build -t ${BACKEND_IMAGE}:latest .'
                    sh 'docker run --rm ${BACKEND_IMAGE}:latest python -c "print(\"Backend works!\")"'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'echo "🔨 Building frontend..."'
                    sh 'docker build -t ${FRONTEND_IMAGE}:latest .'
                    sh 'docker run --rm ${FRONTEND_IMAGE}:latest ls -la /usr/share/nginx/html'
                }
            }
        }
        
        stage('List Images') {
            steps {
                sh 'echo "📦 Docker Images:"'
                sh 'docker images | grep todo'
            }
        }
    }
}

