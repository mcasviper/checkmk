#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest
from cmk.gui.plugins.wato.check_parameters.interfaces import (
    _transform_discovery_if_rules,
    _transform_if_check_parameters,
)


@pytest.mark.parametrize('params, result', [
    (
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                True,
                {},
            ),
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                True,
                {},
            ),
        },
    ),
    (
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'alias',
                    'pad_portnumbers': True,
                    'labels': {
                        'single': 'wlp'
                    },
                },
            ),
            "grouping": (
                True,
                {
                    'group_items': [{
                        'group_name': 'wlp_group',
                        'member_appearance': 'index',
                    }],
                    'labels': {
                        'group': 'wlp'
                    },
                },
            ),
            'matching_conditions': (
                False,
                {
                    'porttypes': ['5', '9'],
                    'portstates': ['13'],
                    'admin_states': ['2'],
                    'match_index': ['10.*', '2'],
                    'match_desc': ['wlp'],
                    'match_alias': ['lo'],
                },
            ),
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'alias',
                    'pad_portnumbers': True,
                    'labels': {
                        'single': 'wlp'
                    },
                },
            ),
            "grouping": (
                True,
                {
                    'group_items': [{
                        'group_name': 'wlp_group',
                        'member_appearance': 'index',
                    }],
                    'labels': {
                        'group': 'wlp'
                    },
                },
            ),
            'matching_conditions': (
                False,
                {
                    'porttypes': ['5', '9'],
                    'portstates': ['13'],
                    'admin_states': ['2'],
                    'match_index': ['10.*', '2'],
                    'match_desc': ['wlp'],
                    'match_alias': ['lo'],
                },
            ),
        },
    ),
    (
        {
            'pad_portnumbers': False,
            'item_appearance': 'alias',
            'match_desc': ['enxe4b97ab99f99', 'vboxnet0', 'lo'],
            'portstates': ['1', '2', '3'],
            'porttypes': ['6'],
            'match_alias': ['enxe4b97ab99f99', 'vboxnet0', 'lo'],
            'rmon': True,
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'alias',
                    'pad_portnumbers': False,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'match_alias': ['enxe4b97ab99f99', 'vboxnet0', 'lo'],
                    'match_desc': ['enxe4b97ab99f99', 'vboxnet0', 'lo'],
                    'portstates': ['1', '2', '3'],
                    'porttypes': ['6'],
                },
            ),
        },
    ),
    (
        {
            'portstates': ['1', '2', '9'],
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'portstates': ['1', '2'],
                    'porttypes': [
                        '6', '32', '62', '117', '127', '128', '129', '180', '181', '182', '205',
                        '229'
                    ]
                },
            ),
        },
    ),
    (
        {
            'porttypes': ['6'],
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'portstates': ['1'],
                    'porttypes': ['6'],
                },
            ),
        },
    ),
    (
        {
            'portstates': ['9'],
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'admin_states': ['2'],
                    'porttypes': [
                        '6', '32', '62', '117', '127', '128', '129', '180', '181', '182', '205',
                        '229'
                    ],
                },
            ),
        },
    ),
    (
        {
            'match_alias': ['uplink'],
            'match_desc': ['eth.*'],
        },
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'portstates': ['1'],
                    'porttypes': [
                        '6', '32', '62', '117', '127', '128', '129', '180', '181', '182', '205',
                        '229'
                    ],
                    'match_alias': ['uplink'],
                    'match_desc': ['eth.*'],
                },
            ),
        },
    ),
    (
        {},
        {
            'discovery_single': (
                True,
                {
                    'item_appearance': 'index',
                    'pad_portnumbers': True,
                },
            ),
            'matching_conditions': (
                False,
                {
                    'portstates': ['1'],
                    'porttypes': [
                        '6', '32', '62', '117', '127', '128', '129', '180', '181', '182', '205',
                        '229'
                    ],
                },
            ),
        },
    ),
])
def test_transform_discovery_if_rules(params, result):
    assert _transform_discovery_if_rules(params) == result


@pytest.mark.parametrize('params, result', [
    (
        {
            'speed': 100000000,
            'traffic': [('both', ('upper', ('perc', (5.0, 20.0))))],
            'state': ['1'],
            'nucasts': (1, 2),
            'discards': (1, 2),
        },
        {
            'speed': 100000000,
            'traffic': [('both', ('upper', ('perc', (5.0, 20.0))))],
            'state': ['1'],
            'nucasts': (1, 2),
            'discards': (1, 2),
        },
    ),
    (
        {
            'errors': (0.01, 0.1),
        },
        {
            'errors_in': (0.01, 0.1),
            'errors_out': (0.01, 0.1),
        },
    ),
    (
        {
            'state': ['1', '2', '9'],
        },
        {
            'state': ['1', '2'],
        },
    ),
    (
        {
            'state': ['9'],
        },
        {
            'admin_state': ['2'],
        },
    ),
    (
        {
            'map_operstates': [(['1', '3', '9'], 1)],
        },
        {
            'map_operstates': [(['1', '3'], 1)],
            'map_admin_states': [(['2'], 1)],
        },
    ),
    (
        {
            'map_operstates': [(['9'], 1), (['5', '6'], 2)],
        },
        {
            'map_operstates': [(['5', '6'], 2)],
            'map_admin_states': [(['2'], 1)],
        },
    ),
    (
        {
            'map_operstates': [(['9'], 1)],
        },
        {
            'map_admin_states': [(['2'], 1)],
        },
    ),
])
def test_transform_check_if_rules(params, result):
    assert _transform_if_check_parameters(params) == result