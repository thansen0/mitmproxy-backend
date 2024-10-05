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

# C++ Example

```
sudo apt install libgrpc++-dev libgrpc-dev protobuf-compiler-grpc
# Turn into makefile someday
# run in protos/ folder
protoc --proto_path=. --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin image_classification.proto
protoc --proto_path=. --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin text_binary_classification.proto

# run by FastAllClassifier file
g++ -std=c++17 FastAllClassifier.cpp protos/image_classification.pb.cc protos/image_classification.grpc.pb.cc protos/text_binary_classification.pb.cc protos/text_binary_classification.grpc.pb.cc -o FastAllClassifier -lgrpc++ -lprotobuf -lpthread
```

Incidentally I'm getting an error when I try to run apt install, saying I have the wrong linux headers, although it works anyways.

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
