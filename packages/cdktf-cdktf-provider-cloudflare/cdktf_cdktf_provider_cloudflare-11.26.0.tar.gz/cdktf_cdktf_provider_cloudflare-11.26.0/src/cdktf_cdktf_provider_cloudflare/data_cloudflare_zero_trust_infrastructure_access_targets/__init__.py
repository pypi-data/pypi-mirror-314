r'''
# `data_cloudflare_zero_trust_infrastructure_access_targets`

Refer to the Terraform Registry for docs: [`data_cloudflare_zero_trust_infrastructure_access_targets`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets).
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


class DataCloudflareZeroTrustInfrastructureAccessTargets(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargets",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets cloudflare_zero_trust_infrastructure_access_targets}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        created_after: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        hostname_contains: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        modified_after: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets cloudflare_zero_trust_infrastructure_access_targets} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#account_id DataCloudflareZeroTrustInfrastructureAccessTargets#account_id}
        :param created_after: A date and time after a target was created to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#created_after DataCloudflareZeroTrustInfrastructureAccessTargets#created_after}
        :param hostname: The hostname of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname DataCloudflareZeroTrustInfrastructureAccessTargets#hostname}
        :param hostname_contains: Partial match to the hostname of a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname_contains DataCloudflareZeroTrustInfrastructureAccessTargets#hostname_contains}
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        :param modified_after: A date and time after a target was modified to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#modified_after DataCloudflareZeroTrustInfrastructureAccessTargets#modified_after}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187c61c51fa833ac833e6c40658fecffd3220231367e3568da25fac4e1c1e369)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataCloudflareZeroTrustInfrastructureAccessTargetsConfig(
            account_id=account_id,
            created_after=created_after,
            hostname=hostname,
            hostname_contains=hostname_contains,
            ipv4=ipv4,
            ipv6=ipv6,
            modified_after=modified_after,
            virtual_network_id=virtual_network_id,
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
        '''Generates CDKTF code for importing a DataCloudflareZeroTrustInfrastructureAccessTargets resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataCloudflareZeroTrustInfrastructureAccessTargets to import.
        :param import_from_id: The id of the existing DataCloudflareZeroTrustInfrastructureAccessTargets that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataCloudflareZeroTrustInfrastructureAccessTargets to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b539e07cb23801e618971a0ad9e4f3a55bf1f06164bde4a7931a5e7a77919682)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCreatedAfter")
    def reset_created_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAfter", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetHostnameContains")
    def reset_hostname_contains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostnameContains", []))

    @jsii.member(jsii_name="resetIpv4")
    def reset_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @jsii.member(jsii_name="resetModifiedAfter")
    def reset_modified_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifiedAfter", []))

    @jsii.member(jsii_name="resetVirtualNetworkId")
    def reset_virtual_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkId", []))

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
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsList":
        return typing.cast("DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAfterInput")
    def created_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameContainsInput")
    def hostname_contains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameContainsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="modifiedAfterInput")
    def modified_after_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modifiedAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbde5f547f8b1e3ddd6714a4be25313b069b66b25811f71120cef6cc37a6fc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAfter")
    def created_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAfter"))

    @created_after.setter
    def created_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312e47ffedcf4eac19fe75eeefe3979a71c15139233f821e078338acd52760d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069d5c148405b78bbcf6db92aa7515dc0fa4c48aade8ec7c2322113778fc9ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnameContains")
    def hostname_contains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnameContains"))

    @hostname_contains.setter
    def hostname_contains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab31bb7710c633ebb791458656351adeb0b8c995dea462634878a3712ca97a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnameContains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4"))

    @ipv4.setter
    def ipv4(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ec9869aedde3b108796c6b5c6e1f08c847216a974080c60f6a8bf7dcae3b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6"))

    @ipv6.setter
    def ipv6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f054a77eb9310004208c2c112497f655600303288df1ab6a8618ea799a302f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modifiedAfter")
    def modified_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedAfter"))

    @modified_after.setter
    def modified_after(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d520c897e878608c48c9b77c9b5311f7054c6614acff729f7c39ec477b2c18aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modifiedAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde163bcb13b79b6258e6b4461a4e393fd64668f4be52fd5c9b4f5595b666e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsConfig",
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
        "created_after": "createdAfter",
        "hostname": "hostname",
        "hostname_contains": "hostnameContains",
        "ipv4": "ipv4",
        "ipv6": "ipv6",
        "modified_after": "modifiedAfter",
        "virtual_network_id": "virtualNetworkId",
    },
)
class DataCloudflareZeroTrustInfrastructureAccessTargetsConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        created_after: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        hostname_contains: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        modified_after: typing.Optional[builtins.str] = None,
        virtual_network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#account_id DataCloudflareZeroTrustInfrastructureAccessTargets#account_id}
        :param created_after: A date and time after a target was created to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#created_after DataCloudflareZeroTrustInfrastructureAccessTargets#created_after}
        :param hostname: The hostname of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname DataCloudflareZeroTrustInfrastructureAccessTargets#hostname}
        :param hostname_contains: Partial match to the hostname of a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname_contains DataCloudflareZeroTrustInfrastructureAccessTargets#hostname_contains}
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        :param modified_after: A date and time after a target was modified to filter on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#modified_after DataCloudflareZeroTrustInfrastructureAccessTargets#modified_after}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e759dbb71cb2106b941cc26d23a455af93c9af32fd93cf083e5b7eec1b85a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument created_after", value=created_after, expected_type=type_hints["created_after"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument hostname_contains", value=hostname_contains, expected_type=type_hints["hostname_contains"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument modified_after", value=modified_after, expected_type=type_hints["modified_after"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
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
        if created_after is not None:
            self._values["created_after"] = created_after
        if hostname is not None:
            self._values["hostname"] = hostname
        if hostname_contains is not None:
            self._values["hostname_contains"] = hostname_contains
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if modified_after is not None:
            self._values["modified_after"] = modified_after
        if virtual_network_id is not None:
            self._values["virtual_network_id"] = virtual_network_id

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#account_id DataCloudflareZeroTrustInfrastructureAccessTargets#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def created_after(self) -> typing.Optional[builtins.str]:
        '''A date and time after a target was created to filter on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#created_after DataCloudflareZeroTrustInfrastructureAccessTargets#created_after}
        '''
        result = self._values.get("created_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname of the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname DataCloudflareZeroTrustInfrastructureAccessTargets#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname_contains(self) -> typing.Optional[builtins.str]:
        '''Partial match to the hostname of a target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#hostname_contains DataCloudflareZeroTrustInfrastructureAccessTargets#hostname_contains}
        '''
        result = self._values.get("hostname_contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(self) -> typing.Optional[builtins.str]:
        '''The target's IPv4 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[builtins.str]:
        '''The target's IPv6 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modified_after(self) -> typing.Optional[builtins.str]:
        '''A date and time after a target was modified to filter on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#modified_after DataCloudflareZeroTrustInfrastructureAccessTargets#modified_after}
        '''
        result = self._values.get("modified_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> typing.Optional[builtins.str]:
        '''The private virtual network identifier for the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        result = self._values.get("virtual_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZeroTrustInfrastructureAccessTargetsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargets",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip"},
)
class DataCloudflareZeroTrustInfrastructureAccessTargetsTargets:
    def __init__(
        self,
        *,
        ip: typing.Union["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param ip: The IPv4/IPv6 address that identifies where to reach a target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip DataCloudflareZeroTrustInfrastructureAccessTargets#ip}
        '''
        if isinstance(ip, dict):
            ip = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp(**ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a37e069ce8f11ec5e86afc1b74823b7a05b642b882e667a6cf1493ab4456637)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip": ip,
        }

    @builtins.property
    def ip(self) -> "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp":
        '''The IPv4/IPv6 address that identifies where to reach a target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip DataCloudflareZeroTrustInfrastructureAccessTargets#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast("DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZeroTrustInfrastructureAccessTargetsTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp",
    jsii_struct_bases=[],
    name_mapping={"ipv4": "ipv4", "ipv6": "ipv6"},
)
class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp:
    def __init__(
        self,
        *,
        ipv4: typing.Optional[typing.Union["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        '''
        if isinstance(ipv4, dict):
            ipv4 = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4(**ipv4)
        if isinstance(ipv6, dict):
            ipv6 = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6(**ipv6)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfdce5b4f69c0f812e2c1ca0828321aeeddbbe0c058f731805652a4284026a4f)
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
    ) -> typing.Optional["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4"]:
        '''The target's IPv4 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4"], result)

    @builtins.property
    def ipv6(
        self,
    ) -> typing.Optional["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6"]:
        '''The target's IPv6 address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional["DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4",
    jsii_struct_bases=[],
    name_mapping={"ip_addr": "ipAddr", "virtual_network_id": "virtualNetworkId"},
)
class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4:
    def __init__(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787f1194a68f8afa7aece5fa26101b3d52687d65232218943acdccad57ac2ae2)
            check_type(argname="argument ip_addr", value=ip_addr, expected_type=type_hints["ip_addr"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_addr": ip_addr,
            "virtual_network_id": virtual_network_id,
        }

    @builtins.property
    def ip_addr(self) -> builtins.str:
        '''The IP address of the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        '''
        result = self._values.get("ip_addr")
        assert result is not None, "Required property 'ip_addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The private virtual network identifier for the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c394441705e5805e411c02419f72deab94e62a80074f219a1baccd762ffc0cf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9215f9350b313b8dc5de1c5b34a755386e95d332a5cc2b4b0c591b3e60a65109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1d7e44daed5e897396ad332116587712b3563ccaf627b1ba33c0cf01d6d89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b06d030ea937e5c37d05e67122cd229330037215a153545dceefd492d1077ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6",
    jsii_struct_bases=[],
    name_mapping={"ip_addr": "ipAddr", "virtual_network_id": "virtualNetworkId"},
)
class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6:
    def __init__(
        self,
        *,
        ip_addr: builtins.str,
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac9d672aafea907f72a9ee2239314ab0798e6b873644f278fa1b1e269e54311)
            check_type(argname="argument ip_addr", value=ip_addr, expected_type=type_hints["ip_addr"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_addr": ip_addr,
            "virtual_network_id": virtual_network_id,
        }

    @builtins.property
    def ip_addr(self) -> builtins.str:
        '''The IP address of the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        '''
        result = self._values.get("ip_addr")
        assert result is not None, "Required property 'ip_addr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The private virtual network identifier for the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88685a867c00959e91cde9f6a4bc155d1a20843641518926e2e678891a487bd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a963610b3cc0bd218be90a4bc31b88a07098d601d06fee9a97980ded19fa6609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b011b6a39f14ef3e802ea02cdbc9d583db60e2f5424c7a98e537420bd0e82af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5479ac0c84ca48775a106e61cea97a5f8a150133efadcd6be08ac0eb87b6acb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be4243f09947c8f3265b917190cbb9bb5489f2b8f0669c13269471237e756cee)
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
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        value = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4(
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
        :param ip_addr: The IP address of the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ip_addr DataCloudflareZeroTrustInfrastructureAccessTargets#ip_addr}
        :param virtual_network_id: The private virtual network identifier for the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#virtual_network_id DataCloudflareZeroTrustInfrastructureAccessTargets#virtual_network_id}
        '''
        value = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6(
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
    def ipv4(
        self,
    ) -> DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4OutputReference:
        return typing.cast(DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4OutputReference, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(
        self,
    ) -> DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6OutputReference:
        return typing.cast(DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6OutputReference, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp]:
        return typing.cast(typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3476bb2c6ede7b626035f36b047440fbd9259a5890fa286d267d1d83fa1f2af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fcc1dcf5e7d95872dc69beba712ee0e1430bc0336be69a5f7544d0c94fa0586)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c87c8e0b97114f5a67ceafe3a998cbbcd6a4ffc702bb719ebc711325070325)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21b73ebd1fa8ef225ee8d75d09a1e9b7c08fc8070230ff478d0dc0d4be3ae58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f14a06bf6ac2fbc0140b61daedc1fec968b733ed7a5582e9ede5d67c0da30d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87513eddf37fe342b95ee24d123d8bb5636bdb47bce2b6cd284adb2ce2cfafa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859eb0f4ef250bebe4eb0c3147d10ac11c327802b9fd8d719202bf206986a8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareZeroTrustInfrastructureAccessTargets.DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff506aa4c366fdd1f081094cb4feb95d0b3beb27ba398a5e18f1e0684e3f0e5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIp")
    def put_ip(
        self,
        *,
        ipv4: typing.Optional[typing.Union[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4, typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ipv4: The target's IPv4 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv4 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv4}
        :param ipv6: The target's IPv6 address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/data-sources/zero_trust_infrastructure_access_targets#ipv6 DataCloudflareZeroTrustInfrastructureAccessTargets#ipv6}
        '''
        value = DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp(
            ipv4=ipv4, ipv6=ipv6
        )

        return typing.cast(None, jsii.invoke(self, "putIp", [value]))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(
        self,
    ) -> DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpOutputReference:
        return typing.cast(DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpOutputReference, jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="modifiedAt")
    def modified_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(
        self,
    ) -> typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp]:
        return typing.cast(typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets]:
        return typing.cast(typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5468bb6ee677362c8fddd11d7ee353894657a87700083b2648709dd6a8a30b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataCloudflareZeroTrustInfrastructureAccessTargets",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsConfig",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargets",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4OutputReference",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6OutputReference",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpOutputReference",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsList",
    "DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsOutputReference",
]

publication.publish()

def _typecheckingstub__187c61c51fa833ac833e6c40658fecffd3220231367e3568da25fac4e1c1e369(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: builtins.str,
    created_after: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    hostname_contains: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    modified_after: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b539e07cb23801e618971a0ad9e4f3a55bf1f06164bde4a7931a5e7a77919682(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbde5f547f8b1e3ddd6714a4be25313b069b66b25811f71120cef6cc37a6fc21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312e47ffedcf4eac19fe75eeefe3979a71c15139233f821e078338acd52760d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069d5c148405b78bbcf6db92aa7515dc0fa4c48aade8ec7c2322113778fc9ebb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab31bb7710c633ebb791458656351adeb0b8c995dea462634878a3712ca97a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ec9869aedde3b108796c6b5c6e1f08c847216a974080c60f6a8bf7dcae3b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f054a77eb9310004208c2c112497f655600303288df1ab6a8618ea799a302f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d520c897e878608c48c9b77c9b5311f7054c6614acff729f7c39ec477b2c18aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde163bcb13b79b6258e6b4461a4e393fd64668f4be52fd5c9b4f5595b666e03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e759dbb71cb2106b941cc26d23a455af93c9af32fd93cf083e5b7eec1b85a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    created_after: typing.Optional[builtins.str] = None,
    hostname: typing.Optional[builtins.str] = None,
    hostname_contains: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    modified_after: typing.Optional[builtins.str] = None,
    virtual_network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a37e069ce8f11ec5e86afc1b74823b7a05b642b882e667a6cf1493ab4456637(
    *,
    ip: typing.Union[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfdce5b4f69c0f812e2c1ca0828321aeeddbbe0c058f731805652a4284026a4f(
    *,
    ipv4: typing.Optional[typing.Union[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4, typing.Dict[builtins.str, typing.Any]]] = None,
    ipv6: typing.Optional[typing.Union[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787f1194a68f8afa7aece5fa26101b3d52687d65232218943acdccad57ac2ae2(
    *,
    ip_addr: builtins.str,
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c394441705e5805e411c02419f72deab94e62a80074f219a1baccd762ffc0cf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9215f9350b313b8dc5de1c5b34a755386e95d332a5cc2b4b0c591b3e60a65109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1d7e44daed5e897396ad332116587712b3563ccaf627b1ba33c0cf01d6d89b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b06d030ea937e5c37d05e67122cd229330037215a153545dceefd492d1077ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv4]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac9d672aafea907f72a9ee2239314ab0798e6b873644f278fa1b1e269e54311(
    *,
    ip_addr: builtins.str,
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88685a867c00959e91cde9f6a4bc155d1a20843641518926e2e678891a487bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a963610b3cc0bd218be90a4bc31b88a07098d601d06fee9a97980ded19fa6609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b011b6a39f14ef3e802ea02cdbc9d583db60e2f5424c7a98e537420bd0e82af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5479ac0c84ca48775a106e61cea97a5f8a150133efadcd6be08ac0eb87b6acb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIpIpv6]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4243f09947c8f3265b917190cbb9bb5489f2b8f0669c13269471237e756cee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3476bb2c6ede7b626035f36b047440fbd9259a5890fa286d267d1d83fa1f2af9(
    value: typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargetsIp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcc1dcf5e7d95872dc69beba712ee0e1430bc0336be69a5f7544d0c94fa0586(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c87c8e0b97114f5a67ceafe3a998cbbcd6a4ffc702bb719ebc711325070325(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21b73ebd1fa8ef225ee8d75d09a1e9b7c08fc8070230ff478d0dc0d4be3ae58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f14a06bf6ac2fbc0140b61daedc1fec968b733ed7a5582e9ede5d67c0da30d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87513eddf37fe342b95ee24d123d8bb5636bdb47bce2b6cd284adb2ce2cfafa8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859eb0f4ef250bebe4eb0c3147d10ac11c327802b9fd8d719202bf206986a8f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff506aa4c366fdd1f081094cb4feb95d0b3beb27ba398a5e18f1e0684e3f0e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5468bb6ee677362c8fddd11d7ee353894657a87700083b2648709dd6a8a30b4(
    value: typing.Optional[DataCloudflareZeroTrustInfrastructureAccessTargetsTargets],
) -> None:
    """Type checking stubs"""
    pass
