The flow of the request is as follows:
1. The request is sent the Ingress controller.
2. The Ingress controller receives the request and checks the Host header.
3. The Ingress controller matches the Host header against the rules defined in the Ingress resource.
4. If a match is found, the Ingress controller forwards the request to the appropriate service
5. The service then routes the request to the appropriate pod based on its selector.
6. The pod processes the request and sends a response back through the same path.

- When we have a look at our manifests, we can see that the Ingress resource has rules defined for the host `homework.yourcooldomain.com ` for basicall any path to that particular host (prefix with / in the ingress definition). The rule is defined to route the request to the service with name `homework1-service` on port 80. 
- The service `homework1-service` exists, and has a selector that matches the pods with label `app: homework`. This means that any request that matches the Ingress rule will be forwarded to the pods with this label.
- The only deployment in the manifest is the one with label `app: homework1`, which means that the service selector does not match the label of the pod. This is why the request is not reaching the pod, and you are getting a 404 error.
- To fix this, you need to either change the selector of the service to match the label of the pod, or change the label of the pod to match the selector of the service.


