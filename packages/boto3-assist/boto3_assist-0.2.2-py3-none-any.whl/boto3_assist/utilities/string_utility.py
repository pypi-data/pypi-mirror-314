"""
Geek Cafe, LLC
Maintainers: Eric Wilson
MIT License.  See Project Root for the license information.
"""

import hashlib
import secrets
import string
from datetime import datetime
from decimal import Decimal
import uuid
import json
from aws_lambda_powertools import Logger

logger = Logger()


class JsonEncoder(json.JSONEncoder):
    """
    This class is used to serialize python generics which implement a __json_encode__ method
    and where the recipient does not require type hinting for deserialization.
    If type hinting is required, use GenericJsonEncoder
    """

    def default(self, o):
        # First, check if the object has a custom encoding method
        if hasattr(o, "__json_encode__"):
            return o.__json_encode__()

        # check for dictionary
        if hasattr(o, "__dict__"):
            return {k: v for k, v in o.__dict__.items() if not k.startswith("_")}

        # Handling datetime.datetime objects specifically
        elif isinstance(o, datetime):
            return o.isoformat()
        # handle decimal wrappers
        elif isinstance(o, Decimal):
            return float(o)

        logger.info(f"AplosJsonEncoder failing back: ${type(o)}")

        # Fallback to the base class implementation for other types

        try:
            return super().default(o)
        except TypeError:
            # If an object does not have a __dict__ attribute, you might want to handle it differently.
            # For example, you could choose to return str(o) or implement other specific cases.
            return str(
                o
            )  # Or any other way you wish to serialize objects without __dict__


class StringUtility:
    """String Utilities"""

    SPECIAL_CHARACTERS = "!\\#$%&()*+,-.:;<=>?@[]^_{|}~"

    @staticmethod
    def generate_random_string(
        length=12, digits=True, letters=True, special=False
    ) -> str:
        """
        Generate a random string with specified options.

        Args:
            length (int, optional): The length of the generated string. Defaults to 12.
            digits (bool, optional): Include digits in the string. Defaults to True.
            letters (bool, optional): Include letters in the string. Defaults to True.
            special (bool, optional): Include special characters in the string. Defaults to False.

        Returns:
            str: The generated random string.
        """
        characters = ""
        if letters:
            characters += string.ascii_letters
        if digits:
            characters += string.digits
        if special:
            characters += StringUtility.SPECIAL_CHARACTERS

        random_string = "".join(secrets.choice(characters) for _ in range(length))
        return random_string

    @staticmethod
    def generate_random_password(
        length=15, digits=True, letters=True, special=True
    ) -> str:
        """
        Generate a random password with specified options ensuring a minimum length of 8.

        Args:
            length (int, optional): The length of the generated password. Defaults to 15.
            digits (bool, optional): Include digits in the password. Defaults to True.
            letters (bool, optional): Include letters in the password. Defaults to True.
            special (bool, optional): Include special characters in the password. Defaults to True.

        Raises:
            RuntimeError: If no character sets are selected.

        Returns:
            str: The generated random password.
        """
        characters = ""
        if length < 8:
            length = 8

        if letters:
            characters += string.ascii_letters
        if digits:
            characters += string.digits
        if special:
            characters += StringUtility.SPECIAL_CHARACTERS

        if len(characters) == 0:
            raise RuntimeError(
                "You must choose at least one of the options: digits, letters, special"
            )

        password = []
        if letters:
            password.append(secrets.choice(string.ascii_lowercase))
            password.append(secrets.choice(string.ascii_lowercase))
            password.append(secrets.choice(string.ascii_uppercase))
            password.append(secrets.choice(string.ascii_uppercase))
        if digits:
            password.append(secrets.choice(string.digits))
            password.append(secrets.choice(string.digits))
        if special:
            password.append(secrets.choice(StringUtility.SPECIAL_CHARACTERS))
            password.append(secrets.choice(StringUtility.SPECIAL_CHARACTERS))

        remaining_length = length - len(password)
        password.extend(secrets.choice(characters) for _ in range(remaining_length))

        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    @staticmethod
    def wrap_text(text: str, max_width: int) -> str:
        """
        Wrap text to a specified maximum width.

        Args:
            text (str): The text to wrap.
            max_width (int): The maximum width of each line.

        Returns:
            str: The wrapped text.
        """
        wrapped_text = ""
        if not text:
            return text

        while len(text) > max_width:
            break_point = (
                text.rfind(" ", 0, max_width) if " " in text[0:max_width] else max_width
            )
            if break_point == -1:
                break_point = max_width
            wrapped_text += text[:break_point] + "\n"
            text = text[break_point:].lstrip()
        wrapped_text += text
        return wrapped_text

    @staticmethod
    def generate_uuid() -> str:
        """
        Generate a random UUID.

        Returns:
            str: The generated UUID as a string.
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_hash(input_string: str) -> str:
        """
        Generate a SHA-256 hash for the given input string.

        Args:
            input_string (str): The string to hash.

        Returns:
            str: The resulting hash value as a hexadecimal string.
        """
        encoded_string = input_string.encode()
        hash_object = hashlib.sha256()
        hash_object.update(encoded_string)
        return hash_object.hexdigest()

    @staticmethod
    def get_size_in_kb(input_string: str | dict) -> float:
        """
        Get the size of the input string in kilobytes.

        Args:
            input_string (str): The input string.

        Returns:
            int: The size of the input string in kilobytes.
        """
        size_in_bytes = StringUtility.get_size_in_bytes(input_string)

        size = size_in_bytes / 1024

        return size

    @staticmethod
    def get_size_in_bytes(input_string: str | dict) -> int:
        """
        Get the size of the input string in kilobytes.

        Args:
            input_string (str): The input string.

        Returns:
            int: The size of the input string in kilobytes.
        """
        if isinstance(input_string, dict):
            input_string = json.dumps(input_string, cls=JsonEncoder)
        # encodes the string to bytes, which is necessary because the length of a string
        # can differ from the length of its byte representation,
        # especially for non-ASCII characters.
        _bytes: bytes = input_string.encode("utf-8")
        size = int(len(_bytes))

        return size
