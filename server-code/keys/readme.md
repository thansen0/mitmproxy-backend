# Generating keys

These keys must be passed into the docker container and must be added to root certificates of end users since they're a custom set. You can generate them using the following script

```
openssl genrsa -out cert.key 2048
# (Specify the mitm domain as Common Name, e.g. \*.google.com)
openssl req -new -x509 -key cert.key -out cert.crt
cat cert.key cert.crt > cert.pem
```

Where cert.key is the private key and cert.crt is the public key.
