# Protobuf (gRPC) reminders

Run the following line to generate protos, I did it in the protos folder

```
pip install grpcio
pip install grpcio-tools
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. protos/connection.proto
```

## gRPC SSL keys

Generate keys (and be sure to set CN or SAN field as vps.parentcontrols.win)

```
openssl genrsa -out cert.key 2048
openssl req -new -x509 -key cert.key -out cert.crt
cat cert.key cert.crt > cert.pem
```

## Testing SSL

One great set of commands I found allow you to set up a server and client, and test your generated keys.

```
openssl s_server -cert server.crt -key server.key -port [port]
openssl s_client -connect [hostname]:[port] -showcerts
```

# Go Example (DEPRECATED)

To avoid the GIL, I'm going to try writting this in go. To install locally, run

```
wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
# add to .bashrc
export PATH=$PATH:/usr/local/go/bin
go mod init mitmproxy/server-code
go mod tidy
go get google.golang.org/grpc
go get google.golang.org/protobuf/cmd/protoc-gen-go
```
