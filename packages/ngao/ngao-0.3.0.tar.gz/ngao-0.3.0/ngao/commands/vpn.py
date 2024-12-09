def add_vpn_command(subparsers):
    parser = subparsers.add_parser("vpn", help="Start or manage a VPN tunnel")
    parser.add_argument("action", choices=["start", "stop", "status"], help="Action to perform")
    parser.set_defaults(func=handle_vpn)

def handle_vpn(args):
    if args.action == "start":
        print("Starting VPN tunnel...")
    elif args.action == "stop":
        print("Stopping VPN tunnel...")
    elif args.action == "status":
        print("Fetching VPN status...")
