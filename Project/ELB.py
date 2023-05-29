class Elb:
    def __init__(self, elbv2_client) -> None:
        """Class that represents amazon elastic load balancer services.

        Args:
            elbv2_client : client to create, manage and configure AWS ELB service at low level
        """
        self.elbv2_client = elbv2_client

    def create_elb(self, name: str, pub_sub: list, tags: list, elb_sg: str):
        """This method creates application load balancer.

        Args:
            name (str): Name of the load balancer.
            pub_sub (list): Public subnets.
            tags (list): Tags to add to the load balancers.
            elb_sg (str): Security group ID.
        """
        if self.checl_elb(name):
            self.elbv2_client.create_load_balancer(
                Name=name,
                Subnets=pub_sub,
                SecurityGroups=[
                    elb_sg,
                ],
                Scheme='internet-facing',
                Tags=tags,
                Type='application',
                IpAddressType='ipv4',
            )

    def checl_elb(self, name) -> bool:
        """This method check if load balancer is created or not.

        Args:
            name (_type_): The name of the load balancer to find.

        Returns:
            bool: Return False if load balancer exists, else True.
        """
        for lb in self.elbv2_client.describe_load_balancers()['LoadBalancers']:
            if name == lb['LoadBalancerName']:
                return False
        else:
            return True