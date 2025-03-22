#!/bin/bash

# Make a small change to trigger the pipeline
echo "# Test change" >> README.md

# Commit and push the change
git add README.md
git commit -m "Test: Trigger Jenkins pipeline"
git push

echo "Pipeline triggered! Check Jenkins at http://localhost:30000 for build status." 