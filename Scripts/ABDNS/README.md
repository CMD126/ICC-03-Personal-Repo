# ABDNS.py

`ABDNS.py` is a Python script designed for managing and automating DNS-related tasks. It provides functionalities such as querying DNS records, updating entries, and monitoring DNS changes. The script is modular and can be integrated into larger network automation workflows.

## Features

- Query DNS records (A, AAAA, CNAME, MX, etc.)
- Update and manage DNS entries
- Monitor DNS changes and notify users
- Command-line interface for ease of use
- Supports running with elevated privileges for operations requiring administrative access

## Usage

Some DNS management operations may require administrative privileges. To run the script with elevated permissions, use `sudo`:

```bash
sudo python ABDNS.py [options]
```

### Example

```bash
sudo python ABDNS.py --query example.com
```

## Requirements

- Python 3.x
- `dnspython` library (install with `pip install dnspython`)

## Configuration

Edit the configuration section in `ABDNS.py` to set DNS server details and notification preferences.

## License

This project is licensed under the MIT License.

