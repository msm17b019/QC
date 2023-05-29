class Elb:
    def __init__(self, elbv2_client) -> None:
        """Class that represents amazon elastic load balancer services.

        Args:
            elbv2_client : client to create, manage and configure AWS ELB service at low level
        """
        self.elbv2_client = elbv2_client

    def create_elb(self, name: str, pub_sub: list, tags: list, elb_sg: str, vpc_id: str):
        """This method creates application load balancer.

        Args:
            name (str): Name of the load balancer.
            pub_sub (list): Public subnets.
            tags (list): Tags to add to the load balancers.
            elb_sg (str): Security group ID.
            vpc_id (str): VPC ID.
        """
        if self.check_elb(name):
            response1 = self.elbv2_client.create_load_balancer(
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
            self.elb_arn = response1['LoadBalancers'][0]['LoadBalancerArn']
            self.elb_dns_name = response1['LoadBalancers'][0]['DNSName']

            response2 = self.elbv2_client.create_listener(
                LoadBalancerArn=self.elb_arn,
                Protocol='HTTP',
                Port=80,
            )
            self.listener_arn = response2['Listeners'][0]['ListenerArn']

            response3 = self.elbv2_client.create_target_group(
                Name='QubeTG',
                Protocol='HTTP',
                Port=80,
                VpcId=vpc_id,
                TargetType='instance',
                Tags=tags
            )
            self.target_group_arn = response3['TargetGroups'][0]['TargetGroupArn']

            response4 = self.elbv2_client.create_rule(
                ListenerArn=self.listener_arn,
                Conditions=[
                    {
                        'Field': 'path-pattern',
                        'Values': [
                            f'{self.elb_dns_name}/worldsogood'
                        ]
                    }
                ],
                Actions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': self.target_group_arn
                    }
                ]
            )

    def check_elb(self, name) -> bool:
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