# Namecheap DNS Subdomain Updater

This Python script updates or adds specific DNS records (e.g., `A` records) for subdomains in Namecheap without overwriting other existing DNS records. It leverages the Namecheap API to ensure precise control over DNS management.

---

## Features

- Updates existing DNS records for specified subdomains.
- Adds new subdomain DNS records if they don’t already exist.
- Preserves all other DNS records during the update process.
- Uses a configuration file (`config.ini`) for credentials and domain/subdomain management.
- Automatically retrieves the current WAN IP address.

---

## Requirements

- Python 3.7+
- Namecheap API enabled for your account.
- API credentials from your Namecheap account.
- Internet connection.

---

## Setup

### 1. Enable Namecheap API

1. Log in to your Namecheap account.
2. Navigate to **Profile > Tools > API Access**.
3. Enable API access and add your public IP address to the whitelist.

---

### 2. Configure `config.ini`

Create a `config.ini` file in the project directory with the following structure:

```ini
[NamecheapAPI]
api_user = your_api_username
api_key = your_api_key
username = your_account_username
client_ip = your_client_ip

[Domains]
subdomains = mysub:mydomain.com, www:example.com, @:example.org
```

- Replace placeholders with your Namecheap API credentials and domains.
- Use the format `subdomain:domain` in the `subdomains` list.

---

### 3. Usage

Run the script directly. The script automatically fetches the current WAN IP and updates the specified subdomains:

```bash
python update_namecheap.py
```

---

## How It Works

1. **Retrieve Existing Records**:
   - Fetches all DNS records for the domain using `namecheap.domains.dns.getHosts`.

2. **Update/Add Subdomains**:
   - Updates the record if the subdomain exists.
   - Adds a new record if the subdomain does not exist.

3. **Submit Updated Records**:
   - Sends all records (unchanged and updated) back to Namecheap via `namecheap.domains.dns.setHosts`.

4. **WAN IP Retrieval**:
   - Fetches the current WAN IP using `https://api.ipify.org`.

---

## Example Output

```plaintext
Updating DNS record for mysub.mydomain.com with IP 203.0.113.42
DNS record updated successfully for mysub.mydomain.com.

Updating DNS record for www.example.com with IP 203.0.113.42
DNS record updated successfully for www.example.com.

Updating DNS record for example.org with IP 203.0.113.42
DNS record updated successfully for example.org.
```

---
To run this script every hour using a cron job, follow these steps:

1. **Make the Script Executable**:
   Ensure the script is executable by running:
   ```bash
   chmod +x update_namecheap.py
   ```

2. **Edit the Crontab**:
   Open the crontab editor:
   ```bash
   crontab -e
   ```

3. **Add the Cron Job**:
   Add the following line to execute the script every hour:
   ```bash
   0 * * * * /usr/bin/python3 /path/to/update_namecheap.py >> /path/to/logfile.log 2>&1
   ```
   - Replace `/usr/bin/python3` with the path to your Python interpreter.
   - Replace `/path/to/update_namecheap.py` with the full path to your script.
   - Replace `/path/to/logfile.log` with the path to your desired log file.

4. **Save and Exit**:
   Save the file and exit the editor. The cron job will now run the script at the start of every hour.

5. **Check Logs**:
   Monitor the log file to ensure the script executes correctly and logs any errors or outputs.

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
- Python community for powerful libraries like `http.client` and `ElementTree`. 

--- 
