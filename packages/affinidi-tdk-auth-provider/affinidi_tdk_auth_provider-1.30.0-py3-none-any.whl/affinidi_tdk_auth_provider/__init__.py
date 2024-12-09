r'''
# @affinidi-tdk/auth-provider

Affinidi TDK Internal module for managing access tokens.

## Install

### Javascript

```bash
npm install @affinidi-tdk/auth-provider
```

## Python

### Install Python package

run inside [python virtual env](https://docs.python.org/3/library/venv.html)

```bash
pip install affinidi_tdk_auth_provider
```

## Usage

### Python package usage

```python
import affinidi_tdk_auth_provider

stats = {
  apiGatewayUrl,
  keyId,
  tokenId,
  passphrase,
  privateKey,
  projectId,
  tokenEndpoint,
}

authProvider = affinidi_tdk_auth_provider.AuthProvider(stats)

projectScopedToken = authProvider.fetch_project_scoped_token()
```

### Javascript package usage

```python
import { AuthProvider } from '@affinidi-tdk/auth-provider'

const authProvider = new AuthProvider({
  apiGatewayUrl,
  keyId,
  tokenId,
  passphrase,
  privateKey,
  projectId,
  tokenEndpoint,
})

const projectScopedToken = await authProvider.fetchProjectScopedToken()
```

### Mnually Build JSII python package

This is step is required, as python package is not published to pypi.org yet

```bash
git clone git@github.com:affinidi/affinidi-tdk.git
cd packages/auth-provider/
npm i --prefix .
npm run build
npm run package
```

```bash
pip install dist/python/affinidi_tdk_auth_provider-0.1.4-py3-none-any.whl
```
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


class AuthProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi-tdk/auth-provider.AuthProvider",
):
    def __init__(self, param: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param param: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d864337db85b1ea4c15a8b13092be48e1a0f7026ae9183bfd6c6621a9b32d781)
            check_type(argname="argument param", value=param, expected_type=type_hints["param"])
        jsii.create(self.__class__, self, [param])

    @jsii.member(jsii_name="createIotaToken")
    def create_iota_token(
        self,
        iota_config_id: builtins.str,
        did: builtins.str,
        iota_session_id: typing.Optional[builtins.str] = None,
    ) -> "IotaTokenOutput":
        '''
        :param iota_config_id: -
        :param did: -
        :param iota_session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e4e9e70b8509c9bb72a927cf1033b2f1a7c360b093c4f9f125ba51962dfd36)
            check_type(argname="argument iota_config_id", value=iota_config_id, expected_type=type_hints["iota_config_id"])
            check_type(argname="argument did", value=did, expected_type=type_hints["did"])
            check_type(argname="argument iota_session_id", value=iota_session_id, expected_type=type_hints["iota_session_id"])
        return typing.cast("IotaTokenOutput", jsii.invoke(self, "createIotaToken", [iota_config_id, did, iota_session_id]))

    @jsii.member(jsii_name="fetchProjectScopedToken")
    def fetch_project_scoped_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.ainvoke(self, "fetchProjectScopedToken", []))


