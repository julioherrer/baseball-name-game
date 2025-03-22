#!/bin/bash

# Get Jenkins pod name
JENKINS_POD=$(kubectl get pods -n jenkins -l app=jenkins -o jsonpath="{.items[0].metadata.name}")

# Get Jenkins admin password
JENKINS_PASSWORD=$(kubectl exec -n jenkins $JENKINS_POD -- cat /var/jenkins_home/secrets/initialAdminPassword)

# Create pipeline configuration
cat <<EOF | kubectl exec -i -n jenkins $JENKINS_POD -- bash -c 'cat > /var/jenkins_home/jobs/baseball-game-pipeline/config.xml'
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@1289.vd1c337fd5354">
  <description>Pipeline for baseball game application</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@3697.rc380.6d9b_5e8b_e3fd">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@5.0.0">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>git@github.com:julioherrer/baseball-name-game.git</url>
          <credentialsId>git-credentials</credentialsId>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
EOF

# Create jobs directory if it doesn't exist
kubectl exec -n jenkins $JENKINS_POD -- mkdir -p /var/jenkins_home/jobs/baseball-game-pipeline

# Set correct permissions
kubectl exec -n jenkins $JENKINS_POD -- chown -R jenkins:jenkins /var/jenkins_home/jobs/baseball-game-pipeline

# Restart Jenkins to apply changes
echo "Restarting Jenkins to apply pipeline configuration..."
kubectl delete pod -n jenkins $JENKINS_POD

# Wait for Jenkins to restart
echo "Waiting for Jenkins to restart..."
kubectl wait --for=condition=ready pod -l app=jenkins -n jenkins --timeout=300s

echo "Pipeline setup completed!"
echo "Access Jenkins at http://localhost:30000"
echo "Username: admin"
echo "Password: $JENKINS_PASSWORD"
echo ""
echo "Next steps:"
echo "1. Log in to Jenkins"
echo "2. Go to Manage Jenkins > Manage Credentials"
echo "3. Add your Docker registry credentials"
echo "4. Trigger a build from the pipeline page" 