def add_billing_command(subparsers):
    parser = subparsers.add_parser("billing", help="Manage billing and subscriptions")
    parser.add_argument("--phone", required=True, help="Phone number with country code (e.g., +1234567890)")
    parser.set_defaults(func=handle_billing)

def handle_billing(args):
    if args.phone.startswith("+") and args.phone[1:].isdigit():
        print(f"Managing billing for phone: {args.phone}")
    else:
        print("Invalid phone number format. Ensure it starts with '+' followed by digits.")
