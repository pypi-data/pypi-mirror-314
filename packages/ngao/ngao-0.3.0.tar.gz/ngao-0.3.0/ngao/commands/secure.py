import socket
import os
import ngiri
import phonenumbers

def add_secure_command(subparsers):
    parser = subparsers.add_parser("secure", help="Pentest and secure an IP")
    group = parser.add_mutually_exclusive_group(required=True)
    
    # Secure IP Address
    group.add_argument("--ip", help="IP address to test security")
    
    # Secure Phone Number
    group.add_argument("--phone", help="Phone number to test security")
    
    parser.set_defaults(func=handle_secure)

def handle_secure(args):
    if args.ip:
        print(f"Starting security checks for IP address: {args.ip}")
        check_ip_security(args.ip)
    elif args.phone:
        print(f"Starting security checks for phone number: {args.phone}")
        check_phone_security(args.phone)

def check_ip_security(ip):
    # Simple example: Check if the IP address is reachable (ping)
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        print(f"{ip} is reachable. Starting vulnerability scan...")

        # Example: Port scanning (just checking common ports)
        common_ports = [80, 443, 22, 21, 53]
        for port in common_ports:
            check_port(ip, port)
    else:
        print(f"{ip} is not reachable. Skipping scan.")

def check_port(ip, port):
    try:
        sock = socket.create_connection((ip, port), timeout=3)
        print(f"Port {port} is OPEN on {ip}")
        sock.close()
    except socket.error:
        print(f"Port {port} is CLOSED on {ip}")

def check_phone_security(phone):
    try:
        # Check if the phone number is valid (basic validation)
        parsed_phone = phonenumbers.parse(phone)
        if phonenumbers.is_valid_number(parsed_phone):
            print(f"Phone number {phone} is valid.")
            # Further phone security checks can be added here (e.g., checking for spam/robocalls)
        else:
            print(f"Phone number {phone} is invalid.")
    except phonenumbers.phonenumberutil.NumberParseException:
        print(f"Error parsing phone number {phone}. Ensure it is correctly formatted.")
