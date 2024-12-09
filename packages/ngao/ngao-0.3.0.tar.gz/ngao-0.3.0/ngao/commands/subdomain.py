def add_subdomain_command(subparsers):
    parser = subparsers.add_parser("subdomain", help="Manage subdomains")
    parser.add_argument("action", choices=["add", "remove", "list"], help="Action to perform")
    parser.add_argument("subdomain", nargs="?", help="Subdomain to add or remove (e.g., mysub.ngao.dev)")
    parser.set_defaults(func=handle_subdomain)

def handle_subdomain(args):
    if args.action == "add" and args.subdomain:
        print(f"Adding subdomain: {args.subdomain}")
    elif args.action == "remove" and args.subdomain:
        print(f"Removing subdomain: {args.subdomain}")
    elif args.action == "list":
        print("Listing all subdomains...")
    else:
        print("Invalid subdomain command. Use --help for usage.")
