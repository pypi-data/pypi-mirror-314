def add_udp_command(subparsers):
    parser = subparsers.add_parser("udp", help="Start a UDP tunnel")
    parser.add_argument("port", type=int, help="Local port to expose")
    parser.set_defaults(func=handle_udp)

def handle_udp(args):
    print(f"Starting UDP tunnel for port {args.port}")
