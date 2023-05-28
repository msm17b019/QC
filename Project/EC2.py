class Ec2:
    def __init__(self,ec2_client):
        """Class that represents Amazon EC2 service.

        Args:
            ec2_client : EC2 client to create, manage and configure AWS EC2 service at low level
        """
        self.ec2_client=ec2_client