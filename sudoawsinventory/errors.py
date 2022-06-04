class Error(Exception):
    __module__ = 'sudoawsinventory'

class InvalidServiceException(Error):
    __module__ = 'sudoawsinventory'

    def __init__(self, service_name):
        if (type(service_name) == type([])):
            service_name = ', '.join(service_name)
        message = f'Invalid Service: {service_name}'
        super().__init__(message)

class InvalidRegionException(Error):
    __module__ = 'sudoawsinventory'

    def __init__(self, region_name):
        if (type(region_name) == type([])):
            region_name = ', '.join(region_name)
        message = f'Invalid Region: {region_name}'
        super().__init__(message)
