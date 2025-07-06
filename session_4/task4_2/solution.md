Easily done throught the command:

```bash
k create secret generic mydirtysecret -n studybuddies --from-literal=thebestlecturerever=jaja
``` 
You can check the yaml manifest of the secret with:

```bash
k get secret mydirtysecret -o yaml
```

The value of the secret is base64 encoded, so you can decode it with:

```bash
echo "encoded_value" | base64 --d  # Command might differ a bit depending on your system
```


And of course...*you are a pro!*