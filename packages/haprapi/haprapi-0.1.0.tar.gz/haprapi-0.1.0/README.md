# HAProxi

HAProxi is a Python library for interacting with HAProxy's runtime API. It provides a simple and intuitive interface to manage and monitor HAProxy instances programmatically.

## Features

- Connect to HAProxy's runtime API
- Retrieve HAProxy information and statistics
- Manage backend servers (enable/disable)
- Manage frontends (enable/disable)
- Parse and structure HAProxy data

## Installation

To install HAProxi, run the following command:

```bash
pip install haprapi
```

## Usage

Here's a basic example of how to use HAProxi:

```python
from haprapi import Client

# Initialize the client
client = Client('localhost', 9999)

# Get HAProxy information
info = client.get_info()
print(info)

# Get statistics
stats = client.get_stat()
print(stats)

# Enable a server
client.enable_server('backend_name', 'server_name')

# Disable a frontend
client.disable_frontend('frontend_name')
```

## Documentation

For detailed documentation, please refer to the docstrings in the source code.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the GPL-3.0 License.