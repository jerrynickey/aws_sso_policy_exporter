# AWS IAM Policy Exporter

## Overview

**AWS IAM Policy Exporter** is a Python-based tool designed to automate the extraction of IAM roles and their associated policies from an AWS account. It collects both inline and managed policies, parses their actions, and exports the data into a structured Excel file for auditing, reporting, or governance purposes.

## Features

- Lists all IAM roles in your AWS account
- Extracts inline policies and their actions
- Identifies attached AWS-managed policies
- Handles missing or malformed policy statements gracefully
- Exports the data to an Excel file (`aws_roles_policies.xlsx`)
- Includes logging for progress and error tracking

## Prerequisites

- Python 3.8+
- AWS CLI configured with credentials
- IAM permissions:
  - `iam:ListRoles`
  - `iam:ListRolePolicies`
  - `iam:GetRolePolicy`
  - `iam:ListAttachedRolePolicies`
  - `iam:GetPolicy`
  - `iam:GetPolicyVersion`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jerrynicke/aws_sso__policy_exporter.git
   cd aws_sso__policy_exporter
   ```
