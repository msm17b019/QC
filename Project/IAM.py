import json

class Iam:
    def __init__(self, iam_client) -> None:
        """Class that represents AWS IAM services.

        Args:
            iam_client : IAM client to create, manage and configure AWS IAM service at low level
        """
        self.iam_client = iam_client

    def create_instance_profile(self, name: str, tags: list) -> str:
        """This method creates an IAM instance profile.

        Args:
            name (str): Name of the instance profile.
            tags (list): tags to add to the instance profile.

        Returns:
            str: Return the instance profile id.
        """
        if self.check_instance_profile(name):
            self.ip = self.iam_client.create_instance_profile(
                InstanceProfileName=name,
                Tags=tags           
            )

            waiter = self.iam_client.get_waiter('instance_profile_exists')
            waiter.wait(InstanceProfileName=name)

            self.ip_id = self.ip['InstanceProfile']['InstanceProfileId']

            assume_role_policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            self.role = self.iam_client.create_role(
                RoleName="QubeRole",
                AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
                Tags=tags
            )

            self.iam_role_name = "QubeRole"

            self.iam_client.add_role_to_instance_profile(
                InstanceProfileName=name,
                RoleName="QubeRole"
            )

        return self.ip_id

    def check_instance_profile(self, name: str) -> bool:
        """This method checks if instance profile exists with the given name.

        Args:
            name (str): Name of the instance profile to check.

        Returns:
            bool: Return False if instance profile exists, else True.
        """
        for ip in self.iam_client.list_instance_profiles(PathPrefix='/')['InstanceProfiles']:
            if name == ip['InstanceProfileName']:
                self.iam_role_name = ip['Roles'][0]['RoleName']
                self.ip_id = ip['InstanceProfileId']
                return False
        else:
            return True

    def create_add_iam_policy_to_role(self, name: str, tags: list, asg_arn: str):
        """This method creates and attaches IAM policy to the IAM role.

        Args:
            name (str): Name of the IAM policy.
            tags (list): Tags to add to the IAM policy.
            asg_arn (str): Auto scaling group arn.
        """
        policy_json = {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Sid": "AllowAccessToKMS",
                "Effect": "Allow",
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey",
                    "kms:ListKeys"
                ],
                "Resource": '*'
                }
            ]
            }

        if self.check_iam_policy(name):
            self.policy = self.iam_client.create_policy(
                PolicyName=name,
                PolicyDocument=json.dumps(policy_json),
                Tags=tags
            )

            self.iam_client.attach_role_policy(
                RoleName=self.iam_role_name,
                PolicyArn=self.policy['Policy']['Arn']
            )
    
    def check_iam_policy(self, name: str) -> bool :
        """This method checks if IAM policy is attached to IAM role.

        Args:
            name (str): Name to check for the IAM policy.

        Returns:
            bool: Return False if IAM policy is attached to role, else True.
        """
        try:
            for policy in self.iam_client.list_attached_role_policies(RoleName=self.iam_role_name)['AttachedPolicies']:
                if name == policy['PolicyName']:
                    return False
            else:
                return True
        except:
            return True
