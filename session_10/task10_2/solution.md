The following steps outline how to deploy a ingressmagic using Helm and Kubernetes in the `ingress` namespace:


```bash
k create ns ingress
namespace/ingress created
```

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

```bash
helm install ingressmagic bitnami/nginx -n ingress

NAME: ingressmagic
LAST DEPLOYED: Mon Jul 21 15:34:55 2025
NAMESPACE: ingress
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: nginx
CHART VERSION: 21.0.8
APP VERSION: 1.29.0

NOTICE: Starting August 28th, 2025, only a limited subset of images/charts will remain available for free. Backup will be available for some time at the 'Bitnami Legacy' repository. More info at https://github.com/bitnami/containers/issues/83267

** Please be patient while the chart is being deployed **
NGINX can be accessed through the following DNS name from within your cluster:

    ingressmagic-nginx.ingress.svc.cluster.local (port 80)

To access NGINX from outside the cluster, follow the steps below:

1. Get the NGINX URL by running these commands:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace ingress -w ingressmagic-nginx'

    export SERVICE_PORT=$(kubectl get --namespace ingress -o jsonpath="{.spec.ports[0].port}" services ingressmagic-nginx)
    export SERVICE_IP=$(kubectl get svc --namespace ingress ingressmagic-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    echo "http://${SERVICE_IP}:${SERVICE_PORT}"

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - cloneStaticSiteFromGit.gitSync.resources
  - resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
```

```bash
helm list -n ingress

NAME        	NAMESPACE	REVISION	UPDATED                              	STATUS  	CHART       	APP VERSION
ingressmagic	ingress  	1       	2025-07-21 15:34:55.539284 +0200 CEST	deployed	nginx-21.0.8	1.29.0
```
