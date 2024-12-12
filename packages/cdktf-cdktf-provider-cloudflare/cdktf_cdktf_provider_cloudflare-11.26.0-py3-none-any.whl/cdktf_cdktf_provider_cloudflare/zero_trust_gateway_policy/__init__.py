r'''
# `cloudflare_zero_trust_gateway_policy`

Refer to the Terraform Registry for docs: [`cloudflare_zero_trust_gateway_policy`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ZeroTrustGatewayPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy cloudflare_zero_trust_gateway_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        action: builtins.str,
        description: builtins.str,
        name: builtins.str,
        precedence: jsii.Number,
        device_posture: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[builtins.str] = None,
        rule_settings: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy cloudflare_zero_trust_gateway_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#account_id ZeroTrustGatewayPolicy#account_id}
        :param action: The action executed by matched teams rule. Available values: ``allow``, ``block``, ``safesearch``, ``ytrestricted``, ``on``, ``off``, ``scan``, ``noscan``, ``isolate``, ``noisolate``, ``override``, ``l4_override``, ``egress``, ``audit_ssh``, ``resolve``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        :param description: The description of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#description ZeroTrustGatewayPolicy#description}
        :param name: The name of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#name ZeroTrustGatewayPolicy#name}
        :param precedence: The evaluation precedence of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#precedence ZeroTrustGatewayPolicy#precedence}
        :param device_posture: The wirefilter expression to be used for device_posture check matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#device_posture ZeroTrustGatewayPolicy#device_posture}
        :param enabled: Indicator of rule enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        :param filters: The protocol or layer to evaluate the traffic and identity expressions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#filters ZeroTrustGatewayPolicy#filters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#id ZeroTrustGatewayPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: The wirefilter expression to be used for identity matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#identity ZeroTrustGatewayPolicy#identity}
        :param rule_settings: rule_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#rule_settings ZeroTrustGatewayPolicy#rule_settings}
        :param traffic: The wirefilter expression to be used for traffic matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#traffic ZeroTrustGatewayPolicy#traffic}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e786f3b51fdd9d9ed8a9ede6d413dce3bca2cd0cf1cb66429b00315285745858)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZeroTrustGatewayPolicyConfig(
            account_id=account_id,
            action=action,
            description=description,
            name=name,
            precedence=precedence,
            device_posture=device_posture,
            enabled=enabled,
            filters=filters,
            id=id,
            identity=identity,
            rule_settings=rule_settings,
            traffic=traffic,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ZeroTrustGatewayPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ZeroTrustGatewayPolicy to import.
        :param import_from_id: The id of the existing ZeroTrustGatewayPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ZeroTrustGatewayPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a82a394c6d2096b6cfe77d2cb2d7a0802d1cb0b8c4111b58a4499f87b9cb2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRuleSettings")
    def put_rule_settings(
        self,
        *,
        add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_child_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        audit_ssh: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsAuditSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        biso_admin_controls: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        block_page_reason: typing.Optional[builtins.str] = None,
        bypass_parent_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_session: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsCheckSession", typing.Dict[builtins.str, typing.Any]]] = None,
        dns_resolvers: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsDnsResolvers", typing.Dict[builtins.str, typing.Any]]] = None,
        egress: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsEgress", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_cname_category_matches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_categories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_override: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsL4Override", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_settings: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        override_host: typing.Optional[builtins.str] = None,
        override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        payload_log: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        resolve_dns_through_cloudflare: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        untrusted_cert: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_headers: Add custom headers to allowed requests in the form of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#add_headers ZeroTrustGatewayPolicy#add_headers}
        :param allow_child_bypass: Allow parent MSP accounts to enable bypass their children's rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#allow_child_bypass ZeroTrustGatewayPolicy#allow_child_bypass}
        :param audit_ssh: audit_ssh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#audit_ssh ZeroTrustGatewayPolicy#audit_ssh}
        :param biso_admin_controls: biso_admin_controls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#biso_admin_controls ZeroTrustGatewayPolicy#biso_admin_controls}
        :param block_page_enabled: Indicator of block page enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_enabled ZeroTrustGatewayPolicy#block_page_enabled}
        :param block_page_reason: The displayed reason for a user being blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_reason ZeroTrustGatewayPolicy#block_page_reason}
        :param bypass_parent_rule: Allow child MSP accounts to bypass their parent's rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#bypass_parent_rule ZeroTrustGatewayPolicy#bypass_parent_rule}
        :param check_session: check_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#check_session ZeroTrustGatewayPolicy#check_session}
        :param dns_resolvers: dns_resolvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#dns_resolvers ZeroTrustGatewayPolicy#dns_resolvers}
        :param egress: egress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#egress ZeroTrustGatewayPolicy#egress}
        :param ignore_cname_category_matches: Set to true, to ignore the category matches at CNAME domains in a response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ignore_cname_category_matches ZeroTrustGatewayPolicy#ignore_cname_category_matches}
        :param insecure_disable_dnssec_validation: Disable DNSSEC validation (must be Allow rule). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#insecure_disable_dnssec_validation ZeroTrustGatewayPolicy#insecure_disable_dnssec_validation}
        :param ip_categories: Turns on IP category based filter on dns if the rule contains dns category checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip_categories ZeroTrustGatewayPolicy#ip_categories}
        :param l4_override: l4override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#l4override ZeroTrustGatewayPolicy#l4override}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#notification_settings ZeroTrustGatewayPolicy#notification_settings}
        :param override_host: The host to override matching DNS queries with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_host ZeroTrustGatewayPolicy#override_host}
        :param override_ips: The IPs to override matching DNS queries with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_ips ZeroTrustGatewayPolicy#override_ips}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#payload_log ZeroTrustGatewayPolicy#payload_log}
        :param resolve_dns_through_cloudflare: Enable sending queries that match the resolver policy to Cloudflare's default 1.1.1.1 DNS resolver. Cannot be set when ``dns_resolvers`` are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#resolve_dns_through_cloudflare ZeroTrustGatewayPolicy#resolve_dns_through_cloudflare}
        :param untrusted_cert: untrusted_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#untrusted_cert ZeroTrustGatewayPolicy#untrusted_cert}
        '''
        value = ZeroTrustGatewayPolicyRuleSettings(
            add_headers=add_headers,
            allow_child_bypass=allow_child_bypass,
            audit_ssh=audit_ssh,
            biso_admin_controls=biso_admin_controls,
            block_page_enabled=block_page_enabled,
            block_page_reason=block_page_reason,
            bypass_parent_rule=bypass_parent_rule,
            check_session=check_session,
            dns_resolvers=dns_resolvers,
            egress=egress,
            ignore_cname_category_matches=ignore_cname_category_matches,
            insecure_disable_dnssec_validation=insecure_disable_dnssec_validation,
            ip_categories=ip_categories,
            l4_override=l4_override,
            notification_settings=notification_settings,
            override_host=override_host,
            override_ips=override_ips,
            payload_log=payload_log,
            resolve_dns_through_cloudflare=resolve_dns_through_cloudflare,
            untrusted_cert=untrusted_cert,
        )

        return typing.cast(None, jsii.invoke(self, "putRuleSettings", [value]))

    @jsii.member(jsii_name="resetDevicePosture")
    def reset_device_posture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevicePosture", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFilters")
    def reset_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetRuleSettings")
    def reset_rule_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleSettings", []))

    @jsii.member(jsii_name="resetTraffic")
    def reset_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraffic", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="ruleSettings")
    def rule_settings(self) -> "ZeroTrustGatewayPolicyRuleSettingsOutputReference":
        return typing.cast("ZeroTrustGatewayPolicyRuleSettingsOutputReference", jsii.get(self, "ruleSettings"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="devicePostureInput")
    def device_posture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "devicePostureInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filtersInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleSettingsInput")
    def rule_settings_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettings"]:
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettings"], jsii.get(self, "ruleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trafficInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bb7ba5f48d9b8e2a3bb95f022537a9bfc450f3475c72a300c1cae1683f9ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7bbd14973f8b3f0a43994b287c91e533e76cb5b8c5e095101c90750c11d93b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83db28167eff420a547cf252dd8e7781e5796c1cace39c68df6c1a06b2da2d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="devicePosture")
    def device_posture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "devicePosture"))

    @device_posture.setter
    def device_posture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee39d2975aef69e34e1a231b8e211addc371b9ad64dceb2f20e20d4ae852c237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devicePosture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45825779e8075f762c6a646e54a09f77631a4328dfb317cc06b661e8121e179b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filters"))

    @filters.setter
    def filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18e5f294f5711f739edce78df2d227cbee0051bd29aba76a875d970ca98100b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199dad41e61259de131f6a72dd8ad9affc8ef8c527c7afeb38ce174cd0a6c61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @identity.setter
    def identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fff43c71cbeb7eff49371043e13151751ba92b81c1e0493e6f2f3ebce50d929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa62bd411e5957a4f46d586eb095eb3d653370b09ee649ce6849dd5a2d07624b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5210b06d00643b59aad339b83d84162c64bdb7c26827fb9528babd7e3e61786c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traffic"))

    @traffic.setter
    def traffic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872dd1a90e3d9f1a1ba75703168e5c9754c8cbf3777f03ea7b5294d225912329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traffic", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "action": "action",
        "description": "description",
        "name": "name",
        "precedence": "precedence",
        "device_posture": "devicePosture",
        "enabled": "enabled",
        "filters": "filters",
        "id": "id",
        "identity": "identity",
        "rule_settings": "ruleSettings",
        "traffic": "traffic",
    },
)
class ZeroTrustGatewayPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        account_id: builtins.str,
        action: builtins.str,
        description: builtins.str,
        name: builtins.str,
        precedence: jsii.Number,
        device_posture: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[builtins.str] = None,
        rule_settings: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#account_id ZeroTrustGatewayPolicy#account_id}
        :param action: The action executed by matched teams rule. Available values: ``allow``, ``block``, ``safesearch``, ``ytrestricted``, ``on``, ``off``, ``scan``, ``noscan``, ``isolate``, ``noisolate``, ``override``, ``l4_override``, ``egress``, ``audit_ssh``, ``resolve``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        :param description: The description of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#description ZeroTrustGatewayPolicy#description}
        :param name: The name of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#name ZeroTrustGatewayPolicy#name}
        :param precedence: The evaluation precedence of the teams rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#precedence ZeroTrustGatewayPolicy#precedence}
        :param device_posture: The wirefilter expression to be used for device_posture check matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#device_posture ZeroTrustGatewayPolicy#device_posture}
        :param enabled: Indicator of rule enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        :param filters: The protocol or layer to evaluate the traffic and identity expressions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#filters ZeroTrustGatewayPolicy#filters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#id ZeroTrustGatewayPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: The wirefilter expression to be used for identity matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#identity ZeroTrustGatewayPolicy#identity}
        :param rule_settings: rule_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#rule_settings ZeroTrustGatewayPolicy#rule_settings}
        :param traffic: The wirefilter expression to be used for traffic matching. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#traffic ZeroTrustGatewayPolicy#traffic}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rule_settings, dict):
            rule_settings = ZeroTrustGatewayPolicyRuleSettings(**rule_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3d5137255dbb7219c971b313cd804791e2a0ef37964d8a593b17f6a3718187)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument device_posture", value=device_posture, expected_type=type_hints["device_posture"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument rule_settings", value=rule_settings, expected_type=type_hints["rule_settings"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "action": action,
            "description": description,
            "name": name,
            "precedence": precedence,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if device_posture is not None:
            self._values["device_posture"] = device_posture
        if enabled is not None:
            self._values["enabled"] = enabled
        if filters is not None:
            self._values["filters"] = filters
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if rule_settings is not None:
            self._values["rule_settings"] = rule_settings
        if traffic is not None:
            self._values["traffic"] = traffic

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#account_id ZeroTrustGatewayPolicy#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> builtins.str:
        '''The action executed by matched teams rule.

        Available values: ``allow``, ``block``, ``safesearch``, ``ytrestricted``, ``on``, ``off``, ``scan``, ``noscan``, ``isolate``, ``noisolate``, ``override``, ``l4_override``, ``egress``, ``audit_ssh``, ``resolve``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''The description of the teams rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#description ZeroTrustGatewayPolicy#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the teams rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#name ZeroTrustGatewayPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def precedence(self) -> jsii.Number:
        '''The evaluation precedence of the teams rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#precedence ZeroTrustGatewayPolicy#precedence}
        '''
        result = self._values.get("precedence")
        assert result is not None, "Required property 'precedence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def device_posture(self) -> typing.Optional[builtins.str]:
        '''The wirefilter expression to be used for device_posture check matching.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#device_posture ZeroTrustGatewayPolicy#device_posture}
        '''
        result = self._values.get("device_posture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator of rule enablement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The protocol or layer to evaluate the traffic and identity expressions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#filters ZeroTrustGatewayPolicy#filters}
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#id ZeroTrustGatewayPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional[builtins.str]:
        '''The wirefilter expression to be used for identity matching.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#identity ZeroTrustGatewayPolicy#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_settings(self) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettings"]:
        '''rule_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#rule_settings ZeroTrustGatewayPolicy#rule_settings}
        '''
        result = self._values.get("rule_settings")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettings"], result)

    @builtins.property
    def traffic(self) -> typing.Optional[builtins.str]:
        '''The wirefilter expression to be used for traffic matching.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#traffic ZeroTrustGatewayPolicy#traffic}
        '''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettings",
    jsii_struct_bases=[],
    name_mapping={
        "add_headers": "addHeaders",
        "allow_child_bypass": "allowChildBypass",
        "audit_ssh": "auditSsh",
        "biso_admin_controls": "bisoAdminControls",
        "block_page_enabled": "blockPageEnabled",
        "block_page_reason": "blockPageReason",
        "bypass_parent_rule": "bypassParentRule",
        "check_session": "checkSession",
        "dns_resolvers": "dnsResolvers",
        "egress": "egress",
        "ignore_cname_category_matches": "ignoreCnameCategoryMatches",
        "insecure_disable_dnssec_validation": "insecureDisableDnssecValidation",
        "ip_categories": "ipCategories",
        "l4_override": "l4Override",
        "notification_settings": "notificationSettings",
        "override_host": "overrideHost",
        "override_ips": "overrideIps",
        "payload_log": "payloadLog",
        "resolve_dns_through_cloudflare": "resolveDnsThroughCloudflare",
        "untrusted_cert": "untrustedCert",
    },
)
class ZeroTrustGatewayPolicyRuleSettings:
    def __init__(
        self,
        *,
        add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allow_child_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        audit_ssh: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsAuditSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        biso_admin_controls: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        block_page_reason: typing.Optional[builtins.str] = None,
        bypass_parent_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_session: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsCheckSession", typing.Dict[builtins.str, typing.Any]]] = None,
        dns_resolvers: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsDnsResolvers", typing.Dict[builtins.str, typing.Any]]] = None,
        egress: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsEgress", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_cname_category_matches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_categories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_override: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsL4Override", typing.Dict[builtins.str, typing.Any]]] = None,
        notification_settings: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        override_host: typing.Optional[builtins.str] = None,
        override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        payload_log: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        resolve_dns_through_cloudflare: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        untrusted_cert: typing.Optional[typing.Union["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param add_headers: Add custom headers to allowed requests in the form of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#add_headers ZeroTrustGatewayPolicy#add_headers}
        :param allow_child_bypass: Allow parent MSP accounts to enable bypass their children's rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#allow_child_bypass ZeroTrustGatewayPolicy#allow_child_bypass}
        :param audit_ssh: audit_ssh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#audit_ssh ZeroTrustGatewayPolicy#audit_ssh}
        :param biso_admin_controls: biso_admin_controls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#biso_admin_controls ZeroTrustGatewayPolicy#biso_admin_controls}
        :param block_page_enabled: Indicator of block page enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_enabled ZeroTrustGatewayPolicy#block_page_enabled}
        :param block_page_reason: The displayed reason for a user being blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_reason ZeroTrustGatewayPolicy#block_page_reason}
        :param bypass_parent_rule: Allow child MSP accounts to bypass their parent's rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#bypass_parent_rule ZeroTrustGatewayPolicy#bypass_parent_rule}
        :param check_session: check_session block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#check_session ZeroTrustGatewayPolicy#check_session}
        :param dns_resolvers: dns_resolvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#dns_resolvers ZeroTrustGatewayPolicy#dns_resolvers}
        :param egress: egress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#egress ZeroTrustGatewayPolicy#egress}
        :param ignore_cname_category_matches: Set to true, to ignore the category matches at CNAME domains in a response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ignore_cname_category_matches ZeroTrustGatewayPolicy#ignore_cname_category_matches}
        :param insecure_disable_dnssec_validation: Disable DNSSEC validation (must be Allow rule). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#insecure_disable_dnssec_validation ZeroTrustGatewayPolicy#insecure_disable_dnssec_validation}
        :param ip_categories: Turns on IP category based filter on dns if the rule contains dns category checks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip_categories ZeroTrustGatewayPolicy#ip_categories}
        :param l4_override: l4override block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#l4override ZeroTrustGatewayPolicy#l4override}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#notification_settings ZeroTrustGatewayPolicy#notification_settings}
        :param override_host: The host to override matching DNS queries with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_host ZeroTrustGatewayPolicy#override_host}
        :param override_ips: The IPs to override matching DNS queries with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_ips ZeroTrustGatewayPolicy#override_ips}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#payload_log ZeroTrustGatewayPolicy#payload_log}
        :param resolve_dns_through_cloudflare: Enable sending queries that match the resolver policy to Cloudflare's default 1.1.1.1 DNS resolver. Cannot be set when ``dns_resolvers`` are specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#resolve_dns_through_cloudflare ZeroTrustGatewayPolicy#resolve_dns_through_cloudflare}
        :param untrusted_cert: untrusted_cert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#untrusted_cert ZeroTrustGatewayPolicy#untrusted_cert}
        '''
        if isinstance(audit_ssh, dict):
            audit_ssh = ZeroTrustGatewayPolicyRuleSettingsAuditSsh(**audit_ssh)
        if isinstance(biso_admin_controls, dict):
            biso_admin_controls = ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls(**biso_admin_controls)
        if isinstance(check_session, dict):
            check_session = ZeroTrustGatewayPolicyRuleSettingsCheckSession(**check_session)
        if isinstance(dns_resolvers, dict):
            dns_resolvers = ZeroTrustGatewayPolicyRuleSettingsDnsResolvers(**dns_resolvers)
        if isinstance(egress, dict):
            egress = ZeroTrustGatewayPolicyRuleSettingsEgress(**egress)
        if isinstance(l4_override, dict):
            l4_override = ZeroTrustGatewayPolicyRuleSettingsL4Override(**l4_override)
        if isinstance(notification_settings, dict):
            notification_settings = ZeroTrustGatewayPolicyRuleSettingsNotificationSettings(**notification_settings)
        if isinstance(payload_log, dict):
            payload_log = ZeroTrustGatewayPolicyRuleSettingsPayloadLog(**payload_log)
        if isinstance(untrusted_cert, dict):
            untrusted_cert = ZeroTrustGatewayPolicyRuleSettingsUntrustedCert(**untrusted_cert)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8f89e3048662a05610c3fc4775c975b8cbfc7190cf304482a2b63c0a5c20af)
            check_type(argname="argument add_headers", value=add_headers, expected_type=type_hints["add_headers"])
            check_type(argname="argument allow_child_bypass", value=allow_child_bypass, expected_type=type_hints["allow_child_bypass"])
            check_type(argname="argument audit_ssh", value=audit_ssh, expected_type=type_hints["audit_ssh"])
            check_type(argname="argument biso_admin_controls", value=biso_admin_controls, expected_type=type_hints["biso_admin_controls"])
            check_type(argname="argument block_page_enabled", value=block_page_enabled, expected_type=type_hints["block_page_enabled"])
            check_type(argname="argument block_page_reason", value=block_page_reason, expected_type=type_hints["block_page_reason"])
            check_type(argname="argument bypass_parent_rule", value=bypass_parent_rule, expected_type=type_hints["bypass_parent_rule"])
            check_type(argname="argument check_session", value=check_session, expected_type=type_hints["check_session"])
            check_type(argname="argument dns_resolvers", value=dns_resolvers, expected_type=type_hints["dns_resolvers"])
            check_type(argname="argument egress", value=egress, expected_type=type_hints["egress"])
            check_type(argname="argument ignore_cname_category_matches", value=ignore_cname_category_matches, expected_type=type_hints["ignore_cname_category_matches"])
            check_type(argname="argument insecure_disable_dnssec_validation", value=insecure_disable_dnssec_validation, expected_type=type_hints["insecure_disable_dnssec_validation"])
            check_type(argname="argument ip_categories", value=ip_categories, expected_type=type_hints["ip_categories"])
            check_type(argname="argument l4_override", value=l4_override, expected_type=type_hints["l4_override"])
            check_type(argname="argument notification_settings", value=notification_settings, expected_type=type_hints["notification_settings"])
            check_type(argname="argument override_host", value=override_host, expected_type=type_hints["override_host"])
            check_type(argname="argument override_ips", value=override_ips, expected_type=type_hints["override_ips"])
            check_type(argname="argument payload_log", value=payload_log, expected_type=type_hints["payload_log"])
            check_type(argname="argument resolve_dns_through_cloudflare", value=resolve_dns_through_cloudflare, expected_type=type_hints["resolve_dns_through_cloudflare"])
            check_type(argname="argument untrusted_cert", value=untrusted_cert, expected_type=type_hints["untrusted_cert"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_headers is not None:
            self._values["add_headers"] = add_headers
        if allow_child_bypass is not None:
            self._values["allow_child_bypass"] = allow_child_bypass
        if audit_ssh is not None:
            self._values["audit_ssh"] = audit_ssh
        if biso_admin_controls is not None:
            self._values["biso_admin_controls"] = biso_admin_controls
        if block_page_enabled is not None:
            self._values["block_page_enabled"] = block_page_enabled
        if block_page_reason is not None:
            self._values["block_page_reason"] = block_page_reason
        if bypass_parent_rule is not None:
            self._values["bypass_parent_rule"] = bypass_parent_rule
        if check_session is not None:
            self._values["check_session"] = check_session
        if dns_resolvers is not None:
            self._values["dns_resolvers"] = dns_resolvers
        if egress is not None:
            self._values["egress"] = egress
        if ignore_cname_category_matches is not None:
            self._values["ignore_cname_category_matches"] = ignore_cname_category_matches
        if insecure_disable_dnssec_validation is not None:
            self._values["insecure_disable_dnssec_validation"] = insecure_disable_dnssec_validation
        if ip_categories is not None:
            self._values["ip_categories"] = ip_categories
        if l4_override is not None:
            self._values["l4_override"] = l4_override
        if notification_settings is not None:
            self._values["notification_settings"] = notification_settings
        if override_host is not None:
            self._values["override_host"] = override_host
        if override_ips is not None:
            self._values["override_ips"] = override_ips
        if payload_log is not None:
            self._values["payload_log"] = payload_log
        if resolve_dns_through_cloudflare is not None:
            self._values["resolve_dns_through_cloudflare"] = resolve_dns_through_cloudflare
        if untrusted_cert is not None:
            self._values["untrusted_cert"] = untrusted_cert

    @builtins.property
    def add_headers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Add custom headers to allowed requests in the form of key-value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#add_headers ZeroTrustGatewayPolicy#add_headers}
        '''
        result = self._values.get("add_headers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allow_child_bypass(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow parent MSP accounts to enable bypass their children's rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#allow_child_bypass ZeroTrustGatewayPolicy#allow_child_bypass}
        '''
        result = self._values.get("allow_child_bypass")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def audit_ssh(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsAuditSsh"]:
        '''audit_ssh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#audit_ssh ZeroTrustGatewayPolicy#audit_ssh}
        '''
        result = self._values.get("audit_ssh")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsAuditSsh"], result)

    @builtins.property
    def biso_admin_controls(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls"]:
        '''biso_admin_controls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#biso_admin_controls ZeroTrustGatewayPolicy#biso_admin_controls}
        '''
        result = self._values.get("biso_admin_controls")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls"], result)

    @builtins.property
    def block_page_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator of block page enablement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_enabled ZeroTrustGatewayPolicy#block_page_enabled}
        '''
        result = self._values.get("block_page_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def block_page_reason(self) -> typing.Optional[builtins.str]:
        '''The displayed reason for a user being blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#block_page_reason ZeroTrustGatewayPolicy#block_page_reason}
        '''
        result = self._values.get("block_page_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bypass_parent_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow child MSP accounts to bypass their parent's rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#bypass_parent_rule ZeroTrustGatewayPolicy#bypass_parent_rule}
        '''
        result = self._values.get("bypass_parent_rule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def check_session(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsCheckSession"]:
        '''check_session block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#check_session ZeroTrustGatewayPolicy#check_session}
        '''
        result = self._values.get("check_session")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsCheckSession"], result)

    @builtins.property
    def dns_resolvers(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsDnsResolvers"]:
        '''dns_resolvers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#dns_resolvers ZeroTrustGatewayPolicy#dns_resolvers}
        '''
        result = self._values.get("dns_resolvers")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsDnsResolvers"], result)

    @builtins.property
    def egress(self) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsEgress"]:
        '''egress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#egress ZeroTrustGatewayPolicy#egress}
        '''
        result = self._values.get("egress")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsEgress"], result)

    @builtins.property
    def ignore_cname_category_matches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true, to ignore the category matches at CNAME domains in a response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ignore_cname_category_matches ZeroTrustGatewayPolicy#ignore_cname_category_matches}
        '''
        result = self._values.get("ignore_cname_category_matches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def insecure_disable_dnssec_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable DNSSEC validation (must be Allow rule).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#insecure_disable_dnssec_validation ZeroTrustGatewayPolicy#insecure_disable_dnssec_validation}
        '''
        result = self._values.get("insecure_disable_dnssec_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_categories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Turns on IP category based filter on dns if the rule contains dns category checks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip_categories ZeroTrustGatewayPolicy#ip_categories}
        '''
        result = self._values.get("ip_categories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def l4_override(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsL4Override"]:
        '''l4override block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#l4override ZeroTrustGatewayPolicy#l4override}
        '''
        result = self._values.get("l4_override")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsL4Override"], result)

    @builtins.property
    def notification_settings(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsNotificationSettings"]:
        '''notification_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#notification_settings ZeroTrustGatewayPolicy#notification_settings}
        '''
        result = self._values.get("notification_settings")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsNotificationSettings"], result)

    @builtins.property
    def override_host(self) -> typing.Optional[builtins.str]:
        '''The host to override matching DNS queries with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_host ZeroTrustGatewayPolicy#override_host}
        '''
        result = self._values.get("override_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IPs to override matching DNS queries with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#override_ips ZeroTrustGatewayPolicy#override_ips}
        '''
        result = self._values.get("override_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def payload_log(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsPayloadLog"]:
        '''payload_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#payload_log ZeroTrustGatewayPolicy#payload_log}
        '''
        result = self._values.get("payload_log")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsPayloadLog"], result)

    @builtins.property
    def resolve_dns_through_cloudflare(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable sending queries that match the resolver policy to Cloudflare's default 1.1.1.1 DNS resolver. Cannot be set when ``dns_resolvers`` are specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#resolve_dns_through_cloudflare ZeroTrustGatewayPolicy#resolve_dns_through_cloudflare}
        '''
        result = self._values.get("resolve_dns_through_cloudflare")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def untrusted_cert(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert"]:
        '''untrusted_cert block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#untrusted_cert ZeroTrustGatewayPolicy#untrusted_cert}
        '''
        result = self._values.get("untrusted_cert")
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsAuditSsh",
    jsii_struct_bases=[],
    name_mapping={"command_logging": "commandLogging"},
)
class ZeroTrustGatewayPolicyRuleSettingsAuditSsh:
    def __init__(
        self,
        *,
        command_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param command_logging: Log all SSH commands. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#command_logging ZeroTrustGatewayPolicy#command_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e13806ef402ec94ed21dd8e335b31ece45f371213e9bd91cd4f83a977b851a3)
            check_type(argname="argument command_logging", value=command_logging, expected_type=type_hints["command_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "command_logging": command_logging,
        }

    @builtins.property
    def command_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Log all SSH commands.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#command_logging ZeroTrustGatewayPolicy#command_logging}
        '''
        result = self._values.get("command_logging")
        assert result is not None, "Required property 'command_logging' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsAuditSsh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsAuditSshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsAuditSshOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7cbe1aad2274aab866344e2e4178aa08f6f0894258b0a1d57502ac56a236f45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="commandLoggingInput")
    def command_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commandLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="commandLogging")
    def command_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "commandLogging"))

    @command_logging.setter
    def command_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9da99cbe034882dfcd29f81babcb2a2c1f9170d681b8bdcfdf43385b072238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commandLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5fc353cec0452da1882b51e0644b7d85e988ab68deb41c5016c972fb20c440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls",
    jsii_struct_bases=[],
    name_mapping={
        "disable_clipboard_redirection": "disableClipboardRedirection",
        "disable_copy_paste": "disableCopyPaste",
        "disable_download": "disableDownload",
        "disable_keyboard": "disableKeyboard",
        "disable_printing": "disablePrinting",
        "disable_upload": "disableUpload",
    },
)
class ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls:
    def __init__(
        self,
        *,
        disable_clipboard_redirection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_clipboard_redirection: Disable clipboard redirection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_clipboard_redirection ZeroTrustGatewayPolicy#disable_clipboard_redirection}
        :param disable_copy_paste: Disable copy-paste. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_copy_paste ZeroTrustGatewayPolicy#disable_copy_paste}
        :param disable_download: Disable download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_download ZeroTrustGatewayPolicy#disable_download}
        :param disable_keyboard: Disable keyboard usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_keyboard ZeroTrustGatewayPolicy#disable_keyboard}
        :param disable_printing: Disable printing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_printing ZeroTrustGatewayPolicy#disable_printing}
        :param disable_upload: Disable upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_upload ZeroTrustGatewayPolicy#disable_upload}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd65a816aca7befaa772d1c5d0ecc9d1f288ab4e81f1ffdade3c911a0b13b14)
            check_type(argname="argument disable_clipboard_redirection", value=disable_clipboard_redirection, expected_type=type_hints["disable_clipboard_redirection"])
            check_type(argname="argument disable_copy_paste", value=disable_copy_paste, expected_type=type_hints["disable_copy_paste"])
            check_type(argname="argument disable_download", value=disable_download, expected_type=type_hints["disable_download"])
            check_type(argname="argument disable_keyboard", value=disable_keyboard, expected_type=type_hints["disable_keyboard"])
            check_type(argname="argument disable_printing", value=disable_printing, expected_type=type_hints["disable_printing"])
            check_type(argname="argument disable_upload", value=disable_upload, expected_type=type_hints["disable_upload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_clipboard_redirection is not None:
            self._values["disable_clipboard_redirection"] = disable_clipboard_redirection
        if disable_copy_paste is not None:
            self._values["disable_copy_paste"] = disable_copy_paste
        if disable_download is not None:
            self._values["disable_download"] = disable_download
        if disable_keyboard is not None:
            self._values["disable_keyboard"] = disable_keyboard
        if disable_printing is not None:
            self._values["disable_printing"] = disable_printing
        if disable_upload is not None:
            self._values["disable_upload"] = disable_upload

    @builtins.property
    def disable_clipboard_redirection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable clipboard redirection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_clipboard_redirection ZeroTrustGatewayPolicy#disable_clipboard_redirection}
        '''
        result = self._values.get("disable_clipboard_redirection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_copy_paste(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable copy-paste.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_copy_paste ZeroTrustGatewayPolicy#disable_copy_paste}
        '''
        result = self._values.get("disable_copy_paste")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable download.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_download ZeroTrustGatewayPolicy#disable_download}
        '''
        result = self._values.get("disable_download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_keyboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable keyboard usage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_keyboard ZeroTrustGatewayPolicy#disable_keyboard}
        '''
        result = self._values.get("disable_keyboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_printing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable printing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_printing ZeroTrustGatewayPolicy#disable_printing}
        '''
        result = self._values.get("disable_printing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_upload(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable upload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_upload ZeroTrustGatewayPolicy#disable_upload}
        '''
        result = self._values.get("disable_upload")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsBisoAdminControlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsBisoAdminControlsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e487688fb41ca3eaba6906db9cc86e97d2f8b3c4b56ad97fcb47b4ac4a290d93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableClipboardRedirection")
    def reset_disable_clipboard_redirection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableClipboardRedirection", []))

    @jsii.member(jsii_name="resetDisableCopyPaste")
    def reset_disable_copy_paste(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCopyPaste", []))

    @jsii.member(jsii_name="resetDisableDownload")
    def reset_disable_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDownload", []))

    @jsii.member(jsii_name="resetDisableKeyboard")
    def reset_disable_keyboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableKeyboard", []))

    @jsii.member(jsii_name="resetDisablePrinting")
    def reset_disable_printing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePrinting", []))

    @jsii.member(jsii_name="resetDisableUpload")
    def reset_disable_upload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUpload", []))

    @builtins.property
    @jsii.member(jsii_name="disableClipboardRedirectionInput")
    def disable_clipboard_redirection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableClipboardRedirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableCopyPasteInput")
    def disable_copy_paste_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCopyPasteInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDownloadInput")
    def disable_download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDownloadInput"))

    @builtins.property
    @jsii.member(jsii_name="disableKeyboardInput")
    def disable_keyboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableKeyboardInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePrintingInput")
    def disable_printing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePrintingInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUploadInput")
    def disable_upload_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUploadInput"))

    @builtins.property
    @jsii.member(jsii_name="disableClipboardRedirection")
    def disable_clipboard_redirection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableClipboardRedirection"))

    @disable_clipboard_redirection.setter
    def disable_clipboard_redirection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9bbcec73a36fe7169ee4ee06744bac7806848fe3b7ca8fa570d03ed444765a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableClipboardRedirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableCopyPaste")
    def disable_copy_paste(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableCopyPaste"))

    @disable_copy_paste.setter
    def disable_copy_paste(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbea7feea9d1db4a4a40fd2a41878db080aba8e2041189c592cff4ab2993913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCopyPaste", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableDownload")
    def disable_download(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableDownload"))

    @disable_download.setter
    def disable_download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88937c12c1d5f3f330962cf416ce6554dbedad8460bedfb586fbdbe8894c9dcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDownload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableKeyboard")
    def disable_keyboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableKeyboard"))

    @disable_keyboard.setter
    def disable_keyboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f8c3f6b69fd2fa48e05564c519de28dce43b69c2c4549435901d1a554a636c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableKeyboard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disablePrinting")
    def disable_printing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePrinting"))

    @disable_printing.setter
    def disable_printing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e80f7749ea055b75493a4ef78600bb41e387f7d26dfc4db8d1a341b2775790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePrinting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUpload")
    def disable_upload(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUpload"))

    @disable_upload.setter
    def disable_upload(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33def006c69a6239b3c2addd29dba93eb7f0636cb665013b749278343319da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUpload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b16262088665bd23c4414f6ce9e1ef921a03111175eb5160228b5b8cbdb35cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsCheckSession",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration", "enforce": "enforce"},
)
class ZeroTrustGatewayPolicyRuleSettingsCheckSession:
    def __init__(
        self,
        *,
        duration: builtins.str,
        enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param duration: Configure how fresh the session needs to be to be considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#duration ZeroTrustGatewayPolicy#duration}
        :param enforce: Enable session enforcement for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enforce ZeroTrustGatewayPolicy#enforce}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56199ee2205a76f737af972538e10f89fe9b1ad3b1ae437325cab49c99f6877b)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
            "enforce": enforce,
        }

    @builtins.property
    def duration(self) -> builtins.str:
        '''Configure how fresh the session needs to be to be considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#duration ZeroTrustGatewayPolicy#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable session enforcement for this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enforce ZeroTrustGatewayPolicy#enforce}
        '''
        result = self._values.get("enforce")
        assert result is not None, "Required property 'enforce' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsCheckSession(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsCheckSessionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsCheckSessionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e808649dd9d4901863979bb24d8623d67310b6fc114de70bc108fa8480a248)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b8a53e3936669c3400cdac4a0dcaa9df95fde0f9b01f93cddf02a0f6de668b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704639372dcc580a04c74d5c5fb881b8f14087b8aad093f31515ad4d3b70b1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cea6cb3a0aa5166676514ff8fe2f424ad1b786908f73d5bd1b9cc8d02add24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolvers",
    jsii_struct_bases=[],
    name_mapping={"ipv4": "ipv4", "ipv6": "ipv6"},
)
class ZeroTrustGatewayPolicyRuleSettingsDnsResolvers:
    def __init__(
        self,
        *,
        ipv4: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ipv6: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ipv4: ipv4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61e86bdabb946d2d3a72397fbab37eed75de1962c303d02d391da06329eb2b1)
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6

    @builtins.property
    def ipv4(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4"]]]:
        '''ipv4 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4"]]], result)

    @builtins.property
    def ipv6(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6"]]]:
        '''ipv6 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsDnsResolvers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4",
    jsii_struct_bases=[],
    name_mapping={
        "ip": "ip",
        "port": "port",
        "route_through_private_network": "routeThroughPrivateNetwork",
        "vnet_id": "vnetId",
    },
)
class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4:
    def __init__(
        self,
        *,
        ip: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        route_through_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: The IPv4 or IPv6 address of the upstream resolver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        :param port: A port number to use for the upstream resolver. Defaults to ``53``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        :param route_through_private_network: Whether to connect to this resolver over a private network. Must be set when ``vnet_id`` is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#route_through_private_network ZeroTrustGatewayPolicy#route_through_private_network}
        :param vnet_id: specify a virtual network for this resolver. Uses default virtual network id if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#vnet_id ZeroTrustGatewayPolicy#vnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c24719bdc3038d165f74ab720bef83026321ba3145104cfaa1c1b20d148cab8)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument route_through_private_network", value=route_through_private_network, expected_type=type_hints["route_through_private_network"])
            check_type(argname="argument vnet_id", value=vnet_id, expected_type=type_hints["vnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
        }
        if port is not None:
            self._values["port"] = port
        if route_through_private_network is not None:
            self._values["route_through_private_network"] = route_through_private_network
        if vnet_id is not None:
            self._values["vnet_id"] = vnet_id

    @builtins.property
    def ip(self) -> builtins.str:
        '''The IPv4 or IPv6 address of the upstream resolver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''A port number to use for the upstream resolver. Defaults to ``53``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def route_through_private_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to connect to this resolver over a private network. Must be set when ``vnet_id`` is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#route_through_private_network ZeroTrustGatewayPolicy#route_through_private_network}
        '''
        result = self._values.get("route_through_private_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vnet_id(self) -> typing.Optional[builtins.str]:
        '''specify a virtual network for this resolver. Uses default virtual network id if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#vnet_id ZeroTrustGatewayPolicy#vnet_id}
        '''
        result = self._values.get("vnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4List",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8325a1a409077918c933b460bfcc5f3a826ee186f245ca9839b836c70d772e06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533b1bf8395b943248c885e85812eb93b2a774de10422d63612cf28ac14cafaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c2d41d484fcff6d4869072b8c656d8d1637c6d2ded398ea49a1d65dbaebbd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dd7a58248308472bd5468feb92374998e6b7b5590ec736782c3a553637e060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71763ee18b7be04bf6a77a7792383688b0cfd8db3c6ed614cd32776113332c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe57289c5a429db420b6145e99ddaaf5ede4dc135885cf66ffa8e5fa4303b979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b79a03168b1f67148b565cda58d26b288c914a1d512954035060c72b5e3d87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRouteThroughPrivateNetwork")
    def reset_route_through_private_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteThroughPrivateNetwork", []))

    @jsii.member(jsii_name="resetVnetId")
    def reset_vnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetId", []))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="routeThroughPrivateNetworkInput")
    def route_through_private_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routeThroughPrivateNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIdInput")
    def vnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fd7414892d1597a66dac08101d741d4f8d59be453c0dea8a8d1338514cb5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f65de8183eaebfe0f9215db319b0e90ea52991fb28e72d46082a8ace1646ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeThroughPrivateNetwork")
    def route_through_private_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routeThroughPrivateNetwork"))

    @route_through_private_network.setter
    def route_through_private_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4329b10738e673d9049a8ce03c03876d48454709cdddfc3de5497fc5492f8189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeThroughPrivateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetId")
    def vnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetId"))

    @vnet_id.setter
    def vnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b0d19c27d6fd136e1e0d206878f3628b4675a45ec9fc28cefe607883cb7397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fe51044e877d271f848c76ef15c1b3e10a340760aa9758e97ea688bc18e0a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6",
    jsii_struct_bases=[],
    name_mapping={
        "ip": "ip",
        "port": "port",
        "route_through_private_network": "routeThroughPrivateNetwork",
        "vnet_id": "vnetId",
    },
)
class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6:
    def __init__(
        self,
        *,
        ip: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        route_through_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip: The IPv4 or IPv6 address of the upstream resolver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        :param port: A port number to use for the upstream resolver. Defaults to ``53``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        :param route_through_private_network: Whether to connect to this resolver over a private network. Must be set when ``vnet_id`` is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#route_through_private_network ZeroTrustGatewayPolicy#route_through_private_network}
        :param vnet_id: specify a virtual network for this resolver. Uses default virtual network id if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#vnet_id ZeroTrustGatewayPolicy#vnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f85e4dfa7046f3af0deee7ff5a1e3a4b86af348b71fe1af87e2692b77712992)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument route_through_private_network", value=route_through_private_network, expected_type=type_hints["route_through_private_network"])
            check_type(argname="argument vnet_id", value=vnet_id, expected_type=type_hints["vnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
        }
        if port is not None:
            self._values["port"] = port
        if route_through_private_network is not None:
            self._values["route_through_private_network"] = route_through_private_network
        if vnet_id is not None:
            self._values["vnet_id"] = vnet_id

    @builtins.property
    def ip(self) -> builtins.str:
        '''The IPv4 or IPv6 address of the upstream resolver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''A port number to use for the upstream resolver. Defaults to ``53``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def route_through_private_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to connect to this resolver over a private network. Must be set when ``vnet_id`` is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#route_through_private_network ZeroTrustGatewayPolicy#route_through_private_network}
        '''
        result = self._values.get("route_through_private_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vnet_id(self) -> typing.Optional[builtins.str]:
        '''specify a virtual network for this resolver. Uses default virtual network id if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#vnet_id ZeroTrustGatewayPolicy#vnet_id}
        '''
        result = self._values.get("vnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6List",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4bfb32196b3551481e8cca349977d12590376dd4642cc0bc2726152543abe8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc981020efa520611da174b7843290c261f1dc2e2a32ec583c026ee3b10931fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8407ffb93365f1e2e11b27875a35c4dca52915c0e1f10356b9a1e7ef826cbc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6117090d75a8b51dc4d30205a60b06123d6019c3934be55e60967b5f4d56c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0a68cd7314b423e0e39a7e15fbd9a1108fa2272438d35e24cb18ade3535045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80c31a75c73774f61153c8df8e0968b4f59e3a499f73f0e7f101d5efe967bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aefc0967e7ec9bfc17da46922d77545c41748b7953a536aa596d76d466151ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRouteThroughPrivateNetwork")
    def reset_route_through_private_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteThroughPrivateNetwork", []))

    @jsii.member(jsii_name="resetVnetId")
    def reset_vnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetId", []))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="routeThroughPrivateNetworkInput")
    def route_through_private_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routeThroughPrivateNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetIdInput")
    def vnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d1a1427283f10bb887bae9c8c09aa3473bb39bee635cb748cc7bec7288aff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0988a9d00ba8ce08c0f3fe89efeabad47e3fd9a2817225d945e7d064436329d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeThroughPrivateNetwork")
    def route_through_private_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routeThroughPrivateNetwork"))

    @route_through_private_network.setter
    def route_through_private_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8866e5fdf3ff5e525fe793fa1633c72c80b4ba2ef2047c9e8d0446894140b9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeThroughPrivateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetId")
    def vnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnetId"))

    @vnet_id.setter
    def vnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f45582a25857306e9cd17c9127b3d076c4693372dd57adbbf473a7705fc42db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bb6c8dd0d7cf527e474f84d5a925a39708320a10e08bdafbc5a00915848a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewayPolicyRuleSettingsDnsResolversOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsDnsResolversOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe77d83fd907f5544880a4f430e59c13a1392f63bd7abfafdef6f884393e209)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpv4")
    def put_ipv4(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669ea23d8599a8644f7eeadecdb0f6bdc876d012383fbd95625edd251989a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpv4", [value]))

    @jsii.member(jsii_name="putIpv6")
    def put_ipv6(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9dc0db711eacec9887cafb44e734357f3d89b9fb5f4d297e2f7ca1f2c366bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpv6", [value]))

    @jsii.member(jsii_name="resetIpv4")
    def reset_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4List:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4List, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6List:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6List, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298b64663e24f0ea5c0535778501a4f36f10bbaead2fca81e35f69674e0c9d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsEgress",
    jsii_struct_bases=[],
    name_mapping={"ipv4": "ipv4", "ipv6": "ipv6", "ipv4_fallback": "ipv4Fallback"},
)
class ZeroTrustGatewayPolicyRuleSettingsEgress:
    def __init__(
        self,
        *,
        ipv4: builtins.str,
        ipv6: builtins.str,
        ipv4_fallback: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ipv4: The IPv4 address to be used for egress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        :param ipv6: The IPv6 range to be used for egress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        :param ipv4_fallback: The IPv4 address to be used for egress in the event of an error egressing with the primary IPv4. Can be '0.0.0.0' to indicate local egreass via Warp IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4_fallback ZeroTrustGatewayPolicy#ipv4_fallback}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c20c20790982b1f4876312fe70df67926222adacb75525c029e94887d98091)
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument ipv4_fallback", value=ipv4_fallback, expected_type=type_hints["ipv4_fallback"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ipv4": ipv4,
            "ipv6": ipv6,
        }
        if ipv4_fallback is not None:
            self._values["ipv4_fallback"] = ipv4_fallback

    @builtins.property
    def ipv4(self) -> builtins.str:
        '''The IPv4 address to be used for egress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        '''
        result = self._values.get("ipv4")
        assert result is not None, "Required property 'ipv4' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv6(self) -> builtins.str:
        '''The IPv6 range to be used for egress.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        '''
        result = self._values.get("ipv6")
        assert result is not None, "Required property 'ipv6' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ipv4_fallback(self) -> typing.Optional[builtins.str]:
        '''The IPv4 address to be used for egress in the event of an error egressing with the primary IPv4.

        Can be '0.0.0.0' to indicate local egreass via Warp IPs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4_fallback ZeroTrustGatewayPolicy#ipv4_fallback}
        '''
        result = self._values.get("ipv4_fallback")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsEgress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsEgressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsEgressOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0796cb8575c970172d0ce9e0ad3d1e0860b3ab8d36b679e13b1f966c06bade9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIpv4Fallback")
    def reset_ipv4_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Fallback", []))

    @builtins.property
    @jsii.member(jsii_name="ipv4FallbackInput")
    def ipv4_fallback_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4FallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4"))

    @ipv4.setter
    def ipv4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966af7cdf684fe3aa938943063e2d7977054accb6cead27577e182dd385c3c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Fallback")
    def ipv4_fallback(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Fallback"))

    @ipv4_fallback.setter
    def ipv4_fallback(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6e3514c0230e5012ef0492d45c9d1b43937198b0bd8b5bd65da9a5cc57ee88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Fallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6"))

    @ipv6.setter
    def ipv6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a862b5eb8ce043e340f8e643740e87ed76e3bbe47211aecb9ed70ca4ad785c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6833a6d490876a271d35b87f147a66acb5deb7685ab224819007c64d0e400263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsL4Override",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "port": "port"},
)
class ZeroTrustGatewayPolicyRuleSettingsL4Override:
    def __init__(self, *, ip: builtins.str, port: jsii.Number) -> None:
        '''
        :param ip: Override IP to forward traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        :param port: Override Port to forward traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbef793f0f9dfeabe7b5485433aab6102e162df9a897abc8d4b8aa339fee92ea)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
            "port": port,
        }

    @builtins.property
    def ip(self) -> builtins.str:
        '''Override IP to forward traffic to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Override Port to forward traffic to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsL4Override(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsL4OverrideOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsL4OverrideOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6376ac5fce76140ef3b8fb4f6af9e78a84d144fa24bf3dea6601411840482eb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a062656fb3774493c7ec44c60f40ddae4dcc2ab4ae76d3fac41cfca847cee672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5059f6a84f9af734199f2419a73019521b0ef42cdde25d33f3848ffa428e0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6992764ef0e447a8c43336bc9eb62ac1a401718853c978e226e191973c17cb66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsNotificationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "message": "message",
        "support_url": "supportUrl",
    },
)
class ZeroTrustGatewayPolicyRuleSettingsNotificationSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#message ZeroTrustGatewayPolicy#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#support_url ZeroTrustGatewayPolicy#support_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8db5c5eeaf4ff44b629eb99747f03cd75818482acd82211db67f8e37ddf7fc2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if message is not None:
            self._values["message"] = message
        if support_url is not None:
            self._values["support_url"] = support_url

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable notification settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Notification content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#message ZeroTrustGatewayPolicy#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''Support URL to show in the notification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#support_url ZeroTrustGatewayPolicy#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsNotificationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsNotificationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsNotificationSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727c90cf4d7e78e845de5b7b5c003c1d7edca7319b28566b450c0738e7d213fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetSupportUrl")
    def reset_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportUrl", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlInput")
    def support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07fe27be482df4e82f9d62e5ba477d03b5e5c742909acc39649a932218a327d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d84b8cc06ab08f7faaa2667ba6cd5bff03d1528475aad86fda1a6c8af8c291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99fef0f410d5c6360be8db0b53fa52f68d0a745a5d8ac7815daf6cddc788b82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6537fcfae534b3c752b2fbe6489d26533be9a49e9425c470c18a6d3d0f036ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewayPolicyRuleSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1fbdcc6d5b96639588760d6d409fb65e4ee361bc0d52ea6c5e7f0dbd6ada66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuditSsh")
    def put_audit_ssh(
        self,
        *,
        command_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param command_logging: Log all SSH commands. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#command_logging ZeroTrustGatewayPolicy#command_logging}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsAuditSsh(
            command_logging=command_logging
        )

        return typing.cast(None, jsii.invoke(self, "putAuditSsh", [value]))

    @jsii.member(jsii_name="putBisoAdminControls")
    def put_biso_admin_controls(
        self,
        *,
        disable_clipboard_redirection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_clipboard_redirection: Disable clipboard redirection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_clipboard_redirection ZeroTrustGatewayPolicy#disable_clipboard_redirection}
        :param disable_copy_paste: Disable copy-paste. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_copy_paste ZeroTrustGatewayPolicy#disable_copy_paste}
        :param disable_download: Disable download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_download ZeroTrustGatewayPolicy#disable_download}
        :param disable_keyboard: Disable keyboard usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_keyboard ZeroTrustGatewayPolicy#disable_keyboard}
        :param disable_printing: Disable printing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_printing ZeroTrustGatewayPolicy#disable_printing}
        :param disable_upload: Disable upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#disable_upload ZeroTrustGatewayPolicy#disable_upload}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls(
            disable_clipboard_redirection=disable_clipboard_redirection,
            disable_copy_paste=disable_copy_paste,
            disable_download=disable_download,
            disable_keyboard=disable_keyboard,
            disable_printing=disable_printing,
            disable_upload=disable_upload,
        )

        return typing.cast(None, jsii.invoke(self, "putBisoAdminControls", [value]))

    @jsii.member(jsii_name="putCheckSession")
    def put_check_session(
        self,
        *,
        duration: builtins.str,
        enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param duration: Configure how fresh the session needs to be to be considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#duration ZeroTrustGatewayPolicy#duration}
        :param enforce: Enable session enforcement for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enforce ZeroTrustGatewayPolicy#enforce}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsCheckSession(
            duration=duration, enforce=enforce
        )

        return typing.cast(None, jsii.invoke(self, "putCheckSession", [value]))

    @jsii.member(jsii_name="putDnsResolvers")
    def put_dns_resolvers(
        self,
        *,
        ipv4: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4, typing.Dict[builtins.str, typing.Any]]]]] = None,
        ipv6: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ipv4: ipv4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsDnsResolvers(ipv4=ipv4, ipv6=ipv6)

        return typing.cast(None, jsii.invoke(self, "putDnsResolvers", [value]))

    @jsii.member(jsii_name="putEgress")
    def put_egress(
        self,
        *,
        ipv4: builtins.str,
        ipv6: builtins.str,
        ipv4_fallback: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ipv4: The IPv4 address to be used for egress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4 ZeroTrustGatewayPolicy#ipv4}
        :param ipv6: The IPv6 range to be used for egress. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv6 ZeroTrustGatewayPolicy#ipv6}
        :param ipv4_fallback: The IPv4 address to be used for egress in the event of an error egressing with the primary IPv4. Can be '0.0.0.0' to indicate local egreass via Warp IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ipv4_fallback ZeroTrustGatewayPolicy#ipv4_fallback}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsEgress(
            ipv4=ipv4, ipv6=ipv6, ipv4_fallback=ipv4_fallback
        )

        return typing.cast(None, jsii.invoke(self, "putEgress", [value]))

    @jsii.member(jsii_name="putL4Override")
    def put_l4_override(self, *, ip: builtins.str, port: jsii.Number) -> None:
        '''
        :param ip: Override IP to forward traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#ip ZeroTrustGatewayPolicy#ip}
        :param port: Override Port to forward traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#port ZeroTrustGatewayPolicy#port}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsL4Override(ip=ip, port=port)

        return typing.cast(None, jsii.invoke(self, "putL4Override", [value]))

    @jsii.member(jsii_name="putNotificationSettings")
    def put_notification_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#message ZeroTrustGatewayPolicy#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#support_url ZeroTrustGatewayPolicy#support_url}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsNotificationSettings(
            enabled=enabled, message=message, support_url=support_url
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationSettings", [value]))

    @jsii.member(jsii_name="putPayloadLog")
    def put_payload_log(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable or disable DLP Payload Logging for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsPayloadLog(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putPayloadLog", [value]))

    @jsii.member(jsii_name="putUntrustedCert")
    def put_untrusted_cert(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Action to be taken when the SSL certificate of upstream is invalid. Available values: ``pass_through``, ``block``, ``error``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        '''
        value = ZeroTrustGatewayPolicyRuleSettingsUntrustedCert(action=action)

        return typing.cast(None, jsii.invoke(self, "putUntrustedCert", [value]))

    @jsii.member(jsii_name="resetAddHeaders")
    def reset_add_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddHeaders", []))

    @jsii.member(jsii_name="resetAllowChildBypass")
    def reset_allow_child_bypass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowChildBypass", []))

    @jsii.member(jsii_name="resetAuditSsh")
    def reset_audit_ssh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditSsh", []))

    @jsii.member(jsii_name="resetBisoAdminControls")
    def reset_biso_admin_controls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBisoAdminControls", []))

    @jsii.member(jsii_name="resetBlockPageEnabled")
    def reset_block_page_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPageEnabled", []))

    @jsii.member(jsii_name="resetBlockPageReason")
    def reset_block_page_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPageReason", []))

    @jsii.member(jsii_name="resetBypassParentRule")
    def reset_bypass_parent_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassParentRule", []))

    @jsii.member(jsii_name="resetCheckSession")
    def reset_check_session(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckSession", []))

    @jsii.member(jsii_name="resetDnsResolvers")
    def reset_dns_resolvers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsResolvers", []))

    @jsii.member(jsii_name="resetEgress")
    def reset_egress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgress", []))

    @jsii.member(jsii_name="resetIgnoreCnameCategoryMatches")
    def reset_ignore_cname_category_matches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCnameCategoryMatches", []))

    @jsii.member(jsii_name="resetInsecureDisableDnssecValidation")
    def reset_insecure_disable_dnssec_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureDisableDnssecValidation", []))

    @jsii.member(jsii_name="resetIpCategories")
    def reset_ip_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCategories", []))

    @jsii.member(jsii_name="resetL4Override")
    def reset_l4_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Override", []))

    @jsii.member(jsii_name="resetNotificationSettings")
    def reset_notification_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationSettings", []))

    @jsii.member(jsii_name="resetOverrideHost")
    def reset_override_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideHost", []))

    @jsii.member(jsii_name="resetOverrideIps")
    def reset_override_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideIps", []))

    @jsii.member(jsii_name="resetPayloadLog")
    def reset_payload_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadLog", []))

    @jsii.member(jsii_name="resetResolveDnsThroughCloudflare")
    def reset_resolve_dns_through_cloudflare(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolveDnsThroughCloudflare", []))

    @jsii.member(jsii_name="resetUntrustedCert")
    def reset_untrusted_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntrustedCert", []))

    @builtins.property
    @jsii.member(jsii_name="auditSsh")
    def audit_ssh(self) -> ZeroTrustGatewayPolicyRuleSettingsAuditSshOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsAuditSshOutputReference, jsii.get(self, "auditSsh"))

    @builtins.property
    @jsii.member(jsii_name="bisoAdminControls")
    def biso_admin_controls(
        self,
    ) -> ZeroTrustGatewayPolicyRuleSettingsBisoAdminControlsOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsBisoAdminControlsOutputReference, jsii.get(self, "bisoAdminControls"))

    @builtins.property
    @jsii.member(jsii_name="checkSession")
    def check_session(
        self,
    ) -> ZeroTrustGatewayPolicyRuleSettingsCheckSessionOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsCheckSessionOutputReference, jsii.get(self, "checkSession"))

    @builtins.property
    @jsii.member(jsii_name="dnsResolvers")
    def dns_resolvers(
        self,
    ) -> ZeroTrustGatewayPolicyRuleSettingsDnsResolversOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsDnsResolversOutputReference, jsii.get(self, "dnsResolvers"))

    @builtins.property
    @jsii.member(jsii_name="egress")
    def egress(self) -> ZeroTrustGatewayPolicyRuleSettingsEgressOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsEgressOutputReference, jsii.get(self, "egress"))

    @builtins.property
    @jsii.member(jsii_name="l4Override")
    def l4_override(
        self,
    ) -> ZeroTrustGatewayPolicyRuleSettingsL4OverrideOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsL4OverrideOutputReference, jsii.get(self, "l4Override"))

    @builtins.property
    @jsii.member(jsii_name="notificationSettings")
    def notification_settings(
        self,
    ) -> ZeroTrustGatewayPolicyRuleSettingsNotificationSettingsOutputReference:
        return typing.cast(ZeroTrustGatewayPolicyRuleSettingsNotificationSettingsOutputReference, jsii.get(self, "notificationSettings"))

    @builtins.property
    @jsii.member(jsii_name="payloadLog")
    def payload_log(
        self,
    ) -> "ZeroTrustGatewayPolicyRuleSettingsPayloadLogOutputReference":
        return typing.cast("ZeroTrustGatewayPolicyRuleSettingsPayloadLogOutputReference", jsii.get(self, "payloadLog"))

    @builtins.property
    @jsii.member(jsii_name="untrustedCert")
    def untrusted_cert(
        self,
    ) -> "ZeroTrustGatewayPolicyRuleSettingsUntrustedCertOutputReference":
        return typing.cast("ZeroTrustGatewayPolicyRuleSettingsUntrustedCertOutputReference", jsii.get(self, "untrustedCert"))

    @builtins.property
    @jsii.member(jsii_name="addHeadersInput")
    def add_headers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "addHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowChildBypassInput")
    def allow_child_bypass_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowChildBypassInput"))

    @builtins.property
    @jsii.member(jsii_name="auditSshInput")
    def audit_ssh_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh], jsii.get(self, "auditSshInput"))

    @builtins.property
    @jsii.member(jsii_name="bisoAdminControlsInput")
    def biso_admin_controls_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls], jsii.get(self, "bisoAdminControlsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageEnabledInput")
    def block_page_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blockPageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageReasonInput")
    def block_page_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockPageReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassParentRuleInput")
    def bypass_parent_rule_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bypassParentRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="checkSessionInput")
    def check_session_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession], jsii.get(self, "checkSessionInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsResolversInput")
    def dns_resolvers_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers], jsii.get(self, "dnsResolversInput"))

    @builtins.property
    @jsii.member(jsii_name="egressInput")
    def egress_input(self) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress], jsii.get(self, "egressInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCnameCategoryMatchesInput")
    def ignore_cname_category_matches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCnameCategoryMatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureDisableDnssecValidationInput")
    def insecure_disable_dnssec_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureDisableDnssecValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCategoriesInput")
    def ip_categories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipCategoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="l4OverrideInput")
    def l4_override_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override], jsii.get(self, "l4OverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationSettingsInput")
    def notification_settings_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings], jsii.get(self, "notificationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideHostInput")
    def override_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideHostInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideIpsInput")
    def override_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "overrideIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadLogInput")
    def payload_log_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsPayloadLog"]:
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsPayloadLog"], jsii.get(self, "payloadLogInput"))

    @builtins.property
    @jsii.member(jsii_name="resolveDnsThroughCloudflareInput")
    def resolve_dns_through_cloudflare_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resolveDnsThroughCloudflareInput"))

    @builtins.property
    @jsii.member(jsii_name="untrustedCertInput")
    def untrusted_cert_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert"]:
        return typing.cast(typing.Optional["ZeroTrustGatewayPolicyRuleSettingsUntrustedCert"], jsii.get(self, "untrustedCertInput"))

    @builtins.property
    @jsii.member(jsii_name="addHeaders")
    def add_headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "addHeaders"))

    @add_headers.setter
    def add_headers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1f1f59b388e3b04d2fdc50bcdbc60dff8c312c77394e51f79fc0d9b92f994a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowChildBypass")
    def allow_child_bypass(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowChildBypass"))

    @allow_child_bypass.setter
    def allow_child_bypass(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1fc79c6b71da20148ca5347784263aad3f198663797834c88c471ac2f6931d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowChildBypass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockPageEnabled")
    def block_page_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blockPageEnabled"))

    @block_page_enabled.setter
    def block_page_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c07d9f8c9923508c1d3b62f502d6885231364fd4bb9b55025d663a8724fdbaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockPageEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blockPageReason")
    def block_page_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blockPageReason"))

    @block_page_reason.setter
    def block_page_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3d7023f11f573d6aa4c4544f31529aa72cdad798b28111ae3c6552206225a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockPageReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bypassParentRule")
    def bypass_parent_rule(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bypassParentRule"))

    @bypass_parent_rule.setter
    def bypass_parent_rule(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb65d78b3a1632140634e15585710dfceb0568352431b9f8446d8a5724d20f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassParentRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCnameCategoryMatches")
    def ignore_cname_category_matches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCnameCategoryMatches"))

    @ignore_cname_category_matches.setter
    def ignore_cname_category_matches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4927b6567e05d6e5b2db1c5b2bda5bf1451af31383f529e592384aa9be803593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCnameCategoryMatches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureDisableDnssecValidation")
    def insecure_disable_dnssec_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureDisableDnssecValidation"))

    @insecure_disable_dnssec_validation.setter
    def insecure_disable_dnssec_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bcb95e227278b99caf156a3ac3c9bc6a4fa2b8a8754c0b078eb2f6c5217ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureDisableDnssecValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCategories")
    def ip_categories(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipCategories"))

    @ip_categories.setter
    def ip_categories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f014d156e2c8bd4d2dbc18cac0b25ceace721dfd317b7e86bd517b6887b3cd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCategories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideHost")
    def override_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideHost"))

    @override_host.setter
    def override_host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bf89906aba8fc768c718b27a46d417bbdb17a2b72217c7e29b4b14a2bd7dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideIps")
    def override_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "overrideIps"))

    @override_ips.setter
    def override_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb235300b38c3bc913d31e7540997e53e6b2b3d34b84653711dcf7077567a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolveDnsThroughCloudflare")
    def resolve_dns_through_cloudflare(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resolveDnsThroughCloudflare"))

    @resolve_dns_through_cloudflare.setter
    def resolve_dns_through_cloudflare(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f244a322bbc2a1c167c15aec0b258cd8699df11dccce657701aba9b74e04f3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolveDnsThroughCloudflare", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettings]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817376f6438ce5c9a592596111f84b92b1694af7ef6956d0054320459c45801c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsPayloadLog",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ZeroTrustGatewayPolicyRuleSettingsPayloadLog:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable or disable DLP Payload Logging for this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b51240c3300c0b57214e6902ad1a0ceb3f4e668d2ed20f684b5475d28ffa52)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable or disable DLP Payload Logging for this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#enabled ZeroTrustGatewayPolicy#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsPayloadLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsPayloadLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsPayloadLogOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65667181409e7bb7a033d5bb7c77d32d87a33789cff432f6d8cb2dc31045537)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9824ebf004acc38e59c20e20925665eb2c2d3768d451cf96b49010d5521c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsPayloadLog]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsPayloadLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsPayloadLog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ccf9550ba44eee5bccc3ee04815bbe69f75d41d08cf37ea5c47ef167c46c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsUntrustedCert",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class ZeroTrustGatewayPolicyRuleSettingsUntrustedCert:
    def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
        '''
        :param action: Action to be taken when the SSL certificate of upstream is invalid. Available values: ``pass_through``, ``block``, ``error``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b688dd86837fff9fcf647af267f3c878d950d8ea4e7a2a8c9e8c3ce7e09e71fa)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Action to be taken when the SSL certificate of upstream is invalid. Available values: ``pass_through``, ``block``, ``error``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_policy#action ZeroTrustGatewayPolicy#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewayPolicyRuleSettingsUntrustedCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewayPolicyRuleSettingsUntrustedCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewayPolicy.ZeroTrustGatewayPolicyRuleSettingsUntrustedCertOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7071c4ca8192d51c7c471be9587d21242e649f892b6474bf5efa053f997942)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab7c9f74d80e11871006aeb9dc12808ee977fbebfaba5357da7c34b4e06604e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewayPolicyRuleSettingsUntrustedCert]:
        return typing.cast(typing.Optional[ZeroTrustGatewayPolicyRuleSettingsUntrustedCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsUntrustedCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4a37808e9878e4b67e98ae7a831999670583ffe153d2849dff1b1a0011d1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ZeroTrustGatewayPolicy",
    "ZeroTrustGatewayPolicyConfig",
    "ZeroTrustGatewayPolicyRuleSettings",
    "ZeroTrustGatewayPolicyRuleSettingsAuditSsh",
    "ZeroTrustGatewayPolicyRuleSettingsAuditSshOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls",
    "ZeroTrustGatewayPolicyRuleSettingsBisoAdminControlsOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsCheckSession",
    "ZeroTrustGatewayPolicyRuleSettingsCheckSessionOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolvers",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4List",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4OutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6List",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6OutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsDnsResolversOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsEgress",
    "ZeroTrustGatewayPolicyRuleSettingsEgressOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsL4Override",
    "ZeroTrustGatewayPolicyRuleSettingsL4OverrideOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsNotificationSettings",
    "ZeroTrustGatewayPolicyRuleSettingsNotificationSettingsOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsPayloadLog",
    "ZeroTrustGatewayPolicyRuleSettingsPayloadLogOutputReference",
    "ZeroTrustGatewayPolicyRuleSettingsUntrustedCert",
    "ZeroTrustGatewayPolicyRuleSettingsUntrustedCertOutputReference",
]

publication.publish()

def _typecheckingstub__e786f3b51fdd9d9ed8a9ede6d413dce3bca2cd0cf1cb66429b00315285745858(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    action: builtins.str,
    description: builtins.str,
    name: builtins.str,
    precedence: jsii.Number,
    device_posture: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[builtins.str] = None,
    rule_settings: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a82a394c6d2096b6cfe77d2cb2d7a0802d1cb0b8c4111b58a4499f87b9cb2b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bb7ba5f48d9b8e2a3bb95f022537a9bfc450f3475c72a300c1cae1683f9ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7bbd14973f8b3f0a43994b287c91e533e76cb5b8c5e095101c90750c11d93b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83db28167eff420a547cf252dd8e7781e5796c1cace39c68df6c1a06b2da2d0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee39d2975aef69e34e1a231b8e211addc371b9ad64dceb2f20e20d4ae852c237(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45825779e8075f762c6a646e54a09f77631a4328dfb317cc06b661e8121e179b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18e5f294f5711f739edce78df2d227cbee0051bd29aba76a875d970ca98100b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199dad41e61259de131f6a72dd8ad9affc8ef8c527c7afeb38ce174cd0a6c61c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fff43c71cbeb7eff49371043e13151751ba92b81c1e0493e6f2f3ebce50d929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa62bd411e5957a4f46d586eb095eb3d653370b09ee649ce6849dd5a2d07624b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5210b06d00643b59aad339b83d84162c64bdb7c26827fb9528babd7e3e61786c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872dd1a90e3d9f1a1ba75703168e5c9754c8cbf3777f03ea7b5294d225912329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3d5137255dbb7219c971b313cd804791e2a0ef37964d8a593b17f6a3718187(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    action: builtins.str,
    description: builtins.str,
    name: builtins.str,
    precedence: jsii.Number,
    device_posture: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[builtins.str] = None,
    rule_settings: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8f89e3048662a05610c3fc4775c975b8cbfc7190cf304482a2b63c0a5c20af(
    *,
    add_headers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allow_child_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    audit_ssh: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsAuditSsh, typing.Dict[builtins.str, typing.Any]]] = None,
    biso_admin_controls: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    block_page_reason: typing.Optional[builtins.str] = None,
    bypass_parent_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_session: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsCheckSession, typing.Dict[builtins.str, typing.Any]]] = None,
    dns_resolvers: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers, typing.Dict[builtins.str, typing.Any]]] = None,
    egress: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsEgress, typing.Dict[builtins.str, typing.Any]]] = None,
    ignore_cname_category_matches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    insecure_disable_dnssec_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_categories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    l4_override: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsL4Override, typing.Dict[builtins.str, typing.Any]]] = None,
    notification_settings: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    override_host: typing.Optional[builtins.str] = None,
    override_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    payload_log: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsPayloadLog, typing.Dict[builtins.str, typing.Any]]] = None,
    resolve_dns_through_cloudflare: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    untrusted_cert: typing.Optional[typing.Union[ZeroTrustGatewayPolicyRuleSettingsUntrustedCert, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e13806ef402ec94ed21dd8e335b31ece45f371213e9bd91cd4f83a977b851a3(
    *,
    command_logging: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7cbe1aad2274aab866344e2e4178aa08f6f0894258b0a1d57502ac56a236f45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9da99cbe034882dfcd29f81babcb2a2c1f9170d681b8bdcfdf43385b072238(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5fc353cec0452da1882b51e0644b7d85e988ab68deb41c5016c972fb20c440(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsAuditSsh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd65a816aca7befaa772d1c5d0ecc9d1f288ab4e81f1ffdade3c911a0b13b14(
    *,
    disable_clipboard_redirection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_copy_paste: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_keyboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_printing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_upload: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e487688fb41ca3eaba6906db9cc86e97d2f8b3c4b56ad97fcb47b4ac4a290d93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bbcec73a36fe7169ee4ee06744bac7806848fe3b7ca8fa570d03ed444765a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbea7feea9d1db4a4a40fd2a41878db080aba8e2041189c592cff4ab2993913(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88937c12c1d5f3f330962cf416ce6554dbedad8460bedfb586fbdbe8894c9dcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f8c3f6b69fd2fa48e05564c519de28dce43b69c2c4549435901d1a554a636c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e80f7749ea055b75493a4ef78600bb41e387f7d26dfc4db8d1a341b2775790(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33def006c69a6239b3c2addd29dba93eb7f0636cb665013b749278343319da4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b16262088665bd23c4414f6ce9e1ef921a03111175eb5160228b5b8cbdb35cb(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsBisoAdminControls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56199ee2205a76f737af972538e10f89fe9b1ad3b1ae437325cab49c99f6877b(
    *,
    duration: builtins.str,
    enforce: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e808649dd9d4901863979bb24d8623d67310b6fc114de70bc108fa8480a248(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b8a53e3936669c3400cdac4a0dcaa9df95fde0f9b01f93cddf02a0f6de668b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704639372dcc580a04c74d5c5fb881b8f14087b8aad093f31515ad4d3b70b1b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cea6cb3a0aa5166676514ff8fe2f424ad1b786908f73d5bd1b9cc8d02add24(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsCheckSession],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61e86bdabb946d2d3a72397fbab37eed75de1962c303d02d391da06329eb2b1(
    *,
    ipv4: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ipv6: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c24719bdc3038d165f74ab720bef83026321ba3145104cfaa1c1b20d148cab8(
    *,
    ip: builtins.str,
    port: typing.Optional[jsii.Number] = None,
    route_through_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8325a1a409077918c933b460bfcc5f3a826ee186f245ca9839b836c70d772e06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533b1bf8395b943248c885e85812eb93b2a774de10422d63612cf28ac14cafaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c2d41d484fcff6d4869072b8c656d8d1637c6d2ded398ea49a1d65dbaebbd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dd7a58248308472bd5468feb92374998e6b7b5590ec736782c3a553637e060(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71763ee18b7be04bf6a77a7792383688b0cfd8db3c6ed614cd32776113332c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe57289c5a429db420b6145e99ddaaf5ede4dc135885cf66ffa8e5fa4303b979(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b79a03168b1f67148b565cda58d26b288c914a1d512954035060c72b5e3d87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fd7414892d1597a66dac08101d741d4f8d59be453c0dea8a8d1338514cb5b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f65de8183eaebfe0f9215db319b0e90ea52991fb28e72d46082a8ace1646ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4329b10738e673d9049a8ce03c03876d48454709cdddfc3de5497fc5492f8189(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b0d19c27d6fd136e1e0d206878f3628b4675a45ec9fc28cefe607883cb7397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fe51044e877d271f848c76ef15c1b3e10a340760aa9758e97ea688bc18e0a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f85e4dfa7046f3af0deee7ff5a1e3a4b86af348b71fe1af87e2692b77712992(
    *,
    ip: builtins.str,
    port: typing.Optional[jsii.Number] = None,
    route_through_private_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4bfb32196b3551481e8cca349977d12590376dd4642cc0bc2726152543abe8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc981020efa520611da174b7843290c261f1dc2e2a32ec583c026ee3b10931fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8407ffb93365f1e2e11b27875a35c4dca52915c0e1f10356b9a1e7ef826cbc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6117090d75a8b51dc4d30205a60b06123d6019c3934be55e60967b5f4d56c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0a68cd7314b423e0e39a7e15fbd9a1108fa2272438d35e24cb18ade3535045(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80c31a75c73774f61153c8df8e0968b4f59e3a499f73f0e7f101d5efe967bd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aefc0967e7ec9bfc17da46922d77545c41748b7953a536aa596d76d466151ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d1a1427283f10bb887bae9c8c09aa3473bb39bee635cb748cc7bec7288aff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0988a9d00ba8ce08c0f3fe89efeabad47e3fd9a2817225d945e7d064436329d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8866e5fdf3ff5e525fe793fa1633c72c80b4ba2ef2047c9e8d0446894140b9ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f45582a25857306e9cd17c9127b3d076c4693372dd57adbbf473a7705fc42db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bb6c8dd0d7cf527e474f84d5a925a39708320a10e08bdafbc5a00915848a41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe77d83fd907f5544880a4f430e59c13a1392f63bd7abfafdef6f884393e209(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669ea23d8599a8644f7eeadecdb0f6bdc876d012383fbd95625edd251989a36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv4, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dc0db711eacec9887cafb44e734357f3d89b9fb5f4d297e2f7ca1f2c366bd8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustGatewayPolicyRuleSettingsDnsResolversIpv6, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298b64663e24f0ea5c0535778501a4f36f10bbaead2fca81e35f69674e0c9d84(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsDnsResolvers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c20c20790982b1f4876312fe70df67926222adacb75525c029e94887d98091(
    *,
    ipv4: builtins.str,
    ipv6: builtins.str,
    ipv4_fallback: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0796cb8575c970172d0ce9e0ad3d1e0860b3ab8d36b679e13b1f966c06bade9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966af7cdf684fe3aa938943063e2d7977054accb6cead27577e182dd385c3c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6e3514c0230e5012ef0492d45c9d1b43937198b0bd8b5bd65da9a5cc57ee88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a862b5eb8ce043e340f8e643740e87ed76e3bbe47211aecb9ed70ca4ad785c12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6833a6d490876a271d35b87f147a66acb5deb7685ab224819007c64d0e400263(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsEgress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbef793f0f9dfeabe7b5485433aab6102e162df9a897abc8d4b8aa339fee92ea(
    *,
    ip: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6376ac5fce76140ef3b8fb4f6af9e78a84d144fa24bf3dea6601411840482eb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a062656fb3774493c7ec44c60f40ddae4dcc2ab4ae76d3fac41cfca847cee672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5059f6a84f9af734199f2419a73019521b0ef42cdde25d33f3848ffa428e0aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6992764ef0e447a8c43336bc9eb62ac1a401718853c978e226e191973c17cb66(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsL4Override],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db5c5eeaf4ff44b629eb99747f03cd75818482acd82211db67f8e37ddf7fc2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727c90cf4d7e78e845de5b7b5c003c1d7edca7319b28566b450c0738e7d213fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07fe27be482df4e82f9d62e5ba477d03b5e5c742909acc39649a932218a327d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d84b8cc06ab08f7faaa2667ba6cd5bff03d1528475aad86fda1a6c8af8c291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fef0f410d5c6360be8db0b53fa52f68d0a745a5d8ac7815daf6cddc788b82e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6537fcfae534b3c752b2fbe6489d26533be9a49e9425c470c18a6d3d0f036ea7(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsNotificationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1fbdcc6d5b96639588760d6d409fb65e4ee361bc0d52ea6c5e7f0dbd6ada66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1f1f59b388e3b04d2fdc50bcdbc60dff8c312c77394e51f79fc0d9b92f994a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1fc79c6b71da20148ca5347784263aad3f198663797834c88c471ac2f6931d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c07d9f8c9923508c1d3b62f502d6885231364fd4bb9b55025d663a8724fdbaf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3d7023f11f573d6aa4c4544f31529aa72cdad798b28111ae3c6552206225a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb65d78b3a1632140634e15585710dfceb0568352431b9f8446d8a5724d20f54(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4927b6567e05d6e5b2db1c5b2bda5bf1451af31383f529e592384aa9be803593(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bcb95e227278b99caf156a3ac3c9bc6a4fa2b8a8754c0b078eb2f6c5217ea6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f014d156e2c8bd4d2dbc18cac0b25ceace721dfd317b7e86bd517b6887b3cd45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bf89906aba8fc768c718b27a46d417bbdb17a2b72217c7e29b4b14a2bd7dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb235300b38c3bc913d31e7540997e53e6b2b3d34b84653711dcf7077567a4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f244a322bbc2a1c167c15aec0b258cd8699df11dccce657701aba9b74e04f3df(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817376f6438ce5c9a592596111f84b92b1694af7ef6956d0054320459c45801c(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b51240c3300c0b57214e6902ad1a0ceb3f4e668d2ed20f684b5475d28ffa52(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65667181409e7bb7a033d5bb7c77d32d87a33789cff432f6d8cb2dc31045537(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9824ebf004acc38e59c20e20925665eb2c2d3768d451cf96b49010d5521c4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ccf9550ba44eee5bccc3ee04815bbe69f75d41d08cf37ea5c47ef167c46c67(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsPayloadLog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b688dd86837fff9fcf647af267f3c878d950d8ea4e7a2a8c9e8c3ce7e09e71fa(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7071c4ca8192d51c7c471be9587d21242e649f892b6474bf5efa053f997942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab7c9f74d80e11871006aeb9dc12808ee977fbebfaba5357da7c34b4e06604e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4a37808e9878e4b67e98ae7a831999670583ffe153d2849dff1b1a0011d1ba(
    value: typing.Optional[ZeroTrustGatewayPolicyRuleSettingsUntrustedCert],
) -> None:
    """Type checking stubs"""
    pass
