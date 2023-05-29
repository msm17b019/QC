class Iam:
    def __init__(self, iam_client) -> None:
        """Class that represents AWS IAM services.

        Args:
            iam_client : IAM client to create, manage and configure AWS IAM service at low level
        """
        self.iam_client = iam_client

    def create_instance_profile(self, name: str, tags: list):
        """This method creates an IAM instance profile.

        Args:
            name (str): Name of the instance profile.
            tags (list): tags to add to the instance profile.
        """
        self.ip = self.iam_client.create_instance_profile(
            InstanceProfileName=name,
                Tags=tags           
        )

        self.iam_role_name = self.ip['InstanceProfile']['Roles']['RoleName']

    def check_instance_profile(self, name: str) -> bool:
        """This method checks if instance profile exists with the given name.

        Args:
            name (str): Name of the instance profile to check.

        Returns:
            bool: Return False if instance profile exists, else True.
        """
        for ip in self.iam_client.list_instance_profiles(PathPrefix='/')['InstanceProfiles']:
            if name == ip['InstanceProfileName']:
                self.iam_role_name = ip['Roles']['RoleName']
                return False
        else:
            return True

    def create_add_iam_policy_to_role(self, name: str, tags: list, aws_account_id: str, asg_id: str, asg_name: str):
        """This method creates and attaches IAM policy to the IAM role.

        Args:
            name (str): Name of the IAM policy.
            tags (list): Tags to add to the IAM policy.
            aws_account_id (str): AWS account ID.
            asg_id (str): Auto scaling group ID.
            asg_name (str): Auto scaling group name.
        """
        policy_json = {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Sid": "AllowAccessFromASG",
                "Effect": "Allow",
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey",
                ],
                "Resource": '*',
                "Condition": {
                    "StringEquals": {
                    "aws:SourceArn": f"arn:aws:autoscaling:ap-south-1:{aws_account_id}:autoScalingGroup:{asg_id}:autoScalingGroupName/{asg_name}"
                    }
                }
                },
                {
                "Sid": "DenyAccessFromOtherEntities",
                "Effect": "Deny",
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:DescribeKey"
                ],
                "Resource": '*'
                }
            ]
            }

        self.policy = self.iam_client.create_policy(
            PolicyName=name,
            PolicyDocument=policy_json,
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
                if name in policy['PolicyName']:
                    return False
            else:
                return True
        except:
            return True
