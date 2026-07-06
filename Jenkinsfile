
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'pwd'
                sh 'ls -la'
                sh 'echo "Current branch: ${BRANCH_NAME}"'
            }
        }
    }
}
