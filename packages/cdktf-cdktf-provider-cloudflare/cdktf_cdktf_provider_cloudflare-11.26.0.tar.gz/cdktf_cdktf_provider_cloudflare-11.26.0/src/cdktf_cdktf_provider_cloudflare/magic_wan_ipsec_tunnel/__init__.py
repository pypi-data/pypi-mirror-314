r'''
# `cloudflare_magic_wan_ipsec_tunnel`

Refer to the Terraform Registry for docs: [`cloudflare_magic_wan_ipsec_tunnel`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel).
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


class MagicWanIpsecTunnel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.magicWanIpsecTunnel.MagicWanIpsecTunnel",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel cloudflare_magic_wan_ipsec_tunnel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cloudflare_endpoint: builtins.str,
        customer_endpoint: builtins.str,
        interface_address: builtins.str,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        allow_null_cipher: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        fqdn_id: typing.Optional[builtins.str] = None,
        health_check_direction: typing.Optional[builtins.str] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_rate: typing.Optional[builtins.str] = None,
        health_check_target: typing.Optional[builtins.str] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        hex_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        psk: typing.Optional[builtins.str] = None,
        remote_id: typing.Optional[builtins.str] = None,
        replay_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel cloudflare_magic_wan_ipsec_tunnel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cloudflare_endpoint: IP address assigned to the Cloudflare side of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#cloudflare_endpoint MagicWanIpsecTunnel#cloudflare_endpoint}
        :param customer_endpoint: IP address assigned to the customer side of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#customer_endpoint MagicWanIpsecTunnel#customer_endpoint}
        :param interface_address: 31-bit prefix (/31 in CIDR notation) supporting 2 hosts, one for each side of the tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#interface_address MagicWanIpsecTunnel#interface_address}
        :param name: Name of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#name MagicWanIpsecTunnel#name}
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#account_id MagicWanIpsecTunnel#account_id}
        :param allow_null_cipher: Specifies if this tunnel may use a null cipher (ENCR_NULL) in Phase 2. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#allow_null_cipher MagicWanIpsecTunnel#allow_null_cipher}
        :param description: An optional description of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#description MagicWanIpsecTunnel#description}
        :param fqdn_id: ``remote_id`` in the form of a fqdn. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#fqdn_id MagicWanIpsecTunnel#fqdn_id}
        :param health_check_direction: Specifies the direction for the health check. Available values: ``unidirectional``, ``bidirectional`` Default: ``unidirectional``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_direction MagicWanIpsecTunnel#health_check_direction}
        :param health_check_enabled: Specifies if ICMP tunnel health checks are enabled. Default: ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_enabled MagicWanIpsecTunnel#health_check_enabled}
        :param health_check_rate: Specifies the ICMP rate for the health check. Available values: ``low``, ``mid``, ``high`` Default: ``mid``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_rate MagicWanIpsecTunnel#health_check_rate}
        :param health_check_target: The IP address of the customer endpoint that will receive tunnel health checks. Default: ``<customer_gre_endpoint>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_target MagicWanIpsecTunnel#health_check_target}
        :param health_check_type: Specifies the ICMP echo type for the health check (``request`` or ``reply``). Available values: ``request``, ``reply`` Default: ``reply``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_type MagicWanIpsecTunnel#health_check_type}
        :param hex_id: ``remote_id`` as a hex string. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#hex_id MagicWanIpsecTunnel#hex_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#id MagicWanIpsecTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param psk: Pre shared key to be used with the IPsec tunnel. If left unset, it will be autogenerated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#psk MagicWanIpsecTunnel#psk}
        :param remote_id: ID to be used while setting up the IPsec tunnel. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#remote_id MagicWanIpsecTunnel#remote_id}
        :param replay_protection: Specifies if replay protection is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#replay_protection MagicWanIpsecTunnel#replay_protection}
        :param user_id: ``remote_id`` in the form of an email address. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#user_id MagicWanIpsecTunnel#user_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f1fe5e75a852e61f1152817182fc7f3c460e7c5413cd76a378cfde02f3182f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MagicWanIpsecTunnelConfig(
            cloudflare_endpoint=cloudflare_endpoint,
            customer_endpoint=customer_endpoint,
            interface_address=interface_address,
            name=name,
            account_id=account_id,
            allow_null_cipher=allow_null_cipher,
            description=description,
            fqdn_id=fqdn_id,
            health_check_direction=health_check_direction,
            health_check_enabled=health_check_enabled,
            health_check_rate=health_check_rate,
            health_check_target=health_check_target,
            health_check_type=health_check_type,
            hex_id=hex_id,
            id=id,
            psk=psk,
            remote_id=remote_id,
            replay_protection=replay_protection,
            user_id=user_id,
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
        '''Generates CDKTF code for importing a MagicWanIpsecTunnel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MagicWanIpsecTunnel to import.
        :param import_from_id: The id of the existing MagicWanIpsecTunnel that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MagicWanIpsecTunnel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6d93a5d2eae08a29b3f6faf432d82d8f0864b071555a85d5b5b9d1eae7e983)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAllowNullCipher")
    def reset_allow_null_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNullCipher", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFqdnId")
    def reset_fqdn_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdnId", []))

    @jsii.member(jsii_name="resetHealthCheckDirection")
    def reset_health_check_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckDirection", []))

    @jsii.member(jsii_name="resetHealthCheckEnabled")
    def reset_health_check_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckEnabled", []))

    @jsii.member(jsii_name="resetHealthCheckRate")
    def reset_health_check_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckRate", []))

    @jsii.member(jsii_name="resetHealthCheckTarget")
    def reset_health_check_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckTarget", []))

    @jsii.member(jsii_name="resetHealthCheckType")
    def reset_health_check_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckType", []))

    @jsii.member(jsii_name="resetHexId")
    def reset_hex_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHexId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPsk")
    def reset_psk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPsk", []))

    @jsii.member(jsii_name="resetRemoteId")
    def reset_remote_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteId", []))

    @jsii.member(jsii_name="resetReplayProtection")
    def reset_replay_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplayProtection", []))

    @jsii.member(jsii_name="resetUserId")
    def reset_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserId", []))

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
    @jsii.member(jsii_name="allowNullCipherInput")
    def allow_null_cipher_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNullCipherInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudflareEndpointInput")
    def cloudflare_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudflareEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="customerEndpointInput")
    def customer_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdnIdInput")
    def fqdn_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fqdnIdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckDirectionInput")
    def health_check_direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckDirectionInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabledInput")
    def health_check_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "healthCheckEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckRateInput")
    def health_check_rate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckRateInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckTargetInput")
    def health_check_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckTypeInput")
    def health_check_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hexIdInput")
    def hex_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hexIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceAddressInput")
    def interface_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pskInput")
    def psk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pskInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIdInput")
    def remote_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replayProtectionInput")
    def replay_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replayProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="userIdInput")
    def user_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866a448aaf0700a10a0c6c76bdb0144f76fbd46eb74fb043de5f2f62a2f5acf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowNullCipher")
    def allow_null_cipher(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNullCipher"))

    @allow_null_cipher.setter
    def allow_null_cipher(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df90defa4d3ee9eb286e3b6882883333b2037a241cee530668f58efeb8a8681f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNullCipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudflareEndpoint")
    def cloudflare_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudflareEndpoint"))

    @cloudflare_endpoint.setter
    def cloudflare_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0d52d3ae271abdefc733424184ed1f7673d2752613f044f4165f26305dfdffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudflareEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerEndpoint")
    def customer_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerEndpoint"))

    @customer_endpoint.setter
    def customer_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3732fb5fad013e6c715dbaa24931b2a81a1d8473cad0c611f241363dd8304bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6b112485e2bc5ff223d63eeb22853fd3ec9e54a7ffc89165769b5f6a4fcbcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fqdnId")
    def fqdn_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdnId"))

    @fqdn_id.setter
    def fqdn_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdc79f57abee4033bebc61dde063594d61e80492f35d85ae1c5cfcfafcb6c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdnId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckDirection")
    def health_check_direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckDirection"))

    @health_check_direction.setter
    def health_check_direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c31ec23ccd33c572e340a738d2e41da76717b97ac6e88e98be5398b23fb8e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckDirection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "healthCheckEnabled"))

    @health_check_enabled.setter
    def health_check_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7775e6e20ccdcedb9213482783902db7f96dcb890de6909058e9a373d5b7e7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckRate")
    def health_check_rate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckRate"))

    @health_check_rate.setter
    def health_check_rate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b82c6fe8cc3c31ab8a6f1c61fd75af71f9049692e0d4b9f53fd47974fa21db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckTarget")
    def health_check_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckTarget"))

    @health_check_target.setter
    def health_check_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1feceb5db07cde3d4975135a6180108de8470ced65125deae6b8cda958872e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckType")
    def health_check_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckType"))

    @health_check_type.setter
    def health_check_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85dc2101a1575f36d0f4ca095923a22151197dc5a057e06452cc15a955dddc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hexId")
    def hex_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hexId"))

    @hex_id.setter
    def hex_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4918934d69057e22fb4be945cec2d82e2e91ae836d942a89a6220fecb060b6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hexId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac489a9928694edac4effc8e9ddaedad8795f5da77acdaaaefa401400d54b9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceAddress")
    def interface_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceAddress"))

    @interface_address.setter
    def interface_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0201d238fe30cd014cd1b34a6380166d26155fcbc0ca78bb2fdd25872b7a7410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e5991012ada9de51f5d52cae81dcce77af9c09ad3cf72b31e102e61e398263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="psk")
    def psk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "psk"))

    @psk.setter
    def psk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29186ec283b1927eeb264de6b7676b7da548cd8d15f8361aa6c2a0c3e6b838a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "psk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteId")
    def remote_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteId"))

    @remote_id.setter
    def remote_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855dd80e6d77fb75864d1809263bda04d63fc6c26e1876dcb9faa4c47b8c8135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replayProtection")
    def replay_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replayProtection"))

    @replay_protection.setter
    def replay_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dd721dc971cf8e1e7d768951455ff3eabb7a5d782840f14b182f25212b5595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replayProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d6143e792f65ecf2041f3cf137471fb0b60f16f239d62af140ee077fd8432f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.magicWanIpsecTunnel.MagicWanIpsecTunnelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cloudflare_endpoint": "cloudflareEndpoint",
        "customer_endpoint": "customerEndpoint",
        "interface_address": "interfaceAddress",
        "name": "name",
        "account_id": "accountId",
        "allow_null_cipher": "allowNullCipher",
        "description": "description",
        "fqdn_id": "fqdnId",
        "health_check_direction": "healthCheckDirection",
        "health_check_enabled": "healthCheckEnabled",
        "health_check_rate": "healthCheckRate",
        "health_check_target": "healthCheckTarget",
        "health_check_type": "healthCheckType",
        "hex_id": "hexId",
        "id": "id",
        "psk": "psk",
        "remote_id": "remoteId",
        "replay_protection": "replayProtection",
        "user_id": "userId",
    },
)
class MagicWanIpsecTunnelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloudflare_endpoint: builtins.str,
        customer_endpoint: builtins.str,
        interface_address: builtins.str,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        allow_null_cipher: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        fqdn_id: typing.Optional[builtins.str] = None,
        health_check_direction: typing.Optional[builtins.str] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_rate: typing.Optional[builtins.str] = None,
        health_check_target: typing.Optional[builtins.str] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        hex_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        psk: typing.Optional[builtins.str] = None,
        remote_id: typing.Optional[builtins.str] = None,
        replay_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cloudflare_endpoint: IP address assigned to the Cloudflare side of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#cloudflare_endpoint MagicWanIpsecTunnel#cloudflare_endpoint}
        :param customer_endpoint: IP address assigned to the customer side of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#customer_endpoint MagicWanIpsecTunnel#customer_endpoint}
        :param interface_address: 31-bit prefix (/31 in CIDR notation) supporting 2 hosts, one for each side of the tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#interface_address MagicWanIpsecTunnel#interface_address}
        :param name: Name of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#name MagicWanIpsecTunnel#name}
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#account_id MagicWanIpsecTunnel#account_id}
        :param allow_null_cipher: Specifies if this tunnel may use a null cipher (ENCR_NULL) in Phase 2. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#allow_null_cipher MagicWanIpsecTunnel#allow_null_cipher}
        :param description: An optional description of the IPsec tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#description MagicWanIpsecTunnel#description}
        :param fqdn_id: ``remote_id`` in the form of a fqdn. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#fqdn_id MagicWanIpsecTunnel#fqdn_id}
        :param health_check_direction: Specifies the direction for the health check. Available values: ``unidirectional``, ``bidirectional`` Default: ``unidirectional``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_direction MagicWanIpsecTunnel#health_check_direction}
        :param health_check_enabled: Specifies if ICMP tunnel health checks are enabled. Default: ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_enabled MagicWanIpsecTunnel#health_check_enabled}
        :param health_check_rate: Specifies the ICMP rate for the health check. Available values: ``low``, ``mid``, ``high`` Default: ``mid``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_rate MagicWanIpsecTunnel#health_check_rate}
        :param health_check_target: The IP address of the customer endpoint that will receive tunnel health checks. Default: ``<customer_gre_endpoint>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_target MagicWanIpsecTunnel#health_check_target}
        :param health_check_type: Specifies the ICMP echo type for the health check (``request`` or ``reply``). Available values: ``request``, ``reply`` Default: ``reply``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_type MagicWanIpsecTunnel#health_check_type}
        :param hex_id: ``remote_id`` as a hex string. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#hex_id MagicWanIpsecTunnel#hex_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#id MagicWanIpsecTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param psk: Pre shared key to be used with the IPsec tunnel. If left unset, it will be autogenerated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#psk MagicWanIpsecTunnel#psk}
        :param remote_id: ID to be used while setting up the IPsec tunnel. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#remote_id MagicWanIpsecTunnel#remote_id}
        :param replay_protection: Specifies if replay protection is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#replay_protection MagicWanIpsecTunnel#replay_protection}
        :param user_id: ``remote_id`` in the form of an email address. This value is generated by cloudflare. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#user_id MagicWanIpsecTunnel#user_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e2d1f9b38e27a904863c5ae9a55e291e01f2b09c4186662501f6e0cb52ced4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cloudflare_endpoint", value=cloudflare_endpoint, expected_type=type_hints["cloudflare_endpoint"])
            check_type(argname="argument customer_endpoint", value=customer_endpoint, expected_type=type_hints["customer_endpoint"])
            check_type(argname="argument interface_address", value=interface_address, expected_type=type_hints["interface_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument allow_null_cipher", value=allow_null_cipher, expected_type=type_hints["allow_null_cipher"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fqdn_id", value=fqdn_id, expected_type=type_hints["fqdn_id"])
            check_type(argname="argument health_check_direction", value=health_check_direction, expected_type=type_hints["health_check_direction"])
            check_type(argname="argument health_check_enabled", value=health_check_enabled, expected_type=type_hints["health_check_enabled"])
            check_type(argname="argument health_check_rate", value=health_check_rate, expected_type=type_hints["health_check_rate"])
            check_type(argname="argument health_check_target", value=health_check_target, expected_type=type_hints["health_check_target"])
            check_type(argname="argument health_check_type", value=health_check_type, expected_type=type_hints["health_check_type"])
            check_type(argname="argument hex_id", value=hex_id, expected_type=type_hints["hex_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument psk", value=psk, expected_type=type_hints["psk"])
            check_type(argname="argument remote_id", value=remote_id, expected_type=type_hints["remote_id"])
            check_type(argname="argument replay_protection", value=replay_protection, expected_type=type_hints["replay_protection"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudflare_endpoint": cloudflare_endpoint,
            "customer_endpoint": customer_endpoint,
            "interface_address": interface_address,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if allow_null_cipher is not None:
            self._values["allow_null_cipher"] = allow_null_cipher
        if description is not None:
            self._values["description"] = description
        if fqdn_id is not None:
            self._values["fqdn_id"] = fqdn_id
        if health_check_direction is not None:
            self._values["health_check_direction"] = health_check_direction
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_rate is not None:
            self._values["health_check_rate"] = health_check_rate
        if health_check_target is not None:
            self._values["health_check_target"] = health_check_target
        if health_check_type is not None:
            self._values["health_check_type"] = health_check_type
        if hex_id is not None:
            self._values["hex_id"] = hex_id
        if id is not None:
            self._values["id"] = id
        if psk is not None:
            self._values["psk"] = psk
        if remote_id is not None:
            self._values["remote_id"] = remote_id
        if replay_protection is not None:
            self._values["replay_protection"] = replay_protection
        if user_id is not None:
            self._values["user_id"] = user_id

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
    def cloudflare_endpoint(self) -> builtins.str:
        '''IP address assigned to the Cloudflare side of the IPsec tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#cloudflare_endpoint MagicWanIpsecTunnel#cloudflare_endpoint}
        '''
        result = self._values.get("cloudflare_endpoint")
        assert result is not None, "Required property 'cloudflare_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_endpoint(self) -> builtins.str:
        '''IP address assigned to the customer side of the IPsec tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#customer_endpoint MagicWanIpsecTunnel#customer_endpoint}
        '''
        result = self._values.get("customer_endpoint")
        assert result is not None, "Required property 'customer_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interface_address(self) -> builtins.str:
        '''31-bit prefix (/31 in CIDR notation) supporting 2 hosts, one for each side of the tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#interface_address MagicWanIpsecTunnel#interface_address}
        '''
        result = self._values.get("interface_address")
        assert result is not None, "Required property 'interface_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the IPsec tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#name MagicWanIpsecTunnel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#account_id MagicWanIpsecTunnel#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_null_cipher(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if this tunnel may use a null cipher (ENCR_NULL) in Phase 2. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#allow_null_cipher MagicWanIpsecTunnel#allow_null_cipher}
        '''
        result = self._values.get("allow_null_cipher")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the IPsec tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#description MagicWanIpsecTunnel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fqdn_id(self) -> typing.Optional[builtins.str]:
        '''``remote_id`` in the form of a fqdn. This value is generated by cloudflare.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#fqdn_id MagicWanIpsecTunnel#fqdn_id}
        '''
        result = self._values.get("fqdn_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_direction(self) -> typing.Optional[builtins.str]:
        '''Specifies the direction for the health check. Available values: ``unidirectional``, ``bidirectional`` Default: ``unidirectional``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_direction MagicWanIpsecTunnel#health_check_direction}
        '''
        result = self._values.get("health_check_direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if ICMP tunnel health checks are enabled. Default: ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_enabled MagicWanIpsecTunnel#health_check_enabled}
        '''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def health_check_rate(self) -> typing.Optional[builtins.str]:
        '''Specifies the ICMP rate for the health check. Available values: ``low``, ``mid``, ``high`` Default: ``mid``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_rate MagicWanIpsecTunnel#health_check_rate}
        '''
        result = self._values.get("health_check_rate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_target(self) -> typing.Optional[builtins.str]:
        '''The IP address of the customer endpoint that will receive tunnel health checks. Default: ``<customer_gre_endpoint>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_target MagicWanIpsecTunnel#health_check_target}
        '''
        result = self._values.get("health_check_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the ICMP echo type for the health check (``request`` or ``reply``). Available values: ``request``, ``reply`` Default: ``reply``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#health_check_type MagicWanIpsecTunnel#health_check_type}
        '''
        result = self._values.get("health_check_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hex_id(self) -> typing.Optional[builtins.str]:
        '''``remote_id`` as a hex string. This value is generated by cloudflare.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#hex_id MagicWanIpsecTunnel#hex_id}
        '''
        result = self._values.get("hex_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#id MagicWanIpsecTunnel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psk(self) -> typing.Optional[builtins.str]:
        '''Pre shared key to be used with the IPsec tunnel. If left unset, it will be autogenerated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#psk MagicWanIpsecTunnel#psk}
        '''
        result = self._values.get("psk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_id(self) -> typing.Optional[builtins.str]:
        '''ID to be used while setting up the IPsec tunnel. This value is generated by cloudflare.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#remote_id MagicWanIpsecTunnel#remote_id}
        '''
        result = self._values.get("remote_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replay_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if replay protection is enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#replay_protection MagicWanIpsecTunnel#replay_protection}
        '''
        result = self._values.get("replay_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_id(self) -> typing.Optional[builtins.str]:
        '''``remote_id`` in the form of an email address. This value is generated by cloudflare.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/magic_wan_ipsec_tunnel#user_id MagicWanIpsecTunnel#user_id}
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MagicWanIpsecTunnelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MagicWanIpsecTunnel",
    "MagicWanIpsecTunnelConfig",
]

publication.publish()

def _typecheckingstub__07f1fe5e75a852e61f1152817182fc7f3c460e7c5413cd76a378cfde02f3182f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cloudflare_endpoint: builtins.str,
    customer_endpoint: builtins.str,
    interface_address: builtins.str,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    allow_null_cipher: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    fqdn_id: typing.Optional[builtins.str] = None,
    health_check_direction: typing.Optional[builtins.str] = None,
    health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_check_rate: typing.Optional[builtins.str] = None,
    health_check_target: typing.Optional[builtins.str] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    hex_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    psk: typing.Optional[builtins.str] = None,
    remote_id: typing.Optional[builtins.str] = None,
    replay_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ee6d93a5d2eae08a29b3f6faf432d82d8f0864b071555a85d5b5b9d1eae7e983(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866a448aaf0700a10a0c6c76bdb0144f76fbd46eb74fb043de5f2f62a2f5acf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df90defa4d3ee9eb286e3b6882883333b2037a241cee530668f58efeb8a8681f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d52d3ae271abdefc733424184ed1f7673d2752613f044f4165f26305dfdffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3732fb5fad013e6c715dbaa24931b2a81a1d8473cad0c611f241363dd8304bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6b112485e2bc5ff223d63eeb22853fd3ec9e54a7ffc89165769b5f6a4fcbcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdc79f57abee4033bebc61dde063594d61e80492f35d85ae1c5cfcfafcb6c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c31ec23ccd33c572e340a738d2e41da76717b97ac6e88e98be5398b23fb8e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7775e6e20ccdcedb9213482783902db7f96dcb890de6909058e9a373d5b7e7c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b82c6fe8cc3c31ab8a6f1c61fd75af71f9049692e0d4b9f53fd47974fa21db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1feceb5db07cde3d4975135a6180108de8470ced65125deae6b8cda958872e45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85dc2101a1575f36d0f4ca095923a22151197dc5a057e06452cc15a955dddc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4918934d69057e22fb4be945cec2d82e2e91ae836d942a89a6220fecb060b6ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac489a9928694edac4effc8e9ddaedad8795f5da77acdaaaefa401400d54b9f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0201d238fe30cd014cd1b34a6380166d26155fcbc0ca78bb2fdd25872b7a7410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e5991012ada9de51f5d52cae81dcce77af9c09ad3cf72b31e102e61e398263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29186ec283b1927eeb264de6b7676b7da548cd8d15f8361aa6c2a0c3e6b838a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855dd80e6d77fb75864d1809263bda04d63fc6c26e1876dcb9faa4c47b8c8135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dd721dc971cf8e1e7d768951455ff3eabb7a5d782840f14b182f25212b5595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d6143e792f65ecf2041f3cf137471fb0b60f16f239d62af140ee077fd8432f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e2d1f9b38e27a904863c5ae9a55e291e01f2b09c4186662501f6e0cb52ced4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudflare_endpoint: builtins.str,
    customer_endpoint: builtins.str,
    interface_address: builtins.str,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    allow_null_cipher: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    fqdn_id: typing.Optional[builtins.str] = None,
    health_check_direction: typing.Optional[builtins.str] = None,
    health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_check_rate: typing.Optional[builtins.str] = None,
    health_check_target: typing.Optional[builtins.str] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    hex_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    psk: typing.Optional[builtins.str] = None,
    remote_id: typing.Optional[builtins.str] = None,
    replay_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
