# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import re


def convert(text):
    return int(text) if text.isdigit() else text.lower()


def natural_sort(data):
    return sorted(data, key=lambda key: [convert(c) for c in re.split("([0-9]+)", key)])
