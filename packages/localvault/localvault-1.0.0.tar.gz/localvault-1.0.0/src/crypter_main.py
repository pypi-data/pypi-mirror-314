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

import os
import json
import random
import logging
from src.crypter_db import CrypterDb
from prettytable import PrettyTable
from src.crypter_config import CrypterConfig
from src.crypter_token_generator import CrypterTokenGenerator


class CrypterMain():
    @classmethod
    def init(cls):
        config_dir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        os.makedirs(config_dir, exist_ok=True)
        with CrypterDb(db_name=CrypterConfig.DB_NAME, db_path=config_dir) as db:
            db.setup()
            response = db.insert("secret", {'key': CrypterTokenGenerator.generate_key()}, return_columns=['Id'])
            return cls.format_response(response, return_columns=['Id'])

    @classmethod
    def add_key(cls, key_name, user_name, user_password, output_format='json'):
        config_dir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(db_name=CrypterConfig.DB_NAME, db_path=config_dir) as db:
            salt = list(key_name + user_name)
            random.shuffle(salt)
            user_password = user_password if user_password else CrypterTokenGenerator.generate_password(''.join(salt))
            values = {'key': key_name, 'name': user_name, 'password': user_password}
            return_columns = ['key', 'name', 'password']
            response = db.insert(table_name='records', values=values, return_columns=return_columns)
            return cls.format_response(response, return_columns=return_columns, output_format=output_format)

    @classmethod
    def get_key(cls, table_name='records', key_names=None, output_format='json'):
        config_dir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(db_name=CrypterConfig.DB_NAME, db_path=config_dir) as db:
            return_columns = ['key', 'name', 'password']
            response = db.get(table_name=table_name, key_names=key_names, return_columns=return_columns)
            return cls.format_response(response, return_columns=return_columns, output_format=output_format)

    @classmethod
    def delete_key(cls, table_name='records', key_names=None, output_format='json'):
        config_dir = os.path.join(CrypterConfig.CONFIG_DIR, CrypterConfig.CRYPTER_DIR)
        with CrypterDb(db_name=CrypterConfig.DB_NAME, db_path=config_dir) as db:
            return_columns = ['key', 'name', 'password']
            response = db.delete(table_name=table_name, key_names=key_names, return_columns=return_columns)
            return cls.format_response(response, return_columns=return_columns, output_format=output_format)

    @classmethod
    def _json_format_response(cls, query_result, return_columns):
        query_response = list()
        for row in query_result:
            r = dict()
            for col_name, col_value in zip(return_columns, list(row)):
                r.update({col_name: col_value})
            query_response.append(r)
        return json.dumps(query_response, indent=4)

    @classmethod
    def _tabular_format_response(cls, query_result, return_columns):
        table_data = PrettyTable(return_columns)
        for row in query_result:
            table_data.add_row(row)
        return table_data

    @classmethod
    def format_response(cls, query_result, return_columns, output_format='json'):
        if output_format == 'json':
            return cls._json_format_response(query_result, return_columns)

        if output_format == 'tabular':
            return cls._tabular_format_response(query_result, return_columns)

    @classmethod
    def cloud_init(cls):
        pass

    @classmethod
    def cloud_sync(cls):
        pass