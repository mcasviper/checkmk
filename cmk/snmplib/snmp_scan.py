#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import functools
from typing import Iterable, NamedTuple, Set

import cmk.utils.tty as tty
from cmk.utils.exceptions import MKGeneralException, MKSNMPError
from cmk.utils.log import console
from cmk.utils.type_defs import SectionName

import cmk.snmplib.snmp_cache as snmp_cache
import cmk.snmplib.snmp_modes as snmp_modes
from cmk.snmplib.type_defs import ABCSNMPBackend, SNMPDetectSpec
from cmk.snmplib.utils import evaluate_snmp_detection

SNMPScanSection = NamedTuple("SNMPScanSection", [
    ("name", SectionName),
    ("specs", SNMPDetectSpec),
])


# gather auto_discovered check_plugin_names for this host
def gather_available_raw_section_names(
    sections: Iterable[SNMPScanSection],
    on_error: str,
    *,
    binary_host: bool,
    backend: ABCSNMPBackend,
) -> Set[SectionName]:
    try:
        return _snmp_scan(
            sections,
            on_error=on_error,
            binary_host=binary_host,
            backend=backend,
        )
    except Exception as e:
        if on_error == "raise":
            raise
        if on_error == "warn":
            console.error("SNMP scan failed: %s\n" % e)

    return set()


OID_SYS_DESCR = ".1.3.6.1.2.1.1.1.0"
OID_SYS_OBJ = ".1.3.6.1.2.1.1.2.0"


def _snmp_scan(
    sections: Iterable[SNMPScanSection],
    on_error: str = "ignore",
    *,
    binary_host: bool,
    backend: ABCSNMPBackend,
) -> Set[SectionName]:
    snmp_cache.initialize_single_oid_cache(backend.config)
    console.vverbose("  SNMP scan:\n")
    _snmp_scan_cache_description(
        binary_host=binary_host,
        backend=backend,
    )

    found_sections = _snmp_scan_find_sections(
        sections,
        on_error=on_error,
        backend=backend,
    )
    _output_snmp_check_plugins("SNMP scan found", found_sections)
    snmp_cache.write_single_oid_cache(backend.config)
    return found_sections


def _snmp_scan_cache_description(
    binary_host: bool,
    *,
    backend: ABCSNMPBackend,
) -> None:
    if not binary_host:
        for oid, name in [
            (OID_SYS_DESCR, "system description"),
            (OID_SYS_OBJ, "system object"),
        ]:
            value = snmp_modes.get_single_oid(
                oid,
                backend=backend,
            )
            if value is None:
                raise MKSNMPError(
                    "Cannot fetch %s OID %s. Please check your SNMP "
                    "configuration. Possible reason might be: Wrong credentials, "
                    "wrong SNMP version, Firewall rules, etc." % (name, oid),)
    else:
        # Fake OID values to prevent issues with a lot of scan functions
        console.vverbose(
            "       Skipping system description OID "
            '(Set %s and %s to "")\n',
            OID_SYS_DESCR,
            OID_SYS_OBJ,
        )
        snmp_cache.set_single_oid_cache(OID_SYS_DESCR, "")
        snmp_cache.set_single_oid_cache(OID_SYS_OBJ, "")


def _snmp_scan_find_sections(
    sections: Iterable[SNMPScanSection],
    *,
    on_error: str,
    backend: ABCSNMPBackend,
) -> Set[SectionName]:
    found_sections: Set[SectionName] = set()
    for name, specs in sections:
        oid_value_getter = functools.partial(
            snmp_modes.get_single_oid,
            section_name=name,
            backend=backend,
        )
        try:
            if evaluate_snmp_detection(
                    detect_spec=specs,
                    oid_value_getter=oid_value_getter,
            ):
                found_sections.add(name)
        except MKGeneralException:
            # some error messages which we explicitly want to show to the user
            # should be raised through this
            raise
        except Exception:
            if on_error == "warn":
                console.warning("   Exception in SNMP scan function of %s" % name)
            elif on_error == "raise":
                raise
    return found_sections


def _output_snmp_check_plugins(
    title: str,
    collection: Iterable[SectionName],
) -> None:
    if collection:
        collection_out = " ".join(str(n) for n in sorted(collection))
    else:
        collection_out = "-"
    console.vverbose("   %-35s%s%s%s%s\n" % (
        title,
        tty.bold,
        tty.yellow,
        collection_out,
        tty.normal,
    ))
