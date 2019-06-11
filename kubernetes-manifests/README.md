# Deploy using Kubernetes

https://github.com/GoogleCloudPlatform/cloud-code-samples/tree/master/python/python-hello-world

## Using local Docker for Mac Kubernetes

Prerequisite: Docker for Mac Kubernetes is running on local machine.

Create a namespace

```bash
kubectl create namespace flaskr
```

Create a service account

```bash
kubectl create serviceaccount flaskr-admin
```

Create a context for review the dev version

```bash
kubectl config set-context review --namespace=flaskr --cluster docker-desktop --user flaskr-admin
```

Switch to the new `review` context

```bash
kubectl config use-context review
```

Create the Kubernetes manifest for the local deployment: `./kubernetes-manifests/flaskr-review-local.deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flaskr-review-deployment
  labels:
    app: flaskr
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flaskr
  template:
    metadata:
      labels:
        app: flaskr
    spec:
      containers:
        - name: flaskr
          image: flaskr:latest
          imagePullPolicy: Never
          ports:
          - containerPort: 8080
```

Note the `imagePullPolicy: Never`. With this settings Kubernetes will use the local Docker image repository.

Add more configuration to the `yaml`: namespaces, service accounts, service

The following commands help to expose a container. The first one lists containers and use the selected one in the second command.

```bash
kubectl get pods --namespace flaskr 
kubectl --namespace flaskr port-forward flaskr-review-deployment-55f7b97dd4-w76kg 8080:8080
```

Expose a service using LoadBalancer. The app inside the docker uses port 8080 (target-port). Let's expose it to `9090` on the host machine.

```bash
kubectl expose deployment flaskr-review-deployment --type LoadBalancer --port 9090 --target-port 8080
```

# Deploy to Google Cloud Kubernetes Engine

- Setup `.dockerignore`.
- Create `Dockerfile`

## Google Cloud Kubernetes implementation

- [Deploying a language-specific app](https://cloud.google.com/kubernetes-engine/docs/quickstarts/deploying-a-language-specific-app)

Steps:

1. Create a service account.
2. Build a container and upload it to registry
3. Deploy the container
4. Create a load balancer service to expose the url
5. Create a volume and attach to the pod
6. Add init container to run the database initialization
