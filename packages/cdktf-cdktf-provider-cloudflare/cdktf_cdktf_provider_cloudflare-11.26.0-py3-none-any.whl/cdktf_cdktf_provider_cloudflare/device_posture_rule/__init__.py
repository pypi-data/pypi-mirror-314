r'''
# `cloudflare_device_posture_rule`

Refer to the Terraform Registry for docs: [`cloudflare_device_posture_rule`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule).
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


class DevicePostureRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule cloudflare_device_posture_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule cloudflare_device_posture_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#account_id DevicePostureRule#account_id}
        :param type: The device posture rule type. Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``client_certificate``, ``client_certificate_v2``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``, ``sentinelone``, ``kolide``, ``tanium_s2s``, ``intune``, ``sentinelone_s2s``, ``custom_s2s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#type DevicePostureRule#type}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#description DevicePostureRule#description}.
        :param expiration: Expire posture results after the specified amount of time. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#expiration DevicePostureRule#expiration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#id DevicePostureRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#input DevicePostureRule#input}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#match DevicePostureRule#match}
        :param name: Name of the device posture rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#name DevicePostureRule#name}
        :param schedule: Tells the client when to run the device posture check. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#schedule DevicePostureRule#schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494f8f43c04817278220af714151722da52fb36b0bd580bd1d619b7d97cbb1af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DevicePostureRuleConfig(
            account_id=account_id,
            type=type,
            description=description,
            expiration=expiration,
            id=id,
            input=input,
            match=match,
            name=name,
            schedule=schedule,
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
        '''Generates CDKTF code for importing a DevicePostureRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DevicePostureRule to import.
        :param import_from_id: The id of the existing DevicePostureRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DevicePostureRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7a13a54673655fd368bb6fe701257fde9a44cc211870a5e9daf92c0992a036)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc988f0d9ae7d1d4202d73f8b30e897c9672ab2dc71b4f472b2aeefb48e18ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba2261b3b5e73ce9692241d0cb3f3d3f3b31045f11fe96109d78a473da3dc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

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
    @jsii.member(jsii_name="input")
    def input(self) -> "DevicePostureRuleInputList":
        return typing.cast("DevicePostureRuleInputList", jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> "DevicePostureRuleMatchList":
        return typing.cast("DevicePostureRuleMatchList", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113a65c63dbb9fa728571d146a4c14fdd5a75f1386fe8a44aa0f0e02b8225dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0384b2fbd09b72376b01b1fcd8bf095bfee99348a8763bc669e50bd919666331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef2c09ecd134b16867e2569200742966cdc1bb38389214a813498e0d1fc04b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd37e21c027196f9aad5dc1310fc7ef1ce3332c3be23df3cfca8856dbe0b9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d595444183bfd85332545bc1adb550a16d317e738ff4d2a0b8949e6e36117b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57114897a71f5585126106626c5d177c2f2c2574406ebaa1afd0ced8e1b1f472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25988da3b1a31806454122c26a530282600cd866dcc7f5fc0a75dba99778a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleConfig",
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
        "type": "type",
        "description": "description",
        "expiration": "expiration",
        "id": "id",
        "input": "input",
        "match": "match",
        "name": "name",
        "schedule": "schedule",
    },
)
class DevicePostureRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#account_id DevicePostureRule#account_id}
        :param type: The device posture rule type. Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``client_certificate``, ``client_certificate_v2``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``, ``sentinelone``, ``kolide``, ``tanium_s2s``, ``intune``, ``sentinelone_s2s``, ``custom_s2s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#type DevicePostureRule#type}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#description DevicePostureRule#description}.
        :param expiration: Expire posture results after the specified amount of time. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#expiration DevicePostureRule#expiration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#id DevicePostureRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#input DevicePostureRule#input}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#match DevicePostureRule#match}
        :param name: Name of the device posture rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#name DevicePostureRule#name}
        :param schedule: Tells the client when to run the device posture check. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#schedule DevicePostureRule#schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa817da09a38468daa126847f27e850ad6afc1a4888ce613898f3cf9d30b4fb4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
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
        if description is not None:
            self._values["description"] = description
        if expiration is not None:
            self._values["expiration"] = expiration
        if id is not None:
            self._values["id"] = id
        if input is not None:
            self._values["input"] = input
        if match is not None:
            self._values["match"] = match
        if name is not None:
            self._values["name"] = name
        if schedule is not None:
            self._values["schedule"] = schedule

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#account_id DevicePostureRule#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The device posture rule type.

        Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``client_certificate``, ``client_certificate_v2``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``, ``sentinelone``, ``kolide``, ``tanium_s2s``, ``intune``, ``sentinelone_s2s``, ``custom_s2s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#type DevicePostureRule#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#description DevicePostureRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Expire posture results after the specified amount of time.

        Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#expiration DevicePostureRule#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#id DevicePostureRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]]:
        '''input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#input DevicePostureRule#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#match DevicePostureRule#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the device posture rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#name DevicePostureRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Tells the client when to run the device posture check.

        Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#schedule DevicePostureRule#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInput",
    jsii_struct_bases=[],
    name_mapping={
        "active_threats": "activeThreats",
        "certificate_id": "certificateId",
        "check_disks": "checkDisks",
        "check_private_key": "checkPrivateKey",
        "cn": "cn",
        "compliance_status": "complianceStatus",
        "connection_id": "connectionId",
        "count_operator": "countOperator",
        "domain": "domain",
        "eid_last_seen": "eidLastSeen",
        "enabled": "enabled",
        "exists": "exists",
        "extended_key_usage": "extendedKeyUsage",
        "id": "id",
        "infected": "infected",
        "is_active": "isActive",
        "issue_count": "issueCount",
        "last_seen": "lastSeen",
        "locations": "locations",
        "network_status": "networkStatus",
        "operational_state": "operationalState",
        "operator": "operator",
        "os": "os",
        "os_distro_name": "osDistroName",
        "os_distro_revision": "osDistroRevision",
        "os_version_extra": "osVersionExtra",
        "overall": "overall",
        "path": "path",
        "require_all": "requireAll",
        "risk_level": "riskLevel",
        "running": "running",
        "score": "score",
        "sensor_config": "sensorConfig",
        "sha256": "sha256",
        "state": "state",
        "thumbprint": "thumbprint",
        "total_score": "totalScore",
        "version": "version",
        "version_operator": "versionOperator",
    },
)
class DevicePostureRuleInput:
    def __init__(
        self,
        *,
        active_threats: typing.Optional[jsii.Number] = None,
        certificate_id: typing.Optional[builtins.str] = None,
        check_disks: typing.Optional[typing.Sequence[builtins.str]] = None,
        check_private_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cn: typing.Optional[builtins.str] = None,
        compliance_status: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        count_operator: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        eid_last_seen: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extended_key_usage: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        infected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issue_count: typing.Optional[builtins.str] = None,
        last_seen: typing.Optional[builtins.str] = None,
        locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInputLocations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_status: typing.Optional[builtins.str] = None,
        operational_state: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        os_distro_name: typing.Optional[builtins.str] = None,
        os_distro_revision: typing.Optional[builtins.str] = None,
        os_version_extra: typing.Optional[builtins.str] = None,
        overall: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        require_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        risk_level: typing.Optional[builtins.str] = None,
        running: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        score: typing.Optional[jsii.Number] = None,
        sensor_config: typing.Optional[builtins.str] = None,
        sha256: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        thumbprint: typing.Optional[builtins.str] = None,
        total_score: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
        version_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_threats: The number of active threats from SentinelOne. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#active_threats DevicePostureRule#active_threats}
        :param certificate_id: The UUID of a Cloudflare managed certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#certificate_id DevicePostureRule#certificate_id}
        :param check_disks: Specific volume(s) to check for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#check_disks DevicePostureRule#check_disks}
        :param check_private_key: Confirm the certificate was not imported from another device. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#check_private_key DevicePostureRule#check_private_key}
        :param cn: The common name for a certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#cn DevicePostureRule#cn}
        :param compliance_status: The workspace one or intune device compliance status. ``compliant`` and ``noncompliant`` are values supported by both providers. ``unknown``, ``conflict``, ``error``, ``ingraceperiod`` values are only supported by intune. Available values: ``compliant``, ``noncompliant``, ``unknown``, ``conflict``, ``error``, ``ingraceperiod``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#compliance_status DevicePostureRule#compliance_status}
        :param connection_id: The workspace one or intune connection id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#connection_id DevicePostureRule#connection_id}
        :param count_operator: The count comparison operator for kolide. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#count_operator DevicePostureRule#count_operator}
        :param domain: The domain that the client must join. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#domain DevicePostureRule#domain}
        :param eid_last_seen: The time a device last seen in Tanium. Must be in the format ``1h`` or ``30m``. Valid units are ``d``, ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#eid_last_seen DevicePostureRule#eid_last_seen}
        :param enabled: True if the firewall must be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#enabled DevicePostureRule#enabled}
        :param exists: Checks if the file should exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#exists DevicePostureRule#exists}
        :param extended_key_usage: List of values indicating purposes for which the certificate public key can be used. Available values: ``clientAuth``, ``emailProtection``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#extended_key_usage DevicePostureRule#extended_key_usage}
        :param id: The Teams List id. Required for ``serial_number`` and ``unique_client_id`` rule types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#id DevicePostureRule#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param infected: True if SentinelOne device is infected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#infected DevicePostureRule#infected}
        :param is_active: True if SentinelOne device is active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#is_active DevicePostureRule#is_active}
        :param issue_count: The number of issues for kolide. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#issue_count DevicePostureRule#issue_count}
        :param last_seen: The duration of time that the host was last seen from Crowdstrike. Must be in the format ``1h`` or ``30m``. Valid units are ``d``, ``h`` and ``m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#last_seen DevicePostureRule#last_seen}
        :param locations: locations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#locations DevicePostureRule#locations}
        :param network_status: The network status from SentinelOne. Available values: ``connected``, ``disconnected``, ``disconnecting``, ``connecting``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#network_status DevicePostureRule#network_status}
        :param operational_state: The current operational state of a SentinelOne Agent. Available values: ``na``, ``partially_disabled``, ``auto_fully_disabled``, ``fully_disabled``, ``auto_partially_disabled``, ``disabled_error``, ``db_corruption``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#operational_state DevicePostureRule#operational_state}
        :param operator: The version comparison operator. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#operator DevicePostureRule#operator}
        :param os: OS signal score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os DevicePostureRule#os}
        :param os_distro_name: The operating system excluding version information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_distro_name DevicePostureRule#os_distro_name}
        :param os_distro_revision: The operating system version excluding OS name information or release name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_distro_revision DevicePostureRule#os_distro_revision}
        :param os_version_extra: Extra version value following the operating system semantic version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_version_extra DevicePostureRule#os_version_extra}
        :param overall: Overall ZTA score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#overall DevicePostureRule#overall}
        :param path: The path to the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#path DevicePostureRule#path}
        :param require_all: True if all drives must be encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#require_all DevicePostureRule#require_all}
        :param risk_level: The risk level from Tanium. Available values: ``low``, ``medium``, ``high``, ``critical``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#risk_level DevicePostureRule#risk_level}
        :param running: Checks if the application should be running. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#running DevicePostureRule#running}
        :param score: A value between 0-100 assigned to devices set by the 3rd party posture provider for custom device posture integrations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#score DevicePostureRule#score}
        :param sensor_config: Sensor signal score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#sensor_config DevicePostureRule#sensor_config}
        :param sha256: The sha256 hash of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#sha256 DevicePostureRule#sha256}
        :param state: The host’s current online status from Crowdstrike. Available values: ``online``, ``offline``, ``unknown``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#state DevicePostureRule#state}
        :param thumbprint: The thumbprint of the file certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#thumbprint DevicePostureRule#thumbprint}
        :param total_score: The total score from Tanium. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#total_score DevicePostureRule#total_score}
        :param version: The operating system semantic version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#version DevicePostureRule#version}
        :param version_operator: The version comparison operator for Crowdstrike. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#version_operator DevicePostureRule#version_operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5189d7ffb5c296d0a8d0cf95c7694928856e6a6a5e5a63551b29645ddcdcf7)
            check_type(argname="argument active_threats", value=active_threats, expected_type=type_hints["active_threats"])
            check_type(argname="argument certificate_id", value=certificate_id, expected_type=type_hints["certificate_id"])
            check_type(argname="argument check_disks", value=check_disks, expected_type=type_hints["check_disks"])
            check_type(argname="argument check_private_key", value=check_private_key, expected_type=type_hints["check_private_key"])
            check_type(argname="argument cn", value=cn, expected_type=type_hints["cn"])
            check_type(argname="argument compliance_status", value=compliance_status, expected_type=type_hints["compliance_status"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument count_operator", value=count_operator, expected_type=type_hints["count_operator"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument eid_last_seen", value=eid_last_seen, expected_type=type_hints["eid_last_seen"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument infected", value=infected, expected_type=type_hints["infected"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument issue_count", value=issue_count, expected_type=type_hints["issue_count"])
            check_type(argname="argument last_seen", value=last_seen, expected_type=type_hints["last_seen"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument network_status", value=network_status, expected_type=type_hints["network_status"])
            check_type(argname="argument operational_state", value=operational_state, expected_type=type_hints["operational_state"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument os_distro_name", value=os_distro_name, expected_type=type_hints["os_distro_name"])
            check_type(argname="argument os_distro_revision", value=os_distro_revision, expected_type=type_hints["os_distro_revision"])
            check_type(argname="argument os_version_extra", value=os_version_extra, expected_type=type_hints["os_version_extra"])
            check_type(argname="argument overall", value=overall, expected_type=type_hints["overall"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument require_all", value=require_all, expected_type=type_hints["require_all"])
            check_type(argname="argument risk_level", value=risk_level, expected_type=type_hints["risk_level"])
            check_type(argname="argument running", value=running, expected_type=type_hints["running"])
            check_type(argname="argument score", value=score, expected_type=type_hints["score"])
            check_type(argname="argument sensor_config", value=sensor_config, expected_type=type_hints["sensor_config"])
            check_type(argname="argument sha256", value=sha256, expected_type=type_hints["sha256"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
            check_type(argname="argument total_score", value=total_score, expected_type=type_hints["total_score"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument version_operator", value=version_operator, expected_type=type_hints["version_operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_threats is not None:
            self._values["active_threats"] = active_threats
        if certificate_id is not None:
            self._values["certificate_id"] = certificate_id
        if check_disks is not None:
            self._values["check_disks"] = check_disks
        if check_private_key is not None:
            self._values["check_private_key"] = check_private_key
        if cn is not None:
            self._values["cn"] = cn
        if compliance_status is not None:
            self._values["compliance_status"] = compliance_status
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if count_operator is not None:
            self._values["count_operator"] = count_operator
        if domain is not None:
            self._values["domain"] = domain
        if eid_last_seen is not None:
            self._values["eid_last_seen"] = eid_last_seen
        if enabled is not None:
            self._values["enabled"] = enabled
        if exists is not None:
            self._values["exists"] = exists
        if extended_key_usage is not None:
            self._values["extended_key_usage"] = extended_key_usage
        if id is not None:
            self._values["id"] = id
        if infected is not None:
            self._values["infected"] = infected
        if is_active is not None:
            self._values["is_active"] = is_active
        if issue_count is not None:
            self._values["issue_count"] = issue_count
        if last_seen is not None:
            self._values["last_seen"] = last_seen
        if locations is not None:
            self._values["locations"] = locations
        if network_status is not None:
            self._values["network_status"] = network_status
        if operational_state is not None:
            self._values["operational_state"] = operational_state
        if operator is not None:
            self._values["operator"] = operator
        if os is not None:
            self._values["os"] = os
        if os_distro_name is not None:
            self._values["os_distro_name"] = os_distro_name
        if os_distro_revision is not None:
            self._values["os_distro_revision"] = os_distro_revision
        if os_version_extra is not None:
            self._values["os_version_extra"] = os_version_extra
        if overall is not None:
            self._values["overall"] = overall
        if path is not None:
            self._values["path"] = path
        if require_all is not None:
            self._values["require_all"] = require_all
        if risk_level is not None:
            self._values["risk_level"] = risk_level
        if running is not None:
            self._values["running"] = running
        if score is not None:
            self._values["score"] = score
        if sensor_config is not None:
            self._values["sensor_config"] = sensor_config
        if sha256 is not None:
            self._values["sha256"] = sha256
        if state is not None:
            self._values["state"] = state
        if thumbprint is not None:
            self._values["thumbprint"] = thumbprint
        if total_score is not None:
            self._values["total_score"] = total_score
        if version is not None:
            self._values["version"] = version
        if version_operator is not None:
            self._values["version_operator"] = version_operator

    @builtins.property
    def active_threats(self) -> typing.Optional[jsii.Number]:
        '''The number of active threats from SentinelOne.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#active_threats DevicePostureRule#active_threats}
        '''
        result = self._values.get("active_threats")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def certificate_id(self) -> typing.Optional[builtins.str]:
        '''The UUID of a Cloudflare managed certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#certificate_id DevicePostureRule#certificate_id}
        '''
        result = self._values.get("certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_disks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specific volume(s) to check for encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#check_disks DevicePostureRule#check_disks}
        '''
        result = self._values.get("check_disks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def check_private_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Confirm the certificate was not imported from another device.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#check_private_key DevicePostureRule#check_private_key}
        '''
        result = self._values.get("check_private_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cn(self) -> typing.Optional[builtins.str]:
        '''The common name for a certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#cn DevicePostureRule#cn}
        '''
        result = self._values.get("cn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compliance_status(self) -> typing.Optional[builtins.str]:
        '''The workspace one or intune device compliance status.

        ``compliant`` and ``noncompliant`` are values supported by both providers. ``unknown``, ``conflict``, ``error``, ``ingraceperiod`` values are only supported by intune. Available values: ``compliant``, ``noncompliant``, ``unknown``, ``conflict``, ``error``, ``ingraceperiod``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#compliance_status DevicePostureRule#compliance_status}
        '''
        result = self._values.get("compliance_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The workspace one or intune connection id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#connection_id DevicePostureRule#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def count_operator(self) -> typing.Optional[builtins.str]:
        '''The count comparison operator for kolide. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#count_operator DevicePostureRule#count_operator}
        '''
        result = self._values.get("count_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain that the client must join.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#domain DevicePostureRule#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eid_last_seen(self) -> typing.Optional[builtins.str]:
        '''The time a device last seen in Tanium.

        Must be in the format ``1h`` or ``30m``. Valid units are ``d``, ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#eid_last_seen DevicePostureRule#eid_last_seen}
        '''
        result = self._values.get("eid_last_seen")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the firewall must be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#enabled DevicePostureRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Checks if the file should exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#exists DevicePostureRule#exists}
        '''
        result = self._values.get("exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extended_key_usage(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values indicating purposes for which the certificate public key can be used. Available values: ``clientAuth``, ``emailProtection``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#extended_key_usage DevicePostureRule#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The Teams List id. Required for ``serial_number`` and ``unique_client_id`` rule types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#id DevicePostureRule#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if SentinelOne device is infected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#infected DevicePostureRule#infected}
        '''
        result = self._values.get("infected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if SentinelOne device is active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#is_active DevicePostureRule#is_active}
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issue_count(self) -> typing.Optional[builtins.str]:
        '''The number of issues for kolide.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#issue_count DevicePostureRule#issue_count}
        '''
        result = self._values.get("issue_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_seen(self) -> typing.Optional[builtins.str]:
        '''The duration of time that the host was last seen from Crowdstrike.

        Must be in the format ``1h`` or ``30m``. Valid units are ``d``, ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#last_seen DevicePostureRule#last_seen}
        '''
        result = self._values.get("last_seen")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInputLocations"]]]:
        '''locations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#locations DevicePostureRule#locations}
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInputLocations"]]], result)

    @builtins.property
    def network_status(self) -> typing.Optional[builtins.str]:
        '''The network status from SentinelOne. Available values: ``connected``, ``disconnected``, ``disconnecting``, ``connecting``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#network_status DevicePostureRule#network_status}
        '''
        result = self._values.get("network_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operational_state(self) -> typing.Optional[builtins.str]:
        '''The current operational state of a SentinelOne Agent. Available values: ``na``, ``partially_disabled``, ``auto_fully_disabled``, ``fully_disabled``, ``auto_partially_disabled``, ``disabled_error``, ``db_corruption``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#operational_state DevicePostureRule#operational_state}
        '''
        result = self._values.get("operational_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''The version comparison operator. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#operator DevicePostureRule#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''OS signal score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os DevicePostureRule#os}
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_distro_name(self) -> typing.Optional[builtins.str]:
        '''The operating system excluding version information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_distro_name DevicePostureRule#os_distro_name}
        '''
        result = self._values.get("os_distro_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_distro_revision(self) -> typing.Optional[builtins.str]:
        '''The operating system version excluding OS name information or release name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_distro_revision DevicePostureRule#os_distro_revision}
        '''
        result = self._values.get("os_distro_revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_version_extra(self) -> typing.Optional[builtins.str]:
        '''Extra version value following the operating system semantic version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#os_version_extra DevicePostureRule#os_version_extra}
        '''
        result = self._values.get("os_version_extra")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overall(self) -> typing.Optional[builtins.str]:
        '''Overall ZTA score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#overall DevicePostureRule#overall}
        '''
        result = self._values.get("overall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#path DevicePostureRule#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if all drives must be encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#require_all DevicePostureRule#require_all}
        '''
        result = self._values.get("require_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def risk_level(self) -> typing.Optional[builtins.str]:
        '''The risk level from Tanium. Available values: ``low``, ``medium``, ``high``, ``critical``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#risk_level DevicePostureRule#risk_level}
        '''
        result = self._values.get("risk_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def running(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Checks if the application should be running.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#running DevicePostureRule#running}
        '''
        result = self._values.get("running")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def score(self) -> typing.Optional[jsii.Number]:
        '''A value between 0-100 assigned to devices set by the 3rd party posture provider for custom device posture integrations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#score DevicePostureRule#score}
        '''
        result = self._values.get("score")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sensor_config(self) -> typing.Optional[builtins.str]:
        '''Sensor signal score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#sensor_config DevicePostureRule#sensor_config}
        '''
        result = self._values.get("sensor_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sha256(self) -> typing.Optional[builtins.str]:
        '''The sha256 hash of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#sha256 DevicePostureRule#sha256}
        '''
        result = self._values.get("sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The host’s current online status from Crowdstrike. Available values: ``online``, ``offline``, ``unknown``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#state DevicePostureRule#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thumbprint(self) -> typing.Optional[builtins.str]:
        '''The thumbprint of the file certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#thumbprint DevicePostureRule#thumbprint}
        '''
        result = self._values.get("thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_score(self) -> typing.Optional[jsii.Number]:
        '''The total score from Tanium.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#total_score DevicePostureRule#total_score}
        '''
        result = self._values.get("total_score")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The operating system semantic version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#version DevicePostureRule#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_operator(self) -> typing.Optional[builtins.str]:
        '''The version comparison operator for Crowdstrike. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#version_operator DevicePostureRule#version_operator}
        '''
        result = self._values.get("version_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureRuleInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49aeee82282cc7fbe77ebc8dcabc3e352d6a4510e0e064712ce0010d08d5dfab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DevicePostureRuleInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3cb79c7906e646ce5a0e40c63fefb6f93f5b3434b4977130fab76ceb38d233)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureRuleInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0b4f1db1869a08dae27417ed72ca3eee21a30df7c4106a17f841c80e517e8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e225b7db827ae8c40479108e4844e7dd1976f6035121d709452836ff9db0849)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ca76c9518c3f0f8b0c7514171764de7c05bcd7638b1b7805526411dc5e6971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d348b03b9860dd93f49a9101b4d06f94ff5f7e962cff18ecfa2a2cfd19be85f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputLocations",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths", "trust_stores": "trustStores"},
)
class DevicePostureRuleInputLocations:
    def __init__(
        self,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        trust_stores: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param paths: List of paths to check for client certificate rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#paths DevicePostureRule#paths}
        :param trust_stores: List of trust stores to check for client certificate rule. Available values: ``system``, ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#trust_stores DevicePostureRule#trust_stores}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5896925cebf69eb589556ec46cd25e0b8b4b666dec960444ea8e39f6b87112b2)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument trust_stores", value=trust_stores, expected_type=type_hints["trust_stores"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if paths is not None:
            self._values["paths"] = paths
        if trust_stores is not None:
            self._values["trust_stores"] = trust_stores

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of paths to check for client certificate rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#paths DevicePostureRule#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trust_stores(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of trust stores to check for client certificate rule. Available values: ``system``, ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#trust_stores DevicePostureRule#trust_stores}
        '''
        result = self._values.get("trust_stores")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleInputLocations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureRuleInputLocationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputLocationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0942f0f9abe0279c26e3f656b708bb61e241076f5d6c1b91c1e28945d4e9542e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DevicePostureRuleInputLocationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbed7130787c04e43da731a4b33df1f243b08a2ef92528f146d245bedff4717)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureRuleInputLocationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871f0242c975c2f70418871a7e39da38a9f300807e6ebf1ba63b505e2c908ea1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7dfa147f4ba0576bbf58094579b5fc0bffc83daee11682c543ae75baf4c67f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9786c3a18a8becba63ab60d58fd665f8a72b2f02ae6286fa5631611a6f4872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b7663080aba494766fd5750afeec37af6ea0b8f5db736b7a75a3dacbaf7503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DevicePostureRuleInputLocationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputLocationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09689ec0ceeb0f7c6779c8c337df810dd75cf51433338269da8a37388effc38f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @jsii.member(jsii_name="resetTrustStores")
    def reset_trust_stores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustStores", []))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustStoresInput")
    def trust_stores_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustStoresInput"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb2f0e4bdeb5e00d9eb77ab71c22b9acc20f61906ff4c3931277aec74994f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustStores")
    def trust_stores(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustStores"))

    @trust_stores.setter
    def trust_stores(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c159dc7ba41897b77af376e0bd2891111a8571ec6c6cd19d052894bd96644bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustStores", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInputLocations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInputLocations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInputLocations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83224fea589a8df203dd189c5e7205b4cf42becb3dea24bccbb4b087c2897358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DevicePostureRuleInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed93bd050f27ea05e0f30cae92cacd3cb8f4fddd33a31e4c8741ffa057f9e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLocations")
    def put_locations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInputLocations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4bdd9155c6bf657dc2d8a1919c470baa0c9c7511e6df6810aa317fbdc384b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocations", [value]))

    @jsii.member(jsii_name="resetActiveThreats")
    def reset_active_threats(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveThreats", []))

    @jsii.member(jsii_name="resetCertificateId")
    def reset_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateId", []))

    @jsii.member(jsii_name="resetCheckDisks")
    def reset_check_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckDisks", []))

    @jsii.member(jsii_name="resetCheckPrivateKey")
    def reset_check_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckPrivateKey", []))

    @jsii.member(jsii_name="resetCn")
    def reset_cn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCn", []))

    @jsii.member(jsii_name="resetComplianceStatus")
    def reset_compliance_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceStatus", []))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetCountOperator")
    def reset_count_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountOperator", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetEidLastSeen")
    def reset_eid_last_seen(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEidLastSeen", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExists")
    def reset_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExists", []))

    @jsii.member(jsii_name="resetExtendedKeyUsage")
    def reset_extended_key_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedKeyUsage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInfected")
    def reset_infected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfected", []))

    @jsii.member(jsii_name="resetIsActive")
    def reset_is_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsActive", []))

    @jsii.member(jsii_name="resetIssueCount")
    def reset_issue_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueCount", []))

    @jsii.member(jsii_name="resetLastSeen")
    def reset_last_seen(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastSeen", []))

    @jsii.member(jsii_name="resetLocations")
    def reset_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocations", []))

    @jsii.member(jsii_name="resetNetworkStatus")
    def reset_network_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkStatus", []))

    @jsii.member(jsii_name="resetOperationalState")
    def reset_operational_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationalState", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetOs")
    def reset_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOs", []))

    @jsii.member(jsii_name="resetOsDistroName")
    def reset_os_distro_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDistroName", []))

    @jsii.member(jsii_name="resetOsDistroRevision")
    def reset_os_distro_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDistroRevision", []))

    @jsii.member(jsii_name="resetOsVersionExtra")
    def reset_os_version_extra(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersionExtra", []))

    @jsii.member(jsii_name="resetOverall")
    def reset_overall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverall", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRequireAll")
    def reset_require_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAll", []))

    @jsii.member(jsii_name="resetRiskLevel")
    def reset_risk_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRiskLevel", []))

    @jsii.member(jsii_name="resetRunning")
    def reset_running(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunning", []))

    @jsii.member(jsii_name="resetScore")
    def reset_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScore", []))

    @jsii.member(jsii_name="resetSensorConfig")
    def reset_sensor_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensorConfig", []))

    @jsii.member(jsii_name="resetSha256")
    def reset_sha256(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetThumbprint")
    def reset_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbprint", []))

    @jsii.member(jsii_name="resetTotalScore")
    def reset_total_score(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalScore", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetVersionOperator")
    def reset_version_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionOperator", []))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> DevicePostureRuleInputLocationsList:
        return typing.cast(DevicePostureRuleInputLocationsList, jsii.get(self, "locations"))

    @builtins.property
    @jsii.member(jsii_name="activeThreatsInput")
    def active_threats_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "activeThreatsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIdInput")
    def certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="checkDisksInput")
    def check_disks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "checkDisksInput"))

    @builtins.property
    @jsii.member(jsii_name="checkPrivateKeyInput")
    def check_private_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "checkPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cnInput")
    def cn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cnInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceStatusInput")
    def compliance_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "complianceStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="countOperatorInput")
    def count_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="eidLastSeenInput")
    def eid_last_seen_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eidLastSeenInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="existsInput")
    def exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "existsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="infectedInput")
    def infected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "infectedInput"))

    @builtins.property
    @jsii.member(jsii_name="isActiveInput")
    def is_active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isActiveInput"))

    @builtins.property
    @jsii.member(jsii_name="issueCountInput")
    def issue_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issueCountInput"))

    @builtins.property
    @jsii.member(jsii_name="lastSeenInput")
    def last_seen_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastSeenInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkStatusInput")
    def network_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="operationalStateInput")
    def operational_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationalStateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="osDistroNameInput")
    def os_distro_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDistroNameInput"))

    @builtins.property
    @jsii.member(jsii_name="osDistroRevisionInput")
    def os_distro_revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDistroRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionExtraInput")
    def os_version_extra_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersionExtraInput"))

    @builtins.property
    @jsii.member(jsii_name="overallInput")
    def overall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overallInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAllInput")
    def require_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAllInput"))

    @builtins.property
    @jsii.member(jsii_name="riskLevelInput")
    def risk_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "riskLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="runningInput")
    def running_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runningInput"))

    @builtins.property
    @jsii.member(jsii_name="scoreInput")
    def score_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scoreInput"))

    @builtins.property
    @jsii.member(jsii_name="sensorConfigInput")
    def sensor_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sensorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Input")
    def sha256_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256Input"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="totalScoreInput")
    def total_score_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalScoreInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="versionOperatorInput")
    def version_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="activeThreats")
    def active_threats(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "activeThreats"))

    @active_threats.setter
    def active_threats(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af256193ba19842f404858e5652ac67c4254ca9bcbb580ef80bf71381e90a64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeThreats", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @certificate_id.setter
    def certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3870d0a3e75cb2257182ffef56f17d509d7afe0e9b0ea4cce80a3f6a1e5cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="checkDisks")
    def check_disks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "checkDisks"))

    @check_disks.setter
    def check_disks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4312d2139f05843bb4bea2ac4c453aa1c06b2d9e83048a70a400c18b76f94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkDisks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="checkPrivateKey")
    def check_private_key(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "checkPrivateKey"))

    @check_private_key.setter
    def check_private_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d441abf79d2514e9da70ae3f4f7225111da67cdf945b0c4944dcd567a3a4a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkPrivateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cn")
    def cn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cn"))

    @cn.setter
    def cn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5c000cbc1fc425420d0d483d9fa13ee73d0dedef058110d64195e2848026ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="complianceStatus")
    def compliance_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "complianceStatus"))

    @compliance_status.setter
    def compliance_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f81cc928b1d5f9597a05f475e68cd848be72b30b30adbfc45a0d768003734c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complianceStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b586981fb5b45c04c00ec31700c84899177a0208ba1b5d6380b4b33524e22f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countOperator")
    def count_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countOperator"))

    @count_operator.setter
    def count_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e682e244097d7252f7a2f98fe7796110c62b9057cacc36426467835e8464b022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e36d2c5e54475a0832f73fa60448356c84a5ced07d50635ae443993626b20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eidLastSeen")
    def eid_last_seen(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eidLastSeen"))

    @eid_last_seen.setter
    def eid_last_seen(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e2bf95fa4a16c4f439cd01e85a27db233978a64ef453aea3cb7189954aedcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eidLastSeen", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__69f168ad98553b54bd5d9d8150fca49faf5b08239be6f7a230e702b18e6bbe65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exists")
    def exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exists"))

    @exists.setter
    def exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8d5e4f9d35e29de4802aba8b03bd4f60dc1ed4a9eb126725e2c8746ce01ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extendedKeyUsage"))

    @extended_key_usage.setter
    def extended_key_usage(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cfb24f2ed75b7e4f297b3f70bafb994e8f2d87f1227212d1899a1f69472d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendedKeyUsage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f421d222cda3b11c807139fb4186b08eaad7151a5233e2871e5927e9e5f99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infected")
    def infected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "infected"))

    @infected.setter
    def infected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3613322da688211944b3a29b686a80b23e9136cce406a691a18dd5e631df9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infected", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isActive")
    def is_active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isActive"))

    @is_active.setter
    def is_active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bb81a86abe19a50dde26c10f0486f63a29e6ce1194cb213dc25c5f099c10f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isActive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issueCount")
    def issue_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issueCount"))

    @issue_count.setter
    def issue_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40526374397e995ec4796b20fbd8cdbeec0e1afd47c0fdf5599682ed254ac3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastSeen")
    def last_seen(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSeen"))

    @last_seen.setter
    def last_seen(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6213719c216c00cd04df9d4fafe0e6db62c005b5a864318fb4fc72863ab042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastSeen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkStatus")
    def network_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkStatus"))

    @network_status.setter
    def network_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b824d07f4c94bc8fdda06f8546d5ec4053f5df26d674e060039a37f0f97bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationalState")
    def operational_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationalState"))

    @operational_state.setter
    def operational_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf090cf61f296001e47cbb017b186cf561866a1e95591c23059fbe9cfb6b18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationalState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14d3372b1fe23805d144a4325d2d61ba72054a3298093f6669d89f5835a64f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d1d1360468ae8c277360c714f2aa92e37a210c4f5e6ff0727d87491d74752d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDistroName")
    def os_distro_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDistroName"))

    @os_distro_name.setter
    def os_distro_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64df9cef991ed7bdc5396cc281da832305d71b6b9e04856a0b57409b9248ec51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDistroName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osDistroRevision")
    def os_distro_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDistroRevision"))

    @os_distro_revision.setter
    def os_distro_revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8820de5a9bc2c9e0278fae6211aef505917b986253507997b00373ceb60042d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDistroRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersionExtra")
    def os_version_extra(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersionExtra"))

    @os_version_extra.setter
    def os_version_extra(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549483c88c79a5e986c2ee070378dbe180abd79c3ad5e27e081e9007042969c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersionExtra", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overall")
    def overall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overall"))

    @overall.setter
    def overall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cfae7d06316d2a4b7cba6105edcafc75add1cd1d2814fc64020ba0a226405f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95538f57139ff2073f888f959e913df262826ba63fff9ec127f8407bc93444de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAll")
    def require_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAll"))

    @require_all.setter
    def require_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eda1f64d8ac088442d401cd0c18dca35ea9e5484efac7df84315e494366cad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="riskLevel")
    def risk_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "riskLevel"))

    @risk_level.setter
    def risk_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63c2d8e915818efba0e8d5a6e6e806895595a3ddf740bbb23ed556d70d119d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "riskLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="running")
    def running(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "running"))

    @running.setter
    def running(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab0e2534a655fda0582b2ac117cb03f137d05edbc0358b6e3fd95967720bc6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "running", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="score")
    def score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "score"))

    @score.setter
    def score(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417df5edd8e49bf9fbfbd8f766408fe32b466607d17e86d19670c61f43e20427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "score", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sensorConfig")
    def sensor_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sensorConfig"))

    @sensor_config.setter
    def sensor_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3f4ea1dc29e979604856b82d0698e51b816c23dca277c802cbe2e27e5e9252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensorConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @sha256.setter
    def sha256(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e301519b0f3c25d96c0d2657988dbc37b52e73b37b96176b2c57caefe79841d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9039d032ccb06b089e600204926a5c7896209d643f75227c9b1acf6e840bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f6ee2a79ed3673cf1258e8580d0447504ded7048b074cd960d5040b7a707c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalScore")
    def total_score(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalScore"))

    @total_score.setter
    def total_score(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb0e8484511329756ac84bcb10868f390bba458d6607396aa0a1da99720d883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalScore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16470c2b91bd05726d3678e5e288ee8313a17f8946d49b9f9b52f4f0bad3d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionOperator")
    def version_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionOperator"))

    @version_operator.setter
    def version_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43d08fba0d50dfb9f96049786176f5ccf1442140a1a52ce6692897861dae0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionOperator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInput]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInput]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInput]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5df1763055034b69fdc812d5d10828d2a4d0805754ba0f47c3cb1a7c672d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatch",
    jsii_struct_bases=[],
    name_mapping={"platform": "platform"},
)
class DevicePostureRuleMatch:
    def __init__(self, *, platform: typing.Optional[builtins.str] = None) -> None:
        '''
        :param platform: The platform of the device. Available values: ``windows``, ``mac``, ``linux``, ``android``, ``ios``, ``chromeos``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#platform DevicePostureRule#platform}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfc29af90f1985dc6f5c7186dd463794fe056488a7dc1bf660c7f04f0ec3d32)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the device. Available values: ``windows``, ``mac``, ``linux``, ``android``, ``ios``, ``chromeos``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/device_posture_rule#platform DevicePostureRule#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureRuleMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3627b13043be2a5afc4695f646ca3e323ea9483bf4794bc16fb5e51331448fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DevicePostureRuleMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f88b77c2037a61eb21fe29e3f27c94a664f20de53f14f224723cffdb5555be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureRuleMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c089de7932e476602bc098ae47e356e9f5860cd84cdeaed5d8b90279890342)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73133f30821f3fa4d55af9ea1928e47a5663a0ce3f98a2f5e19aebaaf2f11e7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41936c2d40d357169dbcd5260a434318660774f2b29c29da3288e5af12be7577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77ac11684684b9bb72b872e9c6380ece7c4e758295a4fee695bdca8b3b31dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DevicePostureRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f89d1d0345ad7a762ea9be4a49982bb7dc401c76a39774a03c10a6f112df0ed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e944670d3e86a9bd0b9cd68438e0fd6bcf06add90ade5e9a23fc4e96d82c02f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleMatch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleMatch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleMatch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117ce4a84081f4816f7794c78d75cdb0c7a36cabd16de31e3e3356208cd319a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DevicePostureRule",
    "DevicePostureRuleConfig",
    "DevicePostureRuleInput",
    "DevicePostureRuleInputList",
    "DevicePostureRuleInputLocations",
    "DevicePostureRuleInputLocationsList",
    "DevicePostureRuleInputLocationsOutputReference",
    "DevicePostureRuleInputOutputReference",
    "DevicePostureRuleMatch",
    "DevicePostureRuleMatchList",
    "DevicePostureRuleMatchOutputReference",
]

publication.publish()

def _typecheckingstub__494f8f43c04817278220af714151722da52fb36b0bd580bd1d619b7d97cbb1af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__af7a13a54673655fd368bb6fe701257fde9a44cc211870a5e9daf92c0992a036(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc988f0d9ae7d1d4202d73f8b30e897c9672ab2dc71b4f472b2aeefb48e18ee1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba2261b3b5e73ce9692241d0cb3f3d3f3b31045f11fe96109d78a473da3dc0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113a65c63dbb9fa728571d146a4c14fdd5a75f1386fe8a44aa0f0e02b8225dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0384b2fbd09b72376b01b1fcd8bf095bfee99348a8763bc669e50bd919666331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef2c09ecd134b16867e2569200742966cdc1bb38389214a813498e0d1fc04b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd37e21c027196f9aad5dc1310fc7ef1ce3332c3be23df3cfca8856dbe0b9f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d595444183bfd85332545bc1adb550a16d317e738ff4d2a0b8949e6e36117b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57114897a71f5585126106626c5d177c2f2c2574406ebaa1afd0ced8e1b1f472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25988da3b1a31806454122c26a530282600cd866dcc7f5fc0a75dba99778a40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa817da09a38468daa126847f27e850ad6afc1a4888ce613898f3cf9d30b4fb4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5189d7ffb5c296d0a8d0cf95c7694928856e6a6a5e5a63551b29645ddcdcf7(
    *,
    active_threats: typing.Optional[jsii.Number] = None,
    certificate_id: typing.Optional[builtins.str] = None,
    check_disks: typing.Optional[typing.Sequence[builtins.str]] = None,
    check_private_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cn: typing.Optional[builtins.str] = None,
    compliance_status: typing.Optional[builtins.str] = None,
    connection_id: typing.Optional[builtins.str] = None,
    count_operator: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    eid_last_seen: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extended_key_usage: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    infected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issue_count: typing.Optional[builtins.str] = None,
    last_seen: typing.Optional[builtins.str] = None,
    locations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInputLocations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_status: typing.Optional[builtins.str] = None,
    operational_state: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    os: typing.Optional[builtins.str] = None,
    os_distro_name: typing.Optional[builtins.str] = None,
    os_distro_revision: typing.Optional[builtins.str] = None,
    os_version_extra: typing.Optional[builtins.str] = None,
    overall: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    require_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    risk_level: typing.Optional[builtins.str] = None,
    running: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    score: typing.Optional[jsii.Number] = None,
    sensor_config: typing.Optional[builtins.str] = None,
    sha256: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    thumbprint: typing.Optional[builtins.str] = None,
    total_score: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
    version_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aeee82282cc7fbe77ebc8dcabc3e352d6a4510e0e064712ce0010d08d5dfab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3cb79c7906e646ce5a0e40c63fefb6f93f5b3434b4977130fab76ceb38d233(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0b4f1db1869a08dae27417ed72ca3eee21a30df7c4106a17f841c80e517e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e225b7db827ae8c40479108e4844e7dd1976f6035121d709452836ff9db0849(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ca76c9518c3f0f8b0c7514171764de7c05bcd7638b1b7805526411dc5e6971(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d348b03b9860dd93f49a9101b4d06f94ff5f7e962cff18ecfa2a2cfd19be85f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5896925cebf69eb589556ec46cd25e0b8b4b666dec960444ea8e39f6b87112b2(
    *,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    trust_stores: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0942f0f9abe0279c26e3f656b708bb61e241076f5d6c1b91c1e28945d4e9542e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbed7130787c04e43da731a4b33df1f243b08a2ef92528f146d245bedff4717(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871f0242c975c2f70418871a7e39da38a9f300807e6ebf1ba63b505e2c908ea1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7dfa147f4ba0576bbf58094579b5fc0bffc83daee11682c543ae75baf4c67f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9786c3a18a8becba63ab60d58fd665f8a72b2f02ae6286fa5631611a6f4872(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b7663080aba494766fd5750afeec37af6ea0b8f5db736b7a75a3dacbaf7503(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInputLocations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09689ec0ceeb0f7c6779c8c337df810dd75cf51433338269da8a37388effc38f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb2f0e4bdeb5e00d9eb77ab71c22b9acc20f61906ff4c3931277aec74994f8a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c159dc7ba41897b77af376e0bd2891111a8571ec6c6cd19d052894bd96644bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83224fea589a8df203dd189c5e7205b4cf42becb3dea24bccbb4b087c2897358(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInputLocations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed93bd050f27ea05e0f30cae92cacd3cb8f4fddd33a31e4c8741ffa057f9e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4bdd9155c6bf657dc2d8a1919c470baa0c9c7511e6df6810aa317fbdc384b3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInputLocations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af256193ba19842f404858e5652ac67c4254ca9bcbb580ef80bf71381e90a64c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3870d0a3e75cb2257182ffef56f17d509d7afe0e9b0ea4cce80a3f6a1e5cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4312d2139f05843bb4bea2ac4c453aa1c06b2d9e83048a70a400c18b76f94f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d441abf79d2514e9da70ae3f4f7225111da67cdf945b0c4944dcd567a3a4a87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5c000cbc1fc425420d0d483d9fa13ee73d0dedef058110d64195e2848026ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f81cc928b1d5f9597a05f475e68cd848be72b30b30adbfc45a0d768003734c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b586981fb5b45c04c00ec31700c84899177a0208ba1b5d6380b4b33524e22f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e682e244097d7252f7a2f98fe7796110c62b9057cacc36426467835e8464b022(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e36d2c5e54475a0832f73fa60448356c84a5ced07d50635ae443993626b20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e2bf95fa4a16c4f439cd01e85a27db233978a64ef453aea3cb7189954aedcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f168ad98553b54bd5d9d8150fca49faf5b08239be6f7a230e702b18e6bbe65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8d5e4f9d35e29de4802aba8b03bd4f60dc1ed4a9eb126725e2c8746ce01ea1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cfb24f2ed75b7e4f297b3f70bafb994e8f2d87f1227212d1899a1f69472d06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f421d222cda3b11c807139fb4186b08eaad7151a5233e2871e5927e9e5f99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3613322da688211944b3a29b686a80b23e9136cce406a691a18dd5e631df9d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bb81a86abe19a50dde26c10f0486f63a29e6ce1194cb213dc25c5f099c10f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40526374397e995ec4796b20fbd8cdbeec0e1afd47c0fdf5599682ed254ac3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6213719c216c00cd04df9d4fafe0e6db62c005b5a864318fb4fc72863ab042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b824d07f4c94bc8fdda06f8546d5ec4053f5df26d674e060039a37f0f97bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf090cf61f296001e47cbb017b186cf561866a1e95591c23059fbe9cfb6b18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14d3372b1fe23805d144a4325d2d61ba72054a3298093f6669d89f5835a64f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d1d1360468ae8c277360c714f2aa92e37a210c4f5e6ff0727d87491d74752d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64df9cef991ed7bdc5396cc281da832305d71b6b9e04856a0b57409b9248ec51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8820de5a9bc2c9e0278fae6211aef505917b986253507997b00373ceb60042d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549483c88c79a5e986c2ee070378dbe180abd79c3ad5e27e081e9007042969c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cfae7d06316d2a4b7cba6105edcafc75add1cd1d2814fc64020ba0a226405f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95538f57139ff2073f888f959e913df262826ba63fff9ec127f8407bc93444de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eda1f64d8ac088442d401cd0c18dca35ea9e5484efac7df84315e494366cad8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63c2d8e915818efba0e8d5a6e6e806895595a3ddf740bbb23ed556d70d119d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab0e2534a655fda0582b2ac117cb03f137d05edbc0358b6e3fd95967720bc6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417df5edd8e49bf9fbfbd8f766408fe32b466607d17e86d19670c61f43e20427(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3f4ea1dc29e979604856b82d0698e51b816c23dca277c802cbe2e27e5e9252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e301519b0f3c25d96c0d2657988dbc37b52e73b37b96176b2c57caefe79841d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9039d032ccb06b089e600204926a5c7896209d643f75227c9b1acf6e840bdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f6ee2a79ed3673cf1258e8580d0447504ded7048b074cd960d5040b7a707c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb0e8484511329756ac84bcb10868f390bba458d6607396aa0a1da99720d883(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16470c2b91bd05726d3678e5e288ee8313a17f8946d49b9f9b52f4f0bad3d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43d08fba0d50dfb9f96049786176f5ccf1442140a1a52ce6692897861dae0bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5df1763055034b69fdc812d5d10828d2a4d0805754ba0f47c3cb1a7c672d86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleInput]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfc29af90f1985dc6f5c7186dd463794fe056488a7dc1bf660c7f04f0ec3d32(
    *,
    platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3627b13043be2a5afc4695f646ca3e323ea9483bf4794bc16fb5e51331448fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f88b77c2037a61eb21fe29e3f27c94a664f20de53f14f224723cffdb5555be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c089de7932e476602bc098ae47e356e9f5860cd84cdeaed5d8b90279890342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73133f30821f3fa4d55af9ea1928e47a5663a0ce3f98a2f5e19aebaaf2f11e7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41936c2d40d357169dbcd5260a434318660774f2b29c29da3288e5af12be7577(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77ac11684684b9bb72b872e9c6380ece7c4e758295a4fee695bdca8b3b31dad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89d1d0345ad7a762ea9be4a49982bb7dc401c76a39774a03c10a6f112df0ed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e944670d3e86a9bd0b9cd68438e0fd6bcf06add90ade5e9a23fc4e96d82c02f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117ce4a84081f4816f7794c78d75cdb0c7a36cabd16de31e3e3356208cd319a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DevicePostureRuleMatch]],
) -> None:
    """Type checking stubs"""
    pass
