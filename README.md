# App with Kubernetes and Docker

## Prerequisites
1. Install Docker and Docker Compose.
2. Install Python 3.12 and pip (if testing locally).
3. Install kubectl and set up access to the AKS cluster (if testing Kubernetes).

## Getting Started
1. Clone the repository
    git clone git@github.com:zeanmio/SSE-Team-Project-2.git
    cd SSE-Team-Project-2

2. Local Testing with Python
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python app/app.py
    Open your browser and navigate to: http://localhost:5000

3. Local Testing with Docker
    docker stop $(docker ps -q)
    docker rm $(docker ps -aq)
    docker build -t flaskapp .
    docker run -d -p 8080:5000 flaskapp
    Open your browser and navigate to: http://localhost:8080

4. Cloud Deployment with Kubernetes
    kubectl apply -f deployment.yml
    kubectl get services
    Locate the EXTERNAL-IP of your service and access the application

## Access the Deployed Application
The application is already deployed to Kubernetes and accessible at the following address: http://51.8.73.87/
