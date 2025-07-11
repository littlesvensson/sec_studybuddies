At first, we will apply the manfest as it is:

```bash
k apply -f scenario.yaml
```

**What will happen?** <br>
* The container will start and immediately exit after 5 seconds (sleep 5), because it’s not a long-running process.
* Liveness probe will fail.
* The pod will likely go into CrashLoopBackOff.
* The app isn't actually serving HTTP on port 8080, so the probe itself is broken.
* You will see Events, restarts, probe failures.

