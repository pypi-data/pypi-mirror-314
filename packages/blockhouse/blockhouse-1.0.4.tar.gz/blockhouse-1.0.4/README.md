## Blockhouse SDK API Package

This is a Python SDK package that is used for various functionality from the Blockhouse API. The package is published on PyPI and can be installed using pip.

## Table of Contents

1. Features
2. Usage
3. Available Functions
4. License
5. Contributing
6. Support
7. Changelog

## Features

- Fetch trade data from the Blockhouse API and send them to our kafka topic.

## Usage

Get the API key from the Blockhouse API and install the package using pip:

```bash
pip install blockhouse
```

Using as a Python Library

```python
from blockhouse import TransferData

td = TransferData(api_key="b19f7dff001b9d9d4f6feb6797d9762d")
res = td.transfer_data()
print(res)
```

## Available Functions:

- TransferData: Fetch trade data from the Blockhouse API and send them to our kafka topic.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Support

If you encounter any issues or have questions, feel free to open email us.

## Changelog

Version 1.0.4
Initial release with:
Refactored code and used api_key to call the API.
