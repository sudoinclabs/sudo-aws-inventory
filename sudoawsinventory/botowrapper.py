from botocore.session import Session as BotoSession
import aws_services
import logging



class Session(BotoSession):
    """Session class for boto sesison."""
    def __init__(self, logger=None):
        super(Session, self).__init__()
        self.logger = logger or logging.getLogger(__name__)

        if self.user_agent_name == 'Botocore':
            botocore_info = 'Botocore/{0}'.format(
                self.user_agent_version)
            if self.user_agent_extra:
                self.user_agent_extra += ' ' + botocore_info
            else:
                self.user_agent_extra = botocore_info
            self.user_agent_name = 'SUDOAWSInventory'


    def create_client(self, service, **kwargs):
        self.logger.debug(service)
        client =  super(Session, self).create_client(service, **kwargs)
        try:
            self.logger.debug("Loading client wrapper")
            client = getattr(aws_services, service).ClientWrapper(self, client, logger=self.logger)
        except AttributeError:
            # Custom wrapper not defined
            pass
        return client

