#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Paul'
import os
from flask_script import Command, Manager, Option, Server, Shell
from app import create_app
from config import DevConfig

config = DevConfig
app = create_app(config)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
