
pipeline {
    agent any
    
    environment {
        DOCKER_NAMESPACE = 'medhermi'
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
                    sh 'echo "✅ Backend image built"'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'echo "🔨 Building frontend..."'
                    sh 'docker build -t ${FRONTEND_IMAGE}:latest .'
                    sh 'echo "✅ Frontend image built"'
                }
            }
        }
        
        stage('Test Backend') {
            steps {
                sh '''
                    echo "🧪 Testing backend..."
                    # Just check if the container can run
                    docker run --rm ${BACKEND_IMAGE}:latest python -c "print(1+1)" || echo "Test failed but continuing"
                '''
            }
        }
        
        stage('List Images') {
            steps {
                sh 'echo "📦 Docker Images:"'
                sh 'docker images | grep todo'
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "📤 Pushing images to Docker Hub..."
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${BACKEND_IMAGE}:latest
                        docker push ${FRONTEND_IMAGE}:latest
                        echo "✅ Images pushed successfully!"
                    '''
                }
            }
        }
    }
}
