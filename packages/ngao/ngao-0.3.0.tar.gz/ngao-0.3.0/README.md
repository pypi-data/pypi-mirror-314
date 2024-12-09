ngao - tunnel local ports to public URLs and inspect traffic

USAGE:
  ngao [command] [flags]

AUTHOR:
  ngao - <support@ngao.pro>

COMMANDS: 
  config          update or migrate ngao's configuration file
  http            start an HTTP tunnel
  tcp             start a TCP tunnel
  tunnel          start a tunnel for use with a tunnel-group backend

EXAMPLES: 
  ngao http 80                                                 # secure public URL for port 80 web server
  ngao http --domain baz.ngao.dev 8080                        # port 8080 available at baz.ngao.dev
  ngao tcp 22                                                  # tunnel arbitrary TCP traffic to port 22
  ngao http 80 --oauth=google --oauth-allow-email=foo@foo.com  # secure your app with oauth

Paid Features: 
  ngao http 80 --domain mydomain.com                           # run ngao with your own custom domain
  ngao http 80 --allow-cidr 2600:8c00::a03c:91ee:fe69:9695/32  # run ngao with IP policy restrictions
  Upgrade your account at https://dashboard.ngao.pro/billing/subscription to access paid features

Upgrade your account at https://dashboard.ngao.pro/billing/subscription to access paid features

Flags:
  -h, --help      help for ngao

Use "ngao [command] --help" for more information about a command.
