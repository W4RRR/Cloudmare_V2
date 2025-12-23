#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Results module for Cloudmare_V2
Handles collection and export of scan results including WAF IPs and real IPs.
"""

import json
import csv
import os
from datetime import datetime

from .colors import good, bad, info, tab, warn, G, R, Y, W


class ScanResults:
    """
    Collects and manages scan results including domains, WAF IPs, and real IPs.
    """
    
    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.scan_date = datetime.now().isoformat()
        self.results = []
        self.summary = {
            'total_subdomains': 0,
            'protected_by_waf': 0,
            'potential_real_ips': 0,
            'errors': 0
        }
    
    def add_result(self, subdomain, waf_ip=None, real_ip=None, waf_provider=None, status='unknown'):
        """
        Add a scan result.
        
        Args:
            subdomain: The subdomain/host being scanned
            waf_ip: IP address of the WAF/CDN (if protected)
            real_ip: Potential real/origin IP address
            waf_provider: Name of WAF provider (cloudflare, sucuri, incapsula)
            status: 'protected', 'exposed', 'error', 'unknown'
        """
        result = {
            'subdomain': subdomain,
            'waf_ip': waf_ip,
            'real_ip': real_ip,
            'waf_provider': waf_provider,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        # Update summary
        self.summary['total_subdomains'] += 1
        if status == 'protected':
            self.summary['protected_by_waf'] += 1
        elif status == 'exposed':
            self.summary['potential_real_ips'] += 1
        elif status == 'error':
            self.summary['errors'] += 1
    
    def get_protected_domains(self):
        """Get all domains protected by WAF."""
        return [r for r in self.results if r['status'] == 'protected']
    
    def get_exposed_domains(self):
        """Get all domains with potential real IPs exposed."""
        return [r for r in self.results if r['status'] == 'exposed']
    
    def get_real_ips(self):
        """Get unique list of potential real IPs."""
        ips = set()
        for r in self.results:
            if r['real_ip']:
                ips.add(r['real_ip'])
        return list(ips)
    
    def save_json(self, filepath):
        """Save results to JSON file."""
        data = {
            'target_domain': self.target_domain,
            'scan_date': self.scan_date,
            'summary': self.summary,
            'results': self.results
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"{tab}{good}Results saved to: {G}{filepath}{W}")
    
    def save_csv(self, filepath):
        """Save results to CSV file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(['Subdomain', 'WAF IP', 'Real IP', 'WAF Provider', 'Status'])
            # Data
            for r in self.results:
                writer.writerow([
                    r['subdomain'],
                    r['waf_ip'] or '',
                    r['real_ip'] or '',
                    r['waf_provider'] or '',
                    r['status']
                ])
        
        print(f"{tab}{good}Results saved to: {G}{filepath}{W}")
    
    def save_txt(self, filepath):
        """Save results to formatted text file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"CLOUDMARE_V2 SCAN RESULTS\n")
            f.write(f"Target: {self.target_domain}\n")
            f.write(f"Date: {self.scan_date}\n")
            f.write("=" * 70 + "\n\n")
            
            # Summary
            f.write("SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Subdomains Scanned: {self.summary['total_subdomains']}\n")
            f.write(f"Protected by WAF: {self.summary['protected_by_waf']}\n")
            f.write(f"Potential Real IPs: {self.summary['potential_real_ips']}\n")
            f.write(f"Errors: {self.summary['errors']}\n\n")
            
            # Protected domains
            protected = self.get_protected_domains()
            if protected:
                f.write("PROTECTED BY WAF\n")
                f.write("-" * 40 + "\n")
                for r in protected:
                    f.write(f"  {r['subdomain']}\n")
                    f.write(f"    WAF IP: {r['waf_ip']}\n")
                    f.write(f"    Provider: {r['waf_provider']}\n\n")
            
            # Exposed domains (potential real IPs)
            exposed = self.get_exposed_domains()
            if exposed:
                f.write("POTENTIAL REAL IPs (NOT PROTECTED)\n")
                f.write("-" * 40 + "\n")
                for r in exposed:
                    f.write(f"  {r['subdomain']}\n")
                    f.write(f"    Real IP: {r['real_ip']}\n\n")
            
            # Unique real IPs
            real_ips = self.get_real_ips()
            if real_ips:
                f.write("UNIQUE REAL IPs FOUND\n")
                f.write("-" * 40 + "\n")
                for ip in real_ips:
                    f.write(f"  {ip}\n")
        
        print(f"{tab}{good}Results saved to: {G}{filepath}{W}")
    
    def save(self, base_filepath, formats=None):
        """
        Save results in multiple formats.
        
        Args:
            base_filepath: Base path without extension (e.g., 'data/output/results-example')
            formats: List of formats to save ('json', 'csv', 'txt'). Defaults to all.
        """
        if formats is None:
            formats = ['json', 'csv', 'txt']
        
        for fmt in formats:
            if fmt == 'json':
                self.save_json(f"{base_filepath}.json")
            elif fmt == 'csv':
                self.save_csv(f"{base_filepath}.csv")
            elif fmt == 'txt':
                self.save_txt(f"{base_filepath}.txt")
    
    def print_summary(self):
        """Print a summary of the results to console."""
        print(f"\n{info}Scan Summary for {Y}{self.target_domain}{W}")
        print(f"{tab}Total Subdomains: {self.summary['total_subdomains']}")
        print(f"{tab}Protected by WAF: {R}{self.summary['protected_by_waf']}{W}")
        print(f"{tab}Potential Real IPs: {G}{self.summary['potential_real_ips']}{W}")
        
        real_ips = self.get_real_ips()
        if real_ips:
            print(f"\n{info}Unique Real IPs Found:")
            for ip in real_ips:
                print(f"{tab}{good}{ip}")


# Global results instance
_current_results = None


def init_results(target_domain):
    """Initialize a new results collection for a scan."""
    global _current_results
    _current_results = ScanResults(target_domain)
    return _current_results


def get_results():
    """Get the current results instance."""
    global _current_results
    return _current_results


def add_result(subdomain, waf_ip=None, real_ip=None, waf_provider=None, status='unknown'):
    """Add a result to the current scan."""
    global _current_results
    if _current_results:
        _current_results.add_result(subdomain, waf_ip, real_ip, waf_provider, status)

