class Asg:
    def __init__(self,as_client) -> None:
        """Class that represents AWS autoscaling services.

        Args:
            as_client : Client to create, manage and configure AWS autoscaling service at low level
        """
        self.as_client = as_client

    def create_asg(self, name: str, lt_id: str, pvt_sub: str, tg_arn: list, tags: list) -> str:
        """This method creates an autoscaling group.

        Args:
            name (str): Name of the autoscaling group.
            lt_id (str): Id of the launch template.
            pvt_sub (str): Private subnet ID.
            tags (list): Tags to add to the autoscaling group.

        Returns:
            str: Return the created autoscaling group ARN.
        """
        if self.check_asg(name):
            self.asg = self.as_client.create_auto_scaling_group(
                AutoScalingGroupName=name,
                LaunchTemplate={
                    'LaunchTemplateId': lt_id,
                    'Version': '$Latest',
                },
                MaxSize=1,
                MinSize=1,
                VPCZoneIdentifier=pvt_sub,
                TargetGroupARNs=tg_arn,
                Tags=tags,
            )

        return self.asg_arn

    def check_asg(self, name: str) -> bool:
        """This method checks if the asg exists or not with the given name.

        Args:
            name (str): Name of the autoscaling aroup.

        Returns:
            bool: False if 
        """
        for asg in self.as_client.describe_auto_scaling_groups()['AutoScalingGroups']:
            if name == asg['AutoScalingGroupName']:
                self.asg_arn = asg['AutoScalingGroupARN']
                return False
        else:
            return True