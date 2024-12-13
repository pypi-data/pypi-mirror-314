import random
import time
from typing import Union

import xxhash

ENCODING = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ENCODING_FIRST_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

last_time = 0
last_decimal = 0

def decimal_to_character(decimal: int) -> str:
    result = ""
    while decimal > 0:
        if decimal <= 62:
            result = ENCODING_FIRST_CHAR[decimal % 52] + result
            decimal //= 52
        else:
            result = ENCODING[decimal % 62] + result
            decimal //= 62
    return result or "0"

def character_to_decimal(character: str) -> int:
    decimal = 0
    base = len(ENCODING)
    for char in character:
        char_index = ENCODING.index(char)
        decimal = decimal * base + char_index
    return decimal

def get_max_rand_decimal(length: int) -> int:
    if length <= 0:
        return 0
    length -= 1
    decimal = 51
    while length > 0:
        length -= 1
        decimal = decimal * 62 + 61
    return decimal

def random_bigint(limit: int) -> int:
    if limit <= 0:
        raise ValueError("Limit must be larger than 0")

    width = (limit.bit_length() + 63) // 64
    max_value = 1 << (width * 64)
    min_value = max_value - (max_value % limit)

    while True:
        sample = random.getrandbits(width * 64)
        if sample < min_value:
            return sample % limit

class IdGenerator:
    def __init__(self, *, length: int = 24, timestamp: bool, fingerprint: bool = False,
                 hyphen: bool = False, sequential: bool = False, magic_number: int = 733882188971,
                 hash_seed: int = 0):
        self.__length = length
        self.__timestamp = timestamp
        self.__fingerprint = fingerprint
        self.__hyphen = hyphen
        self.__sequential = sequential
        self.__magic_number = magic_number
        self.__rand_length = self.__length + 1 - (7 if self.__timestamp else 0) - (5 if self.__fingerprint else 0)

        self.__max_rand_decimal = get_max_rand_decimal(self.__rand_length)
        self.__hash_seed = hash_seed

    def create_id(self, fingerprint: Union[bytes, str, None] = None) -> str:
        if self.__fingerprint and fingerprint is None:
            raise ValueError("fingerprint is required")

        now = int(time.time() * 1000)
        id_parts = []

        if self.__timestamp:
            timestamp_part = decimal_to_character(now - self.__magic_number)
            id_parts.append(timestamp_part[-7:])

        if self.__fingerprint:
            if isinstance(fingerprint, str):
                fingerprint = fingerprint.encode("utf-8")
            fingerprint_hash = xxhash.xxh64(fingerprint, self.__hash_seed).intdigest()
            id_parts.append(decimal_to_character(fingerprint_hash)[2:7])

        if self.__rand_length > 1:
            if self.__sequential:
                global last_decimal, last_time
                if last_time == now:
                    last_decimal += 1
                    decimal = last_decimal
                else:
                    last_time = now
                    decimal = random_bigint(self.__max_rand_decimal)
                    last_decimal = decimal
            else:
                decimal = random_bigint(self.__max_rand_decimal)
            rand_part = decimal_to_character(decimal).zfill(self.__rand_length)[1:]
            id_parts.append(rand_part)

        if self.__hyphen:
            return "-".join(id_parts)
        return "".join(id_parts)
