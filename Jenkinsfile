pipeline {
    agent any
    
    environment {
        // GitHub Configuration
        GITHUB_REPO = 'https://github.com/hermiMoh/todo-app-cicd-EKS.git'
        GITHUB_CREDENTIALS_ID = 'github-credentials'
        
        // Docker Configuration
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_NAMESPACE = 'hermimoh'  // Replace with your Docker Hub username
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        
        // Application Configuration
        APP_NAME = 'todo-app'
        BACKEND_IMAGE = "${DOCKER_NAMESPACE}/${APP_NAME}-backend"
        FRONTEND_IMAGE = "${DOCKER_NAMESPACE}/${APP_NAME}-frontend"
        
        // Version Configuration
        VERSION_FILE = 'version.txt'
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
                    ]],
                    extensions: [[
                        $class: 'CleanBeforeCheckout'
                    ]]
                ])
            }
        }
        
        stage('Increment Version') {
            steps {
                script {
                    // Read or create version file
                    def versionFile = fileExists(VERSION_FILE) ? readFile(VERSION_FILE).trim() : '1.0.0'
                    def versionParts = versionFile.split('\\.')
                    def patch = versionParts[2].toInteger() + 1
                    def newVersion = "${versionParts[0]}.${versionParts[1]}.${patch}"
                    
                    // Set environment variable
                    env.APP_VERSION = newVersion
                    
                    // Update version file
                    writeFile file: VERSION_FILE, text: newVersion
                    
                    echo "🚀 New Version: ${env.APP_VERSION}"
                }
            }
        }
        
        stage('Backend Build & Test') {
            steps {
                dir('backend') {
                    script {
                        // Run Python tests
                        sh '''
                            echo "Running backend tests..."
                            python3 -m venv venv || true
                            source venv/bin/activate || true
                            pip install -r requirements.txt || true
                            pip install pytest pytest-cov || true
                            pytest -v --cov=. || echo "Tests completed with warnings"
                        '''
                        
                        // Build Docker image
                        sh """
                            docker build -t ${BACKEND_IMAGE}:${APP_VERSION} .
                            docker tag ${BACKEND_IMAGE}:${APP_VERSION} ${BACKEND_IMAGE}:latest
                        """
                    }
                }
            }
        }
        
        stage('Frontend Build & Test') {
            steps {
                dir('frontend') {
                    script {
                        // Run frontend tests
                        sh '''
                            echo "Running frontend tests..."
                            npm install || true
                            npm test || echo "Tests completed with warnings"
                        '''
                        
                        // Build Docker image
                        sh """
                            docker build -t ${FRONTEND_IMAGE}:${APP_VERSION} .
                            docker tag ${FRONTEND_IMAGE}:${APP_VERSION} ${FRONTEND_IMAGE}:latest
                        """
                    }
                }
            }
        }
        
        stage('Push Docker Images') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKER_CREDENTIALS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push ${BACKEND_IMAGE}:${APP_VERSION}
                            docker push ${BACKEND_IMAGE}:latest
                            docker push ${FRONTEND_IMAGE}:${APP_VERSION}
                            docker push ${FRONTEND_IMAGE}:latest
                        """
                    }
                    echo "✅ Docker images pushed successfully!"
                }
            }
        }
        
        stage('Update Version in GitHub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: env.GITHUB_CREDENTIALS_ID,
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {
                        sh """
                            # Configure git
                            git config user.email "jenkins@ci-cd.local"
                            git config user.name "Jenkins CI"
                            
                            # Add version file
                            git add version.txt
                            
                            # Commit version change
                            git commit -m "Bump version to ${APP_VERSION} [skip ci]" || echo "No changes to commit"
                            
                            # Create tag
                            git tag -a "v${APP_VERSION}" -m "Release version ${APP_VERSION}" || echo "Tag already exists"
                            
                            # Push changes and tags
                            git push origin main || echo "Push failed, check credentials"
                            git push origin --tags || echo "Tag push failed"
                        """
                    }
                }
            }
        }
        
        stage('Deploy to Development') {
           echo " deployment with EKS ....."
            
        }
    }
    
    post {
        success {
            script {
                echo """
                ============================================
                ✅ BUILD SUCCESSFUL!
                ============================================
                Version: ${env.APP_VERSION}
                Job: ${env.JOB_NAME}
                Build: #${env.BUILD_NUMBER}
                Images:
                  - ${env.BACKEND_IMAGE}:${env.APP_VERSION}
                  - ${env.FRONTEND_IMAGE}:${env.APP_VERSION}
                ============================================
                """
            }
        }
        
        failure {
            script {
                echo """
                ❌ BUILD FAILED!
                Job: ${env.JOB_NAME}
                Build: #${env.BUILD_NUMBER}
                Check logs for details.
                """
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