from compiled import greet_pb2, greet_pb2_grpc
import logging
import grpc


def request_iter():
    for _ in range(5):
        yield greet_pb2.HelloRequest(name="Test stream request")


def run() -> None:
     with grpc.insecure_channel("localhost:50051") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        response = stub.SayHelloBothStream(request_iter())
        for i in response:
            print(f"Greeter client received: {i.message}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
