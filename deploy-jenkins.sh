#!/bin/bash

# Create Jenkins namespace if it doesn't exist
kubectl create namespace jenkins --dry-run=client -o yaml | kubectl apply -f -

# Apply Jenkins deployment
echo "Deploying Jenkins..."
kubectl apply -f k8s/jenkins-deployment.yaml

# Wait for Jenkins pod to be ready
echo "Waiting for Jenkins pod to be ready..."
kubectl wait --for=condition=ready pod -l app=jenkins -n jenkins --timeout=300s

# Get Jenkins pod name
JENKINS_POD=$(kubectl get pods -n jenkins -l app=jenkins -o jsonpath="{.items[0].metadata.name}")

# Get Jenkins admin password
echo "Getting Jenkins admin password..."
JENKINS_PASSWORD=$(kubectl exec -n jenkins $JENKINS_POD -- cat /var/jenkins_home/secrets/initialAdminPassword)

# Install required plugins
echo "Installing required plugins..."
kubectl exec -n jenkins $JENKINS_POD -- jenkins-plugin-cli --plugins \
    docker-workflow \
    kubernetes \
    git \
    pipeline-utility-steps \
    credentials-binding

# Restart Jenkins to apply plugin changes
echo "Restarting Jenkins to apply plugin changes..."
kubectl delete pod -n jenkins $JENKINS_POD

# Wait for Jenkins to restart
echo "Waiting for Jenkins to restart..."
kubectl wait --for=condition=ready pod -l app=jenkins -n jenkins --timeout=300s

echo "Jenkins deployment completed!"
echo "Access Jenkins at http://localhost:30000"
echo "Initial admin password: $JENKINS_PASSWORD"
echo "JNLP port: 30001"
echo ""
echo "Next steps:"
echo "1. Log in to Jenkins with the admin password"
echo "2. Create a new pipeline job named 'baseball-game-pipeline'"
echo "3. Configure the pipeline to use the Jenkinsfile from your repository"
echo "4. Set up Docker and Kubernetes credentials in Jenkins"
echo "5. Access the application at http://localhost:8000"
echo "6. Access the application at http://localhost:30901" 