class BffHeaders(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi-tdk/auth-provider.BffHeaders",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getBffHeaders")
    def get_bff_headers(
        self,
        cookie_name: builtins.str,
        session_id: builtins.str,
        cli_version: typing.Optional[builtins.str] = None,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        '''
        :param cookie_name: -
        :param session_id: -
        :param cli_version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8f68ce25e2047d50c8f1e2d1a6815c7f7ff4fc4ba678d47532446710bd1ff6)
            check_type(argname="argument cookie_name", value=cookie_name, expected_type=type_hints["cookie_name"])
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument cli_version", value=cli_version, expected_type=type_hints["cli_version"])
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.invoke(self, "getBffHeaders", [cookie_name, session_id, cli_version]))


@jsii.interface(jsii_type="@affinidi-tdk/auth-provider.IAuthProviderParams")
class IAuthProviderParams(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        ...

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        ...

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tokenId")
    def token_id(self) -> builtins.str:
        ...

    @token_id.setter
    def token_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="apiGatewayUrl")
    def api_gateway_url(self) -> typing.Optional[builtins.str]:
        ...

    @api_gateway_url.setter
    def api_gateway_url(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> typing.Optional[builtins.str]:
        ...

    @key_id.setter
    def key_id(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> typing.Optional[builtins.str]:
        ...

    @passphrase.setter
    def passphrase(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        ...

    @token_endpoint.setter
    def token_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IAuthProviderParamsProxy:
    __jsii_type__: typing.ClassVar[str] = "@affinidi-tdk/auth-provider.IAuthProviderParams"

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec76b04f0867e837d7ee6d4713cbbaec9698ede2099893bd2af38caa524eb65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b9b35c331d62341caf3866b2e47a9cbb6979400e80500f597a4e30d94f50e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenId")
    def token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenId"))

    @token_id.setter
    def token_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2176875ff16fd4b9541d04c7e8bd451d2d51ddbfb8017715bd72a9beb6b6fb4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiGatewayUrl")
    def api_gateway_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiGatewayUrl"))

    @api_gateway_url.setter
    def api_gateway_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbb1478601c2ce64e1a7a0467bca02f24dee25d6989fe577135dd08293b13d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGatewayUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027ff0d91afd5dc323ff8eba59250e562d43bf190d82c07ee693ad11b1c07ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passphrase"))

    @passphrase.setter
    def passphrase(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7dc7f06c6ab9ffca7ab9c6aaf5e8756c7f2bb955ee27858cc1879966f864816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passphrase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6033c88f1959a48939af82c5d8bf0851a5f7e75e3d4e6d570fad4a063fd05400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAuthProviderParams).__jsii_proxy_class__ = lambda : _IAuthProviderParamsProxy


@jsii.interface(jsii_type="@affinidi-tdk/auth-provider.ISignPayload")
class ISignPayload(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        ...

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        ...

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        ...

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="tokenId")
    def token_id(self) -> builtins.str:
        ...

    @token_id.setter
    def token_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> typing.Optional[builtins.str]:
        ...

    @passphrase.setter
    def passphrase(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISignPayloadProxy:
    __jsii_type__: typing.ClassVar[str] = "@affinidi-tdk/auth-provider.ISignPayload"

    @builtins.property
    @jsii.member(jsii_name="audience")
    def audience(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audience"))

    @audience.setter
    def audience(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9349aedb11daef91bda90271c1b01ce24eb6ad92833164760b8a3d596d7c14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audience", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d001637c7fccb139abe824adc87273a75e7d605cd80e10d05579c2a02f304a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698b7523ca6b9bb8c41589258444cb8f277fab236f97f679d284b7993502125b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenId")
    def token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenId"))

    @token_id.setter
    def token_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dfddcab5336792d13214deab3cd6d86037dd7223d922ac7d881264a245d6281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passphrase"))

    @passphrase.setter
    def passphrase(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832e521c7f3a0551405b74d12d95e26394613278302bd6b3aa949911bbe2034a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passphrase", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISignPayload).__jsii_proxy_class__ = lambda : _ISignPayloadProxy


@jsii.interface(jsii_type="@affinidi-tdk/auth-provider.IValidateToken")
class IValidateToken(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="isExpired")
    def is_expired(self) -> builtins.bool:
        ...

    @is_expired.setter
    def is_expired(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="isValid")
    def is_valid(self) -> builtins.bool:
        ...

    @is_valid.setter
    def is_valid(self, value: builtins.bool) -> None:
        ...


class _IValidateTokenProxy:
    __jsii_type__: typing.ClassVar[str] = "@affinidi-tdk/auth-provider.IValidateToken"

    @builtins.property
    @jsii.member(jsii_name="isExpired")
    def is_expired(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isExpired"))

    @is_expired.setter
    def is_expired(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a2c3006265bc67c0eb852529a720b707b6fd6d82e0838af8c759fb0e3c4ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isExpired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isValid")
    def is_valid(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isValid"))

    @is_valid.setter
    def is_valid(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4defa2b1dff045e08c22a6e90d8e6cb9234d84ddbbe7a12994233ff2e041b9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValid", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IValidateToken).__jsii_proxy_class__ = lambda : _IValidateTokenProxy


class Iota(metaclass=jsii.JSIIMeta, jsii_type="@affinidi-tdk/auth-provider.Iota"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="signIotaJwt")
    def sign_iota_jwt(
        self,
        project_id: builtins.str,
        iota_config_id: builtins.str,
        iota_session_id: builtins.str,
        __3: ISignPayload,
    ) -> builtins.str:
        '''
        :param project_id: -
        :param iota_config_id: -
        :param iota_session_id: -
        :param __3: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a1e584743a5e28b5ee76f547a47b96436bca2429ffcecb58306a3fc848cf1b)
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument iota_config_id", value=iota_config_id, expected_type=type_hints["iota_config_id"])
            check_type(argname="argument iota_session_id", value=iota_session_id, expected_type=type_hints["iota_session_id"])
            check_type(argname="argument __3", value=__3, expected_type=type_hints["__3"])
        return typing.cast(builtins.str, jsii.invoke(self, "signIotaJwt", [project_id, iota_config_id, iota_session_id, __3]))


