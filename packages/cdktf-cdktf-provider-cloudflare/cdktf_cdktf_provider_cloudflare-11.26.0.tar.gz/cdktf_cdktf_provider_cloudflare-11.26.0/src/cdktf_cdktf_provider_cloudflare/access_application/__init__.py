r'''
# `cloudflare_access_application`

Refer to the Terraform Registry for docs: [`cloudflare_access_application`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application).
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


class AccessApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application cloudflare_access_application}.'''

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
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
        custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_type: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header_bg_color: typing.Optional[builtins.str] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        landing_page_design: typing.Optional[typing.Union["AccessApplicationLandingPageDesign", typing.Dict[builtins.str, typing.Any]]] = None,
        logo_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        saas_app: typing.Optional[typing.Union["AccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union["AccessApplicationScimConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application cloudflare_access_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#account_id AccessApplication#account_id}
        :param allow_authenticate_via_warp: When set to true, users can authenticate to this application using their WARP session. When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_authenticate_via_warp AccessApplication#allow_authenticate_via_warp}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_idps AccessApplication#allowed_idps}
        :param app_launcher_logo_url: The logo URL of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_logo_url AccessApplication#app_launcher_logo_url}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        :param bg_color: The background color of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#bg_color AccessApplication#bg_color}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#cors_headers AccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_message AccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application via identity based rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_url AccessApplication#custom_deny_url}
        :param custom_non_identity_deny_url: Option that redirects to a custom URL when a user is denied access to the application via non identity rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_non_identity_deny_url AccessApplication#custom_non_identity_deny_url}
        :param custom_pages: The custom pages selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_pages AccessApplication#custom_pages}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#destinations AccessApplication#destinations}
        :param domain: The primary hostname and path that Access will secure. If the app is visible in the App Launcher dashboard, this is the domain that will be displayed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain AccessApplication#domain}
        :param domain_type: The type of the primary domain. Available values: ``public``, ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain_type AccessApplication#domain_type}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        :param footer_links: footer_links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#footer_links AccessApplication#footer_links}
        :param header_bg_color: The background color of the header bar in the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#header_bg_color AccessApplication#header_bg_color}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#id AccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param landing_page_design: landing_page_design block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#landing_page_design AccessApplication#landing_page_design}
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#logo_url AccessApplication#logo_url}
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param options_preflight_bypass: Allows options preflight requests to bypass Access authentication and go directly to the origin. Cannot turn on if cors_headers is set. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#options_preflight_bypass AccessApplication#options_preflight_bypass}
        :param policies: The policies associated with the application, in ascending order of precedence. Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#policies AccessApplication#policies}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saas_app AccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scim_config AccessApplication#scim_config}
        :param self_hosted_domains: List of public domains secured by Access. Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#self_hosted_domains AccessApplication#self_hosted_domains}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#session_duration AccessApplication#session_duration}
        :param skip_app_launcher_login_page: Option to skip the App Launcher landing page. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_app_launcher_login_page AccessApplication#skip_app_launcher_login_page}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_interstitial AccessApplication#skip_interstitial}
        :param tags: The itags associated with the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#tags AccessApplication#tags}
        :param target_criteria: target_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#target_criteria AccessApplication#target_criteria}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#type AccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#zone_id AccessApplication#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b2963f98659b9017b97318b2a37e45b5084f4b60cafaa3bcd97429790c8eb1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessApplicationConfig(
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
        '''Generates CDKTF code for importing a AccessApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessApplication to import.
        :param import_from_id: The id of the existing AccessApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3f1ea026942d7e5ec2b0495b96b60d5ea2689942f1e955caf45dbd6ab75873)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCorsHeaders")
    def put_cors_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0c9359a2094e6a5d995e98fae21fbe1877ef3aca4c5f09eb4d19306fa8750c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsHeaders", [value]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3cdbe33aad4bdc745e21b73c1af29162e4848f926e074d30ec598698728f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putFooterLinks")
    def put_footer_links(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353086e98e96dbcecf2c69eedd880bba115cd7082c09d49047fc126c3ed53284)
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
        :param button_color: The button color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_color AccessApplication#button_color}
        :param button_text_color: The button text color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_text_color AccessApplication#button_text_color}
        :param image_url: The URL of the image to be displayed in the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#image_url AccessApplication#image_url}
        :param message: The message of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#message AccessApplication#message}
        :param title: The title of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#title AccessApplication#title}
        '''
        value = AccessApplicationLandingPageDesign(
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
        custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppCustomAttribute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppCustomClaim", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_filter_regex: typing.Optional[builtins.str] = None,
        hybrid_and_implicit_options: typing.Optional[typing.Union["AccessApplicationSaasAppHybridAndImplicitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_id_format: typing.Optional[builtins.str] = None,
        name_id_transform_jsonata: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token_lifetime: The lifetime of the Access Token after creation. Valid units are ``m`` and ``h``. Must be greater than or equal to 1m and less than or equal to 24h. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#access_token_lifetime AccessApplication#access_token_lifetime}
        :param allow_pkce_without_client_secret: Allow PKCE flow without a client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_pkce_without_client_secret AccessApplication#allow_pkce_without_client_secret}
        :param app_launcher_url: The URL where this applications tile redirects users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_url AccessApplication#app_launcher_url}
        :param auth_type: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auth_type AccessApplication#auth_type}
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#consumer_service_url AccessApplication#consumer_service_url}
        :param custom_attribute: custom_attribute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_attribute AccessApplication#custom_attribute}
        :param custom_claim: custom_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_claim AccessApplication#custom_claim}
        :param default_relay_state: The relay state used if not provided by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#default_relay_state AccessApplication#default_relay_state}
        :param grant_types: The OIDC flows supported by this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#grant_types AccessApplication#grant_types}
        :param group_filter_regex: A regex to filter Cloudflare groups returned in ID token and userinfo endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#group_filter_regex AccessApplication#group_filter_regex}
        :param hybrid_and_implicit_options: hybrid_and_implicit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#hybrid_and_implicit_options AccessApplication#hybrid_and_implicit_options}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_format AccessApplication#name_id_format}
        :param name_id_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_transform_jsonata AccessApplication#name_id_transform_jsonata}
        :param redirect_uris: The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#redirect_uris AccessApplication#redirect_uris}
        :param refresh_token_options: refresh_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#refresh_token_options AccessApplication#refresh_token_options}
        :param saml_attribute_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saml_attribute_transform_jsonata AccessApplication#saml_attribute_transform_jsonata}
        :param scopes: Define the user information shared with access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#sp_entity_id AccessApplication#sp_entity_id}
        '''
        value = AccessApplicationSaasApp(
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
        authentication: typing.Optional[typing.Union["AccessApplicationScimConfigAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationScimConfigMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param idp_uid: The UIDs of the IdP to use as the source for SCIM resources to provision to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#idp_uid AccessApplication#idp_uid}
        :param remote_uri: The base URI for the application's SCIM-compatible API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#remote_uri AccessApplication#remote_uri}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authentication AccessApplication#authentication}
        :param deactivate_on_delete: If false, propagates DELETE requests to the target application for SCIM resources. If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#deactivate_on_delete AccessApplication#deactivate_on_delete}
        :param enabled: Whether SCIM provisioning is turned on for this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enabled AccessApplication#enabled}
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#mappings AccessApplication#mappings}
        '''
        value = AccessApplicationScimConfig(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf59ef93d4ebe08de54f2b8644e0eef8aec5497fc94bc8f20c8c6ec2efc4bf97)
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
    def cors_headers(self) -> "AccessApplicationCorsHeadersList":
        return typing.cast("AccessApplicationCorsHeadersList", jsii.get(self, "corsHeaders"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "AccessApplicationDestinationsList":
        return typing.cast("AccessApplicationDestinationsList", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="footerLinks")
    def footer_links(self) -> "AccessApplicationFooterLinksList":
        return typing.cast("AccessApplicationFooterLinksList", jsii.get(self, "footerLinks"))

    @builtins.property
    @jsii.member(jsii_name="landingPageDesign")
    def landing_page_design(
        self,
    ) -> "AccessApplicationLandingPageDesignOutputReference":
        return typing.cast("AccessApplicationLandingPageDesignOutputReference", jsii.get(self, "landingPageDesign"))

    @builtins.property
    @jsii.member(jsii_name="saasApp")
    def saas_app(self) -> "AccessApplicationSaasAppOutputReference":
        return typing.cast("AccessApplicationSaasAppOutputReference", jsii.get(self, "saasApp"))

    @builtins.property
    @jsii.member(jsii_name="scimConfig")
    def scim_config(self) -> "AccessApplicationScimConfigOutputReference":
        return typing.cast("AccessApplicationScimConfigOutputReference", jsii.get(self, "scimConfig"))

    @builtins.property
    @jsii.member(jsii_name="targetCriteria")
    def target_criteria(self) -> "AccessApplicationTargetCriteriaList":
        return typing.cast("AccessApplicationTargetCriteriaList", jsii.get(self, "targetCriteria"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]], jsii.get(self, "corsHeadersInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationDestinations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationDestinations"]]], jsii.get(self, "destinationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationFooterLinks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationFooterLinks"]]], jsii.get(self, "footerLinksInput"))

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
    ) -> typing.Optional["AccessApplicationLandingPageDesign"]:
        return typing.cast(typing.Optional["AccessApplicationLandingPageDesign"], jsii.get(self, "landingPageDesignInput"))

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
    def saas_app_input(self) -> typing.Optional["AccessApplicationSaasApp"]:
        return typing.cast(typing.Optional["AccessApplicationSaasApp"], jsii.get(self, "saasAppInput"))

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttributeInput")
    def same_site_cookie_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sameSiteCookieAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="scimConfigInput")
    def scim_config_input(self) -> typing.Optional["AccessApplicationScimConfig"]:
        return typing.cast(typing.Optional["AccessApplicationScimConfig"], jsii.get(self, "scimConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteria"]]], jsii.get(self, "targetCriteriaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__81fb38f689b4bf068fc2e8ba83e0a3ec1a53465fe9ca9bf20ef28753a9f80251)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8618f77c49f6cc0aa7f0027cb90575ee8a8c18ddd9ef18d5a5678f19be2914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAuthenticateViaWarp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIdps")
    def allowed_idps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIdps"))

    @allowed_idps.setter
    def allowed_idps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daff490d3a8108f46fe8affbe607ed3bfce7f0caa97c3a01158863a2d9b81e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIdps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appLauncherLogoUrl")
    def app_launcher_logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLauncherLogoUrl"))

    @app_launcher_logo_url.setter
    def app_launcher_logo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3942e51ffa8e0521e41664e3706ee0d24b9ace1acd8fda40a1ed132fed51d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fe33b6a3e0de6c5d2332cddc4e94399f81b3f96589f00d5cea096ca5c90e89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02da31929754ab70993542e7f44f5e3b8ff2a4113ea0e7fc09dccad505e190e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRedirectToIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgColor")
    def bg_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgColor"))

    @bg_color.setter
    def bg_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1cf66f6d38abaa184e9b102c5bed0a1bcbad3e59e9238776dc720432d89adc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDenyMessage")
    def custom_deny_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyMessage"))

    @custom_deny_message.setter
    def custom_deny_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7394b2b4e1199550fbe6375395d12db57b5a15a49a4d5b7355d6ce5ad25636e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customDenyUrl")
    def custom_deny_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDenyUrl"))

    @custom_deny_url.setter
    def custom_deny_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bda6e3a2399b050e18d5c2bc8f4883cf54b73d8211f3d0847551f970d6b384e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDenyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customNonIdentityDenyUrl")
    def custom_non_identity_deny_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customNonIdentityDenyUrl"))

    @custom_non_identity_deny_url.setter
    def custom_non_identity_deny_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c02dc85ef48581d4ee221e7d19a805202658fbcf18e9fba8a41c92d7b95d2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customNonIdentityDenyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPages")
    def custom_pages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customPages"))

    @custom_pages.setter
    def custom_pages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c473e90aa30a665e643314d41d7fb6411c390c872477fb3ae366ca7054ca72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcbe163ed94bb0a50cb8b1b9b52ea152aa192b9bd50115601e6ab1b87eaf861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainType")
    def domain_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainType"))

    @domain_type.setter
    def domain_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee783452efee50ba00c22af7913e4238a909caf192c62897899f1fcc8c62df3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ffea86ba305f92fcd8ef5768d2698c4bf9c262d3a7e35de9c4bbf7711be2159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBindingCookie", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerBgColor")
    def header_bg_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerBgColor"))

    @header_bg_color.setter
    def header_bg_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93aa224e73174428e31a6e1e5ee5c604aeea58149044bc5361f6d0dd9064f31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7b7a56cc0c2523d37beeaca9d4af0ffe258c84ad7cd8666034d44c91b2c0a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpOnlyCookieAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cee610faa04b0d8e65aad04b0e960f1a472af48d19258d665b5edfc30e57e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoUrl")
    def logo_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoUrl"))

    @logo_url.setter
    def logo_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94205b9b871f765a94dff73949e655473bf7b6ffab02f41b2a507b924040f1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408052199c5db90c8698c809b74ffc55459b674605e439d3b3bfd8a083255a13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48d28f4f6f511c05351cf4007acb73b1c10f4e879d811f8418309e428ee2f41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionsPreflightBypass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "policies"))

    @policies.setter
    def policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3b5a29b8213df2135c08e8acb42a3b3e4ef2a2d290881717559e3b6d338f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sameSiteCookieAttribute")
    def same_site_cookie_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sameSiteCookieAttribute"))

    @same_site_cookie_attribute.setter
    def same_site_cookie_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a95c47163bc493ca9389335db25497d901b8dedf1f1549f91f1f323ea93a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sameSiteCookieAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selfHostedDomains")
    def self_hosted_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "selfHostedDomains"))

    @self_hosted_domains.setter
    def self_hosted_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08559ba467d164f4458e22395f55bf8245e62c4b82fb8455ec3e36241fb1e350)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad3bbb24317d5f07a9fb5037e763a244642bebdc8fa18f8d948e52201c04187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAuth401Redirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionDuration"))

    @session_duration.setter
    def session_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfb91cb0ee9996051ba552f920aa96e9da21960ed72cf49353e36a46107d982)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec60611c612d24adf5943874c42fd6fb6eac7715cc9771a7a22bb392fb75c3d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b86799f85043068c1b6ac6d68b67ebdd5dc15341cb709a8eeccbecf097cf147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipInterstitial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2353fa1a2102657035c34ddc9b9776945570491fe11231c033f4ed41e05eeaf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ac6df2597f216a2f0ef7d91eff615dd9bd4f92bf47b2a9e51dec9e2a97df20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f33c40394937d1eb21e9c367c96d3212115f53970a6ffb9db1ab2ecac777b19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationConfig",
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
class AccessApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationCorsHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_deny_message: typing.Optional[builtins.str] = None,
        custom_deny_url: typing.Optional[builtins.str] = None,
        custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
        custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_type: typing.Optional[builtins.str] = None,
        enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationFooterLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header_bg_color: typing.Optional[builtins.str] = None,
        http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        landing_page_design: typing.Optional[typing.Union["AccessApplicationLandingPageDesign", typing.Dict[builtins.str, typing.Any]]] = None,
        logo_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        saas_app: typing.Optional[typing.Union["AccessApplicationSaasApp", typing.Dict[builtins.str, typing.Any]]] = None,
        same_site_cookie_attribute: typing.Optional[builtins.str] = None,
        scim_config: typing.Optional[typing.Union["AccessApplicationScimConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_duration: typing.Optional[builtins.str] = None,
        skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationTargetCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param account_id: The account identifier to target for the resource. Conflicts with ``zone_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#account_id AccessApplication#account_id}
        :param allow_authenticate_via_warp: When set to true, users can authenticate to this application using their WARP session. When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_authenticate_via_warp AccessApplication#allow_authenticate_via_warp}
        :param allowed_idps: The identity providers selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_idps AccessApplication#allowed_idps}
        :param app_launcher_logo_url: The logo URL of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_logo_url AccessApplication#app_launcher_logo_url}
        :param app_launcher_visible: Option to show/hide applications in App Launcher. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        :param auto_redirect_to_identity: Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        :param bg_color: The background color of the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#bg_color AccessApplication#bg_color}
        :param cors_headers: cors_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#cors_headers AccessApplication#cors_headers}
        :param custom_deny_message: Option that returns a custom error message when a user is denied access to the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_message AccessApplication#custom_deny_message}
        :param custom_deny_url: Option that redirects to a custom URL when a user is denied access to the application via identity based rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_url AccessApplication#custom_deny_url}
        :param custom_non_identity_deny_url: Option that redirects to a custom URL when a user is denied access to the application via non identity rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_non_identity_deny_url AccessApplication#custom_non_identity_deny_url}
        :param custom_pages: The custom pages selected for the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_pages AccessApplication#custom_pages}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#destinations AccessApplication#destinations}
        :param domain: The primary hostname and path that Access will secure. If the app is visible in the App Launcher dashboard, this is the domain that will be displayed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain AccessApplication#domain}
        :param domain_type: The type of the primary domain. Available values: ``public``, ``private``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain_type AccessApplication#domain_type}
        :param enable_binding_cookie: Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        :param footer_links: footer_links block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#footer_links AccessApplication#footer_links}
        :param header_bg_color: The background color of the header bar in the app launcher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#header_bg_color AccessApplication#header_bg_color}
        :param http_only_cookie_attribute: Option to add the ``HttpOnly`` cookie flag to access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#id AccessApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param landing_page_design: landing_page_design block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#landing_page_design AccessApplication#landing_page_design}
        :param logo_url: Image URL for the logo shown in the app launcher dashboard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#logo_url AccessApplication#logo_url}
        :param name: Friendly name of the Access Application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param options_preflight_bypass: Allows options preflight requests to bypass Access authentication and go directly to the origin. Cannot turn on if cors_headers is set. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#options_preflight_bypass AccessApplication#options_preflight_bypass}
        :param policies: The policies associated with the application, in ascending order of precedence. Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#policies AccessApplication#policies}
        :param saas_app: saas_app block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saas_app AccessApplication#saas_app}
        :param same_site_cookie_attribute: Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        :param scim_config: scim_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scim_config AccessApplication#scim_config}
        :param self_hosted_domains: List of public domains secured by Access. Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#self_hosted_domains AccessApplication#self_hosted_domains}
        :param service_auth401_redirect: Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        :param session_duration: How often a user will be forced to re-authorise. Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#session_duration AccessApplication#session_duration}
        :param skip_app_launcher_login_page: Option to skip the App Launcher landing page. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_app_launcher_login_page AccessApplication#skip_app_launcher_login_page}
        :param skip_interstitial: Option to skip the authorization interstitial when using the CLI. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_interstitial AccessApplication#skip_interstitial}
        :param tags: The itags associated with the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#tags AccessApplication#tags}
        :param target_criteria: target_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#target_criteria AccessApplication#target_criteria}
        :param type: The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#type AccessApplication#type}
        :param zone_id: The zone identifier to target for the resource. Conflicts with ``account_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#zone_id AccessApplication#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(landing_page_design, dict):
            landing_page_design = AccessApplicationLandingPageDesign(**landing_page_design)
        if isinstance(saas_app, dict):
            saas_app = AccessApplicationSaasApp(**saas_app)
        if isinstance(scim_config, dict):
            scim_config = AccessApplicationScimConfig(**scim_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f785d33e1451f1cf27417eb2776a2d793dff777b28167e528be38cf2a13a8faa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#account_id AccessApplication#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_authenticate_via_warp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, users can authenticate to this application using their WARP session.

        When set to false this application will always require direct IdP authentication. This setting always overrides the organization setting for WARP authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_authenticate_via_warp AccessApplication#allow_authenticate_via_warp}
        '''
        result = self._values.get("allow_authenticate_via_warp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_idps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The identity providers selected for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_idps AccessApplication#allowed_idps}
        '''
        result = self._values.get("allowed_idps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def app_launcher_logo_url(self) -> typing.Optional[builtins.str]:
        '''The logo URL of the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_logo_url AccessApplication#app_launcher_logo_url}
        '''
        result = self._values.get("app_launcher_logo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_launcher_visible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to show/hide applications in App Launcher. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_visible AccessApplication#app_launcher_visible}
        '''
        result = self._values.get("app_launcher_visible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_redirect_to_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip identity provider selection if only one is configured in ``allowed_idps``. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auto_redirect_to_identity AccessApplication#auto_redirect_to_identity}
        '''
        result = self._values.get("auto_redirect_to_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bg_color(self) -> typing.Optional[builtins.str]:
        '''The background color of the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#bg_color AccessApplication#bg_color}
        '''
        result = self._values.get("bg_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]]:
        '''cors_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#cors_headers AccessApplication#cors_headers}
        '''
        result = self._values.get("cors_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationCorsHeaders"]]], result)

    @builtins.property
    def custom_deny_message(self) -> typing.Optional[builtins.str]:
        '''Option that returns a custom error message when a user is denied access to the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_message AccessApplication#custom_deny_message}
        '''
        result = self._values.get("custom_deny_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_deny_url(self) -> typing.Optional[builtins.str]:
        '''Option that redirects to a custom URL when a user is denied access to the application via identity based rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_deny_url AccessApplication#custom_deny_url}
        '''
        result = self._values.get("custom_deny_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_non_identity_deny_url(self) -> typing.Optional[builtins.str]:
        '''Option that redirects to a custom URL when a user is denied access to the application via non identity rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_non_identity_deny_url AccessApplication#custom_non_identity_deny_url}
        '''
        result = self._values.get("custom_non_identity_deny_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_pages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The custom pages selected for the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_pages AccessApplication#custom_pages}
        '''
        result = self._values.get("custom_pages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationDestinations"]]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#destinations AccessApplication#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationDestinations"]]], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The primary hostname and path that Access will secure.

        If the app is visible in the App Launcher dashboard, this is the domain that will be displayed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain AccessApplication#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_type(self) -> typing.Optional[builtins.str]:
        '''The type of the primary domain. Available values: ``public``, ``private``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#domain_type AccessApplication#domain_type}
        '''
        result = self._values.get("domain_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_binding_cookie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to provide increased security against compromised authorization tokens and CSRF attacks by requiring an additional "binding" cookie on requests.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enable_binding_cookie AccessApplication#enable_binding_cookie}
        '''
        result = self._values.get("enable_binding_cookie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def footer_links(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationFooterLinks"]]]:
        '''footer_links block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#footer_links AccessApplication#footer_links}
        '''
        result = self._values.get("footer_links")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationFooterLinks"]]], result)

    @builtins.property
    def header_bg_color(self) -> typing.Optional[builtins.str]:
        '''The background color of the header bar in the app launcher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#header_bg_color AccessApplication#header_bg_color}
        '''
        result = self._values.get("header_bg_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_only_cookie_attribute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to add the ``HttpOnly`` cookie flag to access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#http_only_cookie_attribute AccessApplication#http_only_cookie_attribute}
        '''
        result = self._values.get("http_only_cookie_attribute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#id AccessApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def landing_page_design(
        self,
    ) -> typing.Optional["AccessApplicationLandingPageDesign"]:
        '''landing_page_design block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#landing_page_design AccessApplication#landing_page_design}
        '''
        result = self._values.get("landing_page_design")
        return typing.cast(typing.Optional["AccessApplicationLandingPageDesign"], result)

    @builtins.property
    def logo_url(self) -> typing.Optional[builtins.str]:
        '''Image URL for the logo shown in the app launcher dashboard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#logo_url AccessApplication#logo_url}
        '''
        result = self._values.get("logo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Friendly name of the Access Application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options_preflight_bypass(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows options preflight requests to bypass Access authentication and go directly to the origin.

        Cannot turn on if cors_headers is set. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#options_preflight_bypass AccessApplication#options_preflight_bypass}
        '''
        result = self._values.get("options_preflight_bypass")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The policies associated with the application, in ascending order of precedence.

        Warning: Do not use this field while you still have this application ID referenced as ``application_id`` in any ``cloudflare_access_policy`` resource, as it can result in an inconsistent state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#policies AccessApplication#policies}
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def saas_app(self) -> typing.Optional["AccessApplicationSaasApp"]:
        '''saas_app block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saas_app AccessApplication#saas_app}
        '''
        result = self._values.get("saas_app")
        return typing.cast(typing.Optional["AccessApplicationSaasApp"], result)

    @builtins.property
    def same_site_cookie_attribute(self) -> typing.Optional[builtins.str]:
        '''Defines the same-site cookie setting for access tokens. Available values: ``none``, ``lax``, ``strict``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#same_site_cookie_attribute AccessApplication#same_site_cookie_attribute}
        '''
        result = self._values.get("same_site_cookie_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scim_config(self) -> typing.Optional["AccessApplicationScimConfig"]:
        '''scim_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scim_config AccessApplication#scim_config}
        '''
        result = self._values.get("scim_config")
        return typing.cast(typing.Optional["AccessApplicationScimConfig"], result)

    @builtins.property
    def self_hosted_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of public domains secured by Access.

        Only present for self_hosted, vnc, and ssh applications. Always includes the value set as ``domain``. Deprecated in favor of ``destinations`` and will be removed in the next major version. Conflicts with ``destinations``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#self_hosted_domains AccessApplication#self_hosted_domains}
        '''
        result = self._values.get("self_hosted_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_auth401_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to return a 401 status code in service authentication rules on failed requests. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#service_auth_401_redirect AccessApplication#service_auth_401_redirect}
        '''
        result = self._values.get("service_auth401_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        '''How often a user will be forced to re-authorise.

        Must be in the format ``48h`` or ``2h45m``. Defaults to ``24h``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#session_duration AccessApplication#session_duration}
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_app_launcher_login_page(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip the App Launcher landing page. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_app_launcher_login_page AccessApplication#skip_app_launcher_login_page}
        '''
        result = self._values.get("skip_app_launcher_login_page")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_interstitial(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Option to skip the authorization interstitial when using the CLI. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#skip_interstitial AccessApplication#skip_interstitial}
        '''
        result = self._values.get("skip_interstitial")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The itags associated with the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#tags AccessApplication#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteria"]]]:
        '''target_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#target_criteria AccessApplication#target_criteria}
        '''
        result = self._values.get("target_criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteria"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The application type. Available values: ``app_launcher``, ``bookmark``, ``biso``, ``dash_sso``, ``saas``, ``self_hosted``, ``ssh``, ``vnc``, ``warp``, ``infrastructure``. Defaults to ``self_hosted``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#type AccessApplication#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. Conflicts with ``account_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#zone_id AccessApplication#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeaders",
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
class AccessApplicationCorsHeaders:
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
        :param allow_all_headers: Value to determine whether all HTTP headers are exposed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_headers AccessApplication#allow_all_headers}
        :param allow_all_methods: Value to determine whether all methods are exposed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_methods AccessApplication#allow_all_methods}
        :param allow_all_origins: Value to determine whether all origins are permitted to make CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_origins AccessApplication#allow_all_origins}
        :param allow_credentials: Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_credentials AccessApplication#allow_credentials}
        :param allowed_headers: List of HTTP headers to expose via CORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_headers AccessApplication#allowed_headers}
        :param allowed_methods: List of methods to expose via CORS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_methods AccessApplication#allowed_methods}
        :param allowed_origins: List of origins permitted to make CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_origins AccessApplication#allowed_origins}
        :param max_age: The maximum time a preflight request will be cached. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#max_age AccessApplication#max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae525a77bbd533b13658910162a82a7ed82713ce55fbce6efb2802432bd142ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_headers AccessApplication#allow_all_headers}
        '''
        result = self._values.get("allow_all_headers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_methods(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all methods are exposed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_methods AccessApplication#allow_all_methods}
        '''
        result = self._values.get("allow_all_methods")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_all_origins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine whether all origins are permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_all_origins AccessApplication#allow_all_origins}
        '''
        result = self._values.get("allow_all_origins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Value to determine if credentials (cookies, authorization headers, or TLS client certificates) are included with requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_credentials AccessApplication#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of HTTP headers to expose via CORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_headers AccessApplication#allowed_headers}
        '''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of methods to expose via CORS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_methods AccessApplication#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of origins permitted to make CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allowed_origins AccessApplication#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''The maximum time a preflight request will be cached.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#max_age AccessApplication#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationCorsHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationCorsHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa79530a53dc744124aeaa81632fbdff14a0c4535f89c37afd43ab415cf95406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessApplicationCorsHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9b295611563f5e8579389c0b30ac3bf53a4e5471f1f6906f361865e1f6d68f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationCorsHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f63511a0bcc23c92f8a3b522588cef9af4c9489d92aa783dbc643495ee3a006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5991c119e726e4e5bae94364d64d111ba5d06dc1fd9a77feeef6241923a1b94c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed799de136d9a06f6402f513b16198e0f010bfa196b8637c9b9f3a949842696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f784385a2e46f6e296c6f09c5dd838571dd28c3c939ef8fe647709d9c6b0fbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationCorsHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationCorsHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c91640a7618248ee2dfbc3c623b9f3d2ccaf579d2752459b82e8c1069a4b359b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3400b2ef69eb057e299d971eff385016e19ae0c0fb70f69517fb2389bf4455f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe554ac39141e522d8cea4b0d84ca98b7e0c53123791c7cdc321b0a2a08c5f1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791c3f6bfef6cb602668374e7ae4047e3cfe4fc8175da1ef5ef7b9f90146a893)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df0cb5c457ec28d6691034d2841ed4bb6cde403ab39fc573324082e69e28e0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d5f5968daf5e6d30f2140162a6148b40fadf726eae33a4a24238a304102543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19571719f469919945233bc1181996c44217f31151077b2376da3c869255841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9790848826046a2cbfaf9752da2eac0aaf648d202e86c384d87ff3c8a5f41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6437b4b77a62619bca135ac9848d2ea144d0abbfa730ca8b0efe1bb71cae125d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationCorsHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationCorsHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationCorsHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f6f5c209667b44cb9092177c7fc64e8a78842aad5f7b1d5d1deb26e1c660cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationDestinations",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "type": "type"},
)
class AccessApplicationDestinations:
    def __init__(
        self,
        *,
        uri: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The URI of the destination. Public destinations can include a domain and path with wildcards. Private destinations are an early access feature and gated behind a feature flag. Private destinations support private IPv4, IPv6, and Server Name Indications (SNI) with optional port ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#uri AccessApplication#uri}
        :param type: The destination type. Available values: ``public``, ``private``. Defaults to ``public``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#type AccessApplication#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04e04dfcccae87efa038ec162df969c0cec439f4b19117ed1ea4473bfe83a7d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#uri AccessApplication#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The destination type. Available values: ``public``, ``private``. Defaults to ``public``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#type AccessApplication#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b9b340d37f4019786ef2d54ef37b1b6e9a5014f49ed4345137d74dc26340a7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessApplicationDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4617120dcf068683b8d898e49640ae9b0d78aee948217002c2bc4c69a829c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5ea431610297d82419116fc0aa1c65f4534d45970cf0e009bc7d3461e5a0c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e77810d4487b59c55871e8521f299f468df756ac081d7bbf7443e6b8e8a4e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ba3b44ada26ab10568e96d9e28412c4965002786f089a4995b151a91d12d973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0b4395a11057b9c1f78b0579f272ce85a8ff4bb8870aa44867497f69c06d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecce3a9b32c81ed197480cc2f8577c26d329c5f19058c07fffe749b90b908b6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0053c5dbb4e9f035f41a5dcad5ec5b54e71858d5e85602eab02c8256598b3268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c34895f7e0a79b0c5ba8dcf66629f92eb272169a2abfd550422ff466698105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e69386f002a02b6676b11a7010491c49d3a3583b5d704c2a789e3c0faad7a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationFooterLinks",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class AccessApplicationFooterLinks:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the footer link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param url: The URL of the footer link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#url AccessApplication#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a283918f835a005a2c46dca747b7b9a44b7593c2aff93d5e6fd63bcfe704cdea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL of the footer link.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#url AccessApplication#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationFooterLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationFooterLinksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationFooterLinksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5355d081c675ef6b32d361cfa3957ba955f2b6c44d72d129c50fe89aaaa8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessApplicationFooterLinksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212cd76d3e6b14aea11265a67d5974e157b174235cb409a102d49f6f71ead33d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationFooterLinksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e5a3c3c870b2af8d1b5d84335cf65a9267fc93202b299cfdfa1717d8f9f2ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f403f07c629c548c1b1e949638dc22d9ccef88f564cf313e70782a6a567a13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83114e3cfa9789ecb7b50ca8c843bbc95d34a50f296602de8045e98ecb0801c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationFooterLinks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationFooterLinks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationFooterLinks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea976940ab4e0525062237dbfb91dc1e58d974df733e4d99f218079057bd5d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationFooterLinksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationFooterLinksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36f95bb5a2d746ee03d9500474665f0876c8a3e681eca02ccca265e7e5a1c95e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f32e7f5a8c0a097ba230d28d9fd33f4f18dbcbd96d94718e321fb8fc8a769498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edca4c3b8c7950e65a971f288e9c04a769bda673153ed00b1a543436350fce6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationFooterLinks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationFooterLinks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationFooterLinks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20ddb59f250ffa10b01f057607e8aa08137620c339bdb2a8fe11d7af0983c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationLandingPageDesign",
    jsii_struct_bases=[],
    name_mapping={
        "button_color": "buttonColor",
        "button_text_color": "buttonTextColor",
        "image_url": "imageUrl",
        "message": "message",
        "title": "title",
    },
)
class AccessApplicationLandingPageDesign:
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
        :param button_color: The button color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_color AccessApplication#button_color}
        :param button_text_color: The button text color of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_text_color AccessApplication#button_text_color}
        :param image_url: The URL of the image to be displayed in the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#image_url AccessApplication#image_url}
        :param message: The message of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#message AccessApplication#message}
        :param title: The title of the landing page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#title AccessApplication#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa34602f22fd0644bebc46d6fd3826bf2ecddecc255937ca6d87aeeb99020319)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_color AccessApplication#button_color}
        '''
        result = self._values.get("button_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def button_text_color(self) -> typing.Optional[builtins.str]:
        '''The button text color of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#button_text_color AccessApplication#button_text_color}
        '''
        result = self._values.get("button_text_color")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the image to be displayed in the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#image_url AccessApplication#image_url}
        '''
        result = self._values.get("image_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''The message of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#message AccessApplication#message}
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''The title of the landing page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#title AccessApplication#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationLandingPageDesign(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationLandingPageDesignOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationLandingPageDesignOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4563866f29e42b2a228ea06df2d61bf5b7a55c2536457088d85a4ac5bdc0b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a4a145464d5dc4a94d3fa02702bf2d4b1c6949fd5c34d0f96bd64ad53afb98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buttonColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buttonTextColor")
    def button_text_color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buttonTextColor"))

    @button_text_color.setter
    def button_text_color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6894bcadefe5e7b50af83e28dbc8aca4df687cb6a2b173487361818bec46cb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buttonTextColor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUrl")
    def image_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUrl"))

    @image_url.setter
    def image_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9894872321eb19f8d71edd0450b37711bf488a5ddf25e607cf7f0c62b430484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @message.setter
    def message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e727e9c0ef0557e103a198910f5ad1e043b9af07dec27e382634ffe5be77c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "message", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75aa9cb97f24af767a167f524c3c7a61a8785d3a89adfa35cf43f4e66c17fc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessApplicationLandingPageDesign]:
        return typing.cast(typing.Optional[AccessApplicationLandingPageDesign], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationLandingPageDesign],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b148ba89a7a77ac870a25c31d352252c9dced333606de93526517ebc5aef2c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasApp",
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
class AccessApplicationSaasApp:
    def __init__(
        self,
        *,
        access_token_lifetime: typing.Optional[builtins.str] = None,
        allow_pkce_without_client_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        app_launcher_url: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        consumer_service_url: typing.Optional[builtins.str] = None,
        custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppCustomAttribute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppCustomClaim", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_relay_state: typing.Optional[builtins.str] = None,
        grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_filter_regex: typing.Optional[builtins.str] = None,
        hybrid_and_implicit_options: typing.Optional[typing.Union["AccessApplicationSaasAppHybridAndImplicitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name_id_format: typing.Optional[builtins.str] = None,
        name_id_transform_jsonata: typing.Optional[builtins.str] = None,
        redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        sp_entity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_token_lifetime: The lifetime of the Access Token after creation. Valid units are ``m`` and ``h``. Must be greater than or equal to 1m and less than or equal to 24h. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#access_token_lifetime AccessApplication#access_token_lifetime}
        :param allow_pkce_without_client_secret: Allow PKCE flow without a client secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_pkce_without_client_secret AccessApplication#allow_pkce_without_client_secret}
        :param app_launcher_url: The URL where this applications tile redirects users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_url AccessApplication#app_launcher_url}
        :param auth_type: **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auth_type AccessApplication#auth_type}
        :param consumer_service_url: The service provider's endpoint that is responsible for receiving and parsing a SAML assertion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#consumer_service_url AccessApplication#consumer_service_url}
        :param custom_attribute: custom_attribute block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_attribute AccessApplication#custom_attribute}
        :param custom_claim: custom_claim block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_claim AccessApplication#custom_claim}
        :param default_relay_state: The relay state used if not provided by the identity provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#default_relay_state AccessApplication#default_relay_state}
        :param grant_types: The OIDC flows supported by this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#grant_types AccessApplication#grant_types}
        :param group_filter_regex: A regex to filter Cloudflare groups returned in ID token and userinfo endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#group_filter_regex AccessApplication#group_filter_regex}
        :param hybrid_and_implicit_options: hybrid_and_implicit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#hybrid_and_implicit_options AccessApplication#hybrid_and_implicit_options}
        :param name_id_format: The format of the name identifier sent to the SaaS application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_format AccessApplication#name_id_format}
        :param name_id_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_transform_jsonata AccessApplication#name_id_transform_jsonata}
        :param redirect_uris: The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#redirect_uris AccessApplication#redirect_uris}
        :param refresh_token_options: refresh_token_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#refresh_token_options AccessApplication#refresh_token_options}
        :param saml_attribute_transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saml_attribute_transform_jsonata AccessApplication#saml_attribute_transform_jsonata}
        :param scopes: Define the user information shared with access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        :param sp_entity_id: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#sp_entity_id AccessApplication#sp_entity_id}
        '''
        if isinstance(hybrid_and_implicit_options, dict):
            hybrid_and_implicit_options = AccessApplicationSaasAppHybridAndImplicitOptions(**hybrid_and_implicit_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cefbcedc5818578827cb55f910f5dea7e97d62fc19dd39c031f17cb5f5aab3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#access_token_lifetime AccessApplication#access_token_lifetime}
        '''
        result = self._values.get("access_token_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_pkce_without_client_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow PKCE flow without a client secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#allow_pkce_without_client_secret AccessApplication#allow_pkce_without_client_secret}
        '''
        result = self._values.get("allow_pkce_without_client_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def app_launcher_url(self) -> typing.Optional[builtins.str]:
        '''The URL where this applications tile redirects users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#app_launcher_url AccessApplication#app_launcher_url}
        '''
        result = self._values.get("app_launcher_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''**Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#auth_type AccessApplication#auth_type}
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_service_url(self) -> typing.Optional[builtins.str]:
        '''The service provider's endpoint that is responsible for receiving and parsing a SAML assertion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#consumer_service_url AccessApplication#consumer_service_url}
        '''
        result = self._values.get("consumer_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_attribute(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppCustomAttribute"]]]:
        '''custom_attribute block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_attribute AccessApplication#custom_attribute}
        '''
        result = self._values.get("custom_attribute")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppCustomAttribute"]]], result)

    @builtins.property
    def custom_claim(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppCustomClaim"]]]:
        '''custom_claim block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#custom_claim AccessApplication#custom_claim}
        '''
        result = self._values.get("custom_claim")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppCustomClaim"]]], result)

    @builtins.property
    def default_relay_state(self) -> typing.Optional[builtins.str]:
        '''The relay state used if not provided by the identity provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#default_relay_state AccessApplication#default_relay_state}
        '''
        result = self._values.get("default_relay_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grant_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The OIDC flows supported by this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#grant_types AccessApplication#grant_types}
        '''
        result = self._values.get("grant_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_filter_regex(self) -> typing.Optional[builtins.str]:
        '''A regex to filter Cloudflare groups returned in ID token and userinfo endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#group_filter_regex AccessApplication#group_filter_regex}
        '''
        result = self._values.get("group_filter_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hybrid_and_implicit_options(
        self,
    ) -> typing.Optional["AccessApplicationSaasAppHybridAndImplicitOptions"]:
        '''hybrid_and_implicit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#hybrid_and_implicit_options AccessApplication#hybrid_and_implicit_options}
        '''
        result = self._values.get("hybrid_and_implicit_options")
        return typing.cast(typing.Optional["AccessApplicationSaasAppHybridAndImplicitOptions"], result)

    @builtins.property
    def name_id_format(self) -> typing.Optional[builtins.str]:
        '''The format of the name identifier sent to the SaaS application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_format AccessApplication#name_id_format}
        '''
        result = self._values.get("name_id_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_id_transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into a NameID value for its SAML assertion. This expression should evaluate to a singular string. The output of this expression can override the ``name_id_format`` setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_id_transform_jsonata AccessApplication#name_id_transform_jsonata}
        '''
        result = self._values.get("name_id_transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permitted URL's for Cloudflare to return Authorization codes and Access/ID tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#redirect_uris AccessApplication#redirect_uris}
        '''
        result = self._values.get("redirect_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def refresh_token_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppRefreshTokenOptions"]]]:
        '''refresh_token_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#refresh_token_options AccessApplication#refresh_token_options}
        '''
        result = self._values.get("refresh_token_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppRefreshTokenOptions"]]], result)

    @builtins.property
    def saml_attribute_transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms an application's user identities into attribute assertions in the SAML response. The expression can transform id, email, name, and groups values. It can also transform fields listed in the saml_attributes or oidc_fields of the identity provider used to authenticate. The output of this expression must be a JSON object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#saml_attribute_transform_jsonata AccessApplication#saml_attribute_transform_jsonata}
        '''
        result = self._values.get("saml_attribute_transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Define the user information shared with access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sp_entity_id(self) -> typing.Optional[builtins.str]:
        '''A globally unique name for an identity or service provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#sp_entity_id AccessApplication#sp_entity_id}
        '''
        result = self._values.get("sp_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasApp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomAttribute",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "friendly_name": "friendlyName",
        "name": "name",
        "name_format": "nameFormat",
        "required": "required",
    },
)
class AccessApplicationSaasAppCustomAttribute:
    def __init__(
        self,
        *,
        source: typing.Union["AccessApplicationSaasAppCustomAttributeSource", typing.Dict[builtins.str, typing.Any]],
        friendly_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_format: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#source AccessApplication#source}
        :param friendly_name: A friendly name for the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#friendly_name AccessApplication#friendly_name}
        :param name: The name of the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param name_format: A globally unique name for an identity or service provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_format AccessApplication#name_format}
        :param required: True if the attribute must be always present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#required AccessApplication#required}
        '''
        if isinstance(source, dict):
            source = AccessApplicationSaasAppCustomAttributeSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47822a0d294ecd1c204d7e43ce43f5c81b4495f154e4d8de423c4ea120d7c080)
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
    def source(self) -> "AccessApplicationSaasAppCustomAttributeSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#source AccessApplication#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("AccessApplicationSaasAppCustomAttributeSource", result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#friendly_name AccessApplication#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_format(self) -> typing.Optional[builtins.str]:
        '''A globally unique name for an identity or service provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_format AccessApplication#name_format}
        '''
        result = self._values.get("name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the attribute must be always present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#required AccessApplication#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppCustomAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppCustomAttributeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomAttributeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5deaa3caa3c864bdcb00a7c435b7ae15521b0d8fbd8b6b7fededa994af5aa5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationSaasAppCustomAttributeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8ade2f4f80a5432c7302f71bdebdea60642416017e167c0f697c1fab9a72b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationSaasAppCustomAttributeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c67459ff871914b79bf01ade3d1f69e2dec200a32a17aeb9e8e2ffef4c5d64e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ecab507188ddfbfcb9a792817b28c3ec9f19eb1409a4f6efdbddd5c340366f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc589e3f3c5b3602f39a53f644e605f4b7c92fb8ae452cedfd033b680a275747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26527e3a1b88ebbdf036684dfc7f2b58892c0e99e198d57ea94ba2aa967b1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationSaasAppCustomAttributeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomAttributeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4db88ced95da88295b22f40e287e904bf65e3fcc0096905b070ec11b69a2df39)
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
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        value = AccessApplicationSaasAppCustomAttributeSource(
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
    def source(self) -> "AccessApplicationSaasAppCustomAttributeSourceOutputReference":
        return typing.cast("AccessApplicationSaasAppCustomAttributeSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["AccessApplicationSaasAppCustomAttributeSource"]:
        return typing.cast(typing.Optional["AccessApplicationSaasAppCustomAttributeSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb32c28a01b2d722459fe7b5cc5d46c1d4fbbb931e4a1ee16bed434d444b830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6696c6834c79882863ec13ff8cd51dbf80bfe1f04d33a4df96c08f63279488d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameFormat")
    def name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameFormat"))

    @name_format.setter
    def name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e8d5b579e56ac8a6c43a0621072d22291e0b8825a15588f20247be75e1a4d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe345dcbe0f490dfef205944df6849210bc382ef052a91c9f933d06b1ff50ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomAttribute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomAttribute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomAttribute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffca61f84302f377b4712b085f9fb553836f560e630b9f0163525ae2801818a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomAttributeSource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "name_by_idp": "nameByIdp"},
)
class AccessApplicationSaasAppCustomAttributeSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eda67f6aa706b9eeedbc74328238a63768a0b8feda2a769ee39f32c8eca67eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_by_idp(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping from IdP ID to claim name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        result = self._values.get("name_by_idp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppCustomAttributeSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppCustomAttributeSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomAttributeSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54953c0eba05eb01197cef40b74f2b3ebef367234083f5c06755c1469632c78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb7a9503bb2eeae21e81557dfbb52a4b860f0e04621cc6ca2793294e50a80fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameByIdp")
    def name_by_idp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nameByIdp"))

    @name_by_idp.setter
    def name_by_idp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ecb5140ac36afc1ba0f51b74b9688b86df647050772d58be91f1feae7ebda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameByIdp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessApplicationSaasAppCustomAttributeSource]:
        return typing.cast(typing.Optional[AccessApplicationSaasAppCustomAttributeSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationSaasAppCustomAttributeSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96223740c8a1b6694da8a99a6fcf6f5039fe272269fa13737f98c357ff34bac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomClaim",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "name": "name",
        "required": "required",
        "scope": "scope",
    },
)
class AccessApplicationSaasAppCustomClaim:
    def __init__(
        self,
        *,
        source: typing.Union["AccessApplicationSaasAppCustomClaimSource", typing.Dict[builtins.str, typing.Any]],
        name: typing.Optional[builtins.str] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#source AccessApplication#source}
        :param name: The name of the attribute as provided to the SaaS app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param required: True if the attribute must be always present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#required AccessApplication#required}
        :param scope: The scope of the claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scope AccessApplication#scope}
        '''
        if isinstance(source, dict):
            source = AccessApplicationSaasAppCustomClaimSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3348f4f49355da1436488e49d56d19cf79080fc38ea1b2059a85ca3d617caf3e)
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
    def source(self) -> "AccessApplicationSaasAppCustomClaimSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#source AccessApplication#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("AccessApplicationSaasAppCustomClaimSource", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the attribute as provided to the SaaS app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the attribute must be always present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#required AccessApplication#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of the claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scope AccessApplication#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppCustomClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppCustomClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9daf1bcec1ecf517dc8d171a9e2c584c4f5a20bbd7250ff68fd76ba3bbcd7f6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationSaasAppCustomClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed00dce5a26f43de5b79d0f4e06f0e0995ccbcbc6ae5eea4a5fa9af79670d16)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationSaasAppCustomClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b2ee450ea687a2cdc1213242f4d2cb330bec7423c84b11d902b57dee7cb7d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccaa077d7f196f67e3554b3a2d1df355ae100c897584b670a93898eee2e6e352)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8689b4874b7fac8203ce003f5fefe12c5cba89014eb8f5c9e51aa31d08a8713c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e04f76b1672eb89592a60cf34d1f914eb2656e12a8ffcc74feb385fc9f3182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationSaasAppCustomClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8074dcc251b86ee9915ab1881091bb866117aec67eb372d8d78847741f5e6c)
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
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        value = AccessApplicationSaasAppCustomClaimSource(
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
    def source(self) -> "AccessApplicationSaasAppCustomClaimSourceOutputReference":
        return typing.cast("AccessApplicationSaasAppCustomClaimSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["AccessApplicationSaasAppCustomClaimSource"]:
        return typing.cast(typing.Optional["AccessApplicationSaasAppCustomClaimSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3370a298ac4ed1df132dec3e91f65d4f08cbe34c5904abcaccf0fb257e018441)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee3667d245af8e63aab48552d098a83c4f8911b538c57133cdf99ba2fd8a95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4123b2c80190bf3a2bcc7c215f9918acbc06ed18037a5c1131f6345b62a395b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomClaim]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomClaim]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomClaim]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ba8383afa4f9bfa06f82bced9b51e03093c7bbbd8e81beab47bde35a71911f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomClaimSource",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "name_by_idp": "nameByIdp"},
)
class AccessApplicationSaasAppCustomClaimSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the attribute as provided by the IDP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param name_by_idp: A mapping from IdP ID to claim name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0526a6066b80926a1e88fea9f9fa363899ee4918aebd48fb89405807ca6550da)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_by_idp(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping from IdP ID to claim name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name_by_idp AccessApplication#name_by_idp}
        '''
        result = self._values.get("name_by_idp")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppCustomClaimSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppCustomClaimSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppCustomClaimSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09294ff6301d42ac0c018c95be5cc058e34e2297bfd7be276e8df8bd18893caa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ee3f67e022de0b11ddeeebc516885c8bcb150aced1f59140cb8ac70df6d6544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameByIdp")
    def name_by_idp(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "nameByIdp"))

    @name_by_idp.setter
    def name_by_idp(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41c871021b9c2096e35904c2d8846e745e2b4d76cecf15cb4f7beaff257c811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameByIdp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessApplicationSaasAppCustomClaimSource]:
        return typing.cast(typing.Optional[AccessApplicationSaasAppCustomClaimSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationSaasAppCustomClaimSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1088785ae58c8db2646331f969abc3b4386c1047af96fbf5b4e3dd5adac1530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppHybridAndImplicitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "return_access_token_from_authorization_endpoint": "returnAccessTokenFromAuthorizationEndpoint",
        "return_id_token_from_authorization_endpoint": "returnIdTokenFromAuthorizationEndpoint",
    },
)
class AccessApplicationSaasAppHybridAndImplicitOptions:
    def __init__(
        self,
        *,
        return_access_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        return_id_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param return_access_token_from_authorization_endpoint: If true, the authorization endpoint will return an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_access_token_from_authorization_endpoint AccessApplication#return_access_token_from_authorization_endpoint}
        :param return_id_token_from_authorization_endpoint: If true, the authorization endpoint will return an id token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_id_token_from_authorization_endpoint AccessApplication#return_id_token_from_authorization_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53e2e5243c8d583a2344fc23a10f606d309cf0d46c3bbca96d3449f785684ef)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_access_token_from_authorization_endpoint AccessApplication#return_access_token_from_authorization_endpoint}
        '''
        result = self._values.get("return_access_token_from_authorization_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def return_id_token_from_authorization_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the authorization endpoint will return an id token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_id_token_from_authorization_endpoint AccessApplication#return_id_token_from_authorization_endpoint}
        '''
        result = self._values.get("return_id_token_from_authorization_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppHybridAndImplicitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppHybridAndImplicitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppHybridAndImplicitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93bd091a31421d9252d0472a3a79d1d28b29ec6a6675c0b2ddccf414cc58727)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae618ef495ca05bc1b0e5e31a09ab813c44625e83b87c76c9a3d0d5d1e6c043)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eab1f377418180f3648ffce1a43c6c3dfae283942c44c313e19bc31acb6d7efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnIdTokenFromAuthorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions]:
        return typing.cast(typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f574593dd28c3a02bd571318c346ae34ab8567a06803cb504970762e1dcdfe28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationSaasAppOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49168f3c8353cfd81f0c05971d66ca3a23f81a2cb09b93d61892c2ae6a801eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomAttribute")
    def put_custom_attribute(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cd218c8928093eafd6be7fce505bfd3e0c12da7626ad8d83967ffe4fa2342b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomAttribute", [value]))

    @jsii.member(jsii_name="putCustomClaim")
    def put_custom_claim(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a28c41559e8fc776b17dd9baa82678ce28411d4b23e60002b30e52ff9db216d)
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
        :param return_access_token_from_authorization_endpoint: If true, the authorization endpoint will return an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_access_token_from_authorization_endpoint AccessApplication#return_access_token_from_authorization_endpoint}
        :param return_id_token_from_authorization_endpoint: If true, the authorization endpoint will return an id token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#return_id_token_from_authorization_endpoint AccessApplication#return_id_token_from_authorization_endpoint}
        '''
        value = AccessApplicationSaasAppHybridAndImplicitOptions(
            return_access_token_from_authorization_endpoint=return_access_token_from_authorization_endpoint,
            return_id_token_from_authorization_endpoint=return_id_token_from_authorization_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putHybridAndImplicitOptions", [value]))

    @jsii.member(jsii_name="putRefreshTokenOptions")
    def put_refresh_token_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationSaasAppRefreshTokenOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f85c470c8a683270d14b6a0c03c8dbc27a892c6a6bba2cb2efa691f0385d469)
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
    def custom_attribute(self) -> AccessApplicationSaasAppCustomAttributeList:
        return typing.cast(AccessApplicationSaasAppCustomAttributeList, jsii.get(self, "customAttribute"))

    @builtins.property
    @jsii.member(jsii_name="customClaim")
    def custom_claim(self) -> AccessApplicationSaasAppCustomClaimList:
        return typing.cast(AccessApplicationSaasAppCustomClaimList, jsii.get(self, "customClaim"))

    @builtins.property
    @jsii.member(jsii_name="hybridAndImplicitOptions")
    def hybrid_and_implicit_options(
        self,
    ) -> AccessApplicationSaasAppHybridAndImplicitOptionsOutputReference:
        return typing.cast(AccessApplicationSaasAppHybridAndImplicitOptionsOutputReference, jsii.get(self, "hybridAndImplicitOptions"))

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
    ) -> "AccessApplicationSaasAppRefreshTokenOptionsList":
        return typing.cast("AccessApplicationSaasAppRefreshTokenOptionsList", jsii.get(self, "refreshTokenOptions"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]], jsii.get(self, "customAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="customClaimInput")
    def custom_claim_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]], jsii.get(self, "customClaimInput"))

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
    ) -> typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions]:
        return typing.cast(typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions], jsii.get(self, "hybridAndImplicitOptionsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppRefreshTokenOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationSaasAppRefreshTokenOptions"]]], jsii.get(self, "refreshTokenOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9d4de27c0a5d97ce469f24949cf637a5650db7115a26b3d09d7c66bec434d9db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2be001e623bd5a595f384cf2157fe0b6164a9b39a76d8d58d75f5b610bf679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowPkceWithoutClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appLauncherUrl")
    def app_launcher_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appLauncherUrl"))

    @app_launcher_url.setter
    def app_launcher_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a7541314e040bb777f94622141aa2c002ad61908f6ad18d7e842053cd34725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appLauncherUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879a5bd02b74d009b5caf0d6c359ea643b2575c58ab49f55f4e7a432ffeb4e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerServiceUrl")
    def consumer_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerServiceUrl"))

    @consumer_service_url.setter
    def consumer_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94a2c28088cf7cc662f244a3f800bf1bf54bac516d83076959956f11517c51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerServiceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRelayState")
    def default_relay_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRelayState"))

    @default_relay_state.setter
    def default_relay_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02808d8eda44dbdfe5a3b70dee71f6053a09169b2856a9e0875036984dbd461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRelayState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grantTypes")
    def grant_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "grantTypes"))

    @grant_types.setter
    def grant_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23898776df248a64d54d13b96b1bc4b97a79b6ebcf9785fab44df16bf02bdce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupFilterRegex")
    def group_filter_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFilterRegex"))

    @group_filter_regex.setter
    def group_filter_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8411c273f7f270da0746adf45dfd1018f400e78ab3f7d2e2cb0dc09cdda9978d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFilterRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameIdFormat")
    def name_id_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameIdFormat"))

    @name_id_format.setter
    def name_id_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e605787461dbd21e4a28b56ec15784c6ac133b55608b68e396120360939e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameIdFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameIdTransformJsonata")
    def name_id_transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameIdTransformJsonata"))

    @name_id_transform_jsonata.setter
    def name_id_transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bdc5b63c27fc7d6035e31fa95aa3c10ea8b1a2e569d038a1d444ca49fe4bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameIdTransformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redirectUris")
    def redirect_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "redirectUris"))

    @redirect_uris.setter
    def redirect_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab448716e484ba8cd9b5c7e2e88b1e602f83d9c57a67eebaea0a3f85711bfa7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlAttributeTransformJsonata")
    def saml_attribute_transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlAttributeTransformJsonata"))

    @saml_attribute_transform_jsonata.setter
    def saml_attribute_transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4695241308b55dacef8f82bbf04f6b1e5123ca35a22e494bf0a0994191ea797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlAttributeTransformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449d6a3b0e7dbb2a5ecef117ebe80fe5b99e99f18c50abf2739c22e078f0fc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spEntityId")
    def sp_entity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spEntityId"))

    @sp_entity_id.setter
    def sp_entity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e2db75ff078ba5cfb1e5cc189d0cc7fd9055c50ea203b8f89249c650476a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spEntityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessApplicationSaasApp]:
        return typing.cast(typing.Optional[AccessApplicationSaasApp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AccessApplicationSaasApp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c590519c61fb7e78a61063bc0819ff040f76e71d44e537d2447a1a19229fc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppRefreshTokenOptions",
    jsii_struct_bases=[],
    name_mapping={"lifetime": "lifetime"},
)
class AccessApplicationSaasAppRefreshTokenOptions:
    def __init__(self, *, lifetime: typing.Optional[builtins.str] = None) -> None:
        '''
        :param lifetime: How long a refresh token will be valid for after creation. Valid units are ``m``, ``h`` and ``d``. Must be longer than 1m. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#lifetime AccessApplication#lifetime}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2eea62ef92d8f2da6ce98ec35847f3045d5bc74d3559fd39de4c564a378a1c)
            check_type(argname="argument lifetime", value=lifetime, expected_type=type_hints["lifetime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lifetime is not None:
            self._values["lifetime"] = lifetime

    @builtins.property
    def lifetime(self) -> typing.Optional[builtins.str]:
        '''How long a refresh token will be valid for after creation.

        Valid units are ``m``, ``h`` and ``d``. Must be longer than 1m.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#lifetime AccessApplication#lifetime}
        '''
        result = self._values.get("lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationSaasAppRefreshTokenOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationSaasAppRefreshTokenOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppRefreshTokenOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad92db897e44adf2455426fb336aa2885a35e7511b28b81947aa57ab0bfb858b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationSaasAppRefreshTokenOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4420d8888d8ad0c8e7c75667d168cac045b99c30cbc8f147d53473e8305987)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationSaasAppRefreshTokenOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adc236acdaab5e69199a78d2fb21026ae39fef18f99d2276df1d102a66346b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d2b7c07d37a65b8f3a79eee1694577f99180edc8e2bd71b379ab0983f22bf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__252ed85d0d0fb19fa8abc29879236693ea613c71b136b2cbdc2ef502d43cd779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppRefreshTokenOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppRefreshTokenOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppRefreshTokenOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71364e5c1da85750e0bdb56b5fb93b7fe47b364da7dd75526fdef78a43eb6b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationSaasAppRefreshTokenOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationSaasAppRefreshTokenOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68795379aa71a92cf81f1a33469f19d0a64428b39c959663ae8622b9a4439da5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2495f8676f791c782358be0128470713190fdae628128451babfc9fcf6ac5486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppRefreshTokenOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppRefreshTokenOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppRefreshTokenOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d850588091297397b1d7a4389bb9da9d41ac87d47b66d82024d326cb333bd57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfig",
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
class AccessApplicationScimConfig:
    def __init__(
        self,
        *,
        idp_uid: builtins.str,
        remote_uri: builtins.str,
        authentication: typing.Optional[typing.Union["AccessApplicationScimConfigAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationScimConfigMappings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param idp_uid: The UIDs of the IdP to use as the source for SCIM resources to provision to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#idp_uid AccessApplication#idp_uid}
        :param remote_uri: The base URI for the application's SCIM-compatible API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#remote_uri AccessApplication#remote_uri}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authentication AccessApplication#authentication}
        :param deactivate_on_delete: If false, propagates DELETE requests to the target application for SCIM resources. If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#deactivate_on_delete AccessApplication#deactivate_on_delete}
        :param enabled: Whether SCIM provisioning is turned on for this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enabled AccessApplication#enabled}
        :param mappings: mappings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#mappings AccessApplication#mappings}
        '''
        if isinstance(authentication, dict):
            authentication = AccessApplicationScimConfigAuthentication(**authentication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6c5195f7e63f351c29487a0738d30642332a15f4c357079bc51887707f8e8f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#idp_uid AccessApplication#idp_uid}
        '''
        result = self._values.get("idp_uid")
        assert result is not None, "Required property 'idp_uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_uri(self) -> builtins.str:
        '''The base URI for the application's SCIM-compatible API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#remote_uri AccessApplication#remote_uri}
        '''
        result = self._values.get("remote_uri")
        assert result is not None, "Required property 'remote_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional["AccessApplicationScimConfigAuthentication"]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authentication AccessApplication#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional["AccessApplicationScimConfigAuthentication"], result)

    @builtins.property
    def deactivate_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If false, propagates DELETE requests to the target application for SCIM resources.

        If true, sets 'active' to false on the SCIM resource. Note: Some targets do not support DELETE operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#deactivate_on_delete AccessApplication#deactivate_on_delete}
        '''
        result = self._values.get("deactivate_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether SCIM provisioning is turned on for this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enabled AccessApplication#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mappings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationScimConfigMappings"]]]:
        '''mappings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#mappings AccessApplication#mappings}
        '''
        result = self._values.get("mappings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationScimConfigMappings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationScimConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigAuthentication",
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
class AccessApplicationScimConfigAuthentication:
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
        :param scheme: The authentication scheme to use when making SCIM requests to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scheme AccessApplication#scheme}
        :param authorization_url: URL used to generate the auth code used during token generation. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authorization_url AccessApplication#authorization_url}
        :param client_id: Client ID used to authenticate when generating a token for authenticating with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_id AccessApplication#client_id}
        :param client_secret: Secret used to authenticate when generating a token for authenticating with the remove SCIM service. Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_secret AccessApplication#client_secret}
        :param password: Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#password AccessApplication#password}
        :param scopes: The authorization scopes to request when generating the token used to authenticate with the remove SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        :param token: Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token AccessApplication#token}
        :param token_url: URL used to generate the token used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token_url AccessApplication#token_url}
        :param user: User name used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#user AccessApplication#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb421ec2a23a9ee11e8d9d5c3b8a55de5528e521898067b24d8988f5085e0e6a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scheme AccessApplication#scheme}
        '''
        result = self._values.get("scheme")
        assert result is not None, "Required property 'scheme' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_url(self) -> typing.Optional[builtins.str]:
        '''URL used to generate the auth code used during token generation.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authorization_url AccessApplication#authorization_url}
        '''
        result = self._values.get("authorization_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Client ID used to authenticate when generating a token for authenticating with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_id AccessApplication#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Secret used to authenticate when generating a token for authenticating with the remove SCIM service.

        Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_secret AccessApplication#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#password AccessApplication#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The authorization scopes to request when generating the token used to authenticate with the remove SCIM service.

        Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token AccessApplication#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_url(self) -> typing.Optional[builtins.str]:
        '''URL used to generate the token used to authenticate with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token_url AccessApplication#token_url}
        '''
        result = self._values.get("token_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''User name used to authenticate with the remote SCIM service.

        Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#user AccessApplication#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationScimConfigAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationScimConfigAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7e88f80dce07a2bf2d42cf4cc99f9e108bbea8fb1451aeedd8a72a00d9280c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b3d30e7a6792404a44f524a953e667d74e613ad2d2dc37d551fefd15fbfb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9920f4fa11371187f3f49d2b41a659a71ace91b272eedbb0c6a1e1d620044b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664640d0c354542e598bb4f47921e77b9e689b02dc7f8864d99f2dbaa4737e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9aaf7f71446ac2b0bfb0a65e063b68ff357c894980482b6ae1140ea3e3b4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128fb41594221fc0444940a8e701776e6efaf0bc069e384e64e908fd85541dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ea706123eb3ef510e7362c3804b771f12aa41b1923c2d6246961c26f686e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7e867160a1c4f7953fbfb15703183ff6238c4c40064284ffe73d6213128eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenUrl")
    def token_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenUrl"))

    @token_url.setter
    def token_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7134939238551b6edddc3dccf6bfd13bdc2e4a89c273735db7ad10ec41562e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00218d4e6ccc9e46084533a2b178f22150318005a22bc4da8f7fdb5b78fc9714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessApplicationScimConfigAuthentication]:
        return typing.cast(typing.Optional[AccessApplicationScimConfigAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationScimConfigAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6b4f7e54bbfc6de10d5b30aa32332528db558fcef34d825ce81b13f9012f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigMappings",
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
class AccessApplicationScimConfigMappings:
    def __init__(
        self,
        *,
        schema: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter: typing.Optional[builtins.str] = None,
        operations: typing.Optional[typing.Union["AccessApplicationScimConfigMappingsOperations", typing.Dict[builtins.str, typing.Any]]] = None,
        strictness: typing.Optional[builtins.str] = None,
        transform_jsonata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schema: Which SCIM resource type this mapping applies to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#schema AccessApplication#schema}
        :param enabled: Whether or not this mapping is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enabled AccessApplication#enabled}
        :param filter: A `SCIM filter expression <https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2>`_ that matches resources that should be provisioned to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#filter AccessApplication#filter}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#operations AccessApplication#operations}
        :param strictness: How strictly to adhere to outbound resource schemas when provisioning to this mapping. "strict" will remove unknown values when provisioning, while "passthrough" will pass unknown values to the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#strictness AccessApplication#strictness}
        :param transform_jsonata: A `JSONata <https://jsonata.org/>`_ expression that transforms the resource before provisioning it in the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#transform_jsonata AccessApplication#transform_jsonata}
        '''
        if isinstance(operations, dict):
            operations = AccessApplicationScimConfigMappingsOperations(**operations)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ce58ff4a2d6074769324c008c1a327b60addbc96ebdfc2813fbfa097eacce3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#schema AccessApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#enabled AccessApplication#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''A `SCIM filter expression <https://datatracker.ietf.org/doc/html/rfc7644#section-3.4.2.2>`_ that matches resources that should be provisioned to this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#filter AccessApplication#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional["AccessApplicationScimConfigMappingsOperations"]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#operations AccessApplication#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional["AccessApplicationScimConfigMappingsOperations"], result)

    @builtins.property
    def strictness(self) -> typing.Optional[builtins.str]:
        '''How strictly to adhere to outbound resource schemas when provisioning to this mapping.

        "strict" will remove unknown values when provisioning, while "passthrough" will pass unknown values to the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#strictness AccessApplication#strictness}
        '''
        result = self._values.get("strictness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transform_jsonata(self) -> typing.Optional[builtins.str]:
        '''A `JSONata <https://jsonata.org/>`_ expression that transforms the resource before provisioning it in the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#transform_jsonata AccessApplication#transform_jsonata}
        '''
        result = self._values.get("transform_jsonata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationScimConfigMappings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationScimConfigMappingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigMappingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a361d04cb6e4b56fedbc880cbafbe124c21d42e6790bbd3d70f0e5bf8579fb6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationScimConfigMappingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e9ea629e1dcb4ec2b6abfb37a18be447a07ef31b5e793bf35a7538f97e16b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationScimConfigMappingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c2cd331d9cb2c82badaa91452c24cf2459f2a893b01a64c43bca45dfce57c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4298223860b849fcf4b82a924ea30294801601d38a0e486b1b5af0b05137c6c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__385d5d62d259d174963ec0be3e6432b00f6a70c2d0096872bf2947f6915464b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e264d03552b7f02bfdfa709ff663b316c1b219fe80d587531049f175e120729f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigMappingsOperations",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessApplicationScimConfigMappingsOperations:
    def __init__(
        self,
        *,
        create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param create: Whether or not this mapping applies to create (POST) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#create AccessApplication#create}
        :param delete: Whether or not this mapping applies to DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#delete AccessApplication#delete}
        :param update: Whether or not this mapping applies to update (PATCH/PUT) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#update AccessApplication#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ff14cbe5991c9130d696bb5991763f3840ff7e1899b56555aa9455d82eb0d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#create AccessApplication#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping applies to DELETE operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#delete AccessApplication#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not this mapping applies to update (PATCH/PUT) operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#update AccessApplication#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationScimConfigMappingsOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationScimConfigMappingsOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigMappingsOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4460b68191c863aaf371162cf1c87eb7d50af7296e63570f6f105cd62987866a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad517945cfc85175f40b65700873555156141369ad2ee8e2d34870d1fdafab3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d122b094ff76da649be407ac286cadc757b4758eaf5ef0222a0f9c44fd6e39a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__795c7b239ef9a07ebd24fd3c94a4e6ca785b86bd1b4374374f1921d4cacb34d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessApplicationScimConfigMappingsOperations]:
        return typing.cast(typing.Optional[AccessApplicationScimConfigMappingsOperations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationScimConfigMappingsOperations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c120ee5f69b9f5f21454f5a6265fe26d0bbc78eb465abfc5277e3cb76c5310d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationScimConfigMappingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigMappingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f47605e34c440383e35510b1ce8d9bcc19f699466ac5421765a3be526c75d3)
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
        :param create: Whether or not this mapping applies to create (POST) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#create AccessApplication#create}
        :param delete: Whether or not this mapping applies to DELETE operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#delete AccessApplication#delete}
        :param update: Whether or not this mapping applies to update (PATCH/PUT) operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#update AccessApplication#update}
        '''
        value = AccessApplicationScimConfigMappingsOperations(
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
    ) -> AccessApplicationScimConfigMappingsOperationsOutputReference:
        return typing.cast(AccessApplicationScimConfigMappingsOperationsOutputReference, jsii.get(self, "operations"))

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
    ) -> typing.Optional[AccessApplicationScimConfigMappingsOperations]:
        return typing.cast(typing.Optional[AccessApplicationScimConfigMappingsOperations], jsii.get(self, "operationsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1d1c0c8f54f1a3da334d82319c846ed373083ec0cd5ea5e07b771fc058ca2d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3c95b40c649c031ad772ef290c9170b96a3c923c87332aaa476efa6035eb55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69192b1dd69948aba5bd21aa7731cf790daa327b44e719b57f3196b8c4817c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictness")
    def strictness(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "strictness"))

    @strictness.setter
    def strictness(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afaccdd06730742227fead2837829418101b181effd8db4ef6caadc1590e070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictness", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transformJsonata")
    def transform_jsonata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transformJsonata"))

    @transform_jsonata.setter
    def transform_jsonata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f737b2255344751916f499a0c000c68f6cb0d36268916654015cc6ecfb30d850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transformJsonata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationScimConfigMappings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationScimConfigMappings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationScimConfigMappings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f8c7af54eafa01b9c76ef5c8964a6ba1a559ed27846ab72a7bcde3134e4c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationScimConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationScimConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af6c39523d36f77545e1ff6ca3e23e35654261f62ffd40b4b783aeb28f03b74c)
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
        :param scheme: The authentication scheme to use when making SCIM requests to this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scheme AccessApplication#scheme}
        :param authorization_url: URL used to generate the auth code used during token generation. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#authorization_url AccessApplication#authorization_url}
        :param client_id: Client ID used to authenticate when generating a token for authenticating with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_id AccessApplication#client_id}
        :param client_secret: Secret used to authenticate when generating a token for authenticating with the remove SCIM service. Required when using ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#client_secret AccessApplication#client_secret}
        :param password: Required when using ``scim_config.0.authentication.0.user``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#password AccessApplication#password}
        :param scopes: The authorization scopes to request when generating the token used to authenticate with the remove SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#scopes AccessApplication#scopes}
        :param token: Token used to authenticate with the remote SCIM service. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token AccessApplication#token}
        :param token_url: URL used to generate the token used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.client_id``. Conflicts with ``scim_config.0.authentication.0.user``, ``scim_config.0.authentication.0.password``, ``scim_config.0.authentication.0.token``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#token_url AccessApplication#token_url}
        :param user: User name used to authenticate with the remote SCIM service. Required when using ``scim_config.0.authentication.0.password``. Conflicts with ``scim_config.0.authentication.0.token``, ``scim_config.0.authentication.0.client_id``, ``scim_config.0.authentication.0.client_secret``, ``scim_config.0.authentication.0.authorization_url``, ``scim_config.0.authentication.0.token_url``, ``scim_config.0.authentication.0.scopes``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#user AccessApplication#user}
        '''
        value = AccessApplicationScimConfigAuthentication(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e850f373dcfb6257979ec640e2cd628e1f40a4c1d7d3984321e2fd6d3fe39af2)
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
    ) -> AccessApplicationScimConfigAuthenticationOutputReference:
        return typing.cast(AccessApplicationScimConfigAuthenticationOutputReference, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="mappings")
    def mappings(self) -> AccessApplicationScimConfigMappingsList:
        return typing.cast(AccessApplicationScimConfigMappingsList, jsii.get(self, "mappings"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[AccessApplicationScimConfigAuthentication]:
        return typing.cast(typing.Optional[AccessApplicationScimConfigAuthentication], jsii.get(self, "authenticationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]], jsii.get(self, "mappingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b8fc19c1ab990bdc654153d924371e340bd0df62eb0337e220eccba37c4605b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d2f76e71dc9af011d8f8bc3a42d53030f5aedc10f16a15fd8112b3b5f0206d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idpUid")
    def idp_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idpUid"))

    @idp_uid.setter
    def idp_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a36cabf534ad36fa103285ef6cd42939de506257564cea6b5b06afd4ab7e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idpUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteUri")
    def remote_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteUri"))

    @remote_uri.setter
    def remote_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d13dbd119e11d34be938987e034ea0ad8455fff400c02f6594d3e59c7b283b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessApplicationScimConfig]:
        return typing.cast(typing.Optional[AccessApplicationScimConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessApplicationScimConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5675bf252307cd78af8b52dd169ed09214abacb8b0e890216158ca028d306486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "protocol": "protocol",
        "target_attributes": "targetAttributes",
    },
)
class AccessApplicationTargetCriteria:
    def __init__(
        self,
        *,
        port: jsii.Number,
        protocol: builtins.str,
        target_attributes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationTargetCriteriaTargetAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param port: The port that the targets use for the chosen communication protocol. A port cannot be assigned to multiple protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#port AccessApplication#port}
        :param protocol: The communication protocol your application secures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#protocol AccessApplication#protocol}
        :param target_attributes: target_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#target_attributes AccessApplication#target_attributes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0722addb8dba86a528b15c5bfb2b89c966365a597e668abe1045e22971185e6d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#port AccessApplication#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The communication protocol your application secures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#protocol AccessApplication#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_attributes(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteriaTargetAttributes"]]:
        '''target_attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#target_attributes AccessApplication#target_attributes}
        '''
        result = self._values.get("target_attributes")
        assert result is not None, "Required property 'target_attributes' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteriaTargetAttributes"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationTargetCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationTargetCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df79994e8a9a1686024be8268f1e17e8211485fe0fbb8cd2d57c711e5e555125)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationTargetCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5793cf6e112b29ccd0aa15fdfe006d587c4e96642c76566561e8202cb6c863)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationTargetCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239a9d305631a419c0a3ac143c9b1820b36f6bc3d99fdde18b12bc6518d3408f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78324898144cd19ad19d8e6f4066a6f98e2b341b227a692e3ee1567204c78618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4281f04673ee89fdec127f840607e9084c27ea8eeb2fd65230e171f14f2aff1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e76f1cd639cc62233e7ad692be5eb20499e4e17018a87b969866c7fa08e5d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationTargetCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70e450185991c0e2de1b76563603bc26b672152bb5a239f73c515fbd58a19057)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTargetAttributes")
    def put_target_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessApplicationTargetCriteriaTargetAttributes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb69646252bea5aa608bfa2d6d155e7bdb8814590784876adbf8797887894e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargetAttributes", [value]))

    @builtins.property
    @jsii.member(jsii_name="targetAttributes")
    def target_attributes(
        self,
    ) -> "AccessApplicationTargetCriteriaTargetAttributesList":
        return typing.cast("AccessApplicationTargetCriteriaTargetAttributesList", jsii.get(self, "targetAttributes"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteriaTargetAttributes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessApplicationTargetCriteriaTargetAttributes"]]], jsii.get(self, "targetAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04135bd840e7808a2ec43c53b8532b59a359bedb86fa72b1e01158979aeb09dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37398b0536532a90e45cb9cdac6a6146ddf3bb3dc2e09ba9ad552c043a0fbc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6b059b82b39925e5cc10805058f0dc11ac2bd480c90b6d3e7addb6c637cb82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteriaTargetAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class AccessApplicationTargetCriteriaTargetAttributes:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The key of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        :param values: The values of the attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#values AccessApplication#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d3630b6366c5ae37e00c2b64a45a4edb973aa6a4b7af9073f4319c13d83767)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The key of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#name AccessApplication#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The values of the attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.48.0/docs/resources/access_application#values AccessApplication#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessApplicationTargetCriteriaTargetAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessApplicationTargetCriteriaTargetAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteriaTargetAttributesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deda956dac02178aff4cc26e55fe5b8506f383282b0ee15c596fd84e1c60127d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessApplicationTargetCriteriaTargetAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040d29959c7c1351d17d115cbd6ea757180178ac418ac5b9665d1096e6d16b7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessApplicationTargetCriteriaTargetAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51f579b3321876b3dc0b5755c4548ceacc26a608f91f152dc84c37e7c047b8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__587d1472bab6585100b66025a6ad12c6ce712d4d659a25a3f6d7c0e57c67fef4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d3ce9fe59bd368f801b6290c4f2a49b6f7bc6599ff84ca52960d01f59c4f86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteriaTargetAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteriaTargetAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteriaTargetAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3921f292dc47b8707948e136690d488a0968749a93b5d751f9877141f32c4abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessApplicationTargetCriteriaTargetAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessApplication.AccessApplicationTargetCriteriaTargetAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0834ed1fd5f3cb6a30d68d291bc18eb7aaf16cfeed1046d3a381509c02aec707)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9565dea7a9b5b454d87fa85b1fb2303bc0fff54baa18ac160c9ec06859196973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c06994d81ef1e3978e6655c0c01653bcea3de21203bcdafd9dd21da46c91438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteriaTargetAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteriaTargetAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteriaTargetAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a193d6e971eacae3f119ebf9dee59538cd477cfbcb6750ccac24f5387e1be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessApplication",
    "AccessApplicationConfig",
    "AccessApplicationCorsHeaders",
    "AccessApplicationCorsHeadersList",
    "AccessApplicationCorsHeadersOutputReference",
    "AccessApplicationDestinations",
    "AccessApplicationDestinationsList",
    "AccessApplicationDestinationsOutputReference",
    "AccessApplicationFooterLinks",
    "AccessApplicationFooterLinksList",
    "AccessApplicationFooterLinksOutputReference",
    "AccessApplicationLandingPageDesign",
    "AccessApplicationLandingPageDesignOutputReference",
    "AccessApplicationSaasApp",
    "AccessApplicationSaasAppCustomAttribute",
    "AccessApplicationSaasAppCustomAttributeList",
    "AccessApplicationSaasAppCustomAttributeOutputReference",
    "AccessApplicationSaasAppCustomAttributeSource",
    "AccessApplicationSaasAppCustomAttributeSourceOutputReference",
    "AccessApplicationSaasAppCustomClaim",
    "AccessApplicationSaasAppCustomClaimList",
    "AccessApplicationSaasAppCustomClaimOutputReference",
    "AccessApplicationSaasAppCustomClaimSource",
    "AccessApplicationSaasAppCustomClaimSourceOutputReference",
    "AccessApplicationSaasAppHybridAndImplicitOptions",
    "AccessApplicationSaasAppHybridAndImplicitOptionsOutputReference",
    "AccessApplicationSaasAppOutputReference",
    "AccessApplicationSaasAppRefreshTokenOptions",
    "AccessApplicationSaasAppRefreshTokenOptionsList",
    "AccessApplicationSaasAppRefreshTokenOptionsOutputReference",
    "AccessApplicationScimConfig",
    "AccessApplicationScimConfigAuthentication",
    "AccessApplicationScimConfigAuthenticationOutputReference",
    "AccessApplicationScimConfigMappings",
    "AccessApplicationScimConfigMappingsList",
    "AccessApplicationScimConfigMappingsOperations",
    "AccessApplicationScimConfigMappingsOperationsOutputReference",
    "AccessApplicationScimConfigMappingsOutputReference",
    "AccessApplicationScimConfigOutputReference",
    "AccessApplicationTargetCriteria",
    "AccessApplicationTargetCriteriaList",
    "AccessApplicationTargetCriteriaOutputReference",
    "AccessApplicationTargetCriteriaTargetAttributes",
    "AccessApplicationTargetCriteriaTargetAttributesList",
    "AccessApplicationTargetCriteriaTargetAttributesOutputReference",
]

publication.publish()

def _typecheckingstub__c1b2963f98659b9017b97318b2a37e45b5084f4b60cafaa3bcd97429790c8eb1(
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
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
    custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_type: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header_bg_color: typing.Optional[builtins.str] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    landing_page_design: typing.Optional[typing.Union[AccessApplicationLandingPageDesign, typing.Dict[builtins.str, typing.Any]]] = None,
    logo_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    saas_app: typing.Optional[typing.Union[AccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[AccessApplicationScimConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__4a3f1ea026942d7e5ec2b0495b96b60d5ea2689942f1e955caf45dbd6ab75873(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0c9359a2094e6a5d995e98fae21fbe1877ef3aca4c5f09eb4d19306fa8750c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3cdbe33aad4bdc745e21b73c1af29162e4848f926e074d30ec598698728f13(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353086e98e96dbcecf2c69eedd880bba115cd7082c09d49047fc126c3ed53284(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf59ef93d4ebe08de54f2b8644e0eef8aec5497fc94bc8f20c8c6ec2efc4bf97(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fb38f689b4bf068fc2e8ba83e0a3ec1a53465fe9ca9bf20ef28753a9f80251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8618f77c49f6cc0aa7f0027cb90575ee8a8c18ddd9ef18d5a5678f19be2914(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daff490d3a8108f46fe8affbe607ed3bfce7f0caa97c3a01158863a2d9b81e73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3942e51ffa8e0521e41664e3706ee0d24b9ace1acd8fda40a1ed132fed51d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fe33b6a3e0de6c5d2332cddc4e94399f81b3f96589f00d5cea096ca5c90e89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02da31929754ab70993542e7f44f5e3b8ff2a4113ea0e7fc09dccad505e190e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cf66f6d38abaa184e9b102c5bed0a1bcbad3e59e9238776dc720432d89adc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7394b2b4e1199550fbe6375395d12db57b5a15a49a4d5b7355d6ce5ad25636e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda6e3a2399b050e18d5c2bc8f4883cf54b73d8211f3d0847551f970d6b384e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c02dc85ef48581d4ee221e7d19a805202658fbcf18e9fba8a41c92d7b95d2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c473e90aa30a665e643314d41d7fb6411c390c872477fb3ae366ca7054ca72(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcbe163ed94bb0a50cb8b1b9b52ea152aa192b9bd50115601e6ab1b87eaf861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee783452efee50ba00c22af7913e4238a909caf192c62897899f1fcc8c62df3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ffea86ba305f92fcd8ef5768d2698c4bf9c262d3a7e35de9c4bbf7711be2159(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93aa224e73174428e31a6e1e5ee5c604aeea58149044bc5361f6d0dd9064f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b7a56cc0c2523d37beeaca9d4af0ffe258c84ad7cd8666034d44c91b2c0a5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cee610faa04b0d8e65aad04b0e960f1a472af48d19258d665b5edfc30e57e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94205b9b871f765a94dff73949e655473bf7b6ffab02f41b2a507b924040f1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408052199c5db90c8698c809b74ffc55459b674605e439d3b3bfd8a083255a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d28f4f6f511c05351cf4007acb73b1c10f4e879d811f8418309e428ee2f41f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3b5a29b8213df2135c08e8acb42a3b3e4ef2a2d290881717559e3b6d338f70(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a95c47163bc493ca9389335db25497d901b8dedf1f1549f91f1f323ea93a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08559ba467d164f4458e22395f55bf8245e62c4b82fb8455ec3e36241fb1e350(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad3bbb24317d5f07a9fb5037e763a244642bebdc8fa18f8d948e52201c04187(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfb91cb0ee9996051ba552f920aa96e9da21960ed72cf49353e36a46107d982(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec60611c612d24adf5943874c42fd6fb6eac7715cc9771a7a22bb392fb75c3d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b86799f85043068c1b6ac6d68b67ebdd5dc15341cb709a8eeccbecf097cf147(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2353fa1a2102657035c34ddc9b9776945570491fe11231c033f4ed41e05eeaf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ac6df2597f216a2f0ef7d91eff615dd9bd4f92bf47b2a9e51dec9e2a97df20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f33c40394937d1eb21e9c367c96d3212115f53970a6ffb9db1ab2ecac777b19f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f785d33e1451f1cf27417eb2776a2d793dff777b28167e528be38cf2a13a8faa(
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
    cors_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationCorsHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_deny_message: typing.Optional[builtins.str] = None,
    custom_deny_url: typing.Optional[builtins.str] = None,
    custom_non_identity_deny_url: typing.Optional[builtins.str] = None,
    custom_pages: typing.Optional[typing.Sequence[builtins.str]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain: typing.Optional[builtins.str] = None,
    domain_type: typing.Optional[builtins.str] = None,
    enable_binding_cookie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    footer_links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationFooterLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header_bg_color: typing.Optional[builtins.str] = None,
    http_only_cookie_attribute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    landing_page_design: typing.Optional[typing.Union[AccessApplicationLandingPageDesign, typing.Dict[builtins.str, typing.Any]]] = None,
    logo_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    options_preflight_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    saas_app: typing.Optional[typing.Union[AccessApplicationSaasApp, typing.Dict[builtins.str, typing.Any]]] = None,
    same_site_cookie_attribute: typing.Optional[builtins.str] = None,
    scim_config: typing.Optional[typing.Union[AccessApplicationScimConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    self_hosted_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_auth401_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_duration: typing.Optional[builtins.str] = None,
    skip_app_launcher_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_interstitial: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationTargetCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae525a77bbd533b13658910162a82a7ed82713ce55fbce6efb2802432bd142ee(
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

def _typecheckingstub__aa79530a53dc744124aeaa81632fbdff14a0c4535f89c37afd43ab415cf95406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9b295611563f5e8579389c0b30ac3bf53a4e5471f1f6906f361865e1f6d68f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f63511a0bcc23c92f8a3b522588cef9af4c9489d92aa783dbc643495ee3a006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5991c119e726e4e5bae94364d64d111ba5d06dc1fd9a77feeef6241923a1b94c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed799de136d9a06f6402f513b16198e0f010bfa196b8637c9b9f3a949842696(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f784385a2e46f6e296c6f09c5dd838571dd28c3c939ef8fe647709d9c6b0fbef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationCorsHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91640a7618248ee2dfbc3c623b9f3d2ccaf579d2752459b82e8c1069a4b359b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3400b2ef69eb057e299d971eff385016e19ae0c0fb70f69517fb2389bf4455f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe554ac39141e522d8cea4b0d84ca98b7e0c53123791c7cdc321b0a2a08c5f1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791c3f6bfef6cb602668374e7ae4047e3cfe4fc8175da1ef5ef7b9f90146a893(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0cb5c457ec28d6691034d2841ed4bb6cde403ab39fc573324082e69e28e0ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d5f5968daf5e6d30f2140162a6148b40fadf726eae33a4a24238a304102543(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19571719f469919945233bc1181996c44217f31151077b2376da3c869255841(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9790848826046a2cbfaf9752da2eac0aaf648d202e86c384d87ff3c8a5f41d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6437b4b77a62619bca135ac9848d2ea144d0abbfa730ca8b0efe1bb71cae125d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f6f5c209667b44cb9092177c7fc64e8a78842aad5f7b1d5d1deb26e1c660cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationCorsHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04e04dfcccae87efa038ec162df969c0cec439f4b19117ed1ea4473bfe83a7d(
    *,
    uri: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9b340d37f4019786ef2d54ef37b1b6e9a5014f49ed4345137d74dc26340a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4617120dcf068683b8d898e49640ae9b0d78aee948217002c2bc4c69a829c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5ea431610297d82419116fc0aa1c65f4534d45970cf0e009bc7d3461e5a0c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e77810d4487b59c55871e8521f299f468df756ac081d7bbf7443e6b8e8a4e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba3b44ada26ab10568e96d9e28412c4965002786f089a4995b151a91d12d973(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0b4395a11057b9c1f78b0579f272ce85a8ff4bb8870aa44867497f69c06d18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecce3a9b32c81ed197480cc2f8577c26d329c5f19058c07fffe749b90b908b6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0053c5dbb4e9f035f41a5dcad5ec5b54e71858d5e85602eab02c8256598b3268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c34895f7e0a79b0c5ba8dcf66629f92eb272169a2abfd550422ff466698105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e69386f002a02b6676b11a7010491c49d3a3583b5d704c2a789e3c0faad7a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a283918f835a005a2c46dca747b7b9a44b7593c2aff93d5e6fd63bcfe704cdea(
    *,
    name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5355d081c675ef6b32d361cfa3957ba955f2b6c44d72d129c50fe89aaaa8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212cd76d3e6b14aea11265a67d5974e157b174235cb409a102d49f6f71ead33d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e5a3c3c870b2af8d1b5d84335cf65a9267fc93202b299cfdfa1717d8f9f2ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f403f07c629c548c1b1e949638dc22d9ccef88f564cf313e70782a6a567a13(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83114e3cfa9789ecb7b50ca8c843bbc95d34a50f296602de8045e98ecb0801c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea976940ab4e0525062237dbfb91dc1e58d974df733e4d99f218079057bd5d84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationFooterLinks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f95bb5a2d746ee03d9500474665f0876c8a3e681eca02ccca265e7e5a1c95e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32e7f5a8c0a097ba230d28d9fd33f4f18dbcbd96d94718e321fb8fc8a769498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edca4c3b8c7950e65a971f288e9c04a769bda673153ed00b1a543436350fce6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20ddb59f250ffa10b01f057607e8aa08137620c339bdb2a8fe11d7af0983c0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationFooterLinks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa34602f22fd0644bebc46d6fd3826bf2ecddecc255937ca6d87aeeb99020319(
    *,
    button_color: typing.Optional[builtins.str] = None,
    button_text_color: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4563866f29e42b2a228ea06df2d61bf5b7a55c2536457088d85a4ac5bdc0b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4a145464d5dc4a94d3fa02702bf2d4b1c6949fd5c34d0f96bd64ad53afb98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6894bcadefe5e7b50af83e28dbc8aca4df687cb6a2b173487361818bec46cb3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9894872321eb19f8d71edd0450b37711bf488a5ddf25e607cf7f0c62b430484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e727e9c0ef0557e103a198910f5ad1e043b9af07dec27e382634ffe5be77c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aa9cb97f24af767a167f524c3c7a61a8785d3a89adfa35cf43f4e66c17fc61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b148ba89a7a77ac870a25c31d352252c9dced333606de93526517ebc5aef2c58(
    value: typing.Optional[AccessApplicationLandingPageDesign],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cefbcedc5818578827cb55f910f5dea7e97d62fc19dd39c031f17cb5f5aab3(
    *,
    access_token_lifetime: typing.Optional[builtins.str] = None,
    allow_pkce_without_client_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    app_launcher_url: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    consumer_service_url: typing.Optional[builtins.str] = None,
    custom_attribute: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_claim: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_relay_state: typing.Optional[builtins.str] = None,
    grant_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_filter_regex: typing.Optional[builtins.str] = None,
    hybrid_and_implicit_options: typing.Optional[typing.Union[AccessApplicationSaasAppHybridAndImplicitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    name_id_format: typing.Optional[builtins.str] = None,
    name_id_transform_jsonata: typing.Optional[builtins.str] = None,
    redirect_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    refresh_token_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppRefreshTokenOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    saml_attribute_transform_jsonata: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    sp_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47822a0d294ecd1c204d7e43ce43f5c81b4495f154e4d8de423c4ea120d7c080(
    *,
    source: typing.Union[AccessApplicationSaasAppCustomAttributeSource, typing.Dict[builtins.str, typing.Any]],
    friendly_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_format: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5deaa3caa3c864bdcb00a7c435b7ae15521b0d8fbd8b6b7fededa994af5aa5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8ade2f4f80a5432c7302f71bdebdea60642416017e167c0f697c1fab9a72b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c67459ff871914b79bf01ade3d1f69e2dec200a32a17aeb9e8e2ffef4c5d64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ecab507188ddfbfcb9a792817b28c3ec9f19eb1409a4f6efdbddd5c340366f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc589e3f3c5b3602f39a53f644e605f4b7c92fb8ae452cedfd033b680a275747(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26527e3a1b88ebbdf036684dfc7f2b58892c0e99e198d57ea94ba2aa967b1f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomAttribute]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db88ced95da88295b22f40e287e904bf65e3fcc0096905b070ec11b69a2df39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb32c28a01b2d722459fe7b5cc5d46c1d4fbbb931e4a1ee16bed434d444b830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6696c6834c79882863ec13ff8cd51dbf80bfe1f04d33a4df96c08f63279488d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e8d5b579e56ac8a6c43a0621072d22291e0b8825a15588f20247be75e1a4d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe345dcbe0f490dfef205944df6849210bc382ef052a91c9f933d06b1ff50ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffca61f84302f377b4712b085f9fb553836f560e630b9f0163525ae2801818a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomAttribute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eda67f6aa706b9eeedbc74328238a63768a0b8feda2a769ee39f32c8eca67eb(
    *,
    name: builtins.str,
    name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54953c0eba05eb01197cef40b74f2b3ebef367234083f5c06755c1469632c78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb7a9503bb2eeae21e81557dfbb52a4b860f0e04621cc6ca2793294e50a80fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ecb5140ac36afc1ba0f51b74b9688b86df647050772d58be91f1feae7ebda4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96223740c8a1b6694da8a99a6fcf6f5039fe272269fa13737f98c357ff34bac6(
    value: typing.Optional[AccessApplicationSaasAppCustomAttributeSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3348f4f49355da1436488e49d56d19cf79080fc38ea1b2059a85ca3d617caf3e(
    *,
    source: typing.Union[AccessApplicationSaasAppCustomClaimSource, typing.Dict[builtins.str, typing.Any]],
    name: typing.Optional[builtins.str] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daf1bcec1ecf517dc8d171a9e2c584c4f5a20bbd7250ff68fd76ba3bbcd7f6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed00dce5a26f43de5b79d0f4e06f0e0995ccbcbc6ae5eea4a5fa9af79670d16(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b2ee450ea687a2cdc1213242f4d2cb330bec7423c84b11d902b57dee7cb7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccaa077d7f196f67e3554b3a2d1df355ae100c897584b670a93898eee2e6e352(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8689b4874b7fac8203ce003f5fefe12c5cba89014eb8f5c9e51aa31d08a8713c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e04f76b1672eb89592a60cf34d1f914eb2656e12a8ffcc74feb385fc9f3182(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppCustomClaim]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8074dcc251b86ee9915ab1881091bb866117aec67eb372d8d78847741f5e6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3370a298ac4ed1df132dec3e91f65d4f08cbe34c5904abcaccf0fb257e018441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee3667d245af8e63aab48552d098a83c4f8911b538c57133cdf99ba2fd8a95e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4123b2c80190bf3a2bcc7c215f9918acbc06ed18037a5c1131f6345b62a395b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ba8383afa4f9bfa06f82bced9b51e03093c7bbbd8e81beab47bde35a71911f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppCustomClaim]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0526a6066b80926a1e88fea9f9fa363899ee4918aebd48fb89405807ca6550da(
    *,
    name: builtins.str,
    name_by_idp: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09294ff6301d42ac0c018c95be5cc058e34e2297bfd7be276e8df8bd18893caa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee3f67e022de0b11ddeeebc516885c8bcb150aced1f59140cb8ac70df6d6544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41c871021b9c2096e35904c2d8846e745e2b4d76cecf15cb4f7beaff257c811(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1088785ae58c8db2646331f969abc3b4386c1047af96fbf5b4e3dd5adac1530(
    value: typing.Optional[AccessApplicationSaasAppCustomClaimSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53e2e5243c8d583a2344fc23a10f606d309cf0d46c3bbca96d3449f785684ef(
    *,
    return_access_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    return_id_token_from_authorization_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93bd091a31421d9252d0472a3a79d1d28b29ec6a6675c0b2ddccf414cc58727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae618ef495ca05bc1b0e5e31a09ab813c44625e83b87c76c9a3d0d5d1e6c043(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab1f377418180f3648ffce1a43c6c3dfae283942c44c313e19bc31acb6d7efd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f574593dd28c3a02bd571318c346ae34ab8567a06803cb504970762e1dcdfe28(
    value: typing.Optional[AccessApplicationSaasAppHybridAndImplicitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49168f3c8353cfd81f0c05971d66ca3a23f81a2cb09b93d61892c2ae6a801eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cd218c8928093eafd6be7fce505bfd3e0c12da7626ad8d83967ffe4fa2342b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomAttribute, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a28c41559e8fc776b17dd9baa82678ce28411d4b23e60002b30e52ff9db216d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppCustomClaim, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f85c470c8a683270d14b6a0c03c8dbc27a892c6a6bba2cb2efa691f0385d469(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationSaasAppRefreshTokenOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4de27c0a5d97ce469f24949cf637a5650db7115a26b3d09d7c66bec434d9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2be001e623bd5a595f384cf2157fe0b6164a9b39a76d8d58d75f5b610bf679(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a7541314e040bb777f94622141aa2c002ad61908f6ad18d7e842053cd34725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879a5bd02b74d009b5caf0d6c359ea643b2575c58ab49f55f4e7a432ffeb4e43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94a2c28088cf7cc662f244a3f800bf1bf54bac516d83076959956f11517c51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02808d8eda44dbdfe5a3b70dee71f6053a09169b2856a9e0875036984dbd461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23898776df248a64d54d13b96b1bc4b97a79b6ebcf9785fab44df16bf02bdce6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8411c273f7f270da0746adf45dfd1018f400e78ab3f7d2e2cb0dc09cdda9978d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e605787461dbd21e4a28b56ec15784c6ac133b55608b68e396120360939e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bdc5b63c27fc7d6035e31fa95aa3c10ea8b1a2e569d038a1d444ca49fe4bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab448716e484ba8cd9b5c7e2e88b1e602f83d9c57a67eebaea0a3f85711bfa7d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4695241308b55dacef8f82bbf04f6b1e5123ca35a22e494bf0a0994191ea797(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449d6a3b0e7dbb2a5ecef117ebe80fe5b99e99f18c50abf2739c22e078f0fc6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e2db75ff078ba5cfb1e5cc189d0cc7fd9055c50ea203b8f89249c650476a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c590519c61fb7e78a61063bc0819ff040f76e71d44e537d2447a1a19229fc1d(
    value: typing.Optional[AccessApplicationSaasApp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2eea62ef92d8f2da6ce98ec35847f3045d5bc74d3559fd39de4c564a378a1c(
    *,
    lifetime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad92db897e44adf2455426fb336aa2885a35e7511b28b81947aa57ab0bfb858b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4420d8888d8ad0c8e7c75667d168cac045b99c30cbc8f147d53473e8305987(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adc236acdaab5e69199a78d2fb21026ae39fef18f99d2276df1d102a66346b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d2b7c07d37a65b8f3a79eee1694577f99180edc8e2bd71b379ab0983f22bf6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252ed85d0d0fb19fa8abc29879236693ea613c71b136b2cbdc2ef502d43cd779(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71364e5c1da85750e0bdb56b5fb93b7fe47b364da7dd75526fdef78a43eb6b4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationSaasAppRefreshTokenOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68795379aa71a92cf81f1a33469f19d0a64428b39c959663ae8622b9a4439da5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2495f8676f791c782358be0128470713190fdae628128451babfc9fcf6ac5486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d850588091297397b1d7a4389bb9da9d41ac87d47b66d82024d326cb333bd57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationSaasAppRefreshTokenOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6c5195f7e63f351c29487a0738d30642332a15f4c357079bc51887707f8e8f(
    *,
    idp_uid: builtins.str,
    remote_uri: builtins.str,
    authentication: typing.Optional[typing.Union[AccessApplicationScimConfigAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivate_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mappings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb421ec2a23a9ee11e8d9d5c3b8a55de5528e521898067b24d8988f5085e0e6a(
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

def _typecheckingstub__ae7e88f80dce07a2bf2d42cf4cc99f9e108bbea8fb1451aeedd8a72a00d9280c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b3d30e7a6792404a44f524a953e667d74e613ad2d2dc37d551fefd15fbfb7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9920f4fa11371187f3f49d2b41a659a71ace91b272eedbb0c6a1e1d620044b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664640d0c354542e598bb4f47921e77b9e689b02dc7f8864d99f2dbaa4737e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9aaf7f71446ac2b0bfb0a65e063b68ff357c894980482b6ae1140ea3e3b4a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128fb41594221fc0444940a8e701776e6efaf0bc069e384e64e908fd85541dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ea706123eb3ef510e7362c3804b771f12aa41b1923c2d6246961c26f686e9e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7e867160a1c4f7953fbfb15703183ff6238c4c40064284ffe73d6213128eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7134939238551b6edddc3dccf6bfd13bdc2e4a89c273735db7ad10ec41562e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00218d4e6ccc9e46084533a2b178f22150318005a22bc4da8f7fdb5b78fc9714(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6b4f7e54bbfc6de10d5b30aa32332528db558fcef34d825ce81b13f9012f7e(
    value: typing.Optional[AccessApplicationScimConfigAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ce58ff4a2d6074769324c008c1a327b60addbc96ebdfc2813fbfa097eacce3(
    *,
    schema: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter: typing.Optional[builtins.str] = None,
    operations: typing.Optional[typing.Union[AccessApplicationScimConfigMappingsOperations, typing.Dict[builtins.str, typing.Any]]] = None,
    strictness: typing.Optional[builtins.str] = None,
    transform_jsonata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a361d04cb6e4b56fedbc880cbafbe124c21d42e6790bbd3d70f0e5bf8579fb6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e9ea629e1dcb4ec2b6abfb37a18be447a07ef31b5e793bf35a7538f97e16b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c2cd331d9cb2c82badaa91452c24cf2459f2a893b01a64c43bca45dfce57c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4298223860b849fcf4b82a924ea30294801601d38a0e486b1b5af0b05137c6c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385d5d62d259d174963ec0be3e6432b00f6a70c2d0096872bf2947f6915464b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e264d03552b7f02bfdfa709ff663b316c1b219fe80d587531049f175e120729f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationScimConfigMappings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ff14cbe5991c9130d696bb5991763f3840ff7e1899b56555aa9455d82eb0d0(
    *,
    create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4460b68191c863aaf371162cf1c87eb7d50af7296e63570f6f105cd62987866a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad517945cfc85175f40b65700873555156141369ad2ee8e2d34870d1fdafab3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d122b094ff76da649be407ac286cadc757b4758eaf5ef0222a0f9c44fd6e39a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c7b239ef9a07ebd24fd3c94a4e6ca785b86bd1b4374374f1921d4cacb34d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c120ee5f69b9f5f21454f5a6265fe26d0bbc78eb465abfc5277e3cb76c5310d2(
    value: typing.Optional[AccessApplicationScimConfigMappingsOperations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f47605e34c440383e35510b1ce8d9bcc19f699466ac5421765a3be526c75d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1c0c8f54f1a3da334d82319c846ed373083ec0cd5ea5e07b771fc058ca2d6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3c95b40c649c031ad772ef290c9170b96a3c923c87332aaa476efa6035eb55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69192b1dd69948aba5bd21aa7731cf790daa327b44e719b57f3196b8c4817c16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afaccdd06730742227fead2837829418101b181effd8db4ef6caadc1590e070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f737b2255344751916f499a0c000c68f6cb0d36268916654015cc6ecfb30d850(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f8c7af54eafa01b9c76ef5c8964a6ba1a559ed27846ab72a7bcde3134e4c07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationScimConfigMappings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6c39523d36f77545e1ff6ca3e23e35654261f62ffd40b4b783aeb28f03b74c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e850f373dcfb6257979ec640e2cd628e1f40a4c1d7d3984321e2fd6d3fe39af2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationScimConfigMappings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8fc19c1ab990bdc654153d924371e340bd0df62eb0337e220eccba37c4605b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2f76e71dc9af011d8f8bc3a42d53030f5aedc10f16a15fd8112b3b5f0206d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a36cabf534ad36fa103285ef6cd42939de506257564cea6b5b06afd4ab7e80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d13dbd119e11d34be938987e034ea0ad8455fff400c02f6594d3e59c7b283b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5675bf252307cd78af8b52dd169ed09214abacb8b0e890216158ca028d306486(
    value: typing.Optional[AccessApplicationScimConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0722addb8dba86a528b15c5bfb2b89c966365a597e668abe1045e22971185e6d(
    *,
    port: jsii.Number,
    protocol: builtins.str,
    target_attributes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationTargetCriteriaTargetAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df79994e8a9a1686024be8268f1e17e8211485fe0fbb8cd2d57c711e5e555125(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5793cf6e112b29ccd0aa15fdfe006d587c4e96642c76566561e8202cb6c863(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239a9d305631a419c0a3ac143c9b1820b36f6bc3d99fdde18b12bc6518d3408f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78324898144cd19ad19d8e6f4066a6f98e2b341b227a692e3ee1567204c78618(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4281f04673ee89fdec127f840607e9084c27ea8eeb2fd65230e171f14f2aff1f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e76f1cd639cc62233e7ad692be5eb20499e4e17018a87b969866c7fa08e5d80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e450185991c0e2de1b76563603bc26b672152bb5a239f73c515fbd58a19057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb69646252bea5aa608bfa2d6d155e7bdb8814590784876adbf8797887894e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessApplicationTargetCriteriaTargetAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04135bd840e7808a2ec43c53b8532b59a359bedb86fa72b1e01158979aeb09dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37398b0536532a90e45cb9cdac6a6146ddf3bb3dc2e09ba9ad552c043a0fbc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6b059b82b39925e5cc10805058f0dc11ac2bd480c90b6d3e7addb6c637cb82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d3630b6366c5ae37e00c2b64a45a4edb973aa6a4b7af9073f4319c13d83767(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deda956dac02178aff4cc26e55fe5b8506f383282b0ee15c596fd84e1c60127d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040d29959c7c1351d17d115cbd6ea757180178ac418ac5b9665d1096e6d16b7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51f579b3321876b3dc0b5755c4548ceacc26a608f91f152dc84c37e7c047b8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587d1472bab6585100b66025a6ad12c6ce712d4d659a25a3f6d7c0e57c67fef4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d3ce9fe59bd368f801b6290c4f2a49b6f7bc6599ff84ca52960d01f59c4f86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3921f292dc47b8707948e136690d488a0968749a93b5d751f9877141f32c4abb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessApplicationTargetCriteriaTargetAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0834ed1fd5f3cb6a30d68d291bc18eb7aaf16cfeed1046d3a381509c02aec707(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9565dea7a9b5b454d87fa85b1fb2303bc0fff54baa18ac160c9ec06859196973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c06994d81ef1e3978e6655c0c01653bcea3de21203bcdafd9dd21da46c91438(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a193d6e971eacae3f119ebf9dee59538cd477cfbcb6750ccac24f5387e1be1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessApplicationTargetCriteriaTargetAttributes]],
) -> None:
    """Type checking stubs"""
    pass
