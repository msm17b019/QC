import boto3
from VPC import Vpc
from SQS import Sqs
from ASG import Asg
from EC2 import Ec2
from IAM import Iam
from ELB import Elb

ec2_resource = boto3.resource("ec2")
ec2_client = boto3.client("ec2")
sqs_resource = boto3.resource("sqs")
as_client = boto3.client("autoscaling")
elbv2_client = boto3.client("elbv2")
iam_client = boto3.client("iam")

qube_vpc = Vpc(ec2_resource, ec2_client)

qube_vpc.create_virtual_private_cloud([{'Key': 'Name', 'Value': 'QubeVPC'}, {'Key': 'Product', 'Value': 'challenge'}], "172.20.0.0/16")

qube_vpc.create_and_attach_internet_gateway([{'Key': 'Name', 'Value': 'QubeIG'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_route_table([{'Key': 'Name', 'Value': 'QubePublicRT'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_subnet("172.20.1.0/24", "ap-south-1a", [{'Key': 'Name', 'Value': 'QubePublicSubnet1'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_subnet("172.20.2.0/24", "ap-south-1b", [{'Key': 'Name', 'Value': 'QubePublicSubnet2'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_nat_gateway([{'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_private_route_table([{'Key': 'Name', 'Value': 'QubePrivateRT'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_private_subnet("172.20.3.0/24", "ap-south-1c", [{'Key': 'Name', 'Value': 'QubePrivateSubnet1'}, {'Key': 'Product', 'Value': 'challenge'}])

alb_sgid = qube_vpc.create_alb_security_group("QubeAlbSG", "Security group for ALB", [{'Key': 'Product', 'Value': 'challenge'}])

asg_sgid = qube_vpc.create_asg_security_group("QubeAsgSG", "Security group for ASG", [{'Key': 'Product', 'Value': 'challenge'}])

qube_sqs = Sqs(sqs_resource)
qube_sqs.create_sqs_queue("QubeSQS", {'Key': 'Product', 'Value': 'challenge'})

qube_iam = Iam(iam_client)
qube_iam.create_instance_profile("QubeIP", [{'Key': 'Product', 'Value': 'challenge'}])
qube_iam.create_add_iam_policy_to_role("QubePolicy", [{'Key': 'Product', 'Value': 'challenge'}], "461338057834", "", "QubeASG")