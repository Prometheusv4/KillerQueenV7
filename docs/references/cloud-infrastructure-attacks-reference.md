# Cloud & Infrastructure Attacks — Killer Queen's Reference

> "The cloud is just someone else's computer. And someone else's computer is just your computer if you have the right IAM keys."
> — Killer Queen

## 1. AWS Attack Pathways

### 1.1 The AWS Kill Chain

```
Recon → Initial Access → Enumeration → Privilege Escalation → Data Exfil → Persistence
  ↓           ↓               ↓               ↓                  ↓            ↓
Public     Leaked keys    whoami          IAM privesc       S3 dump      Backdoor
resources  SSRF→Metadata  List roles      Lambda abuse      RDS extract  IAM users
GitHub     Phished creds  S3 enum         Assume role       DynamoDB     Cross-account
Shodan     Web app vuln   EC2 describe    PassRole          EBS snap     Lambda trigg
```

### 1.2 The Metadata Service Endpoint (169.254.169.254)
The single most important AWS target:
```
http://169.254.169.254/latest/meta-data/           # Instance metadata
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>  # TEMP KEYS
http://169.254.169.254/latest/user-data/           # Bootstrap scripts (often have secrets)
http://169.254.169.254/latest/dynamic/instance-identity/document  # Account ID, region
```

**SSRF to Metadata = instant credential theft.** If the target makes HTTP requests and you control the URL, always test for metadata endpoint access.

**IMDSv2 bypasses**: Some applications don't enforce v2 (token-required). Even with v2, hop-limit misconfigurations can allow SSRF.

## 2. IAM Privilege Escalation — The Pacu Way

Pacu's `iam__privesc_scan` module encodes dozens of escalation paths. Here are the patterns:

### 2.1 Escalation Pattern Categories

| Pattern | Required Permissions | Result |
|---------|---------------------|--------|
| **CreateAccessKey** | `iam:CreateAccessKey` on higher-privilege user | Steal their keys |
| **UpdateLoginProfile** | `iam:UpdateLoginProfile` on higher user | Change their password |
| **CreateLoginProfile** | `iam:CreateLoginProfile` if no profile set | Set password, login as them |
| **AttachUserPolicy** | `iam:AttachUserPolicy` | Attach `AdministratorAccess` |
| **AttachGroupPolicy** | `iam:AttachGroupPolicy` | Attach admin to group you're in |
| **AttachRolePolicy** | `iam:AttachRolePolicy` | Attach admin to role you can assume |
| **PutUserPolicy** | `iam:PutUserPolicy` | Inline admin policy on yourself |
| **PutGroupPolicy** | `iam:PutGroupPolicy` | Inline admin on your group |
| **PutRolePolicy** | `iam:PutRolePolicy` | Inline admin on assumable role |
| **AddUserToGroup** | `iam:AddUserToGroup` | Add yourself to admin group |
| **UpdateAssumeRolePolicy** | `iam:UpdateAssumeRolePolicy` | Allow yourself to assume admin role |
| **CreatePolicyVersion** | `iam:CreatePolicyVersion` | Create new admin version of existing policy |
| **SetDefaultPolicyVersion** | `iam:SetDefaultPolicyVersion` | Switch to malicious policy version |
| **PassRole + Lambda** | `iam:PassRole` + `lambda:CreateFunction` | Create Lambda with privileged role → execute code as that role |
| **PassRole + EC2** | `iam:PassRole` + `ec2:RunInstances` | Launch EC2 with privileged instance profile → SSH in |
| **CreatePolicy** | `iam:CreatePolicy` + attach ability | Create admin policy, attach to yourself |
| **sts:AssumeRole** | `sts:AssumeRole` on privileged role | Assume role directly (if trust policy allows) |
| **iam:UpdateSAMLProvider** | `iam:UpdateSAMLProvider` | Forge SAML assertion as any user |

### 2.2 The IAM Escalation Lab Pattern (from PwnedLabs)
```
Starting policy: iam:Get*, iam:List*, iam:Put*
Looks read-only? Wrong.

iam__privesc_scan reveals:
1. iam:PutUserPolicy → can add inline admin policy to yourself
2. iam:AttachUserPolicy → can attach AdministratorAccess directly
3. iam:CreatePolicyVersion → create new default policy version with admin
```

The lesson: **"Read" permissions often allow writes when combined correctly.**

## 3. Pacu Module Arsenal