@jsii.data_type(
    jsii_type="@affinidi-tdk/auth-provider.IotaTokenOutput",
    jsii_struct_bases=[],
    name_mapping={"iota_jwt": "iotaJwt", "iota_session_id": "iotaSessionId"},
)
class IotaTokenOutput:
    def __init__(
        self,
        *,
        iota_jwt: builtins.str,
        iota_session_id: builtins.str,
    ) -> None:
        '''
        :param iota_jwt: 
        :param iota_session_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6bb1de242176c558470bc42a2a1c9f8fc79f3e43eb11294b9a8e4c67711731)
            check_type(argname="argument iota_jwt", value=iota_jwt, expected_type=type_hints["iota_jwt"])
            check_type(argname="argument iota_session_id", value=iota_session_id, expected_type=type_hints["iota_session_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iota_jwt": iota_jwt,
            "iota_session_id": iota_session_id,
        }

    @builtins.property
    def iota_jwt(self) -> builtins.str:
        result = self._values.get("iota_jwt")
        assert result is not None, "Required property 'iota_jwt' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iota_session_id(self) -> builtins.str:
        result = self._values.get("iota_session_id")
        assert result is not None, "Required property 'iota_session_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotaTokenOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Jwt(metaclass=jsii.JSIIMeta, jsii_type="@affinidi-tdk/auth-provider.Jwt"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fetchPublicKey")
    def fetch_public_key(self, api_gateway_url: builtins.str) -> builtins.str:
        '''
        :param api_gateway_url: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef23ac51be6bc0dbf78dcdef5dcd3e70348889bb9a3968a7526baff8e33c8ac)
            check_type(argname="argument api_gateway_url", value=api_gateway_url, expected_type=type_hints["api_gateway_url"])
        return typing.cast(builtins.str, jsii.ainvoke(self, "fetchPublicKey", [api_gateway_url]))

    @jsii.member(jsii_name="validateToken")
    def validate_token(
        self,
        token: builtins.str,
        public_key: builtins.str,
    ) -> IValidateToken:
        '''
        :param token: -
        :param public_key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13e86e36e8828008f1b3c6f2d084af6b45e162db595854767bbd6d6f46fa505)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
        return typing.cast(IValidateToken, jsii.invoke(self, "validateToken", [token, public_key]))


class ProjectScopedToken(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi-tdk/auth-provider.ProjectScopedToken",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fetchProjectScopedToken")
    def fetch_project_scoped_token(self, __0: "IFetchProjectScopedToken") -> typing.Any:
        '''
        :param __0: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7128fa0590045c08aafd8b12dc1239da7314e89916a66625e3ef33d71b50acc)
            check_type(argname="argument __0", value=__0, expected_type=type_hints["__0"])
        return typing.cast(typing.Any, jsii.ainvoke(self, "fetchProjectScopedToken", [__0]))

    @jsii.member(jsii_name="getUserAccessToken")
    def get_user_access_token(self, __0: ISignPayload) -> typing.Any:
        '''
        :param __0: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ebedcb095bd4580da3af949f59d4a28284144089e40b49f980e2d3f96477e8)
            check_type(argname="argument __0", value=__0, expected_type=type_hints["__0"])
        return typing.cast(typing.Any, jsii.ainvoke(self, "getUserAccessToken", [__0]))

    @jsii.member(jsii_name="signPayload")
    def sign_payload(self, __0: ISignPayload) -> builtins.str:
        '''
        :param __0: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce98596a484db1d16279cc7ef98fc58de3ddbe9d5f3ade4d8a49201039aff21)
            check_type(argname="argument __0", value=__0, expected_type=type_hints["__0"])
        return typing.cast(builtins.str, jsii.ainvoke(self, "signPayload", [__0]))


