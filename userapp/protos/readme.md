# Protobuf (gRPC) reminders

Run the following line to generate protos, I did it in the protos folder

```
pip install grpcio
pip install grpcio-tools
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. protos/connection.proto
# or, for in protos file
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. connection.proto
```
