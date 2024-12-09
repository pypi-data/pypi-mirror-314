r'''
# @affinidi/iota-core

## Install

### Javascript

```bash
npm install @affinidi-tdk/iota-core
```

### Python

run inside [python virtual env](https://docs.python.org/3/library/venv.html)

```bash
pip install affinidi_tdk_iota_core
```

## Usage

Head over to [Affinidi Iota Framework documentation](https://docs.affinidi.com/frameworks/iota-framework) page to better understand how the service works.

For details on how to use this library please head over to [iota-core documentation](https://docs.affinidi.com/dev-tools/affinidi-tdk/libraries/iota-core) page.
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


@jsii.data_type(
    jsii_type="@affinidi-tdk/iota-core.Credentials",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "expiration": "expiration",
        "secret_key": "secretKey",
        "session_token": "sessionToken",
    },
)
class Credentials:
    def __init__(
        self,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[datetime.datetime] = None,
        secret_key: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key_id: 
        :param expiration: 
        :param secret_key: 
        :param session_token: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9555a950a5041dbf4b431b06527d831911230fb74175494a6e646648a79f298)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if expiration is not None:
            self._values["expiration"] = expiration
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration(self) -> typing.Optional[datetime.datetime]:
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Credentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@affinidi-tdk/iota-core.IAuthProviderParams")
class IAuthProviderParams(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="apiGW")
    def api_gw(self) -> builtins.str:
        ...

    @api_gw.setter
    def api_gw(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        ...

    @region.setter
    def region(self, value: builtins.str) -> None:
        ...


class _IAuthProviderParamsProxy:
    __jsii_type__: typing.ClassVar[str] = "@affinidi-tdk/iota-core.IAuthProviderParams"

    @builtins.property
    @jsii.member(jsii_name="apiGW")
    def api_gw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGW"))

    @api_gw.setter
    def api_gw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f911ac6d915182a6fa8b7fdb3886f53099b31b4d4ca45dde5a80ecbda67a4fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGW", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3397434ca71e28890c247dd83532a7225121cb0234987f4a9453a5129ed8374c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAuthProviderParams).__jsii_proxy_class__ = lambda : _IAuthProviderParamsProxy


@jsii.data_type(
    jsii_type="@affinidi-tdk/iota-core.IdentityCredentials",
    jsii_struct_bases=[],
    name_mapping={"identity_id": "identityId", "token": "token"},
)
class IdentityCredentials:
    def __init__(self, *, identity_id: builtins.str, token: builtins.str) -> None:
        '''
        :param identity_id: 
        :param token: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a16dcefd813a348606d27e66c2c6434584832587812eecb156f0424475f82f)
            check_type(argname="argument identity_id", value=identity_id, expected_type=type_hints["identity_id"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_id": identity_id,
            "token": token,
        }

    @builtins.property
    def identity_id(self) -> builtins.str:
        result = self._values.get("identity_id")
        assert result is not None, "Required property 'identity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> builtins.str:
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Iota(metaclass=jsii.JSIIMeta, jsii_type="@affinidi-tdk/iota-core.Iota"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="limitedTokenToIotaCredentials")
    @builtins.classmethod
    def limited_token_to_iota_credentials(
        cls,
        token: builtins.str,
    ) -> "IotaCredentials":
        '''
        :param token: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40b101b3e942acbe75cc253a2139a8c07c6e4d8a86b43ecf88f015a6ca56a6c)
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        return typing.cast("IotaCredentials", jsii.sinvoke(cls, "limitedTokenToIotaCredentials", [token]))


class IotaAuthProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@affinidi-tdk/iota-core.IotaAuthProvider",
):
    def __init__(
        self,
        param: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param param: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944fb76ada99e575f6d980205092b934cf7f47d82e7c861d4dedd685c9290cb5)
            check_type(argname="argument param", value=param, expected_type=type_hints["param"])
        jsii.create(self.__class__, self, [param])

    @jsii.member(jsii_name="exchangeIdentityCredentials")
    def exchange_identity_credentials(
        self,
        *,
        identity_id: builtins.str,
        token: builtins.str,
    ) -> Credentials:
        '''
        :param identity_id: 
        :param token: 
        '''
        identity_credentials = IdentityCredentials(
            identity_id=identity_id, token=token
        )

        return typing.cast(Credentials, jsii.ainvoke(self, "exchangeIdentityCredentials", [identity_credentials]))

    @jsii.member(jsii_name="limitedTokenToIotaCredentials")
    def limited_token_to_iota_credentials(
        self,
        limited_token: builtins.str,
    ) -> "IotaCredentials":
        '''
        :param limited_token: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__260f8381230bd6e5012fe099ee5e384a3f820aa9cf5f045a1883b4e714a9a828)
            check_type(argname="argument limited_token", value=limited_token, expected_type=type_hints["limited_token"])
        return typing.cast("IotaCredentials", jsii.ainvoke(self, "limitedTokenToIotaCredentials", [limited_token]))

    @builtins.property
    @jsii.member(jsii_name="apiGW")
    def api_gw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGW"))

    @api_gw.setter
    def api_gw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c50b0c193d60cbea8f29c9d810e8bc45be3cdeaa759dd883b1062f99dd0d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGW", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daac31b8a626b45ce3780f76640f5ad0a3ee3a89eaee51c1832f3b50b5b29be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@affinidi-tdk/iota-core.IotaCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "connection_client_id": "connectionClientId",
        "credentials": "credentials",
    },
)
class IotaCredentials:
    def __init__(
        self,
        *,
        connection_client_id: builtins.str,
        credentials: typing.Union[Credentials, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param connection_client_id: 
        :param credentials: 
        '''
        if isinstance(credentials, dict):
            credentials = Credentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e88094fa71031782e7d374dcbff7ea79879a9f51e36d13fd03ebe1c1baf77d6)
            check_type(argname="argument connection_client_id", value=connection_client_id, expected_type=type_hints["connection_client_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_client_id": connection_client_id,
            "credentials": credentials,
        }

    @builtins.property
    def connection_client_id(self) -> builtins.str:
        result = self._values.get("connection_client_id")
        assert result is not None, "Required property 'connection_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> Credentials:
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(Credentials, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotaCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Credentials",
    "IAuthProviderParams",
    "IdentityCredentials",
    "Iota",
    "IotaAuthProvider",
    "IotaCredentials",
]

publication.publish()

def _typecheckingstub__e9555a950a5041dbf4b431b06527d831911230fb74175494a6e646648a79f298(
    *,
    access_key_id: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[datetime.datetime] = None,
    secret_key: typing.Optional[builtins.str] = None,
    session_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f911ac6d915182a6fa8b7fdb3886f53099b31b4d4ca45dde5a80ecbda67a4fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3397434ca71e28890c247dd83532a7225121cb0234987f4a9453a5129ed8374c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a16dcefd813a348606d27e66c2c6434584832587812eecb156f0424475f82f(
    *,
    identity_id: builtins.str,
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40b101b3e942acbe75cc253a2139a8c07c6e4d8a86b43ecf88f015a6ca56a6c(
    token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944fb76ada99e575f6d980205092b934cf7f47d82e7c861d4dedd685c9290cb5(
    param: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__260f8381230bd6e5012fe099ee5e384a3f820aa9cf5f045a1883b4e714a9a828(
    limited_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c50b0c193d60cbea8f29c9d810e8bc45be3cdeaa759dd883b1062f99dd0d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daac31b8a626b45ce3780f76640f5ad0a3ee3a89eaee51c1832f3b50b5b29be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e88094fa71031782e7d374dcbff7ea79879a9f51e36d13fd03ebe1c1baf77d6(
    *,
    connection_client_id: builtins.str,
    credentials: typing.Union[Credentials, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass
