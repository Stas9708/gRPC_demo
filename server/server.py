import logging
from typing import Iterator, Iterable
from compiled import greet_pb2, greet_pb2_grpc
import grpc


class Greeter(greet_pb2_grpc.GreeterServicer):
    def SayHello(
        self,
        request: greet_pb2.HelloRequest,
        context: grpc.ServicerContext,
    ) -> greet_pb2.HelloReply:
        print(f"SayHello received {request}")
        return greet_pb2.HelloReply(message="Hello, %s!" % request.name)

    def SayHelloBothStream(
        self,
        request_iter: Iterator[greet_pb2.HelloRequest],
        context: grpc.ServicerContext,
    ) -> Iterable[greet_pb2.HelloReply]:
        for r in request_iter:
            print(f"Stream request {r}")
            return greet_pb2.HelloReply(message="Hello, %s!" % r.name)


def serve() -> None:
    server = grpc.server()
    greet_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()