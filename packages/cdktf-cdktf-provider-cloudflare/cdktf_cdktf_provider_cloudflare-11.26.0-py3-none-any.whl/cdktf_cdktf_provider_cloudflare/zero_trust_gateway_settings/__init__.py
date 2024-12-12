r'''
# `cloudflare_zero_trust_gateway_settings`

Refer to the Terraform Registry for docs: [`cloudflare_zero_trust_gateway_settings`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings).
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


class ZeroTrustGatewaySettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings cloudflare_zero_trust_gateway_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        antivirus: typing.Optional[typing.Union["ZeroTrustGatewaySettingsAntivirus", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page: typing.Optional[typing.Union["ZeroTrustGatewaySettingsBlockPage", typing.Dict[builtins.str, typing.Any]]] = None,
        body_scanning: typing.Optional[typing.Union["ZeroTrustGatewaySettingsBodyScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union["ZeroTrustGatewaySettingsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_certificate: typing.Optional[typing.Union["ZeroTrustGatewaySettingsCustomCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_email_matching: typing.Optional[typing.Union["ZeroTrustGatewaySettingsExtendedEmailMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        fips: typing.Optional[typing.Union["ZeroTrustGatewaySettingsFips", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["ZeroTrustGatewaySettingsLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        payload_log: typing.Optional[typing.Union["ZeroTrustGatewaySettingsPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy: typing.Optional[typing.Union["ZeroTrustGatewaySettingsProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_session_log: typing.Optional[typing.Union["ZeroTrustGatewaySettingsSshSessionLog", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_decrypt_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        url_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings cloudflare_zero_trust_gateway_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#account_id ZeroTrustGatewaySettings#account_id}
        :param activity_log_enabled: Whether to enable the activity log. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#activity_log_enabled ZeroTrustGatewaySettings#activity_log_enabled}
        :param antivirus: antivirus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#antivirus ZeroTrustGatewaySettings#antivirus}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#block_page ZeroTrustGatewaySettings#block_page}
        :param body_scanning: body_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#body_scanning ZeroTrustGatewaySettings#body_scanning}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#certificate ZeroTrustGatewaySettings#certificate}
        :param custom_certificate: custom_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#custom_certificate ZeroTrustGatewaySettings#custom_certificate}
        :param extended_email_matching: extended_email_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#extended_email_matching ZeroTrustGatewaySettings#extended_email_matching}
        :param fips: fips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fips ZeroTrustGatewaySettings#fips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logging ZeroTrustGatewaySettings#logging}
        :param non_identity_browser_isolation_enabled: Enable non-identity onramp for Browser Isolation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#non_identity_browser_isolation_enabled ZeroTrustGatewaySettings#non_identity_browser_isolation_enabled}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#payload_log ZeroTrustGatewaySettings#payload_log}
        :param protocol_detection_enabled: Indicator that protocol detection is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#protocol_detection_enabled ZeroTrustGatewaySettings#protocol_detection_enabled}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#proxy ZeroTrustGatewaySettings#proxy}
        :param ssh_session_log: ssh_session_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#ssh_session_log ZeroTrustGatewaySettings#ssh_session_log}
        :param tls_decrypt_enabled: Indicator that decryption of TLS traffic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls_decrypt_enabled ZeroTrustGatewaySettings#tls_decrypt_enabled}
        :param url_browser_isolation_enabled: Safely browse websites in Browser Isolation through a URL. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#url_browser_isolation_enabled ZeroTrustGatewaySettings#url_browser_isolation_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e835aa6c5393b3bccb9f3757aa1cc8e34cee2d7a93e870dce8110f777030091f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZeroTrustGatewaySettingsConfig(
            account_id=account_id,
            activity_log_enabled=activity_log_enabled,
            antivirus=antivirus,
            block_page=block_page,
            body_scanning=body_scanning,
            certificate=certificate,
            custom_certificate=custom_certificate,
            extended_email_matching=extended_email_matching,
            fips=fips,
            id=id,
            logging=logging,
            non_identity_browser_isolation_enabled=non_identity_browser_isolation_enabled,
            payload_log=payload_log,
            protocol_detection_enabled=protocol_detection_enabled,
            proxy=proxy,
            ssh_session_log=ssh_session_log,
            tls_decrypt_enabled=tls_decrypt_enabled,
            url_browser_isolation_enabled=url_browser_isolation_enabled,
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
        '''Generates CDKTF code for importing a ZeroTrustGatewaySettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ZeroTrustGatewaySettings to import.
        :param import_from_id: The id of the existing ZeroTrustGatewaySettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ZeroTrustGatewaySettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a9c540ee48d79bc94bf225d2e7f3d25e0fad690ba5931d93c9793a03c42dc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAntivirus")
    def put_antivirus(
        self,
        *,
        enabled_download_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled_upload_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        fail_closed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_settings: typing.Optional[typing.Union["ZeroTrustGatewaySettingsAntivirusNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled_download_phase: Scan on file download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_download_phase ZeroTrustGatewaySettings#enabled_download_phase}
        :param enabled_upload_phase: Scan on file upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_upload_phase ZeroTrustGatewaySettings#enabled_upload_phase}
        :param fail_closed: Block requests for files that cannot be scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fail_closed ZeroTrustGatewaySettings#fail_closed}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#notification_settings ZeroTrustGatewaySettings#notification_settings}
        '''
        value = ZeroTrustGatewaySettingsAntivirus(
            enabled_download_phase=enabled_download_phase,
            enabled_upload_phase=enabled_upload_phase,
            fail_closed=fail_closed,
            notification_settings=notification_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAntivirus", [value]))

    @jsii.member(jsii_name="putBlockPage")
    def put_block_page(
        self,
        *,
        background_color: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_text: typing.Optional[builtins.str] = None,
        header_text: typing.Optional[builtins.str] = None,
        logo_path: typing.Optional[builtins.str] = None,
        mailto_address: typing.Optional[builtins.str] = None,
        mailto_subject: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param background_color: Hex code of block page background color. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#background_color ZeroTrustGatewaySettings#background_color}
        :param enabled: Indicator of enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param footer_text: Block page footer text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#footer_text ZeroTrustGatewaySettings#footer_text}
        :param header_text: Block page header text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#header_text ZeroTrustGatewaySettings#header_text}
        :param logo_path: URL of block page logo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logo_path ZeroTrustGatewaySettings#logo_path}
        :param mailto_address: Admin email for users to contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_address ZeroTrustGatewaySettings#mailto_address}
        :param mailto_subject: Subject line for emails created from block page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_subject ZeroTrustGatewaySettings#mailto_subject}
        :param name: Name of block page configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#name ZeroTrustGatewaySettings#name}
        '''
        value = ZeroTrustGatewaySettingsBlockPage(
            background_color=background_color,
            enabled=enabled,
            footer_text=footer_text,
            header_text=header_text,
            logo_path=logo_path,
            mailto_address=mailto_address,
            mailto_subject=mailto_subject,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putBlockPage", [value]))

    @jsii.member(jsii_name="putBodyScanning")
    def put_body_scanning(self, *, inspection_mode: builtins.str) -> None:
        '''
        :param inspection_mode: Body scanning inspection mode. Available values: ``deep``, ``shallow``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#inspection_mode ZeroTrustGatewaySettings#inspection_mode}
        '''
        value = ZeroTrustGatewaySettingsBodyScanning(inspection_mode=inspection_mode)

        return typing.cast(None, jsii.invoke(self, "putBodyScanning", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of certificate for TLS interception. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = ZeroTrustGatewaySettingsCertificate(id=id)

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putCustomCertificate")
    def put_custom_certificate(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether TLS encryption should use a custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param id: ID of custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = ZeroTrustGatewaySettingsCustomCertificate(enabled=enabled, id=id)

        return typing.cast(None, jsii.invoke(self, "putCustomCertificate", [value]))

    @jsii.member(jsii_name="putExtendedEmailMatching")
    def put_extended_email_matching(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        value = ZeroTrustGatewaySettingsExtendedEmailMatching(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putExtendedEmailMatching", [value]))

    @jsii.member(jsii_name="putFips")
    def put_fips(
        self,
        *,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param tls: Only allow FIPS-compliant TLS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls ZeroTrustGatewaySettings#tls}
        '''
        value = ZeroTrustGatewaySettingsFips(tls=tls)

        return typing.cast(None, jsii.invoke(self, "putFips", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        settings_by_rule_type: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleType", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param redact_pii: Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#redact_pii ZeroTrustGatewaySettings#redact_pii}
        :param settings_by_rule_type: settings_by_rule_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#settings_by_rule_type ZeroTrustGatewaySettings#settings_by_rule_type}
        '''
        value = ZeroTrustGatewaySettingsLogging(
            redact_pii=redact_pii, settings_by_rule_type=settings_by_rule_type
        )

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putPayloadLog")
    def put_payload_log(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt matched payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        value = ZeroTrustGatewaySettingsPayloadLog(public_key=public_key)

        return typing.cast(None, jsii.invoke(self, "putPayloadLog", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        *,
        disable_for_time: jsii.Number,
        root_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        tcp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        udp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        virtual_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_for_time: Sets the time limit in seconds that a user can use an override code to bypass WARP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#disable_for_time ZeroTrustGatewaySettings#disable_for_time}
        :param root_ca: Whether root ca is enabled account wide for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#root_ca ZeroTrustGatewaySettings#root_ca}
        :param tcp: Whether gateway proxy is enabled on gateway devices for TCP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tcp ZeroTrustGatewaySettings#tcp}
        :param udp: Whether gateway proxy is enabled on gateway devices for UDP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#udp ZeroTrustGatewaySettings#udp}
        :param virtual_ip: Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#virtual_ip ZeroTrustGatewaySettings#virtual_ip}
        '''
        value = ZeroTrustGatewaySettingsProxy(
            disable_for_time=disable_for_time,
            root_ca=root_ca,
            tcp=tcp,
            udp=udp,
            virtual_ip=virtual_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putSshSessionLog")
    def put_ssh_session_log(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt ssh session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        value = ZeroTrustGatewaySettingsSshSessionLog(public_key=public_key)

        return typing.cast(None, jsii.invoke(self, "putSshSessionLog", [value]))

    @jsii.member(jsii_name="resetActivityLogEnabled")
    def reset_activity_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivityLogEnabled", []))

    @jsii.member(jsii_name="resetAntivirus")
    def reset_antivirus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntivirus", []))

    @jsii.member(jsii_name="resetBlockPage")
    def reset_block_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockPage", []))

    @jsii.member(jsii_name="resetBodyScanning")
    def reset_body_scanning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyScanning", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetCustomCertificate")
    def reset_custom_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCertificate", []))

    @jsii.member(jsii_name="resetExtendedEmailMatching")
    def reset_extended_email_matching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedEmailMatching", []))

    @jsii.member(jsii_name="resetFips")
    def reset_fips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFips", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetNonIdentityBrowserIsolationEnabled")
    def reset_non_identity_browser_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonIdentityBrowserIsolationEnabled", []))

    @jsii.member(jsii_name="resetPayloadLog")
    def reset_payload_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadLog", []))

    @jsii.member(jsii_name="resetProtocolDetectionEnabled")
    def reset_protocol_detection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolDetectionEnabled", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetSshSessionLog")
    def reset_ssh_session_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshSessionLog", []))

    @jsii.member(jsii_name="resetTlsDecryptEnabled")
    def reset_tls_decrypt_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsDecryptEnabled", []))

    @jsii.member(jsii_name="resetUrlBrowserIsolationEnabled")
    def reset_url_browser_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlBrowserIsolationEnabled", []))

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
    @jsii.member(jsii_name="antivirus")
    def antivirus(self) -> "ZeroTrustGatewaySettingsAntivirusOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsAntivirusOutputReference", jsii.get(self, "antivirus"))

    @builtins.property
    @jsii.member(jsii_name="blockPage")
    def block_page(self) -> "ZeroTrustGatewaySettingsBlockPageOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsBlockPageOutputReference", jsii.get(self, "blockPage"))

    @builtins.property
    @jsii.member(jsii_name="bodyScanning")
    def body_scanning(self) -> "ZeroTrustGatewaySettingsBodyScanningOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsBodyScanningOutputReference", jsii.get(self, "bodyScanning"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "ZeroTrustGatewaySettingsCertificateOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsCertificateOutputReference", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="customCertificate")
    def custom_certificate(
        self,
    ) -> "ZeroTrustGatewaySettingsCustomCertificateOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsCustomCertificateOutputReference", jsii.get(self, "customCertificate"))

    @builtins.property
    @jsii.member(jsii_name="extendedEmailMatching")
    def extended_email_matching(
        self,
    ) -> "ZeroTrustGatewaySettingsExtendedEmailMatchingOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsExtendedEmailMatchingOutputReference", jsii.get(self, "extendedEmailMatching"))

    @builtins.property
    @jsii.member(jsii_name="fips")
    def fips(self) -> "ZeroTrustGatewaySettingsFipsOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsFipsOutputReference", jsii.get(self, "fips"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "ZeroTrustGatewaySettingsLoggingOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsLoggingOutputReference", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="payloadLog")
    def payload_log(self) -> "ZeroTrustGatewaySettingsPayloadLogOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsPayloadLogOutputReference", jsii.get(self, "payloadLog"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "ZeroTrustGatewaySettingsProxyOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="sshSessionLog")
    def ssh_session_log(self) -> "ZeroTrustGatewaySettingsSshSessionLogOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsSshSessionLogOutputReference", jsii.get(self, "sshSessionLog"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="activityLogEnabledInput")
    def activity_log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activityLogEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="antivirusInput")
    def antivirus_input(self) -> typing.Optional["ZeroTrustGatewaySettingsAntivirus"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsAntivirus"], jsii.get(self, "antivirusInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageInput")
    def block_page_input(self) -> typing.Optional["ZeroTrustGatewaySettingsBlockPage"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsBlockPage"], jsii.get(self, "blockPageInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyScanningInput")
    def body_scanning_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsBodyScanning"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsBodyScanning"], jsii.get(self, "bodyScanningInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsCertificate"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsCertificate"], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="customCertificateInput")
    def custom_certificate_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsCustomCertificate"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsCustomCertificate"], jsii.get(self, "customCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedEmailMatchingInput")
    def extended_email_matching_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsExtendedEmailMatching"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsExtendedEmailMatching"], jsii.get(self, "extendedEmailMatchingInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsInput")
    def fips_input(self) -> typing.Optional["ZeroTrustGatewaySettingsFips"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsFips"], jsii.get(self, "fipsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional["ZeroTrustGatewaySettingsLogging"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsLogging"], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nonIdentityBrowserIsolationEnabledInput")
    def non_identity_browser_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonIdentityBrowserIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadLogInput")
    def payload_log_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsPayloadLog"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsPayloadLog"], jsii.get(self, "payloadLogInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolDetectionEnabledInput")
    def protocol_detection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protocolDetectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["ZeroTrustGatewaySettingsProxy"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="sshSessionLogInput")
    def ssh_session_log_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsSshSessionLog"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsSshSessionLog"], jsii.get(self, "sshSessionLogInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsDecryptEnabledInput")
    def tls_decrypt_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsDecryptEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="urlBrowserIsolationEnabledInput")
    def url_browser_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "urlBrowserIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f323899588c0d92313196544d971a5ad585faf1ae29ee162ace9408ebbf9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="activityLogEnabled")
    def activity_log_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "activityLogEnabled"))

    @activity_log_enabled.setter
    def activity_log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e67adb7be19cbc0bfa87386d661d832826c3177cf4946417963b444a955c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activityLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8065f220e57c4bb9150da43e628cbef3e8051a55479a0d41e7383e0bbf75aeb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonIdentityBrowserIsolationEnabled")
    def non_identity_browser_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonIdentityBrowserIsolationEnabled"))

    @non_identity_browser_isolation_enabled.setter
    def non_identity_browser_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96f4552601a28dfbf82fc8d3554ad3cbfcd77cdd85a76fa4f5d99baea82a9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonIdentityBrowserIsolationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolDetectionEnabled")
    def protocol_detection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protocolDetectionEnabled"))

    @protocol_detection_enabled.setter
    def protocol_detection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3c3904870a6479963aa3a8a1c0ad7d9703eeaced18b4f0bb5747edff2a17e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolDetectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsDecryptEnabled")
    def tls_decrypt_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsDecryptEnabled"))

    @tls_decrypt_enabled.setter
    def tls_decrypt_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034d122104b57d109ba82488c77b17f9f0ef9ff1895f10237a7c181f90c39e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsDecryptEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlBrowserIsolationEnabled")
    def url_browser_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "urlBrowserIsolationEnabled"))

    @url_browser_isolation_enabled.setter
    def url_browser_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d90746c0ffcc71b60c262f043beb33b5eae8398e7d314ef7dcb3ce0c038558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlBrowserIsolationEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsAntivirus",
    jsii_struct_bases=[],
    name_mapping={
        "enabled_download_phase": "enabledDownloadPhase",
        "enabled_upload_phase": "enabledUploadPhase",
        "fail_closed": "failClosed",
        "notification_settings": "notificationSettings",
    },
)
class ZeroTrustGatewaySettingsAntivirus:
    def __init__(
        self,
        *,
        enabled_download_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled_upload_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        fail_closed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_settings: typing.Optional[typing.Union["ZeroTrustGatewaySettingsAntivirusNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled_download_phase: Scan on file download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_download_phase ZeroTrustGatewaySettings#enabled_download_phase}
        :param enabled_upload_phase: Scan on file upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_upload_phase ZeroTrustGatewaySettings#enabled_upload_phase}
        :param fail_closed: Block requests for files that cannot be scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fail_closed ZeroTrustGatewaySettings#fail_closed}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#notification_settings ZeroTrustGatewaySettings#notification_settings}
        '''
        if isinstance(notification_settings, dict):
            notification_settings = ZeroTrustGatewaySettingsAntivirusNotificationSettings(**notification_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd09d9bb03971346980a53dc8beab627f106cbf77486b51dccc35893ca43614)
            check_type(argname="argument enabled_download_phase", value=enabled_download_phase, expected_type=type_hints["enabled_download_phase"])
            check_type(argname="argument enabled_upload_phase", value=enabled_upload_phase, expected_type=type_hints["enabled_upload_phase"])
            check_type(argname="argument fail_closed", value=fail_closed, expected_type=type_hints["fail_closed"])
            check_type(argname="argument notification_settings", value=notification_settings, expected_type=type_hints["notification_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled_download_phase": enabled_download_phase,
            "enabled_upload_phase": enabled_upload_phase,
            "fail_closed": fail_closed,
        }
        if notification_settings is not None:
            self._values["notification_settings"] = notification_settings

    @builtins.property
    def enabled_download_phase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Scan on file download.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_download_phase ZeroTrustGatewaySettings#enabled_download_phase}
        '''
        result = self._values.get("enabled_download_phase")
        assert result is not None, "Required property 'enabled_download_phase' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def enabled_upload_phase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Scan on file upload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled_upload_phase ZeroTrustGatewaySettings#enabled_upload_phase}
        '''
        result = self._values.get("enabled_upload_phase")
        assert result is not None, "Required property 'enabled_upload_phase' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def fail_closed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Block requests for files that cannot be scanned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fail_closed ZeroTrustGatewaySettings#fail_closed}
        '''
        result = self._values.get("fail_closed")
        assert result is not None, "Required property 'fail_closed' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_settings(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsAntivirusNotificationSettings"]:
        '''notification_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#notification_settings ZeroTrustGatewaySettings#notification_settings}
        '''
        result = self._values.get("notification_settings")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsAntivirusNotificationSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsAntivirus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsAntivirusNotificationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "message": "message",
        "support_url": "supportUrl",
    },
)
class ZeroTrustGatewaySettingsAntivirusNotificationSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#message ZeroTrustGatewaySettings#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#support_url ZeroTrustGatewaySettings#support_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e384ba76a5ab4cac986b4cb9f3bebaefc20aa9bda85ad259ec05cce0095aba2f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Notification content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#message ZeroTrustGatewaySettings#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''Support URL to show in the notification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#support_url ZeroTrustGatewaySettings#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsAntivirusNotificationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsAntivirusNotificationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsAntivirusNotificationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f9cbbfef51b9b6eb0181a6fcff53adaaeb5bde7b8b41815d995a6d5b5d40f46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb49d002dd9dd29090e6fcd58b1f6bc26613d31a70b3e49e3a0acca5ae0e89ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60677138f2066b30df4b6e4fd243c387ac99f119b65f67492872b6266748f471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027440da9503127ee305d9ec89022a8e5d10831bf217d3017a4f36659b36bdf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0646275e897df75e03f5aaab591d07197ed83d764efa01aa0d02d1266340c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewaySettingsAntivirusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsAntivirusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b459be0ddf088ab3125eddad8594bb7fe2e4a2304a3a843a941d34d5831d25b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotificationSettings")
    def put_notification_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#message ZeroTrustGatewaySettings#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#support_url ZeroTrustGatewaySettings#support_url}
        '''
        value = ZeroTrustGatewaySettingsAntivirusNotificationSettings(
            enabled=enabled, message=message, support_url=support_url
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationSettings", [value]))

    @jsii.member(jsii_name="resetNotificationSettings")
    def reset_notification_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationSettings", []))

    @builtins.property
    @jsii.member(jsii_name="notificationSettings")
    def notification_settings(
        self,
    ) -> ZeroTrustGatewaySettingsAntivirusNotificationSettingsOutputReference:
        return typing.cast(ZeroTrustGatewaySettingsAntivirusNotificationSettingsOutputReference, jsii.get(self, "notificationSettings"))

    @builtins.property
    @jsii.member(jsii_name="enabledDownloadPhaseInput")
    def enabled_download_phase_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledDownloadPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledUploadPhaseInput")
    def enabled_upload_phase_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledUploadPhaseInput"))

    @builtins.property
    @jsii.member(jsii_name="failClosedInput")
    def fail_closed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failClosedInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationSettingsInput")
    def notification_settings_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings], jsii.get(self, "notificationSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledDownloadPhase")
    def enabled_download_phase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabledDownloadPhase"))

    @enabled_download_phase.setter
    def enabled_download_phase(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b6246c8f12cf4e4fab792a86ed696b5b5c799c3bbd37eade5636b07ab06202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledDownloadPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabledUploadPhase")
    def enabled_upload_phase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabledUploadPhase"))

    @enabled_upload_phase.setter
    def enabled_upload_phase(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4b4f1f6f66c037e491ac994a1cf9b92d6b069a871a1d4192d7cf3bb3bff7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledUploadPhase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failClosed")
    def fail_closed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failClosed"))

    @fail_closed.setter
    def fail_closed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3846bf104db1fc95e186b0c36aaabe5cd76c41ade765f0e6d7a0fff484bfcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failClosed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsAntivirus]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsAntivirus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsAntivirus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3d80a64fcd759ab802b22dbe3ac6817d11d567d2c2c8afd10b68fe85e0e9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsBlockPage",
    jsii_struct_bases=[],
    name_mapping={
        "background_color": "backgroundColor",
        "enabled": "enabled",
        "footer_text": "footerText",
        "header_text": "headerText",
        "logo_path": "logoPath",
        "mailto_address": "mailtoAddress",
        "mailto_subject": "mailtoSubject",
        "name": "name",
    },
)
class ZeroTrustGatewaySettingsBlockPage:
    def __init__(
        self,
        *,
        background_color: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_text: typing.Optional[builtins.str] = None,
        header_text: typing.Optional[builtins.str] = None,
        logo_path: typing.Optional[builtins.str] = None,
        mailto_address: typing.Optional[builtins.str] = None,
        mailto_subject: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param background_color: Hex code of block page background color. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#background_color ZeroTrustGatewaySettings#background_color}
        :param enabled: Indicator of enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param footer_text: Block page footer text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#footer_text ZeroTrustGatewaySettings#footer_text}
        :param header_text: Block page header text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#header_text ZeroTrustGatewaySettings#header_text}
        :param logo_path: URL of block page logo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logo_path ZeroTrustGatewaySettings#logo_path}
        :param mailto_address: Admin email for users to contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_address ZeroTrustGatewaySettings#mailto_address}
        :param mailto_subject: Subject line for emails created from block page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_subject ZeroTrustGatewaySettings#mailto_subject}
        :param name: Name of block page configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#name ZeroTrustGatewaySettings#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a3d39555b8fed1b96c70cda76ff3bac778cfbbe1eacb30bb48e2d9c75021fa)
            check_type(argname="argument background_color", value=background_color, expected_type=type_hints["background_color"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument footer_text", value=footer_text, expected_type=type_hints["footer_text"])
            check_type(argname="argument header_text", value=header_text, expected_type=type_hints["header_text"])
            check_type(argname="argument logo_path", value=logo_path, expected_type=type_hints["logo_path"])
            check_type(argname="argument mailto_address", value=mailto_address, expected_type=type_hints["mailto_address"])
            check_type(argname="argument mailto_subject", value=mailto_subject, expected_type=type_hints["mailto_subject"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if background_color is not None:
            self._values["background_color"] = background_color
        if enabled is not None:
            self._values["enabled"] = enabled
        if footer_text is not None:
            self._values["footer_text"] = footer_text
        if header_text is not None:
            self._values["header_text"] = header_text
        if logo_path is not None:
            self._values["logo_path"] = logo_path
        if mailto_address is not None:
            self._values["mailto_address"] = mailto_address
        if mailto_subject is not None:
            self._values["mailto_subject"] = mailto_subject
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def background_color(self) -> typing.Optional[builtins.str]:
        '''Hex code of block page background color.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#background_color ZeroTrustGatewaySettings#background_color}
        '''
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator of enablement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def footer_text(self) -> typing.Optional[builtins.str]:
        '''Block page footer text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#footer_text ZeroTrustGatewaySettings#footer_text}
        '''
        result = self._values.get("footer_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_text(self) -> typing.Optional[builtins.str]:
        '''Block page header text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#header_text ZeroTrustGatewaySettings#header_text}
        '''
        result = self._values.get("header_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_path(self) -> typing.Optional[builtins.str]:
        '''URL of block page logo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logo_path ZeroTrustGatewaySettings#logo_path}
        '''
        result = self._values.get("logo_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailto_address(self) -> typing.Optional[builtins.str]:
        '''Admin email for users to contact.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_address ZeroTrustGatewaySettings#mailto_address}
        '''
        result = self._values.get("mailto_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailto_subject(self) -> typing.Optional[builtins.str]:
        '''Subject line for emails created from block page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#mailto_subject ZeroTrustGatewaySettings#mailto_subject}
        '''
        result = self._values.get("mailto_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of block page configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#name ZeroTrustGatewaySettings#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsBlockPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsBlockPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsBlockPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de512ad616d76473a8991922be1d543838a352b7d4de2ea83046759776c5a3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackgroundColor")
    def reset_background_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackgroundColor", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFooterText")
    def reset_footer_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFooterText", []))

    @jsii.member(jsii_name="resetHeaderText")
    def reset_header_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderText", []))

    @jsii.member(jsii_name="resetLogoPath")
    def reset_logo_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoPath", []))

    @jsii.member(jsii_name="resetMailtoAddress")
    def reset_mailto_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailtoAddress", []))

    @jsii.member(jsii_name="resetMailtoSubject")
    def reset_mailto_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailtoSubject", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="backgroundColorInput")
    def background_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backgroundColorInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="footerTextInput")
    def footer_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "footerTextInput"))

    @builtins.property
    @jsii.member(jsii_name="headerTextInput")
    def header_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerTextInput"))

    @builtins.property
    @jsii.member(jsii_name="logoPathInput")
    def logo_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoPathInput"))

    @builtins.property
    @jsii.member(jsii_name="mailtoAddressInput")
    def mailto_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailtoAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="mailtoSubjectInput")
    def mailto_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailtoSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="backgroundColor")
    def background_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backgroundColor"))

    @background_color.setter
    def background_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68001b8afac2bc05878d8e9bfc725da7d4f65d27ea7af5d598cdfa24f0af55c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backgroundColor", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__33fca6b35da440b5ac345def7ed662af2ecc19fae64ef148da3d533ebf6bcb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="footerText")
    def footer_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "footerText"))

    @footer_text.setter
    def footer_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a76dc8d24a81afd3136b88136492e34a41132e6929bdda7d853bf09b90aaa87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "footerText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerText")
    def header_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerText"))

    @header_text.setter
    def header_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e1b413a98ab470a9849e1b38e5070509d379614b46535ef434a97afca9bd93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoPath")
    def logo_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoPath"))

    @logo_path.setter
    def logo_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976c937cbb5b8b0fdc3b77da8944e686948c53a8c7fd90aabde66e267730c3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailtoAddress")
    def mailto_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailtoAddress"))

    @mailto_address.setter
    def mailto_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211d4df20d4f3abe2c4d0497fb46597366801123fb4111c41f8335d31b6d8d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailtoAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailtoSubject")
    def mailto_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailtoSubject"))

    @mailto_subject.setter
    def mailto_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af015bf5de56f891dab42cd5195bcdb478d316eec6ea1b4f1374e780d368c604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailtoSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d32537fb31e9edb19563d8a7ce863eb9948472a700e417ee3932c17b1122b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsBlockPage]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsBlockPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsBlockPage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791d6613114a735f673702d4f0e6beb4ad448b066f9610348b8b2c2f29e0f341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsBodyScanning",
    jsii_struct_bases=[],
    name_mapping={"inspection_mode": "inspectionMode"},
)
class ZeroTrustGatewaySettingsBodyScanning:
    def __init__(self, *, inspection_mode: builtins.str) -> None:
        '''
        :param inspection_mode: Body scanning inspection mode. Available values: ``deep``, ``shallow``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#inspection_mode ZeroTrustGatewaySettings#inspection_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cbbd170d8f6f823b820893b3ed5a378a7bc1843ad9c8cf0fb70afe70ae4020)
            check_type(argname="argument inspection_mode", value=inspection_mode, expected_type=type_hints["inspection_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inspection_mode": inspection_mode,
        }

    @builtins.property
    def inspection_mode(self) -> builtins.str:
        '''Body scanning inspection mode. Available values: ``deep``, ``shallow``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#inspection_mode ZeroTrustGatewaySettings#inspection_mode}
        '''
        result = self._values.get("inspection_mode")
        assert result is not None, "Required property 'inspection_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsBodyScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsBodyScanningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsBodyScanningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c0ab277084fa98b64514c01af9602325cd0de67fa0899bf5fba93bfee35db1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="inspectionModeInput")
    def inspection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectionMode")
    def inspection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectionMode"))

    @inspection_mode.setter
    def inspection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2773fc034e0a156ea01bdca9c8fab8d7a3bf7ca154d0193269881916d7fcff04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsBodyScanning]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsBodyScanning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsBodyScanning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331889683bcd65aa19ed9eae48fbaf62646972c2f94174a855b8ad254adacb3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsCertificate",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class ZeroTrustGatewaySettingsCertificate:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of certificate for TLS interception. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e9786c5067acd84d4389969a90eae8798764ce64c0a2e3d3196b680f67eae8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of certificate for TLS interception.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id}

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
        return "ZeroTrustGatewaySettingsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d1224d3e7062fade21976907776454e544e205c7912c8d26a6256c392eea0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a39d3c4ce993d9f450cbcfe4a12ff2902927cd49cc96b64940673ca12f0af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsCertificate]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9444a264c7ceffe122f683b417837adbe4cacfdb12dc149c4d28380f795624a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsConfig",
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
        "activity_log_enabled": "activityLogEnabled",
        "antivirus": "antivirus",
        "block_page": "blockPage",
        "body_scanning": "bodyScanning",
        "certificate": "certificate",
        "custom_certificate": "customCertificate",
        "extended_email_matching": "extendedEmailMatching",
        "fips": "fips",
        "id": "id",
        "logging": "logging",
        "non_identity_browser_isolation_enabled": "nonIdentityBrowserIsolationEnabled",
        "payload_log": "payloadLog",
        "protocol_detection_enabled": "protocolDetectionEnabled",
        "proxy": "proxy",
        "ssh_session_log": "sshSessionLog",
        "tls_decrypt_enabled": "tlsDecryptEnabled",
        "url_browser_isolation_enabled": "urlBrowserIsolationEnabled",
    },
)
class ZeroTrustGatewaySettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        antivirus: typing.Optional[typing.Union[ZeroTrustGatewaySettingsAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
        block_page: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
        body_scanning: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[ZeroTrustGatewaySettingsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_certificate: typing.Optional[typing.Union["ZeroTrustGatewaySettingsCustomCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_email_matching: typing.Optional[typing.Union["ZeroTrustGatewaySettingsExtendedEmailMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        fips: typing.Optional[typing.Union["ZeroTrustGatewaySettingsFips", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["ZeroTrustGatewaySettingsLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        payload_log: typing.Optional[typing.Union["ZeroTrustGatewaySettingsPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy: typing.Optional[typing.Union["ZeroTrustGatewaySettingsProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_session_log: typing.Optional[typing.Union["ZeroTrustGatewaySettingsSshSessionLog", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_decrypt_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        url_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#account_id ZeroTrustGatewaySettings#account_id}
        :param activity_log_enabled: Whether to enable the activity log. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#activity_log_enabled ZeroTrustGatewaySettings#activity_log_enabled}
        :param antivirus: antivirus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#antivirus ZeroTrustGatewaySettings#antivirus}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#block_page ZeroTrustGatewaySettings#block_page}
        :param body_scanning: body_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#body_scanning ZeroTrustGatewaySettings#body_scanning}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#certificate ZeroTrustGatewaySettings#certificate}
        :param custom_certificate: custom_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#custom_certificate ZeroTrustGatewaySettings#custom_certificate}
        :param extended_email_matching: extended_email_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#extended_email_matching ZeroTrustGatewaySettings#extended_email_matching}
        :param fips: fips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fips ZeroTrustGatewaySettings#fips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logging ZeroTrustGatewaySettings#logging}
        :param non_identity_browser_isolation_enabled: Enable non-identity onramp for Browser Isolation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#non_identity_browser_isolation_enabled ZeroTrustGatewaySettings#non_identity_browser_isolation_enabled}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#payload_log ZeroTrustGatewaySettings#payload_log}
        :param protocol_detection_enabled: Indicator that protocol detection is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#protocol_detection_enabled ZeroTrustGatewaySettings#protocol_detection_enabled}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#proxy ZeroTrustGatewaySettings#proxy}
        :param ssh_session_log: ssh_session_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#ssh_session_log ZeroTrustGatewaySettings#ssh_session_log}
        :param tls_decrypt_enabled: Indicator that decryption of TLS traffic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls_decrypt_enabled ZeroTrustGatewaySettings#tls_decrypt_enabled}
        :param url_browser_isolation_enabled: Safely browse websites in Browser Isolation through a URL. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#url_browser_isolation_enabled ZeroTrustGatewaySettings#url_browser_isolation_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(antivirus, dict):
            antivirus = ZeroTrustGatewaySettingsAntivirus(**antivirus)
        if isinstance(block_page, dict):
            block_page = ZeroTrustGatewaySettingsBlockPage(**block_page)
        if isinstance(body_scanning, dict):
            body_scanning = ZeroTrustGatewaySettingsBodyScanning(**body_scanning)
        if isinstance(certificate, dict):
            certificate = ZeroTrustGatewaySettingsCertificate(**certificate)
        if isinstance(custom_certificate, dict):
            custom_certificate = ZeroTrustGatewaySettingsCustomCertificate(**custom_certificate)
        if isinstance(extended_email_matching, dict):
            extended_email_matching = ZeroTrustGatewaySettingsExtendedEmailMatching(**extended_email_matching)
        if isinstance(fips, dict):
            fips = ZeroTrustGatewaySettingsFips(**fips)
        if isinstance(logging, dict):
            logging = ZeroTrustGatewaySettingsLogging(**logging)
        if isinstance(payload_log, dict):
            payload_log = ZeroTrustGatewaySettingsPayloadLog(**payload_log)
        if isinstance(proxy, dict):
            proxy = ZeroTrustGatewaySettingsProxy(**proxy)
        if isinstance(ssh_session_log, dict):
            ssh_session_log = ZeroTrustGatewaySettingsSshSessionLog(**ssh_session_log)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322ff5308daf0c47711318ff672028d3699332013934aecc39310a2adc383991)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument activity_log_enabled", value=activity_log_enabled, expected_type=type_hints["activity_log_enabled"])
            check_type(argname="argument antivirus", value=antivirus, expected_type=type_hints["antivirus"])
            check_type(argname="argument block_page", value=block_page, expected_type=type_hints["block_page"])
            check_type(argname="argument body_scanning", value=body_scanning, expected_type=type_hints["body_scanning"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument extended_email_matching", value=extended_email_matching, expected_type=type_hints["extended_email_matching"])
            check_type(argname="argument fips", value=fips, expected_type=type_hints["fips"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument non_identity_browser_isolation_enabled", value=non_identity_browser_isolation_enabled, expected_type=type_hints["non_identity_browser_isolation_enabled"])
            check_type(argname="argument payload_log", value=payload_log, expected_type=type_hints["payload_log"])
            check_type(argname="argument protocol_detection_enabled", value=protocol_detection_enabled, expected_type=type_hints["protocol_detection_enabled"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument ssh_session_log", value=ssh_session_log, expected_type=type_hints["ssh_session_log"])
            check_type(argname="argument tls_decrypt_enabled", value=tls_decrypt_enabled, expected_type=type_hints["tls_decrypt_enabled"])
            check_type(argname="argument url_browser_isolation_enabled", value=url_browser_isolation_enabled, expected_type=type_hints["url_browser_isolation_enabled"])
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
        if activity_log_enabled is not None:
            self._values["activity_log_enabled"] = activity_log_enabled
        if antivirus is not None:
            self._values["antivirus"] = antivirus
        if block_page is not None:
            self._values["block_page"] = block_page
        if body_scanning is not None:
            self._values["body_scanning"] = body_scanning
        if certificate is not None:
            self._values["certificate"] = certificate
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if extended_email_matching is not None:
            self._values["extended_email_matching"] = extended_email_matching
        if fips is not None:
            self._values["fips"] = fips
        if id is not None:
            self._values["id"] = id
        if logging is not None:
            self._values["logging"] = logging
        if non_identity_browser_isolation_enabled is not None:
            self._values["non_identity_browser_isolation_enabled"] = non_identity_browser_isolation_enabled
        if payload_log is not None:
            self._values["payload_log"] = payload_log
        if protocol_detection_enabled is not None:
            self._values["protocol_detection_enabled"] = protocol_detection_enabled
        if proxy is not None:
            self._values["proxy"] = proxy
        if ssh_session_log is not None:
            self._values["ssh_session_log"] = ssh_session_log
        if tls_decrypt_enabled is not None:
            self._values["tls_decrypt_enabled"] = tls_decrypt_enabled
        if url_browser_isolation_enabled is not None:
            self._values["url_browser_isolation_enabled"] = url_browser_isolation_enabled

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#account_id ZeroTrustGatewaySettings#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activity_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable the activity log.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#activity_log_enabled ZeroTrustGatewaySettings#activity_log_enabled}
        '''
        result = self._values.get("activity_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def antivirus(self) -> typing.Optional[ZeroTrustGatewaySettingsAntivirus]:
        '''antivirus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#antivirus ZeroTrustGatewaySettings#antivirus}
        '''
        result = self._values.get("antivirus")
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsAntivirus], result)

    @builtins.property
    def block_page(self) -> typing.Optional[ZeroTrustGatewaySettingsBlockPage]:
        '''block_page block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#block_page ZeroTrustGatewaySettings#block_page}
        '''
        result = self._values.get("block_page")
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsBlockPage], result)

    @builtins.property
    def body_scanning(self) -> typing.Optional[ZeroTrustGatewaySettingsBodyScanning]:
        '''body_scanning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#body_scanning ZeroTrustGatewaySettings#body_scanning}
        '''
        result = self._values.get("body_scanning")
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsBodyScanning], result)

    @builtins.property
    def certificate(self) -> typing.Optional[ZeroTrustGatewaySettingsCertificate]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#certificate ZeroTrustGatewaySettings#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsCertificate], result)

    @builtins.property
    def custom_certificate(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsCustomCertificate"]:
        '''custom_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#custom_certificate ZeroTrustGatewaySettings#custom_certificate}
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsCustomCertificate"], result)

    @builtins.property
    def extended_email_matching(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsExtendedEmailMatching"]:
        '''extended_email_matching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#extended_email_matching ZeroTrustGatewaySettings#extended_email_matching}
        '''
        result = self._values.get("extended_email_matching")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsExtendedEmailMatching"], result)

    @builtins.property
    def fips(self) -> typing.Optional["ZeroTrustGatewaySettingsFips"]:
        '''fips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#fips ZeroTrustGatewaySettings#fips}
        '''
        result = self._values.get("fips")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsFips"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional["ZeroTrustGatewaySettingsLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#logging ZeroTrustGatewaySettings#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsLogging"], result)

    @builtins.property
    def non_identity_browser_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable non-identity onramp for Browser Isolation. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#non_identity_browser_isolation_enabled ZeroTrustGatewaySettings#non_identity_browser_isolation_enabled}
        '''
        result = self._values.get("non_identity_browser_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def payload_log(self) -> typing.Optional["ZeroTrustGatewaySettingsPayloadLog"]:
        '''payload_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#payload_log ZeroTrustGatewaySettings#payload_log}
        '''
        result = self._values.get("payload_log")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsPayloadLog"], result)

    @builtins.property
    def protocol_detection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that protocol detection is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#protocol_detection_enabled ZeroTrustGatewaySettings#protocol_detection_enabled}
        '''
        result = self._values.get("protocol_detection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy(self) -> typing.Optional["ZeroTrustGatewaySettingsProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#proxy ZeroTrustGatewaySettings#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsProxy"], result)

    @builtins.property
    def ssh_session_log(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsSshSessionLog"]:
        '''ssh_session_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#ssh_session_log ZeroTrustGatewaySettings#ssh_session_log}
        '''
        result = self._values.get("ssh_session_log")
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsSshSessionLog"], result)

    @builtins.property
    def tls_decrypt_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that decryption of TLS traffic is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls_decrypt_enabled ZeroTrustGatewaySettings#tls_decrypt_enabled}
        '''
        result = self._values.get("tls_decrypt_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def url_browser_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Safely browse websites in Browser Isolation through a URL. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#url_browser_isolation_enabled ZeroTrustGatewaySettings#url_browser_isolation_enabled}
        '''
        result = self._values.get("url_browser_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsCustomCertificate",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "id": "id"},
)
class ZeroTrustGatewaySettingsCustomCertificate:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether TLS encryption should use a custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        :param id: ID of custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa9ac9788657566dfefcc932948f9ba39fd0f8877182b91baa8f602f571b52b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether TLS encryption should use a custom certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of custom certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#id ZeroTrustGatewaySettings#id}

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
        return "ZeroTrustGatewaySettingsCustomCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsCustomCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsCustomCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1097662eb7faa3cfee737d111c0866b34d3f506d61ef369cfd51f6eca9c5013f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a44a727bb3f93c9f997b533d947a6abb32a487a3719dd8ee8842bb153bd67c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e522135454904afb1c41c95125ce2b15e091a1cc13113e6f4cfcc9426cf0737d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsCustomCertificate]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsCustomCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsCustomCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ea7e2edb280e94e8c9dad5a8f63845d4d2794bf3263b2fe8a2cc953bd071d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsExtendedEmailMatching",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ZeroTrustGatewaySettingsExtendedEmailMatching:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc1e682c3640c24403d3834bf74b2d4bbf29a044ada323b5e0106027081f21e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#enabled ZeroTrustGatewaySettings#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsExtendedEmailMatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsExtendedEmailMatchingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsExtendedEmailMatchingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2311620c7bdbc9047919998c7f3610f781f77b08dec5a46a46a75479f6caf7fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9f18c8f02d63ce68e0a61cde4ca9ce448259f5d2c08f8b031669484fd858eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsExtendedEmailMatching]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsExtendedEmailMatching], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsExtendedEmailMatching],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effb4bf1782c51c771bc8a4a5864dd70963085369fc7aeeb7eb1c51f8e4d801f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsFips",
    jsii_struct_bases=[],
    name_mapping={"tls": "tls"},
)
class ZeroTrustGatewaySettingsFips:
    def __init__(
        self,
        *,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param tls: Only allow FIPS-compliant TLS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls ZeroTrustGatewaySettings#tls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd557241794ac6f417ade4765df2dcddad0bf8ffee4a64268465ec8ed6811e1)
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow FIPS-compliant TLS configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tls ZeroTrustGatewaySettings#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsFips(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsFipsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsFipsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d613df1e0f344d17eda1654be919ac77697b119795d34518efe6c4e8a4a2b8f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tls"))

    @tls.setter
    def tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930cfab08485de311c27b30962317418de4f15e01042cea5c8aad139f8de9911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsFips]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsFips], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsFips],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbbcdf57e7ec24ebc402ed72e4b381cff5f2771381e664332c3ec6d4894ee8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLogging",
    jsii_struct_bases=[],
    name_mapping={
        "redact_pii": "redactPii",
        "settings_by_rule_type": "settingsByRuleType",
    },
)
class ZeroTrustGatewaySettingsLogging:
    def __init__(
        self,
        *,
        redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        settings_by_rule_type: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleType", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param redact_pii: Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#redact_pii ZeroTrustGatewaySettings#redact_pii}
        :param settings_by_rule_type: settings_by_rule_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#settings_by_rule_type ZeroTrustGatewaySettings#settings_by_rule_type}
        '''
        if isinstance(settings_by_rule_type, dict):
            settings_by_rule_type = ZeroTrustGatewaySettingsLoggingSettingsByRuleType(**settings_by_rule_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b97d20b9eb69a88247270441a2df923b834aa44eb8e92872548fe5e31178b2)
            check_type(argname="argument redact_pii", value=redact_pii, expected_type=type_hints["redact_pii"])
            check_type(argname="argument settings_by_rule_type", value=settings_by_rule_type, expected_type=type_hints["settings_by_rule_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redact_pii": redact_pii,
            "settings_by_rule_type": settings_by_rule_type,
        }

    @builtins.property
    def redact_pii(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#redact_pii ZeroTrustGatewaySettings#redact_pii}
        '''
        result = self._values.get("redact_pii")
        assert result is not None, "Required property 'redact_pii' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def settings_by_rule_type(
        self,
    ) -> "ZeroTrustGatewaySettingsLoggingSettingsByRuleType":
        '''settings_by_rule_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#settings_by_rule_type ZeroTrustGatewaySettings#settings_by_rule_type}
        '''
        result = self._values.get("settings_by_rule_type")
        assert result is not None, "Required property 'settings_by_rule_type' is missing"
        return typing.cast("ZeroTrustGatewaySettingsLoggingSettingsByRuleType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d3da01cc467bdcb3ee769aa8b9cc68b58ca34b4aab086c96068ecd0b6fd329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettingsByRuleType")
    def put_settings_by_rule_type(
        self,
        *,
        dns: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns", typing.Dict[builtins.str, typing.Any]],
        http: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp", typing.Dict[builtins.str, typing.Any]],
        l4: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#dns ZeroTrustGatewaySettings#dns}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#http ZeroTrustGatewaySettings#http}
        :param l4: l4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#l4 ZeroTrustGatewaySettings#l4}
        '''
        value = ZeroTrustGatewaySettingsLoggingSettingsByRuleType(
            dns=dns, http=http, l4=l4
        )

        return typing.cast(None, jsii.invoke(self, "putSettingsByRuleType", [value]))

    @builtins.property
    @jsii.member(jsii_name="settingsByRuleType")
    def settings_by_rule_type(
        self,
    ) -> "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeOutputReference":
        return typing.cast("ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeOutputReference", jsii.get(self, "settingsByRuleType"))

    @builtins.property
    @jsii.member(jsii_name="redactPiiInput")
    def redact_pii_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "redactPiiInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsByRuleTypeInput")
    def settings_by_rule_type_input(
        self,
    ) -> typing.Optional["ZeroTrustGatewaySettingsLoggingSettingsByRuleType"]:
        return typing.cast(typing.Optional["ZeroTrustGatewaySettingsLoggingSettingsByRuleType"], jsii.get(self, "settingsByRuleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="redactPii")
    def redact_pii(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "redactPii"))

    @redact_pii.setter
    def redact_pii(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f09932b4daf66f5c81279707174f3ce219c1f8c3616f72566097998797a2e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactPii", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsLogging]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsLogging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bffc2f28b662994d0b764f7573fab16092c96ee63dda88a6e26befe1b2f5d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleType",
    jsii_struct_bases=[],
    name_mapping={"dns": "dns", "http": "http", "l4": "l4"},
)
class ZeroTrustGatewaySettingsLoggingSettingsByRuleType:
    def __init__(
        self,
        *,
        dns: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns", typing.Dict[builtins.str, typing.Any]],
        http: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp", typing.Dict[builtins.str, typing.Any]],
        l4: typing.Union["ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#dns ZeroTrustGatewaySettings#dns}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#http ZeroTrustGatewaySettings#http}
        :param l4: l4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#l4 ZeroTrustGatewaySettings#l4}
        '''
        if isinstance(dns, dict):
            dns = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns(**dns)
        if isinstance(http, dict):
            http = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp(**http)
        if isinstance(l4, dict):
            l4 = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4(**l4)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b657d24ad55651e7b9785ae7421dbfded30f196dba75ae072419ba75242936b9)
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument l4", value=l4, expected_type=type_hints["l4"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns": dns,
            "http": http,
            "l4": l4,
        }

    @builtins.property
    def dns(self) -> "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns":
        '''dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#dns ZeroTrustGatewaySettings#dns}
        '''
        result = self._values.get("dns")
        assert result is not None, "Required property 'dns' is missing"
        return typing.cast("ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns", result)

    @builtins.property
    def http(self) -> "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp":
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#http ZeroTrustGatewaySettings#http}
        '''
        result = self._values.get("http")
        assert result is not None, "Required property 'http' is missing"
        return typing.cast("ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp", result)

    @builtins.property
    def l4(self) -> "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4":
        '''l4 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#l4 ZeroTrustGatewaySettings#l4}
        '''
        result = self._values.get("l4")
        assert result is not None, "Required property 'l4' is missing"
        return typing.cast("ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsLoggingSettingsByRuleType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df1f92cede73278805cd67e55f91f767fa0289e13ae9640712160406ca00002)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45ea1224fad7e6db82b69251cd776d8dc5126f69227ab606a9e4badc963db80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAllInput")
    def log_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logAllInput"))

    @builtins.property
    @jsii.member(jsii_name="logBlocksInput")
    def log_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="logAll")
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logAll"))

    @log_all.setter
    def log_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e670de06a563d7b034cc8cfbc1225f581dea55f2eca7681c3715b5f0599d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logBlocks")
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logBlocks"))

    @log_blocks.setter
    def log_blocks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0e21bf12f376ee9efd538f8159b10d0bdb14ea60589baa63201d95b0f69eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a6f55ce93a0d914b2d356aaf82d769cbaef164a57873eb12b995b0bcba73a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15751b0360426b300c8aa1d42bbdcab68e087e53d29ff94d4f35a9495c11eb36)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9fe36ac50421713c1078f52ed0e04df79d0477c78d43e7ba496be9a75be8cb5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAllInput")
    def log_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logAllInput"))

    @builtins.property
    @jsii.member(jsii_name="logBlocksInput")
    def log_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="logAll")
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logAll"))

    @log_all.setter
    def log_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28c9087ca50eab209ea12bc20ea0a027333da1a54f79c375e4b3b5ada036b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logBlocks")
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logBlocks"))

    @log_blocks.setter
    def log_blocks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb2821bf2048274dd52054a83d61bb6add3343658f2c49794b56ad1b5963fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a416302b103436a2edcf02678360208df47a5d15ea0f69f734d2f07387c70c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5fe61a91bac48d9c095576a913e55272fe6e80f1cdeea5fb4f414a226f6f37)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6282dc1c42b96f1d325901f4eba9c7a5f9d24ab866fc2d4e492aad525d115d2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logAllInput")
    def log_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logAllInput"))

    @builtins.property
    @jsii.member(jsii_name="logBlocksInput")
    def log_blocks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="logAll")
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logAll"))

    @log_all.setter
    def log_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0616d2b8b109e5696effd242d889fc02d7e9157b50030f500693eb8d2c3224e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logBlocks")
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logBlocks"))

    @log_blocks.setter
    def log_blocks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe48261579d7fd6c53570ba76cf449b47878178108b48a5db7caffc70c00730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9b782103bac10e4bfee842d163db1487454925a05b478b31649e77937a01b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c93710166ac645ce3bab9c8a81856166efee95c2d02d310ef7df2456194b6539)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDns")
    def put_dns(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        value = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns(
            log_all=log_all, log_blocks=log_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putDns", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        value = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp(
            log_all=log_all, log_blocks=log_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putL4")
    def put_l4(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_all ZeroTrustGatewaySettings#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#log_blocks ZeroTrustGatewaySettings#log_blocks}.
        '''
        value = ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4(
            log_all=log_all, log_blocks=log_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putL4", [value]))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(
        self,
    ) -> ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDnsOutputReference:
        return typing.cast(ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDnsOutputReference, jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(
        self,
    ) -> ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttpOutputReference:
        return typing.cast(ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttpOutputReference, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="l4")
    def l4(self) -> ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4OutputReference:
        return typing.cast(ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4OutputReference, jsii.get(self, "l4"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="l4Input")
    def l4_input(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4], jsii.get(self, "l4Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleType]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be9bc39d2146208ae8009d1ceaceb0934b39ed56ff154165ba619de612e8ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsPayloadLog",
    jsii_struct_bases=[],
    name_mapping={"public_key": "publicKey"},
)
class ZeroTrustGatewaySettingsPayloadLog:
    def __init__(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt matched payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d7724e2446ac19e60dacb460984a1d75fd9ade2e39085daf62401d03337255)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
        }

    @builtins.property
    def public_key(self) -> builtins.str:
        '''Public key used to encrypt matched payloads.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsPayloadLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsPayloadLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsPayloadLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d402127f870a743e0a348580855d710339dff5286db8d814ab867c735289cf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95233322d9e59477e6e88217e45514557df9a8971f8a81d705ac0c9daf15ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsPayloadLog]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsPayloadLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsPayloadLog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5745cbdd6aa61f033c1e5ed7d60f511e501f4328fbdf1ed6091b328e94313d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsProxy",
    jsii_struct_bases=[],
    name_mapping={
        "disable_for_time": "disableForTime",
        "root_ca": "rootCa",
        "tcp": "tcp",
        "udp": "udp",
        "virtual_ip": "virtualIp",
    },
)
class ZeroTrustGatewaySettingsProxy:
    def __init__(
        self,
        *,
        disable_for_time: jsii.Number,
        root_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        tcp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        udp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        virtual_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_for_time: Sets the time limit in seconds that a user can use an override code to bypass WARP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#disable_for_time ZeroTrustGatewaySettings#disable_for_time}
        :param root_ca: Whether root ca is enabled account wide for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#root_ca ZeroTrustGatewaySettings#root_ca}
        :param tcp: Whether gateway proxy is enabled on gateway devices for TCP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tcp ZeroTrustGatewaySettings#tcp}
        :param udp: Whether gateway proxy is enabled on gateway devices for UDP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#udp ZeroTrustGatewaySettings#udp}
        :param virtual_ip: Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#virtual_ip ZeroTrustGatewaySettings#virtual_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fc65e05753867977df7d0b2ad76f8440f0ed89a33e87270e6fae8c9f7bd001)
            check_type(argname="argument disable_for_time", value=disable_for_time, expected_type=type_hints["disable_for_time"])
            check_type(argname="argument root_ca", value=root_ca, expected_type=type_hints["root_ca"])
            check_type(argname="argument tcp", value=tcp, expected_type=type_hints["tcp"])
            check_type(argname="argument udp", value=udp, expected_type=type_hints["udp"])
            check_type(argname="argument virtual_ip", value=virtual_ip, expected_type=type_hints["virtual_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disable_for_time": disable_for_time,
            "root_ca": root_ca,
            "tcp": tcp,
            "udp": udp,
            "virtual_ip": virtual_ip,
        }

    @builtins.property
    def disable_for_time(self) -> jsii.Number:
        '''Sets the time limit in seconds that a user can use an override code to bypass WARP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#disable_for_time ZeroTrustGatewaySettings#disable_for_time}
        '''
        result = self._values.get("disable_for_time")
        assert result is not None, "Required property 'disable_for_time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def root_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether root ca is enabled account wide for ZT clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#root_ca ZeroTrustGatewaySettings#root_ca}
        '''
        result = self._values.get("root_ca")
        assert result is not None, "Required property 'root_ca' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def tcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether gateway proxy is enabled on gateway devices for TCP traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#tcp ZeroTrustGatewaySettings#tcp}
        '''
        result = self._values.get("tcp")
        assert result is not None, "Required property 'tcp' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def udp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether gateway proxy is enabled on gateway devices for UDP traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#udp ZeroTrustGatewaySettings#udp}
        '''
        result = self._values.get("udp")
        assert result is not None, "Required property 'udp' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def virtual_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#virtual_ip ZeroTrustGatewaySettings#virtual_ip}
        '''
        result = self._values.get("virtual_ip")
        assert result is not None, "Required property 'virtual_ip' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2f62e69490c957dce0cc9501e74c93940e691497957fbfb2e8ddb17b6b33a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="disableForTimeInput")
    def disable_for_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "disableForTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rootCaInput")
    def root_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootCaInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpInput")
    def tcp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tcpInput"))

    @builtins.property
    @jsii.member(jsii_name="udpInput")
    def udp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "udpInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualIpInput")
    def virtual_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "virtualIpInput"))

    @builtins.property
    @jsii.member(jsii_name="disableForTime")
    def disable_for_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "disableForTime"))

    @disable_for_time.setter
    def disable_for_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4388670cda180501c39743aeb4032f8a388489ffaf5d978b403037ea4a74f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableForTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootCa")
    def root_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootCa"))

    @root_ca.setter
    def root_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ce2878542bd168b5013be3e60284c89520df9281b066957e24e02e6a66f09e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcp")
    def tcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tcp"))

    @tcp.setter
    def tcp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2221819d42c1e99117b08836b99af6e6cc0654a7070af56d88dfc8c8a2be5c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="udp")
    def udp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "udp"))

    @udp.setter
    def udp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fd5606a0dd740db1585e05c8af27c4d0c508cdc4fa8ea8fc4b9af5ca0a7d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "udp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualIp")
    def virtual_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "virtualIp"))

    @virtual_ip.setter
    def virtual_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f407875936cee3542086ba872c91fb671536edc877e8561d91172b494607eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsProxy]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsProxy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1df0e1a75c88fef1a0664d03a106b9dc0c535a8da6a9e04aa725f758f7256cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsSshSessionLog",
    jsii_struct_bases=[],
    name_mapping={"public_key": "publicKey"},
)
class ZeroTrustGatewaySettingsSshSessionLog:
    def __init__(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt ssh session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b032336f91a95e193eac515b232bd239848a759215b43f1efd8ad9dbd80b6a5)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
        }

    @builtins.property
    def public_key(self) -> builtins.str:
        '''Public key used to encrypt ssh session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_gateway_settings#public_key ZeroTrustGatewaySettings#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustGatewaySettingsSshSessionLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustGatewaySettingsSshSessionLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustGatewaySettings.ZeroTrustGatewaySettingsSshSessionLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d3622506e0d17ba3acc0250491ddba5e00d1e6d5b50e7a9d86054a8aaf7f99e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5caceb25191739a9296e3f2f824bf3e96348c2aa48300b46307551ebe0ea23f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustGatewaySettingsSshSessionLog]:
        return typing.cast(typing.Optional[ZeroTrustGatewaySettingsSshSessionLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustGatewaySettingsSshSessionLog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d136708b8877c0c90f23970d7e78e6ee868e904f23192b12572232941ca36df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ZeroTrustGatewaySettings",
    "ZeroTrustGatewaySettingsAntivirus",
    "ZeroTrustGatewaySettingsAntivirusNotificationSettings",
    "ZeroTrustGatewaySettingsAntivirusNotificationSettingsOutputReference",
    "ZeroTrustGatewaySettingsAntivirusOutputReference",
    "ZeroTrustGatewaySettingsBlockPage",
    "ZeroTrustGatewaySettingsBlockPageOutputReference",
    "ZeroTrustGatewaySettingsBodyScanning",
    "ZeroTrustGatewaySettingsBodyScanningOutputReference",
    "ZeroTrustGatewaySettingsCertificate",
    "ZeroTrustGatewaySettingsCertificateOutputReference",
    "ZeroTrustGatewaySettingsConfig",
    "ZeroTrustGatewaySettingsCustomCertificate",
    "ZeroTrustGatewaySettingsCustomCertificateOutputReference",
    "ZeroTrustGatewaySettingsExtendedEmailMatching",
    "ZeroTrustGatewaySettingsExtendedEmailMatchingOutputReference",
    "ZeroTrustGatewaySettingsFips",
    "ZeroTrustGatewaySettingsFipsOutputReference",
    "ZeroTrustGatewaySettingsLogging",
    "ZeroTrustGatewaySettingsLoggingOutputReference",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleType",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDnsOutputReference",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttpOutputReference",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4OutputReference",
    "ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeOutputReference",
    "ZeroTrustGatewaySettingsPayloadLog",
    "ZeroTrustGatewaySettingsPayloadLogOutputReference",
    "ZeroTrustGatewaySettingsProxy",
    "ZeroTrustGatewaySettingsProxyOutputReference",
    "ZeroTrustGatewaySettingsSshSessionLog",
    "ZeroTrustGatewaySettingsSshSessionLogOutputReference",
]

publication.publish()

def _typecheckingstub__e835aa6c5393b3bccb9f3757aa1cc8e34cee2d7a93e870dce8110f777030091f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    antivirus: typing.Optional[typing.Union[ZeroTrustGatewaySettingsAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    body_scanning: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[ZeroTrustGatewaySettingsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_certificate: typing.Optional[typing.Union[ZeroTrustGatewaySettingsCustomCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_email_matching: typing.Optional[typing.Union[ZeroTrustGatewaySettingsExtendedEmailMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    fips: typing.Optional[typing.Union[ZeroTrustGatewaySettingsFips, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[ZeroTrustGatewaySettingsLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    payload_log: typing.Optional[typing.Union[ZeroTrustGatewaySettingsPayloadLog, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy: typing.Optional[typing.Union[ZeroTrustGatewaySettingsProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_session_log: typing.Optional[typing.Union[ZeroTrustGatewaySettingsSshSessionLog, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_decrypt_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    url_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__b6a9c540ee48d79bc94bf225d2e7f3d25e0fad690ba5931d93c9793a03c42dc5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f323899588c0d92313196544d971a5ad585faf1ae29ee162ace9408ebbf9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e67adb7be19cbc0bfa87386d661d832826c3177cf4946417963b444a955c5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8065f220e57c4bb9150da43e628cbef3e8051a55479a0d41e7383e0bbf75aeb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f4552601a28dfbf82fc8d3554ad3cbfcd77cdd85a76fa4f5d99baea82a9ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3c3904870a6479963aa3a8a1c0ad7d9703eeaced18b4f0bb5747edff2a17e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034d122104b57d109ba82488c77b17f9f0ef9ff1895f10237a7c181f90c39e43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d90746c0ffcc71b60c262f043beb33b5eae8398e7d314ef7dcb3ce0c038558(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd09d9bb03971346980a53dc8beab627f106cbf77486b51dccc35893ca43614(
    *,
    enabled_download_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enabled_upload_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    fail_closed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_settings: typing.Optional[typing.Union[ZeroTrustGatewaySettingsAntivirusNotificationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e384ba76a5ab4cac986b4cb9f3bebaefc20aa9bda85ad259ec05cce0095aba2f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9cbbfef51b9b6eb0181a6fcff53adaaeb5bde7b8b41815d995a6d5b5d40f46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb49d002dd9dd29090e6fcd58b1f6bc26613d31a70b3e49e3a0acca5ae0e89ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60677138f2066b30df4b6e4fd243c387ac99f119b65f67492872b6266748f471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027440da9503127ee305d9ec89022a8e5d10831bf217d3017a4f36659b36bdf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0646275e897df75e03f5aaab591d07197ed83d764efa01aa0d02d1266340c4(
    value: typing.Optional[ZeroTrustGatewaySettingsAntivirusNotificationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b459be0ddf088ab3125eddad8594bb7fe2e4a2304a3a843a941d34d5831d25b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b6246c8f12cf4e4fab792a86ed696b5b5c799c3bbd37eade5636b07ab06202(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4b4f1f6f66c037e491ac994a1cf9b92d6b069a871a1d4192d7cf3bb3bff7a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3846bf104db1fc95e186b0c36aaabe5cd76c41ade765f0e6d7a0fff484bfcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3d80a64fcd759ab802b22dbe3ac6817d11d567d2c2c8afd10b68fe85e0e9c5(
    value: typing.Optional[ZeroTrustGatewaySettingsAntivirus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a3d39555b8fed1b96c70cda76ff3bac778cfbbe1eacb30bb48e2d9c75021fa(
    *,
    background_color: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    footer_text: typing.Optional[builtins.str] = None,
    header_text: typing.Optional[builtins.str] = None,
    logo_path: typing.Optional[builtins.str] = None,
    mailto_address: typing.Optional[builtins.str] = None,
    mailto_subject: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de512ad616d76473a8991922be1d543838a352b7d4de2ea83046759776c5a3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68001b8afac2bc05878d8e9bfc725da7d4f65d27ea7af5d598cdfa24f0af55c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fca6b35da440b5ac345def7ed662af2ecc19fae64ef148da3d533ebf6bcb84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a76dc8d24a81afd3136b88136492e34a41132e6929bdda7d853bf09b90aaa87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e1b413a98ab470a9849e1b38e5070509d379614b46535ef434a97afca9bd93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976c937cbb5b8b0fdc3b77da8944e686948c53a8c7fd90aabde66e267730c3d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211d4df20d4f3abe2c4d0497fb46597366801123fb4111c41f8335d31b6d8d21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af015bf5de56f891dab42cd5195bcdb478d316eec6ea1b4f1374e780d368c604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d32537fb31e9edb19563d8a7ce863eb9948472a700e417ee3932c17b1122b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d6613114a735f673702d4f0e6beb4ad448b066f9610348b8b2c2f29e0f341(
    value: typing.Optional[ZeroTrustGatewaySettingsBlockPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cbbd170d8f6f823b820893b3ed5a378a7bc1843ad9c8cf0fb70afe70ae4020(
    *,
    inspection_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c0ab277084fa98b64514c01af9602325cd0de67fa0899bf5fba93bfee35db1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2773fc034e0a156ea01bdca9c8fab8d7a3bf7ca154d0193269881916d7fcff04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331889683bcd65aa19ed9eae48fbaf62646972c2f94174a855b8ad254adacb3a(
    value: typing.Optional[ZeroTrustGatewaySettingsBodyScanning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e9786c5067acd84d4389969a90eae8798764ce64c0a2e3d3196b680f67eae8(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d1224d3e7062fade21976907776454e544e205c7912c8d26a6256c392eea0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a39d3c4ce993d9f450cbcfe4a12ff2902927cd49cc96b64940673ca12f0af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9444a264c7ceffe122f683b417837adbe4cacfdb12dc149c4d28380f795624a8(
    value: typing.Optional[ZeroTrustGatewaySettingsCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322ff5308daf0c47711318ff672028d3699332013934aecc39310a2adc383991(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    antivirus: typing.Optional[typing.Union[ZeroTrustGatewaySettingsAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    body_scanning: typing.Optional[typing.Union[ZeroTrustGatewaySettingsBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[ZeroTrustGatewaySettingsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_certificate: typing.Optional[typing.Union[ZeroTrustGatewaySettingsCustomCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_email_matching: typing.Optional[typing.Union[ZeroTrustGatewaySettingsExtendedEmailMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    fips: typing.Optional[typing.Union[ZeroTrustGatewaySettingsFips, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[ZeroTrustGatewaySettingsLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    payload_log: typing.Optional[typing.Union[ZeroTrustGatewaySettingsPayloadLog, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy: typing.Optional[typing.Union[ZeroTrustGatewaySettingsProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_session_log: typing.Optional[typing.Union[ZeroTrustGatewaySettingsSshSessionLog, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_decrypt_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    url_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa9ac9788657566dfefcc932948f9ba39fd0f8877182b91baa8f602f571b52b(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1097662eb7faa3cfee737d111c0866b34d3f506d61ef369cfd51f6eca9c5013f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44a727bb3f93c9f997b533d947a6abb32a487a3719dd8ee8842bb153bd67c39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e522135454904afb1c41c95125ce2b15e091a1cc13113e6f4cfcc9426cf0737d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ea7e2edb280e94e8c9dad5a8f63845d4d2794bf3263b2fe8a2cc953bd071d8(
    value: typing.Optional[ZeroTrustGatewaySettingsCustomCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc1e682c3640c24403d3834bf74b2d4bbf29a044ada323b5e0106027081f21e(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2311620c7bdbc9047919998c7f3610f781f77b08dec5a46a46a75479f6caf7fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f18c8f02d63ce68e0a61cde4ca9ce448259f5d2c08f8b031669484fd858eb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effb4bf1782c51c771bc8a4a5864dd70963085369fc7aeeb7eb1c51f8e4d801f(
    value: typing.Optional[ZeroTrustGatewaySettingsExtendedEmailMatching],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd557241794ac6f417ade4765df2dcddad0bf8ffee4a64268465ec8ed6811e1(
    *,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d613df1e0f344d17eda1654be919ac77697b119795d34518efe6c4e8a4a2b8f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930cfab08485de311c27b30962317418de4f15e01042cea5c8aad139f8de9911(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbbcdf57e7ec24ebc402ed72e4b381cff5f2771381e664332c3ec6d4894ee8b(
    value: typing.Optional[ZeroTrustGatewaySettingsFips],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b97d20b9eb69a88247270441a2df923b834aa44eb8e92872548fe5e31178b2(
    *,
    redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    settings_by_rule_type: typing.Union[ZeroTrustGatewaySettingsLoggingSettingsByRuleType, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d3da01cc467bdcb3ee769aa8b9cc68b58ca34b4aab086c96068ecd0b6fd329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f09932b4daf66f5c81279707174f3ce219c1f8c3616f72566097998797a2e6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bffc2f28b662994d0b764f7573fab16092c96ee63dda88a6e26befe1b2f5d55(
    value: typing.Optional[ZeroTrustGatewaySettingsLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b657d24ad55651e7b9785ae7421dbfded30f196dba75ae072419ba75242936b9(
    *,
    dns: typing.Union[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns, typing.Dict[builtins.str, typing.Any]],
    http: typing.Union[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp, typing.Dict[builtins.str, typing.Any]],
    l4: typing.Union[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df1f92cede73278805cd67e55f91f767fa0289e13ae9640712160406ca00002(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45ea1224fad7e6db82b69251cd776d8dc5126f69227ab606a9e4badc963db80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e670de06a563d7b034cc8cfbc1225f581dea55f2eca7681c3715b5f0599d50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0e21bf12f376ee9efd538f8159b10d0bdb14ea60589baa63201d95b0f69eab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a6f55ce93a0d914b2d356aaf82d769cbaef164a57873eb12b995b0bcba73a6(
    value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15751b0360426b300c8aa1d42bbdcab68e087e53d29ff94d4f35a9495c11eb36(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fe36ac50421713c1078f52ed0e04df79d0477c78d43e7ba496be9a75be8cb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28c9087ca50eab209ea12bc20ea0a027333da1a54f79c375e4b3b5ada036b76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb2821bf2048274dd52054a83d61bb6add3343658f2c49794b56ad1b5963fbc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a416302b103436a2edcf02678360208df47a5d15ea0f69f734d2f07387c70c7b(
    value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeHttp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5fe61a91bac48d9c095576a913e55272fe6e80f1cdeea5fb4f414a226f6f37(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6282dc1c42b96f1d325901f4eba9c7a5f9d24ab866fc2d4e492aad525d115d2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0616d2b8b109e5696effd242d889fc02d7e9157b50030f500693eb8d2c3224e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe48261579d7fd6c53570ba76cf449b47878178108b48a5db7caffc70c00730(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9b782103bac10e4bfee842d163db1487454925a05b478b31649e77937a01b9(
    value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleTypeL4],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93710166ac645ce3bab9c8a81856166efee95c2d02d310ef7df2456194b6539(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be9bc39d2146208ae8009d1ceaceb0934b39ed56ff154165ba619de612e8ec8(
    value: typing.Optional[ZeroTrustGatewaySettingsLoggingSettingsByRuleType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d7724e2446ac19e60dacb460984a1d75fd9ade2e39085daf62401d03337255(
    *,
    public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d402127f870a743e0a348580855d710339dff5286db8d814ab867c735289cf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95233322d9e59477e6e88217e45514557df9a8971f8a81d705ac0c9daf15ad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5745cbdd6aa61f033c1e5ed7d60f511e501f4328fbdf1ed6091b328e94313d2(
    value: typing.Optional[ZeroTrustGatewaySettingsPayloadLog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fc65e05753867977df7d0b2ad76f8440f0ed89a33e87270e6fae8c9f7bd001(
    *,
    disable_for_time: jsii.Number,
    root_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    tcp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    udp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    virtual_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2f62e69490c957dce0cc9501e74c93940e691497957fbfb2e8ddb17b6b33a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4388670cda180501c39743aeb4032f8a388489ffaf5d978b403037ea4a74f0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ce2878542bd168b5013be3e60284c89520df9281b066957e24e02e6a66f09e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2221819d42c1e99117b08836b99af6e6cc0654a7070af56d88dfc8c8a2be5c73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fd5606a0dd740db1585e05c8af27c4d0c508cdc4fa8ea8fc4b9af5ca0a7d1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f407875936cee3542086ba872c91fb671536edc877e8561d91172b494607eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df0e1a75c88fef1a0664d03a106b9dc0c535a8da6a9e04aa725f758f7256cd(
    value: typing.Optional[ZeroTrustGatewaySettingsProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b032336f91a95e193eac515b232bd239848a759215b43f1efd8ad9dbd80b6a5(
    *,
    public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3622506e0d17ba3acc0250491ddba5e00d1e6d5b50e7a9d86054a8aaf7f99e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5caceb25191739a9296e3f2f824bf3e96348c2aa48300b46307551ebe0ea23f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d136708b8877c0c90f23970d7e78e6ee868e904f23192b12572232941ca36df(
    value: typing.Optional[ZeroTrustGatewaySettingsSshSessionLog],
) -> None:
    """Type checking stubs"""
    pass
