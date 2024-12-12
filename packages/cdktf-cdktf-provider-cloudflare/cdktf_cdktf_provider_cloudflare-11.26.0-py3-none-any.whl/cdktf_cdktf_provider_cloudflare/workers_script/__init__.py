r'''
# `cloudflare_workers_script`

Refer to the Terraform Registry for docs: [`cloudflare_workers_script`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script).
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


class WorkersScript(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScript",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script cloudflare_workers_script}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        content: builtins.str,
        name: builtins.str,
        analytics_engine_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptAnalyticsEngineBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_database_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptD1DatabaseBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dispatch_namespace: typing.Optional[builtins.str] = None,
        hyperdrive_config_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptHyperdriveConfigBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kv_namespace_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptKvNamespaceBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logpush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        module: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlacement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        plain_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlainTextBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        queue_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptQueueBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        r2_bucket_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptR2BucketBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptSecretTextBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptServiceBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        webassembly_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptWebassemblyBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script cloudflare_workers_script} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#account_id WorkersScript#account_id}
        :param content: The script content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#content WorkersScript#content}
        :param name: The name for the script. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param analytics_engine_binding: analytics_engine_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#analytics_engine_binding WorkersScript#analytics_engine_binding}
        :param compatibility_date: The date to use for the compatibility flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_date WorkersScript#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Worker Scripts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_flags WorkersScript#compatibility_flags}
        :param d1_database_binding: d1_database_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#d1_database_binding WorkersScript#d1_database_binding}
        :param dispatch_namespace: Name of the Workers for Platforms dispatch namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#dispatch_namespace WorkersScript#dispatch_namespace}
        :param hyperdrive_config_binding: hyperdrive_config_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#hyperdrive_config_binding WorkersScript#hyperdrive_config_binding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#id WorkersScript#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kv_namespace_binding: kv_namespace_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#kv_namespace_binding WorkersScript#kv_namespace_binding}
        :param logpush: Enabling allows Worker events to be sent to a defined Logpush destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#logpush WorkersScript#logpush}
        :param module: Whether to upload Worker as a module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#module WorkersScript#module}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#placement WorkersScript#placement}
        :param plain_text_binding: plain_text_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#plain_text_binding WorkersScript#plain_text_binding}
        :param queue_binding: queue_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#queue_binding WorkersScript#queue_binding}
        :param r2_bucket_binding: r2_bucket_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#r2_bucket_binding WorkersScript#r2_bucket_binding}
        :param secret_text_binding: secret_text_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#secret_text_binding WorkersScript#secret_text_binding}
        :param service_binding: service_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#service_binding WorkersScript#service_binding}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#tags WorkersScript#tags}.
        :param webassembly_binding: webassembly_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#webassembly_binding WorkersScript#webassembly_binding}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff91a65eae39ed03c4fdb5f548361f58aa71f020d925825809f305475cc24e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkersScriptConfig(
            account_id=account_id,
            content=content,
            name=name,
            analytics_engine_binding=analytics_engine_binding,
            compatibility_date=compatibility_date,
            compatibility_flags=compatibility_flags,
            d1_database_binding=d1_database_binding,
            dispatch_namespace=dispatch_namespace,
            hyperdrive_config_binding=hyperdrive_config_binding,
            id=id,
            kv_namespace_binding=kv_namespace_binding,
            logpush=logpush,
            module=module,
            placement=placement,
            plain_text_binding=plain_text_binding,
            queue_binding=queue_binding,
            r2_bucket_binding=r2_bucket_binding,
            secret_text_binding=secret_text_binding,
            service_binding=service_binding,
            tags=tags,
            webassembly_binding=webassembly_binding,
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
        '''Generates CDKTF code for importing a WorkersScript resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkersScript to import.
        :param import_from_id: The id of the existing WorkersScript that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkersScript to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a18d8db56da9a802f4ab3dc8c0f4b0e47025df295217c56f9931fd59facc2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAnalyticsEngineBinding")
    def put_analytics_engine_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptAnalyticsEngineBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b284cd52abf3330ce846ca4910bf88ac48c22b1588feb61d55abdfb57d59b2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnalyticsEngineBinding", [value]))

    @jsii.member(jsii_name="putD1DatabaseBinding")
    def put_d1_database_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptD1DatabaseBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1da351b188a4d92534f23217041a343176dfaa3010965410a3ba51c18a675a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putD1DatabaseBinding", [value]))

    @jsii.member(jsii_name="putHyperdriveConfigBinding")
    def put_hyperdrive_config_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptHyperdriveConfigBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96ba4dd5b9b6c8f83872f766e7e472de7b41b8d411ea1b45782e0b7afa24468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHyperdriveConfigBinding", [value]))

    @jsii.member(jsii_name="putKvNamespaceBinding")
    def put_kv_namespace_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptKvNamespaceBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562e52ccbbdc7121b1192a0816d3c5d20e5e48ee5ac9cc705459e4eac1d112c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKvNamespaceBinding", [value]))

    @jsii.member(jsii_name="putPlacement")
    def put_placement(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlacement", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bb0689f27e14d9bc93c5ef631d99e259b44a267f88002d1dfbbd96a50cd1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlacement", [value]))

    @jsii.member(jsii_name="putPlainTextBinding")
    def put_plain_text_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlainTextBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aad1632bce65e6e9428e55ceff9e43eb482f43035ec4598cc545965e0ec4da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlainTextBinding", [value]))

    @jsii.member(jsii_name="putQueueBinding")
    def put_queue_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptQueueBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d482afd01f75176235c60c5334d91459b6d2e8cf89497a5e7cfed324d170125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueueBinding", [value]))

    @jsii.member(jsii_name="putR2BucketBinding")
    def put_r2_bucket_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptR2BucketBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67b4d3291a499ea502a51f847b84d9edc7136e19aee04e481d4da2735436a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putR2BucketBinding", [value]))

    @jsii.member(jsii_name="putSecretTextBinding")
    def put_secret_text_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptSecretTextBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663e0d427f90a564e3f9f55ada5a5eeecd402d9beb540f8006d8a2c8275d4c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretTextBinding", [value]))

    @jsii.member(jsii_name="putServiceBinding")
    def put_service_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptServiceBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb71ae57dedb677dd58bc43a81d2a052b84b211b8191cd6df8516a9a32bd4fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceBinding", [value]))

    @jsii.member(jsii_name="putWebassemblyBinding")
    def put_webassembly_binding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptWebassemblyBinding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018c62df0096a078098368f2d220168f8028f8ecfc523d95d890a6fbb9aa5694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWebassemblyBinding", [value]))

    @jsii.member(jsii_name="resetAnalyticsEngineBinding")
    def reset_analytics_engine_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticsEngineBinding", []))

    @jsii.member(jsii_name="resetCompatibilityDate")
    def reset_compatibility_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityDate", []))

    @jsii.member(jsii_name="resetCompatibilityFlags")
    def reset_compatibility_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompatibilityFlags", []))

    @jsii.member(jsii_name="resetD1DatabaseBinding")
    def reset_d1_database_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetD1DatabaseBinding", []))

    @jsii.member(jsii_name="resetDispatchNamespace")
    def reset_dispatch_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDispatchNamespace", []))

    @jsii.member(jsii_name="resetHyperdriveConfigBinding")
    def reset_hyperdrive_config_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHyperdriveConfigBinding", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKvNamespaceBinding")
    def reset_kv_namespace_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKvNamespaceBinding", []))

    @jsii.member(jsii_name="resetLogpush")
    def reset_logpush(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogpush", []))

    @jsii.member(jsii_name="resetModule")
    def reset_module(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModule", []))

    @jsii.member(jsii_name="resetPlacement")
    def reset_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacement", []))

    @jsii.member(jsii_name="resetPlainTextBinding")
    def reset_plain_text_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlainTextBinding", []))

    @jsii.member(jsii_name="resetQueueBinding")
    def reset_queue_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueBinding", []))

    @jsii.member(jsii_name="resetR2BucketBinding")
    def reset_r2_bucket_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetR2BucketBinding", []))

    @jsii.member(jsii_name="resetSecretTextBinding")
    def reset_secret_text_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretTextBinding", []))

    @jsii.member(jsii_name="resetServiceBinding")
    def reset_service_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceBinding", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetWebassemblyBinding")
    def reset_webassembly_binding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebassemblyBinding", []))

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
    @jsii.member(jsii_name="analyticsEngineBinding")
    def analytics_engine_binding(self) -> "WorkersScriptAnalyticsEngineBindingList":
        return typing.cast("WorkersScriptAnalyticsEngineBindingList", jsii.get(self, "analyticsEngineBinding"))

    @builtins.property
    @jsii.member(jsii_name="d1DatabaseBinding")
    def d1_database_binding(self) -> "WorkersScriptD1DatabaseBindingList":
        return typing.cast("WorkersScriptD1DatabaseBindingList", jsii.get(self, "d1DatabaseBinding"))

    @builtins.property
    @jsii.member(jsii_name="hyperdriveConfigBinding")
    def hyperdrive_config_binding(self) -> "WorkersScriptHyperdriveConfigBindingList":
        return typing.cast("WorkersScriptHyperdriveConfigBindingList", jsii.get(self, "hyperdriveConfigBinding"))

    @builtins.property
    @jsii.member(jsii_name="kvNamespaceBinding")
    def kv_namespace_binding(self) -> "WorkersScriptKvNamespaceBindingList":
        return typing.cast("WorkersScriptKvNamespaceBindingList", jsii.get(self, "kvNamespaceBinding"))

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> "WorkersScriptPlacementList":
        return typing.cast("WorkersScriptPlacementList", jsii.get(self, "placement"))

    @builtins.property
    @jsii.member(jsii_name="plainTextBinding")
    def plain_text_binding(self) -> "WorkersScriptPlainTextBindingList":
        return typing.cast("WorkersScriptPlainTextBindingList", jsii.get(self, "plainTextBinding"))

    @builtins.property
    @jsii.member(jsii_name="queueBinding")
    def queue_binding(self) -> "WorkersScriptQueueBindingList":
        return typing.cast("WorkersScriptQueueBindingList", jsii.get(self, "queueBinding"))

    @builtins.property
    @jsii.member(jsii_name="r2BucketBinding")
    def r2_bucket_binding(self) -> "WorkersScriptR2BucketBindingList":
        return typing.cast("WorkersScriptR2BucketBindingList", jsii.get(self, "r2BucketBinding"))

    @builtins.property
    @jsii.member(jsii_name="secretTextBinding")
    def secret_text_binding(self) -> "WorkersScriptSecretTextBindingList":
        return typing.cast("WorkersScriptSecretTextBindingList", jsii.get(self, "secretTextBinding"))

    @builtins.property
    @jsii.member(jsii_name="serviceBinding")
    def service_binding(self) -> "WorkersScriptServiceBindingList":
        return typing.cast("WorkersScriptServiceBindingList", jsii.get(self, "serviceBinding"))

    @builtins.property
    @jsii.member(jsii_name="webassemblyBinding")
    def webassembly_binding(self) -> "WorkersScriptWebassemblyBindingList":
        return typing.cast("WorkersScriptWebassemblyBindingList", jsii.get(self, "webassemblyBinding"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticsEngineBindingInput")
    def analytics_engine_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptAnalyticsEngineBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptAnalyticsEngineBinding"]]], jsii.get(self, "analyticsEngineBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityDateInput")
    def compatibility_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compatibilityDateInput"))

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlagsInput")
    def compatibility_flags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibilityFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="d1DatabaseBindingInput")
    def d1_database_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptD1DatabaseBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptD1DatabaseBinding"]]], jsii.get(self, "d1DatabaseBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="dispatchNamespaceInput")
    def dispatch_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dispatchNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="hyperdriveConfigBindingInput")
    def hyperdrive_config_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptHyperdriveConfigBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptHyperdriveConfigBinding"]]], jsii.get(self, "hyperdriveConfigBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kvNamespaceBindingInput")
    def kv_namespace_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptKvNamespaceBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptKvNamespaceBinding"]]], jsii.get(self, "kvNamespaceBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="logpushInput")
    def logpush_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logpushInput"))

    @builtins.property
    @jsii.member(jsii_name="moduleInput")
    def module_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "moduleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlacement"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlacement"]]], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="plainTextBindingInput")
    def plain_text_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlainTextBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlainTextBinding"]]], jsii.get(self, "plainTextBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="queueBindingInput")
    def queue_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptQueueBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptQueueBinding"]]], jsii.get(self, "queueBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="r2BucketBindingInput")
    def r2_bucket_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptR2BucketBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptR2BucketBinding"]]], jsii.get(self, "r2BucketBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTextBindingInput")
    def secret_text_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptSecretTextBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptSecretTextBinding"]]], jsii.get(self, "secretTextBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceBindingInput")
    def service_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptServiceBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptServiceBinding"]]], jsii.get(self, "serviceBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="webassemblyBindingInput")
    def webassembly_binding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptWebassemblyBinding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptWebassemblyBinding"]]], jsii.get(self, "webassemblyBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2ca3c27f6a6700ee28e3832fcae15db049a5d2723a9a5abd3bd88fc910c53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compatibilityDate")
    def compatibility_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compatibilityDate"))

    @compatibility_date.setter
    def compatibility_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a46bd088570853c2b5d25072bad96f40225ab4162b4c5b1822d3c87bd6810a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compatibilityFlags")
    def compatibility_flags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "compatibilityFlags"))

    @compatibility_flags.setter
    def compatibility_flags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__decdadb6de4f79ad4960d73aa391c3abf6546ecb024fa20d96613a183d671be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compatibilityFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020e04151b7603f4ce7a71ecc71bbe500fe9298103161c4ea64a898fc07bbe21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dispatchNamespace")
    def dispatch_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dispatchNamespace"))

    @dispatch_namespace.setter
    def dispatch_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76e54b683923451d633c1f59ea6b113ec7b2c62e8bbe0cb8929ab4181df57db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dispatchNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffa8322b7eb33a35cedd4f0f9dedbc03a6f609ee4b41955827496fba26b0cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logpush")
    def logpush(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logpush"))

    @logpush.setter
    def logpush(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15514dbe74dbfe1fad3f9886bc5c24270ced70991f6ab14e8672103ae6fc8b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logpush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "module"))

    @module.setter
    def module(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38861057baa3ad294979833ae4baa7279e49ebc7f7d2f3c8ef8ad299320afa9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec753b3fb07ea8cfab1b999f2a5e5797e7224fe7ab98ddb483999a13b791559e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7008160e54047a6698cb0ad318ee82896ce02df4a7fad3bc0fed95317998bce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptAnalyticsEngineBinding",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset", "name": "name"},
)
class WorkersScriptAnalyticsEngineBinding:
    def __init__(self, *, dataset: builtins.str, name: builtins.str) -> None:
        '''
        :param dataset: The name of the Analytics Engine dataset to write to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#dataset WorkersScript#dataset}
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9621c851aaae3af69caba697fce7b95b3c92dd323ec0ff5fb69ff6bd39e98407)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
            "name": name,
        }

    @builtins.property
    def dataset(self) -> builtins.str:
        '''The name of the Analytics Engine dataset to write to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#dataset WorkersScript#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptAnalyticsEngineBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptAnalyticsEngineBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptAnalyticsEngineBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52d196dc7b449c7c1b93715dd87b69d6160781026fcc9f5c2e30acadc8db263)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptAnalyticsEngineBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c65f8ef1f866940a41daaabc9b25e484d6f36eef4f5b56ba25c9827df33f28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptAnalyticsEngineBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b5050efc42adf984187bf6343c9478befe6f680dd741fd59ec3439ef1082b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a11aa7fc665ceedf1283b2d58886f439408678e15e864838e8d9325d6fee5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd139eedc92cc3817b252f187002d42f6cc3143dc5f45754bccd9170545ac2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff730b441722e2f46fde4cef1d0651ae1f60b9bf772efd4fc03fff04eede02a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptAnalyticsEngineBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptAnalyticsEngineBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4604361c9d9b66d34b36bdf8262926a987792ad7a9a4bc062e00ac5c8a7ba3f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1843e7278c7d3bf8d4d8d806179d376fcce101ba38076ef068f7d99dd72eee35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1d3fd09b790de0156684a82ff207ec1b4b2cf295e83c1bcb080a9da19d1aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptAnalyticsEngineBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptAnalyticsEngineBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptAnalyticsEngineBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2daf848cf4cd762df7ea3ab77be82186400c98306b775ab449d78b4ad0a44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptConfig",
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
        "content": "content",
        "name": "name",
        "analytics_engine_binding": "analyticsEngineBinding",
        "compatibility_date": "compatibilityDate",
        "compatibility_flags": "compatibilityFlags",
        "d1_database_binding": "d1DatabaseBinding",
        "dispatch_namespace": "dispatchNamespace",
        "hyperdrive_config_binding": "hyperdriveConfigBinding",
        "id": "id",
        "kv_namespace_binding": "kvNamespaceBinding",
        "logpush": "logpush",
        "module": "module",
        "placement": "placement",
        "plain_text_binding": "plainTextBinding",
        "queue_binding": "queueBinding",
        "r2_bucket_binding": "r2BucketBinding",
        "secret_text_binding": "secretTextBinding",
        "service_binding": "serviceBinding",
        "tags": "tags",
        "webassembly_binding": "webassemblyBinding",
    },
)
class WorkersScriptConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        content: builtins.str,
        name: builtins.str,
        analytics_engine_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptAnalyticsEngineBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
        compatibility_date: typing.Optional[builtins.str] = None,
        compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        d1_database_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptD1DatabaseBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dispatch_namespace: typing.Optional[builtins.str] = None,
        hyperdrive_config_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptHyperdriveConfigBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        kv_namespace_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptKvNamespaceBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        logpush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        module: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlacement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        plain_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptPlainTextBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        queue_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptQueueBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        r2_bucket_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptR2BucketBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptSecretTextBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptServiceBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        webassembly_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkersScriptWebassemblyBinding", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#account_id WorkersScript#account_id}
        :param content: The script content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#content WorkersScript#content}
        :param name: The name for the script. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param analytics_engine_binding: analytics_engine_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#analytics_engine_binding WorkersScript#analytics_engine_binding}
        :param compatibility_date: The date to use for the compatibility flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_date WorkersScript#compatibility_date}
        :param compatibility_flags: Compatibility flags used for Worker Scripts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_flags WorkersScript#compatibility_flags}
        :param d1_database_binding: d1_database_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#d1_database_binding WorkersScript#d1_database_binding}
        :param dispatch_namespace: Name of the Workers for Platforms dispatch namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#dispatch_namespace WorkersScript#dispatch_namespace}
        :param hyperdrive_config_binding: hyperdrive_config_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#hyperdrive_config_binding WorkersScript#hyperdrive_config_binding}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#id WorkersScript#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kv_namespace_binding: kv_namespace_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#kv_namespace_binding WorkersScript#kv_namespace_binding}
        :param logpush: Enabling allows Worker events to be sent to a defined Logpush destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#logpush WorkersScript#logpush}
        :param module: Whether to upload Worker as a module. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#module WorkersScript#module}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#placement WorkersScript#placement}
        :param plain_text_binding: plain_text_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#plain_text_binding WorkersScript#plain_text_binding}
        :param queue_binding: queue_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#queue_binding WorkersScript#queue_binding}
        :param r2_bucket_binding: r2_bucket_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#r2_bucket_binding WorkersScript#r2_bucket_binding}
        :param secret_text_binding: secret_text_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#secret_text_binding WorkersScript#secret_text_binding}
        :param service_binding: service_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#service_binding WorkersScript#service_binding}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#tags WorkersScript#tags}.
        :param webassembly_binding: webassembly_binding block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#webassembly_binding WorkersScript#webassembly_binding}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff7b79f452a4dac9e7059b6adbee078a1b1970a8ad1c6c8b7a71849b9988441)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument analytics_engine_binding", value=analytics_engine_binding, expected_type=type_hints["analytics_engine_binding"])
            check_type(argname="argument compatibility_date", value=compatibility_date, expected_type=type_hints["compatibility_date"])
            check_type(argname="argument compatibility_flags", value=compatibility_flags, expected_type=type_hints["compatibility_flags"])
            check_type(argname="argument d1_database_binding", value=d1_database_binding, expected_type=type_hints["d1_database_binding"])
            check_type(argname="argument dispatch_namespace", value=dispatch_namespace, expected_type=type_hints["dispatch_namespace"])
            check_type(argname="argument hyperdrive_config_binding", value=hyperdrive_config_binding, expected_type=type_hints["hyperdrive_config_binding"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kv_namespace_binding", value=kv_namespace_binding, expected_type=type_hints["kv_namespace_binding"])
            check_type(argname="argument logpush", value=logpush, expected_type=type_hints["logpush"])
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument plain_text_binding", value=plain_text_binding, expected_type=type_hints["plain_text_binding"])
            check_type(argname="argument queue_binding", value=queue_binding, expected_type=type_hints["queue_binding"])
            check_type(argname="argument r2_bucket_binding", value=r2_bucket_binding, expected_type=type_hints["r2_bucket_binding"])
            check_type(argname="argument secret_text_binding", value=secret_text_binding, expected_type=type_hints["secret_text_binding"])
            check_type(argname="argument service_binding", value=service_binding, expected_type=type_hints["service_binding"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument webassembly_binding", value=webassembly_binding, expected_type=type_hints["webassembly_binding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "content": content,
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
        if analytics_engine_binding is not None:
            self._values["analytics_engine_binding"] = analytics_engine_binding
        if compatibility_date is not None:
            self._values["compatibility_date"] = compatibility_date
        if compatibility_flags is not None:
            self._values["compatibility_flags"] = compatibility_flags
        if d1_database_binding is not None:
            self._values["d1_database_binding"] = d1_database_binding
        if dispatch_namespace is not None:
            self._values["dispatch_namespace"] = dispatch_namespace
        if hyperdrive_config_binding is not None:
            self._values["hyperdrive_config_binding"] = hyperdrive_config_binding
        if id is not None:
            self._values["id"] = id
        if kv_namespace_binding is not None:
            self._values["kv_namespace_binding"] = kv_namespace_binding
        if logpush is not None:
            self._values["logpush"] = logpush
        if module is not None:
            self._values["module"] = module
        if placement is not None:
            self._values["placement"] = placement
        if plain_text_binding is not None:
            self._values["plain_text_binding"] = plain_text_binding
        if queue_binding is not None:
            self._values["queue_binding"] = queue_binding
        if r2_bucket_binding is not None:
            self._values["r2_bucket_binding"] = r2_bucket_binding
        if secret_text_binding is not None:
            self._values["secret_text_binding"] = secret_text_binding
        if service_binding is not None:
            self._values["service_binding"] = service_binding
        if tags is not None:
            self._values["tags"] = tags
        if webassembly_binding is not None:
            self._values["webassembly_binding"] = webassembly_binding

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#account_id WorkersScript#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> builtins.str:
        '''The script content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#content WorkersScript#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the script. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytics_engine_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]]:
        '''analytics_engine_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#analytics_engine_binding WorkersScript#analytics_engine_binding}
        '''
        result = self._values.get("analytics_engine_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]], result)

    @builtins.property
    def compatibility_date(self) -> typing.Optional[builtins.str]:
        '''The date to use for the compatibility flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_date WorkersScript#compatibility_date}
        '''
        result = self._values.get("compatibility_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compatibility_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Compatibility flags used for Worker Scripts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#compatibility_flags WorkersScript#compatibility_flags}
        '''
        result = self._values.get("compatibility_flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def d1_database_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptD1DatabaseBinding"]]]:
        '''d1_database_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#d1_database_binding WorkersScript#d1_database_binding}
        '''
        result = self._values.get("d1_database_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptD1DatabaseBinding"]]], result)

    @builtins.property
    def dispatch_namespace(self) -> typing.Optional[builtins.str]:
        '''Name of the Workers for Platforms dispatch namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#dispatch_namespace WorkersScript#dispatch_namespace}
        '''
        result = self._values.get("dispatch_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hyperdrive_config_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptHyperdriveConfigBinding"]]]:
        '''hyperdrive_config_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#hyperdrive_config_binding WorkersScript#hyperdrive_config_binding}
        '''
        result = self._values.get("hyperdrive_config_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptHyperdriveConfigBinding"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#id WorkersScript#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kv_namespace_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptKvNamespaceBinding"]]]:
        '''kv_namespace_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#kv_namespace_binding WorkersScript#kv_namespace_binding}
        '''
        result = self._values.get("kv_namespace_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptKvNamespaceBinding"]]], result)

    @builtins.property
    def logpush(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling allows Worker events to be sent to a defined Logpush destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#logpush WorkersScript#logpush}
        '''
        result = self._values.get("logpush")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def module(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to upload Worker as a module.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#module WorkersScript#module}
        '''
        result = self._values.get("module")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def placement(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlacement"]]]:
        '''placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#placement WorkersScript#placement}
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlacement"]]], result)

    @builtins.property
    def plain_text_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlainTextBinding"]]]:
        '''plain_text_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#plain_text_binding WorkersScript#plain_text_binding}
        '''
        result = self._values.get("plain_text_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptPlainTextBinding"]]], result)

    @builtins.property
    def queue_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptQueueBinding"]]]:
        '''queue_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#queue_binding WorkersScript#queue_binding}
        '''
        result = self._values.get("queue_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptQueueBinding"]]], result)

    @builtins.property
    def r2_bucket_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptR2BucketBinding"]]]:
        '''r2_bucket_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#r2_bucket_binding WorkersScript#r2_bucket_binding}
        '''
        result = self._values.get("r2_bucket_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptR2BucketBinding"]]], result)

    @builtins.property
    def secret_text_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptSecretTextBinding"]]]:
        '''secret_text_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#secret_text_binding WorkersScript#secret_text_binding}
        '''
        result = self._values.get("secret_text_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptSecretTextBinding"]]], result)

    @builtins.property
    def service_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptServiceBinding"]]]:
        '''service_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#service_binding WorkersScript#service_binding}
        '''
        result = self._values.get("service_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptServiceBinding"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#tags WorkersScript#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def webassembly_binding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptWebassemblyBinding"]]]:
        '''webassembly_binding block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#webassembly_binding WorkersScript#webassembly_binding}
        '''
        result = self._values.get("webassembly_binding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkersScriptWebassemblyBinding"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptD1DatabaseBinding",
    jsii_struct_bases=[],
    name_mapping={"database_id": "databaseId", "name": "name"},
)
class WorkersScriptD1DatabaseBinding:
    def __init__(self, *, database_id: builtins.str, name: builtins.str) -> None:
        '''
        :param database_id: Database ID of D1 database to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#database_id WorkersScript#database_id}
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7232f89aadc69c774a7f8feac025bd52afa312d7ec92117f43e7f598221dbd1)
            check_type(argname="argument database_id", value=database_id, expected_type=type_hints["database_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_id": database_id,
            "name": name,
        }

    @builtins.property
    def database_id(self) -> builtins.str:
        '''Database ID of D1 database to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#database_id WorkersScript#database_id}
        '''
        result = self._values.get("database_id")
        assert result is not None, "Required property 'database_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptD1DatabaseBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptD1DatabaseBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptD1DatabaseBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1d659919ad42630e2826ffab5b26b11c365631ee10fc136606edefb2749b67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptD1DatabaseBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fa5d5e3c7a08d82e4a4ef6e2181db247cb1d936bb14de4094a5db7fe3b1551)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptD1DatabaseBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03fc65256afbe1b4076878df545a74284e5434bfc7d69d98d6056193a03de6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__805404daa0ff5ec5141f65078847a27745e3630ca161d2fb7a1a6fd9b0b9161d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45ba930095d2eb73d8a0bc4e89054ff5bf8ef2b8ed716c0e8024c8a28989bd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptD1DatabaseBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptD1DatabaseBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptD1DatabaseBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824ca2283a740369f43bd8c37cf8805f38fa258aef01629ebff0bf3a916d1a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptD1DatabaseBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptD1DatabaseBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a287c62f734bedf5306b1b49adeb4a011d0fbcd741d3f328303250f2ac4f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="databaseIdInput")
    def database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseId")
    def database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseId"))

    @database_id.setter
    def database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1444535ff43683f2bb9360401c5889b4873e5c9a93356605beea82d05e808921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1abb879ccdf91ac69bef673c0275c23f727eb760cc6f987985b27773285092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptD1DatabaseBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptD1DatabaseBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptD1DatabaseBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf942cb10224aad01bb1b44558b1e3a6e50bc0a1e054359b6868ae12a29997e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptHyperdriveConfigBinding",
    jsii_struct_bases=[],
    name_mapping={"binding": "binding", "id": "id"},
)
class WorkersScriptHyperdriveConfigBinding:
    def __init__(self, *, binding: builtins.str, id: builtins.str) -> None:
        '''
        :param binding: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#binding WorkersScript#binding}
        :param id: The ID of the Hyperdrive config to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#id WorkersScript#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e145021a11811890cc9d33de0ec52fc16b8039fbf7d11faac6be0c4149f3124b)
            check_type(argname="argument binding", value=binding, expected_type=type_hints["binding"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "binding": binding,
            "id": id,
        }

    @builtins.property
    def binding(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#binding WorkersScript#binding}
        '''
        result = self._values.get("binding")
        assert result is not None, "Required property 'binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The ID of the Hyperdrive config to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#id WorkersScript#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptHyperdriveConfigBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptHyperdriveConfigBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptHyperdriveConfigBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4403b3d630cc3979f8a53e894c79e08c9635cf5fecff03bbb6d2f3d9fa275c1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptHyperdriveConfigBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac579c9604ad802883490df9c74a13b68dc81cc84b849d792ffba37d7f5dc926)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptHyperdriveConfigBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22696c4da332a0addf9595dd425e96fbebd25c938a7b4af92142cb0212fa2ba5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8939c7da65d3e7b48664cc0a039272889be330ac4b57c9d43244e87ba79377fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__879ae2075d820707f4a75aadec152cc08dc1fd4269dcabb305fa5a631ee3a4b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptHyperdriveConfigBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptHyperdriveConfigBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptHyperdriveConfigBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edae2755fe6b72517d77fce67db8cfddab9201232759856211a767233fc7063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptHyperdriveConfigBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptHyperdriveConfigBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae478a297bb0a3310b551f005ee2b4f268d9318aaa98a3a09df25f1bf174a941)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bindingInput")
    def binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="binding")
    def binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binding"))

    @binding.setter
    def binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602c07e839e9599bdedfe40f4c3c4a1c8614dfc6764b9375dfa08858bfe6708d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd30c38ccf81910adc53cd7cd287d30d2ce3af9cbaf644364dd5a861344db21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptHyperdriveConfigBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptHyperdriveConfigBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptHyperdriveConfigBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b404598a2eac040918a46b38cbb19c171d26112ecb92b1c5051a8271be0526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptKvNamespaceBinding",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace_id": "namespaceId"},
)
class WorkersScriptKvNamespaceBinding:
    def __init__(self, *, name: builtins.str, namespace_id: builtins.str) -> None:
        '''
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param namespace_id: ID of the KV namespace you want to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#namespace_id WorkersScript#namespace_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd33229aeb920fb4d7b72e9a3dfc1256300aff0789474b16be0f4d55ba750b00)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace_id": namespace_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> builtins.str:
        '''ID of the KV namespace you want to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#namespace_id WorkersScript#namespace_id}
        '''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptKvNamespaceBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptKvNamespaceBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptKvNamespaceBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97203cbccf54457c3a00dd501fa92f2e84397ecabc1f89c5c2e021085d32f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptKvNamespaceBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a822d9f7aefb86272ad326445512af3dc917424de5b47b2956693fa1a07a7f29)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptKvNamespaceBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a40ee8ed4a0af6e89b964b2427c7b69345b50d513bb0695038022820555f1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ea64b3e4344b92670f80200c0544459a3fca79159fff36d7a7c1dc1ca5574a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc25029c3fab05cbf864960d79a9108e65b958b34a60c2f1dad9ea97a0d8b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptKvNamespaceBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptKvNamespaceBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptKvNamespaceBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae6dca037c6f0f7b9364faa5808c1799a5832970f743f6101af5f3927ffb0ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptKvNamespaceBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptKvNamespaceBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8231f4ffd670176ffa1a108d4aed6ae382d2ed0895e4337164b4a3835554969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceIdInput")
    def namespace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949c2fc55b1bbe0ff049dac439f7d161cdf236e6e19e389cafdb1801bd317e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c959b5bef9a8985e09fdd51dd454d024545cefdcca8770a4372010e3e2efdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptKvNamespaceBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptKvNamespaceBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptKvNamespaceBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433c20234cff06c4ba1847942af45f938a43f8fca8d0b44ae43bf811b8ad2fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlacement",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class WorkersScriptPlacement:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: The placement mode for the Worker. Available values: ``smart``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#mode WorkersScript#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e4978ff81453269afcd828d0429a67b9641991131251e08ef91557a3cab1ea)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''The placement mode for the Worker. Available values: ``smart``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#mode WorkersScript#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptPlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptPlacementList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlacementList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__238dbbce4a1786bc8158a654c960e668fa3428222c8a4875c01cec74453a3e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkersScriptPlacementOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7b258f37b97b1130dede02bb4357e6f071eee60e19d0c54f33a4e8e0b754fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptPlacementOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d86de14147b0113e06e7869affbbbdbff2d3e1ab613275580459148f4029c77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b495204c824fb0f8e1343d57cb764c1fbcc91fb2dc8c1c60a71a0823c352c1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e732fc6124f25d8e05379f0cb95e92a62b235c527e413981d6e40317d78b041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlacement]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlacement]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlacement]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f0d1515eb820bbb564034b6111dfa841ce8e753f809d0c9be4011bf7ab5cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptPlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0a158c6e91af48c4f305bec5f3dd074b7898a16087f8fb8d6760231f63f750f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efbc9bf511fddd2db4b69eab68daae2a4eb96a27da4c0d7144c960dd2835f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlacement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlacement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlacement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ccdfa338a27dc2280667eadc3dfa61b4800c5eb4db50906cc4755c705744a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlainTextBinding",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "text": "text"},
)
class WorkersScriptPlainTextBinding:
    def __init__(self, *, name: builtins.str, text: builtins.str) -> None:
        '''
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param text: The plain text you want to store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#text WorkersScript#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bc19489586dc614f32d680138d7e8ee42ed192463d72f077a96422147b64b3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "text": text,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''The plain text you want to store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#text WorkersScript#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptPlainTextBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptPlainTextBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlainTextBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60c80bff52613efb43c498249c2b4a31671c8a6d4292a4e666517ffbc44f859d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkersScriptPlainTextBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df204ec9e5a71ed50a3eb8352259b65bc0fb4741f6b154b24c1667dd5e27a36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptPlainTextBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ceb884aa61ab0b9beb342e6fd5a75eac3174584db1b2f24d134ecf0238bdb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__160d83b3f8fe5e38ed837c8040861b243617774aa6e3f34f4cb06325dfcf3eb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5c006298d6a46fc831e3558d28c6dfa5ca9340d50965a5d5be00a54bfe7777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlainTextBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlainTextBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlainTextBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6dea5e16ff756619d73a04e7bd96bf354ed76e139d557e6e0017db4aefa9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptPlainTextBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptPlainTextBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb74365645e95c3b142d5324549bf71fa1ffa2eb92c7ddfa63cd48587b4ab359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c92a4257f2a1fe67a2430bc1a6c456ae04b8f660f92a8c72e640d24c9c637d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e803c6691bf9821b22b7731add4adcdb4427a9e878ae82f1e84d758faeb5d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlainTextBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlainTextBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlainTextBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7666f5663121fd5d31cbe1117d9ab863cd6383186357157eaa2b8ee981b642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptQueueBinding",
    jsii_struct_bases=[],
    name_mapping={"binding": "binding", "queue": "queue"},
)
class WorkersScriptQueueBinding:
    def __init__(self, *, binding: builtins.str, queue: builtins.str) -> None:
        '''
        :param binding: The name of the global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#binding WorkersScript#binding}
        :param queue: Name of the queue you want to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#queue WorkersScript#queue}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe52fd50f2051f75a72f376f6399ed972846221ac672b524aa41f53bea537df)
            check_type(argname="argument binding", value=binding, expected_type=type_hints["binding"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "binding": binding,
            "queue": queue,
        }

    @builtins.property
    def binding(self) -> builtins.str:
        '''The name of the global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#binding WorkersScript#binding}
        '''
        result = self._values.get("binding")
        assert result is not None, "Required property 'binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def queue(self) -> builtins.str:
        '''Name of the queue you want to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#queue WorkersScript#queue}
        '''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptQueueBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptQueueBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptQueueBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf96a98c8ebf8a5de9957a9e70e7ad46ce4653843d4f6e7e425bd3e72f8a8e7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkersScriptQueueBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24215ec11bb5ba69bd9d36cf0b11358ee2e9d2514d1d35370b34bf6a53ed691f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptQueueBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f515d6ac71eea1adaec36ee7eb44fd8bf8ab4c5344a3e6703926245708b347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7f090d4a0dbea055f7c00c7948e1a543343f7cd48a69c6e5d1d37a0e404b05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1971b9741026b296e8bad9229c0cbf99355cd5b90283c285951f55105ea02eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptQueueBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptQueueBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptQueueBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf24edc7803b6df8181bdf279b903fa51e69425f98a7f742ffe4362174bcdc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptQueueBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptQueueBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a81abf938871d7942b30da4125a8a9b75e9a461be5ee33212e7243a163b876c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bindingInput")
    def binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bindingInput"))

    @builtins.property
    @jsii.member(jsii_name="queueInput")
    def queue_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueInput"))

    @builtins.property
    @jsii.member(jsii_name="binding")
    def binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binding"))

    @binding.setter
    def binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b99cb9a5aa63ef2b7ca9e691cf986c65454e9aae0a06ed66fa3399f896349b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queue")
    def queue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queue"))

    @queue.setter
    def queue(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce063396e430f7ab9872497e544de254fa7ceab5f6362ecee5e29165dfc2679e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptQueueBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptQueueBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptQueueBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33bf6e566c9c49921236d789e56182d2c308abcc0eafcdb574ed1eca21d54797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptR2BucketBinding",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "name": "name"},
)
class WorkersScriptR2BucketBinding:
    def __init__(self, *, bucket_name: builtins.str, name: builtins.str) -> None:
        '''
        :param bucket_name: The name of the Bucket to bind to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#bucket_name WorkersScript#bucket_name}
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb37f700731e28bf724ac24fbfb7e0185c2b37e13469a67d2d71654bf5a76997)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "name": name,
        }

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The name of the Bucket to bind to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#bucket_name WorkersScript#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptR2BucketBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptR2BucketBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptR2BucketBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d68393d142f60b1e1a3e1a8637fd66d89dce73204056c061977b0e2fd41b51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkersScriptR2BucketBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ad51572a61806a5d7f6b48a306991f37b4ceddabe8050c375fc4f83631c00d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptR2BucketBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362234e1d083b7c0a41ba4087a32faa29fd0c68c44236b3130a6098349837910)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16e90feb98153b9ccc526423d0314590606f384aeb67d54a1bfc18eaa27e2190)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c9340e984c15b21bab30a8d3ccfe28c04c9e2d5795715a2105ccf5eb3eb4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptR2BucketBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptR2BucketBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptR2BucketBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef6eee10120d7f7280b1d4ca677fa103827d8392a1ab23e59890c4667618c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptR2BucketBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptR2BucketBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c60a0d593acc3dd3f202b1b1d16976e6642db374fd361fc8b3bb70245be845f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45adaf1f063dcdf97a570f06191f07befad431c0233761060c2ffeb6739c9cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9296aece9fc207b813100762e69deeb15b56cfa9674e08be9969e7e040bed339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptR2BucketBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptR2BucketBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptR2BucketBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd8345c65d3c99f12d56b57dc73cc22d2cbb7aaeeab009b536d4b05542e3ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptSecretTextBinding",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "text": "text"},
)
class WorkersScriptSecretTextBinding:
    def __init__(self, *, name: builtins.str, text: builtins.str) -> None:
        '''
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param text: The secret text you want to store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#text WorkersScript#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca23dab904a7a222a276827b9799975a405c6a2509a272a9256d7b036de36d3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "text": text,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''The secret text you want to store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#text WorkersScript#text}
        '''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptSecretTextBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptSecretTextBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptSecretTextBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d302ab7d5f18bd1837dffbd00d8ec9f1dba4dfc950e6e48649916d4fe048f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptSecretTextBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28145a6315e9845db79e80e229f01b3660735dd09a3820f7248f7832e16b0a53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptSecretTextBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ed5b8e0a3fe0f10db1902c5b009d5b05761e037147798a1b724d7d4c1acb9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f92893afa7a270ea20c8449a6cc6e4c963856415d546a0a90abd275eaf6f49d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b32338acd0a705d7982957a5ed2a8307c86bd181d57ba289b1f1fcb51169fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptSecretTextBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptSecretTextBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptSecretTextBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8545fdf71644cd202e64487d8a7b8d1f5eaf45183930d263046ba350d5840d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptSecretTextBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptSecretTextBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d84ecef45c499d349c22a8f5853757959ba1f1fd431067384719b95826ee11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bc6c9b5683279d4c4e1f198eac1b9b385c22de597f2f4804ccbce92dbb073c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9926d1d4f6cd1b0ecf43363a3c1b2d978cfd9a6b8d1089411f48fe80ac2724c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptSecretTextBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptSecretTextBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptSecretTextBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75c654f66314d56e2283857a9923211013e624651d9e01c0d0b73338a02672a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptServiceBinding",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "service": "service", "environment": "environment"},
)
class WorkersScriptServiceBinding:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: builtins.str,
        environment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        :param service: The name of the Worker to bind to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#service WorkersScript#service}
        :param environment: The name of the Worker environment to bind to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#environment WorkersScript#environment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b7d21923d9754548ce0690a7013146e005f95370d0866ae8570c74d8407426)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service": service,
        }
        if environment is not None:
            self._values["environment"] = environment

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''The name of the Worker to bind to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#service WorkersScript#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''The name of the Worker environment to bind to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#environment WorkersScript#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptServiceBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptServiceBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptServiceBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__189c032e71c2b1d0cbbd9b996a8f5025db061f337f72672f416a8010fb2c72fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WorkersScriptServiceBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b3cb375fd6bed18367507e6ac2c256bcbee988fa4f65c4ea430b1ec8d8ce7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptServiceBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298a45f2f773bddf4fc0a4b1d5a89953737bd68695e3e76ded4b5d8b914fd6ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f280a19be520f4271adf27d0f45e8a41e5669ecda78abbb9c5d0a2d97eb5c5d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb2cb15e9b608c79aecdbb7591c4ffd8e0aa951cd16e3b046d8da81f6f5b6a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptServiceBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptServiceBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptServiceBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5265069da2eb4f39095f770177ba455e3cf7756aac1cc6235207321784dce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptServiceBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptServiceBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d8faddbf8793a51e2fd994f133d011347045c1b20d166861b534296f088b14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c748d2076d6f62249443cc260c8b57a92f2963a9b9efa0d1ae7b82cafcb171e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de54a9fe15803594f28eea393a12b44c521579550550cb5daf961c9908a00eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5e4600c5e749b44b73e194a1b16b82060b956292974893b4efe53d4dc02717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptServiceBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptServiceBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptServiceBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6070aecf63e09546c096a10895c31a378efb61c18c4628a612401db746f278b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptWebassemblyBinding",
    jsii_struct_bases=[],
    name_mapping={"module": "module", "name": "name"},
)
class WorkersScriptWebassemblyBinding:
    def __init__(self, *, module: builtins.str, name: builtins.str) -> None:
        '''
        :param module: The base64 encoded wasm module you want to store. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#module WorkersScript#module}
        :param name: The global variable for the binding in your Worker code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29250cd05f661568a7f48ad9c98e607917f8be197855c16c8b27cd6f6352944c)
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "module": module,
            "name": name,
        }

    @builtins.property
    def module(self) -> builtins.str:
        '''The base64 encoded wasm module you want to store.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#module WorkersScript#module}
        '''
        result = self._values.get("module")
        assert result is not None, "Required property 'module' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The global variable for the binding in your Worker code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/workers_script#name WorkersScript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkersScriptWebassemblyBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkersScriptWebassemblyBindingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptWebassemblyBindingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c9ca31d2b2136863ccce33f0324400e41c43f6870bdf12c34522116cc167e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkersScriptWebassemblyBindingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d16963e17ca5bb81b2169bb70a3b3af310955132aa558db7994c1c3797b4d51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkersScriptWebassemblyBindingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b652846a7ebe8b0f973bf86bb6c76885e6cc4a36d688325f0c0fb45901fd51d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5e5cad36d721699417536b08373c413e3a3b7052812461f97cc35e9172609e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86067c75de167084ba8f052e130db59e135fa33087d852dafcf7285f863cbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptWebassemblyBinding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptWebassemblyBinding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptWebassemblyBinding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9933c52a38d2b54ceb5f7815e078547aa547df774bf5b7399f17c6c017814c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkersScriptWebassemblyBindingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.workersScript.WorkersScriptWebassemblyBindingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72750d0f8cfd6bf37b5058721a6ceee693b68a64bb4b12b6e99544dc8e0c25fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="moduleInput")
    def module_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "moduleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="module")
    def module(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "module"))

    @module.setter
    def module(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d528ba94f47236324d5daded3bb6286256638508634db2c0f77e4f9f858d7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "module", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e1e0c63bb402f9c52deb742cdcc4d23e079d6ca770aa23b3d5c0acf53e2bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptWebassemblyBinding]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptWebassemblyBinding]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptWebassemblyBinding]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5485bc3ff4d48b5b74b34484c8eb631e2337b4e602c745ef6569124794f6bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkersScript",
    "WorkersScriptAnalyticsEngineBinding",
    "WorkersScriptAnalyticsEngineBindingList",
    "WorkersScriptAnalyticsEngineBindingOutputReference",
    "WorkersScriptConfig",
    "WorkersScriptD1DatabaseBinding",
    "WorkersScriptD1DatabaseBindingList",
    "WorkersScriptD1DatabaseBindingOutputReference",
    "WorkersScriptHyperdriveConfigBinding",
    "WorkersScriptHyperdriveConfigBindingList",
    "WorkersScriptHyperdriveConfigBindingOutputReference",
    "WorkersScriptKvNamespaceBinding",
    "WorkersScriptKvNamespaceBindingList",
    "WorkersScriptKvNamespaceBindingOutputReference",
    "WorkersScriptPlacement",
    "WorkersScriptPlacementList",
    "WorkersScriptPlacementOutputReference",
    "WorkersScriptPlainTextBinding",
    "WorkersScriptPlainTextBindingList",
    "WorkersScriptPlainTextBindingOutputReference",
    "WorkersScriptQueueBinding",
    "WorkersScriptQueueBindingList",
    "WorkersScriptQueueBindingOutputReference",
    "WorkersScriptR2BucketBinding",
    "WorkersScriptR2BucketBindingList",
    "WorkersScriptR2BucketBindingOutputReference",
    "WorkersScriptSecretTextBinding",
    "WorkersScriptSecretTextBindingList",
    "WorkersScriptSecretTextBindingOutputReference",
    "WorkersScriptServiceBinding",
    "WorkersScriptServiceBindingList",
    "WorkersScriptServiceBindingOutputReference",
    "WorkersScriptWebassemblyBinding",
    "WorkersScriptWebassemblyBindingList",
    "WorkersScriptWebassemblyBindingOutputReference",
]

publication.publish()

def _typecheckingstub__9ff91a65eae39ed03c4fdb5f548361f58aa71f020d925825809f305475cc24e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    content: builtins.str,
    name: builtins.str,
    analytics_engine_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptAnalyticsEngineBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compatibility_date: typing.Optional[builtins.str] = None,
    compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    d1_database_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptD1DatabaseBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dispatch_namespace: typing.Optional[builtins.str] = None,
    hyperdrive_config_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptHyperdriveConfigBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kv_namespace_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptKvNamespaceBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logpush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    module: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlacement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    plain_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlainTextBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    queue_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptQueueBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    r2_bucket_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptR2BucketBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptSecretTextBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptServiceBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    webassembly_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptWebassemblyBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b2a18d8db56da9a802f4ab3dc8c0f4b0e47025df295217c56f9931fd59facc2d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b284cd52abf3330ce846ca4910bf88ac48c22b1588feb61d55abdfb57d59b2bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptAnalyticsEngineBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1da351b188a4d92534f23217041a343176dfaa3010965410a3ba51c18a675a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptD1DatabaseBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96ba4dd5b9b6c8f83872f766e7e472de7b41b8d411ea1b45782e0b7afa24468(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptHyperdriveConfigBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562e52ccbbdc7121b1192a0816d3c5d20e5e48ee5ac9cc705459e4eac1d112c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptKvNamespaceBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb0689f27e14d9bc93c5ef631d99e259b44a267f88002d1dfbbd96a50cd1e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlacement, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aad1632bce65e6e9428e55ceff9e43eb482f43035ec4598cc545965e0ec4da8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlainTextBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d482afd01f75176235c60c5334d91459b6d2e8cf89497a5e7cfed324d170125(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptQueueBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67b4d3291a499ea502a51f847b84d9edc7136e19aee04e481d4da2735436a4d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptR2BucketBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663e0d427f90a564e3f9f55ada5a5eeecd402d9beb540f8006d8a2c8275d4c4f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptSecretTextBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb71ae57dedb677dd58bc43a81d2a052b84b211b8191cd6df8516a9a32bd4fdb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptServiceBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018c62df0096a078098368f2d220168f8028f8ecfc523d95d890a6fbb9aa5694(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptWebassemblyBinding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2ca3c27f6a6700ee28e3832fcae15db049a5d2723a9a5abd3bd88fc910c53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a46bd088570853c2b5d25072bad96f40225ab4162b4c5b1822d3c87bd6810a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decdadb6de4f79ad4960d73aa391c3abf6546ecb024fa20d96613a183d671be1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020e04151b7603f4ce7a71ecc71bbe500fe9298103161c4ea64a898fc07bbe21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76e54b683923451d633c1f59ea6b113ec7b2c62e8bbe0cb8929ab4181df57db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffa8322b7eb33a35cedd4f0f9dedbc03a6f609ee4b41955827496fba26b0cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15514dbe74dbfe1fad3f9886bc5c24270ced70991f6ab14e8672103ae6fc8b2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38861057baa3ad294979833ae4baa7279e49ebc7f7d2f3c8ef8ad299320afa9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec753b3fb07ea8cfab1b999f2a5e5797e7224fe7ab98ddb483999a13b791559e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7008160e54047a6698cb0ad318ee82896ce02df4a7fad3bc0fed95317998bce0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9621c851aaae3af69caba697fce7b95b3c92dd323ec0ff5fb69ff6bd39e98407(
    *,
    dataset: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52d196dc7b449c7c1b93715dd87b69d6160781026fcc9f5c2e30acadc8db263(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c65f8ef1f866940a41daaabc9b25e484d6f36eef4f5b56ba25c9827df33f28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b5050efc42adf984187bf6343c9478befe6f680dd741fd59ec3439ef1082b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a11aa7fc665ceedf1283b2d58886f439408678e15e864838e8d9325d6fee5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd139eedc92cc3817b252f187002d42f6cc3143dc5f45754bccd9170545ac2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff730b441722e2f46fde4cef1d0651ae1f60b9bf772efd4fc03fff04eede02a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptAnalyticsEngineBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4604361c9d9b66d34b36bdf8262926a987792ad7a9a4bc062e00ac5c8a7ba3f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1843e7278c7d3bf8d4d8d806179d376fcce101ba38076ef068f7d99dd72eee35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1d3fd09b790de0156684a82ff207ec1b4b2cf295e83c1bcb080a9da19d1aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2daf848cf4cd762df7ea3ab77be82186400c98306b775ab449d78b4ad0a44d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptAnalyticsEngineBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff7b79f452a4dac9e7059b6adbee078a1b1970a8ad1c6c8b7a71849b9988441(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    content: builtins.str,
    name: builtins.str,
    analytics_engine_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptAnalyticsEngineBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compatibility_date: typing.Optional[builtins.str] = None,
    compatibility_flags: typing.Optional[typing.Sequence[builtins.str]] = None,
    d1_database_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptD1DatabaseBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dispatch_namespace: typing.Optional[builtins.str] = None,
    hyperdrive_config_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptHyperdriveConfigBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    kv_namespace_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptKvNamespaceBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    logpush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    module: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    placement: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlacement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    plain_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptPlainTextBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    queue_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptQueueBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    r2_bucket_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptR2BucketBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_text_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptSecretTextBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptServiceBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    webassembly_binding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkersScriptWebassemblyBinding, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7232f89aadc69c774a7f8feac025bd52afa312d7ec92117f43e7f598221dbd1(
    *,
    database_id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1d659919ad42630e2826ffab5b26b11c365631ee10fc136606edefb2749b67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fa5d5e3c7a08d82e4a4ef6e2181db247cb1d936bb14de4094a5db7fe3b1551(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03fc65256afbe1b4076878df545a74284e5434bfc7d69d98d6056193a03de6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805404daa0ff5ec5141f65078847a27745e3630ca161d2fb7a1a6fd9b0b9161d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ba930095d2eb73d8a0bc4e89054ff5bf8ef2b8ed716c0e8024c8a28989bd06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824ca2283a740369f43bd8c37cf8805f38fa258aef01629ebff0bf3a916d1a93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptD1DatabaseBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a287c62f734bedf5306b1b49adeb4a011d0fbcd741d3f328303250f2ac4f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1444535ff43683f2bb9360401c5889b4873e5c9a93356605beea82d05e808921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1abb879ccdf91ac69bef673c0275c23f727eb760cc6f987985b27773285092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf942cb10224aad01bb1b44558b1e3a6e50bc0a1e054359b6868ae12a29997e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptD1DatabaseBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e145021a11811890cc9d33de0ec52fc16b8039fbf7d11faac6be0c4149f3124b(
    *,
    binding: builtins.str,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4403b3d630cc3979f8a53e894c79e08c9635cf5fecff03bbb6d2f3d9fa275c1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac579c9604ad802883490df9c74a13b68dc81cc84b849d792ffba37d7f5dc926(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22696c4da332a0addf9595dd425e96fbebd25c938a7b4af92142cb0212fa2ba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8939c7da65d3e7b48664cc0a039272889be330ac4b57c9d43244e87ba79377fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879ae2075d820707f4a75aadec152cc08dc1fd4269dcabb305fa5a631ee3a4b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edae2755fe6b72517d77fce67db8cfddab9201232759856211a767233fc7063(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptHyperdriveConfigBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae478a297bb0a3310b551f005ee2b4f268d9318aaa98a3a09df25f1bf174a941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602c07e839e9599bdedfe40f4c3c4a1c8614dfc6764b9375dfa08858bfe6708d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd30c38ccf81910adc53cd7cd287d30d2ce3af9cbaf644364dd5a861344db21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b404598a2eac040918a46b38cbb19c171d26112ecb92b1c5051a8271be0526(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptHyperdriveConfigBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd33229aeb920fb4d7b72e9a3dfc1256300aff0789474b16be0f4d55ba750b00(
    *,
    name: builtins.str,
    namespace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97203cbccf54457c3a00dd501fa92f2e84397ecabc1f89c5c2e021085d32f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a822d9f7aefb86272ad326445512af3dc917424de5b47b2956693fa1a07a7f29(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a40ee8ed4a0af6e89b964b2427c7b69345b50d513bb0695038022820555f1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea64b3e4344b92670f80200c0544459a3fca79159fff36d7a7c1dc1ca5574a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc25029c3fab05cbf864960d79a9108e65b958b34a60c2f1dad9ea97a0d8b54(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae6dca037c6f0f7b9364faa5808c1799a5832970f743f6101af5f3927ffb0ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptKvNamespaceBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8231f4ffd670176ffa1a108d4aed6ae382d2ed0895e4337164b4a3835554969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949c2fc55b1bbe0ff049dac439f7d161cdf236e6e19e389cafdb1801bd317e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c959b5bef9a8985e09fdd51dd454d024545cefdcca8770a4372010e3e2efdab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433c20234cff06c4ba1847942af45f938a43f8fca8d0b44ae43bf811b8ad2fa2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptKvNamespaceBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e4978ff81453269afcd828d0429a67b9641991131251e08ef91557a3cab1ea(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238dbbce4a1786bc8158a654c960e668fa3428222c8a4875c01cec74453a3e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7b258f37b97b1130dede02bb4357e6f071eee60e19d0c54f33a4e8e0b754fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d86de14147b0113e06e7869affbbbdbff2d3e1ab613275580459148f4029c77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b495204c824fb0f8e1343d57cb764c1fbcc91fb2dc8c1c60a71a0823c352c1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e732fc6124f25d8e05379f0cb95e92a62b235c527e413981d6e40317d78b041(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f0d1515eb820bbb564034b6111dfa841ce8e753f809d0c9be4011bf7ab5cfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlacement]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a158c6e91af48c4f305bec5f3dd074b7898a16087f8fb8d6760231f63f750f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efbc9bf511fddd2db4b69eab68daae2a4eb96a27da4c0d7144c960dd2835f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ccdfa338a27dc2280667eadc3dfa61b4800c5eb4db50906cc4755c705744a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlacement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bc19489586dc614f32d680138d7e8ee42ed192463d72f077a96422147b64b3(
    *,
    name: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c80bff52613efb43c498249c2b4a31671c8a6d4292a4e666517ffbc44f859d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df204ec9e5a71ed50a3eb8352259b65bc0fb4741f6b154b24c1667dd5e27a36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ceb884aa61ab0b9beb342e6fd5a75eac3174584db1b2f24d134ecf0238bdb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160d83b3f8fe5e38ed837c8040861b243617774aa6e3f34f4cb06325dfcf3eb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5c006298d6a46fc831e3558d28c6dfa5ca9340d50965a5d5be00a54bfe7777(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6dea5e16ff756619d73a04e7bd96bf354ed76e139d557e6e0017db4aefa9cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptPlainTextBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb74365645e95c3b142d5324549bf71fa1ffa2eb92c7ddfa63cd48587b4ab359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c92a4257f2a1fe67a2430bc1a6c456ae04b8f660f92a8c72e640d24c9c637d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e803c6691bf9821b22b7731add4adcdb4427a9e878ae82f1e84d758faeb5d82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7666f5663121fd5d31cbe1117d9ab863cd6383186357157eaa2b8ee981b642(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptPlainTextBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe52fd50f2051f75a72f376f6399ed972846221ac672b524aa41f53bea537df(
    *,
    binding: builtins.str,
    queue: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf96a98c8ebf8a5de9957a9e70e7ad46ce4653843d4f6e7e425bd3e72f8a8e7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24215ec11bb5ba69bd9d36cf0b11358ee2e9d2514d1d35370b34bf6a53ed691f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f515d6ac71eea1adaec36ee7eb44fd8bf8ab4c5344a3e6703926245708b347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7f090d4a0dbea055f7c00c7948e1a543343f7cd48a69c6e5d1d37a0e404b05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1971b9741026b296e8bad9229c0cbf99355cd5b90283c285951f55105ea02eb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf24edc7803b6df8181bdf279b903fa51e69425f98a7f742ffe4362174bcdc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptQueueBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a81abf938871d7942b30da4125a8a9b75e9a461be5ee33212e7243a163b876c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b99cb9a5aa63ef2b7ca9e691cf986c65454e9aae0a06ed66fa3399f896349b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce063396e430f7ab9872497e544de254fa7ceab5f6362ecee5e29165dfc2679e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bf6e566c9c49921236d789e56182d2c308abcc0eafcdb574ed1eca21d54797(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptQueueBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb37f700731e28bf724ac24fbfb7e0185c2b37e13469a67d2d71654bf5a76997(
    *,
    bucket_name: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d68393d142f60b1e1a3e1a8637fd66d89dce73204056c061977b0e2fd41b51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ad51572a61806a5d7f6b48a306991f37b4ceddabe8050c375fc4f83631c00d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362234e1d083b7c0a41ba4087a32faa29fd0c68c44236b3130a6098349837910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e90feb98153b9ccc526423d0314590606f384aeb67d54a1bfc18eaa27e2190(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c9340e984c15b21bab30a8d3ccfe28c04c9e2d5795715a2105ccf5eb3eb4a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef6eee10120d7f7280b1d4ca677fa103827d8392a1ab23e59890c4667618c5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptR2BucketBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c60a0d593acc3dd3f202b1b1d16976e6642db374fd361fc8b3bb70245be845f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45adaf1f063dcdf97a570f06191f07befad431c0233761060c2ffeb6739c9cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9296aece9fc207b813100762e69deeb15b56cfa9674e08be9969e7e040bed339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd8345c65d3c99f12d56b57dc73cc22d2cbb7aaeeab009b536d4b05542e3ba7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptR2BucketBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca23dab904a7a222a276827b9799975a405c6a2509a272a9256d7b036de36d3(
    *,
    name: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d302ab7d5f18bd1837dffbd00d8ec9f1dba4dfc950e6e48649916d4fe048f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28145a6315e9845db79e80e229f01b3660735dd09a3820f7248f7832e16b0a53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ed5b8e0a3fe0f10db1902c5b009d5b05761e037147798a1b724d7d4c1acb9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f92893afa7a270ea20c8449a6cc6e4c963856415d546a0a90abd275eaf6f49d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b32338acd0a705d7982957a5ed2a8307c86bd181d57ba289b1f1fcb51169fca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8545fdf71644cd202e64487d8a7b8d1f5eaf45183930d263046ba350d5840d99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptSecretTextBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d84ecef45c499d349c22a8f5853757959ba1f1fd431067384719b95826ee11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bc6c9b5683279d4c4e1f198eac1b9b385c22de597f2f4804ccbce92dbb073c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9926d1d4f6cd1b0ecf43363a3c1b2d978cfd9a6b8d1089411f48fe80ac2724c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75c654f66314d56e2283857a9923211013e624651d9e01c0d0b73338a02672a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptSecretTextBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b7d21923d9754548ce0690a7013146e005f95370d0866ae8570c74d8407426(
    *,
    name: builtins.str,
    service: builtins.str,
    environment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189c032e71c2b1d0cbbd9b996a8f5025db061f337f72672f416a8010fb2c72fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b3cb375fd6bed18367507e6ac2c256bcbee988fa4f65c4ea430b1ec8d8ce7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298a45f2f773bddf4fc0a4b1d5a89953737bd68695e3e76ded4b5d8b914fd6ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f280a19be520f4271adf27d0f45e8a41e5669ecda78abbb9c5d0a2d97eb5c5d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb2cb15e9b608c79aecdbb7591c4ffd8e0aa951cd16e3b046d8da81f6f5b6a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5265069da2eb4f39095f770177ba455e3cf7756aac1cc6235207321784dce2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptServiceBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d8faddbf8793a51e2fd994f133d011347045c1b20d166861b534296f088b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c748d2076d6f62249443cc260c8b57a92f2963a9b9efa0d1ae7b82cafcb171e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de54a9fe15803594f28eea393a12b44c521579550550cb5daf961c9908a00eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5e4600c5e749b44b73e194a1b16b82060b956292974893b4efe53d4dc02717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6070aecf63e09546c096a10895c31a378efb61c18c4628a612401db746f278b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptServiceBinding]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29250cd05f661568a7f48ad9c98e607917f8be197855c16c8b27cd6f6352944c(
    *,
    module: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9ca31d2b2136863ccce33f0324400e41c43f6870bdf12c34522116cc167e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d16963e17ca5bb81b2169bb70a3b3af310955132aa558db7994c1c3797b4d51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b652846a7ebe8b0f973bf86bb6c76885e6cc4a36d688325f0c0fb45901fd51d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e5cad36d721699417536b08373c413e3a3b7052812461f97cc35e9172609e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86067c75de167084ba8f052e130db59e135fa33087d852dafcf7285f863cbbe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9933c52a38d2b54ceb5f7815e078547aa547df774bf5b7399f17c6c017814c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkersScriptWebassemblyBinding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72750d0f8cfd6bf37b5058721a6ceee693b68a64bb4b12b6e99544dc8e0c25fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d528ba94f47236324d5daded3bb6286256638508634db2c0f77e4f9f858d7dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e1e0c63bb402f9c52deb742cdcc4d23e079d6ca770aa23b3d5c0acf53e2bf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5485bc3ff4d48b5b74b34484c8eb631e2337b4e602c745ef6569124794f6bf4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkersScriptWebassemblyBinding]],
) -> None:
    """Type checking stubs"""
    pass
