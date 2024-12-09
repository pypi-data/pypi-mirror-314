# BSD 3-Clause License
# Copyright (c) 2024, mac
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

import re
import base64
import random
import string
import hashlib
import secrets
from cryptography.fernet import Fernet


class CrypterTokenGenerator():
    @classmethod
    def generate_key(cls):
        return Fernet.generate_key()

    @classmethod
    def generate_password(cls, salt, chunk_size=4):
        sha256Hash = hashlib.sha256()
        sha256Hash.update(salt.encode())
        sha256HexDigest = sha256Hash.hexdigest()
        passwordString = base64.urlsafe_b64encode(sha256HexDigest.encode())
        lower_case_in_password = re.findall(f"[{string.ascii_lowercase}]", passwordString.decode())
        upper_case_in_password = re.findall(f"[{string.ascii_uppercase}]", passwordString.decode())
        digits_in_password = re.findall(f"[{string.digits}]", passwordString.decode())
        special_chars_in_password = re.findall(f"[{string.punctuation}]", passwordString.decode())
        special_chars_in_password.extend([secrets.choice(string.punctuation) for i in range(chunk_size)])
        random.shuffle(lower_case_in_password);random.shuffle(upper_case_in_password)
        random.shuffle(digits_in_password);random.shuffle(special_chars_in_password)
        final_password = lower_case_in_password[:chunk_size] + upper_case_in_password[:chunk_size] + digits_in_password[:chunk_size] + special_chars_in_password[:chunk_size]
        random.shuffle(final_password)

        return ''.join(final_password)

    @classmethod
    def encrypt(self, key, data):
        return Fernet.key(key).encrypt(data)

    @classmethod
    def decrypt(self, key, data):
        return Fernet.key(key).decrypt(data)

