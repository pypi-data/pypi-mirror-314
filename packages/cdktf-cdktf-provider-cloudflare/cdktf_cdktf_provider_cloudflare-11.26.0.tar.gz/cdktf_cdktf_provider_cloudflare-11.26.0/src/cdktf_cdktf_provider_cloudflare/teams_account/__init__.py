r'''
# `cloudflare_teams_account`

Refer to the Terraform Registry for docs: [`cloudflare_teams_account`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account).
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


class TeamsAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account cloudflare_teams_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        antivirus: typing.Optional[typing.Union["TeamsAccountAntivirus", typing.Dict[builtins.str, typing.Any]]] = None,
        block_page: typing.Optional[typing.Union["TeamsAccountBlockPage", typing.Dict[builtins.str, typing.Any]]] = None,
        body_scanning: typing.Optional[typing.Union["TeamsAccountBodyScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union["TeamsAccountCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_certificate: typing.Optional[typing.Union["TeamsAccountCustomCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_email_matching: typing.Optional[typing.Union["TeamsAccountExtendedEmailMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        fips: typing.Optional[typing.Union["TeamsAccountFips", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["TeamsAccountLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        payload_log: typing.Optional[typing.Union["TeamsAccountPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy: typing.Optional[typing.Union["TeamsAccountProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_session_log: typing.Optional[typing.Union["TeamsAccountSshSessionLog", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account cloudflare_teams_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#account_id TeamsAccount#account_id}
        :param activity_log_enabled: Whether to enable the activity log. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#activity_log_enabled TeamsAccount#activity_log_enabled}
        :param antivirus: antivirus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#antivirus TeamsAccount#antivirus}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#block_page TeamsAccount#block_page}
        :param body_scanning: body_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#body_scanning TeamsAccount#body_scanning}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#certificate TeamsAccount#certificate}
        :param custom_certificate: custom_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#custom_certificate TeamsAccount#custom_certificate}
        :param extended_email_matching: extended_email_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#extended_email_matching TeamsAccount#extended_email_matching}
        :param fips: fips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fips TeamsAccount#fips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logging TeamsAccount#logging}
        :param non_identity_browser_isolation_enabled: Enable non-identity onramp for Browser Isolation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#non_identity_browser_isolation_enabled TeamsAccount#non_identity_browser_isolation_enabled}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#payload_log TeamsAccount#payload_log}
        :param protocol_detection_enabled: Indicator that protocol detection is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#protocol_detection_enabled TeamsAccount#protocol_detection_enabled}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#proxy TeamsAccount#proxy}
        :param ssh_session_log: ssh_session_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#ssh_session_log TeamsAccount#ssh_session_log}
        :param tls_decrypt_enabled: Indicator that decryption of TLS traffic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls_decrypt_enabled TeamsAccount#tls_decrypt_enabled}
        :param url_browser_isolation_enabled: Safely browse websites in Browser Isolation through a URL. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#url_browser_isolation_enabled TeamsAccount#url_browser_isolation_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eef26928a068969f65502fd07d1b2647d3b494fccba80cfd2689b7d1f33a94b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TeamsAccountConfig(
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
        '''Generates CDKTF code for importing a TeamsAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TeamsAccount to import.
        :param import_from_id: The id of the existing TeamsAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TeamsAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b64d72102b29db49271ca830a051e31e459bc2bd60eb2530603aaf5321d32d8)
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
        notification_settings: typing.Optional[typing.Union["TeamsAccountAntivirusNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled_download_phase: Scan on file download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_download_phase TeamsAccount#enabled_download_phase}
        :param enabled_upload_phase: Scan on file upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_upload_phase TeamsAccount#enabled_upload_phase}
        :param fail_closed: Block requests for files that cannot be scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fail_closed TeamsAccount#fail_closed}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#notification_settings TeamsAccount#notification_settings}
        '''
        value = TeamsAccountAntivirus(
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
        :param background_color: Hex code of block page background color. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#background_color TeamsAccount#background_color}
        :param enabled: Indicator of enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param footer_text: Block page footer text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#footer_text TeamsAccount#footer_text}
        :param header_text: Block page header text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#header_text TeamsAccount#header_text}
        :param logo_path: URL of block page logo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logo_path TeamsAccount#logo_path}
        :param mailto_address: Admin email for users to contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_address TeamsAccount#mailto_address}
        :param mailto_subject: Subject line for emails created from block page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_subject TeamsAccount#mailto_subject}
        :param name: Name of block page configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#name TeamsAccount#name}
        '''
        value = TeamsAccountBlockPage(
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
        :param inspection_mode: Body scanning inspection mode. Available values: ``deep``, ``shallow``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#inspection_mode TeamsAccount#inspection_mode}
        '''
        value = TeamsAccountBodyScanning(inspection_mode=inspection_mode)

        return typing.cast(None, jsii.invoke(self, "putBodyScanning", [value]))

    @jsii.member(jsii_name="putCertificate")
    def put_certificate(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of certificate for TLS interception. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = TeamsAccountCertificate(id=id)

        return typing.cast(None, jsii.invoke(self, "putCertificate", [value]))

    @jsii.member(jsii_name="putCustomCertificate")
    def put_custom_certificate(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether TLS encryption should use a custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param id: ID of custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = TeamsAccountCustomCertificate(enabled=enabled, id=id)

        return typing.cast(None, jsii.invoke(self, "putCustomCertificate", [value]))

    @jsii.member(jsii_name="putExtendedEmailMatching")
    def put_extended_email_matching(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        value = TeamsAccountExtendedEmailMatching(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putExtendedEmailMatching", [value]))

    @jsii.member(jsii_name="putFips")
    def put_fips(
        self,
        *,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param tls: Only allow FIPS-compliant TLS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls TeamsAccount#tls}
        '''
        value = TeamsAccountFips(tls=tls)

        return typing.cast(None, jsii.invoke(self, "putFips", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        settings_by_rule_type: typing.Union["TeamsAccountLoggingSettingsByRuleType", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param redact_pii: Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#redact_pii TeamsAccount#redact_pii}
        :param settings_by_rule_type: settings_by_rule_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#settings_by_rule_type TeamsAccount#settings_by_rule_type}
        '''
        value = TeamsAccountLogging(
            redact_pii=redact_pii, settings_by_rule_type=settings_by_rule_type
        )

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putPayloadLog")
    def put_payload_log(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt matched payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        value = TeamsAccountPayloadLog(public_key=public_key)

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
        :param disable_for_time: Sets the time limit in seconds that a user can use an override code to bypass WARP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#disable_for_time TeamsAccount#disable_for_time}
        :param root_ca: Whether root ca is enabled account wide for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#root_ca TeamsAccount#root_ca}
        :param tcp: Whether gateway proxy is enabled on gateway devices for TCP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tcp TeamsAccount#tcp}
        :param udp: Whether gateway proxy is enabled on gateway devices for UDP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#udp TeamsAccount#udp}
        :param virtual_ip: Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#virtual_ip TeamsAccount#virtual_ip}
        '''
        value = TeamsAccountProxy(
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
        :param public_key: Public key used to encrypt ssh session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        value = TeamsAccountSshSessionLog(public_key=public_key)

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
    def antivirus(self) -> "TeamsAccountAntivirusOutputReference":
        return typing.cast("TeamsAccountAntivirusOutputReference", jsii.get(self, "antivirus"))

    @builtins.property
    @jsii.member(jsii_name="blockPage")
    def block_page(self) -> "TeamsAccountBlockPageOutputReference":
        return typing.cast("TeamsAccountBlockPageOutputReference", jsii.get(self, "blockPage"))

    @builtins.property
    @jsii.member(jsii_name="bodyScanning")
    def body_scanning(self) -> "TeamsAccountBodyScanningOutputReference":
        return typing.cast("TeamsAccountBodyScanningOutputReference", jsii.get(self, "bodyScanning"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> "TeamsAccountCertificateOutputReference":
        return typing.cast("TeamsAccountCertificateOutputReference", jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="customCertificate")
    def custom_certificate(self) -> "TeamsAccountCustomCertificateOutputReference":
        return typing.cast("TeamsAccountCustomCertificateOutputReference", jsii.get(self, "customCertificate"))

    @builtins.property
    @jsii.member(jsii_name="extendedEmailMatching")
    def extended_email_matching(
        self,
    ) -> "TeamsAccountExtendedEmailMatchingOutputReference":
        return typing.cast("TeamsAccountExtendedEmailMatchingOutputReference", jsii.get(self, "extendedEmailMatching"))

    @builtins.property
    @jsii.member(jsii_name="fips")
    def fips(self) -> "TeamsAccountFipsOutputReference":
        return typing.cast("TeamsAccountFipsOutputReference", jsii.get(self, "fips"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "TeamsAccountLoggingOutputReference":
        return typing.cast("TeamsAccountLoggingOutputReference", jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="payloadLog")
    def payload_log(self) -> "TeamsAccountPayloadLogOutputReference":
        return typing.cast("TeamsAccountPayloadLogOutputReference", jsii.get(self, "payloadLog"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "TeamsAccountProxyOutputReference":
        return typing.cast("TeamsAccountProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="sshSessionLog")
    def ssh_session_log(self) -> "TeamsAccountSshSessionLogOutputReference":
        return typing.cast("TeamsAccountSshSessionLogOutputReference", jsii.get(self, "sshSessionLog"))

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
    def antivirus_input(self) -> typing.Optional["TeamsAccountAntivirus"]:
        return typing.cast(typing.Optional["TeamsAccountAntivirus"], jsii.get(self, "antivirusInput"))

    @builtins.property
    @jsii.member(jsii_name="blockPageInput")
    def block_page_input(self) -> typing.Optional["TeamsAccountBlockPage"]:
        return typing.cast(typing.Optional["TeamsAccountBlockPage"], jsii.get(self, "blockPageInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyScanningInput")
    def body_scanning_input(self) -> typing.Optional["TeamsAccountBodyScanning"]:
        return typing.cast(typing.Optional["TeamsAccountBodyScanning"], jsii.get(self, "bodyScanningInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional["TeamsAccountCertificate"]:
        return typing.cast(typing.Optional["TeamsAccountCertificate"], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="customCertificateInput")
    def custom_certificate_input(
        self,
    ) -> typing.Optional["TeamsAccountCustomCertificate"]:
        return typing.cast(typing.Optional["TeamsAccountCustomCertificate"], jsii.get(self, "customCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedEmailMatchingInput")
    def extended_email_matching_input(
        self,
    ) -> typing.Optional["TeamsAccountExtendedEmailMatching"]:
        return typing.cast(typing.Optional["TeamsAccountExtendedEmailMatching"], jsii.get(self, "extendedEmailMatchingInput"))

    @builtins.property
    @jsii.member(jsii_name="fipsInput")
    def fips_input(self) -> typing.Optional["TeamsAccountFips"]:
        return typing.cast(typing.Optional["TeamsAccountFips"], jsii.get(self, "fipsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional["TeamsAccountLogging"]:
        return typing.cast(typing.Optional["TeamsAccountLogging"], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nonIdentityBrowserIsolationEnabledInput")
    def non_identity_browser_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonIdentityBrowserIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadLogInput")
    def payload_log_input(self) -> typing.Optional["TeamsAccountPayloadLog"]:
        return typing.cast(typing.Optional["TeamsAccountPayloadLog"], jsii.get(self, "payloadLogInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolDetectionEnabledInput")
    def protocol_detection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protocolDetectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["TeamsAccountProxy"]:
        return typing.cast(typing.Optional["TeamsAccountProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="sshSessionLogInput")
    def ssh_session_log_input(self) -> typing.Optional["TeamsAccountSshSessionLog"]:
        return typing.cast(typing.Optional["TeamsAccountSshSessionLog"], jsii.get(self, "sshSessionLogInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__efc24d086deedf9517131c4221eee35f5c4e21f0809ff758684023b0bc0dd7e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfe1ff4b0f086dee6cc8d68a7a05750e8e8f6a39c9c2c391291584bc235d0892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activityLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f01cd8b87a4182be3d898cf4b665c4f1f442fd816ce094db3d75311df0b25a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2274640593869a1e023b020a7d52768da9a98e3d1046393d38ce4862e5194aa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__461f92434e89b51d153df092ab18794a4585b3d2fedeb2584efd9bb8df423e5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00f563072e1a5e310cd825a89595e9836d934e0337bc54837f89c6c7f8c3b688)
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
            type_hints = typing.get_type_hints(_typecheckingstub__164de1ae58401ab926682a04998d7110ef293735820b51dd193ae20953df60cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlBrowserIsolationEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountAntivirus",
    jsii_struct_bases=[],
    name_mapping={
        "enabled_download_phase": "enabledDownloadPhase",
        "enabled_upload_phase": "enabledUploadPhase",
        "fail_closed": "failClosed",
        "notification_settings": "notificationSettings",
    },
)
class TeamsAccountAntivirus:
    def __init__(
        self,
        *,
        enabled_download_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled_upload_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        fail_closed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        notification_settings: typing.Optional[typing.Union["TeamsAccountAntivirusNotificationSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled_download_phase: Scan on file download. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_download_phase TeamsAccount#enabled_download_phase}
        :param enabled_upload_phase: Scan on file upload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_upload_phase TeamsAccount#enabled_upload_phase}
        :param fail_closed: Block requests for files that cannot be scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fail_closed TeamsAccount#fail_closed}
        :param notification_settings: notification_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#notification_settings TeamsAccount#notification_settings}
        '''
        if isinstance(notification_settings, dict):
            notification_settings = TeamsAccountAntivirusNotificationSettings(**notification_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6703f255bd303f508704a42376dc3deca453ae1e45a046cca3a88da3fce48)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_download_phase TeamsAccount#enabled_download_phase}
        '''
        result = self._values.get("enabled_download_phase")
        assert result is not None, "Required property 'enabled_download_phase' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def enabled_upload_phase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Scan on file upload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled_upload_phase TeamsAccount#enabled_upload_phase}
        '''
        result = self._values.get("enabled_upload_phase")
        assert result is not None, "Required property 'enabled_upload_phase' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def fail_closed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Block requests for files that cannot be scanned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fail_closed TeamsAccount#fail_closed}
        '''
        result = self._values.get("fail_closed")
        assert result is not None, "Required property 'fail_closed' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def notification_settings(
        self,
    ) -> typing.Optional["TeamsAccountAntivirusNotificationSettings"]:
        '''notification_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#notification_settings TeamsAccount#notification_settings}
        '''
        result = self._values.get("notification_settings")
        return typing.cast(typing.Optional["TeamsAccountAntivirusNotificationSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountAntivirus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountAntivirusNotificationSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "message": "message",
        "support_url": "supportUrl",
    },
)
class TeamsAccountAntivirusNotificationSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#message TeamsAccount#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#support_url TeamsAccount#support_url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe76ee86d94aaabc04add39fe7141c7c3c6d518bbe3584ac06e7eb2d433f796)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Notification content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#message TeamsAccount#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''Support URL to show in the notification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#support_url TeamsAccount#support_url}
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountAntivirusNotificationSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountAntivirusNotificationSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountAntivirusNotificationSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc868dd5be9700f7c36ea7ec51955968f99f4103c152a076d98361c29d6b3357)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c9772347973f45f2f2343cbf5aa9f419bc00a635b96facda43af41f116cebea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa727bf8a6338185c7cd92d7dc9bebe0b37c0214b4666176996002caa9d0721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b332388db739038b83e677a500e3ab7a8c8f958164ee9ce65da15286ed0bc1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TeamsAccountAntivirusNotificationSettings]:
        return typing.cast(typing.Optional[TeamsAccountAntivirusNotificationSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountAntivirusNotificationSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea093a55867ec506e6de020b597a7eb54af25e08e5f664a17a9f536424a63189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsAccountAntivirusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountAntivirusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ed742aaca36fa69c267fd1febe2c6c25f0f6e17ae95532eddfa23c2a437baec)
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
        :param enabled: Enable notification settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param message: Notification content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#message TeamsAccount#message}
        :param support_url: Support URL to show in the notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#support_url TeamsAccount#support_url}
        '''
        value = TeamsAccountAntivirusNotificationSettings(
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
    ) -> TeamsAccountAntivirusNotificationSettingsOutputReference:
        return typing.cast(TeamsAccountAntivirusNotificationSettingsOutputReference, jsii.get(self, "notificationSettings"))

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
    ) -> typing.Optional[TeamsAccountAntivirusNotificationSettings]:
        return typing.cast(typing.Optional[TeamsAccountAntivirusNotificationSettings], jsii.get(self, "notificationSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__85e3c263a84a30585c736b4e799cb93f0e538630a5125a5f5b626b333f27e7ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c8daddfac5caee701ea289f7040f6f53c1bba64cb2baa621277bd5a94a5e11c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__527d83d1b2d221667ef3d87465698ebda0c422bea790191e84787890ca7a3ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failClosed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountAntivirus]:
        return typing.cast(typing.Optional[TeamsAccountAntivirus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountAntivirus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9a4ff69ef114e0881c85964c2c9b10d568e6755ff69543fc4106b1940b2da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountBlockPage",
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
class TeamsAccountBlockPage:
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
        :param background_color: Hex code of block page background color. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#background_color TeamsAccount#background_color}
        :param enabled: Indicator of enablement. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param footer_text: Block page footer text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#footer_text TeamsAccount#footer_text}
        :param header_text: Block page header text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#header_text TeamsAccount#header_text}
        :param logo_path: URL of block page logo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logo_path TeamsAccount#logo_path}
        :param mailto_address: Admin email for users to contact. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_address TeamsAccount#mailto_address}
        :param mailto_subject: Subject line for emails created from block page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_subject TeamsAccount#mailto_subject}
        :param name: Name of block page configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#name TeamsAccount#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36255eaa79cd0c9aa2c292c491f09f94b6b62a097cac76af03244c4f97c98ff3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#background_color TeamsAccount#background_color}
        '''
        result = self._values.get("background_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator of enablement.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def footer_text(self) -> typing.Optional[builtins.str]:
        '''Block page footer text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#footer_text TeamsAccount#footer_text}
        '''
        result = self._values.get("footer_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header_text(self) -> typing.Optional[builtins.str]:
        '''Block page header text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#header_text TeamsAccount#header_text}
        '''
        result = self._values.get("header_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logo_path(self) -> typing.Optional[builtins.str]:
        '''URL of block page logo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logo_path TeamsAccount#logo_path}
        '''
        result = self._values.get("logo_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailto_address(self) -> typing.Optional[builtins.str]:
        '''Admin email for users to contact.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_address TeamsAccount#mailto_address}
        '''
        result = self._values.get("mailto_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mailto_subject(self) -> typing.Optional[builtins.str]:
        '''Subject line for emails created from block page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#mailto_subject TeamsAccount#mailto_subject}
        '''
        result = self._values.get("mailto_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of block page configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#name TeamsAccount#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountBlockPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountBlockPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountBlockPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__527b3b1c1eb56df08a4c73b760fc6669597697f095e315d6cbfe33541df4b7db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dfe624729e9f485a04a12da9659f35c62dd59b84b3a1867ff2c3f98838f1123)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f700efb75ee1dbad76190ac693694d9492e7ebc44de0e005de957887ed207b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="footerText")
    def footer_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "footerText"))

    @footer_text.setter
    def footer_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366e2187ef7f0edc04bfd245ba59b669756f27b28433e0600821bd75ef2959a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "footerText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerText")
    def header_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerText"))

    @header_text.setter
    def header_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3289acb6be17ca216f6ed11d894eb0231fc493c11ce29b3724ed2084a6f3ac98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerText", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoPath")
    def logo_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoPath"))

    @logo_path.setter
    def logo_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c331426fe27038dd965dd3bd7dbf000e4ead221545c30d76afd7e0abed9c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailtoAddress")
    def mailto_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailtoAddress"))

    @mailto_address.setter
    def mailto_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a61a160ee6f4682519fc3dd853f39e6d9c44445f33acce29de305bf14cb4bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailtoAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mailtoSubject")
    def mailto_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailtoSubject"))

    @mailto_subject.setter
    def mailto_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2571f0683fedccc81de76824d4bdbce2d74b53b0eaca30ecb2c4c098509c383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailtoSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96641c03b96e60cefe86f46cf4a5850784324a649d39b057ca606f9ee9adc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountBlockPage]:
        return typing.cast(typing.Optional[TeamsAccountBlockPage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountBlockPage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbfec8662f6f3cb5842d30deff2af7d3674fe4c2b0d4c2dadccf362640a5d0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountBodyScanning",
    jsii_struct_bases=[],
    name_mapping={"inspection_mode": "inspectionMode"},
)
class TeamsAccountBodyScanning:
    def __init__(self, *, inspection_mode: builtins.str) -> None:
        '''
        :param inspection_mode: Body scanning inspection mode. Available values: ``deep``, ``shallow``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#inspection_mode TeamsAccount#inspection_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694a0f7b8cecea20c622def5a29cbf666e99e6dd97e60dc8da1d613c81e9bf3b)
            check_type(argname="argument inspection_mode", value=inspection_mode, expected_type=type_hints["inspection_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inspection_mode": inspection_mode,
        }

    @builtins.property
    def inspection_mode(self) -> builtins.str:
        '''Body scanning inspection mode. Available values: ``deep``, ``shallow``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#inspection_mode TeamsAccount#inspection_mode}
        '''
        result = self._values.get("inspection_mode")
        assert result is not None, "Required property 'inspection_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountBodyScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountBodyScanningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountBodyScanningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77a5be02a06b510e140a0d18490a5744c7d85b15104450fa4d29e9df8e3c5f43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__786acfd89e0c3cc10fb514dd583e53d24fc6421954a9c640dbadd8ddce1d1435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountBodyScanning]:
        return typing.cast(typing.Optional[TeamsAccountBodyScanning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountBodyScanning]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70e6840555697f62974fdab59429fc88dbd9561f8a2886a94b976d21a00990f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountCertificate",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class TeamsAccountCertificate:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of certificate for TLS interception. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f6580e545ac36ccc86425127bfb8aa1043e714d477d6eee28efd3b2f1e99fa)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of certificate for TLS interception.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id}

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
        return "TeamsAccountCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab819599626377dbc171f533cd077acb14d2381864ee8776b531763ab083a465)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eff3ce2d57e376f336bfc7cbe8f559ebb7a38ab158059562c9639b3121bb409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountCertificate]:
        return typing.cast(typing.Optional[TeamsAccountCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountCertificate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0155b2eacb1496f5c0cbfd47a90ee2f167a08b9ca5119d6f013bfc89bfc2284d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountConfig",
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
class TeamsAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        antivirus: typing.Optional[typing.Union[TeamsAccountAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
        block_page: typing.Optional[typing.Union[TeamsAccountBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
        body_scanning: typing.Optional[typing.Union[TeamsAccountBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Union[TeamsAccountCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_certificate: typing.Optional[typing.Union["TeamsAccountCustomCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_email_matching: typing.Optional[typing.Union["TeamsAccountExtendedEmailMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        fips: typing.Optional[typing.Union["TeamsAccountFips", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["TeamsAccountLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        payload_log: typing.Optional[typing.Union["TeamsAccountPayloadLog", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proxy: typing.Optional[typing.Union["TeamsAccountProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_session_log: typing.Optional[typing.Union["TeamsAccountSshSessionLog", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#account_id TeamsAccount#account_id}
        :param activity_log_enabled: Whether to enable the activity log. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#activity_log_enabled TeamsAccount#activity_log_enabled}
        :param antivirus: antivirus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#antivirus TeamsAccount#antivirus}
        :param block_page: block_page block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#block_page TeamsAccount#block_page}
        :param body_scanning: body_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#body_scanning TeamsAccount#body_scanning}
        :param certificate: certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#certificate TeamsAccount#certificate}
        :param custom_certificate: custom_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#custom_certificate TeamsAccount#custom_certificate}
        :param extended_email_matching: extended_email_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#extended_email_matching TeamsAccount#extended_email_matching}
        :param fips: fips block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fips TeamsAccount#fips}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logging TeamsAccount#logging}
        :param non_identity_browser_isolation_enabled: Enable non-identity onramp for Browser Isolation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#non_identity_browser_isolation_enabled TeamsAccount#non_identity_browser_isolation_enabled}
        :param payload_log: payload_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#payload_log TeamsAccount#payload_log}
        :param protocol_detection_enabled: Indicator that protocol detection is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#protocol_detection_enabled TeamsAccount#protocol_detection_enabled}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#proxy TeamsAccount#proxy}
        :param ssh_session_log: ssh_session_log block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#ssh_session_log TeamsAccount#ssh_session_log}
        :param tls_decrypt_enabled: Indicator that decryption of TLS traffic is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls_decrypt_enabled TeamsAccount#tls_decrypt_enabled}
        :param url_browser_isolation_enabled: Safely browse websites in Browser Isolation through a URL. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#url_browser_isolation_enabled TeamsAccount#url_browser_isolation_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(antivirus, dict):
            antivirus = TeamsAccountAntivirus(**antivirus)
        if isinstance(block_page, dict):
            block_page = TeamsAccountBlockPage(**block_page)
        if isinstance(body_scanning, dict):
            body_scanning = TeamsAccountBodyScanning(**body_scanning)
        if isinstance(certificate, dict):
            certificate = TeamsAccountCertificate(**certificate)
        if isinstance(custom_certificate, dict):
            custom_certificate = TeamsAccountCustomCertificate(**custom_certificate)
        if isinstance(extended_email_matching, dict):
            extended_email_matching = TeamsAccountExtendedEmailMatching(**extended_email_matching)
        if isinstance(fips, dict):
            fips = TeamsAccountFips(**fips)
        if isinstance(logging, dict):
            logging = TeamsAccountLogging(**logging)
        if isinstance(payload_log, dict):
            payload_log = TeamsAccountPayloadLog(**payload_log)
        if isinstance(proxy, dict):
            proxy = TeamsAccountProxy(**proxy)
        if isinstance(ssh_session_log, dict):
            ssh_session_log = TeamsAccountSshSessionLog(**ssh_session_log)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9d9533e41d2295fc2ee51cc4d9cd2e8469c56522fd3bc9b7fc09c081ee7753)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#account_id TeamsAccount#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activity_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable the activity log.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#activity_log_enabled TeamsAccount#activity_log_enabled}
        '''
        result = self._values.get("activity_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def antivirus(self) -> typing.Optional[TeamsAccountAntivirus]:
        '''antivirus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#antivirus TeamsAccount#antivirus}
        '''
        result = self._values.get("antivirus")
        return typing.cast(typing.Optional[TeamsAccountAntivirus], result)

    @builtins.property
    def block_page(self) -> typing.Optional[TeamsAccountBlockPage]:
        '''block_page block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#block_page TeamsAccount#block_page}
        '''
        result = self._values.get("block_page")
        return typing.cast(typing.Optional[TeamsAccountBlockPage], result)

    @builtins.property
    def body_scanning(self) -> typing.Optional[TeamsAccountBodyScanning]:
        '''body_scanning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#body_scanning TeamsAccount#body_scanning}
        '''
        result = self._values.get("body_scanning")
        return typing.cast(typing.Optional[TeamsAccountBodyScanning], result)

    @builtins.property
    def certificate(self) -> typing.Optional[TeamsAccountCertificate]:
        '''certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#certificate TeamsAccount#certificate}
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[TeamsAccountCertificate], result)

    @builtins.property
    def custom_certificate(self) -> typing.Optional["TeamsAccountCustomCertificate"]:
        '''custom_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#custom_certificate TeamsAccount#custom_certificate}
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional["TeamsAccountCustomCertificate"], result)

    @builtins.property
    def extended_email_matching(
        self,
    ) -> typing.Optional["TeamsAccountExtendedEmailMatching"]:
        '''extended_email_matching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#extended_email_matching TeamsAccount#extended_email_matching}
        '''
        result = self._values.get("extended_email_matching")
        return typing.cast(typing.Optional["TeamsAccountExtendedEmailMatching"], result)

    @builtins.property
    def fips(self) -> typing.Optional["TeamsAccountFips"]:
        '''fips block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#fips TeamsAccount#fips}
        '''
        result = self._values.get("fips")
        return typing.cast(typing.Optional["TeamsAccountFips"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(self) -> typing.Optional["TeamsAccountLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#logging TeamsAccount#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["TeamsAccountLogging"], result)

    @builtins.property
    def non_identity_browser_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable non-identity onramp for Browser Isolation. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#non_identity_browser_isolation_enabled TeamsAccount#non_identity_browser_isolation_enabled}
        '''
        result = self._values.get("non_identity_browser_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def payload_log(self) -> typing.Optional["TeamsAccountPayloadLog"]:
        '''payload_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#payload_log TeamsAccount#payload_log}
        '''
        result = self._values.get("payload_log")
        return typing.cast(typing.Optional["TeamsAccountPayloadLog"], result)

    @builtins.property
    def protocol_detection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that protocol detection is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#protocol_detection_enabled TeamsAccount#protocol_detection_enabled}
        '''
        result = self._values.get("protocol_detection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proxy(self) -> typing.Optional["TeamsAccountProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#proxy TeamsAccount#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["TeamsAccountProxy"], result)

    @builtins.property
    def ssh_session_log(self) -> typing.Optional["TeamsAccountSshSessionLog"]:
        '''ssh_session_log block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#ssh_session_log TeamsAccount#ssh_session_log}
        '''
        result = self._values.get("ssh_session_log")
        return typing.cast(typing.Optional["TeamsAccountSshSessionLog"], result)

    @builtins.property
    def tls_decrypt_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that decryption of TLS traffic is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls_decrypt_enabled TeamsAccount#tls_decrypt_enabled}
        '''
        result = self._values.get("tls_decrypt_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def url_browser_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Safely browse websites in Browser Isolation through a URL. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#url_browser_isolation_enabled TeamsAccount#url_browser_isolation_enabled}
        '''
        result = self._values.get("url_browser_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountCustomCertificate",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "id": "id"},
)
class TeamsAccountCustomCertificate:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Whether TLS encryption should use a custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        :param id: ID of custom certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd5755a5f479ae45faa6deab233688d5d1325c0ba66d182cf6cdc4a9b8550f5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of custom certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#id TeamsAccount#id}

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
        return "TeamsAccountCustomCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountCustomCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountCustomCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d8ba0ba359724a07e43e37891f4875f86d6d289e0c676b18044dfeb004afa5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba91b45882b4408fe4fa1a405f9388f1534ebce1579705239ce7765695c5bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cdbdce8ebed3219c8c8f88614360559c9c272e68c8942e2ff8c019b0741b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountCustomCertificate]:
        return typing.cast(typing.Optional[TeamsAccountCustomCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountCustomCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faad44e29eff99d6380be1cc6286fc523a7e2614a972db6072f38e1231ba3a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountExtendedEmailMatching",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class TeamsAccountExtendedEmailMatching:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3656bc7b3b78a14de7513b725682635cda9c9ab7e7552d2a4caba49a1438c5f7)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether e-mails should be matched on all variants of user emails (with + or . modifiers) in Firewall policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#enabled TeamsAccount#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountExtendedEmailMatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountExtendedEmailMatchingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountExtendedEmailMatchingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__787be82cf99a0c0fc0f1f7046dff01d855154bfb31250be06d6d8d1b1014f293)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1292a5e0be3e5173b3489f8a00beecfdf4f8fdbb14897aed001f1fea71478800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountExtendedEmailMatching]:
        return typing.cast(typing.Optional[TeamsAccountExtendedEmailMatching], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountExtendedEmailMatching],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8855283eebe0e9369cdd3ed3a979067af4e16c38f30999daadd10fdb68cda012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountFips",
    jsii_struct_bases=[],
    name_mapping={"tls": "tls"},
)
class TeamsAccountFips:
    def __init__(
        self,
        *,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param tls: Only allow FIPS-compliant TLS configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls TeamsAccount#tls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194a120d72438dcb19ad861bd1fc450aa12124342200c24b86511a23af3fd457)
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow FIPS-compliant TLS configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tls TeamsAccount#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountFips(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountFipsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountFipsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66f4b9e4947214368b09aa52b1f7632b3d60932728293f4a623033d2c3a8e99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae2bf2eacae78234abea4a267a5aece6e02fd89286d4b855b2263592ae2ca2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountFips]:
        return typing.cast(typing.Optional[TeamsAccountFips], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountFips]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d18a1c9fd73bf34f435dcbe4bb8ce8112d78774a7eee838c72823cd886f4b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLogging",
    jsii_struct_bases=[],
    name_mapping={
        "redact_pii": "redactPii",
        "settings_by_rule_type": "settingsByRuleType",
    },
)
class TeamsAccountLogging:
    def __init__(
        self,
        *,
        redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        settings_by_rule_type: typing.Union["TeamsAccountLoggingSettingsByRuleType", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param redact_pii: Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#redact_pii TeamsAccount#redact_pii}
        :param settings_by_rule_type: settings_by_rule_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#settings_by_rule_type TeamsAccount#settings_by_rule_type}
        '''
        if isinstance(settings_by_rule_type, dict):
            settings_by_rule_type = TeamsAccountLoggingSettingsByRuleType(**settings_by_rule_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82e1585f1d1d8ce068bd33de4dfd4bcb64fb90a4a05d226bc744d7e3d8aa4de8)
            check_type(argname="argument redact_pii", value=redact_pii, expected_type=type_hints["redact_pii"])
            check_type(argname="argument settings_by_rule_type", value=settings_by_rule_type, expected_type=type_hints["settings_by_rule_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "redact_pii": redact_pii,
            "settings_by_rule_type": settings_by_rule_type,
        }

    @builtins.property
    def redact_pii(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Redact personally identifiable information from activity logging (PII fields are: source IP, user email, user ID, device ID, URL, referrer, user agent).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#redact_pii TeamsAccount#redact_pii}
        '''
        result = self._values.get("redact_pii")
        assert result is not None, "Required property 'redact_pii' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def settings_by_rule_type(self) -> "TeamsAccountLoggingSettingsByRuleType":
        '''settings_by_rule_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#settings_by_rule_type TeamsAccount#settings_by_rule_type}
        '''
        result = self._values.get("settings_by_rule_type")
        assert result is not None, "Required property 'settings_by_rule_type' is missing"
        return typing.cast("TeamsAccountLoggingSettingsByRuleType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2361d44ddf69303acaf0b0cfae766852d324bb007e810d4a24fe0ef3ca64353e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettingsByRuleType")
    def put_settings_by_rule_type(
        self,
        *,
        dns: typing.Union["TeamsAccountLoggingSettingsByRuleTypeDns", typing.Dict[builtins.str, typing.Any]],
        http: typing.Union["TeamsAccountLoggingSettingsByRuleTypeHttp", typing.Dict[builtins.str, typing.Any]],
        l4: typing.Union["TeamsAccountLoggingSettingsByRuleTypeL4", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#dns TeamsAccount#dns}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#http TeamsAccount#http}
        :param l4: l4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#l4 TeamsAccount#l4}
        '''
        value = TeamsAccountLoggingSettingsByRuleType(dns=dns, http=http, l4=l4)

        return typing.cast(None, jsii.invoke(self, "putSettingsByRuleType", [value]))

    @builtins.property
    @jsii.member(jsii_name="settingsByRuleType")
    def settings_by_rule_type(
        self,
    ) -> "TeamsAccountLoggingSettingsByRuleTypeOutputReference":
        return typing.cast("TeamsAccountLoggingSettingsByRuleTypeOutputReference", jsii.get(self, "settingsByRuleType"))

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
    ) -> typing.Optional["TeamsAccountLoggingSettingsByRuleType"]:
        return typing.cast(typing.Optional["TeamsAccountLoggingSettingsByRuleType"], jsii.get(self, "settingsByRuleTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__352057726bbcc94a88b3ab95451f4a553f15888d0aa4f076eb98f19b02d19759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redactPii", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountLogging]:
        return typing.cast(typing.Optional[TeamsAccountLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountLogging]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d01240fd4f8e59c7b8a04779defaf1585d6f92afe1c6c9a2ec4decf9728c529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleType",
    jsii_struct_bases=[],
    name_mapping={"dns": "dns", "http": "http", "l4": "l4"},
)
class TeamsAccountLoggingSettingsByRuleType:
    def __init__(
        self,
        *,
        dns: typing.Union["TeamsAccountLoggingSettingsByRuleTypeDns", typing.Dict[builtins.str, typing.Any]],
        http: typing.Union["TeamsAccountLoggingSettingsByRuleTypeHttp", typing.Dict[builtins.str, typing.Any]],
        l4: typing.Union["TeamsAccountLoggingSettingsByRuleTypeL4", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#dns TeamsAccount#dns}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#http TeamsAccount#http}
        :param l4: l4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#l4 TeamsAccount#l4}
        '''
        if isinstance(dns, dict):
            dns = TeamsAccountLoggingSettingsByRuleTypeDns(**dns)
        if isinstance(http, dict):
            http = TeamsAccountLoggingSettingsByRuleTypeHttp(**http)
        if isinstance(l4, dict):
            l4 = TeamsAccountLoggingSettingsByRuleTypeL4(**l4)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a906a38baee581243411daf966a7a6ed57a09027e62aa06e9ffc72338455c3)
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument l4", value=l4, expected_type=type_hints["l4"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns": dns,
            "http": http,
            "l4": l4,
        }

    @builtins.property
    def dns(self) -> "TeamsAccountLoggingSettingsByRuleTypeDns":
        '''dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#dns TeamsAccount#dns}
        '''
        result = self._values.get("dns")
        assert result is not None, "Required property 'dns' is missing"
        return typing.cast("TeamsAccountLoggingSettingsByRuleTypeDns", result)

    @builtins.property
    def http(self) -> "TeamsAccountLoggingSettingsByRuleTypeHttp":
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#http TeamsAccount#http}
        '''
        result = self._values.get("http")
        assert result is not None, "Required property 'http' is missing"
        return typing.cast("TeamsAccountLoggingSettingsByRuleTypeHttp", result)

    @builtins.property
    def l4(self) -> "TeamsAccountLoggingSettingsByRuleTypeL4":
        '''l4 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#l4 TeamsAccount#l4}
        '''
        result = self._values.get("l4")
        assert result is not None, "Required property 'l4' is missing"
        return typing.cast("TeamsAccountLoggingSettingsByRuleTypeL4", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountLoggingSettingsByRuleType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeDns",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class TeamsAccountLoggingSettingsByRuleTypeDns:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2261f9133cee44c3be7f221cd466098ce7c06e05e2a1179bc0ff72c1f09924)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountLoggingSettingsByRuleTypeDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountLoggingSettingsByRuleTypeDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e595a9d9bc4afe14b3353bc64bafba64d8d649b8753f9c4a9e3565149780fca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df76a521476aedd34d191c96db2eac11ebfb9e74b12c090e12e501a330910fb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e0575668b8b6c28825246a31b4bebf69904772e1e2b0c316717d5190b60c5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7030a5895b50bea580e5bed4706639ed08df12be1a2e16e51e147493475219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeHttp",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class TeamsAccountLoggingSettingsByRuleTypeHttp:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f927924d537a73be3142b2e42d527dde53856638f01f670b9ca5d818c32f2d)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountLoggingSettingsByRuleTypeHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountLoggingSettingsByRuleTypeHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ae1c9d5a8470fcb892e78f146523524eb343dfe67371eb6ee2545e7603585e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fede7b7c62295c379c2609fd0e684ba8b75f612def82fd5ab004efdffc0f7db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c73b3051b9ba4b705bb68e8ad0fc557f7221a9808e0e44a434a8448c7e5a5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d90c25706203adc21e970bf8345409e215891420941ac324abbe3598a5d9f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeL4",
    jsii_struct_bases=[],
    name_mapping={"log_all": "logAll", "log_blocks": "logBlocks"},
)
class TeamsAccountLoggingSettingsByRuleTypeL4:
    def __init__(
        self,
        *,
        log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb9d485773317a46ffafc4a3bf4bae6a239d426bf8dbc57c0bcdbab7c11a62d)
            check_type(argname="argument log_all", value=log_all, expected_type=type_hints["log_all"])
            check_type(argname="argument log_blocks", value=log_blocks, expected_type=type_hints["log_blocks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_all": log_all,
            "log_blocks": log_blocks,
        }

    @builtins.property
    def log_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to log all activity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        '''
        result = self._values.get("log_all")
        assert result is not None, "Required property 'log_all' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_blocks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.'''
        result = self._values.get("log_blocks")
        assert result is not None, "Required property 'log_blocks' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountLoggingSettingsByRuleTypeL4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountLoggingSettingsByRuleTypeL4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeL4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbcdf5fa233715c421247a39fd188d2608f0197d334784fe1fb915d4798f0342)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b5522950ffb7bf4b126d758d7089183e35e7fd5824fd1189e95bfb674cc9109)
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
            type_hints = typing.get_type_hints(_typecheckingstub__138cd8a230a5c04e9eb91e037fbd8b672c26671daed96b2264dd06793dc1e14d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c56bf29763536211148d9c473c07137a269a035f0fe6e37b57c6029b1f71a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsAccountLoggingSettingsByRuleTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountLoggingSettingsByRuleTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78fd824a76e5042dec4b27841b5748002becaa9edd7a8a1800b1c3f3dae9a0cb)
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
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        value = TeamsAccountLoggingSettingsByRuleTypeDns(
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
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        value = TeamsAccountLoggingSettingsByRuleTypeHttp(
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
        :param log_all: Whether to log all activity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_all TeamsAccount#log_all}
        :param log_blocks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#log_blocks TeamsAccount#log_blocks}.
        '''
        value = TeamsAccountLoggingSettingsByRuleTypeL4(
            log_all=log_all, log_blocks=log_blocks
        )

        return typing.cast(None, jsii.invoke(self, "putL4", [value]))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> TeamsAccountLoggingSettingsByRuleTypeDnsOutputReference:
        return typing.cast(TeamsAccountLoggingSettingsByRuleTypeDnsOutputReference, jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> TeamsAccountLoggingSettingsByRuleTypeHttpOutputReference:
        return typing.cast(TeamsAccountLoggingSettingsByRuleTypeHttpOutputReference, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="l4")
    def l4(self) -> TeamsAccountLoggingSettingsByRuleTypeL4OutputReference:
        return typing.cast(TeamsAccountLoggingSettingsByRuleTypeL4OutputReference, jsii.get(self, "l4"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(self) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="l4Input")
    def l4_input(self) -> typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4], jsii.get(self, "l4Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountLoggingSettingsByRuleType]:
        return typing.cast(typing.Optional[TeamsAccountLoggingSettingsByRuleType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsAccountLoggingSettingsByRuleType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f89b1df9fb4f146cf11f0eb7c81aa5925c3035dbee50dad8583d3c275032ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountPayloadLog",
    jsii_struct_bases=[],
    name_mapping={"public_key": "publicKey"},
)
class TeamsAccountPayloadLog:
    def __init__(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt matched payloads. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad17fc527fc6d611dac35a9a445fabc5ada9c9d7364d19f31d53b48e0649404f)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
        }

    @builtins.property
    def public_key(self) -> builtins.str:
        '''Public key used to encrypt matched payloads.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountPayloadLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountPayloadLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountPayloadLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5264cf32b3b3c1d493f080323c26fa914a6dbc41f4efe22849d74ed3aaea523c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__589c28b280e41b46ed9c76484eda9e50bfd2805022ac5b3b58e42b1d63de6f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountPayloadLog]:
        return typing.cast(typing.Optional[TeamsAccountPayloadLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountPayloadLog]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b6187f6abab2cb755e733261a1ee98d8604a4b85c57f9915aadae98ce22d21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountProxy",
    jsii_struct_bases=[],
    name_mapping={
        "disable_for_time": "disableForTime",
        "root_ca": "rootCa",
        "tcp": "tcp",
        "udp": "udp",
        "virtual_ip": "virtualIp",
    },
)
class TeamsAccountProxy:
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
        :param disable_for_time: Sets the time limit in seconds that a user can use an override code to bypass WARP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#disable_for_time TeamsAccount#disable_for_time}
        :param root_ca: Whether root ca is enabled account wide for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#root_ca TeamsAccount#root_ca}
        :param tcp: Whether gateway proxy is enabled on gateway devices for TCP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tcp TeamsAccount#tcp}
        :param udp: Whether gateway proxy is enabled on gateway devices for UDP traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#udp TeamsAccount#udp}
        :param virtual_ip: Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#virtual_ip TeamsAccount#virtual_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130801578f58eaff857521cd311a5d3d1ea77bec955b8c1ee439bf2b07c3dbfd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#disable_for_time TeamsAccount#disable_for_time}
        '''
        result = self._values.get("disable_for_time")
        assert result is not None, "Required property 'disable_for_time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def root_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether root ca is enabled account wide for ZT clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#root_ca TeamsAccount#root_ca}
        '''
        result = self._values.get("root_ca")
        assert result is not None, "Required property 'root_ca' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def tcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether gateway proxy is enabled on gateway devices for TCP traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#tcp TeamsAccount#tcp}
        '''
        result = self._values.get("tcp")
        assert result is not None, "Required property 'tcp' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def udp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether gateway proxy is enabled on gateway devices for UDP traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#udp TeamsAccount#udp}
        '''
        result = self._values.get("udp")
        assert result is not None, "Required property 'udp' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def virtual_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether virtual IP (CGNAT) is enabled account wide and will override existing local interface IP for ZT clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#virtual_ip TeamsAccount#virtual_ip}
        '''
        result = self._values.get("virtual_ip")
        assert result is not None, "Required property 'virtual_ip' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea760050892ffb637c567ca5e08b971812de7bea23e06a459c17bd72844f346)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d242c651d7ba888401e80ed8a2a2e7418d6888f387ded126dfdc3e40bc57e2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79def2d13ba589a840713d74c071c681e839c738d696e757eff1648bb7b50b19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb89969ba7a56e902d4e49ee207d5ae0f68784cf24d1cf29b21e2c5d32909579)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34e4bc9e10de540d7442b87808ef3ac22f6d24a31449a9bedf3a70757e872fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18aade8824dff1fbcd0f7f4aec68a85b41e645a0d4f841cab704cf1a1a1d37c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountProxy]:
        return typing.cast(typing.Optional[TeamsAccountProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountProxy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6102917a023774c6605540ab2a06e5cc703ed5e06be953b3558f6112feaf9388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountSshSessionLog",
    jsii_struct_bases=[],
    name_mapping={"public_key": "publicKey"},
)
class TeamsAccountSshSessionLog:
    def __init__(self, *, public_key: builtins.str) -> None:
        '''
        :param public_key: Public key used to encrypt ssh session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1414a306fa01121aeda7c16c2028731d9400230a604b81b758813713255fe943)
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key": public_key,
        }

    @builtins.property
    def public_key(self) -> builtins.str:
        '''Public key used to encrypt ssh session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/teams_account#public_key TeamsAccount#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsAccountSshSessionLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsAccountSshSessionLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsAccount.TeamsAccountSshSessionLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c5b869614c3c21e821c08f9a0779ae14b53df25426b61900b0cc0e158f1d483)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cff0eed37fd4c595a25f3af8f8718ffe483f1dc13f1e3ceeac690ef1132405d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsAccountSshSessionLog]:
        return typing.cast(typing.Optional[TeamsAccountSshSessionLog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsAccountSshSessionLog]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccb2192299f7979ea643fb755a27abcc4a2f42ed6fddd4ec461a021920912d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TeamsAccount",
    "TeamsAccountAntivirus",
    "TeamsAccountAntivirusNotificationSettings",
    "TeamsAccountAntivirusNotificationSettingsOutputReference",
    "TeamsAccountAntivirusOutputReference",
    "TeamsAccountBlockPage",
    "TeamsAccountBlockPageOutputReference",
    "TeamsAccountBodyScanning",
    "TeamsAccountBodyScanningOutputReference",
    "TeamsAccountCertificate",
    "TeamsAccountCertificateOutputReference",
    "TeamsAccountConfig",
    "TeamsAccountCustomCertificate",
    "TeamsAccountCustomCertificateOutputReference",
    "TeamsAccountExtendedEmailMatching",
    "TeamsAccountExtendedEmailMatchingOutputReference",
    "TeamsAccountFips",
    "TeamsAccountFipsOutputReference",
    "TeamsAccountLogging",
    "TeamsAccountLoggingOutputReference",
    "TeamsAccountLoggingSettingsByRuleType",
    "TeamsAccountLoggingSettingsByRuleTypeDns",
    "TeamsAccountLoggingSettingsByRuleTypeDnsOutputReference",
    "TeamsAccountLoggingSettingsByRuleTypeHttp",
    "TeamsAccountLoggingSettingsByRuleTypeHttpOutputReference",
    "TeamsAccountLoggingSettingsByRuleTypeL4",
    "TeamsAccountLoggingSettingsByRuleTypeL4OutputReference",
    "TeamsAccountLoggingSettingsByRuleTypeOutputReference",
    "TeamsAccountPayloadLog",
    "TeamsAccountPayloadLogOutputReference",
    "TeamsAccountProxy",
    "TeamsAccountProxyOutputReference",
    "TeamsAccountSshSessionLog",
    "TeamsAccountSshSessionLogOutputReference",
]

publication.publish()

def _typecheckingstub__7eef26928a068969f65502fd07d1b2647d3b494fccba80cfd2689b7d1f33a94b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    activity_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    antivirus: typing.Optional[typing.Union[TeamsAccountAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page: typing.Optional[typing.Union[TeamsAccountBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    body_scanning: typing.Optional[typing.Union[TeamsAccountBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[TeamsAccountCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_certificate: typing.Optional[typing.Union[TeamsAccountCustomCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_email_matching: typing.Optional[typing.Union[TeamsAccountExtendedEmailMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    fips: typing.Optional[typing.Union[TeamsAccountFips, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[TeamsAccountLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    payload_log: typing.Optional[typing.Union[TeamsAccountPayloadLog, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy: typing.Optional[typing.Union[TeamsAccountProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_session_log: typing.Optional[typing.Union[TeamsAccountSshSessionLog, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5b64d72102b29db49271ca830a051e31e459bc2bd60eb2530603aaf5321d32d8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc24d086deedf9517131c4221eee35f5c4e21f0809ff758684023b0bc0dd7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe1ff4b0f086dee6cc8d68a7a05750e8e8f6a39c9c2c391291584bc235d0892(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f01cd8b87a4182be3d898cf4b665c4f1f442fd816ce094db3d75311df0b25a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2274640593869a1e023b020a7d52768da9a98e3d1046393d38ce4862e5194aa8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461f92434e89b51d153df092ab18794a4585b3d2fedeb2584efd9bb8df423e5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f563072e1a5e310cd825a89595e9836d934e0337bc54837f89c6c7f8c3b688(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164de1ae58401ab926682a04998d7110ef293735820b51dd193ae20953df60cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6703f255bd303f508704a42376dc3deca453ae1e45a046cca3a88da3fce48(
    *,
    enabled_download_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enabled_upload_phase: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    fail_closed: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    notification_settings: typing.Optional[typing.Union[TeamsAccountAntivirusNotificationSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe76ee86d94aaabc04add39fe7141c7c3c6d518bbe3584ac06e7eb2d433f796(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc868dd5be9700f7c36ea7ec51955968f99f4103c152a076d98361c29d6b3357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9772347973f45f2f2343cbf5aa9f419bc00a635b96facda43af41f116cebea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa727bf8a6338185c7cd92d7dc9bebe0b37c0214b4666176996002caa9d0721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b332388db739038b83e677a500e3ab7a8c8f958164ee9ce65da15286ed0bc1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea093a55867ec506e6de020b597a7eb54af25e08e5f664a17a9f536424a63189(
    value: typing.Optional[TeamsAccountAntivirusNotificationSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed742aaca36fa69c267fd1febe2c6c25f0f6e17ae95532eddfa23c2a437baec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e3c263a84a30585c736b4e799cb93f0e538630a5125a5f5b626b333f27e7ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8daddfac5caee701ea289f7040f6f53c1bba64cb2baa621277bd5a94a5e11c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527d83d1b2d221667ef3d87465698ebda0c422bea790191e84787890ca7a3ca4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9a4ff69ef114e0881c85964c2c9b10d568e6755ff69543fc4106b1940b2da4(
    value: typing.Optional[TeamsAccountAntivirus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36255eaa79cd0c9aa2c292c491f09f94b6b62a097cac76af03244c4f97c98ff3(
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

def _typecheckingstub__527b3b1c1eb56df08a4c73b760fc6669597697f095e315d6cbfe33541df4b7db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfe624729e9f485a04a12da9659f35c62dd59b84b3a1867ff2c3f98838f1123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f700efb75ee1dbad76190ac693694d9492e7ebc44de0e005de957887ed207b8b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366e2187ef7f0edc04bfd245ba59b669756f27b28433e0600821bd75ef2959a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3289acb6be17ca216f6ed11d894eb0231fc493c11ce29b3724ed2084a6f3ac98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c331426fe27038dd965dd3bd7dbf000e4ead221545c30d76afd7e0abed9c14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a61a160ee6f4682519fc3dd853f39e6d9c44445f33acce29de305bf14cb4bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2571f0683fedccc81de76824d4bdbce2d74b53b0eaca30ecb2c4c098509c383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96641c03b96e60cefe86f46cf4a5850784324a649d39b057ca606f9ee9adc1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbfec8662f6f3cb5842d30deff2af7d3674fe4c2b0d4c2dadccf362640a5d0f4(
    value: typing.Optional[TeamsAccountBlockPage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694a0f7b8cecea20c622def5a29cbf666e99e6dd97e60dc8da1d613c81e9bf3b(
    *,
    inspection_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a5be02a06b510e140a0d18490a5744c7d85b15104450fa4d29e9df8e3c5f43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786acfd89e0c3cc10fb514dd583e53d24fc6421954a9c640dbadd8ddce1d1435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70e6840555697f62974fdab59429fc88dbd9561f8a2886a94b976d21a00990f(
    value: typing.Optional[TeamsAccountBodyScanning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f6580e545ac36ccc86425127bfb8aa1043e714d477d6eee28efd3b2f1e99fa(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab819599626377dbc171f533cd077acb14d2381864ee8776b531763ab083a465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eff3ce2d57e376f336bfc7cbe8f559ebb7a38ab158059562c9639b3121bb409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0155b2eacb1496f5c0cbfd47a90ee2f167a08b9ca5119d6f013bfc89bfc2284d(
    value: typing.Optional[TeamsAccountCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9d9533e41d2295fc2ee51cc4d9cd2e8469c56522fd3bc9b7fc09c081ee7753(
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
    antivirus: typing.Optional[typing.Union[TeamsAccountAntivirus, typing.Dict[builtins.str, typing.Any]]] = None,
    block_page: typing.Optional[typing.Union[TeamsAccountBlockPage, typing.Dict[builtins.str, typing.Any]]] = None,
    body_scanning: typing.Optional[typing.Union[TeamsAccountBodyScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Union[TeamsAccountCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_certificate: typing.Optional[typing.Union[TeamsAccountCustomCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_email_matching: typing.Optional[typing.Union[TeamsAccountExtendedEmailMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    fips: typing.Optional[typing.Union[TeamsAccountFips, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[TeamsAccountLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    non_identity_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    payload_log: typing.Optional[typing.Union[TeamsAccountPayloadLog, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_detection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proxy: typing.Optional[typing.Union[TeamsAccountProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_session_log: typing.Optional[typing.Union[TeamsAccountSshSessionLog, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_decrypt_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    url_browser_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd5755a5f479ae45faa6deab233688d5d1325c0ba66d182cf6cdc4a9b8550f5(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8ba0ba359724a07e43e37891f4875f86d6d289e0c676b18044dfeb004afa5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba91b45882b4408fe4fa1a405f9388f1534ebce1579705239ce7765695c5bf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cdbdce8ebed3219c8c8f88614360559c9c272e68c8942e2ff8c019b0741b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faad44e29eff99d6380be1cc6286fc523a7e2614a972db6072f38e1231ba3a36(
    value: typing.Optional[TeamsAccountCustomCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3656bc7b3b78a14de7513b725682635cda9c9ab7e7552d2a4caba49a1438c5f7(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787be82cf99a0c0fc0f1f7046dff01d855154bfb31250be06d6d8d1b1014f293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1292a5e0be3e5173b3489f8a00beecfdf4f8fdbb14897aed001f1fea71478800(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8855283eebe0e9369cdd3ed3a979067af4e16c38f30999daadd10fdb68cda012(
    value: typing.Optional[TeamsAccountExtendedEmailMatching],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194a120d72438dcb19ad861bd1fc450aa12124342200c24b86511a23af3fd457(
    *,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66f4b9e4947214368b09aa52b1f7632b3d60932728293f4a623033d2c3a8e99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae2bf2eacae78234abea4a267a5aece6e02fd89286d4b855b2263592ae2ca2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d18a1c9fd73bf34f435dcbe4bb8ce8112d78774a7eee838c72823cd886f4b3a(
    value: typing.Optional[TeamsAccountFips],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e1585f1d1d8ce068bd33de4dfd4bcb64fb90a4a05d226bc744d7e3d8aa4de8(
    *,
    redact_pii: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    settings_by_rule_type: typing.Union[TeamsAccountLoggingSettingsByRuleType, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2361d44ddf69303acaf0b0cfae766852d324bb007e810d4a24fe0ef3ca64353e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352057726bbcc94a88b3ab95451f4a553f15888d0aa4f076eb98f19b02d19759(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d01240fd4f8e59c7b8a04779defaf1585d6f92afe1c6c9a2ec4decf9728c529(
    value: typing.Optional[TeamsAccountLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a906a38baee581243411daf966a7a6ed57a09027e62aa06e9ffc72338455c3(
    *,
    dns: typing.Union[TeamsAccountLoggingSettingsByRuleTypeDns, typing.Dict[builtins.str, typing.Any]],
    http: typing.Union[TeamsAccountLoggingSettingsByRuleTypeHttp, typing.Dict[builtins.str, typing.Any]],
    l4: typing.Union[TeamsAccountLoggingSettingsByRuleTypeL4, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2261f9133cee44c3be7f221cd466098ce7c06e05e2a1179bc0ff72c1f09924(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e595a9d9bc4afe14b3353bc64bafba64d8d649b8753f9c4a9e3565149780fca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df76a521476aedd34d191c96db2eac11ebfb9e74b12c090e12e501a330910fb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0575668b8b6c28825246a31b4bebf69904772e1e2b0c316717d5190b60c5d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7030a5895b50bea580e5bed4706639ed08df12be1a2e16e51e147493475219(
    value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f927924d537a73be3142b2e42d527dde53856638f01f670b9ca5d818c32f2d(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae1c9d5a8470fcb892e78f146523524eb343dfe67371eb6ee2545e7603585e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fede7b7c62295c379c2609fd0e684ba8b75f612def82fd5ab004efdffc0f7db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c73b3051b9ba4b705bb68e8ad0fc557f7221a9808e0e44a434a8448c7e5a5c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d90c25706203adc21e970bf8345409e215891420941ac324abbe3598a5d9f1f(
    value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeHttp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb9d485773317a46ffafc4a3bf4bae6a239d426bf8dbc57c0bcdbab7c11a62d(
    *,
    log_all: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_blocks: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcdf5fa233715c421247a39fd188d2608f0197d334784fe1fb915d4798f0342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5522950ffb7bf4b126d758d7089183e35e7fd5824fd1189e95bfb674cc9109(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138cd8a230a5c04e9eb91e037fbd8b672c26671daed96b2264dd06793dc1e14d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c56bf29763536211148d9c473c07137a269a035f0fe6e37b57c6029b1f71a0(
    value: typing.Optional[TeamsAccountLoggingSettingsByRuleTypeL4],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fd824a76e5042dec4b27841b5748002becaa9edd7a8a1800b1c3f3dae9a0cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f89b1df9fb4f146cf11f0eb7c81aa5925c3035dbee50dad8583d3c275032ac(
    value: typing.Optional[TeamsAccountLoggingSettingsByRuleType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad17fc527fc6d611dac35a9a445fabc5ada9c9d7364d19f31d53b48e0649404f(
    *,
    public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5264cf32b3b3c1d493f080323c26fa914a6dbc41f4efe22849d74ed3aaea523c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589c28b280e41b46ed9c76484eda9e50bfd2805022ac5b3b58e42b1d63de6f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b6187f6abab2cb755e733261a1ee98d8604a4b85c57f9915aadae98ce22d21(
    value: typing.Optional[TeamsAccountPayloadLog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130801578f58eaff857521cd311a5d3d1ea77bec955b8c1ee439bf2b07c3dbfd(
    *,
    disable_for_time: jsii.Number,
    root_ca: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    tcp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    udp: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    virtual_ip: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea760050892ffb637c567ca5e08b971812de7bea23e06a459c17bd72844f346(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d242c651d7ba888401e80ed8a2a2e7418d6888f387ded126dfdc3e40bc57e2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79def2d13ba589a840713d74c071c681e839c738d696e757eff1648bb7b50b19(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb89969ba7a56e902d4e49ee207d5ae0f68784cf24d1cf29b21e2c5d32909579(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34e4bc9e10de540d7442b87808ef3ac22f6d24a31449a9bedf3a70757e872fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18aade8824dff1fbcd0f7f4aec68a85b41e645a0d4f841cab704cf1a1a1d37c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6102917a023774c6605540ab2a06e5cc703ed5e06be953b3558f6112feaf9388(
    value: typing.Optional[TeamsAccountProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1414a306fa01121aeda7c16c2028731d9400230a604b81b758813713255fe943(
    *,
    public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5b869614c3c21e821c08f9a0779ae14b53df25426b61900b0cc0e158f1d483(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff0eed37fd4c595a25f3af8f8718ffe483f1dc13f1e3ceeac690ef1132405d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccb2192299f7979ea643fb755a27abcc4a2f42ed6fddd4ec461a021920912d9(
    value: typing.Optional[TeamsAccountSshSessionLog],
) -> None:
    """Type checking stubs"""
    pass