### 3.1 Reconnaissance Modules
| Module | Purpose |
|--------|---------|
| `aws__enum_account` | Enumerate account ID, regions, resources |
| `aws__enum_spend` | Spending patterns — reveals active services |
| `aws__enum_iam` | Users, roles, groups, policies |
| `iam__enum_users_roles_policies_groups` | Deep IAM enumeration |
| `iam__enum_permissions` | What can THIS user actually do? |
| `s3__enum_bucket` | Discover buckets, test read/write/list |
| `ec2__enum` | Instances, security groups, AMIs |
| `lambda__enum` | Lambda functions, layers, event mappings |
| `rds__enum` | Database instances, snapshots |
| `cloudtrail__enum` | Trail configurations — how are you being logged? |

### 3.2 Privilege Escalation
| Module | Purpose |
|--------|---------|
| `iam__privesc_scan` | Scan ALL escalation paths for current user |
| `iam__backdoor_users` | Create access keys for other users (persistence) |
| `iam__backdoor_roles` | Add trust policy to roles (persistent assume) |
| `iam__backdoor_assume_role` | Create role trusting external account |

### 3.3 Data Exfiltration
| Module | Purpose |
|--------|---------|
| `s3__download_bucket` | Mass download bucket contents |
| `rds__explore_snapshots` | Restore DB snapshot to your account |
| `ebs__explore_snapshots` | Mount and explore EBS snapshots |
| `dynamodb__enum` | Enumerate DynamoDB tables, dump data |

### 3.4 Evasion
| Module | Purpose |
|--------|---------|
| `cloudtrail__download_logs` | Review what's been logged about you |
| `detection__honey_tokens` | Detect honey tokens (guardDuty, etc.) |
| `aws__survive` | Persistence mechanisms |

## 4. CloudGoat Scenario Attack Patterns

### Scenario: iam_privesc_by_rollback
- Developer has limited IAM permissions but can create policy versions
- Create a new DEFAULT version with AdministratorAccess
- The old restricted version becomes non-default
- PWNED

### Scenario: cloud_breach_s3
- EC2 instance with SSRF vulnerability
- SSRF → IMDS → instance profile credentials
- Instance profile has S3 access to sensitive bucket
- PWNED

### Scenario: lambda_privesc
- Limited user can invoke Lambda function
- Lambda function has admin privileges
- Inject payload into Lambda execution → execute as Lambda role
- PWNED

### Scenario: iam_privesc_by_attachment
- User has `iam:AttachUserPolicy` (looks benign)
- Attach AdministratorAccess to self
- PWNED

### Scenario: rce_web_app
- Web app vulnerability (SQLi, etc.) on EC2
- Exploit web app → code execution on EC2
- Access IMDS → steal instance profile credentials
- Instance profile has high privileges
- PWNED

### Scenario: ec2_ssrf
- EC2 hosts web app vulnerable to SSRF
- SSRF to IMDS v1 → steal credentials
- Those credentials allow more EC2 access
- Launch new instances with privileged roles
- PWNED

## 5. Cross-Service Attack Chains

### Lambda Abuse
```
1. Find Lambda with `lambda:InvokeFunction`
2. If it processes user input (API Gateway trigger), inject payload
3. Lambda role can be much more privileged than your user
4. Exfiltrate Lambda's credentials via DNS/HTTP callback
5. Use Lambda's role to escalate
```

### EC2 Instance Profile Theft
```
1. RCE on any EC2 instance (web app, SSH brute, SSRF to app)
2. curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
3. Get temporary creds for instance profile
4. Use those creds from attacker machine
5. Instance profile often has S3, DynamoDB, or even admin access
```

### S3 → RCE Chain
```
1. Find writable S3 bucket used by application
2. Upload malicious file (JS for web app, template for Lambda, etc.)
3. Application loads your content → XSS, template injection, code exec
```

### RDS Snapshot Exfiltration
```
1. RDS instance with sensitive data
2. `rds:DescribeDBSnapshots` + `rds:ModifyDBSnapshotAttribute`
3. Share snapshot with attacker's AWS account
4. Restore snapshot in attacker account → full database access
```

## 6. CloudTrail Evasion

### What Gets Logged:
- Every API call (if trail is configured)
- Source IP, user agent, parameters
- Response elements

### Evasion Techniques:
1. **Use less-logged regions**: Some organizations don't enable trails globally
2. **Use different services**: CloudTrail logs API calls, but some data-plane operations (S3 GetObject) may not be logged unless specifically enabled
3. **Credential isolation**: Use temporary credentials from role assumption — harder to trace back
4. **Timing**: Spread operations across time, use normal business hours
5. **Source IP**: Use IPs within the target's expected range (VPN, office)

