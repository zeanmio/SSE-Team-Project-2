# DreamCanvas

## Access the Deployed Application
The application is deployed to Kubernetes and currently accessible at the following address: http://135.234.194.94/

## Prerequisites
1. Install Docker and Docker Compose.
2. Install Python 3.12 and pip (if testing locally).
3. Install kubectl and set up access to the AKS cluster (if testing Kubernetes).

## For Developing
### 1. Local Testing with Python
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```
Open your browser and navigate to: http://localhost:5000

### 2. Local Testing with Docker
```bash
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker build -t flaskapp .
docker run -d -p 8080:5000 --env-file .env flaskapp
```
Open your browser and navigate to: http://localhost:8080

### 3. Cloud Deployment with Kubernetes
You don't need to run Kubernetes commands manually. Just push your changes to the main branch, and the GitHub Actions workflow will automatically build and deploy your application to the AKS cluster.
```bash
kubectl delete service flask-app-service
kubectl apply -f deployment.yml
kubectl get services
```
Locate the EXTERNAL-IP of your service and access the application

## For Key Setting
### 1. Create a .env file locally
```bash
XXX_KEY=your_key
```

### 2. Create a Kubernetes secret
```bash
kubectl create secret generic xxx-secret --from-literal=XXX_KEY="your_key"
kubectl get secret openai-secret -o yaml
```

### 3. Add to GitHub Actions secret
Settings -> Secrets and variables -> Actions -> New repository secret
