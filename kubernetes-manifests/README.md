# Deploy using Kubernetes

https://github.com/GoogleCloudPlatform/cloud-code-samples/tree/master/python/python-hello-world

## Using local Docker for Mac Kubernetes

Prerequisite:
 
- Docker for Mac Kubernetes is running on local machine.
- Alternative option on Linux: [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) + [Kind](https://kind.sigs.k8s.io/)

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
- [Gilab Runner and Kubernetes](https://medium.com/@davivc/how-to-set-up-gitlab-ci-cd-with-google-cloud-container-registry-and-kubernetes-fa88ab7b1295)
 
Steps:

1. Create a service account and download the authentication in json
2. Build a container and upload it to registry
3. Deploy the container
4. Create a load-balancer service to expose the url
5. Create a volume and attach to the pod
6. Add init container to run the database initialization

Debug `.gitlab-ci.yml` with a local `gitlab-runner`:

```bash
$ gitlab-runner exec docker --env GC_PROJECT_ID="$(<./project-id.json)" --env GC_SERVICE_ACCOUNT_KEY="$(<./gc-service-account-key.json)" build
```

Important findings: update `.gcloudignore` to allow `./dist` upload to the GCloud Builder, otherwise the builder cannot find the required folder. (The default behaviour is ignoring everything from .gitignore list.)

Build docker image in GitLab. Add `docker:dind` service to the task.

```
build:
  stage: build
  services:
    - docker:dind
```

Run docker-in-docker task in local environment:

```bash
gitlab-runner exec docker --env CI_BUILD_REF_NAME="maybe branch name" --env GC_PROJECT_ID="the-project-id" --env GC_SERVICE_ACCOUNT_KEY="$(<./gc-service-account-key.json)" --docker-volumes /var/run/docker.sock:/var/run/docker.sock --docker-privileged build
```

## Storage, volumes

- Need a persistent volume
- Need a persistent volume claim

Useful notes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

- Why `docker login -u _json_key`: https://cloud.google.com/container-registry/docs/advanced-authentication
- Docker login password from STDIN: https://docs.docker.com/engine/reference/commandline/login/

Overview about review apps: https://about.gitlab.com/2016/11/22/introducing-review-apps/

Using `yaml` merge key: https://yaml.org/type/merge.html

Predefined variables in Gitlab CI: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html

Deploying a containerized web application to Google Cloud Kubernetes: https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app

Persistent Volumes on Google Cloud

IMPORTANT! Because the Dockerfile created as non root container, have to setup a `securityContext` with the same `ID` as in Dockerfile.

```
securityContext:
        fsGroup: 1024
```

Substitute environment variables in Kubernetes manifest files. Use `envsubst`. Mac installation: `brew install gettext`.
```bash
$ CI_COMMIT_REF_SLUG=demo envsubst < ./kubernetes-manifests/flaskr-review-local.deployment.yaml | kubectl apply -f -
```

Add dynamic image tag management using `envsubst`.
- new commands in `Pipfile`
- using argument in `Dockerfile`

```
build-docker = "sh -c 'pipenv run build && IMAGE_TAG=${IMAGE_TAG:-latest} docker build --build-arg flaskr_image_name=flaskr:$IMAGE_TAG -t flaskr:$IMAGE_TAG .'"
deploy-kubernetes-local = "sh -c 'pipenv run build-docker && IMAGE_TAG=${IMAGE_TAG:-latest} envsubst < kubernetes-manifests/flaskr-review-local.deployment.yaml | kubectl apply -f -'"
```

## Setup Ingress Controller

What is Ingress? https://kubernetes.io/docs/concepts/services-networking/ingress/

Goal is to provide dynamic domain names for previewing development branch.

First install NGINX Ingress Controller in Kubernetes. Details: https://kubernetes.github.io/ingress-nginx/deploy/

Docker for Mac:

```
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud-generic.yaml
```

Most default Ingress redirect:

```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  labels:
    app: flaskr-${IMAGE_TAG}
  name: flaskr-review-ingress-${IMAGE_TAG}
  namespace: flaskr
spec:
  backend:
    serviceName: flaskr-review-load-balancer-${IMAGE_TAG}
    servicePort: 9090
```

Using free DNS resolver:

- lvh.me, example: branch-name.lvh.me
- xip.io, example: branch-name.127.0.0.1.xip.io
- nip.io, example: branch-name.127.0.0.1.nip.io

It works!

```
$ IMAGE_TAG=demo pipenv run deploy-kubernetes-local
$ IMAGE_TAG=branch-name pipenv run deploy-kubernetes-local
```

Different urls will show different version of the application: 
- demo.127.0.0.1.xip.io,
- branch-name.127.0.0.1.xip.io

Consideration. Kubernetes doesn't reload the image if it is built with the same tag as before. Suggested approach is to use git hash as tag. (https://github.com/kubernetes/kubernetes/issues/33664). An option could be change the scale to 0 and back to normal replica number.

Example: `kubectl scale --replicas=1 -n flaskr deployment flaskr-review-deployment-demo`

## Setup dynamic review deployment with GitLab CI and Google Cloud Platform Kubernetes

Changes are implemented in `kubernetes-manifests/flaskr-review-gcp.deployment.yaml`.

Important environment variables:

- `IMAGE_TAG` - using the GitLab CI provided slug string based on the branch name.
- `IMAGE_NAME` - points to Google Cloud registry where the image will be uploaded.
- `APP_DOMAIN` - Kubernetes Cluster main IP address.
- `GC_PROJECT_ID` - Google Cloud project id.

Prerequisite: downloaded key file saved in json format.

Test it locally:

```
$ gitlab-runner exec docker --env GC_PROJECT_ID="$(<./gc-project-id.txt)" --env GC_SERVICE_ACCOUNT_KEY="$(<./gc-service-account-key.json)" build
```