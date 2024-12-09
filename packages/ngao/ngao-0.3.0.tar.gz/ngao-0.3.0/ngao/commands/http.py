def add_http_command(subparsers):
    parser = subparsers.add_parser("http", help="Start an HTTP tunnel")
    parser.add_argument("port", type=int, help="Local port to expose")
    parser.add_argument("--domain", type=str, help="Custom domain (paid feature)")
    parser.add_argument("--oauth", type=str, help="Enable OAuth")
    parser.set_defaults(func=handle_http)

def handle_http(args):
    print(f"Starting HTTP tunnel for port {args.port}")
    if args.domain:
        print(f"Using custom domain: {args.domain}")
    if args.oauth:
        print(f"OAuth enabled: {args.oauth}")
