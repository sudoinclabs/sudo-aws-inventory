from curses.has_key import has_key
import botocore
from botowrapper import Session
from errors import Error, InvalidServiceException, InvalidRegionException
import json
import logging

class AWSApi(object):
    """docstring for AWSApi."""
    def __init__(self, regions, services, excluded_services, logger=None):
        super(AWSApi, self).__init__()

        self.regions = regions

        self.requested_services = services
        self.excluded_services = excluded_services

        self.logger = logger or logging.getLogger(__name__)

        self.boto_session = Session(logger=self.logger)

        self.get_aws_services()
        self.validate_services()
        self.validate_regions()
        self.get_actions()


    def get_aws_services(self):

        self.logger.debug('Fetching AWS Services')

        available_services = self.boto_session.get_available_services()

        aws_services = {}
        for service in available_services:
            available_regions = self.boto_session.get_available_regions(service)
            aws_services[service] = {'regions': available_regions}

            if available_regions:
                self.logger.debug('{0: <20} -> {1}.'.format(service,', '.join(available_regions)))
            else:
                self.logger.debug('{0: <20} -> Global service.'.format(service))


        self.aws_services = aws_services
        return aws_services

    def validate_services(self, services=None, excluded_services=None):
        available_services = self.aws_services.keys()

        if not services:
            services = self.requested_services

        if not excluded_services:
            excluded_services = self.excluded_services

        if services:
            invalid_included_services = [service for service in services if service not in available_services]
            if invalid_included_services:
                raise InvalidServiceException(invalid_included_services)
        else:
            services = available_services

        if excluded_services:
            invalid_excluded_services = [service for service in excluded_services if service not in available_services]
            if invalid_excluded_services:
                raise InvalidServiceException(invalid_excluded_services)

            services = [service for service in services if service not in excluded_services]

        self.enabled_services = services

    def validate_regions(self, regions=None):
        if not regions:
            regions = self.regions

        available_regions = set()
        for service in self.enabled_services:
            available_regions.update(self.aws_services[service]['regions'])

        invalid_regions = [region for region in regions if region not in available_regions]
        if invalid_regions:
            raise InvalidRegionException(invalid_regions)

    def get_actions(self):

        for service in self.enabled_services:
            actions = []
            # fetch actions from boto
            api_version = self.boto_session.get_config_variable('api_versions').get(service, None)
            service_model = self.boto_session.get_service_model(service, api_version=api_version)


            for action in service_model.operation_names:
                action_name = action.lower()
                if action_name.startswith('list') or action_name.startswith('describe'):
                    operation_model = service_model.operation_model(action)

                    try:
                        if not operation_model.input_shape.required_members:
                            actions.append(action)
                    except AttributeError:
                        # no input shape
                        actions.append(action)


            self.aws_services[service]['actions'] = actions

    def fetch_inventory(self):
        session = self.boto_session

        self.sts = session.create_client(
            'sts'
        )
        self.logger.debug(self.sts.get_caller_identity())

        self.json = {}

        for service in self.enabled_services:
            self.json[service] = {}
            actions = self.aws_services[service]['actions']
            regions = self.aws_services[service]['regions']

            # call each API across each region
            api_version = session.get_config_variable('api_versions').get(service, None)

            for region in regions:
                self.json[service][region] = {}
                client = session.create_client(
                    service,
                    region_name=region,
                    api_version=api_version,
                )
                for action in actions:
                    aws_op = botocore.xform_name(action)

                    self.logger.debug('[%s][%s] API "%s". Function name "%s".',
                             region,
                             service,
                             action,
                             aws_op)

                    response = None
                    try:
                        if client.can_paginate(aws_op):
                            paginator = client.get_paginator(aws_op)
                            response = paginator.paginate().build_full_result()
                        else:
                            response = getattr(client, aws_op)()
                    except botocore.exceptions.ClientError:
                        # The operation not yet supported for the service in the region
                        # There is not much we can do about it.
                        pass
                    except client.exceptions.AccessDeniedException as e:
                        self.logger.debug(e)
                    finally:
                        if not response:
                            response = {}
                        if "ResponseMetadata" in response.keys():
                            del response["ResponseMetadata"]
                        for key in response.keys():
                            if response[key]:
                                self.json[service][region][action] = response

    def write_json(self, results="output.json"):
        json_object = json.dumps(self.json, indent=4, default=str)

        with open(results, "w") as outfile:
            outfile.write(json_object)