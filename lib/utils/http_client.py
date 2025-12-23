#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom HTTP client with modern TLS configuration to avoid WAF blocking.
Uses cipher suites and settings that mimic modern browsers.
"""

import ssl
import random

import thirdparty.requests as requests
import thirdparty.urllib3 as urllib3
from thirdparty.urllib3.util.ssl_ import create_urllib3_context

urllib3.disable_warnings()

# Modern cipher suites that mimic Chrome/Firefox
MODERN_CIPHERS = [
    'TLS_AES_128_GCM_SHA256',
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-CHACHA20-POLY1305',
    'ECDHE-RSA-AES128-SHA',
    'ECDHE-RSA-AES256-SHA',
    'AES128-GCM-SHA256',
    'AES256-GCM-SHA384',
    'AES128-SHA',
    'AES256-SHA',
]

# Browser-like User-Agents
BROWSER_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
]


class TLSAdapter(requests.adapters.HTTPAdapter):
    """
    Custom HTTPS adapter that uses modern TLS settings to avoid WAF detection.
    """
    
    def __init__(self, *args, **kwargs):
        self.ssl_context = self._create_ssl_context()
        super().__init__(*args, **kwargs)
    
    def _create_ssl_context(self):
        """Create SSL context with modern cipher suites."""
        try:
            # Try to create a modern SSL context
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.set_ciphers(':'.join(MODERN_CIPHERS))
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            # Enable TLS 1.2 and 1.3
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            return ctx
        except Exception:
            # Fallback to default context if custom fails
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx
    
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)


def get_browser_headers(user_agent=None):
    """Get headers that mimic a real browser."""
    ua = user_agent or random.choice(BROWSER_USER_AGENTS)
    return {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }


def create_session(use_tls_adapter=True):
    """
    Create a requests session with modern TLS configuration.
    
    Args:
        use_tls_adapter: If True, use custom TLS adapter to avoid WAF blocking
    
    Returns:
        requests.Session configured with modern TLS settings
    """
    session = requests.Session()
    
    if use_tls_adapter:
        adapter = TLSAdapter()
        session.mount('https://', adapter)
        session.mount('http://', adapter)
    
    # Set default headers to mimic browser
    session.headers.update(get_browser_headers())
    
    return session


def safe_get(url, timeout=10, **kwargs):
    """
    Make a GET request with modern TLS settings and error handling.
    
    Args:
        url: URL to request
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.get
    
    Returns:
        Response object or None if request failed
    """
    try:
        session = create_session()
        kwargs.setdefault('timeout', timeout)
        kwargs.setdefault('verify', False)
        return session.get(url, **kwargs)
    except Exception:
        return None


def safe_post(url, timeout=10, **kwargs):
    """
    Make a POST request with modern TLS settings and error handling.
    
    Args:
        url: URL to request
        timeout: Request timeout in seconds
        **kwargs: Additional arguments passed to requests.post
    
    Returns:
        Response object or None if request failed
    """
    try:
        session = create_session()
        kwargs.setdefault('timeout', timeout)
        kwargs.setdefault('verify', False)
        return session.post(url, **kwargs)
    except Exception:
        return None

