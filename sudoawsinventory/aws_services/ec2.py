import logging

class ClientWrapper(object):
    """Client Wrapper for EC2."""
    def __init__(self, session, client, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.debug("Custom client init: ec2")
        self.session = session
        self.client = client

    def __getattr__(self, name, *args):
        method = getattr(self.client, name)
        return method

    def describe_images(self, **kwargs):
        self.logger.debug("Custom describe images")
        if not kwargs.keys():
            kwargs['ExecutableUsers'] = ['self']
        return self.client.describe_images(**kwargs)