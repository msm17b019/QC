import boto3

ec2_client = boto3.client('ec2')

cidr_block = "172.20.0.0/16"

response = ec2_client.describe_vpcs()
vpcs = response['Vpcs']

for vpc in vpcs:
    if cidr_block == vpc['CidrBlock'] and vpc['Tags'] == [{'Key': 'Name', 'Value': 'QubeVPC'}, {'Key': 'Product', 'Value': 'challenge'}]:
        break
else:
    vpc = ec2_client.create_vpc(
        CidrBlock=cidr_block,
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Product',
                        'Value': 'challenge'
                    },
                    {
                        'Key': 'Name',
                        'Value': 'QubeVPC'
                    }
                ]
            },
        ]
    )