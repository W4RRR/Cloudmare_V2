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

> 🔧 **This version includes:** Python 3 compatibility fixes, automatic dependency installation, and performance improvements.

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

# Usage example
python Cloudmare_V2.py -u target.site --bruter -sC -sSh -sSt --host verified.site
```

### Main Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL |
| `--bruter` | Bruteforce to find associated domains |
| `--subbruter` | Subdomain bruteforce |
| `-sC, --search-censys` | Search using Censys API |
| `-sSh, --search-shodan` | Search using Shodan API |
| `-sSt, --search-st` | Search using SecurityTrails API |
| `--random-agent` | Random User-Agent |
| `-o, --output` | Save found subdomains |

## 📱 Termux Users

```bash
pkg upgrade && pkg update
pkg install git python libxml2 libxslt dnsutils
git clone https://github.com/W4RRR/Cloudmare_V2.git
cd Cloudmare_V2
python Cloudmare_V2.py -h
```

## ✅ Compatibility

- ✅ Python 3.7+
- ✅ Windows
- ✅ Linux
- ✅ macOS
- ✅ Termux (Android)

## ✨ Changes in V2

- 🔄 Full Python 3 compatibility
- 📦 Automatic dependency installation
- 🛠️ Removed obsolete dependencies (six)
- ⚡ Performance improvements
- 🐛 Fixed import errors

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
