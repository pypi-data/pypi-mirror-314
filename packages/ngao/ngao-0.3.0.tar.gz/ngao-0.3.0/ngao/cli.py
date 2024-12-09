import argparse
from ngao.commands import config, http, tcp, udp, vpn, subdomain, billing, secure

def main():
    parser = argparse.ArgumentParser(
        description="Ngao - Tunnel local ports to public URLs , Get Vpn Services , Tcp and RDP and inspect traffic",
        usage="""
  ngao [command] [flags]

COMMANDS:
  config          update or migrate ngao's configuration file
  http            start an HTTP tunnel
  tcp             start a TCP tunnel
  udp             start a UDP tunnel
  vpn             start a VPN tunnel
  subdomain       manage subdomains
  billing         manage billing and subscriptions

EXAMPLES:
  ngao http 80                                                 # secure public URL for port 80 web server
  ngao http --domain baz.ngao.dev 8080                        # port 8080 available at baz.ngao.dev
  ngao tcp 22                                                  # tunnel arbitrary TCP traffic to port 22
  ngao udp 53                                                  # tunnel UDP traffic to port 53
  ngao vpn start                                               # start a VPN tunnel
  ngao subdomain add mysub.ngao.dev                           # add a subdomain
  ngao billing --phone +1234567890                            # manage billing for phone +1234567890
""",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command", help="Available commands")

    # Add subcommands
    config.add_config_command(subparsers)
    http.add_http_command(subparsers)
    tcp.add_tcp_command(subparsers)
    udp.add_udp_command(subparsers)
    vpn.add_vpn_command(subparsers)
    subdomain.add_subdomain_command(subparsers)
    billing.add_billing_command(subparsers)
    secure.add_secure_command(subparsers)  # Add secure command

    # Parse the arguments and call the corresponding function
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
