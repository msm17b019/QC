class Ec2:
    def __init__(self,ec2_client):
        """Class that represents Amazon EC2 service.

        Args:
            ec2_client : EC2 client to create, manage and configure AWS EC2 service at low level
        """
        self.ec2_client=ec2_client

    def create_launch_template(self, name: str, tags: list, sg: list, pvt_sub: str):
        self.ec2_client.create_launch_template(
            LaunchTemplateName=name,
            LaunchTemplateData={
                'IamInstanceProfile': {
                    'Arn': 'string',
                    'Name': 'string'
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
                'KeyName': 'string',
                'Monitoring': {
                    'Enabled': False
                },
                'UserData': 'string',
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