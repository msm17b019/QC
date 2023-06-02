class Ec2:
    def __init__(self,ec2_client):
        """Class that represents Amazon EC2 service.

        Args:
            ec2_client : EC2 client to create, manage and configure AWS EC2 service at low level
        """
        self.ec2_client=ec2_client

    def create_launch_template(self, name: str, iam_ip_name: str, tags: list, sg: list) -> str:
        """This method creates launch template.

        Args:
            name (str): Name of the launch template.
            iam_ip_name (str): IAM instance profile.
            tags (list): tags to add to the launch template.
            sg (list): security groups.

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
                    'ImageId': 'ami-078efad6f7ec18b8a',
                    'KeyName': 'QubeKey',
                    'Monitoring': {
                        'Enabled': False
                    },
                    'UserData': 'IyEvYmluL2Jhc2gKeXVtIGluc3RhbGwgaHR0cGQgLXkKc2VydmljZSBodHRwZCBzdGFydApjaGtjb25maWcgaHR0cGQgb24KbWtkaXIgLXAgL3Zhci93d3cvaHRtbC93b3JsZHNvZ29vZAplY2hvICJIZWxsbyB3b3JsZCBweXRob24iID4gL3Zhci93d3cvaHRtbC93b3JsZHNvZ29vZC9pbmRleC5odG1sCg==',
                    'SecurityGroupIds': sg,
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
        for lt in self.ec2_client.describe_launch_templates()['LaunchTemplates']:
            if name == lt['LaunchTemplateName']:
                self.lt_id = lt['LaunchTemplateId']
                return False
        else:
            return True
        
    def create_key(self, tags: list) -> None:
        """This method creates key pair.

        Args:
            tags (list): Tags to add to the key pair.
        """
        if self.check_key_pair():
            self.kp = self.ec2_client.create_key_pair(
                KeyName = 'QubeKey',
                KeyType = 'rsa',
                KeyFormat = 'pem',
                TagSpecifications=[
                        {
                            'ResourceType': 'key-pair',
                            'Tags': tags
                        },
                    ],
            )

            # Save the private key to a file
            with open('QubeKey.pem', 'w') as key_file:
                key_file.write(self.kp['KeyMaterial'])

    def check_key_pair(self) -> bool:
        """This method checks if key pair with name QubeKey already exists.

        Returns:
            bool: Return False if already exists, else True.
        """
        for key in self.ec2_client.describe_key_pairs()['KeyPairs']:
            if "QubeKey" == key['KeyName']:
                return False
        else:
            return True
