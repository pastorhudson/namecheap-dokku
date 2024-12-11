# Namecheap DNS Subdomain Updater

This Python script updates or adds specific DNS records (e.g., `A` records) for subdomains in Namecheap without overwriting other existing DNS records. It leverages the Namecheap API to ensure precise control over DNS management.

---

## Features

- Updates existing DNS records for specified subdomains.
- Adds new subdomain DNS records if they don’t already exist.
- Preserves all other DNS records during the update process.
- Uses a configuration file (`config.ini`) for credentials and domain/subdomain management.
- Supports dynamic IP address updates via command-line arguments.

---

## Requirements

- Python 3.7+
- Namecheap API enabled for your account.
- API credentials from your Namecheap account.

---

## Setup

### 1. Enable Namecheap API

1. Log in to your Namecheap account.
2. Navigate to **Profile > Tools > API Access**.
3. Enable API access and add your public IP address to the whitelist.

---

### 2. Install Dependencies

Install the required Python modules:
```bash
pip install requests
```

---

### 3. Configure `config.ini`

Create a `config.ini` file in the project directory with the following structure:

```ini
[NamecheapAPI]
api_user = your_api_username
api_key = your_api_key
username = your_account_username
client_ip = your_client_ip

[Domains]
subdomains = home:pastorhudson.com, www:example.com, @:example.org
```

- Replace placeholders with your Namecheap API credentials and domains.
- Use the format `subdomain:domain` in the `subdomains` list.

---

### 4. Usage

Run the script with the desired IP address as a command-line argument:
```bash
python main.py <new_ip_address>
```

#### Example:
```bash
python main.py 192.168.1.1
```

This updates or adds the specified subdomains to point to `192.168.1.1`.

---

## How It Works

1. **Retrieve Existing Records**:
   - Fetches all DNS records for the domain using `namecheap.domains.dns.getHosts`.

2. **Update/Add Subdomains**:
   - Updates the record if the subdomain exists.
   - Adds a new record if the subdomain does not exist.

3. **Submit Updated Records**:
   - Sends all records (unchanged and updated) back to Namecheap via `namecheap.domains.dns.setHosts`.

---

## Example Output

```plaintext
Updating DNS record for home.pastorhudson.com with IP 192.168.1.1
DNS record updated successfully for home.pastorhudson.com.

Updating DNS record for www.example.com with IP 192.168.1.1
DNS record updated successfully for www.example.com.

Updating DNS record for example.org with IP 192.168.1.1
DNS record updated successfully for example.org.
```

---

## Troubleshooting

### Common Issues:

1. **Invalid Subdomain Entries**:
   - Ensure `config.ini` has correctly formatted `subdomains` (`subdomain:domain`).

2. **API Access Error**:
   - Verify that your client IP is whitelisted in Namecheap’s API settings.

3. **Namespace Errors**:
   - Ensure you are using the latest version of the script, which handles XML namespaces correctly.

---

## Contributing

Feel free to contribute to this project! Fork the repository and submit a pull request with your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Namecheap for providing a robust API for domain management.
- Python community for powerful libraries like `requests` and `ElementTree`.

