import base64
import os

from dynamodb_encryption_sdk.delegated_keys.jce import JceNameLocalDelegatedKey
from dynamodb_encryption_sdk.identifiers import EncryptionKeyType, KeyEncodingType
from dynamodb_encryption_sdk.material_providers.wrapped import (
    WrappedCryptographicMaterialsProvider,
)

from ..constant import CRYPTO_ENCRYPTION_ENV_VAR, CRYPTO_SIGN_ENV_VAR

_encryption_key = JceNameLocalDelegatedKey(
    key=base64.b64decode(
        os.getenv(CRYPTO_ENCRYPTION_ENV_VAR) or base64.b64encode(os.urandom(32))
    ),
    algorithm="AES",
    key_type=EncryptionKeyType.SYMMETRIC,
    key_encoding=KeyEncodingType.RAW,
)
_signing_key = JceNameLocalDelegatedKey(
    key=base64.b64decode(
        os.getenv(CRYPTO_SIGN_ENV_VAR) or base64.b64encode(os.urandom(32))
    ),
    algorithm="HmacSHA512",
    key_type=EncryptionKeyType.SYMMETRIC,
    key_encoding=KeyEncodingType.RAW,
)

wrapped_material_provider = WrappedCryptographicMaterialsProvider(
    wrapping_key=_encryption_key,
    unwrapping_key=_encryption_key,
    signing_key=_signing_key,
)
