r'''
## @affinidi-tdk/common

## Install

### Javascript

```bash
npm install @affinidi-tdk/common
```

## Python

run inside [python virtual env](https://docs.python.org/3/library/venv.html)

```bash
pip install affinidi_tdk_common
```

## Manually build package

```bash
npm i --prefix .
npm run build
npm run package
```

The code will be generated under /dist for each language.
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

from ._jsii import *


@jsii.enum(jsii_type="@affinidi-tdk/common.Environment")
class Environment(enum.Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"


class EnvironmentUtils(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi-tdk/common.EnvironmentUtils",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fetchApiGwUrl")
    @builtins.classmethod
    def fetch_api_gw_url(cls, env: typing.Optional[Environment] = None) -> builtins.str:
        '''
        :param env: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2523c2bfca1a8da7a5c629220884b2d2bc48dc61af04e099db6b9b96fe212a)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fetchApiGwUrl", [env]))

    @jsii.member(jsii_name="fetchElementsAuthTokenUrl")
    @builtins.classmethod
    def fetch_elements_auth_token_url(
        cls,
        env: typing.Optional[Environment] = None,
    ) -> builtins.str:
        '''
        :param env: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca98f168741b0bb1b4a2af1de08548f6f8619361018f500dd3d78db4f2b9672)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fetchElementsAuthTokenUrl", [env]))

    @jsii.member(jsii_name="fetchEnvironment")
    @builtins.classmethod
    def fetch_environment(cls) -> Environment:
        return typing.cast(Environment, jsii.sinvoke(cls, "fetchEnvironment", []))

    @jsii.member(jsii_name="fetchIotUrl")
    @builtins.classmethod
    def fetch_iot_url(cls, env: typing.Optional[Environment] = None) -> builtins.str:
        '''
        :param env: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3e22cc96432d30261cd6f7d086264e9897f1911e43076b7e00cbc860c39c8a)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fetchIotUrl", [env]))

    @jsii.member(jsii_name="fetchRegion")
    @builtins.classmethod
    def fetch_region(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fetchRegion", []))


class VaultUtils(metaclass=jsii.JSIIMeta, jsii_type="@affinidi-tdk/common.VaultUtils"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="buildClaimLink")
    @builtins.classmethod
    def build_claim_link(cls, credential_offer_uri: builtins.str) -> builtins.str:
        '''
        :param credential_offer_uri: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe578ac77e374dcbb02294aafba1146db193a672872c139fa9807f3105031c5)
            check_type(argname="argument credential_offer_uri", value=credential_offer_uri, expected_type=type_hints["credential_offer_uri"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "buildClaimLink", [credential_offer_uri]))

    @jsii.member(jsii_name="buildShareLink")
    @builtins.classmethod
    def build_share_link(
        cls,
        request: builtins.str,
        client_id: builtins.str,
    ) -> builtins.str:
        '''
        :param request: -
        :param client_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bba8c32303353353983449ea48e678017ec8a290c4078c69d20d940fed54ca)
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "buildShareLink", [request, client_id]))


__all__ = [
    "Environment",
    "EnvironmentUtils",
    "VaultUtils",
]

publication.publish()

def _typecheckingstub__ea2523c2bfca1a8da7a5c629220884b2d2bc48dc61af04e099db6b9b96fe212a(
    env: typing.Optional[Environment] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca98f168741b0bb1b4a2af1de08548f6f8619361018f500dd3d78db4f2b9672(
    env: typing.Optional[Environment] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3e22cc96432d30261cd6f7d086264e9897f1911e43076b7e00cbc860c39c8a(
    env: typing.Optional[Environment] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe578ac77e374dcbb02294aafba1146db193a672872c139fa9807f3105031c5(
    credential_offer_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bba8c32303353353983449ea48e678017ec8a290c4078c69d20d940fed54ca(
    request: builtins.str,
    client_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