## 7. Cloudflare Bypass Techniques

### 7.1 Origin IP Exposure
Cloudflare protects the origin, but the origin IP might leak:
- **DNS history**: SecurityTrails, DNSDumpster, crt.sh
- **Direct IP ranges**: Scan known origin IP ranges
- **Email headers**: If the server sends mail, origin IP in headers
- **SSL certificates**: Certificate Transparency logs may expose origin
- **Subdomains not behind CF**: dev.direct.target.com, origin.target.com
- **CrimeFlare-style enumeration**: Probe known CF IP ranges for the origin

### 7.2 Bot Detection Evasion
- **TLS fingerprinting**: Use browser-realistic TLS ciphers (not Python requests defaults)
- **Headless browser stealth**: puppeteer-extra + stealth plugin
- **JavaScript challenge solving**: Execute JS challenges in a real browser context
- **Session pools**: Rotate IPs and browser fingerprints

### 7.3 Turnstile/CAPTCHA Bypass
- **2captcha/Anti-Captcha services**: Outsource challenge solving
- **Controlled browser approach**: Launch real Chrome, solve challenge, export cookies
- **Cookie replay**: `cf_clearance` cookie can be replayed from solving session
- **Pattern for outsourcing**: Solve once → export cookies → replay cookies in programmatic requests

### 7.4 WAF Bypass (Cloudflare-specific)
- **Chunked transfer encoding tricks**
- **Unicode normalization bypasses**
- **HTTP parameter pollution**
- **Content-Type confusion**

## 8. Kubernetes & Container Attacks

### Container Escape:
1. **Privileged container** → cgroup release_agent → host code execution
2. **Docker socket mounted** → `docker run -v /:/host` → host filesystem access
3. **CAP_SYS_ADMIN** → mount host filesystem → chroot escape
4. **kernel exploit** → escape the namespace
5. **procfs/sysfs leaks** → host information disclosure

### Kubernetes Specific:
1. **Service account token theft** → `cat /run/secrets/kubernetes.io/serviceaccount/token`
2. **API server access** → `kubectl` with stolen token → cluster admin
3. **etcd access** → cluster secrets in plaintext
4. **Helm/Tiller** → historically had no auth
5. **Misconfigured RBAC** → overly permissive roles

## 9. Serverless Exploitation Patterns

### Lambda:
- **Event injection**: Control input to Lambda → influence execution
- **Dependency confusion**: Lambda uses vulnerable/poisoned packages
- **Environment variable theft**: Lambda env vars often contain secrets
- **/tmp persistence**: Lambda instances are reused → write to /tmp for persistence across warm starts
- **Outbound network**: Lambda can reach internet → exfiltrate data

### API Gateway:
- **CORS misconfig**: Reflects Origin → cookies stolen across origins
- **API key leakage**: Keys in client-side code, GitHub
- **Authorization bypass**: Custom authorizers with logic bugs

## 10. Killer Queen's Cloud Attack Checklist

```
RECON:
[ ] DNS enumeration (all subdomains)
[ ] Certificate Transparency logs
[ ] GitHub search for org name + "secret" | "password" | "key" | "access_key"
[ ] S3 bucket brute force (org-name, org-name-prod, org-name-dev, etc.)
[ ] Shodan/Censys for exposed services

INITIAL ACCESS:
[ ] Test SSRF to metadata endpoint (169.254.169.254)
[ ] Check for public S3 buckets
[ ] Check for public ECR/DockerHub repos
[ ] Test web app for SSTI/RCE on EC2/Lambda
[ ] Leaked credentials from GitHub

ENUMERATION (after getting any creds):
[ ] whoami — what user/role?
[ ] List IAM policies — what permissions?
[ ] List S3 buckets — what data?
[ ] List EC2 instances — what's running?
[ ] List Lambda functions — what event sources?
[ ] Describe CloudTrail — are you being logged?

PRIVESC:
[ ] Run iam__privesc_scan equivalent
[ ] Check PassRole + Lambda/EC2
[ ] Check AssumeRole on any role
[ ] Check policy attachment permissions
[ ] Check for version rollback possibilities

PERSISTENCE:
[ ] Create new IAM user with admin
[ ] Add access key to existing user
[ ] Modify role trust policy
[ ] Create Lambda with cron trigger
[ ] Cross-account access setup

EXFIL:
[ ] S3 bucket download
[ ] RDS snapshot share
[ ] EBS snapshot share
[ ] DynamoDB scan
[ ] CloudWatch log extraction
```
