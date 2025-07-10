Let's list our Custom Resource Definitions (CRDs) in the cluster:

```bash
k get crd

NAME                                  CREATED AT
certificaterequests.cert-manager.io   2025-07-07T11:50:21Z
certificates.cert-manager.io          2025-07-07T11:50:21Z
challenges.acme.cert-manager.io       2025-07-07T11:50:21Z
clusterissuers.cert-manager.io        2025-07-07T11:50:21Z
issuers.cert-manager.io               2025-07-07T11:50:21Z
orders.acme.cert-manager.io           2025-07-07T11:50:21Z
```

The second CRD is `certificates.cert-manager.io`, let's check its `apiVersion`:

```bash
k get crd certificates.cert-manager.io -o yaml | grep apiVersion
apiVersion: apiextensions.k8s.io/v1
```
Tadaaaa! So in our case, the answer would be:
"I am a pro and the version of the `certificates.cert-manager.io` is `apiextensions.k8s.io/v1`.
