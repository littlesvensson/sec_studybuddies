We will create holyconfig ConfigMap with usage of --from-literal option:

```bash
k create cm holyconfig --from-literal=BESTCHAPTERINTHEWORLD=security
```
The second task will use the --from-file option as we want to create a ConfigMap from a file. The path will depend on your current working directory, so make sure to adjust it accordingly. The command will look like this in case you are in the session_3 directory:

```bash
k create cm holyconfig2 -n studybuddies --from-env-file=task3_4/config
```
