# SUDO AWS Inventory

SUDO AWS Inventory is used by SUDO internal CMDB to collect AWS Inventory. The OSS version is stripped of internal details but its fully functional and can collect AWS inventory for all known AWS services.

The Inventory tool supports detecting the supported regions and querying them.


Pre Requisites
--------------

- Python 3.8
- botocore
- User with readonly permissions

CLI Examples
---------------

- Collect inventory

`$ python sudoawsinventory.py`

* List supported services.

`$ python sudoawsinventory.py --list-services`

- List actions for enabled services.

`$ python aws_inventory.py --list-operations`

License
-------

MIT

Acknowledgements
----------------
Inspiration was taken from: https://github.com/nccgroup/aws-inventory