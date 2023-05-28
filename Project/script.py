import boto3
from VPC import Vpc


ec2_resource = boto3.resource("ec2")
ec2_client = boto3.client("ec2")

qube_vpc = Vpc(ec2_resource, ec2_client)

qube_vpc.create_virtual_private_cloud([{'Key': 'Name', 'Value': 'QubeVPC'}, {'Key': 'Product', 'Value': 'challenge'}], "172.20.0.0/16")

qube_vpc.create_and_attach_internet_gateway([{'Key': 'Name', 'Value': 'QubeIG'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_route_table([{'Key': 'Name', 'Value': 'QubePublicRT'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_subnet("172.20.1.0/24", "ap-south-1a", [{'Key': 'Name', 'Value': 'QubePublicSubnet1'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_public_subnet("172.20.2.0/24", "ap-south-1b", [{'Key': 'Name', 'Value': 'QubePublicSubnet2'}, {'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_nat_gateway([{'Key': 'Product', 'Value': 'challenge'}])

qube_vpc.create_private_route_table([{'Key': 'Name', 'Value': 'QubePrivateRT'}, {'Key': 'Product', 'Value': 'challenge'}])