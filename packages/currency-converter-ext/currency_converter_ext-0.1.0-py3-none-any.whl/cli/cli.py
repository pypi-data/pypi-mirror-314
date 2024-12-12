"""
Currency Converter CLI Application

Demonstrates usage of the CurrencyConverter library.
"""

import sys
import platform
import os
from typing import Optional

from currency_converter.main import CurrencyConverter, CurrencyConverterError

def clear_screen() -> None:
    """Clear the console screen in a platform-independent way"""
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

def get_input(prompt: str, valid_range: Optional[range] = None) -> str:
    """Get and validate user input"""
    while True:
        try:
            value = input(prompt)
            if valid_range:
                num_value = int(value)
                if num_value in valid_range:
                    return value
                print(f"Please enter a number between {min(valid_range)} and {max(valid_range)}.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")

def display_menu() -> str:
    """Display main menu and get user choice"""
    clear_screen()
    print("\n╔════════════════════════╗")
    print("║   Currency Converter   ║")
    print("╠════════════════════════╣")
    print("║ 1. Convert Currency    ║")
    print("║ 2. Update Rates        ║")
    print("║ 3. View Current Rates  ║")
    print("║ 4. Exit                ║")
    print("╚════════════════════════╝")
    return get_input("Enter your choice (1-4): ", range(1, 5))

def display_currency_menu(converter: CurrencyConverter, prompt: str) -> str:
    """Display currency selection menu"""
    print("\nAvailable Currencies:")
    for i, currency in enumerate(converter.currencies, 1):
        print(f"║ {i}. {currency} ║")
    print("╚════════════════════════╝")
    
    choice = int(get_input(f"{prompt} (1-{len(converter.currencies)}): ", 
                            range(1, len(converter.currencies) + 1)))
    return converter.currencies[choice - 1]

def get_amount() -> float:
    """Get and validate amount input"""
    while True:
        try:
            amount = float(input("Enter amount to convert: "))
            if amount > 0:
                return amount
            print("Please enter a positive amount.")
        except ValueError:
            print("Please enter a valid number.")

def display_current_rates(converter: CurrencyConverter) -> None:
    """Display current exchange rates"""
    clear_screen()
    rates_info = converter.rates_info
    
    print("\nCurrent Exchange Rates")
    print("═" * 40)
    print(f"Base Currency: {rates_info['base_currency']}")
    print(f"Last Updated: {rates_info['last_updated']}")
    print(f"Source: {rates_info['source']}")
    print("─" * 40)
    
    for currency, rate in rates_info['rates'].items():
        if currency != rates_info['base_currency']:
            print(f"{rates_info['base_currency']} → {currency}: {rate:.4f}")
    
    print("═" * 40)
    input("\nPress Enter to continue...")

def main():
    """Main application loop"""
    try:
        # Initialize the converter with USD as base currency
        converter = CurrencyConverter()
        
        while True:
            choice = display_menu()
            
            if choice == '1':  # Convert Currency
                try:
                    base_currency = display_currency_menu(converter, "Select base currency")
                    target_currency = display_currency_menu(converter, "Select target currency")
                    amount = get_amount()
                    precision = int(get_input("Enter decimal precision (1-4): ", range(1, 5)))
                    
                    print("\nSelect locale format:")
                    print("1. US-style (1,234.56)")
                    print("2. Euro-style (1.234,56)")
                    locale_choice = get_input("Enter choice (1-2): ", range(1, 3))
                    locale = 'en' if locale_choice == '1' else 'eu'
                    
                    result = converter.convert(amount, base_currency, target_currency, precision, locale)
                    print(f"\n{amount} {base_currency} = {result}")
                    input("\nPress Enter to continue...")
                    
                except CurrencyConverterError as ve:
                    print(f"Error: {ve}")
                    input("\nPress Enter to continue...")
                    
            elif choice == '2':  # Update Rates
                converter.refresh_rates()
                input("\nPress Enter to continue...")
                
            elif choice == '3':  # View Current Rates
                display_current_rates(converter)
                
            elif choice == '4':  # Exit
                clear_screen()
                print("Thank you for using the Currency Converter!")
                sys.exit(0)
                
    except KeyboardInterrupt:
        clear_screen()
        print("\nProgram terminated by user.")
        sys.exit(0)

def run_cli():
    """Entry point for CLI"""
    main()