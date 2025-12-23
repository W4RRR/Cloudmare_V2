# Cloudmare_V2

```
   _____ _                 _                        __      _____  
  / ____| |               | |                       \ \    / /__ \ 
 | |    | | ___  _   _  __| |_ __ ___   __ _ _ __ ___\ \  / /  ) |
 | |    | |/ _ \| | | |/ _` | '_ ` _ \ / _` | '__/ _ \\ \/ /  / / 
 | |____| | (_) | |_| | (_| | | | | | | (_| | | |  __/ \  /  / /_ 
  \_____|_|\___/ \__,_|\__,_|_| |_| |_|\__,_|_|  \___|  \/  |____|
```

**Cloudmare_V2** is an enhanced tool to find origin servers of websites protected by Cloudflare, Sucuri, or Incapsula with misconfigured DNS.

> 🔧 **This version includes:** Python 3 compatibility fixes, automatic dependency installation, modern TLS configuration, and performance improvements.

## 🚀 Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/W4RRR/Cloudmare_V2.git

# 2. Navigate to the folder
cd Cloudmare_V2

# 3. Run (dependencies are installed automatically)
python Cloudmare_V2.py -h
```

### Manual Dependency Installation (optional)

```bash
pip install -r requirements.txt
```

## 💻 Usage

```bash
# Basic help
python Cloudmare_V2.py -h

# Full help
python Cloudmare_V2.py -hh

# Basic usage example
python Cloudmare_V2.py -u target.site

# Full scan with all options
python Cloudmare_V2.py -u target.site --random-agent --bruter -sC -sSh -sSt

# With delay between requests (recommended to avoid rate limiting)
python Cloudmare_V2.py -u target.site --random-agent --delay 1.0-2.5
```

## 📋 Main Options

### Target Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL (required) |
| `--disable-sublister` | Disable subdomain enumeration |
| `--bruter` | Bruteforce to find associated domains |
| `--subbruter` | Subdomain bruteforce using subbrute module |

### Request Options

| Option | Description |
|--------|-------------|
| `--user-agent` | Set custom User-Agent header |
| `--random-agent` | Use random User-Agent for each request |
| `--host` | Set custom HTTP Host header |
| `--headers` | Set custom headers (e.g. "Origin: example.com, ETag: 123") |
| `--ignore-redirects` | Ignore HTTP redirections |
| `--threads` | Max concurrent requests (default: 30) |
| `--delay` | Random delay between requests (e.g. "1.0-2.5" for 1-2.5 seconds) |

### Search Options (API Integration)

| Option | Description |
|--------|-------------|
| `-sC, --search-censys` | Search using Censys API |
| `-sSh, --search-shodan` | Search using Shodan API |
| `-sSt, --search-st` | Search using SecurityTrails API |

### Output Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Save subdomains to file |
| `--oG, --output-good` | Save only valid subdomains |
| `--oI, --output-ip` | Save subdomain IPs |

## 🔑 API Configuration

Configure your API keys in `data/APIs/api.conf`:

```ini
[VTOTAL]
api_key = your_virustotal_api_key

[CENSYS]
api_id = your_censys_id
secret = your_censys_secret

[SHODAN]
api_key = your_shodan_api_key

[SECURITYTRAILS]
api_key = your_securitytrails_api_key
```

> **Note:** API keys should be entered without quotes.

## 📱 Termux Users

```bash
pkg upgrade && pkg update
pkg install git python libxml2 libxslt dnsutils
git clone https://github.com/W4RRR/Cloudmare_V2.git
cd Cloudmare_V2
python Cloudmare_V2.py -h
```

## ✅ Compatibility

- ✅ Python 3.7 - 3.13
- ✅ Windows
- ✅ Linux (Kali, Ubuntu, Debian, etc.)
- ✅ macOS
- ✅ Termux (Android)

## ✨ Changes in V2

### Latest Updates
- 🔒 **Modern TLS Configuration** - Uses browser-like TLS fingerprint to avoid WAF blocking
- ⏱️ **Request Delay** - New `--delay` parameter to add random delays between requests
- 🛡️ **Better Error Handling** - Descriptive error messages instead of cryptic "None" errors
- 🔐 **Smart Credential Management** - Only asks to delete API keys on actual authentication errors
- 🌐 **Browser-like Headers** - Requests now include realistic browser headers

### Core Improvements
- 🔄 Full Python 3 compatibility (including Python 3.13)
- 📦 Automatic dependency installation
- 🛠️ Removed obsolete dependencies
- ⚡ Performance improvements
- 🐛 Fixed import and SSL errors

## 🔧 Troubleshooting

### SSL Errors
If you encounter SSL handshake errors, the tool now automatically uses modern TLS configuration. If problems persist, try:
```bash
python Cloudmare_V2.py -u target.site --delay 2.0-4.0
```

### Rate Limiting
If you're getting blocked or receiving errors, use the delay option:
```bash
python Cloudmare_V2.py -u target.site --delay 1.5-3.0
```

### API Errors
- Make sure your API keys are correctly configured in `data/APIs/api.conf`
- API keys should be entered without quotes
- Some APIs have rate limits - use `--delay` to avoid hitting them

## 🙏 Credits

| | |
|---|---|
| **Original Creator** | MrH0wl (2018-2019) |
| **Redesigned by** | .W4R (2025) |

### Original Contact
- 📧 Email: secmare@protonmail.com
- 🐦 Twitter: @mrh0wl

## 📝 License

GPL v3.0

---

<p align="center">
  <b>Cloudmare_V2</b> - CloudProxy & Reverse Proxy Bypass Tool - Enhanced Edition<br>
  <a href="https://github.com/W4RRR/Cloudmare_V2">https://github.com/W4RRR/Cloudmare_V2</a>
</p>
