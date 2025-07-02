import boto3
import pandas as pd
import logging
from botocore.exceptions import NoCredentialsError, ClientError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Initialize IAM client
try:
    iam = boto3.client('iam')
except NoCredentialsError:
    logging.error("AWS credentials not found. Please configure them using 'aws configure'.")
    exit()

# Prepare data container
policy_data = []

try:
    # List all IAM roles
    roles_response = iam.list_roles()
    roles = roles_response['Roles']
    logging.info(f"Found {len(roles)} roles.")

    for role in roles:
        role_name = role['RoleName']
        logging.info(f"Processing role: {role_name}")

        # Get inline policies
        inline_policies = iam.list_role_policies(RoleName=role_name)['PolicyNames']
        for policy_name in inline_policies:
            try:
                policy_doc = iam.get_role_policy(RoleName=role_name, PolicyName=policy_name)['PolicyDocument']
                statements = policy_doc.get('Statement', [])
                if not isinstance(statements, list):
                    statements = [statements]

                for stmt in statements:
                    if 'Action' in stmt:
                        actions = stmt['Action'] if isinstance(stmt['Action'], list) else [stmt['Action']]
                        for action in actions:
                            policy_data.append({
                                'role': role_name,
                                'policy_name': policy_name,
                                'policy_type': 'Customer inline',
                                'action': action
                            })
                    else:
                        policy_data.append({
                            'role': role_name,
                            'policy_name': policy_name,
                            'policy_type': 'Customer inline',
                            'action': 'SKIPPED: No Action key'
                        })
            except ClientError as e:
                logging.warning(f"Failed to get inline policy {policy_name} for role {role_name}: {e}")

        # Get attached managed policies
        attached_policies = iam.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in attached_policies:
            policy_data.append({
                'role': role_name,
                'policy_name': policy['PolicyName'],
                'policy_type': 'AWSManaged',
                'action': 'N/A'
            })

except ClientError as e:
    logging.error(f"Failed to retrieve roles or policies: {e}")
    exit()

# Export to Excel
df = pd.DataFrame(policy_data)
output_file = "aws_roles_policies_cdp_uat.xlsx"
df.to_excel(output_file, index=False)
logging.info(f"Policy data exported to {output_file}")
