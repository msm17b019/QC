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
            self.myvpc_id = self.myvpc.id

    def check_virtual_private_cloud(self, tags: list, cidr: str) -> bool:
        """This method checks if the virtual private cloud exists with given name and tags.

        Args:
            tags (list): tags to add to the vpc
            cidr (str): CIDR block

        Returns:
            bool: False if it exists. True if it doesn't. 
        """
        for vpc in self.ec2_client.describe_vpcs()['Vpcs']:
            if cidr == vpc['CidrBlock'] and tags[0] in vpc['Tags'] and tags[1] in vpc['Tags']:
                self.myvpc_id = vpc['VpcId']
                return False
        else:
            return True

    def create_and_attach_internet_gateway(self, tags: list) -> None:
        """This method creates and attaches an internet gateway with the vpc created.

        Args:
            tags (list): tags to add to an internet gateway.
        """
        if self.check_internet_gateway(tags):
            self.igw = self.ec2_resource.create_internet_gateway()
            self.igw.create_tags(Tags=tags)
            self.igw_id = self.igw.id

        if self.check_igw_attached_to_vpc():
            self.ec2_client.attach_internet_gateway(InternetGatewayId=self.igw_id, VpcId=self.myvpc_id)

    def check_internet_gateway(self, tags: list) -> bool:
        """This method checks if an internet gateway exists with the given tags.

        Args:
            tags (list): tags to find if the internet gateway exists with the same tags.
        """
        for igw in self.ec2_client.describe_internet_gateways()['InternetGateways']:
            if tags[0] in igw['Tags'] and tags[1] in igw['Tags']:
                self.igw_id = igw['InternetGatewayId']
                return False
        else:
            return True

    def check_igw_attached_to_vpc(self) -> bool:
        """This method checks if internet gateway is attached to vpc or not.

        Returns:
            bool: False if internet gateway is attached to vpc, else True.
        """
        for igw in self.ec2_client.describe_internet_gateways()['InternetGateways']:
            if self.igw_id == igw['InternetGatewayId']:
                if igw['Attachments'] == []:
                    return True
                else:
                    return False
        else:
            return False
                
    def create_public_route_table(self, tags: list) -> None:
        """This method creates public route table.

        Args:
            tags (list): Tags to add to the public route table
        """
        if self.check_public_route_table(tags):
            self.public_rt = self.ec2_resource.create_route_table(VpcId=self.myvpc_id)
            self.public_rt.create_tags(Tags=tags)
            self.public_rt_id = self.public_rt.id
            self.public_rt.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=self.igw_id
            )

    def check_public_route_table(self, tags: list) -> bool:
        """This method checks whether public route table is created or not.

        Args:
            tags (list): Tags to find the route table created.

        Returns:
            bool: False if public route table exists, else True.
        """
        for prt in self.ec2_client.describe_route_tables()['RouteTables']:
            if tags[0] in prt['Tags'] and tags[1] in prt['Tags']:
                self.public_rt_id = prt['RouteTableId']
                return False
        else:
            return True
        
    def create_public_subnet(self, cidr: str, availability_zone: str, tags: list) -> None:
        """This method creates public subnet.

        Args:
            cidr (str): The CIDR block of subnet.
            availability_zone (str): Subnet will be created in that AZ.
            tags (list): Tags to add to the subnet.
        """

        if self.check_public_subnet(tags):
            self.public_subnet = self.ec2_resource.create_subnet(CidrBlock=cidr, VpcId=self.myvpc_id,AvailabilityZone=availability_zone)
            self.public_subnet.create_tags(Tags=tags)
            self.ec2_client.associate_route_table(RouteTableId=self.public_rt_id, SubnetId=self.public_subnet.id)

    def check_public_subnet(self, tags: list) -> bool:
        """This method checks if public subnet exists.

        Args:
            cidr (str): The CIDR block of subnet.
            availability_zone (str): Subnet availability zone.
            tags (list): Tags of the subnet.

        Returns:
            bool: False if public subnet exists, else True.
        """
        for pub_subnet in self.ec2_client.describe_subnets()['Subnets']:
            if pub_subnet['VpcId'] == self.myvpc_id:
                if tags[0] in pub_subnet['Tags'] and tags[1] in pub_subnet['Tags']:
                    return False
        else:
            return True
        
    def create_nat_gateway(self, tags: list) -> None:
        """This method creates an NAT gateway.

        Args:
            tags (list): tags to add to the nat gateway.
        """
        if self.check_nat_gateway(tags):
            elastic_ip = self.ec2_client.allocate_address(Domain='vpc', TagSpecifications=[{'ResourceType': 'elastic-ip', 'Tags': tags},])
            for pub_subnet in self.ec2_client.describe_subnets()['Subnets']:
                if pub_subnet['VpcId'] == self.myvpc_id:
                    if {'Key': 'Name', 'Value': 'QubePublicSubnet1'} in pub_subnet['Tags'] and {'Key': 'Product', 'Value': 'challenge'} in pub_subnet['Tags']:
                        self.pub_sub1_id = pub_subnet['SubnetId']
                        break
            tags = tags + [{'Key': 'Name', 'Value': 'QubeNG'}]
            self.nat_gw = self.ec2_client.create_nat_gateway(SubnetId=self.pub_sub1_id, AllocationId=elastic_ip['AllocationId'], TagSpecifications=[{'ResourceType': 'natgateway', 'Tags': tags},])
            self.ec2_client.get_waiter('nat_gateway_available').wait(
                NatGatewayIds=[self.nat_gw['NatGateway']['NatGatewayId']])
            self.nat_gw_id = self.nat_gw['NatGateway']['NatGatewayId']

    def check_nat_gateway(self, tags: list) -> bool:
        """This method checks if NAT gateway is already created.

        Args:
            tags (list): Tags to find if the NAT already created.

        Returns:
            bool: False if NAT exists, else True.
        """
        tags_to_find = []
        tags_to_find = tags.copy()
        tags_to_find = tags_to_find + [{'Key': 'Name', 'Value': 'QubeNG'}]
        for ng in self.ec2_client.describe_nat_gateways()['NatGateways']:
            if tags_to_find[0] in ng['Tags'] and tags_to_find[1] in ng['Tags']:
                self.nat_gw_id = ng['NatGatewayId']
                return False
        else:
            return True
        
    def create_private_route_table(self, tags: list) -> None:
        """This method creates a private route table.

        Args:
            tags (list): Tags to add to the private route table.
        """
        if self.check_private_route_table(tags):
            self.private_rt = self.ec2_resource.create_route_table(VpcId=self.myvpc_id)
            self.private_rt.create_tags(Tags=tags)
            self.private_rt_id = self.private_rt.id
            self.private_rt.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                NatGatewayId=self.nat_gw_id
            )

    def check_private_route_table(self, tags: list) -> bool:
        """This method checks whether private route table is created or not.

        Args:
            tags (list): Tags to find the route table created.

        Returns:
            bool: False if private route table exists, else True.
        """
        for prt in self.ec2_client.describe_route_tables()['RouteTables']:
            if tags[0] in prt['Tags'] and tags[1] in prt['Tags']:
                self.private_rt_id = prt['RouteTableId']
                return False
        else:
            return True
        
    def create_private_subnet(self, cidr: str, availability_zone: str, tags: list) -> None:
        """This method creates private subnet.

        Args:
            cidr (str): The CIDR block of subnet.
            availability_zone (str): Subnet will be created in that AZ.
            tags (list): Tags to add to the subnet.
        """

        if self.check_private_subnet(tags):
            self.private_subnet = self.ec2_resource.create_subnet(CidrBlock=cidr, VpcId=self.myvpc_id,AvailabilityZone=availability_zone)
            self.private_subnet.create_tags(Tags=tags)
            self.ec2_client.associate_route_table(RouteTableId=self.private_rt_id, SubnetId=self.private_subnet.id)

    def check_private_subnet(self, tags: list) -> bool:
        """This method checks if private subnet exists.

        Args:
            cidr (str): The CIDR block of subnet.
            availability_zone (str): Subnet availability zone.
            tags (list): Tags of the subnet.

        Returns:
            bool: False if private subnet exists, else True.
        """
        for private_subnet in self.ec2_client.describe_subnets()['Subnets']:
            if private_subnet['VpcId'] == self.myvpc_id:
                if tags[0] in private_subnet['Tags'] and tags[1] in private_subnet['Tags']:
                    return False
        else:
            return True

    def create_alb_security_group(self, name: str, desc: str, tags: list) -> str:
        """This method creates security group for application load balancer.

        Args:
            name (str): Name of the security group.
            desc (str): Description for the security group.
            tags (list): Tags to add to the security group.

        Returns:
            str: The security group id.
        """
        if self.check_alb_security_group(name):
            sg = self.ec2_client.create_security_group(
                GroupName=name,
                Description=desc,
                VpcId=self.myvpc_id,
                TagSpecifications=[{'ResourceType': 'security-group', 'Tags': tags},]
            )

            self.group_id = sg['GroupId']

            self.ec2_client.authorize_security_group_ingress(
                GroupId=self.group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            return self.group_id

    
    def check_alb_security_group(self, name: str) -> bool:
        """This method checks if security group is there for alb or not.

        Args:
            name (str): Name of the security group to check.

        Returns:
            bool: False if alb security group exists, else True.
        """
        for sg in self.ec2_client.describe_security_groups()['SecurityGroups']:
            if sg['GroupName'] == name:
                self.group_id = sg['GroupId']
                return False
        else:
            return True
        
    def create_asg_security_group(self, name: str, desc: str, tags: list) -> str:
        """This method creates security group for application load balancer.

        Args:
            name (str): Name of the security group.
            desc (str): Description for the security group.
            tags (list): Tags to add to the security group.

        Returns:
            str: The security group id.
        """
        if self.check_asg_security_group(name):
            sg = self.ec2_client.create_security_group(
                GroupName=name,
                Description=desc,
                VpcId=self.myvpc_id,
                TagSpecifications=[{'ResourceType': 'security-group', 'Tags': tags},]
            )

            self.asg_sgid = sg['GroupId']

            self.ec2_client.authorize_security_group_ingress(
                GroupId=self.asg_sgid,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80, 
                        'UserIdGroupPairs': [
                            {
                                'GroupId': self.group_id
                            }
                        ]
                    }
                ]
            )
            return self.asg_sgid
    
    def check_asg_security_group(self, name: str) -> bool:
        """This method checks if security group is there for asg or not.

        Args:
            name (str): Name of the security group to check.

        Returns:
            bool: False if asg security group exists, else True.
        """
        for sg in self.ec2_client.describe_security_groups()['SecurityGroups']:
            if sg['GroupName'] == name:
                self.asg_sgid = sg['GroupId']
                return False
        else:
            return True