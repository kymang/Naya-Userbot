# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import pymongo
import dns.resolver
from Prime.database.config_db import config


dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


class Database:
    def get(self, module: str, variable: str, default=None):
        """Get value from database"""
        raise NotImplementedError

    def set(self, module: str, variable: str, value):
        """Set key in database"""
        raise NotImplementedError

    def remove(self, module: str, variable: str):
        """Remove key from database"""
        raise NotImplementedError

    def get_collection(self, module: str) -> dict:
        """Get database for selected module"""
        raise NotImplementedError

    def close(self):
        """Close the database"""
        raise NotImplementedError


class MongoDatabase(Database):
    def __init__(self, url, name):
        self._client = pymongo.MongoClient(url)
        self._database = self._client[name]

    def set(self, module: str, variable: str, value):
        self._database[module].replace_one(
            {"var": variable}, {"var": variable, "val": value}, upsert=True
        )

    def get(self, module: str, variable: str, expected_value=None):
        doc = self._database[module].find_one({"var": variable})
        return expected_value if doc is None else doc["val"]

    def get_collection(self, module: str):
        return {item["var"]: item["val"] for item in self._database[module].find()}

    def remove(self, module: str, variable: str):
        self._database[module].delete_one({"var": variable})

    def close(self):
        self._client.close()
        
if config.db_type in ["mongo", "mongodb"]:
    db = MongoDatabase(config.db_url, config.db_name)
