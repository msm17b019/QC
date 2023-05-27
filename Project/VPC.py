class Vpc:
    def __init__(self, ec2_resource, ec2_client):
        """ Class that respresents Amazon VPC

        Args:
            ec2_resource : EC2 resource to create, manage and configure AWS EC2 service at high level
            ec2_client : EC2 client to create, manage and configure AWS EC2 service at low level
        """
        self.ec2_resource = ec2_resource 
        self.ec2_client = ec2_client

    def create_virtual_private_cloud(self, tags: list, cidr: str) -> None:
        """This method creates virtual private cloud with given tags and cidr range.

        Args:
            tags (list): tags to add to the vpc
            cidr (str): CIDR block
        """
        if self.check_virtual_private_cloud(tags, cidr):
            self.myvpc = self.ec2_resource.create_vpc(CidrBlock=cidr)
            self.myvpc.create_tags(Tags=tags)
            self.myvpc.wait_until_available()

    def check_virtual_private_cloud(self, tags: list, cidr: str) -> bool:
        """This method checks if the virtual private cloud exists with given name and tags.

        Args:
            tags (list): tags to add to the vpc
            cidr (str): CIDR block

        Returns:
            bool: True if it exists. False if it doesn't. 
        """
        for vpc in self.ec2_client.describe_vpcs()['Vpcs']:
            if cidr == vpc['CidrBlock'] and vpc['Tags'] == tags:
                return False
        else:
            return True

    def create_internet_gateway(self, tags: list) -> None:
        """This method creates an internet gateway with the given tags.

        Args:
            tags (list): tags to add to an internet gateway.
        """
        if self.check_internet_gateway(tags):
            self.igw = self.ec2_resource.create_internet_gateway()
            self.igw.create_tags(Tags=tags)

    def check_internet_gateway(self, tags: list) -> bool:
        """This method checks if an internet gateway exists with the given tags.

        Args:
            tags (list): tags to find if the internet gateway exists with the same tags.
        """
        for igw in self.ec2_client.describe_internet_gateways()['InternetGateways']:
            if tags == igw['Tags']:
                return False
        else:
            return True
