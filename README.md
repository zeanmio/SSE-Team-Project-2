# App with Kubernetes and Docker

## Prerequisites
1. Install Docker and Docker Compose.
2. Install Python 3.12 and pip (if testing locally).
3. Install kubectl and set up access to the AKS cluster (if testing Kubernetes).

## Getting Started
### 1. Clone the repository
```bash
git clone git@github.com:zeanmio/SSE-Team-Project-2.git
cd SSE-Team-Project-2
```

### 2. Local Testing with Python
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```
Open your browser and navigate to: http://localhost:5000

### 3. Local Testing with Docker
```bash
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker build -t flaskapp .
docker run -d -p 8080:5000 --env-file .env flaskapp
```
Open your browser and navigate to: http://localhost:8080

### 4. Cloud Deployment with Kubernetes
```bash
kubectl delete service flask-app-service
kubectl apply -f deployment.yml
kubectl get services
```
Locate the EXTERNAL-IP of your service and access the application

## Access the Deployed Application
The application is deployed to Kubernetes and currently accessible at the following address: http://135.234.194.94/