@jsii.interface(jsii_type="@affinidi-tdk/auth-provider.IFetchProjectScopedToken")
class IFetchProjectScopedToken(ISignPayload, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="apiGatewayUrl")
    def api_gateway_url(self) -> builtins.str:
        ...

    @api_gateway_url.setter
    def api_gateway_url(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        ...

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        ...


class _IFetchProjectScopedTokenProxy(
    jsii.proxy_for(ISignPayload), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@affinidi-tdk/auth-provider.IFetchProjectScopedToken"

    @builtins.property
    @jsii.member(jsii_name="apiGatewayUrl")
    def api_gateway_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGatewayUrl"))

    @api_gateway_url.setter
    def api_gateway_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc4db8339b2ee1790a1a7b09b5b5435114a70851d999d4d5c24ea7fd4b88134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGatewayUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bfecf4546a879d848e26fb1c3a09e26f928eb074fbaf172520fefefa0a9766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFetchProjectScopedToken).__jsii_proxy_class__ = lambda : _IFetchProjectScopedTokenProxy


__all__ = [
    "AuthProvider",
    "BffHeaders",
    "IAuthProviderParams",
    "IFetchProjectScopedToken",
    "ISignPayload",
    "IValidateToken",
    "Iota",
    "IotaTokenOutput",
    "Jwt",
    "ProjectScopedToken",
]

publication.publish()

def _typecheckingstub__d864337db85b1ea4c15a8b13092be48e1a0f7026ae9183bfd6c6621a9b32d781(
    param: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e4e9e70b8509c9bb72a927cf1033b2f1a7c360b093c4f9f125ba51962dfd36(
    iota_config_id: builtins.str,
    did: builtins.str,
    iota_session_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8f68ce25e2047d50c8f1e2d1a6815c7f7ff4fc4ba678d47532446710bd1ff6(
    cookie_name: builtins.str,
    session_id: builtins.str,
    cli_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec76b04f0867e837d7ee6d4713cbbaec9698ede2099893bd2af38caa524eb65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b9b35c331d62341caf3866b2e47a9cbb6979400e80500f597a4e30d94f50e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2176875ff16fd4b9541d04c7e8bd451d2d51ddbfb8017715bd72a9beb6b6fb4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbb1478601c2ce64e1a7a0467bca02f24dee25d6989fe577135dd08293b13d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027ff0d91afd5dc323ff8eba59250e562d43bf190d82c07ee693ad11b1c07ac9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dc7f06c6ab9ffca7ab9c6aaf5e8756c7f2bb955ee27858cc1879966f864816(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6033c88f1959a48939af82c5d8bf0851a5f7e75e3d4e6d570fad4a063fd05400(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9349aedb11daef91bda90271c1b01ce24eb6ad92833164760b8a3d596d7c14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d001637c7fccb139abe824adc87273a75e7d605cd80e10d05579c2a02f304a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698b7523ca6b9bb8c41589258444cb8f277fab236f97f679d284b7993502125b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dfddcab5336792d13214deab3cd6d86037dd7223d922ac7d881264a245d6281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832e521c7f3a0551405b74d12d95e26394613278302bd6b3aa949911bbe2034a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a2c3006265bc67c0eb852529a720b707b6fd6d82e0838af8c759fb0e3c4ed7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4defa2b1dff045e08c22a6e90d8e6cb9234d84ddbbe7a12994233ff2e041b9b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a1e584743a5e28b5ee76f547a47b96436bca2429ffcecb58306a3fc848cf1b(
    project_id: builtins.str,
    iota_config_id: builtins.str,
    iota_session_id: builtins.str,
    __3: ISignPayload,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6bb1de242176c558470bc42a2a1c9f8fc79f3e43eb11294b9a8e4c67711731(
    *,
    iota_jwt: builtins.str,
    iota_session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef23ac51be6bc0dbf78dcdef5dcd3e70348889bb9a3968a7526baff8e33c8ac(
    api_gateway_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13e86e36e8828008f1b3c6f2d084af6b45e162db595854767bbd6d6f46fa505(
    token: builtins.str,
    public_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7128fa0590045c08aafd8b12dc1239da7314e89916a66625e3ef33d71b50acc(
    __0: IFetchProjectScopedToken,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ebedcb095bd4580da3af949f59d4a28284144089e40b49f980e2d3f96477e8(
    __0: ISignPayload,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce98596a484db1d16279cc7ef98fc58de3ddbe9d5f3ade4d8a49201039aff21(
    __0: ISignPayload,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc4db8339b2ee1790a1a7b09b5b5435114a70851d999d4d5c24ea7fd4b88134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bfecf4546a879d848e26fb1c3a09e26f928eb074fbaf172520fefefa0a9766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
