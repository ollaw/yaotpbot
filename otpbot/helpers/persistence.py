import logging
import os
from typing import List, Tuple

import boto3
from boto3.dynamodb.conditions import Key
from dynamodb_encryption_sdk.encrypted.resource import EncryptedResource

from ..constant import (
    DYNAMO__KEY_ID,
    DYNAMO__KEY_NAME,
    DYNAMO__KEY_SEED,
    DYNAMO_ENDPOINT_ENV_VAR,
    DYNAMO_TABLE_NAME,
)
from ..helpers.crypto import wrapped_material_provider

logger = logging.getLogger(__name__)

dynamo = boto3.resource("dynamodb", endpoint_url=os.getenv(DYNAMO_ENDPOINT_ENV_VAR))
client_crypto = EncryptedResource(
    resource=dynamo, materials_provider=wrapped_material_provider
).Table(DYNAMO_TABLE_NAME)


def get(chat_id: str, otp_name: str) -> str:
    if query := client_crypto.query(
        KeyConditionExpression=Key("id").eq(f"{chat_id}")
        & Key("name").eq(f"{otp_name}"),
    )["Items"]:
        return query[0]["seed"]
    else:
        logger.error(f"Key {otp_name} for {chat_id} was not found.")
        raise Exception(f"Key {otp_name} for {chat_id} was not found.")


def put(chat_id: str, otp_name: str, seed: str):
    client_crypto.put_item(
        Item={
            DYNAMO__KEY_ID: f"{chat_id}",
            DYNAMO__KEY_NAME: f"{otp_name}",
            DYNAMO__KEY_SEED: f"{seed}",
        },
    )


def exists(chat_id: str, otp_name: str) -> bool:
    query = client_crypto.query(
        KeyConditionExpression=Key("id").eq(f"{chat_id}")
        & Key("name").eq(f"{otp_name}"),
    )
    return "Items" in query


def delete(chat_id: str, otp_name: str) -> None:
    client_crypto.delete_item(Key={"id": f"{chat_id}", "name": f"{otp_name}"})


def load(chat_id: str) -> List[Tuple[str, str]]:
    if query := client_crypto.query(
        KeyConditionExpression=Key("id").eq(f"{chat_id}"),
        # ProjectionExpression="#n,seed",
        # ExpressionAttributeNames={"#n": "name"},
    )["Items"]:
        return [(k["name"], k["seed"]) for k in query]
    return []
