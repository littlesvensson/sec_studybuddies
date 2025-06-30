```bash
k run meowmaster -it --rm --restart=Never --image=wernight/funbox -- nyancat
```

* `k` - shortcut for `kubectl` command
* `run` - command to create a pod
* `meowww` - name of the pod, 
* `-it` - interactive terminal, 
* `--rm` - remove the pod after it exits, 
* `--restart=Never` - do not restart the pod, 
* `--image=wernight/funbox` - image to use
* `-- nyancat` - command to run in the container.