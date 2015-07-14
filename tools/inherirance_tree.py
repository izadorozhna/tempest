#!/usr/bin/env python

# Copyright 2014 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pprint
import sys
import unittest
from optparse import OptionParser
import inspect

import check_uuid as cu
import tempest.api.identity as t

pkg = t
checker = cu.TestChecker(pkg)
tests = checker.get_tests()


def is_test_method(method):
    return method.startswith('test_')


def inheritors(parent_class):
    subclasses = set()
    work = [parent_class]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


def filter_all_children(test_class):
    inheritors_all = inheritors(test_class)
    children = sorted(list(inheritors_all))
    filtered_child = []
    for child in children:
        all_test_methods = dict(child.__dict__).keys()
        for method in all_test_methods:
            if is_test_method(method):
                # print child, method
                filtered_child.append(child)
    return filtered_child


all_children = filter_all_children(unittest.TestCase)
pprint.pprint(all_children)

