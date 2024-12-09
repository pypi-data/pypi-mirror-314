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
import logging
import sqlalchemy as db
from datetime import datetime


class CrypterDb(object):
    def __init__(self, db_name, db_path):
        self.db_name = db_name
        self.db_file = f"{os.path.join(db_path, db_name)}.db"
        self.engine = None
        self.connection = None
        self.meta = None

    def __enter__(self):
        self.engine = db.create_engine(f"sqlite:///{self.db_file}")
        self.meta = db.MetaData()
        self.connection = self.engine.connect()
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self.connection:
            self.connection.commit()
            self.connection.close()
        self.connection = None
        self.engine = None
        self.meta = None

    def is_db_present(self):
        return os.path.exists(self.db_file)

    def setup(self):
        secret = db.Table("secret", self.meta,
                          db.Column("Id", db.Integer(), nullable=False, primary_key=True, autoincrement=True),
                          db.Column("key", db.String(255), nullable=False),
                          db.Column("created_at", db.DATETIME, nullable=True, default=datetime.now()),
                          db.Column("modified_at", db.DATETIME, nullable=True, default=datetime.now()),
                          db.Column("is_deleted", db.Boolean, nullable=True, default=False),
                          sqlite_autoincrement=True
        )
        records = db.Table("records", self.meta,
                    db.Column("Id", db.Integer(), nullable=False, primary_key=True, autoincrement=True),
                    db.Column("key", db.String(255), nullable=False),
                    db.Column("name", db.String(255), nullable=False),
                    db.Column("password", db.String(255), nullable=False),
                    db.Column("created_at", db.DATETIME, nullable=True, default=datetime.now()),
                    db.Column("modified_at", db.DATETIME, nullable=True, default=datetime.now()),
                    db.Column("is_deleted", db.Boolean, nullable=True, default=False),
                    sqlite_autoincrement=True
        )
        self.meta.create_all(self.engine)

    def execute(self, query):
        result = self.connection.execute(query)
        return result

    def insert(self, table_name, values, return_columns=None):
        if not self.is_db_present():
            raise Exception("No database found. Please run the 'crypter init' command to setup.")
        table = db.Table(table_name, self.meta, autoload_with=self.engine)
        query = table.insert().values(**values)
        if return_columns:
            args = [table.columns[col] for col in return_columns]
            query = query.returning(*args)
        return self.execute(query).fetchall()

    def update(self):
        pass

    def get(self, table_name, key_names, return_columns=None):
        if not self.is_db_present():
            raise Exception("No database found. Please run the 'crypter init' command to setup.")
        table = db.Table(table_name, self.meta, autoload_with=self.engine)
        query = table.select()
        if key_names:
            query = query.where(table.columns.key.in_(key_names))
        if return_columns:
            args = [table.columns[col] for col in return_columns]
            query = query.with_only_columns(*args)
        return self.execute(query).fetchall()

    def delete(self, table_name, key_names, return_columns=None):
        if not self.is_db_present():
            raise Exception("No database found. Please run the 'crypter init' command to setup.")
        table = db.Table(table_name, self.meta, autoload_with=self.engine)
        result = list()
        query = table.delete().where(table.columns.key.in_(key_names))
        if return_columns:
            args = [table.columns[col] for col in return_columns]
            query = query.returning(*args)
        return self.execute(query).fetchall()

    def drop(self, table_name):
        if not self.is_db_present():
            raise Exception("No database found. Please run the 'crypter init' command to setup.")
        table = db.Table(table_name, self.meta, autoload_with=self.engine)
        table.drop(self.engine)
        