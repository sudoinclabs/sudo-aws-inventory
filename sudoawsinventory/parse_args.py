import argparse

def parse_args(args=None):
    parser = argparse.ArgumentParser(
                        description='Run Inventory on AWS account.')

    parser.add_argument('--regions',
                        default=[],
                        nargs='+',
                        help='Name of regions to include, defaults to all')

    parser.add_argument('--services', default=[], nargs='+',
                        help='Name of AWS services to include')

    parser.add_argument('--exclude-services', dest='excluded_services',
                        default=[],
                        nargs='+',
                        help='Name of AWS services to exclude')

    parser.add_argument('--list-services',
                        action='store_true',
                        help=('Validate and print services'))

    parser.add_argument('--list-actions',
                        action='store_true',
                        help='Validate services and print service actions')

    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug messages')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print the account resources to stdout')

    parser.add_argument('--version',
                        action='store_true',
                        help='Print version')

    parsed = parser.parse_args(args)

    return parsed