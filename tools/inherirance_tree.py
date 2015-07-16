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
import testtools
import inspect

import check_uuid as cu
import tempest as t

pkg = t
checker = cu.TestChecker(pkg)
tests = checker.get_tests()


def is_test_method(method):
    return method.startswith('test_')


def does_class_have_testmethods(class_name):
    all_test_methods = dict(class_name.__dict__).keys()
    for method in all_test_methods:
        if is_test_method(method):
            return True
    else:
        return False


def inheritors(parent_class, n):
    res = {}
    subs = parent_class.__subclasses__()
    res['class'] = parent_class
    res['children'] = []
    res['methods'] = []
    res['vars'] = []
    res['parent_tests'] = []
    res['closest_parent'] = []
    res['p_parent_tests'] = []
    all_test_methods = dict(parent_class.__dict__).keys()
    for method in all_test_methods:
        if is_test_method(method):
            res['methods'].append(method)
    res['closest_parent'] = inspect.getmro(parent_class)[1]

    if does_class_have_testmethods(inspect.getmro(parent_class)[1]):
        for m in dict(inspect.getmro(parent_class)[1].__dict__).keys():
            if is_test_method(m):
                res['parent_tests'].append(m)
        for v in vars(parent_class).keys():
            if not v.startswith("__"):
                res['vars'].append(v)

    if does_class_have_testmethods(inspect.getmro(parent_class)[2]):
        for m in dict(inspect.getmro(parent_class)[2].__dict__).keys():
            if is_test_method(m):
                res['p_parent_tests'].append(m)

    for sub in subs:
        sub_res, _ = inheritors(sub, n)
        res['children'].append(sub_res)
    # if not res['children']:
    #     del res['children']
    if not res['methods']:
        if does_class_have_testmethods(inspect.getmro(parent_class)[1]):

            variables = []
            for v in vars(parent_class).keys():
                if not v.startswith("__"):
                    variables.append(v)

            parents = []
            pars = inspect.getmro(parent_class)[1:-3]
            for p in pars:
                if not str(p).split("'")[1].split('.')[-1].startswith("Base"):
                    parents.append(p)
                else:
                    break

            parent_tests = []
            for p in parents:
                for m in dict(p.__dict__).keys():
                    if is_test_method(m):
                        parent_tests.append(m)

            n.append({'class:': parent_class,
                      'vars': variables,
                      'parents': parents,
                      'parent_tests': parent_tests})

        # del res['methods']
    return res, n

no_methods = []
a, no_methods = inheritors(testtools.testcase.TestCase, no_methods)
pprint.pprint(a)
print '\n----------------------------------------------------------'

# pprint.pprint(no_methods)
# print len(no_methods)

# f = []
# f.append(a)
# f1 = json.dumps(f, indent=4)
# output_file = 'res.json'
# with open(output_file, 'w') as outf:
#     outf.writelines(f1)
#     outf.write('\n')

# n_res = json.dumps(no_methods, indent=4)
#
# output_file = 'without_tests.txt'
# with open(output_file, 'w') as outf:
#     outf.writelines(n_res)
#     outf.write('\n')
#
