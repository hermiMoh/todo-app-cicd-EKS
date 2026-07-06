
pipeline {
    agent any
    
    tools {
        // Specify tools if not using Docker
        // maven 'Maven-3.9'
        // jdk 'JDK-17'
    }
    
    environment {
        // GitHub Configuration
        GITHUB_REPO = 'https://github.com/hermiMoh/todo-app-cicd-EKS.git'
        GITHUB_CREDENTIALS_ID = 'github-credentials'
        
        // Docker Configuration
        DOCKER_REGISTRY = 'docker.io'  // or your registry URL
        DOCKER_NAMESPACE = 'medhermi'  // Replace with your Docker Hub username
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        
        // Application Configuration
        APP_NAME = 'todo-app'
        BACKEND_IMAGE = "${DOCKER_NAMESPACE}/${APP_NAME}-backend"
        FRONTEND_IMAGE = "${DOCKER_NAMESPACE}/${APP_NAME}-frontend"
        
        // Version Configuration
        VERSION_FILE = 'version.txt'
        MAJOR_VERSION = '1'
        MINOR_VERSION = '0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: env.GITHUB_CREDENTIALS_ID,
                        url: env.GITHUB_REPO
                    ]]
                ])
            }
        }
        
        stage('Increment Version') {
            steps {
                script {
                    // Read current version
                    def versionFile = readFile(VERSION_FILE).trim()
                    def versionParts = versionFile.split('\\.')
                    def patch = versionParts[2].toInteger() + 1
                    def newVersion = "${versionParts[0]}.${versionParts[1]}.${patch}"
                    
                    // Set environment variable
                    env.APP_VERSION = newVersion
                    
                    // Update version file
                    writeFile file: VERSION_FILE, text: newVersion
                    
                    // Display version
                    echo "New Version: ${env.APP_VERSION}"
                    
                    // Also set timestamp for tag
                    env.BUILD_TIMESTAMP = new Date().format('yyyyMMddHHmmss')
                }
            }
        }
        
        stage('Backend Build & Test') {
            steps {
                dir('backend') {
                    script {
                        // Run tests
                        sh '''
                            python3 -m venv venv
                            source venv/bin/activate
                            pip install -r requirements.txt
                            pip install pytest pytest-cov
                            pytest -v --cov=. || true
                        '''
                        
                        // Build Docker image
                        docker.build("${env.BACKEND_IMAGE}:${env.APP_VERSION}")
                        docker.build("${env.BACKEND_IMAGE}:latest")
                    }
                }
            }
        }
        
        stage('Frontend Build & Test') {
            steps {
                dir('frontend') {
                    script {
                        // Run tests (if you have them)
                        sh '''
                            npm install
                            npm test || true
                        '''
                        
                        // Build Docker image
                        docker.build("${env.FRONTEND_IMAGE}:${env.APP_VERSION}")
                        docker.build("${env.FRONTEND_IMAGE}:latest")
                    }
                }
            }
        }
        
        stage('Push Docker Images') {
            steps {
                script {
                    // Login to Docker registry
                    docker.withRegistry("https://${env.DOCKER_REGISTRY}", env.DOCKER_CREDENTIALS_ID) {
                        // Push backend
                        docker.image("${env.BACKEND_IMAGE}:${env.APP_VERSION}").push()
                        docker.image("${env.BACKEND_IMAGE}:latest").push()
                        
                        // Push frontend
                        docker.image("${env.FRONTEND_IMAGE}:${env.APP_VERSION}").push()
                        docker.image("${env.FRONTEND_IMAGE}:latest").push()
                    }
                    
                    echo "Docker images pushed successfully:"
                    echo "Backend: ${env.BACKEND_IMAGE}:${env.APP_VERSION}"
                    echo "Frontend: ${env.FRONTEND_IMAGE}:${env.APP_VERSION}"
                }
            }
        }
        
        stage('Update Version in GitHub') {
            steps {
                script {
                    // Configure git
                    sh '''
                        git config user.email "jenkins@ci-cd.local"
                        git config user.name "Jenkins CI"
                        
                        # Add version file
                        git add version.txt
                        
                        # Commit version change
                        git commit -m "Bump version to ${APP_VERSION} [skip ci]"
                        
                        # Create tag
                        git tag -a "v${APP_VERSION}" -m "Release version ${APP_VERSION}"
                        
                        # Push changes and tags
                        git push origin main
                        git push origin --tags
                    '''
                }
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'main'
            }
            steps {
                script {
                    
                    
                    // Deploy (if you have a dev server)
                   /* sh '''
                        # If deploying to localhost
                        docker-compose -f docker-compose.dev.yml down || true
                        docker-compose -f docker-compose.dev.yml up -d
                        
                        echo "Deployed version ${APP_VERSION} to Development"
                    '''*/
                }
            }
        }
    }
    
    post {
        success {
            script {
                def version = env.APP_VERSION
                def commitMsg = "Build ${env.BUILD_NUMBER} - Version ${version}"
                
                // Send email notification
                emailext (
                    subject: "✅ BUILD SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Build Successful</h2>
                        <p><b>Version:</b> ${version}</p>
                        <p><b>Job:</b> ${env.JOB_NAME}</p>
                        <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                        <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><b>Docker Images:</b></p>
                        <ul>
                            <li>${env.BACKEND_IMAGE}:${version}</li>
                            <li>${env.FRONTEND_IMAGE}:${version}</li>
                        </ul>
                        <p><b>Commit:</b> ${env.GIT_COMMIT}</p>
                        <p><b>Branch:</b> ${env.GIT_BRANCH}</p>
                    """,
                    to: 'team@yourcompany.com',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider']]
                )
            }
        }
        
        failure {
            script {
                emailext (
                    subject: "❌ BUILD FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Build Failed</h2>
                        <p><b>Job:</b> ${env.JOB_NAME}</p>
                        <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                        <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><b>Branch:</b> ${env.GIT_BRANCH}</p>
                        <p><b>Please check the logs for details.</b></p>
                    """,
                    to: 'team@yourcompany.com'
                )
            }
        }
        
        cleanup {
            script {
                // Clean up workspace
                cleanWs()
            }
        }
    }
}
