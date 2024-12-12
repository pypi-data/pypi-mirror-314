r'''
# `cloudflare_infrastructure_access_target`

Refer to the Terraform Registry for docs: [`cloudflare_infrastructure_access_target`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target).
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


class InfrastructureAccessTarget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTarget",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target cloudflare_infrastructure_access_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        hostname: builtins.str,
        ip: typing.Union["InfrastructureAccessTargetIp", typing.Dict[builtins.str, typing.Any]],
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target cloudflare_infrastructure_access_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#account_id InfrastructureAccessTarget#account_id}
        :param hostname: A non-unique field that refers to a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#hostname InfrastructureAccessTarget#hostname}
        :param ip: The IPv4/IPv6 address that identifies where to reach a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip InfrastructureAccessTarget#ip}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa4b1d2c3ab0c129bfde6ed09dc61301ceafbacd80d13f625566733c130d8fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = InfrastructureAccessTargetConfig(
            account_id=account_id,
            hostname=hostname,
            ip=ip,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a InfrastructureAccessTarget resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the InfrastructureAccessTarget to import.
        :param import_from_id: The id of the existing InfrastructureAccessTarget that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the InfrastructureAccessTarget to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce46f049b869ff4b2858189d0d2558e2ba26964dd201c64b59246251ed0febf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIp")
    def put_ip(
        self,
        *,
        ipv4: typing.Optional[typing.Union["InfrastructureAccessTargetIpIpv4", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union["InfrastructureAccessTargetIpIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv4 InfrastructureAccessTarget#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv6 InfrastructureAccessTarget#ipv6}
        '''
        value = InfrastructureAccessTargetIp(ipv4=ipv4, ipv6=ipv6)

        return typing.cast(None, jsii.invoke(self, "putIp", [value]))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> "InfrastructureAccessTargetIpOutputReference":
        return typing.cast("InfrastructureAccessTargetIpOutputReference", jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="modifiedAt")
    def modified_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "InfrastructureAccessTargetIp"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "InfrastructureAccessTargetIp"]], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e78511e4e698d39ad681145483e65224f8c6da314709ab634c1962857f5757c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096477a33588803401a173a2d439818ba6bb3624d75143e5c48d946f73490d9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetConfig",
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
        "hostname": "hostname",
        "ip": "ip",
    },
)
class InfrastructureAccessTargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostname: builtins.str,
        ip: typing.Union["InfrastructureAccessTargetIp", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#account_id InfrastructureAccessTarget#account_id}
        :param hostname: A non-unique field that refers to a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#hostname InfrastructureAccessTarget#hostname}
        :param ip: The IPv4/IPv6 address that identifies where to reach a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip InfrastructureAccessTarget#ip}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ip, dict):
            ip = InfrastructureAccessTargetIp(**ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3b866f97c17c7ae5bbeb083bf35f82e0506978714e50fb7097d75a86f62bb1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "hostname": hostname,
            "ip": ip,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#account_id InfrastructureAccessTarget#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''A non-unique field that refers to a target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#hostname InfrastructureAccessTarget#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> "InfrastructureAccessTargetIp":
        '''The IPv4/IPv6 address that identifies where to reach a target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip InfrastructureAccessTarget#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast("InfrastructureAccessTargetIp", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureAccessTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIp",
    jsii_struct_bases=[],
    name_mapping={"ipv4": "ipv4", "ipv6": "ipv6"},
)
class InfrastructureAccessTargetIp:
    def __init__(
        self,
        *,
        ipv4: typing.Optional[typing.Union["InfrastructureAccessTargetIpIpv4", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union["InfrastructureAccessTargetIpIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv4 InfrastructureAccessTarget#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv6 InfrastructureAccessTarget#ipv6}
        '''
        if isinstance(ipv4, dict):
            ipv4 = InfrastructureAccessTargetIpIpv4(**ipv4)
        if isinstance(ipv6, dict):
            ipv6 = InfrastructureAccessTargetIpIpv6(**ipv6)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cc323f7ff351a879d40997fc74bdd00d5bf3f24633feed7387245005e08321)
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6

    @builtins.property
    def ipv4(self) -> typing.Optional["InfrastructureAccessTargetIpIpv4"]:
        '''The target's IPv4 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv4 InfrastructureAccessTarget#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional["InfrastructureAccessTargetIpIpv4"], result)

    @builtins.property
    def ipv6(self) -> typing.Optional["InfrastructureAccessTargetIpIpv6"]:
        '''The target's IPv6 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ipv6 InfrastructureAccessTarget#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional["InfrastructureAccessTargetIpIpv6"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureAccessTargetIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIpIpv4",
    jsii_struct_bases=[],
    name_mapping={"ip_addr": "ipAddr", "virtual_network_id": "virtualNetworkId"},
)
class InfrastructureAccessTargetIpIpv4:
    def __init__(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1af5ed8f4356edfa6cd11ef7a9087919ccf3682ac27d111af77c0c09e212d8f)
            check_type(argname="argument ip_addr", value=ip_addr, expected_type=type_hints["ip_addr"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_addr": ip_addr,
            "virtual_network_id": virtual_network_id,
        }

    @builtins.property
    def ip_addr(self) -> builtins.str:
        '''The IP address of the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        '''
        result = self._values.get("ip_addr")
        assert result is not None, "Required property 'ip_addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The private virtual network identifier for the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureAccessTargetIpIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfrastructureAccessTargetIpIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIpIpv4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2816cdbb33523c718ea4c4260d7535f70a97edddf1c23cced2ebc6a97bf0fb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipAddrInput")
    def ip_addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddrInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddr")
    def ip_addr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddr"))

    @ip_addr.setter
    def ip_addr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f722a972a19fabf7416efd9163789da30da595c650dcefb5913726e44fb03e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732b2fcc562cd81f2b77c28eddedbe6f6d436007d354aea4e717d8113c0b051a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f978535b1d1de364548e5c31ae583235ceab27ce291b3b69d27b1a5c161fd5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIpIpv6",
    jsii_struct_bases=[],
    name_mapping={"ip_addr": "ipAddr", "virtual_network_id": "virtualNetworkId"},
)
class InfrastructureAccessTargetIpIpv6:
    def __init__(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af86c7e95906b9927bafe47bd96b4bb50081342cef123fad33b368a8ace6b0d2)
            check_type(argname="argument ip_addr", value=ip_addr, expected_type=type_hints["ip_addr"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_addr": ip_addr,
            "virtual_network_id": virtual_network_id,
        }

    @builtins.property
    def ip_addr(self) -> builtins.str:
        '''The IP address of the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        '''
        result = self._values.get("ip_addr")
        assert result is not None, "Required property 'ip_addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The private virtual network identifier for the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfrastructureAccessTargetIpIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfrastructureAccessTargetIpIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIpIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acdcc0f9dfe2742ad5df92a60902f62db5f103068369ba6a4a425a51243d01ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ipAddrInput")
    def ip_addr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddrInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddr")
    def ip_addr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddr"))

    @ip_addr.setter
    def ip_addr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec56bc64ac1097deebe246dbbe962cb6163b581bc6ee2026a895d9282b2a97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d0c6b2b29f5ad7b49194226454455ec48fd399f050ecefbc1002e6c6ef507d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d06a1496352c73820af4716f4d5edbc53a44bdec2a77978a20cee6d435a90b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class InfrastructureAccessTargetIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.infrastructureAccessTarget.InfrastructureAccessTargetIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f070d1df28f2dc32bc38189586dd75959a4630eeddc23c1ffaa09e863e1b9e07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpv4")
    def put_ipv4(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        value = InfrastructureAccessTargetIpIpv4(
            ip_addr=ip_addr, virtual_network_id=virtual_network_id
        )

        return typing.cast(None, jsii.invoke(self, "putIpv4", [value]))

    @jsii.member(jsii_name="putIpv6")
    def put_ipv6(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#ip_addr InfrastructureAccessTarget#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/infrastructure_access_target#virtual_network_id InfrastructureAccessTarget#virtual_network_id}
        '''
        value = InfrastructureAccessTargetIpIpv6(
            ip_addr=ip_addr, virtual_network_id=virtual_network_id
        )

        return typing.cast(None, jsii.invoke(self, "putIpv6", [value]))

    @jsii.member(jsii_name="resetIpv4")
    def reset_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> InfrastructureAccessTargetIpIpv4OutputReference:
        return typing.cast(InfrastructureAccessTargetIpIpv4OutputReference, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> InfrastructureAccessTargetIpIpv6OutputReference:
        return typing.cast(InfrastructureAccessTargetIpIpv6OutputReference, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478770b5d29cde788d7faeec74e4ac313313b067d3394511924d0ea2f81bc797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "InfrastructureAccessTarget",
    "InfrastructureAccessTargetConfig",
    "InfrastructureAccessTargetIp",
    "InfrastructureAccessTargetIpIpv4",
    "InfrastructureAccessTargetIpIpv4OutputReference",
    "InfrastructureAccessTargetIpIpv6",
    "InfrastructureAccessTargetIpIpv6OutputReference",
    "InfrastructureAccessTargetIpOutputReference",
]

publication.publish()

def _typecheckingstub__2fa4b1d2c3ab0c129bfde6ed09dc61301ceafbacd80d13f625566733c130d8fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    hostname: builtins.str,
    ip: typing.Union[InfrastructureAccessTargetIp, typing.Dict[builtins.str, typing.Any]],
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

def _typecheckingstub__6ce46f049b869ff4b2858189d0d2558e2ba26964dd201c64b59246251ed0febf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e78511e4e698d39ad681145483e65224f8c6da314709ab634c1962857f5757c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096477a33588803401a173a2d439818ba6bb3624d75143e5c48d946f73490d9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3b866f97c17c7ae5bbeb083bf35f82e0506978714e50fb7097d75a86f62bb1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    hostname: builtins.str,
    ip: typing.Union[InfrastructureAccessTargetIp, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cc323f7ff351a879d40997fc74bdd00d5bf3f24633feed7387245005e08321(
    *,
    ipv4: typing.Optional[typing.Union[InfrastructureAccessTargetIpIpv4, typing.Dict[builtins.str, typing.Any]]] = None,
    ipv6: typing.Optional[typing.Union[InfrastructureAccessTargetIpIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1af5ed8f4356edfa6cd11ef7a9087919ccf3682ac27d111af77c0c09e212d8f(
    *,
    ip_addr: builtins.str,
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2816cdbb33523c718ea4c4260d7535f70a97edddf1c23cced2ebc6a97bf0fb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f722a972a19fabf7416efd9163789da30da595c650dcefb5913726e44fb03e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732b2fcc562cd81f2b77c28eddedbe6f6d436007d354aea4e717d8113c0b051a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f978535b1d1de364548e5c31ae583235ceab27ce291b3b69d27b1a5c161fd5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv4]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af86c7e95906b9927bafe47bd96b4bb50081342cef123fad33b368a8ace6b0d2(
    *,
    ip_addr: builtins.str,
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdcc0f9dfe2742ad5df92a60902f62db5f103068369ba6a4a425a51243d01ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec56bc64ac1097deebe246dbbe962cb6163b581bc6ee2026a895d9282b2a97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d0c6b2b29f5ad7b49194226454455ec48fd399f050ecefbc1002e6c6ef507d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d06a1496352c73820af4716f4d5edbc53a44bdec2a77978a20cee6d435a90b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIpIpv6]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f070d1df28f2dc32bc38189586dd75959a4630eeddc23c1ffaa09e863e1b9e07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478770b5d29cde788d7faeec74e4ac313313b067d3394511924d0ea2f81bc797(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, InfrastructureAccessTargetIp]],
) -> None:
    """Type checking stubs"""
    pass
