# hackingthe.cloud — AWS Attack Encyclopedia (Index)

Full content at: /root/killer-queen-knowledge/hackingthecloud/content/aws/
51 files (376KB) covering all AWS attack surfaces.

## Enumeration (10 files)
account_id_from_ec2, account_id_from_s3_bucket, brute_force_iam_permissions,
enum_iam_user_role, enumerate_principal_arn_from_unique_id,
enumerate_root_email_from_console, loot_public_ebs_snapshots, whoami,
discover_secrets_in_public_aims, get-account-id-from-keys

## Exploitation (13 files)
iam_privilege_escalation (30 techniques), ec2-metadata-ssrf,
lambda-steal-iam-credentials, cognito_identity_pool_excessive_privileges,
cognito_user_self_signup, local_ec2_priv_esc_through_user_data,
obfuscated_admin_policy, orphaned_cloudfront_or_dns_takeover_via_s3,
s3-bucket-replication-exfiltration, route53_modification_privilege_escalation,
s3_server_access_logs, abusing-container-registry, s3_streaming_copy

## Post-Exploitation (15 files)
iam_persistence, iam_rogue_oidc_identity_provider, iam_roles_anywhere_persistence,
lambda_persistence, s3_acl_persistence, user_data_script_persistence,
run_shell_commands_on_ec2, create_a_console_session_from_iam_credentials,
survive_access_key_deletion_with_sts_getfederationtoken,
get_iam_creds_from_console_session, codebuild_github_runner_persistence,
role-chain-juggling, intercept_ssm_communications,
download_tools_and_exfiltrate_data_with_aws_cli, iam_persistence_eventual_consistency

## Avoiding Detection (5 files)
guardduty-pentest, guardduty-pentest-botocore, guardduty-tor-client,
modify-guardduty-config, steal-keys-undetected

## General Knowledge (8 files)
intro_metadata_service, introduction_user_data, using_stolen_iam_credentials,
aws_organizations_defaults, connection-tracking, iam-key-identifiers,
block-expensive-actions-with-scps, aws_cli_tips_and_tricks

Source: https://github.com/Hacking-the-Cloud/hackingthe.cloud
