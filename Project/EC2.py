class Ec2:
    def __init__(self,ec2_client):
        """Class that represents Amazon EC2 service.

        Args:
            ec2_client : EC2 client to create, manage and configure AWS EC2 service at low level
        """
        self.ec2_client=ec2_client

    def create_launch_template(self, name: str, iam_ip_name: str, tags: list, sg: list, pvt_sub: str) -> str:
        """This method creates launch template.

        Args:
            name (str): Name of the launch template.
            iam_ip_name (str): IAM instance profile.
            tags (list): tags to add to the launch template.
            sg (list): security groups.
            pvt_sub (str): private subnet.

        Returns:
            str: Return launch template id.
        """
        if self.check_launch_template(name):
            self.lt = self.ec2_client.create_launch_template(
                LaunchTemplateName=name,
                LaunchTemplateData={
                    'IamInstanceProfile': {
                        'Name': iam_ip_name
                    },
                    'NetworkInterfaces': [
                        {
                            'AssociatePublicIpAddress': False,
                            'Groups': [
                                sg,
                            ],
                            'SubnetId': pvt_sub,
                        },
                    ],
                    'ImageId': 'ami-078efad6f7ec18b8a',
                    'Monitoring': {
                        'Enabled': False
                    },
                    'UserData': 'IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQp5dW0gaW5zdGFsbCAteSBodHRwZAplY2hvICJoZWxsb3dvcmxkIiA+IC9vcHQvbGF1bmNoZmlsZQplY2hvICJIZWxsbyB3b3JsZCBweXRob24iID4gL3Zhci93d3cvaHRtbC9pbmRleC5odG1sCnNlcnZpY2UgaHR0cGQgc3RhcnQK',
                    'TagSpecifications': [
                        {
                            'ResourceType': 'launch-template',
                            'Tags': tags
                        },
                    ],
                    'SecurityGroupIds': [
                        sg,
                    ],
                    'InstanceRequirements': {
                        'VCpuCount': {
                            'Min': 2,
                            'Max': 2
                        },
                        'MemoryMiB': {
                            'Min': 4000,
                            'Max': 4200
                        },
                    },
                },
                TagSpecifications=[
                    {
                        'ResourceType': 'launch-template',
                        'Tags': tags
                    },
                ]
            )

            self.lt_id = self.lt['LaunchTemplate']['LaunchTemplateId']

        return self.lt_id

    def check_launch_template(self, name: str) -> bool:
        """This method checks if launch template exists with the given name.

        Args:
            name (str): The name of the launch template to find.

        Returns:
            bool: Return False if launch template with the given name exists, else True.
        """
        for lt in self.ec2_client.describe_launch_templates():
            if name == lt['LaunchTemplates']['LaunchTemplateName']:
                self.lt_id = lt['LaunchTemplates']['LaunchTemplateId']
                return False
        else:
            return True