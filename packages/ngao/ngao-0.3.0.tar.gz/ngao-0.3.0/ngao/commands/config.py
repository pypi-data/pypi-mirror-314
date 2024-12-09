from ngao.commands.utils import make_request

def add_config_command(subparsers):
    parser = subparsers.add_parser("config", help="Update or migrate ngao's configuration file")
    parser.add_argument("--key", required=True, help="Configuration key to update")
    parser.add_argument("--value", required=True, help="New value for the key")
    parser.set_defaults(func=handle_config)

def handle_config(args):
    print(f"Updating configuration: {args.key} = {args.value}")
    response = make_request("console", "/api/config", method="POST", data={"key": args.key, "value": args.value})
    print(f"Configuration updated: {response}")

