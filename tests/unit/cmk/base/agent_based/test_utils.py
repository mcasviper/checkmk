#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# pylint: disable=protected-access

from typing import Callable, Iterable

import pytest  # type: ignore[import]

from cmk.utils.type_defs import HostKey, ParsedSectionName, SectionName, SourceType

from cmk.core_helpers.type_defs import AgentRawDataSection

import cmk.base.api.agent_based.register.section_plugins as section_plugins
from cmk.base.sources.agent import AgentHostSections
from cmk.base.agent_based.data_provider import (
    ParsedSectionsBroker,
    ParsedSectionsResolver,
    SectionsParser,
)
from cmk.base.agent_based.utils import get_section_kwargs, get_section_cluster_kwargs


def _test_section(
    *,
    section_name: str,
    parsed_section_name: str,
    parse_function: Callable,
    supersedes: Iterable[str],
) -> section_plugins.AgentSectionPlugin:
    return section_plugins.trivial_section_factory(SectionName(section_name))._replace(
        parsed_section_name=ParsedSectionName(parsed_section_name),
        parse_function=parse_function,
        supersedes={SectionName(n) for n in supersedes},
    )


SECTION_ONE = _test_section(
    section_name="one",
    parsed_section_name="parsed",
    parse_function=lambda x: {
        "parsed_by": "one",
        "node": x[0][0]
    },
    supersedes=(),
)

SECTION_TWO = _test_section(
    section_name="two",
    parsed_section_name="parsed",
    parse_function=lambda x: {
        "parsed_by": "two",
        "node": x[0][0]
    },
    supersedes={"one"},
)

SECTION_THREE = _test_section(
    section_name="three",
    parsed_section_name="parsed2",
    parse_function=lambda x: {
        "parsed_by": "three",
        "node": x[0][0]
    },
    supersedes=(),
)

SECTION_FOUR = _test_section(
    section_name="four",
    parsed_section_name="parsed_four",
    parse_function=lambda x: {
        "parsed_by": "four",
        "node": x[0][0]
    },
    supersedes={"one"},
)

NODE_1: AgentRawDataSection = [
    ["node1", "data 1"],
    ["node1", "data 2"],
]

NODE_2: AgentRawDataSection = [
    ["node2", "data 1"],
    ["node2", "data 2"],
]


@pytest.mark.parametrize("required_sections,expected_result", [
    (["nonexistent"], {}),
    (["parsed"], {
        "section": {
            "parsed_by": "two",
            "node": "node1"
        }
    }),
    (["parsed", "nonexistent"], {
        "section_parsed": {
            "parsed_by": "two",
            "node": "node1"
        },
        "section_nonexistent": None
    }),
    (["parsed", "parsed2"], {
        "section_parsed": {
            "parsed_by": "two",
            "node": "node1"
        },
        "section_parsed2": {
            "parsed_by": "three",
            "node": "node1"
        }
    }),
])
def test_get_section_kwargs(required_sections, expected_result):

    node_sections = AgentHostSections(sections={
        SectionName("one"): NODE_1,
        SectionName("two"): NODE_1,
        SectionName("three"): NODE_1
    })

    host_key = HostKey("node1", "127.0.0.1", SourceType.HOST)

    parsed_sections_broker = ParsedSectionsBroker({
        host_key: (
            ParsedSectionsResolver(
                section_plugins=[SECTION_ONE, SECTION_TWO, SECTION_THREE, SECTION_FOUR]),
            SectionsParser(host_sections=node_sections),
        ),
    })

    kwargs = get_section_kwargs(
        parsed_sections_broker,
        host_key,
        [ParsedSectionName(n) for n in required_sections],
    )

    assert expected_result == kwargs


@pytest.mark.parametrize("required_sections,expected_result", [
    (["nonexistent"], {}),
    (["parsed"], {
        "section": {
            "node1": {
                "parsed_by": "two",
                "node": "node1"
            },
            "node2": {
                "parsed_by": "two",
                "node": "node2"
            },
        }
    }),
    (["parsed", "nonexistent"], {
        "section_parsed": {
            "node1": {
                "parsed_by": "two",
                "node": "node1"
            },
            "node2": {
                "parsed_by": "two",
                "node": "node2"
            },
        },
        "section_nonexistent": {
            "node1": None,
            "node2": None
        }
    }),
    (["parsed", "parsed2"], {
        "section_parsed": {
            "node1": {
                "parsed_by": "two",
                "node": "node1"
            },
            "node2": {
                "parsed_by": "two",
                "node": "node2"
            },
        },
        "section_parsed2": {
            "node1": {
                "parsed_by": "three",
                "node": "node1"
            },
            "node2": {
                "parsed_by": "three",
                "node": "node2"
            },
        }
    }),
])
def test_get_section_cluster_kwargs(required_sections, expected_result):

    node1_sections = AgentHostSections(sections={
        SectionName("one"): NODE_1,
        SectionName("two"): NODE_1,
        SectionName("three"): NODE_1
    })

    node2_sections = AgentHostSections(sections={
        SectionName("two"): NODE_2,
        SectionName("three"): NODE_2,
    })

    parsed_sections_broker = ParsedSectionsBroker({
        HostKey("node1", "127.0.0.1", SourceType.HOST): (
            ParsedSectionsResolver(
                section_plugins=[SECTION_ONE, SECTION_TWO, SECTION_THREE, SECTION_FOUR],),
            SectionsParser(host_sections=node1_sections),
        ),
        HostKey("node2", "127.0.0.1", SourceType.HOST): (
            ParsedSectionsResolver(
                section_plugins=[SECTION_ONE, SECTION_TWO, SECTION_THREE, SECTION_FOUR],),
            SectionsParser(host_sections=node2_sections),
        ),
    })

    kwargs = get_section_cluster_kwargs(
        parsed_sections_broker,
        [
            HostKey("node1", "127.0.0.1", SourceType.HOST),
            HostKey("node2", "127.0.0.1", SourceType.HOST),
        ],
        [ParsedSectionName(n) for n in required_sections],
    )

    assert expected_result == kwargs
