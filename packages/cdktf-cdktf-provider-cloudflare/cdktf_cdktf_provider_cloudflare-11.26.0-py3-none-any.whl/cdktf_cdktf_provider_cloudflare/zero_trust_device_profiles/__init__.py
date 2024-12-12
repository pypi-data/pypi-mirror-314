r'''
# `cloudflare_zero_trust_device_profiles`

Refer to the Terraform Registry for docs: [`cloudflare_zero_trust_device_profiles`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles).
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


class ZeroTrustDeviceProfiles(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustDeviceProfiles.ZeroTrustDeviceProfiles",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles cloudflare_zero_trust_device_profiles}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        description: builtins.str,
        name: builtins.str,
        allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_connect: typing.Optional[jsii.Number] = None,
        captive_portal: typing.Optional[jsii.Number] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_office_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        service_mode_v2_mode: typing.Optional[builtins.str] = None,
        service_mode_v2_port: typing.Optional[jsii.Number] = None,
        support_url: typing.Optional[builtins.str] = None,
        switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel_protocol: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles cloudflare_zero_trust_device_profiles} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#account_id ZeroTrustDeviceProfiles#account_id}
        :param description: Description of Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#description ZeroTrustDeviceProfiles#description}
        :param name: Name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#name ZeroTrustDeviceProfiles#name}
        :param allowed_to_leave: Whether to allow devices to leave the organization. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allowed_to_leave ZeroTrustDeviceProfiles#allowed_to_leave}
        :param allow_mode_switch: Whether to allow mode switch for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_mode_switch ZeroTrustDeviceProfiles#allow_mode_switch}
        :param allow_updates: Whether to allow updates under this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_updates ZeroTrustDeviceProfiles#allow_updates}
        :param auto_connect: The amount of time in seconds to reconnect after having been disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#auto_connect ZeroTrustDeviceProfiles#auto_connect}
        :param captive_portal: The captive portal value for this policy. Defaults to ``180``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#captive_portal ZeroTrustDeviceProfiles#captive_portal}
        :param default: Whether the policy refers to the default account policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#default ZeroTrustDeviceProfiles#default}
        :param disable_auto_fallback: Whether to disable auto fallback for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#disable_auto_fallback ZeroTrustDeviceProfiles#disable_auto_fallback}
        :param enabled: Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#enabled ZeroTrustDeviceProfiles#enabled}
        :param exclude_office_ips: Whether to add Microsoft IPs to split tunnel exclusions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#exclude_office_ips ZeroTrustDeviceProfiles#exclude_office_ips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#id ZeroTrustDeviceProfiles#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#match ZeroTrustDeviceProfiles#match}
        :param precedence: The precedence of the policy. Lower values indicate higher precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#precedence ZeroTrustDeviceProfiles#precedence}
        :param service_mode_v2_mode: The service mode. Available values: ``1dot1``, ``warp``, ``proxy``, ``posture_only``, ``warp_tunnel_only``. Defaults to ``warp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_mode ZeroTrustDeviceProfiles#service_mode_v2_mode}
        :param service_mode_v2_port: The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_port ZeroTrustDeviceProfiles#service_mode_v2_port}
        :param support_url: The support URL that will be opened when sending feedback. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#support_url ZeroTrustDeviceProfiles#support_url}
        :param switch_locked: Enablement of the ZT client switch lock. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#switch_locked ZeroTrustDeviceProfiles#switch_locked}
        :param tunnel_protocol: Determines which tunnel protocol to use. Available values: ``""``, ``wireguard``, ``masque``. Defaults to ``wireguard``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#tunnel_protocol ZeroTrustDeviceProfiles#tunnel_protocol}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a94795cd422e70fe2040aadded521c77178341e23daf261ff1f79fdd41d9fa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZeroTrustDeviceProfilesConfig(
            account_id=account_id,
            description=description,
            name=name,
            allowed_to_leave=allowed_to_leave,
            allow_mode_switch=allow_mode_switch,
            allow_updates=allow_updates,
            auto_connect=auto_connect,
            captive_portal=captive_portal,
            default=default,
            disable_auto_fallback=disable_auto_fallback,
            enabled=enabled,
            exclude_office_ips=exclude_office_ips,
            id=id,
            match=match,
            precedence=precedence,
            service_mode_v2_mode=service_mode_v2_mode,
            service_mode_v2_port=service_mode_v2_port,
            support_url=support_url,
            switch_locked=switch_locked,
            tunnel_protocol=tunnel_protocol,
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
        '''Generates CDKTF code for importing a ZeroTrustDeviceProfiles resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ZeroTrustDeviceProfiles to import.
        :param import_from_id: The id of the existing ZeroTrustDeviceProfiles that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ZeroTrustDeviceProfiles to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391546eff6fadb00ddd82b3c560708c4d453dbbf2a4fd4705b44d57ed2b741a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAllowedToLeave")
    def reset_allowed_to_leave(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedToLeave", []))

    @jsii.member(jsii_name="resetAllowModeSwitch")
    def reset_allow_mode_switch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowModeSwitch", []))

    @jsii.member(jsii_name="resetAllowUpdates")
    def reset_allow_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowUpdates", []))

    @jsii.member(jsii_name="resetAutoConnect")
    def reset_auto_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoConnect", []))

    @jsii.member(jsii_name="resetCaptivePortal")
    def reset_captive_portal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaptivePortal", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDisableAutoFallback")
    def reset_disable_auto_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableAutoFallback", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExcludeOfficeIps")
    def reset_exclude_office_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeOfficeIps", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetPrecedence")
    def reset_precedence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrecedence", []))

    @jsii.member(jsii_name="resetServiceModeV2Mode")
    def reset_service_mode_v2_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceModeV2Mode", []))

    @jsii.member(jsii_name="resetServiceModeV2Port")
    def reset_service_mode_v2_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceModeV2Port", []))

    @jsii.member(jsii_name="resetSupportUrl")
    def reset_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportUrl", []))

    @jsii.member(jsii_name="resetSwitchLocked")
    def reset_switch_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSwitchLocked", []))

    @jsii.member(jsii_name="resetTunnelProtocol")
    def reset_tunnel_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelProtocol", []))

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
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedToLeaveInput")
    def allowed_to_leave_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowedToLeaveInput"))

    @builtins.property
    @jsii.member(jsii_name="allowModeSwitchInput")
    def allow_mode_switch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowModeSwitchInput"))

    @builtins.property
    @jsii.member(jsii_name="allowUpdatesInput")
    def allow_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoConnectInput")
    def auto_connect_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="captivePortalInput")
    def captive_portal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "captivePortalInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disableAutoFallbackInput")
    def disable_auto_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableAutoFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeOfficeIpsInput")
    def exclude_office_ips_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeOfficeIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2ModeInput")
    def service_mode_v2_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceModeV2ModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2PortInput")
    def service_mode_v2_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serviceModeV2PortInput"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlInput")
    def support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="switchLockedInput")
    def switch_locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "switchLockedInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelProtocolInput")
    def tunnel_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a6eab02b20f403c7f6bc3890af60040384548b355153f08c817200f2aa8966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedToLeave")
    def allowed_to_leave(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowedToLeave"))

    @allowed_to_leave.setter
    def allowed_to_leave(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88913fa411a4b5659f606385f5146ae18a2db1340a258410cceaa70b000422b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedToLeave", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowModeSwitch")
    def allow_mode_switch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowModeSwitch"))

    @allow_mode_switch.setter
    def allow_mode_switch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03dc384135e05ebd6aace0df014d455e6150a49ddf4930e2bbfdb1c412ffbf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowModeSwitch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowUpdates")
    def allow_updates(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowUpdates"))

    @allow_updates.setter
    def allow_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5056d3f32fb9a8473a19d8e47c5e57df9d2706e06b4ebdef0976c3d2948986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowUpdates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoConnect")
    def auto_connect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoConnect"))

    @auto_connect.setter
    def auto_connect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbd95c2803a4fc3f1ed46b062a6dd1a632c203ec6025be6385b2a520f84ff10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="captivePortal")
    def captive_portal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "captivePortal"))

    @captive_portal.setter
    def captive_portal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3a403f5378641f5b4db82f2798e41169103857826921af6d8bac1e414a795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "captivePortal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eca38a6c949839edfec11851e12139a33a8f31688de2a949c14a9a7abc01ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d1f448d7848e26fb7748bb745aa9dda8c726c8c8512a1975e92e1aa3c40d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableAutoFallback")
    def disable_auto_fallback(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableAutoFallback"))

    @disable_auto_fallback.setter
    def disable_auto_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ad3e91f42c2eb9fb9ce4cd327adb97c5389773c1df180f3207a7f35fb47da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableAutoFallback", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__56f57007fa5a2936ecefcfbc68193b72cbb93c45ba88de732c3cc3b3b978cca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeOfficeIps")
    def exclude_office_ips(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeOfficeIps"))

    @exclude_office_ips.setter
    def exclude_office_ips(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a798911a6d1afd26b8e8e5fd0078f3a21a3b01bcb21fb097b49ef04082988cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeOfficeIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3dd4ae1f12b20337096c1bbc657886248a615f1534e205aec1fa0cee6b84c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c98392c29329097151d0873cb262378d578084f56e8d4e8d3d0578a63eb75ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e73394f78f344f4f4a1d85848f79fc4faa90e5754d12aafbfae80f42a0c1a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8991eab084edcee3f0f05da068c62bb0be61adf19ad56525d4a3103571dc7b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2Mode")
    def service_mode_v2_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceModeV2Mode"))

    @service_mode_v2_mode.setter
    def service_mode_v2_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148ec053e948df909f0a1718ec0d1224af4de3beb4d0a8ffe1217b7a9fcacec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceModeV2Mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceModeV2Port")
    def service_mode_v2_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serviceModeV2Port"))

    @service_mode_v2_port.setter
    def service_mode_v2_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e151d2a5e3a45ab1e6c6d2b9ac582620a7ac452ae317c8196ca8672551e3ce9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceModeV2Port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fd240b6a69609e47941861487d39470da3fe28ee2625391705e9caf7b2d399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="switchLocked")
    def switch_locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "switchLocked"))

    @switch_locked.setter
    def switch_locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bfe4aed5dfe7b511c59a6ff964f745d21da967790bc7351b80aa645030ff7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "switchLocked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelProtocol")
    def tunnel_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelProtocol"))

    @tunnel_protocol.setter
    def tunnel_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d9b667b6756f642c874b12f4103f0bd0bdf4737062cfa7dd7c6f29cff2b126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelProtocol", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustDeviceProfiles.ZeroTrustDeviceProfilesConfig",
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
        "description": "description",
        "name": "name",
        "allowed_to_leave": "allowedToLeave",
        "allow_mode_switch": "allowModeSwitch",
        "allow_updates": "allowUpdates",
        "auto_connect": "autoConnect",
        "captive_portal": "captivePortal",
        "default": "default",
        "disable_auto_fallback": "disableAutoFallback",
        "enabled": "enabled",
        "exclude_office_ips": "excludeOfficeIps",
        "id": "id",
        "match": "match",
        "precedence": "precedence",
        "service_mode_v2_mode": "serviceModeV2Mode",
        "service_mode_v2_port": "serviceModeV2Port",
        "support_url": "supportUrl",
        "switch_locked": "switchLocked",
        "tunnel_protocol": "tunnelProtocol",
    },
)
class ZeroTrustDeviceProfilesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        name: builtins.str,
        allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_connect: typing.Optional[jsii.Number] = None,
        captive_portal: typing.Optional[jsii.Number] = None,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_office_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        match: typing.Optional[builtins.str] = None,
        precedence: typing.Optional[jsii.Number] = None,
        service_mode_v2_mode: typing.Optional[builtins.str] = None,
        service_mode_v2_port: typing.Optional[jsii.Number] = None,
        support_url: typing.Optional[builtins.str] = None,
        switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel_protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#account_id ZeroTrustDeviceProfiles#account_id}
        :param description: Description of Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#description ZeroTrustDeviceProfiles#description}
        :param name: Name of the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#name ZeroTrustDeviceProfiles#name}
        :param allowed_to_leave: Whether to allow devices to leave the organization. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allowed_to_leave ZeroTrustDeviceProfiles#allowed_to_leave}
        :param allow_mode_switch: Whether to allow mode switch for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_mode_switch ZeroTrustDeviceProfiles#allow_mode_switch}
        :param allow_updates: Whether to allow updates under this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_updates ZeroTrustDeviceProfiles#allow_updates}
        :param auto_connect: The amount of time in seconds to reconnect after having been disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#auto_connect ZeroTrustDeviceProfiles#auto_connect}
        :param captive_portal: The captive portal value for this policy. Defaults to ``180``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#captive_portal ZeroTrustDeviceProfiles#captive_portal}
        :param default: Whether the policy refers to the default account policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#default ZeroTrustDeviceProfiles#default}
        :param disable_auto_fallback: Whether to disable auto fallback for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#disable_auto_fallback ZeroTrustDeviceProfiles#disable_auto_fallback}
        :param enabled: Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#enabled ZeroTrustDeviceProfiles#enabled}
        :param exclude_office_ips: Whether to add Microsoft IPs to split tunnel exclusions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#exclude_office_ips ZeroTrustDeviceProfiles#exclude_office_ips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#id ZeroTrustDeviceProfiles#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param match: Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#match ZeroTrustDeviceProfiles#match}
        :param precedence: The precedence of the policy. Lower values indicate higher precedence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#precedence ZeroTrustDeviceProfiles#precedence}
        :param service_mode_v2_mode: The service mode. Available values: ``1dot1``, ``warp``, ``proxy``, ``posture_only``, ``warp_tunnel_only``. Defaults to ``warp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_mode ZeroTrustDeviceProfiles#service_mode_v2_mode}
        :param service_mode_v2_port: The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_port ZeroTrustDeviceProfiles#service_mode_v2_port}
        :param support_url: The support URL that will be opened when sending feedback. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#support_url ZeroTrustDeviceProfiles#support_url}
        :param switch_locked: Enablement of the ZT client switch lock. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#switch_locked ZeroTrustDeviceProfiles#switch_locked}
        :param tunnel_protocol: Determines which tunnel protocol to use. Available values: ``""``, ``wireguard``, ``masque``. Defaults to ``wireguard``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#tunnel_protocol ZeroTrustDeviceProfiles#tunnel_protocol}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d65e1baf61cfd3b5a5393c737468dc23fb57f098459868934678fa10ddd1079)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_to_leave", value=allowed_to_leave, expected_type=type_hints["allowed_to_leave"])
            check_type(argname="argument allow_mode_switch", value=allow_mode_switch, expected_type=type_hints["allow_mode_switch"])
            check_type(argname="argument allow_updates", value=allow_updates, expected_type=type_hints["allow_updates"])
            check_type(argname="argument auto_connect", value=auto_connect, expected_type=type_hints["auto_connect"])
            check_type(argname="argument captive_portal", value=captive_portal, expected_type=type_hints["captive_portal"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument disable_auto_fallback", value=disable_auto_fallback, expected_type=type_hints["disable_auto_fallback"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exclude_office_ips", value=exclude_office_ips, expected_type=type_hints["exclude_office_ips"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument service_mode_v2_mode", value=service_mode_v2_mode, expected_type=type_hints["service_mode_v2_mode"])
            check_type(argname="argument service_mode_v2_port", value=service_mode_v2_port, expected_type=type_hints["service_mode_v2_port"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument switch_locked", value=switch_locked, expected_type=type_hints["switch_locked"])
            check_type(argname="argument tunnel_protocol", value=tunnel_protocol, expected_type=type_hints["tunnel_protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "description": description,
            "name": name,
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
        if allowed_to_leave is not None:
            self._values["allowed_to_leave"] = allowed_to_leave
        if allow_mode_switch is not None:
            self._values["allow_mode_switch"] = allow_mode_switch
        if allow_updates is not None:
            self._values["allow_updates"] = allow_updates
        if auto_connect is not None:
            self._values["auto_connect"] = auto_connect
        if captive_portal is not None:
            self._values["captive_portal"] = captive_portal
        if default is not None:
            self._values["default"] = default
        if disable_auto_fallback is not None:
            self._values["disable_auto_fallback"] = disable_auto_fallback
        if enabled is not None:
            self._values["enabled"] = enabled
        if exclude_office_ips is not None:
            self._values["exclude_office_ips"] = exclude_office_ips
        if id is not None:
            self._values["id"] = id
        if match is not None:
            self._values["match"] = match
        if precedence is not None:
            self._values["precedence"] = precedence
        if service_mode_v2_mode is not None:
            self._values["service_mode_v2_mode"] = service_mode_v2_mode
        if service_mode_v2_port is not None:
            self._values["service_mode_v2_port"] = service_mode_v2_port
        if support_url is not None:
            self._values["support_url"] = support_url
        if switch_locked is not None:
            self._values["switch_locked"] = switch_locked
        if tunnel_protocol is not None:
            self._values["tunnel_protocol"] = tunnel_protocol

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#account_id ZeroTrustDeviceProfiles#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Description of Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#description ZeroTrustDeviceProfiles#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#name ZeroTrustDeviceProfiles#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_to_leave(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow devices to leave the organization. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allowed_to_leave ZeroTrustDeviceProfiles#allowed_to_leave}
        '''
        result = self._values.get("allowed_to_leave")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_mode_switch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow mode switch for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_mode_switch ZeroTrustDeviceProfiles#allow_mode_switch}
        '''
        result = self._values.get("allow_mode_switch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow updates under this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#allow_updates ZeroTrustDeviceProfiles#allow_updates}
        '''
        result = self._values.get("allow_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_connect(self) -> typing.Optional[jsii.Number]:
        '''The amount of time in seconds to reconnect after having been disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#auto_connect ZeroTrustDeviceProfiles#auto_connect}
        '''
        result = self._values.get("auto_connect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def captive_portal(self) -> typing.Optional[jsii.Number]:
        '''The captive portal value for this policy. Defaults to ``180``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#captive_portal ZeroTrustDeviceProfiles#captive_portal}
        '''
        result = self._values.get("captive_portal")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the policy refers to the default account policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#default ZeroTrustDeviceProfiles#default}
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_auto_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable auto fallback for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#disable_auto_fallback ZeroTrustDeviceProfiles#disable_auto_fallback}
        '''
        result = self._values.get("disable_auto_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the policy is enabled (cannot be set for default policies). Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#enabled ZeroTrustDeviceProfiles#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_office_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to add Microsoft IPs to split tunnel exclusions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#exclude_office_ips ZeroTrustDeviceProfiles#exclude_office_ips}
        '''
        result = self._values.get("exclude_office_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#id ZeroTrustDeviceProfiles#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional[builtins.str]:
        '''Wirefilter expression to match a device against when evaluating whether this policy should take effect for that device.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#match ZeroTrustDeviceProfiles#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def precedence(self) -> typing.Optional[jsii.Number]:
        '''The precedence of the policy. Lower values indicate higher precedence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#precedence ZeroTrustDeviceProfiles#precedence}
        '''
        result = self._values.get("precedence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_mode_v2_mode(self) -> typing.Optional[builtins.str]:
        '''The service mode. Available values: ``1dot1``, ``warp``, ``proxy``, ``posture_only``, ``warp_tunnel_only``. Defaults to ``warp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_mode ZeroTrustDeviceProfiles#service_mode_v2_mode}
        '''
        result = self._values.get("service_mode_v2_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_mode_v2_port(self) -> typing.Optional[jsii.Number]:
        '''The port to use for the proxy service mode. Required when using ``service_mode_v2_mode``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#service_mode_v2_port ZeroTrustDeviceProfiles#service_mode_v2_port}
        '''
        result = self._values.get("service_mode_v2_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''The support URL that will be opened when sending feedback.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#support_url ZeroTrustDeviceProfiles#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def switch_locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enablement of the ZT client switch lock.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#switch_locked ZeroTrustDeviceProfiles#switch_locked}
        '''
        result = self._values.get("switch_locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel_protocol(self) -> typing.Optional[builtins.str]:
        '''Determines which tunnel protocol to use. Available values: ``""``, ``wireguard``, ``masque``. Defaults to ``wireguard``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_device_profiles#tunnel_protocol ZeroTrustDeviceProfiles#tunnel_protocol}
        '''
        result = self._values.get("tunnel_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustDeviceProfilesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ZeroTrustDeviceProfiles",
    "ZeroTrustDeviceProfilesConfig",
]

publication.publish()

def _typecheckingstub__7a94795cd422e70fe2040aadded521c77178341e23daf261ff1f79fdd41d9fa7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    description: builtins.str,
    name: builtins.str,
    allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_connect: typing.Optional[jsii.Number] = None,
    captive_portal: typing.Optional[jsii.Number] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_office_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[builtins.str] = None,
    precedence: typing.Optional[jsii.Number] = None,
    service_mode_v2_mode: typing.Optional[builtins.str] = None,
    service_mode_v2_port: typing.Optional[jsii.Number] = None,
    support_url: typing.Optional[builtins.str] = None,
    switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel_protocol: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__391546eff6fadb00ddd82b3c560708c4d453dbbf2a4fd4705b44d57ed2b741a3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a6eab02b20f403c7f6bc3890af60040384548b355153f08c817200f2aa8966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88913fa411a4b5659f606385f5146ae18a2db1340a258410cceaa70b000422b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03dc384135e05ebd6aace0df014d455e6150a49ddf4930e2bbfdb1c412ffbf1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5056d3f32fb9a8473a19d8e47c5e57df9d2706e06b4ebdef0976c3d2948986(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbd95c2803a4fc3f1ed46b062a6dd1a632c203ec6025be6385b2a520f84ff10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3a403f5378641f5b4db82f2798e41169103857826921af6d8bac1e414a795(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eca38a6c949839edfec11851e12139a33a8f31688de2a949c14a9a7abc01ce0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d1f448d7848e26fb7748bb745aa9dda8c726c8c8512a1975e92e1aa3c40d33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ad3e91f42c2eb9fb9ce4cd327adb97c5389773c1df180f3207a7f35fb47da1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f57007fa5a2936ecefcfbc68193b72cbb93c45ba88de732c3cc3b3b978cca1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a798911a6d1afd26b8e8e5fd0078f3a21a3b01bcb21fb097b49ef04082988cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3dd4ae1f12b20337096c1bbc657886248a615f1534e205aec1fa0cee6b84c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c98392c29329097151d0873cb262378d578084f56e8d4e8d3d0578a63eb75ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e73394f78f344f4f4a1d85848f79fc4faa90e5754d12aafbfae80f42a0c1a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8991eab084edcee3f0f05da068c62bb0be61adf19ad56525d4a3103571dc7b38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148ec053e948df909f0a1718ec0d1224af4de3beb4d0a8ffe1217b7a9fcacec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e151d2a5e3a45ab1e6c6d2b9ac582620a7ac452ae317c8196ca8672551e3ce9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fd240b6a69609e47941861487d39470da3fe28ee2625391705e9caf7b2d399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bfe4aed5dfe7b511c59a6ff964f745d21da967790bc7351b80aa645030ff7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d9b667b6756f642c874b12f4103f0bd0bdf4737062cfa7dd7c6f29cff2b126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d65e1baf61cfd3b5a5393c737468dc23fb57f098459868934678fa10ddd1079(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    description: builtins.str,
    name: builtins.str,
    allowed_to_leave: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_mode_switch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_connect: typing.Optional[jsii.Number] = None,
    captive_portal: typing.Optional[jsii.Number] = None,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_auto_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_office_ips: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    match: typing.Optional[builtins.str] = None,
    precedence: typing.Optional[jsii.Number] = None,
    service_mode_v2_mode: typing.Optional[builtins.str] = None,
    service_mode_v2_port: typing.Optional[jsii.Number] = None,
    support_url: typing.Optional[builtins.str] = None,
    switch_locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
