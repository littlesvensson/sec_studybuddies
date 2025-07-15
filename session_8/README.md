SESSION 8, 16.7.2025 
========================

* How to work with Services: LoadBalancer, ExternalName, Headless
* Blue/Green, Canary deployments in Kubernetes native way
* Ingress, Use Ingress rules to expose applications
* Provide and troubleshoot access to applications via services

### LoadBalancer
LoadBalancer is used in cloud environments to expose the service externally. It creates an external load balancer that routes traffic to the service. This is the most common way to expose services in production.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: studybuddies
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80                                     # Exposed service port
      targetPort: 8080                             # Container port
```

*What this does:*
- Exposes your app to external traffic via a cloud provider's LoadBalancer.
- The service is reachable via an external IP (automatically assigned, will not work with local environment).
- Internally, traffic is routed to Pods with label app: myapp, hitting port 8080 on the container.

*Use this when:
- You're in a cloud environment (Openstac, AWS, GCP, Azure...)
- You need external access to your app.
- You want automatic IP + DNS assignment via the provider.

### TASK! (#1)

TO DO: Create a LoadBalancer service for the existing Deployment myapp in the `studybuddies` namespace, try it with the create command.

### BONUS: ExternalName Service

A Service of type ExternalName creates a DNS alias inside the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cute-external-service
  namespace: studybuddies
spec:
  type: ExternalName
  externalName: httpbin.org
```

In the example above, when looking up the host cute-external-service.prod.svc.cluster.local, the cluster DNS Service returns a CNAME record with the value httpbin.org.

Let's try it together!

In the folder [externalname](session_7/externalname), you will find two files: [pod.yaml](session_7/externalname/pod.yaml) and [service.yaml](session_7/externalname/service.yaml). Apply them in the `studybuddies` namespace.

```bash
k apply -f session_7/externalname/pod.yaml
k apply -f session_7/externalname/service.yaml
```
Now, let's test it by running a curl command in the pod:

```bash
k exec -it curl-test -n studybuddies -- curl cute-external-service/get
```

>Note: httpbin.org is a free, open-source HTTP request & response testing service. It's designed for developers to inspect HTTP requests, simulate different kinds of responses and test HTTP clients (e.g., curl, Postman, code). /get is one of its endpoints that returns a JSON response with details about the request made to it.


### Headless Service

A Headless Service is a Service with no ClusterIP. It doesn’t load balance - instead, it lets you reach individual Pod IPs directly.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-headless-service
  namespace: studybuddies
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
    - port: 80
```
Headless services are most commonly used with StatefulSets, where each pod needs a stable DNS name.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: studybuddies
spec:
  clusterIP: None                       # None = Headless
  selector:
    app: nginx
  ports:
    - port: 80
```

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nginx
  namespace: studybuddies
spec:
  serviceName: nginx                    # Must match the headless service name
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
```

Let's try it together! In the folder [headless](session_7/headless), you will find two files: [service.yaml](session_7/headless/service.yaml) and [statefulset.yaml](session_7/headless/statefulset.yaml). Apply them in the `studybuddies` namespace.

And now, let's test it by running a curl command in the pod:


```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh

curl echo-0.echo-headless.studybuddies.svc.cluster.local:8080
```


>Notes: In the context of CKAD, you should be able to create a Service YAML from scratch or imperatively, connect pods to services using labels/selectors and understand how DNS resolution works (`my-service.my-namespace.svc.cluster.local`)


## Blue/Green Deployment (CKAD Level)

A Blue-Green Deployment is a deployment strategy where two identical environments, the “blue” environment and the “green” environment, are set up. The blue environment is the production environment, where the live version of the application is currently running, and the green environment is the non-production environment, where new versions of the application are deployed.

When a new version of the application is ready to be deployed, it is deployed to the green environment. Once the new version is deployed and tested, traffic is switched to the green environment, making it the new production environment. The blue environment then becomes the non-production environment, where future versions of the application can be deployed.

![Blue/Green Deployment](../assets/blue_green_deployment.png) <br>
Image source: [medium.com](https://medium.com/cloud-native-daily/blue-green-deployments-with-kubernetes-a-comprehensive-guide-5d196dad1976)

### Task! (#2)

In the folder task8_2, you will find manifess for both blue and green deployment in the deployments.yaml file. Apply them in the `studybuddies` namespace.

- Create a Service that selects the blue version of the app (version: blue).
- Check if the Service is working by running a curl command in the pod.
- Edit the Service to select the green version of the app (version: green).
- Check if the Service is still working by running a curl command in the pod:

```bash
k run -it --rm tester --image=curlimages/curl -n studybuddies --restart=Never -- sh
curl myapp-service:8080
```



## Canary Deployment

A canary deployment in Kubernetes is a strategy where a small subset of users is routed to a new version of an application, while the rest continue using the stable version. This allows teams to test and monitor the new release in production with minimal risk before gradually rolling it out to all users.

### How It Works

```yaml
# Stable Deployment (v1)
metadata:
  name: myapp-v1
  labels:
    app: myapp
    version: v1

# Canary Deployment (v2)
metadata:
  name: myapp-v2
  labels:
    app: myapp
    version: canary

# Shared Service selects both
spec:
  selector:
    app: myapp
```



### TASK! (#3)



## Ingress

An Ingress is an API object that:

- Exposes HTTP/HTTPS routes from outside the cluster to services inside
- Acts like a reverse proxy: routes traffic based on hostnames and paths
- Requires an Ingress Controller (e.g., NGINX Ingress Controller) to function

What You Need to Know for CKAD
1. Understand Basic Ingress YAML
2. Know That an Ingress Controller Is Required
3. Use kubectl port-forward for testing


Common Ingress Tasks in CKAD
You may be asked to:

- Create an Ingress to expose a service
- Route multiple paths or hostnames
- Fix an Ingress that's misconfigured (e.g., wrong pathType, wrong service name)


5. Optional: TLS Support
You’re not required to deeply configure TLS, but should recognize a TLS block:

```yaml
tls:
- hosts:
  - myapp.example.com
  secretName: tls-secret
```

### Task! (#4)

This time, the task is awaiting you in the [Killercoda: Ingress create section].(https://killercoda.com/killer-shell-ckad/scenario/ingress-create). Once you will get the last check successfully, please do not close the scenario, just express your happiness in the chat, we will do some check together.


## Wrap up
8th session is behind us, ou yeaaaaah!

Today, we have had a look at:
* Some new Service types: LoadBalancer, ExternalName, Headless
* How to do Blue/Green and Canary deployments in Kubernetes native way
* What is Ingress and how to use it

Good work, studybuddies! The last session is ahead of us, so let's keep the pace!


