r'''
# `cloudflare_zero_trust_tunnel_cloudflared_config`

Refer to the Terraform Registry for docs: [`cloudflare_zero_trust_tunnel_cloudflared_config`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config).
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


class ZeroTrustTunnelCloudflaredConfigA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigA",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config cloudflare_zero_trust_tunnel_cloudflared_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        config: typing.Union["ZeroTrustTunnelCloudflaredConfigConfig", typing.Dict[builtins.str, typing.Any]],
        tunnel_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config cloudflare_zero_trust_tunnel_cloudflared_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#account_id ZeroTrustTunnelCloudflaredConfigA#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#config ZeroTrustTunnelCloudflaredConfigA#config}
        :param tunnel_id: Identifier of the Tunnel to target for this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tunnel_id ZeroTrustTunnelCloudflaredConfigA#tunnel_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#id ZeroTrustTunnelCloudflaredConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c3e700edd3e4bf5ead6f056e28348ae350d0c39ce57e46a2c6c9127b5877e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = ZeroTrustTunnelCloudflaredConfigAConfig(
            account_id=account_id,
            config=config,
            tunnel_id=tunnel_id,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ZeroTrustTunnelCloudflaredConfigA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ZeroTrustTunnelCloudflaredConfigA to import.
        :param import_from_id: The id of the existing ZeroTrustTunnelCloudflaredConfigA that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ZeroTrustTunnelCloudflaredConfigA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26886a3195522bd58df26c7e41578c5a4b7c8ef2a01aabc8c8b2fc6d581237ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigIngressRule", typing.Dict[builtins.str, typing.Any]]]],
        origin_request: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigOriginRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        warp_routing: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress_rule: ingress_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ingress_rule ZeroTrustTunnelCloudflaredConfigA#ingress_rule}
        :param origin_request: origin_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_request ZeroTrustTunnelCloudflaredConfigA#origin_request}
        :param warp_routing: warp_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#warp_routing ZeroTrustTunnelCloudflaredConfigA#warp_routing}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfig(
            ingress_rule=ingress_rule,
            origin_request=origin_request,
            warp_routing=warp_routing,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "ZeroTrustTunnelCloudflaredConfigConfigOutputReference":
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfigOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfig"]:
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfig"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelIdInput")
    def tunnel_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063215e6de559dfdb173577ef39a73e59c8da14db0dd681f9214f49fade47a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bede05880359079fc7529b2e51e3d16d3d021e372e035a58fa44e1dca1436b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tunnelId")
    def tunnel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelId"))

    @tunnel_id.setter
    def tunnel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95fc4ac1123f5860744e72d1b82de65fe429be4b727ca3fef5e54ece11f1142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigAConfig",
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
        "config": "config",
        "tunnel_id": "tunnelId",
        "id": "id",
    },
)
class ZeroTrustTunnelCloudflaredConfigAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Union["ZeroTrustTunnelCloudflaredConfigConfig", typing.Dict[builtins.str, typing.Any]],
        tunnel_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#account_id ZeroTrustTunnelCloudflaredConfigA#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#config ZeroTrustTunnelCloudflaredConfigA#config}
        :param tunnel_id: Identifier of the Tunnel to target for this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tunnel_id ZeroTrustTunnelCloudflaredConfigA#tunnel_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#id ZeroTrustTunnelCloudflaredConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = ZeroTrustTunnelCloudflaredConfigConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae33dabb83c6599c16c97f82f27e96662097f36b213d22e119d6e7c7e366024)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument tunnel_id", value=tunnel_id, expected_type=type_hints["tunnel_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "config": config,
            "tunnel_id": tunnel_id,
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
        if id is not None:
            self._values["id"] = id

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#account_id ZeroTrustTunnelCloudflaredConfigA#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "ZeroTrustTunnelCloudflaredConfigConfig":
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#config ZeroTrustTunnelCloudflaredConfigA#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfig", result)

    @builtins.property
    def tunnel_id(self) -> builtins.str:
        '''Identifier of the Tunnel to target for this configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tunnel_id ZeroTrustTunnelCloudflaredConfigA#tunnel_id}
        '''
        result = self._values.get("tunnel_id")
        assert result is not None, "Required property 'tunnel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#id ZeroTrustTunnelCloudflaredConfigA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_rule": "ingressRule",
        "origin_request": "originRequest",
        "warp_routing": "warpRouting",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfig:
    def __init__(
        self,
        *,
        ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigIngressRule", typing.Dict[builtins.str, typing.Any]]]],
        origin_request: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigOriginRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        warp_routing: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress_rule: ingress_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ingress_rule ZeroTrustTunnelCloudflaredConfigA#ingress_rule}
        :param origin_request: origin_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_request ZeroTrustTunnelCloudflaredConfigA#origin_request}
        :param warp_routing: warp_routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#warp_routing ZeroTrustTunnelCloudflaredConfigA#warp_routing}
        '''
        if isinstance(origin_request, dict):
            origin_request = ZeroTrustTunnelCloudflaredConfigConfigOriginRequest(**origin_request)
        if isinstance(warp_routing, dict):
            warp_routing = ZeroTrustTunnelCloudflaredConfigConfigWarpRouting(**warp_routing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecc74d84626090dba3f174efaac8078277aacbf27564f772b864127e59e4cd7)
            check_type(argname="argument ingress_rule", value=ingress_rule, expected_type=type_hints["ingress_rule"])
            check_type(argname="argument origin_request", value=origin_request, expected_type=type_hints["origin_request"])
            check_type(argname="argument warp_routing", value=warp_routing, expected_type=type_hints["warp_routing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingress_rule": ingress_rule,
        }
        if origin_request is not None:
            self._values["origin_request"] = origin_request
        if warp_routing is not None:
            self._values["warp_routing"] = warp_routing

    @builtins.property
    def ingress_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigIngressRule"]]:
        '''ingress_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ingress_rule ZeroTrustTunnelCloudflaredConfigA#ingress_rule}
        '''
        result = self._values.get("ingress_rule")
        assert result is not None, "Required property 'ingress_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigIngressRule"]], result)

    @builtins.property
    def origin_request(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigOriginRequest"]:
        '''origin_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_request ZeroTrustTunnelCloudflaredConfigA#origin_request}
        '''
        result = self._values.get("origin_request")
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigOriginRequest"], result)

    @builtins.property
    def warp_routing(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting"]:
        '''warp_routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#warp_routing ZeroTrustTunnelCloudflaredConfigA#warp_routing}
        '''
        result = self._values.get("warp_routing")
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRule",
    jsii_struct_bases=[],
    name_mapping={
        "service": "service",
        "hostname": "hostname",
        "origin_request": "originRequest",
        "path": "path",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfigIngressRule:
    def __init__(
        self,
        *,
        service: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
        origin_request: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Name of the service to which the request will be sent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#service ZeroTrustTunnelCloudflaredConfigA#service}
        :param hostname: Hostname to match the incoming request with. If the hostname matches, the request will be sent to the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#hostname ZeroTrustTunnelCloudflaredConfigA#hostname}
        :param origin_request: origin_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_request ZeroTrustTunnelCloudflaredConfigA#origin_request}
        :param path: Path of the incoming request. If the path matches, the request will be sent to the local service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#path ZeroTrustTunnelCloudflaredConfigA#path}
        '''
        if isinstance(origin_request, dict):
            origin_request = ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest(**origin_request)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a4e201c4a4ea6a55411d1d57b4c73797a780fa92231ade5c588b010876652f)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument origin_request", value=origin_request, expected_type=type_hints["origin_request"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if origin_request is not None:
            self._values["origin_request"] = origin_request
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def service(self) -> builtins.str:
        '''Name of the service to which the request will be sent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#service ZeroTrustTunnelCloudflaredConfigA#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname to match the incoming request with. If the hostname matches, the request will be sent to the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#hostname ZeroTrustTunnelCloudflaredConfigA#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_request(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest"]:
        '''origin_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_request ZeroTrustTunnelCloudflaredConfigA#origin_request}
        '''
        result = self._values.get("origin_request")
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path of the incoming request. If the path matches, the request will be sent to the local service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#path ZeroTrustTunnelCloudflaredConfigA#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigIngressRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4057401fd474ba55c8e647a6e34cddd8272b77093283ba0d231a47525aefb3d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8281f5c88561a73d2e5b074c1bda6dbc1efbcc1517896971239f7224d816e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0413336206bc9b53cf81a02ff19efd897a5853aac2fd838a2215217bd93167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78fb8afe714a3db09615a0c4ff1883eb8dac7302cb3094041d37930ffd10610d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__520fd98ca2092a08ee6913db42e01d3b78a317db7192198aa8609b485e9cf3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cf1618980b06838d4c7ebab65bd07d5199f890d13959efb0316621b09a9795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "bastion_mode": "bastionMode",
        "ca_pool": "caPool",
        "connect_timeout": "connectTimeout",
        "disable_chunked_encoding": "disableChunkedEncoding",
        "http2_origin": "http2Origin",
        "http_host_header": "httpHostHeader",
        "ip_rules": "ipRules",
        "keep_alive_connections": "keepAliveConnections",
        "keep_alive_timeout": "keepAliveTimeout",
        "no_happy_eyeballs": "noHappyEyeballs",
        "no_tls_verify": "noTlsVerify",
        "origin_server_name": "originServerName",
        "proxy_address": "proxyAddress",
        "proxy_port": "proxyPort",
        "proxy_type": "proxyType",
        "tcp_keep_alive": "tcpKeepAlive",
        "tls_timeout": "tlsTimeout",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest:
    def __init__(
        self,
        *,
        access: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        :param http2_origin: Enables HTTP/2 support for the origin connection. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        if isinstance(access, dict):
            access = ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess(**access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fafe5f372e164d0a5a19b25ff85fd89564bbdca36555e07b7ea4f5efe029d54)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument bastion_mode", value=bastion_mode, expected_type=type_hints["bastion_mode"])
            check_type(argname="argument ca_pool", value=ca_pool, expected_type=type_hints["ca_pool"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument disable_chunked_encoding", value=disable_chunked_encoding, expected_type=type_hints["disable_chunked_encoding"])
            check_type(argname="argument http2_origin", value=http2_origin, expected_type=type_hints["http2_origin"])
            check_type(argname="argument http_host_header", value=http_host_header, expected_type=type_hints["http_host_header"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument keep_alive_connections", value=keep_alive_connections, expected_type=type_hints["keep_alive_connections"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument no_happy_eyeballs", value=no_happy_eyeballs, expected_type=type_hints["no_happy_eyeballs"])
            check_type(argname="argument no_tls_verify", value=no_tls_verify, expected_type=type_hints["no_tls_verify"])
            check_type(argname="argument origin_server_name", value=origin_server_name, expected_type=type_hints["origin_server_name"])
            check_type(argname="argument proxy_address", value=proxy_address, expected_type=type_hints["proxy_address"])
            check_type(argname="argument proxy_port", value=proxy_port, expected_type=type_hints["proxy_port"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
            check_type(argname="argument tcp_keep_alive", value=tcp_keep_alive, expected_type=type_hints["tcp_keep_alive"])
            check_type(argname="argument tls_timeout", value=tls_timeout, expected_type=type_hints["tls_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access is not None:
            self._values["access"] = access
        if bastion_mode is not None:
            self._values["bastion_mode"] = bastion_mode
        if ca_pool is not None:
            self._values["ca_pool"] = ca_pool
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if disable_chunked_encoding is not None:
            self._values["disable_chunked_encoding"] = disable_chunked_encoding
        if http2_origin is not None:
            self._values["http2_origin"] = http2_origin
        if http_host_header is not None:
            self._values["http_host_header"] = http_host_header
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if keep_alive_connections is not None:
            self._values["keep_alive_connections"] = keep_alive_connections
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if no_happy_eyeballs is not None:
            self._values["no_happy_eyeballs"] = no_happy_eyeballs
        if no_tls_verify is not None:
            self._values["no_tls_verify"] = no_tls_verify
        if origin_server_name is not None:
            self._values["origin_server_name"] = origin_server_name
        if proxy_address is not None:
            self._values["proxy_address"] = proxy_address
        if proxy_port is not None:
            self._values["proxy_port"] = proxy_port
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tcp_keep_alive is not None:
            self._values["tcp_keep_alive"] = tcp_keep_alive
        if tls_timeout is not None:
            self._values["tls_timeout"] = tls_timeout

    @builtins.property
    def access(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess"]:
        '''access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess"], result)

    @builtins.property
    def bastion_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs as jump host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        '''
        result = self._values.get("bastion_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ca_pool(self) -> typing.Optional[builtins.str]:
        '''Path to the certificate authority (CA) for the certificate of your origin.

        This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        '''
        result = self._values.get("ca_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for establishing a new TCP connection to your origin server.

        This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_chunked_encoding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        '''
        result = self._values.get("disable_chunked_encoding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http2_origin(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables HTTP/2 support for the origin connection. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        '''
        result = self._values.get("http2_origin")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_host_header(self) -> typing.Optional[builtins.str]:
        '''Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        '''
        result = self._values.get("http_host_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules"]]]:
        '''ip_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        '''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules"]]], result)

    @builtins.property
    def keep_alive_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle keepalive connections between Tunnel and your origin.

        This does not restrict the total number of concurrent connections. Defaults to ``100``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        '''
        result = self._values.get("keep_alive_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        '''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_happy_eyeballs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        '''
        result = self._values.get("no_happy_eyeballs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_tls_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables TLS verification of the certificate presented by your origin.

        Will allow any certificate from the origin to be accepted. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        '''
        result = self._values.get("no_tls_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def origin_server_name(self) -> typing.Optional[builtins.str]:
        '''Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        '''
        result = self._values.get("origin_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_address(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen address for that proxy. Defaults to ``127.0.0.1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        '''
        result = self._values.get("proxy_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_port(self) -> typing.Optional[jsii.Number]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        '''
        result = self._values.get("proxy_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tcp_keep_alive(self) -> typing.Optional[builtins.str]:
        '''The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server.

        Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        '''
        result = self._values.get("tcp_keep_alive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server.

        Defaults to ``10s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        result = self._values.get("tls_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess",
    jsii_struct_bases=[],
    name_mapping={
        "aud_tag": "audTag",
        "required": "required",
        "team_name": "teamName",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess:
    def __init__(
        self,
        *,
        aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aud_tag: Audience tags of the access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        :param required: Whether the access rule is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        :param team_name: Name of the team to which the access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda61023c603696303ddc0e815a2bdc21bff847f9f1405268a9bd111bc00b7c9)
            check_type(argname="argument aud_tag", value=aud_tag, expected_type=type_hints["aud_tag"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument team_name", value=team_name, expected_type=type_hints["team_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aud_tag is not None:
            self._values["aud_tag"] = aud_tag
        if required is not None:
            self._values["required"] = required
        if team_name is not None:
            self._values["team_name"] = team_name

    @builtins.property
    def aud_tag(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Audience tags of the access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        '''
        result = self._values.get("aud_tag")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the access rule is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def team_name(self) -> typing.Optional[builtins.str]:
        '''Name of the team to which the access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        result = self._values.get("team_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a2554b06be461332e98aa4f418f2f368f8894567b4b9e6d1b0d5ed2793612c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudTag")
    def reset_aud_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudTag", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetTeamName")
    def reset_team_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeamName", []))

    @builtins.property
    @jsii.member(jsii_name="audTagInput")
    def aud_tag_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "audTagInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="teamNameInput")
    def team_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="audTag")
    def aud_tag(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "audTag"))

    @aud_tag.setter
    def aud_tag(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8983b753f92000beeaf050937ee0aa31ead2d3ccabc77c171126a20c9f03c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4fc95c7a4e57ffcb7bcadb906713ee93c80bafc1c131d94a453da0388fb46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teamName")
    def team_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamName"))

    @team_name.setter
    def team_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35af9aea13fa86cae7b1d7785e2cbd1879cfff2c2b54db365e67cf071d6543a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529e111ffde8ee8194c7e0ea78a35d971fb2bb74a310a36cb34071381b424b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules",
    jsii_struct_bases=[],
    name_mapping={"allow": "allow", "ports": "ports", "prefix": "prefix"},
)
class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: Whether to allow the IP prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#allow ZeroTrustTunnelCloudflaredConfigA#allow}
        :param ports: Ports to use within the IP rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ports ZeroTrustTunnelCloudflaredConfigA#ports}
        :param prefix: IP rule prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#prefix ZeroTrustTunnelCloudflaredConfigA#prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d235775b2b5684e6cc2dceeca99f8e0a8655403cb53ce7124bfc6b17815149db)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if ports is not None:
            self._values["ports"] = ports
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def allow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow the IP prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#allow ZeroTrustTunnelCloudflaredConfigA#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Ports to use within the IP rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ports ZeroTrustTunnelCloudflaredConfigA#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''IP rule prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#prefix ZeroTrustTunnelCloudflaredConfigA#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f3c10a26f40d13210388a346fdf9239bb693bb3ef848e394f74b009d513fa7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07bbd8591038edf4d26bcea67f86ab85b691cae167463406c7709a642d35648a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5281d86fb2722983bec40efd52487e12f2acf191867e792edecb7e0ddc32c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8917102a45b4cecdd8adc31bc358a44853bda63799422731bf56317fabc0cd93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e4f07f7e50473550a7c9b018dcfe816a7a303dfc9fd615fc7f93dc4f3498359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4462269b6903779a499f7d09b131646cb5237c67b3fecf8bf119132d64cbf11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d281787f528c6b73260e604e3577db686e5a7c34e1538a6d496dd36ee1387409)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allow"))

    @allow.setter
    def allow(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bb2510b90552efcc5527835abe24d5008726e19ae8c7ebddc80c7a21eacbd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9302b09728de6ca66381ddd53148b1553fcda7309f7a67aff060f176eddec98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173193cda90876e01697cbd4cab180a4a87cb1bd4d55df06c8f87c997248b62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5caeab655464fe3bf58bbe286fc28ef956e6819186a770c79a9da9adbecbfe91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff517f14c7f42bdd799d716367844edd333ee264d787c2ebb44bb88dc658b8a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccess")
    def put_access(
        self,
        *,
        aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aud_tag: Audience tags of the access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        :param required: Whether the access rule is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        :param team_name: Name of the team to which the access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess(
            aud_tag=aud_tag, required=required, team_name=team_name
        )

        return typing.cast(None, jsii.invoke(self, "putAccess", [value]))

    @jsii.member(jsii_name="putIpRules")
    def put_ip_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bd9ac9c18acf700a7da5d18ce4343627404cd4e46d9a7146b52673d8e9a9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRules", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetBastionMode")
    def reset_bastion_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBastionMode", []))

    @jsii.member(jsii_name="resetCaPool")
    def reset_ca_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaPool", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetDisableChunkedEncoding")
    def reset_disable_chunked_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableChunkedEncoding", []))

    @jsii.member(jsii_name="resetHttp2Origin")
    def reset_http2_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Origin", []))

    @jsii.member(jsii_name="resetHttpHostHeader")
    def reset_http_host_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHostHeader", []))

    @jsii.member(jsii_name="resetIpRules")
    def reset_ip_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRules", []))

    @jsii.member(jsii_name="resetKeepAliveConnections")
    def reset_keep_alive_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveConnections", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetNoHappyEyeballs")
    def reset_no_happy_eyeballs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoHappyEyeballs", []))

    @jsii.member(jsii_name="resetNoTlsVerify")
    def reset_no_tls_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoTlsVerify", []))

    @jsii.member(jsii_name="resetOriginServerName")
    def reset_origin_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginServerName", []))

    @jsii.member(jsii_name="resetProxyAddress")
    def reset_proxy_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyAddress", []))

    @jsii.member(jsii_name="resetProxyPort")
    def reset_proxy_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyPort", []))

    @jsii.member(jsii_name="resetProxyType")
    def reset_proxy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyType", []))

    @jsii.member(jsii_name="resetTcpKeepAlive")
    def reset_tcp_keep_alive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpKeepAlive", []))

    @jsii.member(jsii_name="resetTlsTimeout")
    def reset_tls_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccessOutputReference:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccessOutputReference, jsii.get(self, "access"))

    @builtins.property
    @jsii.member(jsii_name="ipRules")
    def ip_rules(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesList:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesList, jsii.get(self, "ipRules"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="bastionModeInput")
    def bastion_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bastionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="caPoolInput")
    def ca_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncodingInput")
    def disable_chunked_encoding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableChunkedEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="http2OriginInput")
    def http2_origin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2OriginInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHostHeaderInput")
    def http_host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpHostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRulesInput")
    def ip_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]], jsii.get(self, "ipRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnectionsInput")
    def keep_alive_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballsInput")
    def no_happy_eyeballs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noHappyEyeballsInput"))

    @builtins.property
    @jsii.member(jsii_name="noTlsVerifyInput")
    def no_tls_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noTlsVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="originServerNameInput")
    def origin_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originServerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddressInput")
    def proxy_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyPortInput")
    def proxy_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "proxyPortInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyTypeInput")
    def proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAliveInput")
    def tcp_keep_alive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tcpKeepAliveInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsTimeoutInput")
    def tls_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="bastionMode")
    def bastion_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bastionMode"))

    @bastion_mode.setter
    def bastion_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48923fc3ddef9f49e85c14415e40d20499141c82fe3d1dd9b87a0ac47cf924f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bastionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caPool")
    def ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPool"))

    @ca_pool.setter
    def ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d703ee5cd2c8672e4f188f8fe912d87f533b31da634d03d38b51c19d697522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3e5d7817fd95f568fcf1fb5639d29c8f666ad9e10abee9c058fbe54a647c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncoding")
    def disable_chunked_encoding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableChunkedEncoding"))

    @disable_chunked_encoding.setter
    def disable_chunked_encoding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bc167b24f6ac416a0849a56a604816f3d2299e9d19b3d42dc6b210d345d501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableChunkedEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="http2Origin")
    def http2_origin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Origin"))

    @http2_origin.setter
    def http2_origin(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2299036b1d042be8ca3bd100a967699cdd11e3569cfa78446ba590285ebed1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHostHeader")
    def http_host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpHostHeader"))

    @http_host_header.setter
    def http_host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05d7869024b1c7614b7c7fb1261badf662db2cbdf6f2848cb90f8807a79ba85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHostHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnections")
    def keep_alive_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveConnections"))

    @keep_alive_connections.setter
    def keep_alive_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730564f629b4c141b2d675ecef9d446a29ba87ef5f4b9736b2be1e9a2f25676e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d35460d731cd259665c23114023246b8ef0e47329f3730738d3d4f0e709877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballs")
    def no_happy_eyeballs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noHappyEyeballs"))

    @no_happy_eyeballs.setter
    def no_happy_eyeballs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebeb7476cd43ee4e21cac202871fa5964433ceb325c24e793ecadb17c1127c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHappyEyeballs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noTlsVerify")
    def no_tls_verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noTlsVerify"))

    @no_tls_verify.setter
    def no_tls_verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef646ed0e45c708ee1676ad488e1f4acc5ae2675826845ad7cae673830b91eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noTlsVerify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originServerName")
    def origin_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originServerName"))

    @origin_server_name.setter
    def origin_server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da22d6267a2da2206a396625ba33f242019921807d1c4b1b9f87590bc408580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originServerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyAddress")
    def proxy_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyAddress"))

    @proxy_address.setter
    def proxy_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e37a105da46732cf233b2cbfb9de43e42668a8641677907dc4120751849fb93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyPort")
    def proxy_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "proxyPort"))

    @proxy_port.setter
    def proxy_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de8c9712ee2ace588f8919a7e00e6c89a295b7018ae7d607da29c2cb2e0bf4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyType")
    def proxy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyType"))

    @proxy_type.setter
    def proxy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471a9c6f83a53c54882522d589ac5a56b002a13aafa292c587acc4f3e7849630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAlive")
    def tcp_keep_alive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tcpKeepAlive"))

    @tcp_keep_alive.setter
    def tcp_keep_alive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ac8f8b909994a46d658c5110b0f90779de875755de36fdcdc6d9a854c0cd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsTimeout")
    def tls_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsTimeout"))

    @tls_timeout.setter
    def tls_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced73ad0d0e21799840ff5b8d47e38bbb4b73325b4ace6815709b5f2f7b6a963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda91d55246e67bacd8ac966d30183a69a04fc3d6d2fc9eb9967f9cdac4085b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f46bedf8d7966cd76d53c9c2c13c957cda69327b17ee69d6a57f29bbea2cf489)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOriginRequest")
    def put_origin_request(
        self,
        *,
        access: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess, typing.Dict[builtins.str, typing.Any]]] = None,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        :param http2_origin: Enables HTTP/2 support for the origin connection. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest(
            access=access,
            bastion_mode=bastion_mode,
            ca_pool=ca_pool,
            connect_timeout=connect_timeout,
            disable_chunked_encoding=disable_chunked_encoding,
            http2_origin=http2_origin,
            http_host_header=http_host_header,
            ip_rules=ip_rules,
            keep_alive_connections=keep_alive_connections,
            keep_alive_timeout=keep_alive_timeout,
            no_happy_eyeballs=no_happy_eyeballs,
            no_tls_verify=no_tls_verify,
            origin_server_name=origin_server_name,
            proxy_address=proxy_address,
            proxy_port=proxy_port,
            proxy_type=proxy_type,
            tcp_keep_alive=tcp_keep_alive,
            tls_timeout=tls_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putOriginRequest", [value]))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetOriginRequest")
    def reset_origin_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequest", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="originRequest")
    def origin_request(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestOutputReference:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestOutputReference, jsii.get(self, "originRequest"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="originRequestInput")
    def origin_request_input(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest], jsii.get(self, "originRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd4678bb3495ed12b3d5b3c1bf6a8a571c871150deb291c4611629067eeb4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd9c3ad847b0d9f5b7346c76011484fbd7cf06c952cf59cd1636a434ac0afd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3b3d685679d4993f6dc77868598c43bf0634c847ebc73b4cb0a923a4f79268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d2ccf7ee2879a9fa849d0185dfbf1def3eca7f065b267912dd02ca90dbb1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequest",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "bastion_mode": "bastionMode",
        "ca_pool": "caPool",
        "connect_timeout": "connectTimeout",
        "disable_chunked_encoding": "disableChunkedEncoding",
        "http2_origin": "http2Origin",
        "http_host_header": "httpHostHeader",
        "ip_rules": "ipRules",
        "keep_alive_connections": "keepAliveConnections",
        "keep_alive_timeout": "keepAliveTimeout",
        "no_happy_eyeballs": "noHappyEyeballs",
        "no_tls_verify": "noTlsVerify",
        "origin_server_name": "originServerName",
        "proxy_address": "proxyAddress",
        "proxy_port": "proxyPort",
        "proxy_type": "proxyType",
        "tcp_keep_alive": "tcpKeepAlive",
        "tls_timeout": "tlsTimeout",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfigOriginRequest:
    def __init__(
        self,
        *,
        access: typing.Optional[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        :param http2_origin: Enables HTTP/2 support for the origin connection. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        if isinstance(access, dict):
            access = ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess(**access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5d3bf55d0c00a7c05d180f0b789427c7dae716dde405899da4b0e2783a1c192)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument bastion_mode", value=bastion_mode, expected_type=type_hints["bastion_mode"])
            check_type(argname="argument ca_pool", value=ca_pool, expected_type=type_hints["ca_pool"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument disable_chunked_encoding", value=disable_chunked_encoding, expected_type=type_hints["disable_chunked_encoding"])
            check_type(argname="argument http2_origin", value=http2_origin, expected_type=type_hints["http2_origin"])
            check_type(argname="argument http_host_header", value=http_host_header, expected_type=type_hints["http_host_header"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument keep_alive_connections", value=keep_alive_connections, expected_type=type_hints["keep_alive_connections"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument no_happy_eyeballs", value=no_happy_eyeballs, expected_type=type_hints["no_happy_eyeballs"])
            check_type(argname="argument no_tls_verify", value=no_tls_verify, expected_type=type_hints["no_tls_verify"])
            check_type(argname="argument origin_server_name", value=origin_server_name, expected_type=type_hints["origin_server_name"])
            check_type(argname="argument proxy_address", value=proxy_address, expected_type=type_hints["proxy_address"])
            check_type(argname="argument proxy_port", value=proxy_port, expected_type=type_hints["proxy_port"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
            check_type(argname="argument tcp_keep_alive", value=tcp_keep_alive, expected_type=type_hints["tcp_keep_alive"])
            check_type(argname="argument tls_timeout", value=tls_timeout, expected_type=type_hints["tls_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access is not None:
            self._values["access"] = access
        if bastion_mode is not None:
            self._values["bastion_mode"] = bastion_mode
        if ca_pool is not None:
            self._values["ca_pool"] = ca_pool
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if disable_chunked_encoding is not None:
            self._values["disable_chunked_encoding"] = disable_chunked_encoding
        if http2_origin is not None:
            self._values["http2_origin"] = http2_origin
        if http_host_header is not None:
            self._values["http_host_header"] = http_host_header
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if keep_alive_connections is not None:
            self._values["keep_alive_connections"] = keep_alive_connections
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if no_happy_eyeballs is not None:
            self._values["no_happy_eyeballs"] = no_happy_eyeballs
        if no_tls_verify is not None:
            self._values["no_tls_verify"] = no_tls_verify
        if origin_server_name is not None:
            self._values["origin_server_name"] = origin_server_name
        if proxy_address is not None:
            self._values["proxy_address"] = proxy_address
        if proxy_port is not None:
            self._values["proxy_port"] = proxy_port
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tcp_keep_alive is not None:
            self._values["tcp_keep_alive"] = tcp_keep_alive
        if tls_timeout is not None:
            self._values["tls_timeout"] = tls_timeout

    @builtins.property
    def access(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess"]:
        '''access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess"], result)

    @builtins.property
    def bastion_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs as jump host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        '''
        result = self._values.get("bastion_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ca_pool(self) -> typing.Optional[builtins.str]:
        '''Path to the certificate authority (CA) for the certificate of your origin.

        This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        '''
        result = self._values.get("ca_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for establishing a new TCP connection to your origin server.

        This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_chunked_encoding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        '''
        result = self._values.get("disable_chunked_encoding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http2_origin(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables HTTP/2 support for the origin connection. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        '''
        result = self._values.get("http2_origin")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_host_header(self) -> typing.Optional[builtins.str]:
        '''Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        '''
        result = self._values.get("http_host_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules"]]]:
        '''ip_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        '''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules"]]], result)

    @builtins.property
    def keep_alive_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle keepalive connections between Tunnel and your origin.

        This does not restrict the total number of concurrent connections. Defaults to ``100``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        '''
        result = self._values.get("keep_alive_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        '''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_happy_eyeballs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        '''
        result = self._values.get("no_happy_eyeballs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_tls_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables TLS verification of the certificate presented by your origin.

        Will allow any certificate from the origin to be accepted. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        '''
        result = self._values.get("no_tls_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def origin_server_name(self) -> typing.Optional[builtins.str]:
        '''Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        '''
        result = self._values.get("origin_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_address(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen address for that proxy. Defaults to ``127.0.0.1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        '''
        result = self._values.get("proxy_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_port(self) -> typing.Optional[jsii.Number]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        '''
        result = self._values.get("proxy_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tcp_keep_alive(self) -> typing.Optional[builtins.str]:
        '''The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server.

        Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        '''
        result = self._values.get("tcp_keep_alive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server.

        Defaults to ``10s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        result = self._values.get("tls_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigOriginRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess",
    jsii_struct_bases=[],
    name_mapping={
        "aud_tag": "audTag",
        "required": "required",
        "team_name": "teamName",
    },
)
class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess:
    def __init__(
        self,
        *,
        aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aud_tag: Audience tags of the access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        :param required: Whether the access rule is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        :param team_name: Name of the team to which the access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636abbba3d6b91bc47723277ca9d1141f813092f82ba1708cb75d1f0c9097db8)
            check_type(argname="argument aud_tag", value=aud_tag, expected_type=type_hints["aud_tag"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument team_name", value=team_name, expected_type=type_hints["team_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aud_tag is not None:
            self._values["aud_tag"] = aud_tag
        if required is not None:
            self._values["required"] = required
        if team_name is not None:
            self._values["team_name"] = team_name

    @builtins.property
    def aud_tag(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Audience tags of the access rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        '''
        result = self._values.get("aud_tag")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the access rule is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def team_name(self) -> typing.Optional[builtins.str]:
        '''Name of the team to which the access rule applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        result = self._values.get("team_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86e0f86e5b3fc8c2e50137741b58ef29e41fe146d0cdfb9d6592b12d8c6dd91d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAudTag")
    def reset_aud_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudTag", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetTeamName")
    def reset_team_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeamName", []))

    @builtins.property
    @jsii.member(jsii_name="audTagInput")
    def aud_tag_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "audTagInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="teamNameInput")
    def team_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="audTag")
    def aud_tag(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "audTag"))

    @aud_tag.setter
    def aud_tag(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a857f05881463e736687791e68e716a84630cfacfc70049c12e56182fc9eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81ad11748c769d98fffc79457073e3599b8f2fc6a9ac81fc81acd315386d00e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teamName")
    def team_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamName"))

    @team_name.setter
    def team_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67df2792519e6992fba24f3cdbd2a77cee676f18b08bffc0ee07cedb00883696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe13f1a97dd912038df207594bec01c8ba0426d9a89f22b5e54042a7328cb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules",
    jsii_struct_bases=[],
    name_mapping={"allow": "allow", "ports": "ports", "prefix": "prefix"},
)
class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: Whether to allow the IP prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#allow ZeroTrustTunnelCloudflaredConfigA#allow}
        :param ports: Ports to use within the IP rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ports ZeroTrustTunnelCloudflaredConfigA#ports}
        :param prefix: IP rule prefix. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#prefix ZeroTrustTunnelCloudflaredConfigA#prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7347cdb4bac460f635c3e0d81bed00a6a471cb8069fb35839659f7a3d1758363)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if ports is not None:
            self._values["ports"] = ports
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def allow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow the IP prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#allow ZeroTrustTunnelCloudflaredConfigA#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Ports to use within the IP rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ports ZeroTrustTunnelCloudflaredConfigA#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''IP rule prefix.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#prefix ZeroTrustTunnelCloudflaredConfigA#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78127096cc5ae0063e160bb19f825429c636818de360b7686d7d460d55f08772)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cb9e4b5952ffbbd6ccd5fec016171eb879db00538b522f5ef0214bd4a95f52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec2cd99bc0f0c6543ca531371f33b5f0380ced60678adee72caadeeb5b03133)
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
            type_hints = typing.get_type_hints(_typecheckingstub__503ecd8cc246812f1d06b91e2ee5dad4ed492514ee78d5cd8acb195163735d64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fcfabaf40d33f5eec50d7660731f2ad12223cb9e0042ddb320481d9ca93e504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2bb700ef399aef680d25c273885a3c276fc005ac26c30ce608104845654e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6200320b30cefd462b26d7ecf0d5820063eafe77bbb1a2082f0e86a3658a98bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allow"))

    @allow.setter
    def allow(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b818793427c25477a5306c6ebc57bbfc742e7f76e6f280ace007b98e43f15a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885c1a40abb847948c1106b209ceda5aed546e8d4d3cced118af9766749ed5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332ee832ee3e9e7e6b75e453380e0471bfae5774b9e080d9b80ffd100d901b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92449f713d7730f876a68b8d8d80003ca3a8a3c6717363c967559cac2829caec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigOriginRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOriginRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14ed818023f6e70d496e8f3d24a0342f4cfb4ff2cdb736e798cdb43c9bfaa173)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccess")
    def put_access(
        self,
        *,
        aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        team_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aud_tag: Audience tags of the access rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#aud_tag ZeroTrustTunnelCloudflaredConfigA#aud_tag}
        :param required: Whether the access rule is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#required ZeroTrustTunnelCloudflaredConfigA#required}
        :param team_name: Name of the team to which the access rule applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#team_name ZeroTrustTunnelCloudflaredConfigA#team_name}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess(
            aud_tag=aud_tag, required=required, team_name=team_name
        )

        return typing.cast(None, jsii.invoke(self, "putAccess", [value]))

    @jsii.member(jsii_name="putIpRules")
    def put_ip_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb15e576c8ce45d2bf18b0bc3a91153ea18730e27d899e55cc443face7fb032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRules", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetBastionMode")
    def reset_bastion_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBastionMode", []))

    @jsii.member(jsii_name="resetCaPool")
    def reset_ca_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaPool", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetDisableChunkedEncoding")
    def reset_disable_chunked_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableChunkedEncoding", []))

    @jsii.member(jsii_name="resetHttp2Origin")
    def reset_http2_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Origin", []))

    @jsii.member(jsii_name="resetHttpHostHeader")
    def reset_http_host_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHostHeader", []))

    @jsii.member(jsii_name="resetIpRules")
    def reset_ip_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRules", []))

    @jsii.member(jsii_name="resetKeepAliveConnections")
    def reset_keep_alive_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveConnections", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetNoHappyEyeballs")
    def reset_no_happy_eyeballs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoHappyEyeballs", []))

    @jsii.member(jsii_name="resetNoTlsVerify")
    def reset_no_tls_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoTlsVerify", []))

    @jsii.member(jsii_name="resetOriginServerName")
    def reset_origin_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginServerName", []))

    @jsii.member(jsii_name="resetProxyAddress")
    def reset_proxy_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyAddress", []))

    @jsii.member(jsii_name="resetProxyPort")
    def reset_proxy_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyPort", []))

    @jsii.member(jsii_name="resetProxyType")
    def reset_proxy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyType", []))

    @jsii.member(jsii_name="resetTcpKeepAlive")
    def reset_tcp_keep_alive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpKeepAlive", []))

    @jsii.member(jsii_name="resetTlsTimeout")
    def reset_tls_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccessOutputReference:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccessOutputReference, jsii.get(self, "access"))

    @builtins.property
    @jsii.member(jsii_name="ipRules")
    def ip_rules(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesList:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesList, jsii.get(self, "ipRules"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="bastionModeInput")
    def bastion_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bastionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="caPoolInput")
    def ca_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncodingInput")
    def disable_chunked_encoding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableChunkedEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="http2OriginInput")
    def http2_origin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2OriginInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHostHeaderInput")
    def http_host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpHostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRulesInput")
    def ip_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]], jsii.get(self, "ipRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnectionsInput")
    def keep_alive_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballsInput")
    def no_happy_eyeballs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noHappyEyeballsInput"))

    @builtins.property
    @jsii.member(jsii_name="noTlsVerifyInput")
    def no_tls_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noTlsVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="originServerNameInput")
    def origin_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originServerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddressInput")
    def proxy_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyPortInput")
    def proxy_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "proxyPortInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyTypeInput")
    def proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAliveInput")
    def tcp_keep_alive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tcpKeepAliveInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsTimeoutInput")
    def tls_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="bastionMode")
    def bastion_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bastionMode"))

    @bastion_mode.setter
    def bastion_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31d4b159536faca5b71ec319f933f5d0d8309dc20fb612cedb58ad3cda679b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bastionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caPool")
    def ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPool"))

    @ca_pool.setter
    def ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712a69bd37ac0a2424e23862764e00b6d78181e2914cf2a34dec1dddbe45d2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a11cbad4d6de372eb7883d507114eb630475d6ea23a58b7bdf09153afe8d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncoding")
    def disable_chunked_encoding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableChunkedEncoding"))

    @disable_chunked_encoding.setter
    def disable_chunked_encoding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36838fba95a0c619011e21bd444a6a986dcb95669169e60a06120f3caabc595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableChunkedEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="http2Origin")
    def http2_origin(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Origin"))

    @http2_origin.setter
    def http2_origin(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f7a86e1dfff26d9d5cdd690048c026ece6dc10c90e8f0d0c0f0bbcc2ac5958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Origin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpHostHeader")
    def http_host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpHostHeader"))

    @http_host_header.setter
    def http_host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438be1ee5abfbdd1d913817cc3bd02abdfac71d9451b467897af34ba57c0eeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHostHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnections")
    def keep_alive_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveConnections"))

    @keep_alive_connections.setter
    def keep_alive_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7a7e50fb00305b05aab1a9a34504b9f087fa35775ce3552c5bf826e8c40e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a0063089e26377a1d0f645ecc027cdd51213031e7b1042ebf2a1c21fbc77ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballs")
    def no_happy_eyeballs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noHappyEyeballs"))

    @no_happy_eyeballs.setter
    def no_happy_eyeballs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fadc061a2ebd7000f9fcce0ecb9d0733a5b8c4391a2d45c324b0e8774eb2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHappyEyeballs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noTlsVerify")
    def no_tls_verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noTlsVerify"))

    @no_tls_verify.setter
    def no_tls_verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45eb764a16a1e8e1ba2029ae09bf43c7eee9a45782ade31b4be1bc38316a4ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noTlsVerify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originServerName")
    def origin_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originServerName"))

    @origin_server_name.setter
    def origin_server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47a0f6c18dd6a911bb9888d6f3946b8cd35b726039d99d1184603f65f43b871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originServerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyAddress")
    def proxy_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyAddress"))

    @proxy_address.setter
    def proxy_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327dfd5201bdfc70f787b62637538c2bcd95e75ac5b93b4b4a1446c41087ed7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyPort")
    def proxy_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "proxyPort"))

    @proxy_port.setter
    def proxy_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e3c3fd9129c2466886c39d709d69c4e80a279e7d263a90f7836d214a037ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proxyType")
    def proxy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyType"))

    @proxy_type.setter
    def proxy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ed5e2a6769463c229129c016b826003db5aae63124d3225b493ad60b7b00ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAlive")
    def tcp_keep_alive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tcpKeepAlive"))

    @tcp_keep_alive.setter
    def tcp_keep_alive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84d9c4d023c40e2023e656a84aa1bff48d21a3dfb57b75f93198b9d99e6ba0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsTimeout")
    def tls_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsTimeout"))

    @tls_timeout.setter
    def tls_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc1f1c89618530620d72521d58eb34983a055b9dae45ef76dd9565c4aaa8047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbd31fb600c0d6fd99236aee67247968ecc971dbe01adecc5cc57df562cac7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustTunnelCloudflaredConfigConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19457e6868b063037de72e53eaf5ef0e9cc6b6117cdbf957d322f714d0825bbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIngressRule")
    def put_ingress_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496c29f1d63f2e3cc84749841a085863960af405b799f157c8cbcc5a0ff2b893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressRule", [value]))

    @jsii.member(jsii_name="putOriginRequest")
    def put_origin_request(
        self,
        *,
        access: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess, typing.Dict[builtins.str, typing.Any]]] = None,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access: access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#access ZeroTrustTunnelCloudflaredConfigA#access}
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#bastion_mode ZeroTrustTunnelCloudflaredConfigA#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ca_pool ZeroTrustTunnelCloudflaredConfigA#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#connect_timeout ZeroTrustTunnelCloudflaredConfigA#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#disable_chunked_encoding ZeroTrustTunnelCloudflaredConfigA#disable_chunked_encoding}
        :param http2_origin: Enables HTTP/2 support for the origin connection. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http2_origin ZeroTrustTunnelCloudflaredConfigA#http2_origin}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#http_host_header ZeroTrustTunnelCloudflaredConfigA#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#ip_rules ZeroTrustTunnelCloudflaredConfigA#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_connections ZeroTrustTunnelCloudflaredConfigA#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#keep_alive_timeout ZeroTrustTunnelCloudflaredConfigA#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_happy_eyeballs ZeroTrustTunnelCloudflaredConfigA#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#no_tls_verify ZeroTrustTunnelCloudflaredConfigA#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#origin_server_name ZeroTrustTunnelCloudflaredConfigA#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_address ZeroTrustTunnelCloudflaredConfigA#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_port ZeroTrustTunnelCloudflaredConfigA#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``""``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#proxy_type ZeroTrustTunnelCloudflaredConfigA#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tcp_keep_alive ZeroTrustTunnelCloudflaredConfigA#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#tls_timeout ZeroTrustTunnelCloudflaredConfigA#tls_timeout}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfigOriginRequest(
            access=access,
            bastion_mode=bastion_mode,
            ca_pool=ca_pool,
            connect_timeout=connect_timeout,
            disable_chunked_encoding=disable_chunked_encoding,
            http2_origin=http2_origin,
            http_host_header=http_host_header,
            ip_rules=ip_rules,
            keep_alive_connections=keep_alive_connections,
            keep_alive_timeout=keep_alive_timeout,
            no_happy_eyeballs=no_happy_eyeballs,
            no_tls_verify=no_tls_verify,
            origin_server_name=origin_server_name,
            proxy_address=proxy_address,
            proxy_port=proxy_port,
            proxy_type=proxy_type,
            tcp_keep_alive=tcp_keep_alive,
            tls_timeout=tls_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putOriginRequest", [value]))

    @jsii.member(jsii_name="putWarpRouting")
    def put_warp_routing(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether WARP routing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#enabled ZeroTrustTunnelCloudflaredConfigA#enabled}
        '''
        value = ZeroTrustTunnelCloudflaredConfigConfigWarpRouting(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putWarpRouting", [value]))

    @jsii.member(jsii_name="resetOriginRequest")
    def reset_origin_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequest", []))

    @jsii.member(jsii_name="resetWarpRouting")
    def reset_warp_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarpRouting", []))

    @builtins.property
    @jsii.member(jsii_name="ingressRule")
    def ingress_rule(self) -> ZeroTrustTunnelCloudflaredConfigConfigIngressRuleList:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigIngressRuleList, jsii.get(self, "ingressRule"))

    @builtins.property
    @jsii.member(jsii_name="originRequest")
    def origin_request(
        self,
    ) -> ZeroTrustTunnelCloudflaredConfigConfigOriginRequestOutputReference:
        return typing.cast(ZeroTrustTunnelCloudflaredConfigConfigOriginRequestOutputReference, jsii.get(self, "originRequest"))

    @builtins.property
    @jsii.member(jsii_name="warpRouting")
    def warp_routing(
        self,
    ) -> "ZeroTrustTunnelCloudflaredConfigConfigWarpRoutingOutputReference":
        return typing.cast("ZeroTrustTunnelCloudflaredConfigConfigWarpRoutingOutputReference", jsii.get(self, "warpRouting"))

    @builtins.property
    @jsii.member(jsii_name="ingressRuleInput")
    def ingress_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]], jsii.get(self, "ingressRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="originRequestInput")
    def origin_request_input(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest], jsii.get(self, "originRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="warpRoutingInput")
    def warp_routing_input(
        self,
    ) -> typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting"]:
        return typing.cast(typing.Optional["ZeroTrustTunnelCloudflaredConfigConfigWarpRouting"], jsii.get(self, "warpRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfig]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75ca61add465032e585d1d118bacb0832f0d53c4293cc5518b7be51dfec264a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigWarpRouting",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ZeroTrustTunnelCloudflaredConfigConfigWarpRouting:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether WARP routing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#enabled ZeroTrustTunnelCloudflaredConfigA#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3e1ea8cd08dc832b2e8e14bd56b1b36e7f2083b8b36c756061fe2f7beedc32)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether WARP routing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_tunnel_cloudflared_config#enabled ZeroTrustTunnelCloudflaredConfigA#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustTunnelCloudflaredConfigConfigWarpRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustTunnelCloudflaredConfigConfigWarpRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustTunnelCloudflaredConfig.ZeroTrustTunnelCloudflaredConfigConfigWarpRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8629155531f17477c6ab961f43617832fd6ee69d2b8d6466e30e9faf33a082e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba61f341da9e8356ab6c9a5c65019866f09914581483a2b19828e9832deb0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigWarpRouting]:
        return typing.cast(typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigWarpRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigWarpRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff4919160f915420f9d741f4579e95fb8e441e0ccbe4e45aefa0aa1ca49489c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ZeroTrustTunnelCloudflaredConfigA",
    "ZeroTrustTunnelCloudflaredConfigAConfig",
    "ZeroTrustTunnelCloudflaredConfigConfig",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRule",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleList",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccessOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesList",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRulesOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequest",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccessOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesList",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRulesOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigOriginRequestOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigOutputReference",
    "ZeroTrustTunnelCloudflaredConfigConfigWarpRouting",
    "ZeroTrustTunnelCloudflaredConfigConfigWarpRoutingOutputReference",
]

publication.publish()

def _typecheckingstub__40c3e700edd3e4bf5ead6f056e28348ae350d0c39ce57e46a2c6c9127b5877e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    config: typing.Union[ZeroTrustTunnelCloudflaredConfigConfig, typing.Dict[builtins.str, typing.Any]],
    tunnel_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__26886a3195522bd58df26c7e41578c5a4b7c8ef2a01aabc8c8b2fc6d581237ad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063215e6de559dfdb173577ef39a73e59c8da14db0dd681f9214f49fade47a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bede05880359079fc7529b2e51e3d16d3d021e372e035a58fa44e1dca1436b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95fc4ac1123f5860744e72d1b82de65fe429be4b727ca3fef5e54ece11f1142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae33dabb83c6599c16c97f82f27e96662097f36b213d22e119d6e7c7e366024(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    config: typing.Union[ZeroTrustTunnelCloudflaredConfigConfig, typing.Dict[builtins.str, typing.Any]],
    tunnel_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecc74d84626090dba3f174efaac8078277aacbf27564f772b864127e59e4cd7(
    *,
    ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRule, typing.Dict[builtins.str, typing.Any]]]],
    origin_request: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    warp_routing: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigWarpRouting, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a4e201c4a4ea6a55411d1d57b4c73797a780fa92231ade5c588b010876652f(
    *,
    service: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
    origin_request: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4057401fd474ba55c8e647a6e34cddd8272b77093283ba0d231a47525aefb3d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8281f5c88561a73d2e5b074c1bda6dbc1efbcc1517896971239f7224d816e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0413336206bc9b53cf81a02ff19efd897a5853aac2fd838a2215217bd93167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fb8afe714a3db09615a0c4ff1883eb8dac7302cb3094041d37930ffd10610d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520fd98ca2092a08ee6913db42e01d3b78a317db7192198aa8609b485e9cf3c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf1618980b06838d4c7ebab65bd07d5199f890d13959efb0316621b09a9795(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fafe5f372e164d0a5a19b25ff85fd89564bbdca36555e07b7ea4f5efe029d54(
    *,
    access: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ca_pool: typing.Optional[builtins.str] = None,
    connect_timeout: typing.Optional[builtins.str] = None,
    disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_host_header: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    keep_alive_connections: typing.Optional[jsii.Number] = None,
    keep_alive_timeout: typing.Optional[builtins.str] = None,
    no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    origin_server_name: typing.Optional[builtins.str] = None,
    proxy_address: typing.Optional[builtins.str] = None,
    proxy_port: typing.Optional[jsii.Number] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tcp_keep_alive: typing.Optional[builtins.str] = None,
    tls_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda61023c603696303ddc0e815a2bdc21bff847f9f1405268a9bd111bc00b7c9(
    *,
    aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    team_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a2554b06be461332e98aa4f418f2f368f8894567b4b9e6d1b0d5ed2793612c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8983b753f92000beeaf050937ee0aa31ead2d3ccabc77c171126a20c9f03c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4fc95c7a4e57ffcb7bcadb906713ee93c80bafc1c131d94a453da0388fb46d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35af9aea13fa86cae7b1d7785e2cbd1879cfff2c2b54db365e67cf071d6543a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529e111ffde8ee8194c7e0ea78a35d971fb2bb74a310a36cb34071381b424b46(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d235775b2b5684e6cc2dceeca99f8e0a8655403cb53ce7124bfc6b17815149db(
    *,
    allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f3c10a26f40d13210388a346fdf9239bb693bb3ef848e394f74b009d513fa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bbd8591038edf4d26bcea67f86ab85b691cae167463406c7709a642d35648a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5281d86fb2722983bec40efd52487e12f2acf191867e792edecb7e0ddc32c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8917102a45b4cecdd8adc31bc358a44853bda63799422731bf56317fabc0cd93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4f07f7e50473550a7c9b018dcfe816a7a303dfc9fd615fc7f93dc4f3498359(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4462269b6903779a499f7d09b131646cb5237c67b3fecf8bf119132d64cbf11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d281787f528c6b73260e604e3577db686e5a7c34e1538a6d496dd36ee1387409(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bb2510b90552efcc5527835abe24d5008726e19ae8c7ebddc80c7a21eacbd7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9302b09728de6ca66381ddd53148b1553fcda7309f7a67aff060f176eddec98d(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173193cda90876e01697cbd4cab180a4a87cb1bd4d55df06c8f87c997248b62c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caeab655464fe3bf58bbe286fc28ef956e6819186a770c79a9da9adbecbfe91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff517f14c7f42bdd799d716367844edd333ee264d787c2ebb44bb88dc658b8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bd9ac9c18acf700a7da5d18ce4343627404cd4e46d9a7146b52673d8e9a9cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48923fc3ddef9f49e85c14415e40d20499141c82fe3d1dd9b87a0ac47cf924f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d703ee5cd2c8672e4f188f8fe912d87f533b31da634d03d38b51c19d697522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3e5d7817fd95f568fcf1fb5639d29c8f666ad9e10abee9c058fbe54a647c16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bc167b24f6ac416a0849a56a604816f3d2299e9d19b3d42dc6b210d345d501(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2299036b1d042be8ca3bd100a967699cdd11e3569cfa78446ba590285ebed1ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05d7869024b1c7614b7c7fb1261badf662db2cbdf6f2848cb90f8807a79ba85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730564f629b4c141b2d675ecef9d446a29ba87ef5f4b9736b2be1e9a2f25676e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d35460d731cd259665c23114023246b8ef0e47329f3730738d3d4f0e709877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebeb7476cd43ee4e21cac202871fa5964433ceb325c24e793ecadb17c1127c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef646ed0e45c708ee1676ad488e1f4acc5ae2675826845ad7cae673830b91eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da22d6267a2da2206a396625ba33f242019921807d1c4b1b9f87590bc408580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e37a105da46732cf233b2cbfb9de43e42668a8641677907dc4120751849fb93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de8c9712ee2ace588f8919a7e00e6c89a295b7018ae7d607da29c2cb2e0bf4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471a9c6f83a53c54882522d589ac5a56b002a13aafa292c587acc4f3e7849630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ac8f8b909994a46d658c5110b0f90779de875755de36fdcdc6d9a854c0cd73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced73ad0d0e21799840ff5b8d47e38bbb4b73325b4ace6815709b5f2f7b6a963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda91d55246e67bacd8ac966d30183a69a04fc3d6d2fc9eb9967f9cdac4085b8(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigIngressRuleOriginRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46bedf8d7966cd76d53c9c2c13c957cda69327b17ee69d6a57f29bbea2cf489(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd4678bb3495ed12b3d5b3c1bf6a8a571c871150deb291c4611629067eeb4f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd9c3ad847b0d9f5b7346c76011484fbd7cf06c952cf59cd1636a434ac0afd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3b3d685679d4993f6dc77868598c43bf0634c847ebc73b4cb0a923a4f79268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d2ccf7ee2879a9fa849d0185dfbf1def3eca7f065b267912dd02ca90dbb1fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigIngressRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d3bf55d0c00a7c05d180f0b789427c7dae716dde405899da4b0e2783a1c192(
    *,
    access: typing.Optional[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ca_pool: typing.Optional[builtins.str] = None,
    connect_timeout: typing.Optional[builtins.str] = None,
    disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http2_origin: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_host_header: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    keep_alive_connections: typing.Optional[jsii.Number] = None,
    keep_alive_timeout: typing.Optional[builtins.str] = None,
    no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    origin_server_name: typing.Optional[builtins.str] = None,
    proxy_address: typing.Optional[builtins.str] = None,
    proxy_port: typing.Optional[jsii.Number] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tcp_keep_alive: typing.Optional[builtins.str] = None,
    tls_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636abbba3d6b91bc47723277ca9d1141f813092f82ba1708cb75d1f0c9097db8(
    *,
    aud_tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    team_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e0f86e5b3fc8c2e50137741b58ef29e41fe146d0cdfb9d6592b12d8c6dd91d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a857f05881463e736687791e68e716a84630cfacfc70049c12e56182fc9eaa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81ad11748c769d98fffc79457073e3599b8f2fc6a9ac81fc81acd315386d00e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67df2792519e6992fba24f3cdbd2a77cee676f18b08bffc0ee07cedb00883696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe13f1a97dd912038df207594bec01c8ba0426d9a89f22b5e54042a7328cb09(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7347cdb4bac460f635c3e0d81bed00a6a471cb8069fb35839659f7a3d1758363(
    *,
    allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78127096cc5ae0063e160bb19f825429c636818de360b7686d7d460d55f08772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cb9e4b5952ffbbd6ccd5fec016171eb879db00538b522f5ef0214bd4a95f52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec2cd99bc0f0c6543ca531371f33b5f0380ced60678adee72caadeeb5b03133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503ecd8cc246812f1d06b91e2ee5dad4ed492514ee78d5cd8acb195163735d64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcfabaf40d33f5eec50d7660731f2ad12223cb9e0042ddb320481d9ca93e504(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2bb700ef399aef680d25c273885a3c276fc005ac26c30ce608104845654e6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6200320b30cefd462b26d7ecf0d5820063eafe77bbb1a2082f0e86a3658a98bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b818793427c25477a5306c6ebc57bbfc742e7f76e6f280ace007b98e43f15a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885c1a40abb847948c1106b209ceda5aed546e8d4d3cced118af9766749ed5f0(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332ee832ee3e9e7e6b75e453380e0471bfae5774b9e080d9b80ffd100d901b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92449f713d7730f876a68b8d8d80003ca3a8a3c6717363c967559cac2829caec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ed818023f6e70d496e8f3d24a0342f4cfb4ff2cdb736e798cdb43c9bfaa173(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb15e576c8ce45d2bf18b0bc3a91153ea18730e27d899e55cc443face7fb032(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31d4b159536faca5b71ec319f933f5d0d8309dc20fb612cedb58ad3cda679b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712a69bd37ac0a2424e23862764e00b6d78181e2914cf2a34dec1dddbe45d2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a11cbad4d6de372eb7883d507114eb630475d6ea23a58b7bdf09153afe8d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36838fba95a0c619011e21bd444a6a986dcb95669169e60a06120f3caabc595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f7a86e1dfff26d9d5cdd690048c026ece6dc10c90e8f0d0c0f0bbcc2ac5958(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438be1ee5abfbdd1d913817cc3bd02abdfac71d9451b467897af34ba57c0eeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7a7e50fb00305b05aab1a9a34504b9f087fa35775ce3552c5bf826e8c40e4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a0063089e26377a1d0f645ecc027cdd51213031e7b1042ebf2a1c21fbc77ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fadc061a2ebd7000f9fcce0ecb9d0733a5b8c4391a2d45c324b0e8774eb2bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45eb764a16a1e8e1ba2029ae09bf43c7eee9a45782ade31b4be1bc38316a4ae6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47a0f6c18dd6a911bb9888d6f3946b8cd35b726039d99d1184603f65f43b871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327dfd5201bdfc70f787b62637538c2bcd95e75ac5b93b4b4a1446c41087ed7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e3c3fd9129c2466886c39d709d69c4e80a279e7d263a90f7836d214a037ef7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ed5e2a6769463c229129c016b826003db5aae63124d3225b493ad60b7b00ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84d9c4d023c40e2023e656a84aa1bff48d21a3dfb57b75f93198b9d99e6ba0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc1f1c89618530620d72521d58eb34983a055b9dae45ef76dd9565c4aaa8047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbd31fb600c0d6fd99236aee67247968ecc971dbe01adecc5cc57df562cac7c(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigOriginRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19457e6868b063037de72e53eaf5ef0e9cc6b6117cdbf957d322f714d0825bbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496c29f1d63f2e3cc84749841a085863960af405b799f157c8cbcc5a0ff2b893(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustTunnelCloudflaredConfigConfigIngressRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75ca61add465032e585d1d118bacb0832f0d53c4293cc5518b7be51dfec264a(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3e1ea8cd08dc832b2e8e14bd56b1b36e7f2083b8b36c756061fe2f7beedc32(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8629155531f17477c6ab961f43617832fd6ee69d2b8d6466e30e9faf33a082e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba61f341da9e8356ab6c9a5c65019866f09914581483a2b19828e9832deb0fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff4919160f915420f9d741f4579e95fb8e441e0ccbe4e45aefa0aa1ca49489c(
    value: typing.Optional[ZeroTrustTunnelCloudflaredConfigConfigWarpRouting],
) -> None:
    """Type checking stubs"""
    pass
