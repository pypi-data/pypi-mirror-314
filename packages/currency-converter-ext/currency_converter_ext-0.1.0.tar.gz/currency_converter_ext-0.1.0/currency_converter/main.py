"""
Currency Converter Library

This module provides a comprehensive currency conversion utility 
with support for multiple currencies and local formatting.
"""

import json
import os
import platform
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

class CurrencyConverterError(Exception):
    """Custom exception for Currency Converter related errors"""
    pass

class CurrencyConverter:
    """
    A flexible currency converter that supports multiple currencies 
    and provides robust error handling and caching.
    """
    
    def __init__(self, base_currency: str = 'USD'):
        """
        Initialize the currency converter.
        
        :param base_currency: The base currency for conversions (default: USD)
        """
        # Supported currencies 
        self.currencies = [
            "USD", "EUR", "UGX", "KES", 
            "GBP", "JPY", "CHF", "CAD", 
            "AUD", "NZD", "CNY", "INR", 
            "BRL", "ZAR"
        ]
        
        # Validate base currency
        if base_currency not in self.currencies:
            raise CurrencyConverterError(f"Unsupported base currency: {base_currency}")
        
        self.BASE_URL = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        self.BASE_CURRENCY = base_currency
        self.CACHE_DURATION = timedelta(hours=24)
        
        # Use platform-independent path handling
        self.app_dir = self._get_app_directory()
        self.rates_file = self.app_dir / 'exchange_rates.json'
        
        # Ensure app directory exists
        self.app_dir.mkdir(parents=True, exist_ok=True)
        
        # Load exchange rates
        self.exchange_rates = self._load_exchange_rates()
        
    def _get_app_directory(self) -> Path:
        """Get the appropriate application directory based on OS"""
        system = platform.system().lower()
        
        if system == 'windows':
            app_dir = Path(os.getenv('APPDATA')) / 'CurrencyConverter'
        elif system == 'darwin':  # macOS
            app_dir = Path.home() / 'Library' / 'Application Support' / 'CurrencyConverter'
        else:  # Linux and other Unix-like systems
            app_dir = Path.home() / '.currencyconverter'
            
        return app_dir
        
    def _load_exchange_rates(self) -> Dict:
        """Load exchange rates from cache file"""
        try:
            if self.rates_file.exists():
                with open(self.rates_file, 'r', encoding='utf-8') as file:
                    rates = json.load(file)
                    
                    # Check if rates are stale
                    last_updated = datetime.fromisoformat(rates['last_updated'])
                    if datetime.now() - last_updated > self.CACHE_DURATION:
                        return self._fetch_latest_rates()
                    return rates
            else:
                return self._fetch_latest_rates()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading rates: {e}")
            return self._get_fallback_rates()
            
    def _save_exchange_rates(self, rates: Dict) -> None:
        """Save exchange rates to cache file"""
        try:
            with open(self.rates_file, 'w', encoding='utf-8') as file:
                json.dump(rates, file, indent=2)
        except IOError as e:
            print(f"Error saving rates: {e}")
            
    def _get_fallback_rates(self) -> Dict:
        """Provide fallback rates in case of API failure"""
        return {
            self.BASE_CURRENCY: 1.0,
            "USD": 1.0 if self.BASE_CURRENCY != "USD" else 1.0,
            "EUR": 0.85,
            "UGX": 3700.0,
            "KES": 110.0,
            "GBP": 0.79,
            "JPY": 110.0,
            "CHF": 0.91,
            "CAD": 1.25,
            "AUD": 1.33,
            "NZD": 1.41,
            "CNY": 6.45,
            "INR": 73.5,
            "BRL": 5.2,
            "ZAR": 14.3,
            "last_updated": datetime.now().isoformat(),
            "source": "fallback"
        }
        
    def _fetch_latest_rates(self) -> Dict:
        """Fetch latest exchange rates from the API"""
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = {
                self.BASE_CURRENCY: 1.0,
                **{curr: data["rates"][curr] for curr in self.currencies if curr != self.BASE_CURRENCY},
                "last_updated": datetime.now().isoformat(),
                "source": "api"
            }
            
            self._save_exchange_rates(rates)
            return rates
            
        except requests.RequestException as e:
            print(f"Error fetching rates from API: {e}")
            return self._get_fallback_rates()
            
    def convert(self, amount: float, from_currency: str, to_currency: str, 
                precision: int = 2, locale: str = 'en') -> str:
        """
        Convert amount between currencies.
        
        :param amount: Amount to convert
        :param from_currency: Source currency code
        :param to_currency: Target currency code
        :param precision: Number of decimal places
        :param locale: Formatting locale (en or eu)
        :return: Formatted converted amount
        """
        if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
            raise CurrencyConverterError("Invalid currency code.")
            
        # Get the exchange rates
        from_rate = self.exchange_rates[from_currency]
        to_rate = self.exchange_rates[to_currency]
        
        # Calculate converted amount
        converted_amount = (amount / from_rate) * to_rate
        
        # Format the result
        return self._format_currency(converted_amount, to_currency, precision, locale)
        
    def _format_currency(self, amount: float, currency_code: str, 
                         precision: int, locale: str) -> str:
        """
        Format currency amount according to locale.
        
        :param amount: Amount to format
        :param currency_code: Currency code
        :param precision: Number of decimal places
        :param locale: Formatting locale
        :return: Formatted currency string
        """
        symbols = {
            "USD": "$", "EUR": "€", "UGX": "USh", "KES": "KSh",
            "GBP": "£", "JPY": "¥", "CHF": "CHF", "CAD": "CA$",
            "AUD": "A$", "NZD": "NZ$", "CNY": "¥", "INR": "₹",
            "BRL": "R$", "ZAR": "R"
        }
        
        symbol = symbols.get(currency_code, currency_code)
        formatted_amount = round(amount, precision)
        
        if locale == 'en':
            return f"{symbol}{formatted_amount:,.{precision}f}"
        elif locale == 'eu':
            return f"{symbol}{formatted_amount:,.{precision}f}".replace(",", " ").replace(".", ",")
        else:
            return f"{symbol}{formatted_amount:.{precision}f}"
            
    def refresh_rates(self) -> None:
        """
        Manually refresh exchange rates.
        """
        try:
            new_rates = self._fetch_latest_rates()
            self.exchange_rates = new_rates
            print("Exchange rates updated successfully!")
            print(f"Source: {new_rates.get('source', 'unknown')}")
            
        except Exception as e:
            print(f"Error refreshing rates: {e}")

    @property
    def rates_info(self) -> Dict:
        """
        Get current rates information.
        
        :return: Dictionary with rates and metadata
        """
        return {
            'base_currency': self.BASE_CURRENCY,
            'last_updated': self.exchange_rates.get('last_updated', 'Unknown'),
            'source': self.exchange_rates.get('source', 'Unknown'),
            'rates': {k: v for k, v in self.exchange_rates.items() 
                      if k not in ['last_updated', 'source']}
        }