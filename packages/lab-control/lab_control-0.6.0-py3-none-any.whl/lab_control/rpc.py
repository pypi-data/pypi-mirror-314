from abc import ABC, abstractmethod
from serial import Serial
import socket
import json
import itertools
from typing import Callable, Any, Self
import types
import inspect


class BidirectionalLineStream(ABC):
    """Abstract base class for a bidirectional line stream. Implementations should be able to read and write lines."""

    @abstractmethod
    def read_line(self) -> str:
        """Read a line from the stream and return it as a string

        Returns:
            str: The line read from the stream
        """
        pass

    @abstractmethod
    def write_line(self, line: str):
        """Write a line to the stream"""
        pass


class SerialBLS(BidirectionalLineStream):
    """A bidirectional line stream with a serial port as the backend"""

    def __init__(self, serial_port: Serial, print_non_json=False):
        """Create a new SerialBLS instance from a serial port

        Args:
            serial_port (Serial): The serial port to use
            print_non_json (bool, optional): Print non-json (non protocol) lines to stdout. Defaults to False.
        """
        self.serial_port = serial_port
        self.print_non_json = print_non_json

    @staticmethod
    def connect(port: str, baudrate: int, print_non_json=False) -> Self:
        """Connect to a serial port and return a SerialBLS instance

        Args:
            port (str): The port to connect to
            baudrate (int): The baudrate to use
            print_non_json (bool, optional): Print non-json (non protocol) lines to stdout. Defaults to False.

        Returns:
            SerialBLS: The SerialBLS instance
        """
        serial_port = Serial(port, baudrate)
        return SerialBLS(serial_port, print_non_json)

    def read_line(self) -> str:
        while True:
            line = self.serial_port.readline().decode("utf-8")
            if line.startswith("{"):
                return line
            if line == "":
                raise EOFError("Serial port closed")
            if self.print_non_json:
                print(f"Non-json: {line}", end="")

    def write_line(self, line: str):
        self.serial_port.write(line.encode("utf-8"))
        self.serial_port.write(b"\n")
        self.serial_port.flush()


class SocketBLS(BidirectionalLineStream):
    """A bidirectional line stream with a socket as the backend"""

    def __init__(self, sock: socket.socket):
        """Create a new SocketBLS instance from a socket

        Args:
            sock (socket.socket): The socket to use
        """
        self.sock = sock
        self.socket_io = socket.SocketIO(sock, "rw")

    @staticmethod
    def connect(host: str, port: int) -> Self:
        """Connect to a socket and return a SocketBLS instance

        Args:
            host (str): The host to connect to
            port (int): The port to connect to

        Returns:
            SocketBLS: The SocketBLS instance
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return SocketBLS(sock)

    def read_line(self) -> str:
        return self.socket_io.readline().decode("utf-8")

    def write_line(self, line: str):
        self.socket_io.write(line.encode("utf-8"))
        self.socket_io.write(b"\n")
        self.socket_io.flush()


class RpcClient:
    """A client class over which to call procedures on a remote server"""

    def __init__(self, bls: BidirectionalLineStream):
        """Create a new RpcClient instance

        Args:
            bls (BidirectionalLineStream): The bidirectional line stream to use
        """
        self.bls = bls
        self.id_gen = itertools.cycle(range(2**32))
        self.responses = {}

    def read_response(self, id: int) -> dict:
        """Read a response from the server (or from the internal response buffer) with the specified id

        All other responses read while awaiting the specified id are stored internally

        Args:
            id (int): The id of the response to read
        """
        if id in self.responses:
            return self.responses.pop(id)
        while True:
            response = json.loads(self.bls.read_line())
            if response.get("id", None) == id:
                return response
            else:
                self.responses[response["id"]] = response

    def call(self, method: str, *args) -> Any:
        """Call a remote procedure with the specified method name and arguments

        Args:
            method (str): The name of the method to call
            *args: The arguments to pass to the method

        Returns:
            Any: The result of the remote procedure call

        Raises:
            ValueError: If the remote procedure call server returns an error or the procedure errors
        """
        call_id = next(self.id_gen)
        request = {"mrpc": "1.0", "call": method, "args": args, "id": call_id}
        self.bls.write_line(json.dumps(request))
        response = self.read_response(call_id)
        if "error" in response:
            raise ValueError(f"Error: {response['error']}")
        return response["result"]

    def register(self, method: Callable) -> Callable:
        """Wrap a stub method so that it is called remotely via this instance

        Since this is a method that takes a function and returns a function, it can be used as a decorator.
        The stub must have type hints for all arguments as true types and not strings.
        The types will be checked when calling and the wrapped method will raise if the types are incorrect before attempting to call the remote procedure.
        Generic aliases eg list[int] will only check the base type (list) and not the inner type (int).

        Args:
            method (Callable): The method to wrap

        Returns:
            Callable: The wrapped method
        """
        simplified_types = []
        for param in inspect.signature(method).parameters.values():
            if param.annotation == inspect._empty or not (
                isinstance(param.annotation, type) or type(param.annotation) in (types.GenericAlias, types.UnionType)
            ):
                raise TypeError(
                    f"Unspecified type for argument {param.name}! Types must be specified for all arguments using true types (not strings)"
                )
            if type(param.annotation) is types.GenericAlias:
                simplified_types.append(param.annotation.__origin__)
            else:
                simplified_types.append(param.annotation)

        def wrapper(*args):
            method(*args)  # basic check to make sure the number of arguments is correct
            params = list(inspect.signature(method).parameters.values())
            args_vals = [param.default for param in params]
            for i, (arg, param, simple_type) in enumerate(zip(args, params, simplified_types)):
                if not isinstance(arg, simple_type):
                    raise TypeError(f"Expected {param.annotation} for {param.name}, got {type(arg)}")
                args_vals[i] = arg
            return self.call(method.__name__, *args_vals)

        wrapper.__name__ = method.__name__
        wrapper.__doc__ = method.__doc__
        wrapper.__signature__ = inspect.signature(method)
        return wrapper


class RpcProxy:
    """This class can be inherited from by a class made up of stub methods to wrap them for remote procedure calls

    On initialization all methods that do not start with an underscore will be replaced by a wrapped version that calls the respective
    method on the remote that is passed in the constructor.
    """

    def __init__(self, client: RpcClient):
        """Create a new RpcProxy instance

        Args:
            client (RpcClient): The client to use for remote procedure calls
        """
        self.client = client
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not name.startswith("_"):
                setattr(self, name, client.register(method))
