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
import unittest
import json

import check_uuid as cu
import tempest as t

pkg = t
checker = cu.TestChecker(pkg)
tests = checker.get_tests()


def is_test_method(method):
    return method.startswith('test_')


def inheritors(parent_class, n):
    res = {}
    subs = parent_class.__subclasses__()
    res['class'] = parent_class
    res['children'] = []
    res['methods'] = []
    all_test_methods = dict(parent_class.__dict__).keys()
    for method in all_test_methods:
        if is_test_method(method):
            res['methods'].append(method)
    for sub in subs:
        sub_res, _ = inheritors(sub, n)
        res['children'].append(sub_res)
    if not res['children']:
        del res['children']
    if not res['methods']:
        n.append(parent_class)
        del res['methods']
    return res, n

res = {}
no_methods = []
a, no_methods = inheritors(unittest.TestCase, no_methods)
pprint.pprint(a)
print '\n----------------------------------------------------------'
pprint.pprint(no_methods)
f_res = json.dumps(str(a))

output_file = 'res.json'
with open(output_file, 'w') as outf:
    outf.write(f_res)

output_file = 'without_tests.txt'
with open(output_file, 'w') as outf:
    for n in no_methods:
        outf.writelines(str(n))
        outf.writelines("\n")

