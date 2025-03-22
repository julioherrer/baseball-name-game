pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'localhost:5000'
        IMAGE_NAME = 'baseball-game'
        KUBERNETES_NAMESPACE = 'default'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                    docker.push("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Update the deployment with the new image
                    sh """
                        kubectl set image deployment/baseball-name-game \
                        baseball-game=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                        -n ${KUBERNETES_NAMESPACE}
                    """
                    
                    // Wait for the deployment to complete
                    sh """
                        kubectl rollout status deployment/baseball-name-game \
                        -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
} 