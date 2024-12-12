r'''
# CDKTF prebuilt bindings for cloudflare/cloudflare provider version 4.48.0

This repo builds and publishes the [Terraform cloudflare provider](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-cloudflare](https://www.npmjs.com/package/@cdktf/provider-cloudflare).

`npm install @cdktf/provider-cloudflare`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-cloudflare](https://pypi.org/project/cdktf-cdktf-provider-cloudflare).

`pipenv install cdktf-cdktf-provider-cloudflare`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Cloudflare](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Cloudflare).

`dotnet add package HashiCorp.Cdktf.Providers.Cloudflare`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-cloudflare](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-cloudflare).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-cloudflare</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-cloudflare-go`](https://github.com/cdktf/cdktf-provider-cloudflare-go) package.

`go get github.com/cdktf/cdktf-provider-cloudflare-go/cloudflare/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-cloudflare-go/blob/main/cloudflare/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-cloudflare).

## Versioning

This project is explicitly not tracking the Terraform cloudflare provider version 1:1. In fact, it always tracks `latest` of `~> 4.3` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform cloudflare provider](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

__all__ = [
    "access_application",
    "access_ca_certificate",
    "access_custom_page",
    "access_group",
    "access_identity_provider",
    "access_keys_configuration",
    "access_mutual_tls_certificate",
    "access_mutual_tls_hostname_settings",
    "access_organization",
    "access_policy",
    "access_rule",
    "access_service_token",
    "access_tag",
    "account",
    "account_member",
    "address_map",
    "api_shield",
    "api_shield_operation",
    "api_shield_operation_schema_validation_settings",
    "api_shield_schema",
    "api_shield_schema_validation_settings",
    "api_token",
    "argo",
    "authenticated_origin_pulls",
    "authenticated_origin_pulls_certificate",
    "bot_management",
    "byo_ip_prefix",
    "certificate_pack",
    "cloud_connector_rules",
    "custom_hostname",
    "custom_hostname_fallback_origin",
    "custom_pages",
    "custom_ssl",
    "d1_database",
    "data_cloudflare_access_application",
    "data_cloudflare_access_identity_provider",
    "data_cloudflare_account_roles",
    "data_cloudflare_accounts",
    "data_cloudflare_api_token_permission_groups",
    "data_cloudflare_dcv_delegation",
    "data_cloudflare_device_posture_rules",
    "data_cloudflare_devices",
    "data_cloudflare_dlp_datasets",
    "data_cloudflare_gateway_app_types",
    "data_cloudflare_gateway_categories",
    "data_cloudflare_infrastructure_access_targets",
    "data_cloudflare_ip_ranges",
    "data_cloudflare_list",
    "data_cloudflare_lists",
    "data_cloudflare_load_balancer_pools",
    "data_cloudflare_origin_ca_certificate",
    "data_cloudflare_origin_ca_root_certificate",
    "data_cloudflare_record",
    "data_cloudflare_rulesets",
    "data_cloudflare_tunnel",
    "data_cloudflare_tunnel_virtual_network",
    "data_cloudflare_user",
    "data_cloudflare_zero_trust_access_application",
    "data_cloudflare_zero_trust_access_identity_provider",
    "data_cloudflare_zero_trust_infrastructure_access_targets",
    "data_cloudflare_zero_trust_tunnel_cloudflared",
    "data_cloudflare_zero_trust_tunnel_virtual_network",
    "data_cloudflare_zone",
    "data_cloudflare_zone_cache_reserve",
    "data_cloudflare_zone_dnssec",
    "data_cloudflare_zones",
    "device_dex_test",
    "device_managed_networks",
    "device_policy_certificates",
    "device_posture_integration",
    "device_posture_rule",
    "device_settings_policy",
    "dlp_profile",
    "email_routing_address",
    "email_routing_catch_all",
    "email_routing_rule",
    "email_routing_settings",
    "fallback_domain",
    "filter",
    "firewall_rule",
    "gre_tunnel",
    "healthcheck",
    "hostname_tls_setting",
    "hostname_tls_setting_ciphers",
    "hyperdrive_config",
    "infrastructure_access_target",
    "ipsec_tunnel",
    "keyless_certificate",
    "leaked_credential_check",
    "leaked_credential_check_rule",
    "list",
    "list_item",
    "load_balancer",
    "load_balancer_monitor",
    "load_balancer_pool",
    "logpull_retention",
    "logpush_job",
    "logpush_ownership_challenge",
    "magic_firewall_ruleset",
    "magic_wan_gre_tunnel",
    "magic_wan_ipsec_tunnel",
    "magic_wan_static_route",
    "managed_headers",
    "mtls_certificate",
    "notification_policy",
    "notification_policy_webhooks",
    "observatory_scheduled_test",
    "origin_ca_certificate",
    "page_rule",
    "pages_domain",
    "pages_project",
    "provider",
    "queue",
    "r2_bucket",
    "rate_limit",
    "record",
    "regional_hostname",
    "regional_tiered_cache",
    "risk_behavior",
    "ruleset",
    "snippet",
    "snippet_rules",
    "spectrum_application",
    "split_tunnel",
    "static_route",
    "teams_account",
    "teams_list",
    "teams_location",
    "teams_proxy_endpoint",
    "teams_rule",
    "tiered_cache",
    "total_tls",
    "tunnel",
    "tunnel_config",
    "tunnel_route",
    "tunnel_virtual_network",
    "turnstile_widget",
    "url_normalization_settings",
    "user_agent_blocking_rule",
    "waiting_room",
    "waiting_room_event",
    "waiting_room_rules",
    "waiting_room_settings",
    "web3_hostname",
    "web_analytics_rule",
    "web_analytics_site",
    "worker_cron_trigger",
    "worker_domain",
    "worker_route",
    "worker_script",
    "worker_secret",
    "workers_cron_trigger",
    "workers_domain",
    "workers_for_platforms_dispatch_namespace",
    "workers_for_platforms_namespace",
    "workers_kv",
    "workers_kv_namespace",
    "workers_route",
    "workers_script",
    "workers_secret",
    "zero_trust_access_application",
    "zero_trust_access_custom_page",
    "zero_trust_access_group",
    "zero_trust_access_identity_provider",
    "zero_trust_access_mtls_certificate",
    "zero_trust_access_mtls_hostname_settings",
    "zero_trust_access_organization",
    "zero_trust_access_policy",
    "zero_trust_access_service_token",
    "zero_trust_access_short_lived_certificate",
    "zero_trust_access_tag",
    "zero_trust_device_certificates",
    "zero_trust_device_managed_networks",
    "zero_trust_device_posture_integration",
    "zero_trust_device_posture_rule",
    "zero_trust_device_profiles",
    "zero_trust_dex_test",
    "zero_trust_dlp_profile",
    "zero_trust_dns_location",
    "zero_trust_gateway_certificate",
    "zero_trust_gateway_policy",
    "zero_trust_gateway_proxy_endpoint",
    "zero_trust_gateway_settings",
    "zero_trust_infrastructure_access_target",
    "zero_trust_key_access_key_configuration",
    "zero_trust_list",
    "zero_trust_local_fallback_domain",
    "zero_trust_risk_behavior",
    "zero_trust_risk_score_integration",
    "zero_trust_split_tunnel",
    "zero_trust_tunnel_cloudflared",
    "zero_trust_tunnel_cloudflared_config",
    "zero_trust_tunnel_route",
    "zero_trust_tunnel_virtual_network",
    "zone",
    "zone_cache_reserve",
    "zone_cache_variants",
    "zone_dnssec",
    "zone_hold",
    "zone_lockdown",
    "zone_settings_override",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import access_application
from . import access_ca_certificate
from . import access_custom_page
from . import access_group
from . import access_identity_provider
from . import access_keys_configuration
from . import access_mutual_tls_certificate
from . import access_mutual_tls_hostname_settings
from . import access_organization
from . import access_policy
from . import access_rule
from . import access_service_token
from . import access_tag
from . import account
from . import account_member
from . import address_map
from . import api_shield
from . import api_shield_operation
from . import api_shield_operation_schema_validation_settings
from . import api_shield_schema
from . import api_shield_schema_validation_settings
from . import api_token
from . import argo
from . import authenticated_origin_pulls
from . import authenticated_origin_pulls_certificate
from . import bot_management
from . import byo_ip_prefix
from . import certificate_pack
from . import cloud_connector_rules
from . import custom_hostname
from . import custom_hostname_fallback_origin
from . import custom_pages
from . import custom_ssl
from . import d1_database
from . import data_cloudflare_access_application
from . import data_cloudflare_access_identity_provider
from . import data_cloudflare_account_roles
from . import data_cloudflare_accounts
from . import data_cloudflare_api_token_permission_groups
from . import data_cloudflare_dcv_delegation
from . import data_cloudflare_device_posture_rules
from . import data_cloudflare_devices
from . import data_cloudflare_dlp_datasets
from . import data_cloudflare_gateway_app_types
from . import data_cloudflare_gateway_categories
from . import data_cloudflare_infrastructure_access_targets
from . import data_cloudflare_ip_ranges
from . import data_cloudflare_list
from . import data_cloudflare_lists
from . import data_cloudflare_load_balancer_pools
from . import data_cloudflare_origin_ca_certificate
from . import data_cloudflare_origin_ca_root_certificate
from . import data_cloudflare_record
from . import data_cloudflare_rulesets
from . import data_cloudflare_tunnel
from . import data_cloudflare_tunnel_virtual_network
from . import data_cloudflare_user
from . import data_cloudflare_zero_trust_access_application
from . import data_cloudflare_zero_trust_access_identity_provider
from . import data_cloudflare_zero_trust_infrastructure_access_targets
from . import data_cloudflare_zero_trust_tunnel_cloudflared
from . import data_cloudflare_zero_trust_tunnel_virtual_network
from . import data_cloudflare_zone
from . import data_cloudflare_zone_cache_reserve
from . import data_cloudflare_zone_dnssec
from . import data_cloudflare_zones
from . import device_dex_test
from . import device_managed_networks
from . import device_policy_certificates
from . import device_posture_integration
from . import device_posture_rule
from . import device_settings_policy
from . import dlp_profile
from . import email_routing_address
from . import email_routing_catch_all
from . import email_routing_rule
from . import email_routing_settings
from . import fallback_domain
from . import filter
from . import firewall_rule
from . import gre_tunnel
from . import healthcheck
from . import hostname_tls_setting
from . import hostname_tls_setting_ciphers
from . import hyperdrive_config
from . import infrastructure_access_target
from . import ipsec_tunnel
from . import keyless_certificate
from . import leaked_credential_check
from . import leaked_credential_check_rule
from . import list
from . import list_item
from . import load_balancer
from . import load_balancer_monitor
from . import load_balancer_pool
from . import logpull_retention
from . import logpush_job
from . import logpush_ownership_challenge
from . import magic_firewall_ruleset
from . import magic_wan_gre_tunnel
from . import magic_wan_ipsec_tunnel
from . import magic_wan_static_route
from . import managed_headers
from . import mtls_certificate
from . import notification_policy
from . import notification_policy_webhooks
from . import observatory_scheduled_test
from . import origin_ca_certificate
from . import page_rule
from . import pages_domain
from . import pages_project
from . import provider
from . import queue
from . import r2_bucket
from . import rate_limit
from . import record
from . import regional_hostname
from . import regional_tiered_cache
from . import risk_behavior
from . import ruleset
from . import snippet
from . import snippet_rules
from . import spectrum_application
from . import split_tunnel
from . import static_route
from . import teams_account
from . import teams_list
from . import teams_location
from . import teams_proxy_endpoint
from . import teams_rule
from . import tiered_cache
from . import total_tls
from . import tunnel
from . import tunnel_config
from . import tunnel_route
from . import tunnel_virtual_network
from . import turnstile_widget
from . import url_normalization_settings
from . import user_agent_blocking_rule
from . import waiting_room
from . import waiting_room_event
from . import waiting_room_rules
from . import waiting_room_settings
from . import web_analytics_rule
from . import web_analytics_site
from . import web3_hostname
from . import worker_cron_trigger
from . import worker_domain
from . import worker_route
from . import worker_script
from . import worker_secret
from . import workers_cron_trigger
from . import workers_domain
from . import workers_for_platforms_dispatch_namespace
from . import workers_for_platforms_namespace
from . import workers_kv
from . import workers_kv_namespace
from . import workers_route
from . import workers_script
from . import workers_secret
from . import zero_trust_access_application
from . import zero_trust_access_custom_page
from . import zero_trust_access_group
from . import zero_trust_access_identity_provider
from . import zero_trust_access_mtls_certificate
from . import zero_trust_access_mtls_hostname_settings
from . import zero_trust_access_organization
from . import zero_trust_access_policy
from . import zero_trust_access_service_token
from . import zero_trust_access_short_lived_certificate
from . import zero_trust_access_tag
from . import zero_trust_device_certificates
from . import zero_trust_device_managed_networks
from . import zero_trust_device_posture_integration
from . import zero_trust_device_posture_rule
from . import zero_trust_device_profiles
from . import zero_trust_dex_test
from . import zero_trust_dlp_profile
from . import zero_trust_dns_location
from . import zero_trust_gateway_certificate
from . import zero_trust_gateway_policy
from . import zero_trust_gateway_proxy_endpoint
from . import zero_trust_gateway_settings
from . import zero_trust_infrastructure_access_target
from . import zero_trust_key_access_key_configuration
from . import zero_trust_list
from . import zero_trust_local_fallback_domain
from . import zero_trust_risk_behavior
from . import zero_trust_risk_score_integration
from . import zero_trust_split_tunnel
from . import zero_trust_tunnel_cloudflared
from . import zero_trust_tunnel_cloudflared_config
from . import zero_trust_tunnel_route
from . import zero_trust_tunnel_virtual_network
from . import zone
from . import zone_cache_reserve
from . import zone_cache_variants
from . import zone_dnssec
from . import zone_hold
from . import zone_lockdown
from . import zone_settings_override
