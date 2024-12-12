r'''
# `cloudflare_access_identity_provider`

Refer to the Terraform Registry for docs: [`cloudflare_access_identity_provider`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider).
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


class AccessIdentityProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider cloudflare_access_identity_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderConfigA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderScimConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider cloudflare_access_identity_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Friendly name of the Access Identity Provider configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#name AccessIdentityProvider#name}
        :param type: The provider type to use. Available values: ``azureAD``, ``centrify``, ``facebook``, ``github``, ``google``, ``google-apps``, ``linkedin``, ``oidc``, ``okta``, ``onelogin``, ``onetimepin``, ``pingone``, ``saml``, ``yandex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#type AccessIdentityProvider#type}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#account_id AccessIdentityProvider#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#config AccessIdentityProvider#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#id AccessIdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#scim_config AccessIdentityProvider#scim_config}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#zone_id AccessIdentityProvider#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0511d522af9e5a5c13f822ada949d0b49e569cfc45b219d7be73fd0c54682fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = AccessIdentityProviderConfig(
            name=name,
            type=type,
            account_id=account_id,
            config=config,
            id=id,
            scim_config=scim_config,
            zone_id=zone_id,
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
        '''Generates CDKTF code for importing a AccessIdentityProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessIdentityProvider to import.
        :param import_from_id: The id of the existing AccessIdentityProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessIdentityProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d28422728d30daa9c495330d6c95f9dc5b63328f50735cb3b2d4648b5f1ac80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderConfigA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247d658a04cc00d779af7489a06e49168a2c166c79ecec1b77145122aa1ca42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putScimConfig")
    def put_scim_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderScimConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4b531c60d279cd875d2b58f85fae8840cc1c238b59bfa82dc513cd1f2f18de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScimConfig", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScimConfig")
    def reset_scim_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScimConfig", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

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
    def config(self) -> "AccessIdentityProviderConfigAList":
        return typing.cast("AccessIdentityProviderConfigAList", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="scimConfig")
    def scim_config(self) -> "AccessIdentityProviderScimConfigList":
        return typing.cast("AccessIdentityProviderScimConfigList", jsii.get(self, "scimConfig"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderConfigA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderConfigA"]]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scimConfigInput")
    def scim_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderScimConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderScimConfig"]]], jsii.get(self, "scimConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0db011d6866b2b9a78c14342821ee60aed0ced616161fb4cd11cd780bab3d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3003c698495eddf638f8f69b32d9cf96810c3e3cbd2d59d80fef8a595c7cada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57af66b8069078a548a9b8fc014229015a2625ae5a93ca06de4e325d24d88937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a18887db6d76fde870ce49b1196ded6cb30373d27d121a06e229acccd5df80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf1b341bcef10e8c53b101d9adb8c27d0194055549fcd920b6e8749cc21d6b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "type": "type",
        "account_id": "accountId",
        "config": "config",
        "id": "id",
        "scim_config": "scimConfig",
        "zone_id": "zoneId",
    },
)
class AccessIdentityProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        type: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderConfigA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessIdentityProviderScimConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Friendly name of the Access Identity Provider configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#name AccessIdentityProvider#name}
        :param type: The provider type to use. Available values: ``azureAD``, ``centrify``, ``facebook``, ``github``, ``google``, ``google-apps``, ``linkedin``, ``oidc``, ``okta``, ``onelogin``, ``onetimepin``, ``pingone``, ``saml``, ``yandex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#type AccessIdentityProvider#type}
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#account_id AccessIdentityProvider#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#config AccessIdentityProvider#config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#id AccessIdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#scim_config AccessIdentityProvider#scim_config}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#zone_id AccessIdentityProvider#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63145cceee3960d5b0fbc5fbdfe48175ae412c31de198914d1454b2416f45997)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scim_config", value=scim_config, expected_type=type_hints["scim_config"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
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
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id
        if scim_config is not None:
            self._values["scim_config"] = scim_config
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
    def name(self) -> builtins.str:
        '''Friendly name of the Access Identity Provider configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#name AccessIdentityProvider#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The provider type to use.

        Available values: ``azureAD``, ``centrify``, ``facebook``, ``github``, ``google``, ``google-apps``, ``linkedin``, ``oidc``, ``okta``, ``onelogin``, ``onetimepin``, ``pingone``, ``saml``, ``yandex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#type AccessIdentityProvider#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource.

        Conflicts with ``zone_id``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#account_id AccessIdentityProvider#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderConfigA"]]]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#config AccessIdentityProvider#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderConfigA"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#id AccessIdentityProvider#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scim_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderScimConfig"]]]:
        '''scim_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#scim_config AccessIdentityProvider#scim_config}
        '''
        result = self._values.get("scim_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessIdentityProviderScimConfig"]]], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource.

        Conflicts with ``account_id``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#zone_id AccessIdentityProvider#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessIdentityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "api_token": "apiToken",
        "apps_domain": "appsDomain",
        "attributes": "attributes",
        "authorization_server_id": "authorizationServerId",
        "auth_url": "authUrl",
        "centrify_account": "centrifyAccount",
        "centrify_app_id": "centrifyAppId",
        "certs_url": "certsUrl",
        "claims": "claims",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "conditional_access_enabled": "conditionalAccessEnabled",
        "directory_id": "directoryId",
        "email_attribute_name": "emailAttributeName",
        "email_claim_name": "emailClaimName",
        "idp_public_cert": "idpPublicCert",
        "issuer_url": "issuerUrl",
        "okta_account": "oktaAccount",
        "onelogin_account": "oneloginAccount",
        "ping_env_id": "pingEnvId",
        "pkce_enabled": "pkceEnabled",
        "scopes": "scopes",
        "sign_request": "signRequest",
        "sso_target_url": "ssoTargetUrl",
        "support_groups": "supportGroups",
        "token_url": "tokenUrl",
    },
)
class AccessIdentityProviderConfigA:
    def __init__(
        self,
        *,
        api_token: typing.Optional[builtins.str] = None,
        apps_domain: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorization_server_id: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        centrify_account: typing.Optional[builtins.str] = None,
        centrify_app_id: typing.Optional[builtins.str] = None,
        certs_url: typing.Optional[builtins.str] = None,
        claims: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        conditional_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        directory_id: typing.Optional[builtins.str] = None,
        email_attribute_name: typing.Optional[builtins.str] = None,
        email_claim_name: typing.Optional[builtins.str] = None,
        idp_public_cert: typing.Optional[builtins.str] = None,
        issuer_url: typing.Optional[builtins.str] = None,
        okta_account: typing.Optional[builtins.str] = None,
        onelogin_account: typing.Optional[builtins.str] = None,
        ping_env_id: typing.Optional[builtins.str] = None,
        pkce_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sso_target_url: typing.Optional[builtins.str] = None,
        support_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#api_token AccessIdentityProvider#api_token}.
        :param apps_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#apps_domain AccessIdentityProvider#apps_domain}.
        :param attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#attributes AccessIdentityProvider#attributes}.
        :param authorization_server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#authorization_server_id AccessIdentityProvider#authorization_server_id}.
        :param auth_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#auth_url AccessIdentityProvider#auth_url}.
        :param centrify_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#centrify_account AccessIdentityProvider#centrify_account}.
        :param centrify_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#centrify_app_id AccessIdentityProvider#centrify_app_id}.
        :param certs_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#certs_url AccessIdentityProvider#certs_url}.
        :param claims: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#claims AccessIdentityProvider#claims}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#client_id AccessIdentityProvider#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#client_secret AccessIdentityProvider#client_secret}.
        :param conditional_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#conditional_access_enabled AccessIdentityProvider#conditional_access_enabled}.
        :param directory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#directory_id AccessIdentityProvider#directory_id}.
        :param email_attribute_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#email_attribute_name AccessIdentityProvider#email_attribute_name}.
        :param email_claim_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#email_claim_name AccessIdentityProvider#email_claim_name}.
        :param idp_public_cert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#idp_public_cert AccessIdentityProvider#idp_public_cert}.
        :param issuer_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#issuer_url AccessIdentityProvider#issuer_url}.
        :param okta_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#okta_account AccessIdentityProvider#okta_account}.
        :param onelogin_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#onelogin_account AccessIdentityProvider#onelogin_account}.
        :param ping_env_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#ping_env_id AccessIdentityProvider#ping_env_id}.
        :param pkce_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#pkce_enabled AccessIdentityProvider#pkce_enabled}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#scopes AccessIdentityProvider#scopes}.
        :param sign_request: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#sign_request AccessIdentityProvider#sign_request}.
        :param sso_target_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#sso_target_url AccessIdentityProvider#sso_target_url}.
        :param support_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#support_groups AccessIdentityProvider#support_groups}.
        :param token_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#token_url AccessIdentityProvider#token_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8b84c002a8e2e3c953f7112a728d977b489f5a381c59189e3f001c31af9a4a)
            check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
            check_type(argname="argument apps_domain", value=apps_domain, expected_type=type_hints["apps_domain"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument authorization_server_id", value=authorization_server_id, expected_type=type_hints["authorization_server_id"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument centrify_account", value=centrify_account, expected_type=type_hints["centrify_account"])
            check_type(argname="argument centrify_app_id", value=centrify_app_id, expected_type=type_hints["centrify_app_id"])
            check_type(argname="argument certs_url", value=certs_url, expected_type=type_hints["certs_url"])
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument conditional_access_enabled", value=conditional_access_enabled, expected_type=type_hints["conditional_access_enabled"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument email_attribute_name", value=email_attribute_name, expected_type=type_hints["email_attribute_name"])
            check_type(argname="argument email_claim_name", value=email_claim_name, expected_type=type_hints["email_claim_name"])
            check_type(argname="argument idp_public_cert", value=idp_public_cert, expected_type=type_hints["idp_public_cert"])
            check_type(argname="argument issuer_url", value=issuer_url, expected_type=type_hints["issuer_url"])
            check_type(argname="argument okta_account", value=okta_account, expected_type=type_hints["okta_account"])
            check_type(argname="argument onelogin_account", value=onelogin_account, expected_type=type_hints["onelogin_account"])
            check_type(argname="argument ping_env_id", value=ping_env_id, expected_type=type_hints["ping_env_id"])
            check_type(argname="argument pkce_enabled", value=pkce_enabled, expected_type=type_hints["pkce_enabled"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument sign_request", value=sign_request, expected_type=type_hints["sign_request"])
            check_type(argname="argument sso_target_url", value=sso_target_url, expected_type=type_hints["sso_target_url"])
            check_type(argname="argument support_groups", value=support_groups, expected_type=type_hints["support_groups"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_token is not None:
            self._values["api_token"] = api_token
        if apps_domain is not None:
            self._values["apps_domain"] = apps_domain
        if attributes is not None:
            self._values["attributes"] = attributes
        if authorization_server_id is not None:
            self._values["authorization_server_id"] = authorization_server_id
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if centrify_account is not None:
            self._values["centrify_account"] = centrify_account
        if centrify_app_id is not None:
            self._values["centrify_app_id"] = centrify_app_id
        if certs_url is not None:
            self._values["certs_url"] = certs_url
        if claims is not None:
            self._values["claims"] = claims
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if conditional_access_enabled is not None:
            self._values["conditional_access_enabled"] = conditional_access_enabled
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if email_attribute_name is not None:
            self._values["email_attribute_name"] = email_attribute_name
        if email_claim_name is not None:
            self._values["email_claim_name"] = email_claim_name
        if idp_public_cert is not None:
            self._values["idp_public_cert"] = idp_public_cert
        if issuer_url is not None:
            self._values["issuer_url"] = issuer_url
        if okta_account is not None:
            self._values["okta_account"] = okta_account
        if onelogin_account is not None:
            self._values["onelogin_account"] = onelogin_account
        if ping_env_id is not None:
            self._values["ping_env_id"] = ping_env_id
        if pkce_enabled is not None:
            self._values["pkce_enabled"] = pkce_enabled
        if scopes is not None:
            self._values["scopes"] = scopes
        if sign_request is not None:
            self._values["sign_request"] = sign_request
        if sso_target_url is not None:
            self._values["sso_target_url"] = sso_target_url
        if support_groups is not None:
            self._values["support_groups"] = support_groups
        if token_url is not None:
            self._values["token_url"] = token_url

    @builtins.property
    def api_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#api_token AccessIdentityProvider#api_token}.'''
        result = self._values.get("api_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apps_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#apps_domain AccessIdentityProvider#apps_domain}.'''
        result = self._values.get("apps_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#attributes AccessIdentityProvider#attributes}.'''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorization_server_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#authorization_server_id AccessIdentityProvider#authorization_server_id}.'''
        result = self._values.get("authorization_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#auth_url AccessIdentityProvider#auth_url}.'''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def centrify_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#centrify_account AccessIdentityProvider#centrify_account}.'''
        result = self._values.get("centrify_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def centrify_app_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#centrify_app_id AccessIdentityProvider#centrify_app_id}.'''
        result = self._values.get("centrify_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certs_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#certs_url AccessIdentityProvider#certs_url}.'''
        result = self._values.get("certs_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def claims(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#claims AccessIdentityProvider#claims}.'''
        result = self._values.get("claims")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#client_id AccessIdentityProvider#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#client_secret AccessIdentityProvider#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conditional_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#conditional_access_enabled AccessIdentityProvider#conditional_access_enabled}.'''
        result = self._values.get("conditional_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#directory_id AccessIdentityProvider#directory_id}.'''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_attribute_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#email_attribute_name AccessIdentityProvider#email_attribute_name}.'''
        result = self._values.get("email_attribute_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_claim_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#email_claim_name AccessIdentityProvider#email_claim_name}.'''
        result = self._values.get("email_claim_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_public_cert(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#idp_public_cert AccessIdentityProvider#idp_public_cert}.'''
        result = self._values.get("idp_public_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#issuer_url AccessIdentityProvider#issuer_url}.'''
        result = self._values.get("issuer_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def okta_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#okta_account AccessIdentityProvider#okta_account}.'''
        result = self._values.get("okta_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def onelogin_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#onelogin_account AccessIdentityProvider#onelogin_account}.'''
        result = self._values.get("onelogin_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ping_env_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#ping_env_id AccessIdentityProvider#ping_env_id}.'''
        result = self._values.get("ping_env_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pkce_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#pkce_enabled AccessIdentityProvider#pkce_enabled}.'''
        result = self._values.get("pkce_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#scopes AccessIdentityProvider#scopes}.'''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sign_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#sign_request AccessIdentityProvider#sign_request}.'''
        result = self._values.get("sign_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sso_target_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#sso_target_url AccessIdentityProvider#sso_target_url}.'''
        result = self._values.get("sso_target_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#support_groups AccessIdentityProvider#support_groups}.'''
        result = self._values.get("support_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#token_url AccessIdentityProvider#token_url}.'''
        result = self._values.get("token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessIdentityProviderConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessIdentityProviderConfigAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderConfigAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eacdf7b146ba5a3f2385060d849de891a24a43876750b774ee7537df3c93653c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessIdentityProviderConfigAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce5c59612bf675c69c74ff2f7303c7dbf7e99571f7353504c410e8c108511e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessIdentityProviderConfigAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c35d35b1ecbc8f765cc12e6038f282b80ee2f27d2d6ccc747e92b2d6b1de12f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60a427eb0fac54c7a82edef0147e3cd2790eee9d4f3d98b0380b63f397cdd24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9139436bd81a85c0d38cffe8182713de5252f7200f3baaa377b76364f1441083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderConfigA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderConfigA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderConfigA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f0a8f35971a001eae7b24cd8985a4b020703bc4f21645f25f4c526dc7c2d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessIdentityProviderConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f611c08da2cf40f717c8203adda96d7263ccd15b04ab3d9d6962feffc98aef26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetApiToken")
    def reset_api_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiToken", []))

    @jsii.member(jsii_name="resetAppsDomain")
    def reset_apps_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppsDomain", []))

    @jsii.member(jsii_name="resetAttributes")
    def reset_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributes", []))

    @jsii.member(jsii_name="resetAuthorizationServerId")
    def reset_authorization_server_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationServerId", []))

    @jsii.member(jsii_name="resetAuthUrl")
    def reset_auth_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUrl", []))

    @jsii.member(jsii_name="resetCentrifyAccount")
    def reset_centrify_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCentrifyAccount", []))

    @jsii.member(jsii_name="resetCentrifyAppId")
    def reset_centrify_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCentrifyAppId", []))

    @jsii.member(jsii_name="resetCertsUrl")
    def reset_certs_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertsUrl", []))

    @jsii.member(jsii_name="resetClaims")
    def reset_claims(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaims", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetConditionalAccessEnabled")
    def reset_conditional_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalAccessEnabled", []))

    @jsii.member(jsii_name="resetDirectoryId")
    def reset_directory_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryId", []))

    @jsii.member(jsii_name="resetEmailAttributeName")
    def reset_email_attribute_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAttributeName", []))

    @jsii.member(jsii_name="resetEmailClaimName")
    def reset_email_claim_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailClaimName", []))

    @jsii.member(jsii_name="resetIdpPublicCert")
    def reset_idp_public_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdpPublicCert", []))

    @jsii.member(jsii_name="resetIssuerUrl")
    def reset_issuer_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerUrl", []))

    @jsii.member(jsii_name="resetOktaAccount")
    def reset_okta_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaAccount", []))

    @jsii.member(jsii_name="resetOneloginAccount")
    def reset_onelogin_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneloginAccount", []))

    @jsii.member(jsii_name="resetPingEnvId")
    def reset_ping_env_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPingEnvId", []))

    @jsii.member(jsii_name="resetPkceEnabled")
    def reset_pkce_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPkceEnabled", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSignRequest")
    def reset_sign_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignRequest", []))

    @jsii.member(jsii_name="resetSsoTargetUrl")
    def reset_sso_target_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoTargetUrl", []))

    @jsii.member(jsii_name="resetSupportGroups")
    def reset_support_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportGroups", []))

    @jsii.member(jsii_name="resetTokenUrl")
    def reset_token_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenUrl", []))

    @builtins.property
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUrl"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenInput")
    def api_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="appsDomainInput")
    def apps_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appsDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="attributesInput")
    def attributes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "attributesInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationServerIdInput")
    def authorization_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="centrifyAccountInput")
    def centrify_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "centrifyAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="centrifyAppIdInput")
    def centrify_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "centrifyAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certsUrlInput")
    def certs_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certsUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="claimsInput")
    def claims_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "claimsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionalAccessEnabledInput")
    def conditional_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "conditionalAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryIdInput")
    def directory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAttributeNameInput")
    def email_attribute_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAttributeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailClaimNameInput")
    def email_claim_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailClaimNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idpPublicCertInput")
    def idp_public_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpPublicCertInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUrlInput")
    def issuer_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaAccountInput")
    def okta_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oktaAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="oneloginAccountInput")
    def onelogin_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oneloginAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="pingEnvIdInput")
    def ping_env_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pingEnvIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pkceEnabledInput")
    def pkce_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pkceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="signRequestInput")
    def sign_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "signRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoTargetUrlInput")
    def sso_target_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoTargetUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="supportGroupsInput")
    def support_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="apiToken")
    def api_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiToken"))

    @api_token.setter
    def api_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdd819677ac2ef1ffd200e93167903a2ac56f2533741b96b50729b2ea003311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appsDomain")
    def apps_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appsDomain"))

    @apps_domain.setter
    def apps_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0aacd4a7fb36af04a53d5ba78286dcadfe026223a57f4bea89c99cb40057b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appsDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4a7b3a600ac07b157d5ef45ce249ae23678b1c125b3232f3bee0cfb09d493f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizationServerId")
    def authorization_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationServerId"))

    @authorization_server_id.setter
    def authorization_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ac4c005287458766feba63121a29694d270cd15924c2f83bb4c1b07aac6636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationServerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d285d55eecaf697663bb1c44b6ccc8f8b08c5593f2b861f9e451821da1b5378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="centrifyAccount")
    def centrify_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "centrifyAccount"))

    @centrify_account.setter
    def centrify_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1386bd3de482ad6b2cb6efd1c300b34f8425bbcb96554084c3231642b9fcdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "centrifyAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="centrifyAppId")
    def centrify_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "centrifyAppId"))

    @centrify_app_id.setter
    def centrify_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b224e258b50e2c3d31be275f34af7520e124abf2562b6e2b6d347c82dbb8bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "centrifyAppId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certsUrl")
    def certs_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certsUrl"))

    @certs_url.setter
    def certs_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b6240d23d0fb04e1d3c6d33936f26bd98e365665bd280c658a62da9be8540b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certsUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "claims"))

    @claims.setter
    def claims(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8becded23f9b521396eb1fb0777e374e32106bd818961864bf866116f4a820c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "claims", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19001a71ceb4807ee9a0838a5344d196b4fc73dc44e91a3a7fa3d4a7feb09dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4f6b10ff7034eed22ad18f8f3c06dc96c93f27b2e738a13660d5d512a5fdac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conditionalAccessEnabled")
    def conditional_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "conditionalAccessEnabled"))

    @conditional_access_enabled.setter
    def conditional_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261b40a42b2544fda5e24516551dd6be8e75baceac74f7fdfb125c68cd285b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionalAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b45fa540e095811dce0b49258d82fb1ab0d0f7e5c0c12a57b4c1859e7646cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAttributeName")
    def email_attribute_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAttributeName"))

    @email_attribute_name.setter
    def email_attribute_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88e8fe7bc4613ca6f912715db7b2799f2e3bca08d37ca218d9c9e80f8cdb709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAttributeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailClaimName")
    def email_claim_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailClaimName"))

    @email_claim_name.setter
    def email_claim_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d90962e38503e724893d9e03eefae943484c6d133a297c7bf84b8aeb026c20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailClaimName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idpPublicCert")
    def idp_public_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpPublicCert"))

    @idp_public_cert.setter
    def idp_public_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd32c32c428ae6e7896cbc6da9a62efab011c3b2919b91ba01e3a0a54a3ab0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpPublicCert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuerUrl")
    def issuer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUrl"))

    @issuer_url.setter
    def issuer_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6f58d6c579c8177ae47664179d0f509681cc3a6daad75bb2b7aabf49236ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oktaAccount")
    def okta_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oktaAccount"))

    @okta_account.setter
    def okta_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58529923ff7f8403da57b8234929236d62c9e682db49895b8d0c9ef3f17e72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oneloginAccount")
    def onelogin_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oneloginAccount"))

    @onelogin_account.setter
    def onelogin_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb912ecfcb1ad2add394e799f7835e88d16b2eac036fef5240a1701ac2d7b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oneloginAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pingEnvId")
    def ping_env_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pingEnvId"))

    @ping_env_id.setter
    def ping_env_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e733a2f598f3a380406ad8a62af53134c4ab0403c8afc2b673350ff1e6db6ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pingEnvId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pkceEnabled")
    def pkce_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pkceEnabled"))

    @pkce_enabled.setter
    def pkce_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342c0be76609369b109ebbe1b02c356e074c14818b367ca8801a6d23b04ee9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pkceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d545a6d4d2b88fc22226d937d0bc9ed0795137c3a1e7889d469fd706b331e162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signRequest")
    def sign_request(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "signRequest"))

    @sign_request.setter
    def sign_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2c05a266367cb468a45deaba097175d9771f504172f5f38a1494dd4fc056ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoTargetUrl")
    def sso_target_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoTargetUrl"))

    @sso_target_url.setter
    def sso_target_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec473bb87f0e6756359ded98b43b3a3c9233a5734db350cc155c4efc8491b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoTargetUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportGroups")
    def support_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportGroups"))

    @support_groups.setter
    def support_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5925bed764006d4ec82dd63d17f6bb68bed472e7b77e1b389c6252f72bad6933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f6c4f874bbb4a3029bdc680f2c3c2107a6da2a44122793fdbd9fd52ff2ac63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderConfigA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderConfigA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderConfigA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__925edd4c80cf487756d167d7b24b4e77760ea53ad556bfb6e018bc865a726629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderScimConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "group_member_deprovision": "groupMemberDeprovision",
        "identity_update_behavior": "identityUpdateBehavior",
        "seat_deprovision": "seatDeprovision",
        "secret": "secret",
        "user_deprovision": "userDeprovision",
    },
)
class AccessIdentityProviderScimConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_member_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        identity_update_behavior: typing.Optional[builtins.str] = None,
        seat_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secret: typing.Optional[builtins.str] = None,
        user_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: A flag to enable or disable SCIM for the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#enabled AccessIdentityProvider#enabled}
        :param group_member_deprovision: Deprecated. Use ``identity_update_behavior``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#group_member_deprovision AccessIdentityProvider#group_member_deprovision}
        :param identity_update_behavior: Indicates how a SCIM event updates a user identity used for policy evaluation. Use "automatic" to automatically update a user's identity and augment it with fields from the SCIM user resource. Use "reauth" to force re-authentication on group membership updates, user identity update will only occur after successful re-authentication. With "reauth" identities will not contain fields from the SCIM user resource. With "no_action" identities will not be changed by SCIM updates in any way and users will not be prompted to reauthenticate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#identity_update_behavior AccessIdentityProvider#identity_update_behavior}
        :param seat_deprovision: A flag to remove a user's seat in Zero Trust when they have been deprovisioned in the Identity Provider. This cannot be enabled unless user_deprovision is also enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#seat_deprovision AccessIdentityProvider#seat_deprovision}
        :param secret: A read-only token generated when the SCIM integration is enabled for the first time. It is redacted on subsequent requests. If you lose this you will need to refresh it token at /access/identity_providers/:idpID/refresh_scim_secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#secret AccessIdentityProvider#secret}
        :param user_deprovision: A flag to enable revoking a user's session in Access and Gateway when they have been deprovisioned in the Identity Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#user_deprovision AccessIdentityProvider#user_deprovision}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e631c279b0bb454bf6e928afb3575b1c678683f997a52731a029edaa8b4e22)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument group_member_deprovision", value=group_member_deprovision, expected_type=type_hints["group_member_deprovision"])
            check_type(argname="argument identity_update_behavior", value=identity_update_behavior, expected_type=type_hints["identity_update_behavior"])
            check_type(argname="argument seat_deprovision", value=seat_deprovision, expected_type=type_hints["seat_deprovision"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument user_deprovision", value=user_deprovision, expected_type=type_hints["user_deprovision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if group_member_deprovision is not None:
            self._values["group_member_deprovision"] = group_member_deprovision
        if identity_update_behavior is not None:
            self._values["identity_update_behavior"] = identity_update_behavior
        if seat_deprovision is not None:
            self._values["seat_deprovision"] = seat_deprovision
        if secret is not None:
            self._values["secret"] = secret
        if user_deprovision is not None:
            self._values["user_deprovision"] = user_deprovision

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag to enable or disable SCIM for the identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#enabled AccessIdentityProvider#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_member_deprovision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Deprecated. Use ``identity_update_behavior``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#group_member_deprovision AccessIdentityProvider#group_member_deprovision}
        '''
        result = self._values.get("group_member_deprovision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def identity_update_behavior(self) -> typing.Optional[builtins.str]:
        '''Indicates how a SCIM event updates a user identity used for policy evaluation.

        Use "automatic" to automatically update a user's identity and augment it with fields from the SCIM user resource. Use "reauth" to force re-authentication on group membership updates, user identity update will only occur after successful re-authentication. With "reauth" identities will not contain fields from the SCIM user resource. With "no_action" identities will not be changed by SCIM updates in any way and users will not be prompted to reauthenticate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#identity_update_behavior AccessIdentityProvider#identity_update_behavior}
        '''
        result = self._values.get("identity_update_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def seat_deprovision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag to remove a user's seat in Zero Trust when they have been deprovisioned in the Identity Provider.

        This cannot be enabled unless user_deprovision is also enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#seat_deprovision AccessIdentityProvider#seat_deprovision}
        '''
        result = self._values.get("seat_deprovision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''A read-only token generated when the SCIM integration is enabled for the first time.

        It is redacted on subsequent requests.  If you lose this you will need to refresh it token at /access/identity_providers/:idpID/refresh_scim_secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#secret AccessIdentityProvider#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_deprovision(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag to enable revoking a user's session in Access and Gateway when they have been deprovisioned in the Identity Provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_identity_provider#user_deprovision AccessIdentityProvider#user_deprovision}
        '''
        result = self._values.get("user_deprovision")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessIdentityProviderScimConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessIdentityProviderScimConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderScimConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c057f63e362b90afb1d2e760c971523ef608970739b4361b26adc86bbf4d94e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessIdentityProviderScimConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e81bb2d985434b92ede2bcd7abf7aa2a64259d8d8130f38dd07358f6f400ad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessIdentityProviderScimConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80be433ae05be650ef4f9a82e13ec499b4084ad4ec0dd54a4479f297bd443bb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d70ae993a1224ccc35f7d599807ac9390d7f676fa66e9f51a0f0bd59f009a64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88358ada0776fc0071837ab23b8565ded4c33df74964cd6e02bb46a06363d2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderScimConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderScimConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderScimConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9884353aa215dc55b6f3f35e6a32653e5cb3aa6d4a04aa3c4a2bbbc7fd0d1224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessIdentityProviderScimConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessIdentityProvider.AccessIdentityProviderScimConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__377dee8c91792a5f8d93d272183fb2ac1971eea00a6290278a0287f5e057dc59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetGroupMemberDeprovision")
    def reset_group_member_deprovision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupMemberDeprovision", []))

    @jsii.member(jsii_name="resetIdentityUpdateBehavior")
    def reset_identity_update_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityUpdateBehavior", []))

    @jsii.member(jsii_name="resetSeatDeprovision")
    def reset_seat_deprovision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeatDeprovision", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="resetUserDeprovision")
    def reset_user_deprovision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDeprovision", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="groupMemberDeprovisionInput")
    def group_member_deprovision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupMemberDeprovisionInput"))

    @builtins.property
    @jsii.member(jsii_name="identityUpdateBehaviorInput")
    def identity_update_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityUpdateBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="seatDeprovisionInput")
    def seat_deprovision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "seatDeprovisionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="userDeprovisionInput")
    def user_deprovision_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userDeprovisionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4546d8636469d45aaec91212ae2f9f1f6c0872318ee29e544dc032893cd1d4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupMemberDeprovision")
    def group_member_deprovision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupMemberDeprovision"))

    @group_member_deprovision.setter
    def group_member_deprovision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a87033ec33e0b36f123366df181ebc00779078256961d5d95df55cd4b9a8c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupMemberDeprovision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityUpdateBehavior")
    def identity_update_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityUpdateBehavior"))

    @identity_update_behavior.setter
    def identity_update_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1247c3ef8210ad41e479a9262422f2ccbb50f9b2d420746c86119d4366dedc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityUpdateBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seatDeprovision")
    def seat_deprovision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "seatDeprovision"))

    @seat_deprovision.setter
    def seat_deprovision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8615d2b92a9864f26056e35ec4e7b5696d58a8d588784afc87d4339b2990df4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seatDeprovision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b74cdbd8bda2d31a00c608265fc3c09772820fffd49d629ac7ea99ba394c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDeprovision")
    def user_deprovision(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userDeprovision"))

    @user_deprovision.setter
    def user_deprovision(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698fa44216082a4088d47fc8e32ee80d4f265a7fc317173386b4499cb4f60bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDeprovision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderScimConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderScimConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderScimConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4545594c586c824ab538c9023eab68a13304fd0168e6493d5eaefeb2123d80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessIdentityProvider",
    "AccessIdentityProviderConfig",
    "AccessIdentityProviderConfigA",
    "AccessIdentityProviderConfigAList",
    "AccessIdentityProviderConfigAOutputReference",
    "AccessIdentityProviderScimConfig",
    "AccessIdentityProviderScimConfigList",
    "AccessIdentityProviderScimConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d0511d522af9e5a5c13f822ada949d0b49e569cfc45b219d7be73fd0c54682fe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderConfigA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderScimConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4d28422728d30daa9c495330d6c95f9dc5b63328f50735cb3b2d4648b5f1ac80(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247d658a04cc00d779af7489a06e49168a2c166c79ecec1b77145122aa1ca42a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderConfigA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4b531c60d279cd875d2b58f85fae8840cc1c238b59bfa82dc513cd1f2f18de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderScimConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0db011d6866b2b9a78c14342821ee60aed0ced616161fb4cd11cd780bab3d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3003c698495eddf638f8f69b32d9cf96810c3e3cbd2d59d80fef8a595c7cada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57af66b8069078a548a9b8fc014229015a2625ae5a93ca06de4e325d24d88937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a18887db6d76fde870ce49b1196ded6cb30373d27d121a06e229acccd5df80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf1b341bcef10e8c53b101d9adb8c27d0194055549fcd920b6e8749cc21d6b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63145cceee3960d5b0fbc5fbdfe48175ae412c31de198914d1454b2416f45997(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderConfigA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessIdentityProviderScimConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8b84c002a8e2e3c953f7112a728d977b489f5a381c59189e3f001c31af9a4a(
    *,
    api_token: typing.Optional[builtins.str] = None,
    apps_domain: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorization_server_id: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    centrify_account: typing.Optional[builtins.str] = None,
    centrify_app_id: typing.Optional[builtins.str] = None,
    certs_url: typing.Optional[builtins.str] = None,
    claims: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    conditional_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    email_attribute_name: typing.Optional[builtins.str] = None,
    email_claim_name: typing.Optional[builtins.str] = None,
    idp_public_cert: typing.Optional[builtins.str] = None,
    issuer_url: typing.Optional[builtins.str] = None,
    okta_account: typing.Optional[builtins.str] = None,
    onelogin_account: typing.Optional[builtins.str] = None,
    ping_env_id: typing.Optional[builtins.str] = None,
    pkce_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    sign_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sso_target_url: typing.Optional[builtins.str] = None,
    support_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacdf7b146ba5a3f2385060d849de891a24a43876750b774ee7537df3c93653c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce5c59612bf675c69c74ff2f7303c7dbf7e99571f7353504c410e8c108511e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c35d35b1ecbc8f765cc12e6038f282b80ee2f27d2d6ccc747e92b2d6b1de12f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60a427eb0fac54c7a82edef0147e3cd2790eee9d4f3d98b0380b63f397cdd24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9139436bd81a85c0d38cffe8182713de5252f7200f3baaa377b76364f1441083(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f0a8f35971a001eae7b24cd8985a4b020703bc4f21645f25f4c526dc7c2d70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderConfigA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f611c08da2cf40f717c8203adda96d7263ccd15b04ab3d9d6962feffc98aef26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdd819677ac2ef1ffd200e93167903a2ac56f2533741b96b50729b2ea003311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0aacd4a7fb36af04a53d5ba78286dcadfe026223a57f4bea89c99cb40057b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4a7b3a600ac07b157d5ef45ce249ae23678b1c125b3232f3bee0cfb09d493f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ac4c005287458766feba63121a29694d270cd15924c2f83bb4c1b07aac6636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d285d55eecaf697663bb1c44b6ccc8f8b08c5593f2b861f9e451821da1b5378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1386bd3de482ad6b2cb6efd1c300b34f8425bbcb96554084c3231642b9fcdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b224e258b50e2c3d31be275f34af7520e124abf2562b6e2b6d347c82dbb8bb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b6240d23d0fb04e1d3c6d33936f26bd98e365665bd280c658a62da9be8540b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8becded23f9b521396eb1fb0777e374e32106bd818961864bf866116f4a820c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19001a71ceb4807ee9a0838a5344d196b4fc73dc44e91a3a7fa3d4a7feb09dd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4f6b10ff7034eed22ad18f8f3c06dc96c93f27b2e738a13660d5d512a5fdac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261b40a42b2544fda5e24516551dd6be8e75baceac74f7fdfb125c68cd285b02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b45fa540e095811dce0b49258d82fb1ab0d0f7e5c0c12a57b4c1859e7646cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88e8fe7bc4613ca6f912715db7b2799f2e3bca08d37ca218d9c9e80f8cdb709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d90962e38503e724893d9e03eefae943484c6d133a297c7bf84b8aeb026c20d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd32c32c428ae6e7896cbc6da9a62efab011c3b2919b91ba01e3a0a54a3ab0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6f58d6c579c8177ae47664179d0f509681cc3a6daad75bb2b7aabf49236ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58529923ff7f8403da57b8234929236d62c9e682db49895b8d0c9ef3f17e72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb912ecfcb1ad2add394e799f7835e88d16b2eac036fef5240a1701ac2d7b05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e733a2f598f3a380406ad8a62af53134c4ab0403c8afc2b673350ff1e6db6ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342c0be76609369b109ebbe1b02c356e074c14818b367ca8801a6d23b04ee9fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d545a6d4d2b88fc22226d937d0bc9ed0795137c3a1e7889d469fd706b331e162(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2c05a266367cb468a45deaba097175d9771f504172f5f38a1494dd4fc056ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec473bb87f0e6756359ded98b43b3a3c9233a5734db350cc155c4efc8491b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5925bed764006d4ec82dd63d17f6bb68bed472e7b77e1b389c6252f72bad6933(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f6c4f874bbb4a3029bdc680f2c3c2107a6da2a44122793fdbd9fd52ff2ac63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925edd4c80cf487756d167d7b24b4e77760ea53ad556bfb6e018bc865a726629(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderConfigA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e631c279b0bb454bf6e928afb3575b1c678683f997a52731a029edaa8b4e22(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_member_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    identity_update_behavior: typing.Optional[builtins.str] = None,
    seat_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secret: typing.Optional[builtins.str] = None,
    user_deprovision: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c057f63e362b90afb1d2e760c971523ef608970739b4361b26adc86bbf4d94e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e81bb2d985434b92ede2bcd7abf7aa2a64259d8d8130f38dd07358f6f400ad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80be433ae05be650ef4f9a82e13ec499b4084ad4ec0dd54a4479f297bd443bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d70ae993a1224ccc35f7d599807ac9390d7f676fa66e9f51a0f0bd59f009a64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88358ada0776fc0071837ab23b8565ded4c33df74964cd6e02bb46a06363d2bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9884353aa215dc55b6f3f35e6a32653e5cb3aa6d4a04aa3c4a2bbbc7fd0d1224(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessIdentityProviderScimConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377dee8c91792a5f8d93d272183fb2ac1971eea00a6290278a0287f5e057dc59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4546d8636469d45aaec91212ae2f9f1f6c0872318ee29e544dc032893cd1d4d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a87033ec33e0b36f123366df181ebc00779078256961d5d95df55cd4b9a8c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1247c3ef8210ad41e479a9262422f2ccbb50f9b2d420746c86119d4366dedc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8615d2b92a9864f26056e35ec4e7b5696d58a8d588784afc87d4339b2990df4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b74cdbd8bda2d31a00c608265fc3c09772820fffd49d629ac7ea99ba394c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698fa44216082a4088d47fc8e32ee80d4f265a7fc317173386b4499cb4f60bcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4545594c586c824ab538c9023eab68a13304fd0168e6493d5eaefeb2123d80d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessIdentityProviderScimConfig]],
) -> None:
    """Type checking stubs"""
    pass
