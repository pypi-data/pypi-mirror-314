import csv
import socket
import json
from haprapi.Models.models import *

class Client:

    @staticmethod
    def recv_all(sock, buffer_size: int = 4096):
        data = b""
        while True:
            chunk = sock.recv(buffer_size)
            if not chunk:
                break
            data += chunk
        return data.decode("utf-8")

    @staticmethod
    def parse_backend_data(data: str) -> Backend:
        """
        Parse the backend data received from HAProxy and create a Backend object.

        This method takes the raw string data from HAProxy, parses it, and constructs a Backend object
        containing information about the backend and its servers.

        Args:
            data (str): The raw string data received from HAProxy containing backend information.

        Returns:
            Backend: An object representing the backend, containing its ID, name, and a list of Server objects.

        Note:
            This method expects the input data to be in a specific format, with the first line being a counter,
            the second line being a header, and subsequent lines containing server information.

        Raises:
            ValueError: If the data format is unexpected or cannot be parsed correctly.
        """
        lines = data.strip().split('\n')
        header = lines[1]  # Skip the first line (1) and use the second line as header
        server_lines = lines[2:]  # Actual data starts from the third line

        # Extract column names from the header
        columns = header.strip('# ').split()

        # Initialize Backend
        backend_id = None
        backend_name = None
        servers = []

        for line in server_lines:
            parts = line.split()
            server_data = dict(zip(columns, parts))

            if backend_id is None:
                backend_id = int(server_data['be_id'])
                backend_name = server_data['be_name']

            server = Server(
                id=int(server_data['srv_id']),
                name=server_data['srv_name'],
                address=server_data['srv_addr'],
                operational_state=ServerOperationalState(int(server_data['srv_op_state'])),
                admin_state=ServerAdminState(int(server_data['srv_admin_state'])),
                user_weight=int(server_data['srv_uweight']),
                initial_weight=int(server_data['srv_iweight']),
                time_since_last_change=int(server_data['srv_time_since_last_change']),
                check_status=int(server_data['srv_check_status']),
                check_result=int(server_data['srv_check_result']),
                check_health=int(server_data['srv_check_health']),
                check_state=int(server_data['srv_check_state']),
                port=int(server_data['srv_port'])
            )
            servers.append(server)

        return Backend(id=backend_id, name=backend_name, servers=servers)

    def __init__(self, socket_host : str = 'localhost', socket_port: int = 9999):
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.socket_path = (socket_host, socket_port)

    def send_command(self, command: str) -> str:
        """
        Send a command to the HAProxy socket and receive the response.

        This method establishes a connection to the HAProxy socket, sends the specified command,
        and returns the full response received from HAProxy.

        Args:
            command (str): The command to send to HAProxy.

        Returns:
            object: The response received from HAProxy. The exact type depends on the recv_all function's implementation.

        Raises:
            socket.error: If there's an error in socket connection or communication.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.socket_path)
            sock.sendall(command.encode() + b'\n')
            return self.recv_all(sock)

    def get_info(self, output_format: str = 'json', desc: bool = False) -> object:
        """
        Retrieve HAProxy information.

        Args:
            output_format (str): The desired output format. Can be 'json', 'csv', or 'typed' format. Defaults to 'json'.
            desc (bool): If True, includes descriptions in the output. Defaults to False.

        Returns:
            dict or str: If output_format is 'json', returns a dictionary. If 'csv', returns a list of dictionaries.
            Otherwise, returns the raw response string.
        """
        response = self.send_command(f'show info {output_format} {desc}')
        if output_format == 'json':
            return json.loads(response)
        return response

    def get_stat(self, filter_by: str = '', output_format: str = 'csv', desc: bool = False) -> list|dict:
        """
        Retrieve HAProxy statistics.

        Args:
            filter_by (str): Filter string to apply to the statistics. Defaults to ''.
            output_format (str): The desired output format. Can be 'json', 'csv', or 'typed' format. Defaults to 'csv'.
            desc (bool): If True, includes descriptions in the output. Defaults to False.

        Returns:
            list or dict: If output_format is 'json', returns a dictionary. If 'csv', returns a list of dictionaries.
            Otherwise, returns the raw response string.
        """
        options = []
        if filter_by:
            options.append(f'{filter_by}')
        if output_format == 'json' and not desc:
            options.append(f'{format}')
        if desc:
            options.append('desc')

        response = self.send_command(f'show stat {"".join(options)}'.rstrip(' '))

        if output_format == 'json':
            return json.loads(response)
        if output_format == 'csv':
            response = [i for i in csv.DictReader(response.lstrip('# ').splitlines())]
        return response

    def get_schema(self) -> dict:
        """
        Retrieve the HAProxy configuration schema.

        Returns:
            dict: The HAProxy configuration schema as a dictionary.
        """
        response = self.send_command(f'show schema json')
        return json.loads(response)

    def get_backend(self, backend: str) -> str:
        """
        Retrieve information about a specific backend.

        Args:
            backend (str): The name of the backend to retrieve information for.

        Returns:
            str: Raw response containing information about the specified backend.
        """
        response = self.send_command(f'show servers state {backend}')
        return response

    def get_backends(self) -> list:
        """
        Retrieve information about all backends.

        Returns:
            list: A list of Backend objects containing information about all backends.
        """
        response = self.send_command(f'show backend').strip().split('\n')
        backends = []
        for backend in response[2:-1]:
            data = self.get_backend(backend)
            backends.append(self.parse_backend_data(data))
        return backends

    def get_frontends(self) -> list:
        """
        Retrieve a list of all frontend names.

        Returns:
            list: A list of strings containing the names of all frontends.
        """
        stats = self.get_stat(filter_by='', output_format='csv', desc=True)
        response = []
        for i in stats:
            if i['svname'].lower() == 'frontend':
                response.append(i['pxname'])
        return response

    def enable_server(self, backend: str, server: str) -> bool:
        """
        Enable a server in a specific backend.

        Args:
            backend (str): The name of the backend containing the server.
            server (str): The name of the server to enable.

        Returns:
            bool: True if the server was successfully enabled, False otherwise.
        """
        response = self.send_command(f'enable server {backend}/{server}')
        if len(response) == 1 and response.isspace():
            return False
        return True

    def disable_server(self, backend: str, server: str) -> bool:
        """
        Disable a server in a specific backend.

        Args:
            backend (str): The name of the backend containing the server.
            server (str): The name of the server to disable.

        Returns:
            bool: True if the server was successfully disabled, False otherwise.
        """
        response = self.send_command(f'disable server {backend}/{server}')
        if len(response) == 1 and response.isspace():
            return False
        return True

    def enable_frontend(self, backend: str, server: str) -> str:
        """
        Enable a frontend.

        Args:
            backend (str): The name of the backend (unused in this context).
            server (str): The name of the frontend to enable.

        Returns:
            str: The raw response from the HAProxy command.
        """
        response = self.send_command(f'enable frontend {backend}/{server}')
        return response

    def disable_frontend(self, backend: str, server: str) -> str:
        """
        Disable a frontend.

        Args:
            backend (str): The name of the backend (unused in this context).
            server (str): The name of the frontend to disable.

        Returns:
            str: The raw response from the HAProxy command.
        """
        response = self.send_command(f'disable frontend {backend}/{server}')
        return response