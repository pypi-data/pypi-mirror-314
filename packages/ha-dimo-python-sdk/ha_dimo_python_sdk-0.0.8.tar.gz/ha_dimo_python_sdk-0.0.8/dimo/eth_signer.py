from typing import NewType
from eth_account import Account
from eth_account.messages import encode_defunct

HexStr = NewType("HexStr", str)


class EthSigner:
    @staticmethod
    def sign_message(message: str, private_key: str) -> str:
        private_key = add_0x_prefix(remove_0x_prefix(private_key))
        message_hash = encode_defunct(text=message)
        account = Account.from_key(private_key)
        signed_message = account.sign_message(message_hash)

        return add_0x_prefix(signed_message.signature.hex())


def is_0x_prefixed(value: str) -> bool:
    if not isinstance(value, str):
        raise TypeError(
            f"is_0x_prefixed requires text typed arguments. Got: {repr(value)}"
        )
    return value.startswith(("0x", "0X"))


def remove_0x_prefix(value: HexStr) -> HexStr:
    if is_0x_prefixed(value):
        return HexStr(value[2:])
    return value


def add_0x_prefix(value: HexStr) -> HexStr:
    if is_0x_prefixed(value):
        return value
    return HexStr("0x" + value)
