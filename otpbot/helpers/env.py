import base64
import logging
import os

import boto3

from ..constant import CRYPTO_ENCRYPTION_ENV_VAR, CRYPTO_SIGN_ENV_VAR, TOKEN_ENV_VAR

logger = logging.getLogger(__name__)


def check_environments():
    _check_token()
    _check_credentials()
    _check_keys()


def _check_token():
    if os.getenv(TOKEN_ENV_VAR) is None:
        logger.error(
            f"Environment variable {TOKEN_ENV_VAR} must be set with valid Telegram Token."
        )
        exit(-1)


def _check_credentials():
    sts = boto3.client("sts")
    try:
        sts.get_caller_identity()
        logger.info("Valid AWS credentials found.")
    except Exception:
        logger.error("AWS credentials are not set or invalid.")
        exit(-1)


def _check_keys():
    if None in [os.getenv(CRYPTO_ENCRYPTION_ENV_VAR), os.getenv(CRYPTO_SIGN_ENV_VAR)]:
        logger.error(
            f"Environment variables {CRYPTO_ENCRYPTION_ENV_VAR} and {CRYPTO_SIGN_ENV_VAR} must be set."
            "\nYou can use following python script to generate one:\n\nimport os,base64\nbase64.b64encode(os.urandom(16)).decode('utf-8')"
        )
        exit(-1)
    if (
        len(base64.b64decode(os.getenv(CRYPTO_ENCRYPTION_ENV_VAR))) not in [16, 24, 32]
    ) or (len(base64.b64decode(os.getenv(CRYPTO_SIGN_ENV_VAR))) not in [16, 24, 32]):
        logger.error(
            f"{CRYPTO_ENCRYPTION_ENV_VAR} or {CRYPTO_SIGN_ENV_VAR} has invalid length."
            "\nValid length are 128,192 or 256 bits."
            "\nYou can use following python script to generate one:\n\nimport os,base64\nbase64.b64encode(os.urandom(16)).decode('utf-8')"
        )
        exit(-1)
