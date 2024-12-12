r'''
# `cloudflare_zero_trust_access_application`

Refer to the Terraform Registry for docs: [`cloudflare_zero_trust_access_application`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application).
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


class ZeroTrustAccessApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application cloudflare_zero_trust_access_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: typing.Optional[builtins.str] = None,
        allow_authenticate_via_warp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_launcher_logo_url: typing.Optional[builtins.str] = None,
        app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bg_color: typing.Optional[builtins.str] = None,
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
        custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_type: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header_bg_color: typing.Optional[builtins.str] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        landing_page_design: typing.Optional[typing.Union["ZeroTrustAccessApplicationLandingPageDesign", typing.Dict[builtins.str, typing.Any]]] = None,
        logo_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        saas_app: typing.Optional[typing.Union["ZeroTrustAccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union["ZeroTrustAccessApplicationScimConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application cloudflare_zero_trust_access_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#account_id ZeroTrustAccessApplication#account_id}
        :param allow_authenticate_via_warp: When set to true, users can authenticate to this application using their WARP session. When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_authenticate_via_warp ZeroTrustAccessApplication#allow_authenticate_via_warp}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_idps ZeroTrustAccessApplication#allowed_idps}
        :param app_launcher_logo_url: The logo URL of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_logo_url ZeroTrustAccessApplication#app_launcher_logo_url}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_visible ZeroTrustAccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auto_redirect_to_identity ZeroTrustAccessApplication#auto_redirect_to_identity}
        :param bg_color: The background color of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#bg_color ZeroTrustAccessApplication#bg_color}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#cors_headers ZeroTrustAccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_message ZeroTrustAccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application via identity based rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_url ZeroTrustAccessApplication#custom_deny_url}
        :param custom_non_identity_deny_url: Option that redirects to a custom URL when a user is denied access to the application via non identity rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_non_identity_deny_url ZeroTrustAccessApplication#custom_non_identity_deny_url}
        :param custom_pages: The custom pages selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_pages ZeroTrustAccessApplication#custom_pages}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#destinations ZeroTrustAccessApplication#destinations}
        :param domain: The primary hostname and path that Access will secure. If the app is visible in the App Launcher dashboard, this is the domain that will be displayed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain ZeroTrustAccessApplication#domain}
        :param domain_type: The type of the primary domain. Available values: ``public``, ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain_type ZeroTrustAccessApplication#domain_type}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enable_binding_cookie ZeroTrustAccessApplication#enable_binding_cookie}
        :param footer_links: footer_links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#footer_links ZeroTrustAccessApplication#footer_links}
        :param header_bg_color: The background color of the header bar in the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#header_bg_color ZeroTrustAccessApplication#header_bg_color}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#http_only_cookie_attribute ZeroTrustAccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#id ZeroTrustAccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param landing_page_design: landing_page_design block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#landing_page_design ZeroTrustAccessApplication#landing_page_design}
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#logo_url ZeroTrustAccessApplication#logo_url}
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param options_preflight_bypass: Allows options preflight requests to bypass Access authentication and go directly to the origin. Cannot turn on if cors_headers is set. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#options_preflight_bypass ZeroTrustAccessApplication#options_preflight_bypass}
        :param policies: The policies associated with the application, in ascending order of precedence. Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#policies ZeroTrustAccessApplication#policies}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saas_app ZeroTrustAccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#same_site_cookie_attribute ZeroTrustAccessApplication#same_site_cookie_attribute}
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scim_config ZeroTrustAccessApplication#scim_config}
        :param self_hosted_domains: List of public domains secured by Access. Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#self_hosted_domains ZeroTrustAccessApplication#self_hosted_domains}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#service_auth_401_redirect ZeroTrustAccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#session_duration ZeroTrustAccessApplication#session_duration}
        :param skip_app_launcher_login_page: Option to skip the App Launcher landing page. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_app_launcher_login_page ZeroTrustAccessApplication#skip_app_launcher_login_page}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_interstitial ZeroTrustAccessApplication#skip_interstitial}
        :param tags: The itags associated with the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#tags ZeroTrustAccessApplication#tags}
        :param target_criteria: target_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#target_criteria ZeroTrustAccessApplication#target_criteria}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#type ZeroTrustAccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#zone_id ZeroTrustAccessApplication#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27338aeeecd2e31c5778c77e6b90d648344d66ce330b5d2a91fa9403173c8b94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZeroTrustAccessApplicationConfig(
            account_id=account_id,
            allow_authenticate_via_warp=allow_authenticate_via_warp,
            allowed_idps=allowed_idps,
            app_launcher_logo_url=app_launcher_logo_url,
            app_launcher_visible=app_launcher_visible,
            auto_redirect_to_identity=auto_redirect_to_identity,
            bg_color=bg_color,
            cors_headers=cors_headers,
            custom_deny_message=custom_deny_message,
            custom_deny_url=custom_deny_url,
            custom_non_identity_deny_url=custom_non_identity_deny_url,
            custom_pages=custom_pages,
            destinations=destinations,
            domain=domain,
            domain_type=domain_type,
            enable_binding_cookie=enable_binding_cookie,
            footer_links=footer_links,
            header_bg_color=header_bg_color,
            http_only_cookie_attribute=http_only_cookie_attribute,
            id=id,
            landing_page_design=landing_page_design,
            logo_url=logo_url,
            name=name,
            options_preflight_bypass=options_preflight_bypass,
            policies=policies,
            saas_app=saas_app,
            same_site_cookie_attribute=same_site_cookie_attribute,
            scim_config=scim_config,
            self_hosted_domains=self_hosted_domains,
            service_auth401_redirect=service_auth401_redirect,
            session_duration=session_duration,
            skip_app_launcher_login_page=skip_app_launcher_login_page,
            skip_interstitial=skip_interstitial,
            tags=tags,
            target_criteria=target_criteria,
            type=type,
            zone_id=zone_id,
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
        '''Generates CDKTF code for importing a ZeroTrustAccessApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ZeroTrustAccessApplication to import.
        :param import_from_id: The id of the existing ZeroTrustAccessApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ZeroTrustAccessApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aed9d1c8ee78428e088d71f6579e3d02e4f30fb17461e201068a0829c6d553)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsHeaders")
    def put_cors_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b74a9e8f14e0bc0b5d1004a5b1f8b96ee3a309867c32ac47e54e67e549b756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsHeaders", [value]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a01e38fa3f74cc489795b06ff4df8da8c34523777fc462714c8fd0a21c8e3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putFooterLinks")
    def put_footer_links(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69b01b6350443f6fa14a95caa04e5b39c3826cfbbbc0be0bb475a2a02a6225e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFooterLinks", [value]))

    @jsii.member(jsii_name="putLandingPageDesign")
    def put_landing_page_design(
        self,
        *,
        button_color: typing.Optional[builtins.str] = None,
        button_text_color: typing.Optional[builtins.str] = None,
        image_url: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param button_color: The button color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_color ZeroTrustAccessApplication#button_color}
        :param button_text_color: The button text color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_text_color ZeroTrustAccessApplication#button_text_color}
        :param image_url: The URL of the image to be displayed in the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#image_url ZeroTrustAccessApplication#image_url}
        :param message: The message of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#message ZeroTrustAccessApplication#message}
        :param title: The title of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#title ZeroTrustAccessApplication#title}
        '''
        value = ZeroTrustAccessApplicationLandingPageDesign(
            button_color=button_color,
            button_text_color=button_text_color,
            image_url=image_url,
            message=message,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putLandingPageDesign", [value]))

    @jsii.member(jsii_name="putSaasApp")
    def put_saas_app(
        self,
        *,
        access_token_lifetime: typing.Optional[builtins.str] = None,
        allow_pkce_without_client_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        app_launcher_url: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        consumer_service_url: typing.Optional[builtins.str] = None,
        custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppCustomAttribute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppCustomClaim", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_filter_regex: typing.Optional[builtins.str] = None,
        hybrid_and_implicit_options: typing.Optional[typing.Union["ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_id_format: typing.Optional[builtins.str] = None,
        name_id_transform_jsonata: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token_lifetime: The lifetime of the Access Token after creation. Valid units are ``m`` and ``h``. Must be greater than or equal to 1m and less than or equal to 24h. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#access_token_lifetime ZeroTrustAccessApplication#access_token_lifetime}
        :param allow_pkce_without_client_secret: Allow PKCE flow without a client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_pkce_without_client_secret ZeroTrustAccessApplication#allow_pkce_without_client_secret}
        :param app_launcher_url: The URL where this applications tile redirects users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_url ZeroTrustAccessApplication#app_launcher_url}
        :param auth_type: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auth_type ZeroTrustAccessApplication#auth_type}
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#consumer_service_url ZeroTrustAccessApplication#consumer_service_url}
        :param custom_attribute: custom_attribute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_attribute ZeroTrustAccessApplication#custom_attribute}
        :param custom_claim: custom_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_claim ZeroTrustAccessApplication#custom_claim}
        :param default_relay_state: The relay state used if not provided by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#default_relay_state ZeroTrustAccessApplication#default_relay_state}
        :param grant_types: The OIDC flows supported by this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#grant_types ZeroTrustAccessApplication#grant_types}
        :param group_filter_regex: A regex to filter Cloudflare groups returned in ID token and userinfo endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#group_filter_regex ZeroTrustAccessApplication#group_filter_regex}
        :param hybrid_and_implicit_options: hybrid_and_implicit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#hybrid_and_implicit_options ZeroTrustAccessApplication#hybrid_and_implicit_options}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_format ZeroTrustAccessApplication#name_id_format}
        :param name_id_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_transform_jsonata ZeroTrustAccessApplication#name_id_transform_jsonata}
        :param redirect_uris: The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#redirect_uris ZeroTrustAccessApplication#redirect_uris}
        :param refresh_token_options: refresh_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#refresh_token_options ZeroTrustAccessApplication#refresh_token_options}
        :param saml_attribute_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saml_attribute_transform_jsonata ZeroTrustAccessApplication#saml_attribute_transform_jsonata}
        :param scopes: Define the user information shared with access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#sp_entity_id ZeroTrustAccessApplication#sp_entity_id}
        '''
        value = ZeroTrustAccessApplicationSaasApp(
            access_token_lifetime=access_token_lifetime,
            allow_pkce_without_client_secret=allow_pkce_without_client_secret,
            app_launcher_url=app_launcher_url,
            auth_type=auth_type,
            consumer_service_url=consumer_service_url,
            custom_attribute=custom_attribute,
            custom_claim=custom_claim,
            default_relay_state=default_relay_state,
            grant_types=grant_types,
            group_filter_regex=group_filter_regex,
            hybrid_and_implicit_options=hybrid_and_implicit_options,
            name_id_format=name_id_format,
            name_id_transform_jsonata=name_id_transform_jsonata,
            redirect_uris=redirect_uris,
            refresh_token_options=refresh_token_options,
            saml_attribute_transform_jsonata=saml_attribute_transform_jsonata,
            scopes=scopes,
            sp_entity_id=sp_entity_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSaasApp", [value]))

    @jsii.member(jsii_name="putScimConfig")
    def put_scim_config(
        self,
        *,
        idp_uid: builtins.str,
        remote_uri: builtins.str,
        authentication: typing.Optional[typing.Union["ZeroTrustAccessApplicationScimConfigAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationScimConfigMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param idp_uid: The UIDs of the IdP to use as the source for SCIM resources to provision to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#idp_uid ZeroTrustAccessApplication#idp_uid}
        :param remote_uri: The base URI for the application's SCIM-compatible API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#remote_uri ZeroTrustAccessApplication#remote_uri}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authentication ZeroTrustAccessApplication#authentication}
        :param deactivate_on_delete: If false, propagates DELETE requests to the target application for SCIM resources. If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#deactivate_on_delete ZeroTrustAccessApplication#deactivate_on_delete}
        :param enabled: Whether SCIM provisioning is turned on for this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enabled ZeroTrustAccessApplication#enabled}
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#mappings ZeroTrustAccessApplication#mappings}
        '''
        value = ZeroTrustAccessApplicationScimConfig(
            idp_uid=idp_uid,
            remote_uri=remote_uri,
            authentication=authentication,
            deactivate_on_delete=deactivate_on_delete,
            enabled=enabled,
            mappings=mappings,
        )

        return typing.cast(None, jsii.invoke(self, "putScimConfig", [value]))

    @jsii.member(jsii_name="putTargetCriteria")
    def put_target_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29efcca397269d22b3a8f8f3a86f3abb19cd0dbf9186b3d59feb062d1fc06075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetCriteria", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAllowAuthenticateViaWarp")
    def reset_allow_authenticate_via_warp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAuthenticateViaWarp", []))

    @jsii.member(jsii_name="resetAllowedIdps")
    def reset_allowed_idps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIdps", []))

    @jsii.member(jsii_name="resetAppLauncherLogoUrl")
    def reset_app_launcher_logo_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLauncherLogoUrl", []))

    @jsii.member(jsii_name="resetAppLauncherVisible")
    def reset_app_launcher_visible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLauncherVisible", []))

    @jsii.member(jsii_name="resetAutoRedirectToIdentity")
    def reset_auto_redirect_to_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRedirectToIdentity", []))

    @jsii.member(jsii_name="resetBgColor")
    def reset_bg_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgColor", []))

    @jsii.member(jsii_name="resetCorsHeaders")
    def reset_cors_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsHeaders", []))

    @jsii.member(jsii_name="resetCustomDenyMessage")
    def reset_custom_deny_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDenyMessage", []))

    @jsii.member(jsii_name="resetCustomDenyUrl")
    def reset_custom_deny_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDenyUrl", []))

    @jsii.member(jsii_name="resetCustomNonIdentityDenyUrl")
    def reset_custom_non_identity_deny_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomNonIdentityDenyUrl", []))

    @jsii.member(jsii_name="resetCustomPages")
    def reset_custom_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPages", []))

    @jsii.member(jsii_name="resetDestinations")
    def reset_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinations", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetDomainType")
    def reset_domain_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainType", []))

    @jsii.member(jsii_name="resetEnableBindingCookie")
    def reset_enable_binding_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableBindingCookie", []))

    @jsii.member(jsii_name="resetFooterLinks")
    def reset_footer_links(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFooterLinks", []))

    @jsii.member(jsii_name="resetHeaderBgColor")
    def reset_header_bg_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderBgColor", []))

    @jsii.member(jsii_name="resetHttpOnlyCookieAttribute")
    def reset_http_only_cookie_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpOnlyCookieAttribute", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLandingPageDesign")
    def reset_landing_page_design(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLandingPageDesign", []))

    @jsii.member(jsii_name="resetLogoUrl")
    def reset_logo_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoUrl", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOptionsPreflightBypass")
    def reset_options_preflight_bypass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionsPreflightBypass", []))

    @jsii.member(jsii_name="resetPolicies")
    def reset_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicies", []))

    @jsii.member(jsii_name="resetSaasApp")
    def reset_saas_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaasApp", []))

    @jsii.member(jsii_name="resetSameSiteCookieAttribute")
    def reset_same_site_cookie_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSameSiteCookieAttribute", []))

    @jsii.member(jsii_name="resetScimConfig")
    def reset_scim_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScimConfig", []))

    @jsii.member(jsii_name="resetSelfHostedDomains")
    def reset_self_hosted_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelfHostedDomains", []))

    @jsii.member(jsii_name="resetServiceAuth401Redirect")
    def reset_service_auth401_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAuth401Redirect", []))

    @jsii.member(jsii_name="resetSessionDuration")
    def reset_session_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionDuration", []))

    @jsii.member(jsii_name="resetSkipAppLauncherLoginPage")
    def reset_skip_app_launcher_login_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipAppLauncherLoginPage", []))

    @jsii.member(jsii_name="resetSkipInterstitial")
    def reset_skip_interstitial(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipInterstitial", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTargetCriteria")
    def reset_target_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetCriteria", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="aud")
    def aud(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aud"))

    @builtins.property
    @jsii.member(jsii_name="corsHeaders")
    def cors_headers(self) -> "ZeroTrustAccessApplicationCorsHeadersList":
        return typing.cast("ZeroTrustAccessApplicationCorsHeadersList", jsii.get(self, "corsHeaders"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "ZeroTrustAccessApplicationDestinationsList":
        return typing.cast("ZeroTrustAccessApplicationDestinationsList", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="footerLinks")
    def footer_links(self) -> "ZeroTrustAccessApplicationFooterLinksList":
        return typing.cast("ZeroTrustAccessApplicationFooterLinksList", jsii.get(self, "footerLinks"))

    @builtins.property
    @jsii.member(jsii_name="landingPageDesign")
    def landing_page_design(
        self,
    ) -> "ZeroTrustAccessApplicationLandingPageDesignOutputReference":
        return typing.cast("ZeroTrustAccessApplicationLandingPageDesignOutputReference", jsii.get(self, "landingPageDesign"))

    @builtins.property
    @jsii.member(jsii_name="saasApp")
    def saas_app(self) -> "ZeroTrustAccessApplicationSaasAppOutputReference":
        return typing.cast("ZeroTrustAccessApplicationSaasAppOutputReference", jsii.get(self, "saasApp"))

    @builtins.property
    @jsii.member(jsii_name="scimConfig")
    def scim_config(self) -> "ZeroTrustAccessApplicationScimConfigOutputReference":
        return typing.cast("ZeroTrustAccessApplicationScimConfigOutputReference", jsii.get(self, "scimConfig"))

    @builtins.property
    @jsii.member(jsii_name="targetCriteria")
    def target_criteria(self) -> "ZeroTrustAccessApplicationTargetCriteriaList":
        return typing.cast("ZeroTrustAccessApplicationTargetCriteriaList", jsii.get(self, "targetCriteria"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAuthenticateViaWarpInput")
    def allow_authenticate_via_warp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAuthenticateViaWarpInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIdpsInput")
    def allowed_idps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIdpsInput"))

    @builtins.property
    @jsii.member(jsii_name="appLauncherLogoUrlInput")
    def app_launcher_logo_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appLauncherLogoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="appLauncherVisibleInput")
    def app_launcher_visible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appLauncherVisibleInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRedirectToIdentityInput")
    def auto_redirect_to_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRedirectToIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="bgColorInput")
    def bg_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgColorInput"))

    @builtins.property
    @jsii.member(jsii_name="corsHeadersInput")
    def cors_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationCorsHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationCorsHeaders"]]], jsii.get(self, "corsHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="customDenyMessageInput")
    def custom_deny_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDenyMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="customDenyUrlInput")
    def custom_deny_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDenyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="customNonIdentityDenyUrlInput")
    def custom_non_identity_deny_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customNonIdentityDenyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="customPagesInput")
    def custom_pages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customPagesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationDestinations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationDestinations"]]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="domainTypeInput")
    def domain_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enableBindingCookieInput")
    def enable_binding_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableBindingCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="footerLinksInput")
    def footer_links_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationFooterLinks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationFooterLinks"]]], jsii.get(self, "footerLinksInput"))

    @builtins.property
    @jsii.member(jsii_name="headerBgColorInput")
    def header_bg_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerBgColorInput"))

    @builtins.property
    @jsii.member(jsii_name="httpOnlyCookieAttributeInput")
    def http_only_cookie_attribute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpOnlyCookieAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="landingPageDesignInput")
    def landing_page_design_input(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationLandingPageDesign"]:
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationLandingPageDesign"], jsii.get(self, "landingPageDesignInput"))

    @builtins.property
    @jsii.member(jsii_name="logoUrlInput")
    def logo_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsPreflightBypassInput")
    def options_preflight_bypass_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionsPreflightBypassInput"))

    @builtins.property
    @jsii.member(jsii_name="policiesInput")
    def policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policiesInput"))

    @builtins.property
    @jsii.member(jsii_name="saasAppInput")
    def saas_app_input(self) -> typing.Optional["ZeroTrustAccessApplicationSaasApp"]:
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationSaasApp"], jsii.get(self, "saasAppInput"))

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttributeInput")
    def same_site_cookie_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sameSiteCookieAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="scimConfigInput")
    def scim_config_input(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationScimConfig"]:
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationScimConfig"], jsii.get(self, "scimConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="selfHostedDomainsInput")
    def self_hosted_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "selfHostedDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAuth401RedirectInput")
    def service_auth401_redirect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serviceAuth401RedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionDurationInput")
    def session_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="skipAppLauncherLoginPageInput")
    def skip_app_launcher_login_page_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipAppLauncherLoginPageInput"))

    @builtins.property
    @jsii.member(jsii_name="skipInterstitialInput")
    def skip_interstitial_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipInterstitialInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCriteriaInput")
    def target_criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteria"]]], jsii.get(self, "targetCriteriaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fec731061956ee4a6f8bb3a95fbebdcd6aaf64c49f851492c2b536b1eddd1f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowAuthenticateViaWarp")
    def allow_authenticate_via_warp(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAuthenticateViaWarp"))

    @allow_authenticate_via_warp.setter
    def allow_authenticate_via_warp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3c1cb91eeae56a8cf2cc59bdb6b2795ccad015bd24206d07e0951f56c89636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAuthenticateViaWarp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIdps")
    def allowed_idps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIdps"))

    @allowed_idps.setter
    def allowed_idps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be64e8ac39fca2dd2500aa0b54d299e1bc29de142d2d4612f9e17af4b10799f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIdps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appLauncherLogoUrl")
    def app_launcher_logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLauncherLogoUrl"))

    @app_launcher_logo_url.setter
    def app_launcher_logo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1457a5e561e09d35265af36cf5ca06925dc1dce9801441f692b1fb3fd3b320ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLauncherLogoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appLauncherVisible")
    def app_launcher_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "appLauncherVisible"))

    @app_launcher_visible.setter
    def app_launcher_visible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d7c21a4a8c8ab0de0d7f1ecc46004dcf0662e0a2cc335f5267670f1f64525c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLauncherVisible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoRedirectToIdentity")
    def auto_redirect_to_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRedirectToIdentity"))

    @auto_redirect_to_identity.setter
    def auto_redirect_to_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b2c9f95fc566b2f077f059a82d95b631ad2429361b9dba2a2ed2694ebf6854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRedirectToIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgColor")
    def bg_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgColor"))

    @bg_color.setter
    def bg_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff301b82f24f646a2cb5ef99ea6a32ce4f9c04cdbb27a5d4ada20b67d4f5eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDenyMessage")
    def custom_deny_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyMessage"))

    @custom_deny_message.setter
    def custom_deny_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47019a4be708eb71f0f058e0eede1241f8158b762556db853df184499ea6ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDenyUrl")
    def custom_deny_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyUrl"))

    @custom_deny_url.setter
    def custom_deny_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e27c1cb8a4167f8e04ac0d6c18ada8a4b250b5de4ca6f3c845385a23be8379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customNonIdentityDenyUrl")
    def custom_non_identity_deny_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customNonIdentityDenyUrl"))

    @custom_non_identity_deny_url.setter
    def custom_non_identity_deny_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3a3d032f0b868b35c26301c384de6a32873fbeb250a3f3294135e8f80a7f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customNonIdentityDenyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPages")
    def custom_pages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customPages"))

    @custom_pages.setter
    def custom_pages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08aca6db6ca2d706006c7c12a3dc79270cee71da8486e494cb688f27442e4f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8004de509defca4d78cf6a2555915db9666893c72c10c436cf77de1e893ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainType")
    def domain_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainType"))

    @domain_type.setter
    def domain_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd46fea72ce47a2cb8c1038d28bc97dd5ab94441af6f154d0d17a712950ec37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableBindingCookie")
    def enable_binding_cookie(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableBindingCookie"))

    @enable_binding_cookie.setter
    def enable_binding_cookie(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a765eff579c85806c83ac9f1fa443520c9cfcb800a0081b0516ce1f5af65fe8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBindingCookie", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerBgColor")
    def header_bg_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerBgColor"))

    @header_bg_color.setter
    def header_bg_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee4e1351d0024499a383aab5b228a41a8b6d5c815456c021b3f24d0b3adf498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerBgColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpOnlyCookieAttribute")
    def http_only_cookie_attribute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpOnlyCookieAttribute"))

    @http_only_cookie_attribute.setter
    def http_only_cookie_attribute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a234bcc12ea03ebba0a2fd2beb7c5da757daf1a34e5f0f7d655bad92a3ee2425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpOnlyCookieAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d151783486bb3f4aff9f1d4aff06c316ba75a01a3e4e7fe45e271701b7dcaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @logo_url.setter
    def logo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0d042e7fb8029cf39fd64da67feaaaabb16a462aa84e0da680533bb09db1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cb26c3ba6e995d5381c8693e2f4791dc952dcf01b159b9dd90e528177d7233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optionsPreflightBypass")
    def options_preflight_bypass(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optionsPreflightBypass"))

    @options_preflight_bypass.setter
    def options_preflight_bypass(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb9aa9809673e3b121460e152319e7a1aabe343c83038d99e1a9389706fdd34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionsPreflightBypass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "policies"))

    @policies.setter
    def policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04ed784e46647bbd756e89e1abc862e4da00addfd61a13f6536f03673217a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttribute")
    def same_site_cookie_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sameSiteCookieAttribute"))

    @same_site_cookie_attribute.setter
    def same_site_cookie_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cead96487ecf56f324721527887db96515004eafe6e4934b0218556799b20014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sameSiteCookieAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfHostedDomains")
    def self_hosted_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "selfHostedDomains"))

    @self_hosted_domains.setter
    def self_hosted_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7027add4c94ff5c6e1d9d981891a6e2d08756603689c68714f7ab199c29667f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selfHostedDomains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAuth401Redirect")
    def service_auth401_redirect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serviceAuth401Redirect"))

    @service_auth401_redirect.setter
    def service_auth401_redirect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018e0e147bf616117e34644ac9fc785c3537999f64d5e9d3d0af55c0e91db961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAuth401Redirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionDuration"))

    @session_duration.setter
    def session_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0735f107a1bad1083eaf92196f572661daa359b0ad1c704fef6dee2068d97a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipAppLauncherLoginPage")
    def skip_app_launcher_login_page(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipAppLauncherLoginPage"))

    @skip_app_launcher_login_page.setter
    def skip_app_launcher_login_page(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895090706d57872884433315cbdbc3cc94643221d625c7ff51d8c73fa56f70db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipAppLauncherLoginPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipInterstitial")
    def skip_interstitial(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipInterstitial"))

    @skip_interstitial.setter
    def skip_interstitial(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d96622f0d48fee60151148031537f7ae6703fa09d88913fc82a3c8e50b291e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipInterstitial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6871878039e238faffb7567ecb3ee909e5a3840597f72ad141e4abcf93aa1ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195de0e3b7b7a39255d38a862a353bf9e4ae6f9519c29c520e71e02578a424ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36279d7f822e7c4fc42a6f41cadc4da245c4c9c778ac045de3186657c462b46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationConfig",
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
        "allow_authenticate_via_warp": "allowAuthenticateViaWarp",
        "allowed_idps": "allowedIdps",
        "app_launcher_logo_url": "appLauncherLogoUrl",
        "app_launcher_visible": "appLauncherVisible",
        "auto_redirect_to_identity": "autoRedirectToIdentity",
        "bg_color": "bgColor",
        "cors_headers": "corsHeaders",
        "custom_deny_message": "customDenyMessage",
        "custom_deny_url": "customDenyUrl",
        "custom_non_identity_deny_url": "customNonIdentityDenyUrl",
        "custom_pages": "customPages",
        "destinations": "destinations",
        "domain": "domain",
        "domain_type": "domainType",
        "enable_binding_cookie": "enableBindingCookie",
        "footer_links": "footerLinks",
        "header_bg_color": "headerBgColor",
        "http_only_cookie_attribute": "httpOnlyCookieAttribute",
        "id": "id",
        "landing_page_design": "landingPageDesign",
        "logo_url": "logoUrl",
        "name": "name",
        "options_preflight_bypass": "optionsPreflightBypass",
        "policies": "policies",
        "saas_app": "saasApp",
        "same_site_cookie_attribute": "sameSiteCookieAttribute",
        "scim_config": "scimConfig",
        "self_hosted_domains": "selfHostedDomains",
        "service_auth401_redirect": "serviceAuth401Redirect",
        "session_duration": "sessionDuration",
        "skip_app_launcher_login_page": "skipAppLauncherLoginPage",
        "skip_interstitial": "skipInterstitial",
        "tags": "tags",
        "target_criteria": "targetCriteria",
        "type": "type",
        "zone_id": "zoneId",
    },
)
class ZeroTrustAccessApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: typing.Optional[builtins.str] = None,
        allow_authenticate_via_warp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
        app_launcher_logo_url: typing.Optional[builtins.str] = None,
        app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bg_color: typing.Optional[builtins.str] = None,
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
        custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_type: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header_bg_color: typing.Optional[builtins.str] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        landing_page_design: typing.Optional[typing.Union["ZeroTrustAccessApplicationLandingPageDesign", typing.Dict[builtins.str, typing.Any]]] = None,
        logo_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        saas_app: typing.Optional[typing.Union["ZeroTrustAccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union["ZeroTrustAccessApplicationScimConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
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
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#account_id ZeroTrustAccessApplication#account_id}
        :param allow_authenticate_via_warp: When set to true, users can authenticate to this application using their WARP session. When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_authenticate_via_warp ZeroTrustAccessApplication#allow_authenticate_via_warp}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_idps ZeroTrustAccessApplication#allowed_idps}
        :param app_launcher_logo_url: The logo URL of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_logo_url ZeroTrustAccessApplication#app_launcher_logo_url}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_visible ZeroTrustAccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auto_redirect_to_identity ZeroTrustAccessApplication#auto_redirect_to_identity}
        :param bg_color: The background color of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#bg_color ZeroTrustAccessApplication#bg_color}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#cors_headers ZeroTrustAccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_message ZeroTrustAccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application via identity based rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_url ZeroTrustAccessApplication#custom_deny_url}
        :param custom_non_identity_deny_url: Option that redirects to a custom URL when a user is denied access to the application via non identity rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_non_identity_deny_url ZeroTrustAccessApplication#custom_non_identity_deny_url}
        :param custom_pages: The custom pages selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_pages ZeroTrustAccessApplication#custom_pages}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#destinations ZeroTrustAccessApplication#destinations}
        :param domain: The primary hostname and path that Access will secure. If the app is visible in the App Launcher dashboard, this is the domain that will be displayed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain ZeroTrustAccessApplication#domain}
        :param domain_type: The type of the primary domain. Available values: ``public``, ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain_type ZeroTrustAccessApplication#domain_type}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enable_binding_cookie ZeroTrustAccessApplication#enable_binding_cookie}
        :param footer_links: footer_links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#footer_links ZeroTrustAccessApplication#footer_links}
        :param header_bg_color: The background color of the header bar in the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#header_bg_color ZeroTrustAccessApplication#header_bg_color}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#http_only_cookie_attribute ZeroTrustAccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#id ZeroTrustAccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param landing_page_design: landing_page_design block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#landing_page_design ZeroTrustAccessApplication#landing_page_design}
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#logo_url ZeroTrustAccessApplication#logo_url}
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param options_preflight_bypass: Allows options preflight requests to bypass Access authentication and go directly to the origin. Cannot turn on if cors_headers is set. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#options_preflight_bypass ZeroTrustAccessApplication#options_preflight_bypass}
        :param policies: The policies associated with the application, in ascending order of precedence. Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#policies ZeroTrustAccessApplication#policies}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saas_app ZeroTrustAccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#same_site_cookie_attribute ZeroTrustAccessApplication#same_site_cookie_attribute}
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scim_config ZeroTrustAccessApplication#scim_config}
        :param self_hosted_domains: List of public domains secured by Access. Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#self_hosted_domains ZeroTrustAccessApplication#self_hosted_domains}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#service_auth_401_redirect ZeroTrustAccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#session_duration ZeroTrustAccessApplication#session_duration}
        :param skip_app_launcher_login_page: Option to skip the App Launcher landing page. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_app_launcher_login_page ZeroTrustAccessApplication#skip_app_launcher_login_page}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_interstitial ZeroTrustAccessApplication#skip_interstitial}
        :param tags: The itags associated with the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#tags ZeroTrustAccessApplication#tags}
        :param target_criteria: target_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#target_criteria ZeroTrustAccessApplication#target_criteria}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#type ZeroTrustAccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#zone_id ZeroTrustAccessApplication#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(landing_page_design, dict):
            landing_page_design = ZeroTrustAccessApplicationLandingPageDesign(**landing_page_design)
        if isinstance(saas_app, dict):
            saas_app = ZeroTrustAccessApplicationSaasApp(**saas_app)
        if isinstance(scim_config, dict):
            scim_config = ZeroTrustAccessApplicationScimConfig(**scim_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1279db324fed64f313ac2ca6fb2cb06c24a138a471a8e0566ec470159c6fbf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument allow_authenticate_via_warp", value=allow_authenticate_via_warp, expected_type=type_hints["allow_authenticate_via_warp"])
            check_type(argname="argument allowed_idps", value=allowed_idps, expected_type=type_hints["allowed_idps"])
            check_type(argname="argument app_launcher_logo_url", value=app_launcher_logo_url, expected_type=type_hints["app_launcher_logo_url"])
            check_type(argname="argument app_launcher_visible", value=app_launcher_visible, expected_type=type_hints["app_launcher_visible"])
            check_type(argname="argument auto_redirect_to_identity", value=auto_redirect_to_identity, expected_type=type_hints["auto_redirect_to_identity"])
            check_type(argname="argument bg_color", value=bg_color, expected_type=type_hints["bg_color"])
            check_type(argname="argument cors_headers", value=cors_headers, expected_type=type_hints["cors_headers"])
            check_type(argname="argument custom_deny_message", value=custom_deny_message, expected_type=type_hints["custom_deny_message"])
            check_type(argname="argument custom_deny_url", value=custom_deny_url, expected_type=type_hints["custom_deny_url"])
            check_type(argname="argument custom_non_identity_deny_url", value=custom_non_identity_deny_url, expected_type=type_hints["custom_non_identity_deny_url"])
            check_type(argname="argument custom_pages", value=custom_pages, expected_type=type_hints["custom_pages"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_type", value=domain_type, expected_type=type_hints["domain_type"])
            check_type(argname="argument enable_binding_cookie", value=enable_binding_cookie, expected_type=type_hints["enable_binding_cookie"])
            check_type(argname="argument footer_links", value=footer_links, expected_type=type_hints["footer_links"])
            check_type(argname="argument header_bg_color", value=header_bg_color, expected_type=type_hints["header_bg_color"])
            check_type(argname="argument http_only_cookie_attribute", value=http_only_cookie_attribute, expected_type=type_hints["http_only_cookie_attribute"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument landing_page_design", value=landing_page_design, expected_type=type_hints["landing_page_design"])
            check_type(argname="argument logo_url", value=logo_url, expected_type=type_hints["logo_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options_preflight_bypass", value=options_preflight_bypass, expected_type=type_hints["options_preflight_bypass"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument saas_app", value=saas_app, expected_type=type_hints["saas_app"])
            check_type(argname="argument same_site_cookie_attribute", value=same_site_cookie_attribute, expected_type=type_hints["same_site_cookie_attribute"])
            check_type(argname="argument scim_config", value=scim_config, expected_type=type_hints["scim_config"])
            check_type(argname="argument self_hosted_domains", value=self_hosted_domains, expected_type=type_hints["self_hosted_domains"])
            check_type(argname="argument service_auth401_redirect", value=service_auth401_redirect, expected_type=type_hints["service_auth401_redirect"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
            check_type(argname="argument skip_app_launcher_login_page", value=skip_app_launcher_login_page, expected_type=type_hints["skip_app_launcher_login_page"])
            check_type(argname="argument skip_interstitial", value=skip_interstitial, expected_type=type_hints["skip_interstitial"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_criteria", value=target_criteria, expected_type=type_hints["target_criteria"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if allow_authenticate_via_warp is not None:
            self._values["allow_authenticate_via_warp"] = allow_authenticate_via_warp
        if allowed_idps is not None:
            self._values["allowed_idps"] = allowed_idps
        if app_launcher_logo_url is not None:
            self._values["app_launcher_logo_url"] = app_launcher_logo_url
        if app_launcher_visible is not None:
            self._values["app_launcher_visible"] = app_launcher_visible
        if auto_redirect_to_identity is not None:
            self._values["auto_redirect_to_identity"] = auto_redirect_to_identity
        if bg_color is not None:
            self._values["bg_color"] = bg_color
        if cors_headers is not None:
            self._values["cors_headers"] = cors_headers
        if custom_deny_message is not None:
            self._values["custom_deny_message"] = custom_deny_message
        if custom_deny_url is not None:
            self._values["custom_deny_url"] = custom_deny_url
        if custom_non_identity_deny_url is not None:
            self._values["custom_non_identity_deny_url"] = custom_non_identity_deny_url
        if custom_pages is not None:
            self._values["custom_pages"] = custom_pages
        if destinations is not None:
            self._values["destinations"] = destinations
        if domain is not None:
            self._values["domain"] = domain
        if domain_type is not None:
            self._values["domain_type"] = domain_type
        if enable_binding_cookie is not None:
            self._values["enable_binding_cookie"] = enable_binding_cookie
        if footer_links is not None:
            self._values["footer_links"] = footer_links
        if header_bg_color is not None:
            self._values["header_bg_color"] = header_bg_color
        if http_only_cookie_attribute is not None:
            self._values["http_only_cookie_attribute"] = http_only_cookie_attribute
        if id is not None:
            self._values["id"] = id
        if landing_page_design is not None:
            self._values["landing_page_design"] = landing_page_design
        if logo_url is not None:
            self._values["logo_url"] = logo_url
        if name is not None:
            self._values["name"] = name
        if options_preflight_bypass is not None:
            self._values["options_preflight_bypass"] = options_preflight_bypass
        if policies is not None:
            self._values["policies"] = policies
        if saas_app is not None:
            self._values["saas_app"] = saas_app
        if same_site_cookie_attribute is not None:
            self._values["same_site_cookie_attribute"] = same_site_cookie_attribute
        if scim_config is not None:
            self._values["scim_config"] = scim_config
        if self_hosted_domains is not None:
            self._values["self_hosted_domains"] = self_hosted_domains
        if service_auth401_redirect is not None:
            self._values["service_auth401_redirect"] = service_auth401_redirect
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if skip_app_launcher_login_page is not None:
            self._values["skip_app_launcher_login_page"] = skip_app_launcher_login_page
        if skip_interstitial is not None:
            self._values["skip_interstitial"] = skip_interstitial
        if tags is not None:
            self._values["tags"] = tags
        if target_criteria is not None:
            self._values["target_criteria"] = target_criteria
        if type is not None:
            self._values["type"] = type
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
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. Conflicts with ``zone_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#account_id ZeroTrustAccessApplication#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_authenticate_via_warp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, users can authenticate to this application using their WARP session.

        When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_authenticate_via_warp ZeroTrustAccessApplication#allow_authenticate_via_warp}
        '''
        result = self._values.get("allow_authenticate_via_warp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_idps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identity providers selected for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_idps ZeroTrustAccessApplication#allowed_idps}
        '''
        result = self._values.get("allowed_idps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def app_launcher_logo_url(self) -> typing.Optional[builtins.str]:
        '''The logo URL of the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_logo_url ZeroTrustAccessApplication#app_launcher_logo_url}
        '''
        result = self._values.get("app_launcher_logo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_launcher_visible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to show/hide applications in App Launcher. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_visible ZeroTrustAccessApplication#app_launcher_visible}
        '''
        result = self._values.get("app_launcher_visible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_redirect_to_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auto_redirect_to_identity ZeroTrustAccessApplication#auto_redirect_to_identity}
        '''
        result = self._values.get("auto_redirect_to_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bg_color(self) -> typing.Optional[builtins.str]:
        '''The background color of the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#bg_color ZeroTrustAccessApplication#bg_color}
        '''
        result = self._values.get("bg_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationCorsHeaders"]]]:
        '''cors_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#cors_headers ZeroTrustAccessApplication#cors_headers}
        '''
        result = self._values.get("cors_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationCorsHeaders"]]], result)

    @builtins.property
    def custom_deny_message(self) -> typing.Optional[builtins.str]:
        '''Option that returns a custom error message when a user is denied access to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_message ZeroTrustAccessApplication#custom_deny_message}
        '''
        result = self._values.get("custom_deny_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_deny_url(self) -> typing.Optional[builtins.str]:
        '''Option that redirects to a custom URL when a user is denied access to the application via identity based rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_deny_url ZeroTrustAccessApplication#custom_deny_url}
        '''
        result = self._values.get("custom_deny_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_non_identity_deny_url(self) -> typing.Optional[builtins.str]:
        '''Option that redirects to a custom URL when a user is denied access to the application via non identity rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_non_identity_deny_url ZeroTrustAccessApplication#custom_non_identity_deny_url}
        '''
        result = self._values.get("custom_non_identity_deny_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_pages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The custom pages selected for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_pages ZeroTrustAccessApplication#custom_pages}
        '''
        result = self._values.get("custom_pages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationDestinations"]]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#destinations ZeroTrustAccessApplication#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationDestinations"]]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The primary hostname and path that Access will secure.

        If the app is visible in the App Launcher dashboard, this is the domain that will be displayed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain ZeroTrustAccessApplication#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_type(self) -> typing.Optional[builtins.str]:
        '''The type of the primary domain. Available values: ``public``, ``private``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#domain_type ZeroTrustAccessApplication#domain_type}
        '''
        result = self._values.get("domain_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_binding_cookie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enable_binding_cookie ZeroTrustAccessApplication#enable_binding_cookie}
        '''
        result = self._values.get("enable_binding_cookie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def footer_links(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationFooterLinks"]]]:
        '''footer_links block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#footer_links ZeroTrustAccessApplication#footer_links}
        '''
        result = self._values.get("footer_links")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationFooterLinks"]]], result)

    @builtins.property
    def header_bg_color(self) -> typing.Optional[builtins.str]:
        '''The background color of the header bar in the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#header_bg_color ZeroTrustAccessApplication#header_bg_color}
        '''
        result = self._values.get("header_bg_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_only_cookie_attribute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to add the ``HttpOnly`` cookie flag to access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#http_only_cookie_attribute ZeroTrustAccessApplication#http_only_cookie_attribute}
        '''
        result = self._values.get("http_only_cookie_attribute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#id ZeroTrustAccessApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def landing_page_design(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationLandingPageDesign"]:
        '''landing_page_design block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#landing_page_design ZeroTrustAccessApplication#landing_page_design}
        '''
        result = self._values.get("landing_page_design")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationLandingPageDesign"], result)

    @builtins.property
    def logo_url(self) -> typing.Optional[builtins.str]:
        '''Image URL for the logo shown in the app launcher dashboard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#logo_url ZeroTrustAccessApplication#logo_url}
        '''
        result = self._values.get("logo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Friendly name of the Access Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options_preflight_bypass(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows options preflight requests to bypass Access authentication and go directly to the origin.

        Cannot turn on if cors_headers is set. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#options_preflight_bypass ZeroTrustAccessApplication#options_preflight_bypass}
        '''
        result = self._values.get("options_preflight_bypass")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policies associated with the application, in ascending order of precedence.

        Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#policies ZeroTrustAccessApplication#policies}
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def saas_app(self) -> typing.Optional["ZeroTrustAccessApplicationSaasApp"]:
        '''saas_app block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saas_app ZeroTrustAccessApplication#saas_app}
        '''
        result = self._values.get("saas_app")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationSaasApp"], result)

    @builtins.property
    def same_site_cookie_attribute(self) -> typing.Optional[builtins.str]:
        '''Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#same_site_cookie_attribute ZeroTrustAccessApplication#same_site_cookie_attribute}
        '''
        result = self._values.get("same_site_cookie_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scim_config(self) -> typing.Optional["ZeroTrustAccessApplicationScimConfig"]:
        '''scim_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scim_config ZeroTrustAccessApplication#scim_config}
        '''
        result = self._values.get("scim_config")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationScimConfig"], result)

    @builtins.property
    def self_hosted_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of public domains secured by Access.

        Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#self_hosted_domains ZeroTrustAccessApplication#self_hosted_domains}
        '''
        result = self._values.get("self_hosted_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_auth401_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#service_auth_401_redirect ZeroTrustAccessApplication#service_auth_401_redirect}
        '''
        result = self._values.get("service_auth401_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        '''How often a user will be forced to re-authorise.

        Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#session_duration ZeroTrustAccessApplication#session_duration}
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_app_launcher_login_page(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip the App Launcher landing page. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_app_launcher_login_page ZeroTrustAccessApplication#skip_app_launcher_login_page}
        '''
        result = self._values.get("skip_app_launcher_login_page")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_interstitial(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip the authorization interstitial when using the CLI. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#skip_interstitial ZeroTrustAccessApplication#skip_interstitial}
        '''
        result = self._values.get("skip_interstitial")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The itags associated with the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#tags ZeroTrustAccessApplication#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteria"]]]:
        '''target_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#target_criteria ZeroTrustAccessApplication#target_criteria}
        '''
        result = self._values.get("target_criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteria"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#type ZeroTrustAccessApplication#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. Conflicts with ``account_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#zone_id ZeroTrustAccessApplication#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationCorsHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_headers": "allowAllHeaders",
        "allow_all_methods": "allowAllMethods",
        "allow_all_origins": "allowAllOrigins",
        "allow_credentials": "allowCredentials",
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "max_age": "maxAge",
    },
)
class ZeroTrustAccessApplicationCorsHeaders:
    def __init__(
        self,
        *,
        allow_all_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_all_methods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_all_origins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allow_all_headers: Value to determine whether all HTTP headers are exposed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_headers ZeroTrustAccessApplication#allow_all_headers}
        :param allow_all_methods: Value to determine whether all methods are exposed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_methods ZeroTrustAccessApplication#allow_all_methods}
        :param allow_all_origins: Value to determine whether all origins are permitted to make CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_origins ZeroTrustAccessApplication#allow_all_origins}
        :param allow_credentials: Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_credentials ZeroTrustAccessApplication#allow_credentials}
        :param allowed_headers: List of HTTP headers to expose via CORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_headers ZeroTrustAccessApplication#allowed_headers}
        :param allowed_methods: List of methods to expose via CORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_methods ZeroTrustAccessApplication#allowed_methods}
        :param allowed_origins: List of origins permitted to make CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_origins ZeroTrustAccessApplication#allowed_origins}
        :param max_age: The maximum time a preflight request will be cached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#max_age ZeroTrustAccessApplication#max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570d0baa177c6afcf552d1711ba79b01b6b8b310579c5b73ce48b2f5f08ca83a)
            check_type(argname="argument allow_all_headers", value=allow_all_headers, expected_type=type_hints["allow_all_headers"])
            check_type(argname="argument allow_all_methods", value=allow_all_methods, expected_type=type_hints["allow_all_methods"])
            check_type(argname="argument allow_all_origins", value=allow_all_origins, expected_type=type_hints["allow_all_origins"])
            check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_all_headers is not None:
            self._values["allow_all_headers"] = allow_all_headers
        if allow_all_methods is not None:
            self._values["allow_all_methods"] = allow_all_methods
        if allow_all_origins is not None:
            self._values["allow_all_origins"] = allow_all_origins
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if allowed_origins is not None:
            self._values["allowed_origins"] = allowed_origins
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allow_all_headers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all HTTP headers are exposed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_headers ZeroTrustAccessApplication#allow_all_headers}
        '''
        result = self._values.get("allow_all_headers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_methods(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all methods are exposed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_methods ZeroTrustAccessApplication#allow_all_methods}
        '''
        result = self._values.get("allow_all_methods")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_origins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all origins are permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_all_origins ZeroTrustAccessApplication#allow_all_origins}
        '''
        result = self._values.get("allow_all_origins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_credentials ZeroTrustAccessApplication#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTTP headers to expose via CORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_headers ZeroTrustAccessApplication#allowed_headers}
        '''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of methods to expose via CORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_methods ZeroTrustAccessApplication#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of origins permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allowed_origins ZeroTrustAccessApplication#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''The maximum time a preflight request will be cached.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#max_age ZeroTrustAccessApplication#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationCorsHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationCorsHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationCorsHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf13cefc63d184418962e80cb3cfb68df3da3156635c6ef76de4f9f77ada4962)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationCorsHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406be4d77a37912670f4a00bc058c73b502c2345c3a7d8e34c78a80ef095811b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationCorsHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdb2f560786dfffb916477a05df4eff5c02ad99ccc77be24ef6d710a814d409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__967f6c1ba44f7f1b8d20843833a24962fe9db2ae4840481c84b45a68b5e65223)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2f7e26847c9f75c420600924ab9bef977fa39cf86ff807b7f92ea65c4b3620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationCorsHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationCorsHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationCorsHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ba2fa0abc6852573fa9953b32ac42d7f6a72e93dc3f9f0d91765701b67e8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationCorsHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationCorsHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fcf1fe95da2b6031991ead48569fbb9ff00b03afd00e3214e3d20386a992210)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowAllHeaders")
    def reset_allow_all_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllHeaders", []))

    @jsii.member(jsii_name="resetAllowAllMethods")
    def reset_allow_all_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllMethods", []))

    @jsii.member(jsii_name="resetAllowAllOrigins")
    def reset_allow_all_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAllOrigins", []))

    @jsii.member(jsii_name="resetAllowCredentials")
    def reset_allow_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCredentials", []))

    @jsii.member(jsii_name="resetAllowedHeaders")
    def reset_allowed_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHeaders", []))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetAllowedOrigins")
    def reset_allowed_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedOrigins", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @builtins.property
    @jsii.member(jsii_name="allowAllHeadersInput")
    def allow_all_headers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllMethodsInput")
    def allow_all_methods_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllOriginsInput")
    def allow_all_origins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAllOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsInput")
    def allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAllHeaders")
    def allow_all_headers(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllHeaders"))

    @allow_all_headers.setter
    def allow_all_headers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d0a09ee60d1b08c6963232e100c6ceaaede5c0ef39009732582d935fc1e905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowAllMethods")
    def allow_all_methods(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllMethods"))

    @allow_all_methods.setter
    def allow_all_methods(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d135a36b855dfbbbf40a911ff12cf0577ed83002a7a7cee84aa8c13c23cb8f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowAllOrigins")
    def allow_all_origins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAllOrigins"))

    @allow_all_origins.setter
    def allow_all_origins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c840a4753ace2f1e243c60b9916c5df15c9d7246abf3c6895676d0a316420c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAllOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowCredentials")
    def allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCredentials"))

    @allow_credentials.setter
    def allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8009166033a2928de4ebc21edad17423ddc0e0deebedab0af8c4dfc5fb83381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082f53f30671b16288afc1a9ad26c542a9b393e4541acc8b87918982ce0310ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef529e72178495b6c43ebe1f695b2cae1293867b0f0c9fff9215f1082c95435a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933b2162a14fe720dc097500c299b6154310fffaa61cea5569bb901b681e85b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca16c2a986f7382e78a17fb496bd86538fd3ee1d9a8475ec1ff814259a785797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationCorsHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationCorsHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationCorsHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad0e91b7680ac85eae84c174e10132dc780ef53bf867a5ccffdfc73790cd36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationDestinations",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "type": "type"},
)
class ZeroTrustAccessApplicationDestinations:
    def __init__(
        self,
        *,
        uri: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the destination. Public destinations can include a domain and path with wildcards. Private destinations are an early access feature and gated behind a feature flag. Private destinations support private IPv4, IPv6, and Server Name Indications (SNI) with optional port ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#uri ZeroTrustAccessApplication#uri}
        :param type: The destination type. Available values: ``public``, ``private``. Defaults to ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#type ZeroTrustAccessApplication#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb53f29245a8f4afef45363f780ecbc61eec9157bc84ce5d2838e235e17fc873)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def uri(self) -> builtins.str:
        '''The URI of the destination.

        Public destinations can include a domain and path with wildcards. Private destinations are an early access feature and gated behind a feature flag. Private destinations support private IPv4, IPv6, and Server Name Indications (SNI) with optional port ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#uri ZeroTrustAccessApplication#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The destination type. Available values: ``public``, ``private``. Defaults to ``public``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#type ZeroTrustAccessApplication#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8168d79a8693c9a4e11c3b5ac3ec9eba59f7a61ff41ef15d1510416071392301)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb9842149a5ba31f0c7bb7a4bc2efc080e3f3c9bf4f718ec8bbd9987bf4badc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c416ede1a70be4b7cef8f1721172a05250854cca34377c9007f895313c8fbaa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbbb8d8255fcf87cb4069296b24e7fdb52c6606b44ac92d6c62f69fcca0ddb3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23f4dd46e14736abe9c77407eda1be11e2e0e38d575e78aea951685bc2c365dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22c25c82c26ed7b257b2d03476a3fbd8bb5dd8bab445155b2691eb44afde5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad05bb67450b8cea2997f05d67e7950ddb7245da376758e1e76342421594589)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3f7e0e5261b28be35a0e20320948333c43ca52eec412f6d1ab534347d28b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642515c81cebe22a173f73f35c34adb39b6ef57f7f0a66229da0ebaf09d59131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4905a20cb306991e008eaa738934cdef4f96e362a5886068f6f65d016dd335f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationFooterLinks",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class ZeroTrustAccessApplicationFooterLinks:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the footer link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param url: The URL of the footer link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#url ZeroTrustAccessApplication#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33de202b3d83c54564f055486a5738ad842797dede2aa86d887444a9647d0ff)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the footer link.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL of the footer link.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#url ZeroTrustAccessApplication#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationFooterLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationFooterLinksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationFooterLinksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ce73644e02d48e6eb68a59282e83ae003bd1ced90461a5197c95a65e17da3d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationFooterLinksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf2e1a33ba6a3d6ec819c36230d12610454e30c60a713b341411d823ba23192)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationFooterLinksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e51e2383e0ec4f8292d683b26b6b451e152ad08ddd5747991e2b6d0d4e4924)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c62edec9276ba061132ebfc6eb52acd5e6ab14a44cf072735b27a81bc4debbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e4c4c388a572055d945d7eede9097569a3ea099aaaad53f249b82ede4ac509c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationFooterLinks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationFooterLinks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationFooterLinks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bc629578b246ab1a8885978399933d192377d2ba319a4f0ec7757ef9614f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationFooterLinksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationFooterLinksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d21bc58a76579810293c6ae93bcda284e56e65f8c609faaeed6b3ca3b2aa86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a6aea00285b792ec70c175c5fae0a1a784246695e5eb80558a8a979b66d634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9137cb5922c257b75cacc27a6774aad64820e641abcc311e7064f16d43af3060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationFooterLinks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationFooterLinks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationFooterLinks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e32afdbdbe0dee00528ada5be0b893b76024e13f0273e8adeff1fc2019313703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationLandingPageDesign",
    jsii_struct_bases=[],
    name_mapping={
        "button_color": "buttonColor",
        "button_text_color": "buttonTextColor",
        "image_url": "imageUrl",
        "message": "message",
        "title": "title",
    },
)
class ZeroTrustAccessApplicationLandingPageDesign:
    def __init__(
        self,
        *,
        button_color: typing.Optional[builtins.str] = None,
        button_text_color: typing.Optional[builtins.str] = None,
        image_url: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param button_color: The button color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_color ZeroTrustAccessApplication#button_color}
        :param button_text_color: The button text color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_text_color ZeroTrustAccessApplication#button_text_color}
        :param image_url: The URL of the image to be displayed in the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#image_url ZeroTrustAccessApplication#image_url}
        :param message: The message of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#message ZeroTrustAccessApplication#message}
        :param title: The title of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#title ZeroTrustAccessApplication#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8926bc90faf274b6c685bf7e4c7c54a0f88e4ee4cf30cf581bdcd7feb90d772e)
            check_type(argname="argument button_color", value=button_color, expected_type=type_hints["button_color"])
            check_type(argname="argument button_text_color", value=button_text_color, expected_type=type_hints["button_text_color"])
            check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if button_color is not None:
            self._values["button_color"] = button_color
        if button_text_color is not None:
            self._values["button_text_color"] = button_text_color
        if image_url is not None:
            self._values["image_url"] = image_url
        if message is not None:
            self._values["message"] = message
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def button_color(self) -> typing.Optional[builtins.str]:
        '''The button color of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_color ZeroTrustAccessApplication#button_color}
        '''
        result = self._values.get("button_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def button_text_color(self) -> typing.Optional[builtins.str]:
        '''The button text color of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#button_text_color ZeroTrustAccessApplication#button_text_color}
        '''
        result = self._values.get("button_text_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the image to be displayed in the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#image_url ZeroTrustAccessApplication#image_url}
        '''
        result = self._values.get("image_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''The message of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#message ZeroTrustAccessApplication#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''The title of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#title ZeroTrustAccessApplication#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationLandingPageDesign(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationLandingPageDesignOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationLandingPageDesignOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__469f1fb2458e3a0a89654ebf80a766ab780607f746e831ffede7d84c08f114c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetButtonColor")
    def reset_button_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetButtonColor", []))

    @jsii.member(jsii_name="resetButtonTextColor")
    def reset_button_text_color(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetButtonTextColor", []))

    @jsii.member(jsii_name="resetImageUrl")
    def reset_image_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUrl", []))

    @jsii.member(jsii_name="resetMessage")
    def reset_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessage", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="buttonColorInput")
    def button_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buttonColorInput"))

    @builtins.property
    @jsii.member(jsii_name="buttonTextColorInput")
    def button_text_color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buttonTextColorInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUrlInput")
    def image_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="messageInput")
    def message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="buttonColor")
    def button_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buttonColor"))

    @button_color.setter
    def button_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b6c4ec3f0d549f31041f7cffde66753d6dd27e2c8402c72ae14d81be888644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buttonColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buttonTextColor")
    def button_text_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buttonTextColor"))

    @button_text_color.setter
    def button_text_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb3e7b45304465a72f40624ad5f08515f2fc0e3094853ae561807b34af88af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buttonTextColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUrl")
    def image_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUrl"))

    @image_url.setter
    def image_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4a91aee042f486c785ac2b6ec48e8a41bb11997c1cc07c7e40daafea05495d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b631466d7f511cd30ae0b7ee0fd957a686eb7d41596b8b527d6dfffc112b7994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5658ce331fa05e1720564dc64cad97c9859e052f5db692bd7949bb1bfda86ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationLandingPageDesign]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationLandingPageDesign], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationLandingPageDesign],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44de85cfb941b73aa477ef6a25f8ff6ec66c03a22228165cede093b7715b5a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasApp",
    jsii_struct_bases=[],
    name_mapping={
        "access_token_lifetime": "accessTokenLifetime",
        "allow_pkce_without_client_secret": "allowPkceWithoutClientSecret",
        "app_launcher_url": "appLauncherUrl",
        "auth_type": "authType",
        "consumer_service_url": "consumerServiceUrl",
        "custom_attribute": "customAttribute",
        "custom_claim": "customClaim",
        "default_relay_state": "defaultRelayState",
        "grant_types": "grantTypes",
        "group_filter_regex": "groupFilterRegex",
        "hybrid_and_implicit_options": "hybridAndImplicitOptions",
        "name_id_format": "nameIdFormat",
        "name_id_transform_jsonata": "nameIdTransformJsonata",
        "redirect_uris": "redirectUris",
        "refresh_token_options": "refreshTokenOptions",
        "saml_attribute_transform_jsonata": "samlAttributeTransformJsonata",
        "scopes": "scopes",
        "sp_entity_id": "spEntityId",
    },
)
class ZeroTrustAccessApplicationSaasApp:
    def __init__(
        self,
        *,
        access_token_lifetime: typing.Optional[builtins.str] = None,
        allow_pkce_without_client_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        app_launcher_url: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        consumer_service_url: typing.Optional[builtins.str] = None,
        custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppCustomAttribute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppCustomClaim", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_filter_regex: typing.Optional[builtins.str] = None,
        hybrid_and_implicit_options: typing.Optional[typing.Union["ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_id_format: typing.Optional[builtins.str] = None,
        name_id_transform_jsonata: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token_lifetime: The lifetime of the Access Token after creation. Valid units are ``m`` and ``h``. Must be greater than or equal to 1m and less than or equal to 24h. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#access_token_lifetime ZeroTrustAccessApplication#access_token_lifetime}
        :param allow_pkce_without_client_secret: Allow PKCE flow without a client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_pkce_without_client_secret ZeroTrustAccessApplication#allow_pkce_without_client_secret}
        :param app_launcher_url: The URL where this applications tile redirects users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_url ZeroTrustAccessApplication#app_launcher_url}
        :param auth_type: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auth_type ZeroTrustAccessApplication#auth_type}
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#consumer_service_url ZeroTrustAccessApplication#consumer_service_url}
        :param custom_attribute: custom_attribute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_attribute ZeroTrustAccessApplication#custom_attribute}
        :param custom_claim: custom_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_claim ZeroTrustAccessApplication#custom_claim}
        :param default_relay_state: The relay state used if not provided by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#default_relay_state ZeroTrustAccessApplication#default_relay_state}
        :param grant_types: The OIDC flows supported by this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#grant_types ZeroTrustAccessApplication#grant_types}
        :param group_filter_regex: A regex to filter Cloudflare groups returned in ID token and userinfo endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#group_filter_regex ZeroTrustAccessApplication#group_filter_regex}
        :param hybrid_and_implicit_options: hybrid_and_implicit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#hybrid_and_implicit_options ZeroTrustAccessApplication#hybrid_and_implicit_options}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_format ZeroTrustAccessApplication#name_id_format}
        :param name_id_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_transform_jsonata ZeroTrustAccessApplication#name_id_transform_jsonata}
        :param redirect_uris: The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#redirect_uris ZeroTrustAccessApplication#redirect_uris}
        :param refresh_token_options: refresh_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#refresh_token_options ZeroTrustAccessApplication#refresh_token_options}
        :param saml_attribute_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saml_attribute_transform_jsonata ZeroTrustAccessApplication#saml_attribute_transform_jsonata}
        :param scopes: Define the user information shared with access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#sp_entity_id ZeroTrustAccessApplication#sp_entity_id}
        '''
        if isinstance(hybrid_and_implicit_options, dict):
            hybrid_and_implicit_options = ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions(**hybrid_and_implicit_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba771b6654419f66e79dfb8d9609f915a6d90c1b92895f9d8bcbc1ad4e696d75)
            check_type(argname="argument access_token_lifetime", value=access_token_lifetime, expected_type=type_hints["access_token_lifetime"])
            check_type(argname="argument allow_pkce_without_client_secret", value=allow_pkce_without_client_secret, expected_type=type_hints["allow_pkce_without_client_secret"])
            check_type(argname="argument app_launcher_url", value=app_launcher_url, expected_type=type_hints["app_launcher_url"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument consumer_service_url", value=consumer_service_url, expected_type=type_hints["consumer_service_url"])
            check_type(argname="argument custom_attribute", value=custom_attribute, expected_type=type_hints["custom_attribute"])
            check_type(argname="argument custom_claim", value=custom_claim, expected_type=type_hints["custom_claim"])
            check_type(argname="argument default_relay_state", value=default_relay_state, expected_type=type_hints["default_relay_state"])
            check_type(argname="argument grant_types", value=grant_types, expected_type=type_hints["grant_types"])
            check_type(argname="argument group_filter_regex", value=group_filter_regex, expected_type=type_hints["group_filter_regex"])
            check_type(argname="argument hybrid_and_implicit_options", value=hybrid_and_implicit_options, expected_type=type_hints["hybrid_and_implicit_options"])
            check_type(argname="argument name_id_format", value=name_id_format, expected_type=type_hints["name_id_format"])
            check_type(argname="argument name_id_transform_jsonata", value=name_id_transform_jsonata, expected_type=type_hints["name_id_transform_jsonata"])
            check_type(argname="argument redirect_uris", value=redirect_uris, expected_type=type_hints["redirect_uris"])
            check_type(argname="argument refresh_token_options", value=refresh_token_options, expected_type=type_hints["refresh_token_options"])
            check_type(argname="argument saml_attribute_transform_jsonata", value=saml_attribute_transform_jsonata, expected_type=type_hints["saml_attribute_transform_jsonata"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument sp_entity_id", value=sp_entity_id, expected_type=type_hints["sp_entity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token_lifetime is not None:
            self._values["access_token_lifetime"] = access_token_lifetime
        if allow_pkce_without_client_secret is not None:
            self._values["allow_pkce_without_client_secret"] = allow_pkce_without_client_secret
        if app_launcher_url is not None:
            self._values["app_launcher_url"] = app_launcher_url
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if consumer_service_url is not None:
            self._values["consumer_service_url"] = consumer_service_url
        if custom_attribute is not None:
            self._values["custom_attribute"] = custom_attribute
        if custom_claim is not None:
            self._values["custom_claim"] = custom_claim
        if default_relay_state is not None:
            self._values["default_relay_state"] = default_relay_state
        if grant_types is not None:
            self._values["grant_types"] = grant_types
        if group_filter_regex is not None:
            self._values["group_filter_regex"] = group_filter_regex
        if hybrid_and_implicit_options is not None:
            self._values["hybrid_and_implicit_options"] = hybrid_and_implicit_options
        if name_id_format is not None:
            self._values["name_id_format"] = name_id_format
        if name_id_transform_jsonata is not None:
            self._values["name_id_transform_jsonata"] = name_id_transform_jsonata
        if redirect_uris is not None:
            self._values["redirect_uris"] = redirect_uris
        if refresh_token_options is not None:
            self._values["refresh_token_options"] = refresh_token_options
        if saml_attribute_transform_jsonata is not None:
            self._values["saml_attribute_transform_jsonata"] = saml_attribute_transform_jsonata
        if scopes is not None:
            self._values["scopes"] = scopes
        if sp_entity_id is not None:
            self._values["sp_entity_id"] = sp_entity_id

    @builtins.property
    def access_token_lifetime(self) -> typing.Optional[builtins.str]:
        '''The lifetime of the Access Token after creation.

        Valid units are ``m`` and ``h``. Must be greater than or equal to 1m and less than or equal to 24h.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#access_token_lifetime ZeroTrustAccessApplication#access_token_lifetime}
        '''
        result = self._values.get("access_token_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_pkce_without_client_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow PKCE flow without a client secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#allow_pkce_without_client_secret ZeroTrustAccessApplication#allow_pkce_without_client_secret}
        '''
        result = self._values.get("allow_pkce_without_client_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def app_launcher_url(self) -> typing.Optional[builtins.str]:
        '''The URL where this applications tile redirects users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#app_launcher_url ZeroTrustAccessApplication#app_launcher_url}
        '''
        result = self._values.get("app_launcher_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''**Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#auth_type ZeroTrustAccessApplication#auth_type}
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_service_url(self) -> typing.Optional[builtins.str]:
        '''The service provider's endpoint that is responsible for receiving and parsing a SAML assertion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#consumer_service_url ZeroTrustAccessApplication#consumer_service_url}
        '''
        result = self._values.get("consumer_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_attribute(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppCustomAttribute"]]]:
        '''custom_attribute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_attribute ZeroTrustAccessApplication#custom_attribute}
        '''
        result = self._values.get("custom_attribute")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppCustomAttribute"]]], result)

    @builtins.property
    def custom_claim(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppCustomClaim"]]]:
        '''custom_claim block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#custom_claim ZeroTrustAccessApplication#custom_claim}
        '''
        result = self._values.get("custom_claim")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppCustomClaim"]]], result)

    @builtins.property
    def default_relay_state(self) -> typing.Optional[builtins.str]:
        '''The relay state used if not provided by the identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#default_relay_state ZeroTrustAccessApplication#default_relay_state}
        '''
        result = self._values.get("default_relay_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OIDC flows supported by this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#grant_types ZeroTrustAccessApplication#grant_types}
        '''
        result = self._values.get("grant_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_filter_regex(self) -> typing.Optional[builtins.str]:
        '''A regex to filter Cloudflare groups returned in ID token and userinfo endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#group_filter_regex ZeroTrustAccessApplication#group_filter_regex}
        '''
        result = self._values.get("group_filter_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hybrid_and_implicit_options(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions"]:
        '''hybrid_and_implicit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#hybrid_and_implicit_options ZeroTrustAccessApplication#hybrid_and_implicit_options}
        '''
        result = self._values.get("hybrid_and_implicit_options")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions"], result)

    @builtins.property
    def name_id_format(self) -> typing.Optional[builtins.str]:
        '''The format of the name identifier sent to the SaaS application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_format ZeroTrustAccessApplication#name_id_format}
        '''
        result = self._values.get("name_id_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_id_transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_id_transform_jsonata ZeroTrustAccessApplication#name_id_transform_jsonata}
        '''
        result = self._values.get("name_id_transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#redirect_uris ZeroTrustAccessApplication#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def refresh_token_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions"]]]:
        '''refresh_token_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#refresh_token_options ZeroTrustAccessApplication#refresh_token_options}
        '''
        result = self._values.get("refresh_token_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions"]]], result)

    @builtins.property
    def saml_attribute_transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#saml_attribute_transform_jsonata ZeroTrustAccessApplication#saml_attribute_transform_jsonata}
        '''
        result = self._values.get("saml_attribute_transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Define the user information shared with access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sp_entity_id(self) -> typing.Optional[builtins.str]:
        '''A globally unique name for an identity or service provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#sp_entity_id ZeroTrustAccessApplication#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasApp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomAttribute",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "friendly_name": "friendlyName",
        "name": "name",
        "name_format": "nameFormat",
        "required": "required",
    },
)
class ZeroTrustAccessApplicationSaasAppCustomAttribute:
    def __init__(
        self,
        *,
        source: typing.Union["ZeroTrustAccessApplicationSaasAppCustomAttributeSource", typing.Dict[builtins.str, typing.Any]],
        friendly_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_format: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#source ZeroTrustAccessApplication#source}
        :param friendly_name: A friendly name for the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#friendly_name ZeroTrustAccessApplication#friendly_name}
        :param name: The name of the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param name_format: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_format ZeroTrustAccessApplication#name_format}
        :param required: True if the attribute must be always present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#required ZeroTrustAccessApplication#required}
        '''
        if isinstance(source, dict):
            source = ZeroTrustAccessApplicationSaasAppCustomAttributeSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf05ee29e111b33731279ab5ef58e817e34b5ec435a0b1dd9d62ef19badb94a6)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_format", value=name_format, expected_type=type_hints["name_format"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if name is not None:
            self._values["name"] = name
        if name_format is not None:
            self._values["name_format"] = name_format
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def source(self) -> "ZeroTrustAccessApplicationSaasAppCustomAttributeSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#source ZeroTrustAccessApplication#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomAttributeSource", result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#friendly_name ZeroTrustAccessApplication#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_format(self) -> typing.Optional[builtins.str]:
        '''A globally unique name for an identity or service provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_format ZeroTrustAccessApplication#name_format}
        '''
        result = self._values.get("name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the attribute must be always present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#required ZeroTrustAccessApplication#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppCustomAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppCustomAttributeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomAttributeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17e2644177328088014db085e14157d3c422c994b899e004f580462ed061b3d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationSaasAppCustomAttributeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7f6c29499c30ccde95a5997eff773874d08cde65f07d966334474f2224f618)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomAttributeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce299c0ceeb006c89984893802d4ac5a3ce90fb81772a0909f91c9136139f89d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b08292be7e04d762a84f3cb3d278b42f1d4c7f09ed896e20accef17984636d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c54b834d0dbf6bd8a788a26ac0aa8853781987041a3d41b6a6733fb389adbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd17fd91e2de880819e5ff7cfb6a02a358081329e7d28474325c556a158bf82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationSaasAppCustomAttributeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomAttributeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07b3ab3ef91af0eb639dccf4246e3a55148a67a8d146027f2f94c43153ad1473)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        value = ZeroTrustAccessApplicationSaasAppCustomAttributeSource(
            name=name, name_by_idp=name_by_idp
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNameFormat")
    def reset_name_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameFormat", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "ZeroTrustAccessApplicationSaasAppCustomAttributeSourceOutputReference":
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomAttributeSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameFormatInput")
    def name_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationSaasAppCustomAttributeSource"]:
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationSaasAppCustomAttributeSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a567c8ea5c5cba33f8611571bc706569e7611d9ab794d245f3dd165decda70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb3b2db980949b725986de7ebf250d75f42671e63eedec96d56d6164c6af2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameFormat")
    def name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameFormat"))

    @name_format.setter
    def name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08f90628b302dce3ca0a3c708fcebc2bf3e949c321033863c67565036d26dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameFormat", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__a0602b1b05666f2db6e2ab331770576ec023a8e47d63168fe26f9837a7088939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomAttribute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomAttribute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomAttribute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052dfd00c6ade1eeb55e57fcd51d82da154ae4eb7a8fb864bc51306842c03f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomAttributeSource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "name_by_idp": "nameByIdp"},
)
class ZeroTrustAccessApplicationSaasAppCustomAttributeSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27123a84c1e01a6f939d33a0493df6d916c8deb15e81e737606b6f56650e23be)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_by_idp", value=name_by_idp, expected_type=type_hints["name_by_idp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if name_by_idp is not None:
            self._values["name_by_idp"] = name_by_idp

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute as provided by the IDP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_by_idp(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping from IdP ID to claim name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        result = self._values.get("name_by_idp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppCustomAttributeSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppCustomAttributeSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomAttributeSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__719f21aff281a27145dc4c3a121e273ecba3e0c06a0aa0fc35ce8f089aae5c85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNameByIdp")
    def reset_name_by_idp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameByIdp", []))

    @builtins.property
    @jsii.member(jsii_name="nameByIdpInput")
    def name_by_idp_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nameByIdpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38062080c8058b9b7814a726edd28686bc7e2cad43d5329995738a2360d52785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameByIdp")
    def name_by_idp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nameByIdp"))

    @name_by_idp.setter
    def name_by_idp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab88eacfa80c31a18010857bfbe5e7242f027bd140ae9df652986420f4aa4458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameByIdp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationSaasAppCustomAttributeSource]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationSaasAppCustomAttributeSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationSaasAppCustomAttributeSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8911c574a947e5998ec86d1d3bca407dc4a7afefdcd3a7262f43eed3228e2a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomClaim",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "name": "name",
        "required": "required",
        "scope": "scope",
    },
)
class ZeroTrustAccessApplicationSaasAppCustomClaim:
    def __init__(
        self,
        *,
        source: typing.Union["ZeroTrustAccessApplicationSaasAppCustomClaimSource", typing.Dict[builtins.str, typing.Any]],
        name: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#source ZeroTrustAccessApplication#source}
        :param name: The name of the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param required: True if the attribute must be always present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#required ZeroTrustAccessApplication#required}
        :param scope: The scope of the claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scope ZeroTrustAccessApplication#scope}
        '''
        if isinstance(source, dict):
            source = ZeroTrustAccessApplicationSaasAppCustomClaimSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4846e51f54a8de0a208da2a437855cac3ca0a20eb8ad16b6e7d59da668d204)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if name is not None:
            self._values["name"] = name
        if required is not None:
            self._values["required"] = required
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def source(self) -> "ZeroTrustAccessApplicationSaasAppCustomClaimSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#source ZeroTrustAccessApplication#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomClaimSource", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the attribute must be always present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#required ZeroTrustAccessApplication#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of the claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scope ZeroTrustAccessApplication#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppCustomClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppCustomClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d86f4d51f9aefcf4172adc470a8faaad0a6e10d3f5ab586d7939a3387f9fe21f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationSaasAppCustomClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059c90605c39da13ab7e429a86f160381ad6d6846dc2cbdad676a37231bc3ee2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbc76d1338868392a25c58cd1277f8c92337640ca8820a1b6b6c5f4cbde8953)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4eeac1b0cc37966c452fe568d1011229238c63ff039e22c42dab68ff763fc7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86244a8d790c9686daaccc1003c61fbc89ef63e16794f3208b7ef7447871e486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1669a5e10f1b79e87bd5b9069fdffe0d01ddb863b6521d2668fd99a9212b4f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationSaasAppCustomClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbab7b7221be9547277233fee27d2d2de3c5f8ac45d9dd007a4785c8c126bfad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        value = ZeroTrustAccessApplicationSaasAppCustomClaimSource(
            name=name, name_by_idp=name_by_idp
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "ZeroTrustAccessApplicationSaasAppCustomClaimSourceOutputReference":
        return typing.cast("ZeroTrustAccessApplicationSaasAppCustomClaimSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationSaasAppCustomClaimSource"]:
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationSaasAppCustomClaimSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3d15c80a11204c22a7a278ce34b09742edd61b3a8f63a6a29630b5212af723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4c377732c1d05abf30fbe21dc6a691c03c58e845060ceb75ec0c54e81b5ba59a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f5e1707532fe467fd693f50da16d9220b168ca03e4a3ac3cb6a6069ea7a8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomClaim]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomClaim]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomClaim]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053f0f67cf42cb806adee0e8822493b0981a92e0fad74c99b030f18a8215048d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomClaimSource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "name_by_idp": "nameByIdp"},
)
class ZeroTrustAccessApplicationSaasAppCustomClaimSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de088843a77bee0081b4d7e0f5e848857ca9e320eb10a16d14d5c55a5d3bacf3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_by_idp", value=name_by_idp, expected_type=type_hints["name_by_idp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if name_by_idp is not None:
            self._values["name_by_idp"] = name_by_idp

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute as provided by the IDP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_by_idp(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping from IdP ID to claim name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name_by_idp ZeroTrustAccessApplication#name_by_idp}
        '''
        result = self._values.get("name_by_idp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppCustomClaimSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppCustomClaimSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppCustomClaimSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5194d214b1b10213dae1aa60d0aaa786adfa9cf7c54bac50677be3b2182cd15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNameByIdp")
    def reset_name_by_idp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameByIdp", []))

    @builtins.property
    @jsii.member(jsii_name="nameByIdpInput")
    def name_by_idp_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "nameByIdpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b84eb1bb627ebedc2c641131f20028ba92d3370fd59d24e39ba397db26fab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameByIdp")
    def name_by_idp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nameByIdp"))

    @name_by_idp.setter
    def name_by_idp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddeae9558a43c8cced66195ffeb972db93b0dfeecf6d1e4f4de52edddc84c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameByIdp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationSaasAppCustomClaimSource]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationSaasAppCustomClaimSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationSaasAppCustomClaimSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f04cea13199de29ca7312a0688d53cf49e7ceb7dbe119ab6510c1e2c9c6797d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "return_access_token_from_authorization_endpoint": "returnAccessTokenFromAuthorizationEndpoint",
        "return_id_token_from_authorization_endpoint": "returnIdTokenFromAuthorizationEndpoint",
    },
)
class ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions:
    def __init__(
        self,
        *,
        return_access_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        return_id_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param return_access_token_from_authorization_endpoint: If true, the authorization endpoint will return an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_access_token_from_authorization_endpoint ZeroTrustAccessApplication#return_access_token_from_authorization_endpoint}
        :param return_id_token_from_authorization_endpoint: If true, the authorization endpoint will return an id token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_id_token_from_authorization_endpoint ZeroTrustAccessApplication#return_id_token_from_authorization_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47ae571f696461fa530e0b47d1efc7aaf34c0de513625409293c9d3e6bab9f3)
            check_type(argname="argument return_access_token_from_authorization_endpoint", value=return_access_token_from_authorization_endpoint, expected_type=type_hints["return_access_token_from_authorization_endpoint"])
            check_type(argname="argument return_id_token_from_authorization_endpoint", value=return_id_token_from_authorization_endpoint, expected_type=type_hints["return_id_token_from_authorization_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if return_access_token_from_authorization_endpoint is not None:
            self._values["return_access_token_from_authorization_endpoint"] = return_access_token_from_authorization_endpoint
        if return_id_token_from_authorization_endpoint is not None:
            self._values["return_id_token_from_authorization_endpoint"] = return_id_token_from_authorization_endpoint

    @builtins.property
    def return_access_token_from_authorization_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the authorization endpoint will return an access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_access_token_from_authorization_endpoint ZeroTrustAccessApplication#return_access_token_from_authorization_endpoint}
        '''
        result = self._values.get("return_access_token_from_authorization_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def return_id_token_from_authorization_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the authorization endpoint will return an id token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_id_token_from_authorization_endpoint ZeroTrustAccessApplication#return_id_token_from_authorization_endpoint}
        '''
        result = self._values.get("return_id_token_from_authorization_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a23c8631a7e3ced1913740badd25b182d8e96d450b36a5e36990ed6998cb39f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReturnAccessTokenFromAuthorizationEndpoint")
    def reset_return_access_token_from_authorization_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnAccessTokenFromAuthorizationEndpoint", []))

    @jsii.member(jsii_name="resetReturnIdTokenFromAuthorizationEndpoint")
    def reset_return_id_token_from_authorization_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnIdTokenFromAuthorizationEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="returnAccessTokenFromAuthorizationEndpointInput")
    def return_access_token_from_authorization_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "returnAccessTokenFromAuthorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="returnIdTokenFromAuthorizationEndpointInput")
    def return_id_token_from_authorization_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "returnIdTokenFromAuthorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="returnAccessTokenFromAuthorizationEndpoint")
    def return_access_token_from_authorization_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "returnAccessTokenFromAuthorizationEndpoint"))

    @return_access_token_from_authorization_endpoint.setter
    def return_access_token_from_authorization_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef48dd0a1ce07f0e0b2c393cc41e88e4a85a50ad9de47aaaddfb48813152bd08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnAccessTokenFromAuthorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnIdTokenFromAuthorizationEndpoint")
    def return_id_token_from_authorization_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "returnIdTokenFromAuthorizationEndpoint"))

    @return_id_token_from_authorization_endpoint.setter
    def return_id_token_from_authorization_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260a94b192ac278986ffa721cb0b4f3ff84c8bc3d6fdea12710e86b6eaaef709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnIdTokenFromAuthorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56656c00569825803da3de6dcf7b591d4680f70dacf3bf0817373f6058bac6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationSaasAppOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a299894c97079b51266055689b9e4f413f7ec554eaa28304f60d4ad33f8534)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomAttribute")
    def put_custom_attribute(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b50850d7ccea4a709ce1bb6660a8e6e5417f6c414de9dfbcfdf6d532f99eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomAttribute", [value]))

    @jsii.member(jsii_name="putCustomClaim")
    def put_custom_claim(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7ab4a71b08357c4ca937bd7fac3142284beded6fb7ccea5473428054cd3867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomClaim", [value]))

    @jsii.member(jsii_name="putHybridAndImplicitOptions")
    def put_hybrid_and_implicit_options(
        self,
        *,
        return_access_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        return_id_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param return_access_token_from_authorization_endpoint: If true, the authorization endpoint will return an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_access_token_from_authorization_endpoint ZeroTrustAccessApplication#return_access_token_from_authorization_endpoint}
        :param return_id_token_from_authorization_endpoint: If true, the authorization endpoint will return an id token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#return_id_token_from_authorization_endpoint ZeroTrustAccessApplication#return_id_token_from_authorization_endpoint}
        '''
        value = ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions(
            return_access_token_from_authorization_endpoint=return_access_token_from_authorization_endpoint,
            return_id_token_from_authorization_endpoint=return_id_token_from_authorization_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putHybridAndImplicitOptions", [value]))

    @jsii.member(jsii_name="putRefreshTokenOptions")
    def put_refresh_token_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05d9069f697f1fad08e514498ad4220505e56b347bbd9357dd86f625f57f4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRefreshTokenOptions", [value]))

    @jsii.member(jsii_name="resetAccessTokenLifetime")
    def reset_access_token_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenLifetime", []))

    @jsii.member(jsii_name="resetAllowPkceWithoutClientSecret")
    def reset_allow_pkce_without_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowPkceWithoutClientSecret", []))

    @jsii.member(jsii_name="resetAppLauncherUrl")
    def reset_app_launcher_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppLauncherUrl", []))

    @jsii.member(jsii_name="resetAuthType")
    def reset_auth_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthType", []))

    @jsii.member(jsii_name="resetConsumerServiceUrl")
    def reset_consumer_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerServiceUrl", []))

    @jsii.member(jsii_name="resetCustomAttribute")
    def reset_custom_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAttribute", []))

    @jsii.member(jsii_name="resetCustomClaim")
    def reset_custom_claim(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomClaim", []))

    @jsii.member(jsii_name="resetDefaultRelayState")
    def reset_default_relay_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRelayState", []))

    @jsii.member(jsii_name="resetGrantTypes")
    def reset_grant_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrantTypes", []))

    @jsii.member(jsii_name="resetGroupFilterRegex")
    def reset_group_filter_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupFilterRegex", []))

    @jsii.member(jsii_name="resetHybridAndImplicitOptions")
    def reset_hybrid_and_implicit_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHybridAndImplicitOptions", []))

    @jsii.member(jsii_name="resetNameIdFormat")
    def reset_name_id_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameIdFormat", []))

    @jsii.member(jsii_name="resetNameIdTransformJsonata")
    def reset_name_id_transform_jsonata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameIdTransformJsonata", []))

    @jsii.member(jsii_name="resetRedirectUris")
    def reset_redirect_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectUris", []))

    @jsii.member(jsii_name="resetRefreshTokenOptions")
    def reset_refresh_token_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshTokenOptions", []))

    @jsii.member(jsii_name="resetSamlAttributeTransformJsonata")
    def reset_saml_attribute_transform_jsonata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlAttributeTransformJsonata", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSpEntityId")
    def reset_sp_entity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpEntityId", []))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="customAttribute")
    def custom_attribute(self) -> ZeroTrustAccessApplicationSaasAppCustomAttributeList:
        return typing.cast(ZeroTrustAccessApplicationSaasAppCustomAttributeList, jsii.get(self, "customAttribute"))

    @builtins.property
    @jsii.member(jsii_name="customClaim")
    def custom_claim(self) -> ZeroTrustAccessApplicationSaasAppCustomClaimList:
        return typing.cast(ZeroTrustAccessApplicationSaasAppCustomClaimList, jsii.get(self, "customClaim"))

    @builtins.property
    @jsii.member(jsii_name="hybridAndImplicitOptions")
    def hybrid_and_implicit_options(
        self,
    ) -> ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptionsOutputReference:
        return typing.cast(ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptionsOutputReference, jsii.get(self, "hybridAndImplicitOptions"))

    @builtins.property
    @jsii.member(jsii_name="idpEntityId")
    def idp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpEntityId"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenOptions")
    def refresh_token_options(
        self,
    ) -> "ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsList":
        return typing.cast("ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsList", jsii.get(self, "refreshTokenOptions"))

    @builtins.property
    @jsii.member(jsii_name="ssoEndpoint")
    def sso_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenLifetimeInput")
    def access_token_lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowPkceWithoutClientSecretInput")
    def allow_pkce_without_client_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowPkceWithoutClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="appLauncherUrlInput")
    def app_launcher_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appLauncherUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerServiceUrlInput")
    def consumer_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="customAttributeInput")
    def custom_attribute_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]], jsii.get(self, "customAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="customClaimInput")
    def custom_claim_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]], jsii.get(self, "customClaimInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRelayStateInput")
    def default_relay_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRelayStateInput"))

    @builtins.property
    @jsii.member(jsii_name="grantTypesInput")
    def grant_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "grantTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupFilterRegexInput")
    def group_filter_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupFilterRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridAndImplicitOptionsInput")
    def hybrid_and_implicit_options_input(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions], jsii.get(self, "hybridAndImplicitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameIdFormatInput")
    def name_id_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameIdFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameIdTransformJsonataInput")
    def name_id_transform_jsonata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameIdTransformJsonataInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectUrisInput")
    def redirect_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "redirectUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshTokenOptionsInput")
    def refresh_token_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationSaasAppRefreshTokenOptions"]]], jsii.get(self, "refreshTokenOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="samlAttributeTransformJsonataInput")
    def saml_attribute_transform_jsonata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlAttributeTransformJsonataInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="spEntityIdInput")
    def sp_entity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spEntityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenLifetime")
    def access_token_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTokenLifetime"))

    @access_token_lifetime.setter
    def access_token_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fb0dce2094353bf862ac6932bf9a358d1d4f375d33d16593dca55a165db522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowPkceWithoutClientSecret")
    def allow_pkce_without_client_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowPkceWithoutClientSecret"))

    @allow_pkce_without_client_secret.setter
    def allow_pkce_without_client_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2640f51230ba19fce15c46e2ca579ade81a67ca68c266692d4174e69fd3ca5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPkceWithoutClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appLauncherUrl")
    def app_launcher_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLauncherUrl"))

    @app_launcher_url.setter
    def app_launcher_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11875e0247acdfcedf65d6a888a32e27757d31f852c7c7c8214f36bd0b3b1d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLauncherUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b350e2f52aebbe4c357cf90efd09abbb3dd37db61e4bf714fefe6c1e6dd7b6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerServiceUrl")
    def consumer_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerServiceUrl"))

    @consumer_service_url.setter
    def consumer_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c732105ba0603af66f74ca876094fdeb8c6ba86f3ced4e967288ff0173389d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerServiceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRelayState")
    def default_relay_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRelayState"))

    @default_relay_state.setter
    def default_relay_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4129f222924b86431073e40812a1aa6aa8aee21ea5cbcf64df4d58c8579b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRelayState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grantTypes")
    def grant_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantTypes"))

    @grant_types.setter
    def grant_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655028a2de9e44243e176070fd158b5821b08b9798d15c1be60d5eeead641b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupFilterRegex")
    def group_filter_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFilterRegex"))

    @group_filter_regex.setter
    def group_filter_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131893fce395bbcbb766470e23b5d8bc39b238559b280a60d56ba0f2f838ca9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFilterRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameIdFormat")
    def name_id_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameIdFormat"))

    @name_id_format.setter
    def name_id_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cacd17173b2abbb9ff19c26687b485dbc7fe5681ef84dd6fbbcdd5e24337b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameIdFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameIdTransformJsonata")
    def name_id_transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameIdTransformJsonata"))

    @name_id_transform_jsonata.setter
    def name_id_transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cd0c18ac4021f516a3a8ef427725b25c2b20992909b7dbc96d1a9a84c7770d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameIdTransformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d7290629a442ba66a60c36f59f78fd19ce6a87637af9f6ce09210a8fb1648b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlAttributeTransformJsonata")
    def saml_attribute_transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlAttributeTransformJsonata"))

    @saml_attribute_transform_jsonata.setter
    def saml_attribute_transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7243c8f3682d4a920b5ea40cdb982e43b5bdb0b7306a016a9e093f32e5eda7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlAttributeTransformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5464e78b786e5658452e709a73cf8396eed6793e0e379a633c781a840745fe88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae5ccdf2561788d69742c6f9acb2ec59053a3e73d1d5f1f80aef0b9b5183235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustAccessApplicationSaasApp]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationSaasApp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationSaasApp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218a8e2563fb056ab19958056423e2a894b1bd20729be4fc196ff028d0b23a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppRefreshTokenOptions",
    jsii_struct_bases=[],
    name_mapping={"lifetime": "lifetime"},
)
class ZeroTrustAccessApplicationSaasAppRefreshTokenOptions:
    def __init__(self, *, lifetime: typing.Optional[builtins.str] = None) -> None:
        '''
        :param lifetime: How long a refresh token will be valid for after creation. Valid units are ``m``, ``h`` and ``d``. Must be longer than 1m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#lifetime ZeroTrustAccessApplication#lifetime}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6490a881c3f568cc7886ac54fafbddda6b2e5baa040de68f6b2849b00d2638b7)
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lifetime is not None:
            self._values["lifetime"] = lifetime

    @builtins.property
    def lifetime(self) -> typing.Optional[builtins.str]:
        '''How long a refresh token will be valid for after creation.

        Valid units are ``m``, ``h`` and ``d``. Must be longer than 1m.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#lifetime ZeroTrustAccessApplication#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationSaasAppRefreshTokenOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da6945e22c57afdd29a0169a519dee4996ec1d4e640ef547b23bc4d2a7aa827c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b2ce34c999e6652b9cb7db83c8f51f25a5b07e2360993bd9c028cb0c6c2222)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db220bb25793b4f1b1249504b276ae0053ed11166c9e29c023176614f7832832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8bea666581ad894137de4e91ff78dd4666b788dd70dedb55233c8719fe660bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d161a6cd047dd2d1d1aac1ac7397f9f91fe14c3de1460876f8e6f3f1e3cadb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e83b2a9a7a3eda2469dbe73dfbefbe03f32707ef4df7299e5f9c8e82d5b868d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7da90fd8d48103370542ab0093d7e08de04f63811ee1483e9df37e008ecfc1f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLifetime")
    def reset_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifetime", []))

    @builtins.property
    @jsii.member(jsii_name="lifetimeInput")
    def lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifetime")
    def lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifetime"))

    @lifetime.setter
    def lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f37139bb87b9b512af5ec8019e31e5d12c9e94b872d3d3f4ee05bea7116ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f4df5778942d62a1fbffda7cf06c517d0fdd87b610a22b8fa5a9b68f4568f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfig",
    jsii_struct_bases=[],
    name_mapping={
        "idp_uid": "idpUid",
        "remote_uri": "remoteUri",
        "authentication": "authentication",
        "deactivate_on_delete": "deactivateOnDelete",
        "enabled": "enabled",
        "mappings": "mappings",
    },
)
class ZeroTrustAccessApplicationScimConfig:
    def __init__(
        self,
        *,
        idp_uid: builtins.str,
        remote_uri: builtins.str,
        authentication: typing.Optional[typing.Union["ZeroTrustAccessApplicationScimConfigAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationScimConfigMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param idp_uid: The UIDs of the IdP to use as the source for SCIM resources to provision to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#idp_uid ZeroTrustAccessApplication#idp_uid}
        :param remote_uri: The base URI for the application's SCIM-compatible API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#remote_uri ZeroTrustAccessApplication#remote_uri}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authentication ZeroTrustAccessApplication#authentication}
        :param deactivate_on_delete: If false, propagates DELETE requests to the target application for SCIM resources. If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#deactivate_on_delete ZeroTrustAccessApplication#deactivate_on_delete}
        :param enabled: Whether SCIM provisioning is turned on for this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enabled ZeroTrustAccessApplication#enabled}
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#mappings ZeroTrustAccessApplication#mappings}
        '''
        if isinstance(authentication, dict):
            authentication = ZeroTrustAccessApplicationScimConfigAuthentication(**authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed24ef6d590cd8e473af78f8b33f160fbe048226d28429cb8e2814bfd91eb53)
            check_type(argname="argument idp_uid", value=idp_uid, expected_type=type_hints["idp_uid"])
            check_type(argname="argument remote_uri", value=remote_uri, expected_type=type_hints["remote_uri"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument deactivate_on_delete", value=deactivate_on_delete, expected_type=type_hints["deactivate_on_delete"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mappings", value=mappings, expected_type=type_hints["mappings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "idp_uid": idp_uid,
            "remote_uri": remote_uri,
        }
        if authentication is not None:
            self._values["authentication"] = authentication
        if deactivate_on_delete is not None:
            self._values["deactivate_on_delete"] = deactivate_on_delete
        if enabled is not None:
            self._values["enabled"] = enabled
        if mappings is not None:
            self._values["mappings"] = mappings

    @builtins.property
    def idp_uid(self) -> builtins.str:
        '''The UIDs of the IdP to use as the source for SCIM resources to provision to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#idp_uid ZeroTrustAccessApplication#idp_uid}
        '''
        result = self._values.get("idp_uid")
        assert result is not None, "Required property 'idp_uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_uri(self) -> builtins.str:
        '''The base URI for the application's SCIM-compatible API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#remote_uri ZeroTrustAccessApplication#remote_uri}
        '''
        result = self._values.get("remote_uri")
        assert result is not None, "Required property 'remote_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationScimConfigAuthentication"]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authentication ZeroTrustAccessApplication#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationScimConfigAuthentication"], result)

    @builtins.property
    def deactivate_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If false, propagates DELETE requests to the target application for SCIM resources.

        If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#deactivate_on_delete ZeroTrustAccessApplication#deactivate_on_delete}
        '''
        result = self._values.get("deactivate_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether SCIM provisioning is turned on for this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enabled ZeroTrustAccessApplication#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mappings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationScimConfigMappings"]]]:
        '''mappings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#mappings ZeroTrustAccessApplication#mappings}
        '''
        result = self._values.get("mappings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationScimConfigMappings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationScimConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "scheme": "scheme",
        "authorization_url": "authorizationUrl",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "password": "password",
        "scopes": "scopes",
        "token": "token",
        "token_url": "tokenUrl",
        "user": "user",
    },
)
class ZeroTrustAccessApplicationScimConfigAuthentication:
    def __init__(
        self,
        *,
        scheme: builtins.str,
        authorization_url: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
        token_url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scheme: The authentication scheme to use when making SCIM requests to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scheme ZeroTrustAccessApplication#scheme}
        :param authorization_url: URL used to generate the auth code used during token generation. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authorization_url ZeroTrustAccessApplication#authorization_url}
        :param client_id: Client ID used to authenticate when generating a token for authenticating with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_id ZeroTrustAccessApplication#client_id}
        :param client_secret: Secret used to authenticate when generating a token for authenticating with the remove SCIM service. Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_secret ZeroTrustAccessApplication#client_secret}
        :param password: Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#password ZeroTrustAccessApplication#password}
        :param scopes: The authorization scopes to request when generating the token used to authenticate with the remove SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        :param token: Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token ZeroTrustAccessApplication#token}
        :param token_url: URL used to generate the token used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token_url ZeroTrustAccessApplication#token_url}
        :param user: User name used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#user ZeroTrustAccessApplication#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ecb6b1233c4fce4b268366016c523f851dd300b1747ce2599833d502464b7d)
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument authorization_url", value=authorization_url, expected_type=type_hints["authorization_url"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheme": scheme,
        }
        if authorization_url is not None:
            self._values["authorization_url"] = authorization_url
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if password is not None:
            self._values["password"] = password
        if scopes is not None:
            self._values["scopes"] = scopes
        if token is not None:
            self._values["token"] = token
        if token_url is not None:
            self._values["token_url"] = token_url
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def scheme(self) -> builtins.str:
        '''The authentication scheme to use when making SCIM requests to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scheme ZeroTrustAccessApplication#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_url(self) -> typing.Optional[builtins.str]:
        '''URL used to generate the auth code used during token generation.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authorization_url ZeroTrustAccessApplication#authorization_url}
        '''
        result = self._values.get("authorization_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID used to authenticate when generating a token for authenticating with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_id ZeroTrustAccessApplication#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Secret used to authenticate when generating a token for authenticating with the remove SCIM service.

        Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_secret ZeroTrustAccessApplication#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#password ZeroTrustAccessApplication#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The authorization scopes to request when generating the token used to authenticate with the remove SCIM service.

        Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token ZeroTrustAccessApplication#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_url(self) -> typing.Optional[builtins.str]:
        '''URL used to generate the token used to authenticate with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token_url ZeroTrustAccessApplication#token_url}
        '''
        result = self._values.get("token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''User name used to authenticate with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#user ZeroTrustAccessApplication#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationScimConfigAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationScimConfigAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2092e0de164ec969f7e9ddec8407a11451c0e89c4116013fc145501728612a58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizationUrl")
    def reset_authorization_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationUrl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetTokenUrl")
    def reset_token_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenUrl", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="authorizationUrlInput")
    def authorization_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUrlInput")
    def token_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationUrl")
    def authorization_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationUrl"))

    @authorization_url.setter
    def authorization_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049351fa1f185a569f1e81166b431f043268cd038a8cc145170d821c864835db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750b8d1c095c9856fe85bbedee0b3499bad2b4291e9097dc8abe54902ef2c15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc26828b8e083a8a2595bd485dbff30f965d4c5a0b0f07bb87106c8b960b99c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ad05a822425dfb66907635ff1d89c311bfe6f43e728bd0a34d5b3a86d1cc7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd5e83f101be05ab311d697646530558ceacc68e0724e87a80e690e1c537a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1570f66ad7030069d7e29f3ff32d5adf89b72076ccbd99c7d721f7e395413db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244f3f0a66f77d883bd43bb55d85fd3f7fde7079a5563a43b16600e49e9a3f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f34107877bdcc9ac6d4df827ffb6e8dfca11942720d52e60589eaa7af7d37da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7c7e20bcb9a12ecd78d646245a861c85aab173a15f94db57bf8c6520257bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5e0f6b8dca149d03908fbbc7aada492af864e2312467a9a037556aaa339bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigMappings",
    jsii_struct_bases=[],
    name_mapping={
        "schema": "schema",
        "enabled": "enabled",
        "filter": "filter",
        "operations": "operations",
        "strictness": "strictness",
        "transform_jsonata": "transformJsonata",
    },
)
class ZeroTrustAccessApplicationScimConfigMappings:
    def __init__(
        self,
        *,
        schema: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter: typing.Optional[builtins.str] = None,
        operations: typing.Optional[typing.Union["ZeroTrustAccessApplicationScimConfigMappingsOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        strictness: typing.Optional[builtins.str] = None,
        transform_jsonata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema: Which SCIM resource type this mapping applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#schema ZeroTrustAccessApplication#schema}
        :param enabled: Whether or not this mapping is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enabled ZeroTrustAccessApplication#enabled}
        :param filter: A `SCIM filter expression <https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2>`_ that matches resources that should be provisioned to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#filter ZeroTrustAccessApplication#filter}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#operations ZeroTrustAccessApplication#operations}
        :param strictness: How strictly to adhere to outbound resource schemas when provisioning to this mapping. "strict" will remove unknown values when provisioning, while "passthrough" will pass unknown values to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#strictness ZeroTrustAccessApplication#strictness}
        :param transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms the resource before provisioning it in the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#transform_jsonata ZeroTrustAccessApplication#transform_jsonata}
        '''
        if isinstance(operations, dict):
            operations = ZeroTrustAccessApplicationScimConfigMappingsOperations(**operations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e429138f79298c45e0a4a980b4a1bc857a8c361b3b91254b9c314a97e8081a)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument operations", value=operations, expected_type=type_hints["operations"])
            check_type(argname="argument strictness", value=strictness, expected_type=type_hints["strictness"])
            check_type(argname="argument transform_jsonata", value=transform_jsonata, expected_type=type_hints["transform_jsonata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if filter is not None:
            self._values["filter"] = filter
        if operations is not None:
            self._values["operations"] = operations
        if strictness is not None:
            self._values["strictness"] = strictness
        if transform_jsonata is not None:
            self._values["transform_jsonata"] = transform_jsonata

    @builtins.property
    def schema(self) -> builtins.str:
        '''Which SCIM resource type this mapping applies to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#schema ZeroTrustAccessApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#enabled ZeroTrustAccessApplication#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A `SCIM filter expression <https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2>`_ that matches resources that should be provisioned to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#filter ZeroTrustAccessApplication#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional["ZeroTrustAccessApplicationScimConfigMappingsOperations"]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#operations ZeroTrustAccessApplication#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional["ZeroTrustAccessApplicationScimConfigMappingsOperations"], result)

    @builtins.property
    def strictness(self) -> typing.Optional[builtins.str]:
        '''How strictly to adhere to outbound resource schemas when provisioning to this mapping.

        "strict" will remove unknown values when provisioning, while "passthrough" will pass unknown values to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#strictness ZeroTrustAccessApplication#strictness}
        '''
        result = self._values.get("strictness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms the resource before provisioning it in the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#transform_jsonata ZeroTrustAccessApplication#transform_jsonata}
        '''
        result = self._values.get("transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationScimConfigMappings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationScimConfigMappingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigMappingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4982d85328e485577e71db6ca0ff28bd4d11ed103fe4e751b6865c29edf27b91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationScimConfigMappingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c12d7ca795066c59b692ad4f51ed06da9a4bbfb1671bcfb9058abce1dbf166d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationScimConfigMappingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11722f82c822bd7d3852c62774d61090e29ff5c91dffd7de692dc798a6a6df8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cda44f403d31af0b43b47ab683ca8fe0a9e2252e5b592cd2fdea6ba3c13297b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__282cc7e4bc2718f13142a71dc8796a2e16a73d45e66b1f4b5a4978083c5d69d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd5e8b7a787876d92c35a2d24bc410013f73b0c55e8fc95ebd31c3eae5cbaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigMappingsOperations",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ZeroTrustAccessApplicationScimConfigMappingsOperations:
    def __init__(
        self,
        *,
        create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param create: Whether or not this mapping applies to create (POST) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#create ZeroTrustAccessApplication#create}
        :param delete: Whether or not this mapping applies to DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#delete ZeroTrustAccessApplication#delete}
        :param update: Whether or not this mapping applies to update (PATCH/PUT) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#update ZeroTrustAccessApplication#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a09fa54b88dde85f9223922abb1ad6ae627c2f2547b57da96c41a7bd6afac9a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping applies to create (POST) operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#create ZeroTrustAccessApplication#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping applies to DELETE operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#delete ZeroTrustAccessApplication#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping applies to update (PATCH/PUT) operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#update ZeroTrustAccessApplication#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationScimConfigMappingsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationScimConfigMappingsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigMappingsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe6e3c8fc9d4e2f3170ae5c2ceb74951b2955571764b4c82a0f6bb0ce4272f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "create"))

    @create.setter
    def create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d292edfba0d7e3b7a55cc8ace4108ac256e7b720216108aea5114f658c3273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "delete"))

    @delete.setter
    def delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777ec6d891e7721b04e14edf7fa10e9f357be6ae8bb41f7940fadfc1ce53f997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "update"))

    @update.setter
    def update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7791b72a4522df28341aaf05fb9e6aedfb520b7fb2772b593fa73fcbeb257460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa06f143a4b3a50d8cd11ef17f7e5fdd9d896da7bb6e6065b6233907d8a6cd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationScimConfigMappingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigMappingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b0cfbf2de00e251c5d618219bf8ae1c16eb631d3bcb73bdd800083e125a428f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        *,
        create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param create: Whether or not this mapping applies to create (POST) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#create ZeroTrustAccessApplication#create}
        :param delete: Whether or not this mapping applies to DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#delete ZeroTrustAccessApplication#delete}
        :param update: Whether or not this mapping applies to update (PATCH/PUT) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#update ZeroTrustAccessApplication#update}
        '''
        value = ZeroTrustAccessApplicationScimConfigMappingsOperations(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putOperations", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetStrictness")
    def reset_strictness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictness", []))

    @jsii.member(jsii_name="resetTransformJsonata")
    def reset_transform_jsonata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformJsonata", []))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(
        self,
    ) -> ZeroTrustAccessApplicationScimConfigMappingsOperationsOutputReference:
        return typing.cast(ZeroTrustAccessApplicationScimConfigMappingsOperationsOutputReference, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="strictnessInput")
    def strictness_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "strictnessInput"))

    @builtins.property
    @jsii.member(jsii_name="transformJsonataInput")
    def transform_jsonata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transformJsonataInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b72c81a9e5cff5cc95e524a0ca8dd864548c4e8e3eda50e28ff65f6724a3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2230b039da2ffe3bcd776feb5c3f409fa81b60bfe83e319d38372684dff96b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5215af50fc75a0e73ad843e3d866e7405d6025619b93538a5fc263322a27dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictness")
    def strictness(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strictness"))

    @strictness.setter
    def strictness(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fbfb35f18e42455dcd9897ac76fe0a3795ed2ce09a0d173aee5c89c2302d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformJsonata")
    def transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformJsonata"))

    @transform_jsonata.setter
    def transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b5dd75241fc8639d24bfc70cba7f606f40751b4614d1808cde1347beac7a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationScimConfigMappings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationScimConfigMappings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationScimConfigMappings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f597ea09f19a498bc840b2423b24294d1e2b77d4259d154703c170544b4578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationScimConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationScimConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd13586a1dd626fd8881187550aa6b978f5254d1731ed2e496df78824dc7bb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        scheme: builtins.str,
        authorization_url: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
        token_url: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scheme: The authentication scheme to use when making SCIM requests to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scheme ZeroTrustAccessApplication#scheme}
        :param authorization_url: URL used to generate the auth code used during token generation. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#authorization_url ZeroTrustAccessApplication#authorization_url}
        :param client_id: Client ID used to authenticate when generating a token for authenticating with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_id ZeroTrustAccessApplication#client_id}
        :param client_secret: Secret used to authenticate when generating a token for authenticating with the remove SCIM service. Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#client_secret ZeroTrustAccessApplication#client_secret}
        :param password: Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#password ZeroTrustAccessApplication#password}
        :param scopes: The authorization scopes to request when generating the token used to authenticate with the remove SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#scopes ZeroTrustAccessApplication#scopes}
        :param token: Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token ZeroTrustAccessApplication#token}
        :param token_url: URL used to generate the token used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#token_url ZeroTrustAccessApplication#token_url}
        :param user: User name used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#user ZeroTrustAccessApplication#user}
        '''
        value = ZeroTrustAccessApplicationScimConfigAuthentication(
            scheme=scheme,
            authorization_url=authorization_url,
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            scopes=scopes,
            token=token,
            token_url=token_url,
            user=user,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="putMappings")
    def put_mappings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac25c5d91f207d1d973db6b446851bef6fca92aad259cb2078316a20ee88afae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMappings", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @jsii.member(jsii_name="resetDeactivateOnDelete")
    def reset_deactivate_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeactivateOnDelete", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMappings")
    def reset_mappings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappings", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> ZeroTrustAccessApplicationScimConfigAuthenticationOutputReference:
        return typing.cast(ZeroTrustAccessApplicationScimConfigAuthenticationOutputReference, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="mappings")
    def mappings(self) -> ZeroTrustAccessApplicationScimConfigMappingsList:
        return typing.cast(ZeroTrustAccessApplicationScimConfigMappingsList, jsii.get(self, "mappings"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="deactivateOnDeleteInput")
    def deactivate_on_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deactivateOnDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idpUidInput")
    def idp_uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idpUidInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingsInput")
    def mappings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]], jsii.get(self, "mappingsInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteUriInput")
    def remote_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteUriInput"))

    @builtins.property
    @jsii.member(jsii_name="deactivateOnDelete")
    def deactivate_on_delete(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deactivateOnDelete"))

    @deactivate_on_delete.setter
    def deactivate_on_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3775745e8c089fcfccac709b3db0b6f61040c230a03b3bc79d4ea941048a425f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deactivateOnDelete", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__7e2aa79d0def243d84c4d4d28f66f98ec868452092917d912ff50c30f8d2a1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idpUid")
    def idp_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpUid"))

    @idp_uid.setter
    def idp_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574933f80f7d7da91678a2b3008b5465fe3e6e53188344329efa68ecfdc57ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteUri")
    def remote_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteUri"))

    @remote_uri.setter
    def remote_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5406d8f276e75d039963d97f7874f104345d19f82c913154fed37bd7d26b09f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ZeroTrustAccessApplicationScimConfig]:
        return typing.cast(typing.Optional[ZeroTrustAccessApplicationScimConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ZeroTrustAccessApplicationScimConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2bc60a07a514931792b4078fe0dd4797301c6149d73dec0fd7e224ca0851a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "protocol": "protocol",
        "target_attributes": "targetAttributes",
    },
)
class ZeroTrustAccessApplicationTargetCriteria:
    def __init__(
        self,
        *,
        port: jsii.Number,
        protocol: builtins.str,
        target_attributes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param port: The port that the targets use for the chosen communication protocol. A port cannot be assigned to multiple protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#port ZeroTrustAccessApplication#port}
        :param protocol: The communication protocol your application secures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#protocol ZeroTrustAccessApplication#protocol}
        :param target_attributes: target_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#target_attributes ZeroTrustAccessApplication#target_attributes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c5f95cc6144bb0d1e2e5b734e8baca1534d63b2e34e895e1b853b7e917b04f)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument target_attributes", value=target_attributes, expected_type=type_hints["target_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "protocol": protocol,
            "target_attributes": target_attributes,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port that the targets use for the chosen communication protocol. A port cannot be assigned to multiple protocols.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#port ZeroTrustAccessApplication#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The communication protocol your application secures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#protocol ZeroTrustAccessApplication#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_attributes(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes"]]:
        '''target_attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#target_attributes ZeroTrustAccessApplication#target_attributes}
        '''
        result = self._values.get("target_attributes")
        assert result is not None, "Required property 'target_attributes' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationTargetCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationTargetCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62177dab3ece260cddeb67aecb9a95abbf1b75a041c89f358a177e6696e730bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationTargetCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f548a3db067bc87929f0721b50f128734ba832335114838cd7e3cea9bdbdfa4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationTargetCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5879327f1788ee3832554f02937a5491bec1fed9f83fab1be99628106ad6b2c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb5fc42c8ea5dbd0629bc52fc476332348ff87a76d5ef05168a623869698e127)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41a1af0605f409c28c193e0882c13cb4394d21bf12f82d78104e2de87cd83196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed3e2bfa0c87cd1fc44be7629b1f403fcee25c6adf7403c3d4119fb2b9703c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationTargetCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c70c7a7d4564a84da124d02399b8a0c3ba64b0f1871bea49f2db0b2a41279567)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetAttributes")
    def put_target_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdfe4436a34c728c31a9ae52d08f087f5a1a4e1431d857ca79491231e44397f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetAttributes", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetAttributes")
    def target_attributes(
        self,
    ) -> "ZeroTrustAccessApplicationTargetCriteriaTargetAttributesList":
        return typing.cast("ZeroTrustAccessApplicationTargetCriteriaTargetAttributesList", jsii.get(self, "targetAttributes"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAttributesInput")
    def target_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ZeroTrustAccessApplicationTargetCriteriaTargetAttributes"]]], jsii.get(self, "targetAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1641fb9b0840e77fea2869966a62fe0826f07b642ad3a16cf31cc6276e522a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958c0c954dc8468a737ed4baa12f7c419e2f09db7b3e152cce47471e08571229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a185ff462507fd4d2cbf7fac7c32d3e0537ff5260ae4069f0e9d867896d2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteriaTargetAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class ZeroTrustAccessApplicationTargetCriteriaTargetAttributes:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        :param values: The values of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#values ZeroTrustAccessApplication#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f104209cd6a81efda2be5c187e27d051bd60b40149a480c6005ff1a991bd4f15)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#name ZeroTrustAccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The values of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/zero_trust_access_application#values ZeroTrustAccessApplication#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZeroTrustAccessApplicationTargetCriteriaTargetAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ZeroTrustAccessApplicationTargetCriteriaTargetAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteriaTargetAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5db129bb26de81d9b431ca362f8e1d8493246a32d3c3b7d6ec79f68cb8d459a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ZeroTrustAccessApplicationTargetCriteriaTargetAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2aa47d42928194f7af1f956436f1389140023b5c701867444db1e9e886146ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ZeroTrustAccessApplicationTargetCriteriaTargetAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7061d1c4b92f7261156a585bf764e9c030d523ddbaf672a5fe92d6fa1c3bdcb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82e078727eaea3267ce9a92c56d1e981fef64d558831e8a328d9f9457ca5a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df9ff37c3a6470841733c644064260747f95ebfbc78ee6d347f0d63c241a8098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0222f97f57b77eef417ee153b2cfe3594245fb820f0483adb696fe9818084eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ZeroTrustAccessApplicationTargetCriteriaTargetAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zeroTrustAccessApplication.ZeroTrustAccessApplicationTargetCriteriaTargetAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2757f0483830b7c8fc4c0162f3fc01ba48da17e180c693862a4c870291bf21ce)
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
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c91996f495047b84c39d77971c792cb49db2d7f122757c7484f19870c8c3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67645c303bbfd48823fbe70074a6af241a50ba10f9b89658291f3e3c0b2ff42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a59f2d2a58be5094365412dfb811501f73e37acfc73d7e7e061f9d5e7b0757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ZeroTrustAccessApplication",
    "ZeroTrustAccessApplicationConfig",
    "ZeroTrustAccessApplicationCorsHeaders",
    "ZeroTrustAccessApplicationCorsHeadersList",
    "ZeroTrustAccessApplicationCorsHeadersOutputReference",
    "ZeroTrustAccessApplicationDestinations",
    "ZeroTrustAccessApplicationDestinationsList",
    "ZeroTrustAccessApplicationDestinationsOutputReference",
    "ZeroTrustAccessApplicationFooterLinks",
    "ZeroTrustAccessApplicationFooterLinksList",
    "ZeroTrustAccessApplicationFooterLinksOutputReference",
    "ZeroTrustAccessApplicationLandingPageDesign",
    "ZeroTrustAccessApplicationLandingPageDesignOutputReference",
    "ZeroTrustAccessApplicationSaasApp",
    "ZeroTrustAccessApplicationSaasAppCustomAttribute",
    "ZeroTrustAccessApplicationSaasAppCustomAttributeList",
    "ZeroTrustAccessApplicationSaasAppCustomAttributeOutputReference",
    "ZeroTrustAccessApplicationSaasAppCustomAttributeSource",
    "ZeroTrustAccessApplicationSaasAppCustomAttributeSourceOutputReference",
    "ZeroTrustAccessApplicationSaasAppCustomClaim",
    "ZeroTrustAccessApplicationSaasAppCustomClaimList",
    "ZeroTrustAccessApplicationSaasAppCustomClaimOutputReference",
    "ZeroTrustAccessApplicationSaasAppCustomClaimSource",
    "ZeroTrustAccessApplicationSaasAppCustomClaimSourceOutputReference",
    "ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions",
    "ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptionsOutputReference",
    "ZeroTrustAccessApplicationSaasAppOutputReference",
    "ZeroTrustAccessApplicationSaasAppRefreshTokenOptions",
    "ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsList",
    "ZeroTrustAccessApplicationSaasAppRefreshTokenOptionsOutputReference",
    "ZeroTrustAccessApplicationScimConfig",
    "ZeroTrustAccessApplicationScimConfigAuthentication",
    "ZeroTrustAccessApplicationScimConfigAuthenticationOutputReference",
    "ZeroTrustAccessApplicationScimConfigMappings",
    "ZeroTrustAccessApplicationScimConfigMappingsList",
    "ZeroTrustAccessApplicationScimConfigMappingsOperations",
    "ZeroTrustAccessApplicationScimConfigMappingsOperationsOutputReference",
    "ZeroTrustAccessApplicationScimConfigMappingsOutputReference",
    "ZeroTrustAccessApplicationScimConfigOutputReference",
    "ZeroTrustAccessApplicationTargetCriteria",
    "ZeroTrustAccessApplicationTargetCriteriaList",
    "ZeroTrustAccessApplicationTargetCriteriaOutputReference",
    "ZeroTrustAccessApplicationTargetCriteriaTargetAttributes",
    "ZeroTrustAccessApplicationTargetCriteriaTargetAttributesList",
    "ZeroTrustAccessApplicationTargetCriteriaTargetAttributesOutputReference",
]

publication.publish()

def _typecheckingstub__27338aeeecd2e31c5778c77e6b90d648344d66ce330b5d2a91fa9403173c8b94(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: typing.Optional[builtins.str] = None,
    allow_authenticate_via_warp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_launcher_logo_url: typing.Optional[builtins.str] = None,
    app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bg_color: typing.Optional[builtins.str] = None,
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
    custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_type: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header_bg_color: typing.Optional[builtins.str] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    landing_page_design: typing.Optional[typing.Union[ZeroTrustAccessApplicationLandingPageDesign, typing.Dict[builtins.str, typing.Any]]] = None,
    logo_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    saas_app: typing.Optional[typing.Union[ZeroTrustAccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[ZeroTrustAccessApplicationScimConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__28aed9d1c8ee78428e088d71f6579e3d02e4f30fb17461e201068a0829c6d553(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b74a9e8f14e0bc0b5d1004a5b1f8b96ee3a309867c32ac47e54e67e549b756(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a01e38fa3f74cc489795b06ff4df8da8c34523777fc462714c8fd0a21c8e3e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69b01b6350443f6fa14a95caa04e5b39c3826cfbbbc0be0bb475a2a02a6225e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29efcca397269d22b3a8f8f3a86f3abb19cd0dbf9186b3d59feb062d1fc06075(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec731061956ee4a6f8bb3a95fbebdcd6aaf64c49f851492c2b536b1eddd1f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3c1cb91eeae56a8cf2cc59bdb6b2795ccad015bd24206d07e0951f56c89636(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be64e8ac39fca2dd2500aa0b54d299e1bc29de142d2d4612f9e17af4b10799f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1457a5e561e09d35265af36cf5ca06925dc1dce9801441f692b1fb3fd3b320ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d7c21a4a8c8ab0de0d7f1ecc46004dcf0662e0a2cc335f5267670f1f64525c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b2c9f95fc566b2f077f059a82d95b631ad2429361b9dba2a2ed2694ebf6854(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff301b82f24f646a2cb5ef99ea6a32ce4f9c04cdbb27a5d4ada20b67d4f5eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47019a4be708eb71f0f058e0eede1241f8158b762556db853df184499ea6ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e27c1cb8a4167f8e04ac0d6c18ada8a4b250b5de4ca6f3c845385a23be8379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3a3d032f0b868b35c26301c384de6a32873fbeb250a3f3294135e8f80a7f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08aca6db6ca2d706006c7c12a3dc79270cee71da8486e494cb688f27442e4f73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8004de509defca4d78cf6a2555915db9666893c72c10c436cf77de1e893ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd46fea72ce47a2cb8c1038d28bc97dd5ab94441af6f154d0d17a712950ec37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a765eff579c85806c83ac9f1fa443520c9cfcb800a0081b0516ce1f5af65fe8e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee4e1351d0024499a383aab5b228a41a8b6d5c815456c021b3f24d0b3adf498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a234bcc12ea03ebba0a2fd2beb7c5da757daf1a34e5f0f7d655bad92a3ee2425(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d151783486bb3f4aff9f1d4aff06c316ba75a01a3e4e7fe45e271701b7dcaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0d042e7fb8029cf39fd64da67feaaaabb16a462aa84e0da680533bb09db1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cb26c3ba6e995d5381c8693e2f4791dc952dcf01b159b9dd90e528177d7233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb9aa9809673e3b121460e152319e7a1aabe343c83038d99e1a9389706fdd34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04ed784e46647bbd756e89e1abc862e4da00addfd61a13f6536f03673217a9a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cead96487ecf56f324721527887db96515004eafe6e4934b0218556799b20014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7027add4c94ff5c6e1d9d981891a6e2d08756603689c68714f7ab199c29667f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018e0e147bf616117e34644ac9fc785c3537999f64d5e9d3d0af55c0e91db961(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0735f107a1bad1083eaf92196f572661daa359b0ad1c704fef6dee2068d97a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895090706d57872884433315cbdbc3cc94643221d625c7ff51d8c73fa56f70db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d96622f0d48fee60151148031537f7ae6703fa09d88913fc82a3c8e50b291e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6871878039e238faffb7567ecb3ee909e5a3840597f72ad141e4abcf93aa1ce6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195de0e3b7b7a39255d38a862a353bf9e4ae6f9519c29c520e71e02578a424ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36279d7f822e7c4fc42a6f41cadc4da245c4c9c778ac045de3186657c462b46b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1279db324fed64f313ac2ca6fb2cb06c24a138a471a8e0566ec470159c6fbf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: typing.Optional[builtins.str] = None,
    allow_authenticate_via_warp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_idps: typing.Optional[typing.Sequence[builtins.str]] = None,
    app_launcher_logo_url: typing.Optional[builtins.str] = None,
    app_launcher_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_redirect_to_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bg_color: typing.Optional[builtins.str] = None,
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
    custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_type: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header_bg_color: typing.Optional[builtins.str] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    landing_page_design: typing.Optional[typing.Union[ZeroTrustAccessApplicationLandingPageDesign, typing.Dict[builtins.str, typing.Any]]] = None,
    logo_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    saas_app: typing.Optional[typing.Union[ZeroTrustAccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[ZeroTrustAccessApplicationScimConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570d0baa177c6afcf552d1711ba79b01b6b8b310579c5b73ce48b2f5f08ca83a(
    *,
    allow_all_headers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_all_methods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_all_origins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf13cefc63d184418962e80cb3cfb68df3da3156635c6ef76de4f9f77ada4962(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406be4d77a37912670f4a00bc058c73b502c2345c3a7d8e34c78a80ef095811b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdb2f560786dfffb916477a05df4eff5c02ad99ccc77be24ef6d710a814d409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967f6c1ba44f7f1b8d20843833a24962fe9db2ae4840481c84b45a68b5e65223(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2f7e26847c9f75c420600924ab9bef977fa39cf86ff807b7f92ea65c4b3620(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ba2fa0abc6852573fa9953b32ac42d7f6a72e93dc3f9f0d91765701b67e8e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationCorsHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcf1fe95da2b6031991ead48569fbb9ff00b03afd00e3214e3d20386a992210(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d0a09ee60d1b08c6963232e100c6ceaaede5c0ef39009732582d935fc1e905(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d135a36b855dfbbbf40a911ff12cf0577ed83002a7a7cee84aa8c13c23cb8f8e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c840a4753ace2f1e243c60b9916c5df15c9d7246abf3c6895676d0a316420c02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8009166033a2928de4ebc21edad17423ddc0e0deebedab0af8c4dfc5fb83381(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082f53f30671b16288afc1a9ad26c542a9b393e4541acc8b87918982ce0310ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef529e72178495b6c43ebe1f695b2cae1293867b0f0c9fff9215f1082c95435a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b2162a14fe720dc097500c299b6154310fffaa61cea5569bb901b681e85b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca16c2a986f7382e78a17fb496bd86538fd3ee1d9a8475ec1ff814259a785797(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad0e91b7680ac85eae84c174e10132dc780ef53bf867a5ccffdfc73790cd36e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationCorsHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb53f29245a8f4afef45363f780ecbc61eec9157bc84ce5d2838e235e17fc873(
    *,
    uri: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8168d79a8693c9a4e11c3b5ac3ec9eba59f7a61ff41ef15d1510416071392301(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb9842149a5ba31f0c7bb7a4bc2efc080e3f3c9bf4f718ec8bbd9987bf4badc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c416ede1a70be4b7cef8f1721172a05250854cca34377c9007f895313c8fbaa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbb8d8255fcf87cb4069296b24e7fdb52c6606b44ac92d6c62f69fcca0ddb3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f4dd46e14736abe9c77407eda1be11e2e0e38d575e78aea951685bc2c365dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22c25c82c26ed7b257b2d03476a3fbd8bb5dd8bab445155b2691eb44afde5ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad05bb67450b8cea2997f05d67e7950ddb7245da376758e1e76342421594589(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3f7e0e5261b28be35a0e20320948333c43ca52eec412f6d1ab534347d28b7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642515c81cebe22a173f73f35c34adb39b6ef57f7f0a66229da0ebaf09d59131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4905a20cb306991e008eaa738934cdef4f96e362a5886068f6f65d016dd335f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33de202b3d83c54564f055486a5738ad842797dede2aa86d887444a9647d0ff(
    *,
    name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce73644e02d48e6eb68a59282e83ae003bd1ced90461a5197c95a65e17da3d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf2e1a33ba6a3d6ec819c36230d12610454e30c60a713b341411d823ba23192(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e51e2383e0ec4f8292d683b26b6b451e152ad08ddd5747991e2b6d0d4e4924(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c62edec9276ba061132ebfc6eb52acd5e6ab14a44cf072735b27a81bc4debbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4c4c388a572055d945d7eede9097569a3ea099aaaad53f249b82ede4ac509c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bc629578b246ab1a8885978399933d192377d2ba319a4f0ec7757ef9614f62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationFooterLinks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d21bc58a76579810293c6ae93bcda284e56e65f8c609faaeed6b3ca3b2aa86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a6aea00285b792ec70c175c5fae0a1a784246695e5eb80558a8a979b66d634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9137cb5922c257b75cacc27a6774aad64820e641abcc311e7064f16d43af3060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32afdbdbe0dee00528ada5be0b893b76024e13f0273e8adeff1fc2019313703(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationFooterLinks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8926bc90faf274b6c685bf7e4c7c54a0f88e4ee4cf30cf581bdcd7feb90d772e(
    *,
    button_color: typing.Optional[builtins.str] = None,
    button_text_color: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469f1fb2458e3a0a89654ebf80a766ab780607f746e831ffede7d84c08f114c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b6c4ec3f0d549f31041f7cffde66753d6dd27e2c8402c72ae14d81be888644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb3e7b45304465a72f40624ad5f08515f2fc0e3094853ae561807b34af88af7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4a91aee042f486c785ac2b6ec48e8a41bb11997c1cc07c7e40daafea05495d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b631466d7f511cd30ae0b7ee0fd957a686eb7d41596b8b527d6dfffc112b7994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5658ce331fa05e1720564dc64cad97c9859e052f5db692bd7949bb1bfda86ff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44de85cfb941b73aa477ef6a25f8ff6ec66c03a22228165cede093b7715b5a3(
    value: typing.Optional[ZeroTrustAccessApplicationLandingPageDesign],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba771b6654419f66e79dfb8d9609f915a6d90c1b92895f9d8bcbc1ad4e696d75(
    *,
    access_token_lifetime: typing.Optional[builtins.str] = None,
    allow_pkce_without_client_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    app_launcher_url: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    consumer_service_url: typing.Optional[builtins.str] = None,
    custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_relay_state: typing.Optional[builtins.str] = None,
    grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_filter_regex: typing.Optional[builtins.str] = None,
    hybrid_and_implicit_options: typing.Optional[typing.Union[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    name_id_format: typing.Optional[builtins.str] = None,
    name_id_transform_jsonata: typing.Optional[builtins.str] = None,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    sp_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf05ee29e111b33731279ab5ef58e817e34b5ec435a0b1dd9d62ef19badb94a6(
    *,
    source: typing.Union[ZeroTrustAccessApplicationSaasAppCustomAttributeSource, typing.Dict[builtins.str, typing.Any]],
    friendly_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_format: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e2644177328088014db085e14157d3c422c994b899e004f580462ed061b3d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7f6c29499c30ccde95a5997eff773874d08cde65f07d966334474f2224f618(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce299c0ceeb006c89984893802d4ac5a3ce90fb81772a0909f91c9136139f89d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b08292be7e04d762a84f3cb3d278b42f1d4c7f09ed896e20accef17984636d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c54b834d0dbf6bd8a788a26ac0aa8853781987041a3d41b6a6733fb389adbf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd17fd91e2de880819e5ff7cfb6a02a358081329e7d28474325c556a158bf82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomAttribute]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b3ab3ef91af0eb639dccf4246e3a55148a67a8d146027f2f94c43153ad1473(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a567c8ea5c5cba33f8611571bc706569e7611d9ab794d245f3dd165decda70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb3b2db980949b725986de7ebf250d75f42671e63eedec96d56d6164c6af2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08f90628b302dce3ca0a3c708fcebc2bf3e949c321033863c67565036d26dcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0602b1b05666f2db6e2ab331770576ec023a8e47d63168fe26f9837a7088939(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052dfd00c6ade1eeb55e57fcd51d82da154ae4eb7a8fb864bc51306842c03f5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomAttribute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27123a84c1e01a6f939d33a0493df6d916c8deb15e81e737606b6f56650e23be(
    *,
    name: builtins.str,
    name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719f21aff281a27145dc4c3a121e273ecba3e0c06a0aa0fc35ce8f089aae5c85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38062080c8058b9b7814a726edd28686bc7e2cad43d5329995738a2360d52785(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab88eacfa80c31a18010857bfbe5e7242f027bd140ae9df652986420f4aa4458(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8911c574a947e5998ec86d1d3bca407dc4a7afefdcd3a7262f43eed3228e2a79(
    value: typing.Optional[ZeroTrustAccessApplicationSaasAppCustomAttributeSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4846e51f54a8de0a208da2a437855cac3ca0a20eb8ad16b6e7d59da668d204(
    *,
    source: typing.Union[ZeroTrustAccessApplicationSaasAppCustomClaimSource, typing.Dict[builtins.str, typing.Any]],
    name: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86f4d51f9aefcf4172adc470a8faaad0a6e10d3f5ab586d7939a3387f9fe21f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059c90605c39da13ab7e429a86f160381ad6d6846dc2cbdad676a37231bc3ee2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbc76d1338868392a25c58cd1277f8c92337640ca8820a1b6b6c5f4cbde8953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4eeac1b0cc37966c452fe568d1011229238c63ff039e22c42dab68ff763fc7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86244a8d790c9686daaccc1003c61fbc89ef63e16794f3208b7ef7447871e486(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1669a5e10f1b79e87bd5b9069fdffe0d01ddb863b6521d2668fd99a9212b4f07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppCustomClaim]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbab7b7221be9547277233fee27d2d2de3c5f8ac45d9dd007a4785c8c126bfad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3d15c80a11204c22a7a278ce34b09742edd61b3a8f63a6a29630b5212af723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c377732c1d05abf30fbe21dc6a691c03c58e845060ceb75ec0c54e81b5ba59a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f5e1707532fe467fd693f50da16d9220b168ca03e4a3ac3cb6a6069ea7a8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053f0f67cf42cb806adee0e8822493b0981a92e0fad74c99b030f18a8215048d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppCustomClaim]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de088843a77bee0081b4d7e0f5e848857ca9e320eb10a16d14d5c55a5d3bacf3(
    *,
    name: builtins.str,
    name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5194d214b1b10213dae1aa60d0aaa786adfa9cf7c54bac50677be3b2182cd15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b84eb1bb627ebedc2c641131f20028ba92d3370fd59d24e39ba397db26fab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddeae9558a43c8cced66195ffeb972db93b0dfeecf6d1e4f4de52edddc84c71(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f04cea13199de29ca7312a0688d53cf49e7ceb7dbe119ab6510c1e2c9c6797d(
    value: typing.Optional[ZeroTrustAccessApplicationSaasAppCustomClaimSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47ae571f696461fa530e0b47d1efc7aaf34c0de513625409293c9d3e6bab9f3(
    *,
    return_access_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    return_id_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a23c8631a7e3ced1913740badd25b182d8e96d450b36a5e36990ed6998cb39f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef48dd0a1ce07f0e0b2c393cc41e88e4a85a50ad9de47aaaddfb48813152bd08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260a94b192ac278986ffa721cb0b4f3ff84c8bc3d6fdea12710e86b6eaaef709(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56656c00569825803da3de6dcf7b591d4680f70dacf3bf0817373f6058bac6da(
    value: typing.Optional[ZeroTrustAccessApplicationSaasAppHybridAndImplicitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a299894c97079b51266055689b9e4f413f7ec554eaa28304f60d4ad33f8534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b50850d7ccea4a709ce1bb6660a8e6e5417f6c414de9dfbcfdf6d532f99eea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7ab4a71b08357c4ca937bd7fac3142284beded6fb7ccea5473428054cd3867(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05d9069f697f1fad08e514498ad4220505e56b347bbd9357dd86f625f57f4a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fb0dce2094353bf862ac6932bf9a358d1d4f375d33d16593dca55a165db522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2640f51230ba19fce15c46e2ca579ade81a67ca68c266692d4174e69fd3ca5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11875e0247acdfcedf65d6a888a32e27757d31f852c7c7c8214f36bd0b3b1d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b350e2f52aebbe4c357cf90efd09abbb3dd37db61e4bf714fefe6c1e6dd7b6f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c732105ba0603af66f74ca876094fdeb8c6ba86f3ced4e967288ff0173389d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4129f222924b86431073e40812a1aa6aa8aee21ea5cbcf64df4d58c8579b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655028a2de9e44243e176070fd158b5821b08b9798d15c1be60d5eeead641b9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131893fce395bbcbb766470e23b5d8bc39b238559b280a60d56ba0f2f838ca9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cacd17173b2abbb9ff19c26687b485dbc7fe5681ef84dd6fbbcdd5e24337b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cd0c18ac4021f516a3a8ef427725b25c2b20992909b7dbc96d1a9a84c7770d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d7290629a442ba66a60c36f59f78fd19ce6a87637af9f6ce09210a8fb1648b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7243c8f3682d4a920b5ea40cdb982e43b5bdb0b7306a016a9e093f32e5eda7f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5464e78b786e5658452e709a73cf8396eed6793e0e379a633c781a840745fe88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae5ccdf2561788d69742c6f9acb2ec59053a3e73d1d5f1f80aef0b9b5183235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218a8e2563fb056ab19958056423e2a894b1bd20729be4fc196ff028d0b23a6f(
    value: typing.Optional[ZeroTrustAccessApplicationSaasApp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6490a881c3f568cc7886ac54fafbddda6b2e5baa040de68f6b2849b00d2638b7(
    *,
    lifetime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6945e22c57afdd29a0169a519dee4996ec1d4e640ef547b23bc4d2a7aa827c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b2ce34c999e6652b9cb7db83c8f51f25a5b07e2360993bd9c028cb0c6c2222(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db220bb25793b4f1b1249504b276ae0053ed11166c9e29c023176614f7832832(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bea666581ad894137de4e91ff78dd4666b788dd70dedb55233c8719fe660bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d161a6cd047dd2d1d1aac1ac7397f9f91fe14c3de1460876f8e6f3f1e3cadb7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e83b2a9a7a3eda2469dbe73dfbefbe03f32707ef4df7299e5f9c8e82d5b868d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da90fd8d48103370542ab0093d7e08de04f63811ee1483e9df37e008ecfc1f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f37139bb87b9b512af5ec8019e31e5d12c9e94b872d3d3f4ee05bea7116ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f4df5778942d62a1fbffda7cf06c517d0fdd87b610a22b8fa5a9b68f4568f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationSaasAppRefreshTokenOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed24ef6d590cd8e473af78f8b33f160fbe048226d28429cb8e2814bfd91eb53(
    *,
    idp_uid: builtins.str,
    remote_uri: builtins.str,
    authentication: typing.Optional[typing.Union[ZeroTrustAccessApplicationScimConfigAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ecb6b1233c4fce4b268366016c523f851dd300b1747ce2599833d502464b7d(
    *,
    scheme: builtins.str,
    authorization_url: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    token: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2092e0de164ec969f7e9ddec8407a11451c0e89c4116013fc145501728612a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049351fa1f185a569f1e81166b431f043268cd038a8cc145170d821c864835db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750b8d1c095c9856fe85bbedee0b3499bad2b4291e9097dc8abe54902ef2c15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc26828b8e083a8a2595bd485dbff30f965d4c5a0b0f07bb87106c8b960b99c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ad05a822425dfb66907635ff1d89c311bfe6f43e728bd0a34d5b3a86d1cc7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd5e83f101be05ab311d697646530558ceacc68e0724e87a80e690e1c537a0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1570f66ad7030069d7e29f3ff32d5adf89b72076ccbd99c7d721f7e395413db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244f3f0a66f77d883bd43bb55d85fd3f7fde7079a5563a43b16600e49e9a3f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f34107877bdcc9ac6d4df827ffb6e8dfca11942720d52e60589eaa7af7d37da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7c7e20bcb9a12ecd78d646245a861c85aab173a15f94db57bf8c6520257bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5e0f6b8dca149d03908fbbc7aada492af864e2312467a9a037556aaa339bff(
    value: typing.Optional[ZeroTrustAccessApplicationScimConfigAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e429138f79298c45e0a4a980b4a1bc857a8c361b3b91254b9c314a97e8081a(
    *,
    schema: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter: typing.Optional[builtins.str] = None,
    operations: typing.Optional[typing.Union[ZeroTrustAccessApplicationScimConfigMappingsOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    strictness: typing.Optional[builtins.str] = None,
    transform_jsonata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4982d85328e485577e71db6ca0ff28bd4d11ed103fe4e751b6865c29edf27b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c12d7ca795066c59b692ad4f51ed06da9a4bbfb1671bcfb9058abce1dbf166d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11722f82c822bd7d3852c62774d61090e29ff5c91dffd7de692dc798a6a6df8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cda44f403d31af0b43b47ab683ca8fe0a9e2252e5b592cd2fdea6ba3c13297b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282cc7e4bc2718f13142a71dc8796a2e16a73d45e66b1f4b5a4978083c5d69d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd5e8b7a787876d92c35a2d24bc410013f73b0c55e8fc95ebd31c3eae5cbaf4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationScimConfigMappings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a09fa54b88dde85f9223922abb1ad6ae627c2f2547b57da96c41a7bd6afac9a(
    *,
    create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe6e3c8fc9d4e2f3170ae5c2ceb74951b2955571764b4c82a0f6bb0ce4272f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d292edfba0d7e3b7a55cc8ace4108ac256e7b720216108aea5114f658c3273(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777ec6d891e7721b04e14edf7fa10e9f357be6ae8bb41f7940fadfc1ce53f997(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7791b72a4522df28341aaf05fb9e6aedfb520b7fb2772b593fa73fcbeb257460(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa06f143a4b3a50d8cd11ef17f7e5fdd9d896da7bb6e6065b6233907d8a6cd4a(
    value: typing.Optional[ZeroTrustAccessApplicationScimConfigMappingsOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0cfbf2de00e251c5d618219bf8ae1c16eb631d3bcb73bdd800083e125a428f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b72c81a9e5cff5cc95e524a0ca8dd864548c4e8e3eda50e28ff65f6724a3aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2230b039da2ffe3bcd776feb5c3f409fa81b60bfe83e319d38372684dff96b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5215af50fc75a0e73ad843e3d866e7405d6025619b93538a5fc263322a27dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fbfb35f18e42455dcd9897ac76fe0a3795ed2ce09a0d173aee5c89c2302d04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b5dd75241fc8639d24bfc70cba7f606f40751b4614d1808cde1347beac7a94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f597ea09f19a498bc840b2423b24294d1e2b77d4259d154703c170544b4578(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationScimConfigMappings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd13586a1dd626fd8881187550aa6b978f5254d1731ed2e496df78824dc7bb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac25c5d91f207d1d973db6b446851bef6fca92aad259cb2078316a20ee88afae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3775745e8c089fcfccac709b3db0b6f61040c230a03b3bc79d4ea941048a425f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2aa79d0def243d84c4d4d28f66f98ec868452092917d912ff50c30f8d2a1e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574933f80f7d7da91678a2b3008b5465fe3e6e53188344329efa68ecfdc57ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5406d8f276e75d039963d97f7874f104345d19f82c913154fed37bd7d26b09f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2bc60a07a514931792b4078fe0dd4797301c6149d73dec0fd7e224ca0851a0(
    value: typing.Optional[ZeroTrustAccessApplicationScimConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c5f95cc6144bb0d1e2e5b734e8baca1534d63b2e34e895e1b853b7e917b04f(
    *,
    port: jsii.Number,
    protocol: builtins.str,
    target_attributes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62177dab3ece260cddeb67aecb9a95abbf1b75a041c89f358a177e6696e730bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f548a3db067bc87929f0721b50f128734ba832335114838cd7e3cea9bdbdfa4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5879327f1788ee3832554f02937a5491bec1fed9f83fab1be99628106ad6b2c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb5fc42c8ea5dbd0629bc52fc476332348ff87a76d5ef05168a623869698e127(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a1af0605f409c28c193e0882c13cb4394d21bf12f82d78104e2de87cd83196(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed3e2bfa0c87cd1fc44be7629b1f403fcee25c6adf7403c3d4119fb2b9703c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70c7a7d4564a84da124d02399b8a0c3ba64b0f1871bea49f2db0b2a41279567(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdfe4436a34c728c31a9ae52d08f087f5a1a4e1431d857ca79491231e44397f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1641fb9b0840e77fea2869966a62fe0826f07b642ad3a16cf31cc6276e522a46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958c0c954dc8468a737ed4baa12f7c419e2f09db7b3e152cce47471e08571229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a185ff462507fd4d2cbf7fac7c32d3e0537ff5260ae4069f0e9d867896d2b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f104209cd6a81efda2be5c187e27d051bd60b40149a480c6005ff1a991bd4f15(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db129bb26de81d9b431ca362f8e1d8493246a32d3c3b7d6ec79f68cb8d459a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2aa47d42928194f7af1f956436f1389140023b5c701867444db1e9e886146ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7061d1c4b92f7261156a585bf764e9c030d523ddbaf672a5fe92d6fa1c3bdcb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82e078727eaea3267ce9a92c56d1e981fef64d558831e8a328d9f9457ca5a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9ff37c3a6470841733c644064260747f95ebfbc78ee6d347f0d63c241a8098(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0222f97f57b77eef417ee153b2cfe3594245fb820f0483adb696fe9818084eb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2757f0483830b7c8fc4c0162f3fc01ba48da17e180c693862a4c870291bf21ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c91996f495047b84c39d77971c792cb49db2d7f122757c7484f19870c8c3d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67645c303bbfd48823fbe70074a6af241a50ba10f9b89658291f3e3c0b2ff42c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a59f2d2a58be5094365412dfb811501f73e37acfc73d7e7e061f9d5e7b0757(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ZeroTrustAccessApplicationTargetCriteriaTargetAttributes]],
) -> None:
    """Type checking stubs"""
    pass
