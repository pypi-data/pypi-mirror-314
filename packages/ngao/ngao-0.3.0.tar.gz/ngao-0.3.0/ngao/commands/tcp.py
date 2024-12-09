def add_tcp_command(subparsers):
    parser = subparsers.add_parser("tcp", help="Start a TCP tunnel")
    parser.add_argument("port", type=int, help="Local port to expose")
    parser.set_defaults(func=handle_tcp)

def handle_tcp(args):
    print(f"Starting TCP tunnel for port {args.port}")
