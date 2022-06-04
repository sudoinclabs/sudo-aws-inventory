#!/usr/bin/env python
import helpers
from awsapi import AWSApi
from parse_args import parse_args

__version__ = "1.0"

logger = helpers.SUDOLogger(name="any_name")


def main(options):
    logger.setLevel(options.debug)

    if options.version:
        print(__version__)
        return

    aws_api = AWSApi(options.regions, options.services, options.excluded_services, logger=logger)


    if options.list_services:
        print('\n'.join(sorted(aws_api.enabled_services)))
        return

    for service in aws_api.enabled_services:
        if options.list_actions:
            actions = '\n'.join(aws_api.aws_services[service]['actions'])
            print(f'[{service}]\n{actions}')
            return

    logger.debug(aws_api.enabled_services)
    aws_api.fetch_inventory()

    aws_api.write_json()

if __name__ == '__main__':
    main(parse_args())
