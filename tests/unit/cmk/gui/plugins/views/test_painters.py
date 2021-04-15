#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from testlib import on_time

import cmk.utils.version as cmk_version
from cmk.gui.globals import html
from cmk.gui.utils.html import HTML

from cmk.utils.structured_data import StructuredDataTree
from cmk.gui import sites
from cmk.gui.views import View, painters_of_datasource
from cmk.gui.type_defs import PainterSpec
from cmk.gui.plugins.views.utils import painter_registry


@pytest.fixture(name="live")
def fixture_livestatus_test_config(mock_livestatus):
    live = mock_livestatus
    live.set_sites(['NO_SITE'])
    live.add_table('hosts', [{
        'name': 'abc',
        'alias': 'abc',
        'address': 'server.example.com',
        'custom_variables': {
            "FILENAME": "/wato/hosts.mk",
            "ADDRESS_FAMILY": "4",
            "ADDRESS_4": "127.0.0.1",
            "ADDRESS_6": "",
            "TAGS": "/wato/ auto-piggyback cmk-agent ip-v4 ip-v4-only lan no-snmp prod site:abc tcp",
        },
        'contacts': [],
        'contact_groups': ['all'],
        'filename': "/wato/hosts.mk",
    }])

    # Initiate status query here to make it not trigger in the tests
    with live(expect_status_query=True):
        sites.live()

    return live


@pytest.mark.usefixtures("load_plugins", "load_config")
def test_registered_painters():
    painters = painter_registry.keys()
    expected_painters = [
        'aggr_acknowledged',
        'aggr_assumed_state',
        'aggr_group',
        'aggr_hosts',
        'aggr_hosts_services',
        'aggr_icons',
        'aggr_in_downtime',
        'aggr_name',
        'aggr_output',
        'aggr_real_state',
        'aggr_state',
        'aggr_state_num',
        'aggr_treestate',
        'aggr_treestate_boxed',
        'alert_stats_crit',
        'alert_stats_ok',
        'alert_stats_problem',
        'alert_stats_unknown',
        'alert_stats_warn',
        'alias',
        'check_manpage',
        'comment_author',
        'comment_comment',
        'comment_entry_type',
        'comment_expires',
        'comment_id',
        'comment_time',
        'comment_what',
        'crash_exception',
        'crash_ident',
        'crash_time',
        'crash_type',
        'crash_version',
        'downtime_author',
        'downtime_comment',
        'downtime_duration',
        'downtime_end_time',
        'downtime_entry_time',
        'downtime_fixed',
        'downtime_id',
        'downtime_origin',
        'downtime_recurring',
        'downtime_start_time',
        'downtime_type',
        'downtime_what',
        'event_application',
        'event_comment',
        'event_contact',
        'event_contact_groups',
        'event_count',
        'event_effective_contact_groups',
        'event_facility',
        'event_first',
        'event_history_icons',
        'event_host',
        'event_host_in_downtime',
        'event_icons',
        'event_id',
        'event_ipaddress',
        'event_last',
        'event_match_groups',
        'event_owner',
        'event_phase',
        'event_pid',
        'event_priority',
        'event_rule_id',
        'event_sl',
        'event_state',
        'event_text',
        'hg_alias',
        'hg_name',
        'hg_num_hosts_down',
        'hg_num_hosts_pending',
        'hg_num_hosts_unreach',
        'hg_num_hosts_up',
        'hg_num_services',
        'hg_num_services_crit',
        'hg_num_services_ok',
        'hg_num_services_pending',
        'hg_num_services_unknown',
        'hg_num_services_warn',
        'history_addinfo',
        'history_line',
        'history_time',
        'history_what',
        'history_what_explained',
        'history_who',
        'host',
        'host_acknowledged',
        'host_address',
        'host_address_families',
        'host_address_family',
        'host_addresses',
        'host_addresses_additional',
        'host_attempt',
        'host_black',
        'host_check_age',
        'host_check_command',
        'host_check_command_expanded',
        'host_check_duration',
        'host_check_interval',
        'host_check_latency',
        'host_check_type',
        'host_childs',
        'host_comments',
        'host_contact_groups',
        'host_contacts',
        'host_custom_notes',
        'host_custom_variable',
        'host_custom_vars',
        'host_docker_node',
        'host_filename',
        'host_flapping',
        'host_graphs',
        'host_group_memberlist',
        'host_icons',
        'host_in_downtime',
        'host_in_notifper',
        'host_ipv4_address',
        'host_ipv6_address',
        'host_is_active',
        'host_is_stale',
        'host_labels',
        'host_last_notification',
        'host_next_check',
        'host_next_notification',
        'host_normal_interval',
        'host_notification_number',
        'host_notification_postponement_reason',
        'host_notifications_enabled',
        'host_notifper',
        'host_parents',
        'host_perf_data',
        'host_plugin_output',
        'host_pnpgraph',
        'host_retry_interval',
        'host_servicelevel',
        'host_services',
        'host_specific_metric',
        'host_staleness',
        'host_state',
        'host_state_age',
        'host_state_onechar',
        'host_tag_address_family',
        'host_tag_agent',
        'host_tag_piggyback',
        'host_tag_snmp_ds',
        'host_tags',
        'host_tags_with_titles',
        'host_with_state',
        'hostgroup_hosts',
        'inv',
        'inv_hardware',
        'inv_hardware_chassis',
        'inv_hardware_components',
        'inv_hardware_components_backplanes',
        'inv_hardware_components_chassis',
        'inv_hardware_components_containers',
        'inv_hardware_components_fans',
        'inv_hardware_components_modules',
        'inv_hardware_components_others',
        'inv_hardware_components_psus',
        'inv_hardware_components_sensors',
        'inv_hardware_components_stacks',
        'inv_hardware_components_unknowns',
        'inv_hardware_cpu',
        'inv_hardware_cpu_arch',
        'inv_hardware_cpu_bus_speed',
        'inv_hardware_cpu_cache_size',
        'inv_hardware_cpu_cores',
        'inv_hardware_cpu_cores_per_cpu',
        'inv_hardware_cpu_cpu_max_capa',
        'inv_hardware_cpu_cpus',
        'inv_hardware_cpu_entitlement',
        'inv_hardware_cpu_implementation_mode',
        'inv_hardware_cpu_logical_cpus',
        'inv_hardware_cpu_max_speed',
        'inv_hardware_cpu_model',
        'inv_hardware_cpu_sharing_mode',
        'inv_hardware_cpu_smt_threads',
        'inv_hardware_cpu_threads',
        'inv_hardware_cpu_threads_per_cpu',
        'inv_hardware_cpu_voltage',
        'inv_hardware_memory',
        'inv_hardware_memory_arrays',
        'inv_hardware_memory_total_ram_usable',
        'inv_hardware_memory_total_swap',
        'inv_hardware_memory_total_vmalloc',
        'inv_hardware_nwadapter',
        'inv_hardware_storage',
        'inv_hardware_storage_controller',
        'inv_hardware_storage_controller_version',
        'inv_hardware_storage_disks',
        'inv_hardware_system',
        'inv_hardware_system_expresscode',
        'inv_hardware_system_manufacturer',
        'inv_hardware_system_model',
        'inv_hardware_system_model_name',
        'inv_hardware_system_product',
        'inv_hardware_system_serial',
        'inv_hardware_system_serial_number',
        'inv_hardware_video',
        'inv_networking',
        'inv_networking_addresses',
        'inv_networking_available_ethernet_ports',
        'inv_networking_interfaces',
        'inv_networking_routes',
        'inv_networking_total_ethernet_ports',
        'inv_networking_total_interfaces',
        'inv_networking_tunnels',
        'inv_networking_wlan',
        'inv_networking_wlan_controller',
        'inv_networking_wlan_controller_accesspoints',
        'inv_software',
        'inv_software_applications',
        'inv_software_applications_check_mk',
        'inv_software_applications_check_mk_agent_version',
        'inv_software_applications_check_mk_cluster_is_cluster',
        'inv_software_applications_check_mk_cluster_nodes',
        'inv_software_applications_check_mk_host_labels',
        'inv_software_applications_check_mk_num_hosts',
        'inv_software_applications_check_mk_num_services',
        'inv_software_applications_check_mk_sites',
        'inv_software_applications_check_mk_versions',
        'inv_software_applications_citrix',
        'inv_software_applications_citrix_controller',
        'inv_software_applications_citrix_controller_controller_version',
        'inv_software_applications_citrix_vm',
        'inv_software_applications_citrix_vm_agent_version',
        'inv_software_applications_citrix_vm_catalog',
        'inv_software_applications_citrix_vm_desktop_group_name',
        'inv_software_applications_docker',
        'inv_software_applications_docker_container',
        'inv_software_applications_docker_container_networks',
        'inv_software_applications_docker_container_node_name',
        'inv_software_applications_docker_container_ports',
        'inv_software_applications_docker_containers',
        'inv_software_applications_docker_images',
        'inv_software_applications_docker_node_labels',
        'inv_software_applications_docker_num_containers_paused',
        'inv_software_applications_docker_num_containers_running',
        'inv_software_applications_docker_num_containers_stopped',
        'inv_software_applications_docker_num_containers_total',
        'inv_software_applications_docker_num_images',
        'inv_software_applications_docker_registry',
        'inv_software_applications_docker_swarm_manager',
        'inv_software_applications_docker_swarm_node_id',
        'inv_software_applications_docker_swarm_state',
        'inv_software_applications_docker_version',
        'inv_software_applications_fortinet_fortigate_high_availability',
        'inv_software_applications_fortinet_fortisandbox',
        'inv_software_applications_ibm_mq',
        'inv_software_applications_ibm_mq_channels',
        'inv_software_applications_ibm_mq_managers',
        'inv_software_applications_ibm_mq_queues',
        'inv_software_applications_kubernetes_assigned_pods',
        'inv_software_applications_kubernetes_ingresses',
        'inv_software_applications_kubernetes_job_container',
        'inv_software_applications_kubernetes_nodes',
        'inv_software_applications_kubernetes_pod_container',
        'inv_software_applications_kubernetes_pod_info',
        'inv_software_applications_kubernetes_pod_info_dns_policy',
        'inv_software_applications_kubernetes_pod_info_host_ip',
        'inv_software_applications_kubernetes_pod_info_host_network',
        'inv_software_applications_kubernetes_pod_info_node',
        'inv_software_applications_kubernetes_pod_info_pod_ip',
        'inv_software_applications_kubernetes_pod_info_qos_class',
        'inv_software_applications_kubernetes_roles',
        'inv_software_applications_kubernetes_selector',
        'inv_software_applications_kubernetes_service_info',
        'inv_software_applications_kubernetes_service_info_cluster_ip',
        'inv_software_applications_kubernetes_service_info_load_balancer_ip',
        'inv_software_applications_kubernetes_service_info_type',
        'inv_software_applications_mssql',
        'inv_software_applications_mssql_instances',
        'inv_software_applications_oracle',
        'inv_software_applications_oracle_dataguard_stats',
        'inv_software_applications_oracle_instance',
        'inv_software_applications_oracle_pga',
        'inv_software_applications_oracle_recovery_area',
        'inv_software_applications_oracle_sga',
        'inv_software_applications_oracle_systemparameter',
        'inv_software_applications_oracle_tablespaces',
        'inv_software_bios',
        'inv_software_bios_date',
        'inv_software_bios_vendor',
        'inv_software_bios_version',
        'inv_software_configuration',
        'inv_software_configuration_snmp_info',
        'inv_software_configuration_snmp_info_contact',
        'inv_software_configuration_snmp_info_location',
        'inv_software_configuration_snmp_info_name',
        'inv_software_firmware',
        'inv_software_firmware_platform_level',
        'inv_software_firmware_vendor',
        'inv_software_firmware_version',
        'inv_software_kernel_config',
        'inv_software_os',
        'inv_software_os_arch',
        'inv_software_os_install_date',
        'inv_software_os_kernel_version',
        'inv_software_os_name',
        'inv_software_os_service_pack',
        'inv_software_os_service_packs',
        'inv_software_os_type',
        'inv_software_os_vendor',
        'inv_software_os_version',
        'inv_software_packages',
        'invbackplane_description',
        'invbackplane_index',
        'invbackplane_location',
        'invbackplane_manufacturer',
        'invbackplane_model',
        'invbackplane_name',
        'invbackplane_serial',
        'invbackplane_software',
        'invchassis_description',
        'invchassis_index',
        'invchassis_location',
        'invchassis_manufacturer',
        'invchassis_model',
        'invchassis_name',
        'invchassis_serial',
        'invchassis_software',
        'invcmksites_apache',
        'invcmksites_autostart',
        'invcmksites_check_helper_usage',
        'invcmksites_check_mk_helper_usage',
        'invcmksites_checker_helper_usage',
        'invcmksites_cmc',
        'invcmksites_crontab',
        'invcmksites_dcd',
        'invcmksites_fetcher_helper_usage',
        'invcmksites_liveproxyd',
        'invcmksites_livestatus_usage',
        'invcmksites_mkeventd',
        'invcmksites_mknotifyd',
        'invcmksites_nagios',
        'invcmksites_npcd',
        'invcmksites_num_hosts',
        'invcmksites_num_services',
        'invcmksites_rrdcached',
        'invcmksites_site',
        'invcmksites_stunnel',
        'invcmksites_used_version',
        'invcmksites_xinetd',
        'invcmkversions_demo',
        'invcmkversions_edition',
        'invcmkversions_num_sites',
        'invcmkversions_number',
        'invcmkversions_version',
        'invcontainer_description',
        'invcontainer_index',
        'invcontainer_location',
        'invcontainer_manufacturer',
        'invcontainer_model',
        'invcontainer_name',
        'invcontainer_serial',
        'invcontainer_software',
        'invdockercontainers_creation',
        'invdockercontainers_id',
        'invdockercontainers_image',
        'invdockercontainers_labels',
        'invdockercontainers_name',
        'invdockercontainers_status',
        'invdockerimages_amount_containers',
        'invdockerimages_creation',
        'invdockerimages_id',
        'invdockerimages_labels',
        'invdockerimages_repodigests',
        'invdockerimages_repotags',
        'invdockerimages_size',
        'inventory_tree',
        'invfan_description',
        'invfan_index',
        'invfan_location',
        'invfan_manufacturer',
        'invfan_model',
        'invfan_name',
        'invfan_serial',
        'invfan_software',
        'invhist_changed',
        'invhist_delta',
        'invhist_new',
        'invhist_removed',
        'invhist_time',
        'invibmmqchannels_monchl',
        'invibmmqchannels_name',
        'invibmmqchannels_qmgr',
        'invibmmqchannels_status',
        'invibmmqchannels_type',
        'invibmmqmanagers_ha',
        'invibmmqmanagers_instname',
        'invibmmqmanagers_instver',
        'invibmmqmanagers_name',
        'invibmmqmanagers_standby',
        'invibmmqmanagers_status',
        'invibmmqqueues_altered',
        'invibmmqqueues_created',
        'invibmmqqueues_maxdepth',
        'invibmmqqueues_maxmsgl',
        'invibmmqqueues_monq',
        'invibmmqqueues_name',
        'invibmmqqueues_qmgr',
        'invinterface_admin_status',
        'invinterface_alias',
        'invinterface_available',
        'invinterface_description',
        'invinterface_index',
        'invinterface_last_change',
        'invinterface_oper_status',
        'invinterface_phys_address',
        'invinterface_port_type',
        'invinterface_speed',
        'invinterface_vlans',
        'invinterface_vlantype',
        'invkernelconfig_parameter',
        'invkernelconfig_value',
        'invmodule_bootloader',
        'invmodule_description',
        'invmodule_firmware',
        'invmodule_index',
        'invmodule_location',
        'invmodule_manufacturer',
        'invmodule_model',
        'invmodule_name',
        'invmodule_serial',
        'invmodule_software',
        'invmodule_type',
        'invoradataguardstats_db_unique',
        'invoradataguardstats_role',
        'invoradataguardstats_sid',
        'invoradataguardstats_switchover',
        'invorainstance_db_creation_time',
        'invorainstance_db_uptime',
        'invorainstance_logins',
        'invorainstance_logmode',
        'invorainstance_openmode',
        'invorainstance_pname',
        'invorainstance_sid',
        'invorainstance_version',
        'invorapga_aggregate_pga_auto_target',
        'invorapga_aggregate_pga_target_parameter',
        'invorapga_bytes_processed',
        'invorapga_extra_bytes_read_written',
        'invorapga_global_memory_bound',
        'invorapga_maximum_pga_allocated',
        'invorapga_maximum_pga_used_for_auto_workareas',
        'invorapga_maximum_pga_used_for_manual_workareas',
        'invorapga_sid',
        'invorapga_total_freeable_pga_memory',
        'invorapga_total_pga_allocated',
        'invorapga_total_pga_inuse',
        'invorapga_total_pga_used_for_auto_workareas',
        'invorapga_total_pga_used_for_manual_workareas',
        'invorarecoveryarea_flashback',
        'invorarecoveryarea_sid',
        'invorasga_buf_cache_size',
        'invorasga_data_trans_cache_size',
        'invorasga_fixed_size',
        'invorasga_free_mem_avail',
        'invorasga_granule_size',
        'invorasga_in_mem_area_size',
        'invorasga_java_pool_size',
        'invorasga_large_pool_size',
        'invorasga_max_size',
        'invorasga_redo_buffer',
        'invorasga_shared_io_pool_size',
        'invorasga_shared_pool_size',
        'invorasga_sid',
        'invorasga_start_oh_shared_pool',
        'invorasga_streams_pool_size',
        'invorasystemparameter_isdefault',
        'invorasystemparameter_name',
        'invorasystemparameter_sid',
        'invorasystemparameter_value',
        'invoratablespace_autoextensible',
        'invoratablespace_current_size',
        'invoratablespace_free_space',
        'invoratablespace_increment_size',
        'invoratablespace_max_size',
        'invoratablespace_name',
        'invoratablespace_num_increments',
        'invoratablespace_sid',
        'invoratablespace_type',
        'invoratablespace_used_size',
        'invoratablespace_version',
        'invother_description',
        'invother_index',
        'invother_location',
        'invother_manufacturer',
        'invother_model',
        'invother_name',
        'invother_serial',
        'invother_software',
        'invpsu_description',
        'invpsu_index',
        'invpsu_location',
        'invpsu_manufacturer',
        'invpsu_model',
        'invpsu_name',
        'invpsu_serial',
        'invpsu_software',
        'invsensor_description',
        'invsensor_index',
        'invsensor_location',
        'invsensor_manufacturer',
        'invsensor_model',
        'invsensor_name',
        'invsensor_serial',
        'invsensor_software',
        'invstack_description',
        'invstack_index',
        'invstack_location',
        'invstack_manufacturer',
        'invstack_model',
        'invstack_name',
        'invstack_serial',
        'invstack_software',
        'invswpac_arch',
        'invswpac_install_date',
        'invswpac_name',
        'invswpac_package_type',
        'invswpac_package_version',
        'invswpac_path',
        'invswpac_size',
        'invswpac_summary',
        'invswpac_vendor',
        'invswpac_version',
        'invtunnels_index',
        'invtunnels_link_priority',
        'invtunnels_peerip',
        'invtunnels_peername',
        'invtunnels_sourceip',
        'invtunnels_tunnel_interface',
        'invunknown_description',
        'invunknown_index',
        'invunknown_location',
        'invunknown_manufacturer',
        'invunknown_model',
        'invunknown_name',
        'invunknown_serial',
        'invunknown_software',
        'log_attempt',
        'log_command',
        'log_comment',
        'log_contact_name',
        'log_date',
        'log_icon',
        'log_lineno',
        'log_message',
        'log_options',
        'log_plugin_output',
        'log_state',
        'log_state_info',
        'log_state_type',
        'log_time',
        'log_type',
        'log_what',
        'num_problems',
        'num_services',
        'num_services_crit',
        'num_services_ok',
        'num_services_pending',
        'num_services_unknown',
        'num_services_warn',
        'perfometer',
        'service_custom_variable',
        'service_description',
        'service_discovery_check',
        'service_discovery_service',
        'service_discovery_state',
        'service_display_name',
        'service_graphs',
        'service_icons',
        'service_labels',
        'service_specific_metric',
        'service_state',
        'service_tags',
        'service_tags_with_titles',
        'sg_alias',
        'sg_name',
        'sg_num_services',
        'sg_num_services_crit',
        'sg_num_services_ok',
        'sg_num_services_pending',
        'sg_num_services_unknown',
        'sg_num_services_warn',
        'sg_services',
        'site_icon',
        'sitealias',
        'sitename_plain',
        'svc_acknowledged',
        'svc_attempt',
        'svc_check_age',
        'svc_check_cache_info',
        'svc_check_command',
        'svc_check_command_expanded',
        'svc_check_duration',
        'svc_check_interval',
        'svc_check_latency',
        'svc_check_period',
        'svc_check_type',
        'svc_comments',
        'svc_contact_groups',
        'svc_contacts',
        'svc_custom_notes',
        'svc_custom_vars',
        'svc_flapping',
        'svc_group_memberlist',
        'svc_in_downtime',
        'svc_in_notifper',
        'svc_is_active',
        'svc_is_stale',
        'svc_last_notification',
        'svc_last_time_ok',
        'svc_long_plugin_output',
        'svc_metrics',
        'svc_next_check',
        'svc_next_notification',
        'svc_normal_interval',
        'svc_notification_number',
        'svc_notification_postponement_reason',
        'svc_notifications_enabled',
        'svc_notifper',
        'svc_perf_data',
        'svc_perf_val01',
        'svc_perf_val02',
        'svc_perf_val03',
        'svc_perf_val04',
        'svc_perf_val05',
        'svc_perf_val06',
        'svc_perf_val07',
        'svc_perf_val08',
        'svc_perf_val09',
        'svc_perf_val10',
        'svc_plugin_output',
        'svc_pnpgraph',
        'svc_retry_interval',
        'svc_servicelevel',
        'svc_staleness',
        'svc_state_age',
        'wato_folder_abs',
        'wato_folder_plain',
        'wato_folder_rel',
    ]

    if not cmk_version.is_raw_edition():
        expected_painters += [
            'svc_metrics_forecast',
            'svc_metrics_hist',
            'sla_fixed',
            'sla_specific',
            'ntop_host_details',
            'ntop_ports',
            'ntop_protocol_breakdown',
            'ntop_top_peers',
            'deployment_downloaded_hash',
            'deployment_icons',
            'deployment_installed_hash',
            'deployment_last_contact',
            'deployment_last_download',
            'deployment_last_error',
            'deployment_target_hash',
        ]

    if cmk_version.is_managed_edition():
        expected_painters += [
            'host_customer',
            'customer_id',
            'customer_name',
            'customer_num_hosts',
            'customer_num_hosts_down',
            'customer_num_hosts_pending',
            'customer_num_hosts_unreach',
            'customer_num_hosts_up',
            'customer_num_services',
            'customer_num_services_crit',
            'customer_num_services_ok',
            'customer_num_services_pending',
            'customer_num_services_unknown',
            'customer_num_services_warn',
        ]

    assert sorted(painters) == sorted(expected_painters)


# We only get all painters after the plugins and config have been loaded. Since there currently no
# way to create test parameters while depending on a fixture we can not use pytests parametrization
@pytest.mark.usefixtures("load_plugins", "load_config")
@pytest.fixture(name="service_painter_idents")
def fixture_service_painter_names():
    return sorted(list(painters_of_datasource("services").keys()))


def test_service_painters(register_builtin_html, service_painter_idents, live):
    with live(expect_status_query=False), html.stashed_vars(), on_time('2018-04-15 16:50', 'CET'):
        html.request.del_vars()

        for painter_ident in service_painter_idents:
            _test_painter(painter_ident, live)


def _test_painter(painter_ident, live):
    _set_expected_queries(painter_ident, live)

    view = View(
        view_name="",
        view_spec={
            "group_painters": [],
            "painters": [PainterSpec(_painter_name_spec(painter_ident), None, None, None)],
            "sorters": [],
            "datasource": "services",
        },
        context={},
    )

    row = _service_row()
    for cell in view.row_cells:
        _tdclass, content = cell.render(row)
        assert isinstance(content, (str, HTML))

        if isinstance(content, str) and "<" in content:
            raise ValueError(f"Painter: {painter_ident} Found HTML tag in "
                             f"str content (will be escaped!): {content}")


# TODO: Better move to livestatus mock?
def _service_row():
    return {
        'host_accept_passive_checks': 0,
        'host_acknowledged': 0,
        'host_action_url_expanded': '',
        'host_active_checks_enabled': 1,
        'host_address': '127.0.0.1',
        'host_alias': 'abc',
        'host_check_command': 'check-mk-host-smart',
        'host_check_command_expanded': 'check-mk-host-smart!',
        'host_check_interval': 0.1,
        'host_check_type': 0,
        'host_childs': [],
        'host_comments_with_extra_info': [],
        'host_comments_with_info': [],
        'host_contact_groups': ['all'],
        'host_contacts': [],
        'host_current_attempt': 1,
        'host_current_notification_number': 0,
        'host_custom_variable_names': [
            'FILENAME', 'ADDRESS_FAMILY', 'ADDRESS_4', 'ADDRESS_6', 'TAGS'
        ],
        'host_custom_variable_values': [
            '/wato/hosts.mk', '4', '127.0.0.1', '', '/wato/ auto-piggyback cmk-agent ip-v4 '
            'ip-v4-only lan no-snmp prod site:stable tcp'
        ],
        'host_custom_variables': {
            'ADDRESS_4': '127.0.0.1',
            'ADDRESS_6': '',
            'ADDRESS_FAMILY': '4',
            'FILENAME': '/wato/hosts.mk',
            'TAGS': '/wato/ auto-piggyback cmk-agent ip-v4 '
                    'ip-v4-only lan no-snmp prod site:stable '
                    'tcp'
        },
        'host_downtimes_with_extra_info': [],
        'host_execution_time': 1.8e-07,
        'host_filename': '/wato/hosts.mk',
        'host_groups': ['check_mk'],
        'host_has_been_checked': 1,
        'host_icon_image': '',
        'host_in_check_period': 1,
        'host_in_notification_period': 1,
        'host_in_service_period': 1,
        'host_inventory': StructuredDataTree().create_tree_from_raw_tree({
            'hardware': {
                'memory': {
                    'total_ram_usable': 33283784704,
                    'total_swap': 1023406080,
                    'total_vmalloc': 35184372087808
                }
            },
            'networking': {
                'addresses': [{
                    'address': '127.0.0.1',
                    'device': 'lo',
                    'type': 'ipv4'
                }, {
                    'address': '::1',
                    'device': 'lo',
                    'type': 'ipv6'
                }, {
                    'address': '10.1.1.100',
                    'device': 'wlp59s0',
                    'type': 'ipv4'
                }, {
                    'address': 'fe80::522e:4d07:26aa:5ac5',
                    'device': 'wlp59s0',
                    'type': 'ipv6'
                }, {
                    'address': '172.17.0.1',
                    'device': 'docker0',
                    'type': 'ipv4'
                }, {
                    'address': 'fe80::42:9aff:fef7:8238',
                    'device': 'docker0',
                    'type': 'ipv6'
                }, {
                    'address': 'fe80::d465:a5ff:fe86:4139',
                    'device': 'vethb457925',
                    'type': 'ipv6'
                }, {
                    'address': 'fe80::60c9:43ff:fe93:4be',
                    'device': 'veth0be86fc',
                    'type': 'ipv6'
                }],
                'available_ethernet_ports': 1,
                'hostname': 'klappspaten',
                'interfaces': [{
                    'alias': 'lo',
                    'available': None,
                    'description': 'lo',
                    'index': 1,
                    'oper_status': 1,
                    'phys_address': '00:00:00:00:00:00',
                    'port_type': 24,
                    'speed': 0
                }, {
                    'alias': 'docker0',
                    'available': False,
                    'description': 'docker0',
                    'index': 2,
                    'oper_status': 1,
                    'phys_address': '02:42:9A:F7:82:38',
                    'port_type': 6,
                    'speed': 0
                }, {
                    'alias': 'vboxnet0',
                    'available': True,
                    'description': 'vboxnet0',
                    'index': 3,
                    'oper_status': 2,
                    'phys_address': '0A:00:27:00:00:00',
                    'port_type': 6,
                    'speed': 10000000
                }, {
                    'alias': 'wlp59s0',
                    'available': False,
                    'description': 'wlp59s0',
                    'index': 6,
                    'oper_status': 1,
                    'phys_address': '3C:58:C2:FF:34:8F',
                    'port_type': 6,
                    'speed': 0
                }],
                'total_ethernet_ports': 3,
                'total_interfaces': 6
            },
            'software': {
                'applications': {
                    'check_mk': {
                        'agent_version': '2.0.0b5',
                        'cluster': {
                            'is_cluster': False
                        },
                        'num_sites': 11,
                        'num_versions': 22,
                        'sites': [{
                            'apache': 'stopped',
                            'autostart': False,
                            'check_helper_usage': 1.48e-321,
                            'check_mk_helper_usage': 0.0,
                            'checker_helper_usage': 2.25692e-30,
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'fetcher_helper_usage': 0.0207974,
                            'liveproxyd': 'stopped',
                            'livestatus_usage': 1.48e-321,
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'num_hosts': '3',
                            'num_services': '79',
                            'rrdcached': 'stopped',
                            'site': 'heute',
                            'stunnel': 'not '
                                       'existent',
                            'used_version': '2021.03.18.cee',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'apache': 'stopped',
                            'autostart': False,
                            'check_helper_usage': 1.48e-321,
                            'check_mk_helper_usage': 0.014576800000000001,
                            'checker_helper_usage': 0.0,
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'fetcher_helper_usage': 0.0,
                            'liveproxyd': 'stopped',
                            'livestatus_usage': 4.94e-322,
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'num_hosts': '1',
                            'num_services': '74',
                            'rrdcached': 'stopped',
                            'site': 'old',
                            'stunnel': 'not '
                                       'existent',
                            'used_version': '1.6.0-2021.03.19.cee',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'apache': 'running',
                            'autostart': False,
                            'check_helper_usage': 1.1957599999999999e-11,
                            'check_mk_helper_usage': 0.0,
                            'checker_helper_usage': 2.55739e-36,
                            'cmc': 'running',
                            'crontab': 'running',
                            'dcd': 'running',
                            'fetcher_helper_usage': 0.529738,
                            'liveproxyd': 'running',
                            'livestatus_usage': 9.345909999999999e-06,
                            'mkeventd': 'running',
                            'mknotifyd': 'running',
                            'num_hosts': '1',
                            'num_services': '69',
                            'rrdcached': 'running',
                            'site': 'abc',
                            'stunnel': 'not '
                                       'existent',
                            'used_version': '2.0.0-2021.03.31.cee',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'apache': 'stopped',
                            'autostart': False,
                            'check_helper_usage': 0.0,
                            'check_mk_helper_usage': 0.0,
                            'checker_helper_usage': 1.3319e-41,
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'fetcher_helper_usage': 0.0208051,
                            'liveproxyd': 'stopped',
                            'livestatus_usage': 25.0,
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'num_hosts': '1',
                            'num_services': '53',
                            'rrdcached': 'stopped',
                            'site': 'stable_slave_1',
                            'stunnel': 'stopped',
                            'used_version': '2.0.0-2021.03.31.cee',
                            'xinetd': 'stopped'
                        }, {
                            'apache': 'running',
                            'cmc': 'running',
                            'crontab': 'running',
                            'dcd': 'running',
                            'liveproxyd': 'running',
                            'mkeventd': 'running',
                            'mknotifyd': 'running',
                            'rrdcached': 'running',
                            'site': 'beta',
                            'stunnel': 'not '
                                       'existent',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'apache': 'running',
                            'cmc': 'running',
                            'crontab': 'running',
                            'dcd': 'running',
                            'liveproxyd': 'running',
                            'mkeventd': 'running',
                            'mknotifyd': 'running',
                            'rrdcached': 'running',
                            'site': 'beta_slave_1',
                            'stunnel': 'not '
                                       'existent',
                            'xinetd': 'running'
                        }, {
                            'apache': 'stopped',
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'liveproxyd': 'stopped',
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'rrdcached': 'stopped',
                            'site': 'beta_slave_2',
                            'stunnel': 'stopped',
                            'xinetd': 'stopped'
                        }, {
                            'apache': 'running',
                            'cmc': 'running',
                            'crontab': 'running',
                            'dcd': 'running',
                            'liveproxyd': 'running',
                            'mkeventd': 'running',
                            'mknotifyd': 'running',
                            'rrdcached': 'running',
                            'site': 'crawl_central',
                            'stunnel': 'not '
                                       'existent',
                            'xinetd': 'running'
                        }, {
                            'apache': 'stopped',
                            'autostart': False,
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'liveproxyd': 'stopped',
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'rrdcached': 'stopped',
                            'site': 'heute_slave_1',
                            'stunnel': 'stopped',
                            'used_version': '2021.03.12.cee',
                            'xinetd': 'stopped'
                        }, {
                            'apache': 'running',
                            'cmc': 'running',
                            'crontab': 'running',
                            'dcd': 'running',
                            'liveproxyd': 'running',
                            'mkeventd': 'running',
                            'mknotifyd': 'running',
                            'rrdcached': 'running',
                            'site': 'lmtest',
                            'stunnel': 'not '
                                       'existent',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'apache': 'stopped',
                            'cmc': 'stopped',
                            'crontab': 'stopped',
                            'dcd': 'stopped',
                            'liveproxyd': 'stopped',
                            'mkeventd': 'stopped',
                            'mknotifyd': 'stopped',
                            'rrdcached': 'stopped',
                            'site': 'stable2',
                            'stunnel': 'not '
                                       'existent',
                            'xinetd': 'not '
                                      'existent'
                        }, {
                            'autostart': False,
                            'site': 'cmk',
                            'used_version': ''
                        }],
                        'versions': [{
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '1.6.0-2021.01.11',
                            'version': '1.6.0-2021.01.11.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '1.6.0-2021.03.03',
                            'version': '1.6.0-2021.03.03.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '1.6.0-2021.03.11',
                            'version': '1.6.0-2021.03.11.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 1,
                            'number': '1.6.0-2021.03.19',
                            'version': '1.6.0-2021.03.19.cee'
                        }, {
                            'demo': False,
                            'edition': 'cme',
                            'num_sites': 0,
                            'number': '1.6.0p19',
                            'version': '1.6.0p19.cme'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.02.03',
                            'version': '2.0.0-2021.02.03.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.02',
                            'version': '2.0.0-2021.03.02.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.08',
                            'version': '2.0.0-2021.03.08.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.09',
                            'version': '2.0.0-2021.03.09.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.10',
                            'version': '2.0.0-2021.03.10.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.11',
                            'version': '2.0.0-2021.03.11.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.17',
                            'version': '2.0.0-2021.03.17.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.18',
                            'version': '2.0.0-2021.03.18.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0-2021.03.29',
                            'version': '2.0.0-2021.03.29.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 2,
                            'number': '2.0.0-2021.03.31',
                            'version': '2.0.0-2021.03.31.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2.0.0',
                            'version': '2.0.0.cee'
                        }, {
                            'demo': False,
                            'edition': 'cre',
                            'num_sites': 0,
                            'number': '2.0.0',
                            'version': '2.0.0.cre'
                        }, {
                            'demo': False,
                            'edition': 'cme',
                            'num_sites': 0,
                            'number': '2.0.0i1',
                            'version': '2.0.0i1.cme'
                        }, {
                            'demo': False,
                            'edition': 'cme',
                            'num_sites': 0,
                            'number': '2.0.0p1',
                            'version': '2.0.0p1.cme'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 0,
                            'number': '2021.03.05',
                            'version': '2021.03.05.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 1,
                            'number': '2021.03.12',
                            'version': '2021.03.12.cee'
                        }, {
                            'demo': False,
                            'edition': 'cee',
                            'num_sites': 1,
                            'number': '2021.03.18',
                            'version': '2021.03.18.cee'
                        }]
                    }
                }
            }
        }),
        'host_is_flapping': 0,
        'host_label_sources': {
            'cmk/check_mk_server': 'discovered',
            'cmk/os_family': 'discovered'
        },
        'host_labels': {
            'cmk/check_mk_server': 'yes',
            'cmk/os_family': 'linux'
        },
        'host_last_check': 1617468248,
        'host_last_notification': 0,
        'host_last_state_change': 1617452715,
        'host_latency': 0,
        'host_max_check_attempts': 1,
        'host_metrics': [],
        'host_modified_attributes_list': [],
        'host_name': 'abc',
        'host_next_check': 1617468259,
        'host_next_notification': 1617452715,
        'host_notes_url_expanded': '',
        'host_notification_period': '24X7',
        'host_notification_postponement_reason': '',
        'host_notifications_enabled': 1,
        'host_num_services': 69,
        'host_num_services_crit': 5,
        'host_num_services_ok': 62,
        'host_num_services_pending': 0,
        'host_num_services_unknown': 1,
        'host_num_services_warn': 1,
        'host_parents': [],
        'host_perf_data': '',
        'host_plugin_output': 'Packet received via smart PING',
        'host_pnpgraph_present': 0,
        'host_retry_interval': 0.1,
        'host_scheduled_downtime_depth': 0,
        'host_services_with_state': [['Uptime', 0, 1], ['Systemd Timesyncd Time', 0, 1],
                                     ['TCP Connections', 0, 1], ['Systemd Service Summary', 0, 1],
                                     ['OMD stable2 status', 2, 1],
                                     ['OMD crawl_central status', 0, 1], ['Interface 7', 3, 1],
                                     ['Interface 2', 0, 1], ['OMD beta_slave_1 status', 0, 1],
                                     ['Temperature Zone 13', 0, 1], ['Temperature Zone 8', 0, 1],
                                     ['OMD heute_slave_1 apache', 0, 1],
                                     ['OMD stable_slave_1 performance', 0, 1],
                                     ['OMD old performance', 0, 1], ['Kernel Performance', 0, 1],
                                     ['Filesystem /opt/omd/sites/stable/tmp', 0, 1],
                                     ['OMD stable_slave_1 apache', 0, 1],
                                     ['Temperature Zone 2', 0, 1], ['Temperature Zone 9', 0, 1],
                                     ['Filesystem /opt/omd/sites/heute/tmp', 0, 1],
                                     ['Mount options of /', 0, 1], ['Nullmailer Queue', 2, 1],
                                     ['Filesystem /',
                                      0, 1], ['Site stable_slave_1 statistics', 0, 1],
                                     ['Memory', 0, 1], ['Mount options of /boot/efi', 0, 1],
                                     ['Interface 3', 2, 1], ['Number of threads', 1, 1],
                                     ['Temperature Zone 10', 0, 1], ['Temperature Zone 5', 0, 1],
                                     ['Check_MK HW/SW Inventory', 0,
                                      1], ['OMD stable apache', 0, 1], ['CPU load', 0, 1],
                                     ['Temperature Zone 11', 0, 1], ['Check_MK Discovery', 0, 1],
                                     ['Temperature Zone 6', 0, 1], ['Temperature Zone 0', 0, 1],
                                     ['Disk IO SUMMARY', 0, 1], ['Filesystem /boot', 0, 1],
                                     ['OMD stable performance', 2, 1], ['Temperature Zone 3', 0, 1],
                                     ['Filesystem /boot/efi', 0, 1], ['Temperature Zone 1', 0, 1],
                                     ['Temperature Zone 4', 0, 1], ['Site heute statistics', 0, 1],
                                     ['Temperature Zone 12', 0, 1], ['Temperature Zone 7', 0, 1],
                                     ['OMD heute apache', 0, 1],
                                     ['Filesystem /opt/omd/sites/stable_slave_1/tmp', 0, 1],
                                     ['mysärvice', 0, 1], ['OMD heute Notification Spooler', 0, 1],
                                     ['CPU utilization', 0, 1], ['OMD heute Event Console', 0, 1],
                                     ['OMD old Event Console', 0, 1], ['OMD lmtest status', 0, 1],
                                     ['OMD stable Event Console', 0, 1],
                                     ['Filesystem /opt/omd/sites/old/tmp', 0, 1],
                                     ['OMD stable_slave_1 Event Console', 0, 1],
                                     ['OMD old Notification Spooler', 0, 1],
                                     ['OMD stable Notification Spooler', 0, 1],
                                     ['OMD heute performance', 0, 1],
                                     ['OMD stable_slave_1 Notification Spooler', 0, 1],
                                     ['Mount options of /boot', 0, 1], ['Check_MK', 0, 1],
                                     ['Site old statistics', 0, 1], ['OMD old apache', 0, 1],
                                     ['Site stable statistics', 0, 1], ['OMD beta status', 0, 1],
                                     ['OMD beta_slave_2 status', 2, 1]],
        'host_services_with_state_filtered': [['Uptime', 0, 1], ['Systemd Timesyncd Time', 0, 1],
                                              ['TCP Connections', 0, 1],
                                              ['Systemd Service Summary', 0, 1],
                                              ['OMD stable2 status', 2, 1],
                                              ['OMD crawl_central status', 0, 1],
                                              ['Interface 7', 3, 1], ['Interface 2', 0, 1],
                                              ['OMD beta_slave_1 status', 0, 1],
                                              ['Temperature Zone 13', 0, 1],
                                              ['Temperature Zone 8', 0, 1],
                                              ['OMD heute_slave_1 apache', 0, 1],
                                              ['OMD stable_slave_1 performance', 0, 1],
                                              ['OMD old performance', 0, 1],
                                              ['Kernel Performance', 0, 1],
                                              ['Filesystem /opt/omd/sites/stable/tmp', 0, 1],
                                              ['OMD stable_slave_1 apache', 0, 1],
                                              ['Temperature Zone 2', 0, 1],
                                              ['Temperature Zone 9', 0, 1],
                                              ['Filesystem /opt/omd/sites/heute/tmp', 0, 1],
                                              ['Mount options of /', 0, 1],
                                              ['Nullmailer Queue', 2, 1], ['Filesystem /', 0, 1],
                                              ['Site stable_slave_1 statistics', 0, 1],
                                              ['Memory', 0, 1],
                                              ['Mount options of /boot/efi', 0, 1],
                                              ['Interface 3', 2, 1], ['Number of threads', 1, 1],
                                              ['Temperature Zone 10', 0, 1],
                                              ['Temperature Zone 5', 0, 1],
                                              ['Check_MK HW/SW Inventory', 0, 1],
                                              ['OMD stable apache', 0, 1], ['CPU load', 0, 1],
                                              ['Temperature Zone 11', 0, 1],
                                              ['Check_MK Discovery', 0, 1],
                                              ['Temperature Zone 6', 0, 1],
                                              ['Temperature Zone 0', 0,
                                               1], ['Disk IO SUMMARY', 0, 1],
                                              ['Filesystem /boot', 0, 1],
                                              ['OMD stable performance', 2, 1],
                                              ['Temperature Zone 3', 0, 1],
                                              ['Filesystem /boot/efi', 0, 1],
                                              ['Temperature Zone 1', 0, 1],
                                              ['Temperature Zone 4', 0, 1],
                                              ['Site heute statistics', 0, 1],
                                              ['Temperature Zone 12', 0, 1],
                                              ['Temperature Zone 7', 0, 1],
                                              ['OMD heute apache', 0, 1],
                                              [
                                                  'Filesystem '
                                                  '/opt/omd/sites/stable_slave_1/tmp', 0, 1
                                              ], ['mysärvice', 0, 1],
                                              ['OMD heute Notification Spooler', 0, 1],
                                              ['CPU utilization', 0, 1],
                                              ['OMD heute Event Console', 0, 1],
                                              ['OMD old Event Console', 0, 1],
                                              ['OMD lmtest status', 0, 1],
                                              ['OMD stable Event Console', 0, 1],
                                              ['Filesystem /opt/omd/sites/old/tmp', 0, 1],
                                              ['OMD stable_slave_1 Event Console', 0, 1],
                                              ['OMD old Notification Spooler', 0, 1],
                                              ['OMD stable Notification Spooler', 0, 1],
                                              ['OMD heute performance', 0, 1],
                                              ['OMD stable_slave_1 Notification '
                                               'Spooler', 0, 1], ['Mount options of /boot', 0, 1],
                                              ['Check_MK', 0, 1], ['Site old statistics', 0, 1],
                                              ['OMD old apache', 0, 1],
                                              ['Site stable statistics', 0, 1],
                                              ['OMD beta status', 0, 1],
                                              ['OMD beta_slave_2 status', 2, 1]],
        'host_staleness': 0.666667,
        'host_state': 0,
        'host_structured_status': b"{'software': {'applications': {'check_mk': {'sit"
                                  b"es': [{'site': 'heute', 'num_hosts': '3', 'num_s"
                                  b"ervices': '79', 'check_helper_usage': 1.48e-321,"
                                  b" 'check_mk_helper_usage': 0.0, 'fetcher_helper_u"
                                  b"sage': 0.0207974, 'checker_helper_usage': 2.2569"
                                  b"2e-30, 'livestatus_usage': 1.48e-321, 'cmc': 'st"
                                  b"opped', 'dcd': 'stopped', 'liveproxyd': 'stopped"
                                  b"', 'mknotifyd': 'stopped', 'apache': 'stopped', "
                                  b"'crontab': 'stopped', 'mkeventd': 'stopped', 'rr"
                                  b"dcached': 'stopped', 'stunnel': 'not existent', "
                                  b"'xinetd': 'not existent'}, {'site': 'old', 'num_"
                                  b"hosts': '1', 'num_services': '74', 'check_helper"
                                  b"_usage': 1.48e-321, 'check_mk_helper_usage': 0.0"
                                  b"14576800000000001, 'fetcher_helper_usage': 0.0, "
                                  b"'checker_helper_usage': 0.0, 'livestatus_usage':"
                                  b" 4.94e-322, 'cmc': 'stopped', 'dcd': 'stopped', "
                                  b"'liveproxyd': 'stopped', 'mknotifyd': 'stopped',"
                                  b" 'apache': 'stopped', 'crontab': 'stopped', 'mke"
                                  b"ventd': 'stopped', 'rrdcached': 'stopped', 'stun"
                                  b"nel': 'not existent', 'xinetd': 'not existent'},"
                                  b" {'site': 'abc', 'num_hosts': '1', 'num_servi"
                                  b"ces': '69', 'check_helper_usage': 1.195759999999"
                                  b"9999e-11, 'check_mk_helper_usage': 0.0, 'fetcher"
                                  b"_helper_usage': 0.529738, 'checker_helper_usage'"
                                  b": 2.55739e-36, 'livestatus_usage': 9.34590999999"
                                  b"9999e-06, 'cmc': 'running', 'dcd': 'running', 'l"
                                  b"iveproxyd': 'running', 'mknotifyd': 'running', '"
                                  b"apache': 'running', 'crontab': 'running', 'mkeve"
                                  b"ntd': 'running', 'rrdcached': 'running', 'stunne"
                                  b"l': 'not existent', 'xinetd': 'not existent'}, {"
                                  b"'site': 'stable_slave_1', 'num_hosts': '1', 'num"
                                  b"_services': '53', 'check_helper_usage': 0.0, 'ch"
                                  b"eck_mk_helper_usage': 0.0, 'fetcher_helper_usage"
                                  b"': 0.0208051, 'checker_helper_usage': 1.3319e-41"
                                  b", 'livestatus_usage': 25.0, 'cmc': 'stopped', 'd"
                                  b"cd': 'stopped', 'liveproxyd': 'stopped', 'mknoti"
                                  b"fyd': 'stopped', 'apache': 'stopped', 'crontab':"
                                  b" 'stopped', 'mkeventd': 'stopped', 'rrdcached': "
                                  b"'stopped', 'stunnel': 'stopped', 'xinetd': 'stop"
                                  b"ped'}, {'site': 'beta', 'cmc': 'running', 'dcd':"
                                  b" 'running', 'liveproxyd': 'running', 'mknotifyd'"
                                  b": 'running', 'apache': 'running', 'crontab': 'ru"
                                  b"nning', 'mkeventd': 'running', 'rrdcached': 'run"
                                  b"ning', 'stunnel': 'not existent', 'xinetd': 'not"
                                  b" existent'}, {'site': 'beta_slave_1', 'cmc': 'ru"
                                  b"nning', 'dcd': 'running', 'liveproxyd': 'running"
                                  b"', 'mknotifyd': 'running', 'apache': 'running', "
                                  b"'crontab': 'running', 'mkeventd': 'running', 'rr"
                                  b"dcached': 'running', 'stunnel': 'not existent', "
                                  b"'xinetd': 'running'}, {'site': 'beta_slave_2', '"
                                  b"cmc': 'stopped', 'dcd': 'stopped', 'liveproxyd':"
                                  b" 'stopped', 'mknotifyd': 'stopped', 'apache': 's"
                                  b"topped', 'crontab': 'stopped', 'mkeventd': 'stop"
                                  b"ped', 'rrdcached': 'stopped', 'stunnel': 'stoppe"
                                  b"d', 'xinetd': 'stopped'}, {'site': 'crawl_centra"
                                  b"l', 'cmc': 'running', 'dcd': 'running', 'livepro"
                                  b"xyd': 'running', 'mknotifyd': 'running', 'apache"
                                  b"': 'running', 'crontab': 'running', 'mkeventd': "
                                  b"'running', 'rrdcached': 'running', 'stunnel': 'n"
                                  b"ot existent', 'xinetd': 'running'}, {'site': 'he"
                                  b"ute_slave_1', 'cmc': 'stopped', 'dcd': 'stopped'"
                                  b", 'liveproxyd': 'stopped', 'mknotifyd': 'stopped"
                                  b"', 'apache': 'stopped', 'crontab': 'stopped', 'm"
                                  b"keventd': 'stopped', 'rrdcached': 'stopped', 'st"
                                  b"unnel': 'stopped', 'xinetd': 'stopped'}, {'site'"
                                  b": 'lmtest', 'cmc': 'running', 'dcd': 'running', "
                                  b"'liveproxyd': 'running', 'mknotifyd': 'running',"
                                  b" 'apache': 'running', 'crontab': 'running', 'mke"
                                  b"ventd': 'running', 'rrdcached': 'running', 'stun"
                                  b"nel': 'not existent', 'xinetd': 'not existent'},"
                                  b" {'site': 'stable2', 'cmc': 'stopped', 'dcd': 's"
                                  b"topped', 'liveproxyd': 'stopped', 'mknotifyd': '"
                                  b"stopped', 'apache': 'stopped', 'crontab': 'stopp"
                                  b"ed', 'mkeventd': 'stopped', 'rrdcached': 'stoppe"
                                  b"d', 'stunnel': 'not existent', 'xinetd': 'not ex"
                                  b"istent'}]}}}}\n",
        'host_tags': {
            'address_family': 'ip-v4-only',
            'agent': 'cmk-agent',
            'criticality': 'prod',
            'ip-v4': 'ip-v4',
            'networking': 'lan',
            'piggyback': 'auto-piggyback',
            'site': 'abc',
            'snmp_ds': 'no-snmp',
            'tcp': 'tcp'
        },
        'rrddata:sys:sys.average:1614553200:1617228000:60': [0, 0, 0],
        'rrddata:sys:sys.average:1616367600:1616968800:60': [0, 0, 0],
        'rrddata:system:system.average:1614553200:1617228000:60': [0, 0, 0],
        'rrddata:system:system.average:1616367600:1616968800:60': [0, 0, 0],
        'service_accept_passive_checks': 1,
        'service_acknowledged': 0,
        'service_action_url_expanded': '',
        'service_active_checks_enabled': 0,
        'service_cache_interval': 0,
        'service_cached_at': 0,
        'service_check_command': 'check_mk-lnx_if',
        'service_check_command_expanded': '',
        'service_check_interval': 1,
        'service_check_period': '24X7',
        'service_check_type': 1,
        'service_comments_with_extra_info': [],
        'service_comments_with_info': [],
        'service_contact_groups': ['all'],
        'service_contacts': [],
        'service_current_attempt': 1,
        'service_current_notification_number': 0,
        'service_custom_variable_names': ["DING"],
        'service_custom_variable_values': ["DONG"],
        'service_custom_variables': {
            "DING": "DONG"
        },
        'service_description': 'Interface 3',
        'service_display_name': 'Interface 3',
        'service_downtimes': [],
        'service_downtimes_with_extra_info': [],
        'service_execution_time': 2.6e-08,
        'service_groups': [],
        'service_has_been_checked': 1,
        'service_host_name': 'abc',
        'service_icon_image': '',
        'service_in_check_period': 1,
        'service_in_notification_period': 1,
        'service_in_passive_check_period': 1,
        'service_in_service_period': 1,
        'service_is_flapping': 0,
        'service_label_sources': {},
        'service_labels': {},
        'service_last_check': 1617468196,
        'service_last_notification': 0,
        'service_last_state_change': 1617309051,
        'service_last_time_ok': 1617302582,
        'service_latency': 0,
        'service_long_plugin_output': '[vboxnet0]\\nOperational state: '
                                      'down(!!)\\nMAC: 0A:00:27:00:00:00\\nSpeed: 10 '
                                      'MBit/s (expected: 0 Bit/s)(!)',
        'service_max_check_attempts': 1,
        'service_metrics': [
            'outdisc', 'outnucast', 'outqlen', 'in', 'out', 'inmcast', 'inbcast', 'inerr', 'indisc',
            'inucast', 'innucast', 'outmcast', 'outbcast', 'outerr', 'outucast'
        ],
        'service_modified_attributes_list': [],
        'service_next_check': 0,
        'service_next_notification': 1617309051,
        'service_notes_url_expanded': '',
        'service_notification_period': '24X7',
        'service_notification_postponement_reason': '',
        'service_notifications_enabled': 1,
        'service_perf_data': '',
        'service_plugin_output': '[vboxnet0], (down)(!!), MAC: 0A:00:27:00:00:00, '
                                 'Speed: 10 MBit/s (expected: 0 Bit/s)(!)',
        'service_pnpgraph_present': 1,
        'service_retry_interval': 1,
        'service_scheduled_downtime_depth': 0,
        'service_service_description': 'Interface 3',
        'service_staleness': 0.933333,
        'service_state': 2,
        'service_tags': {},
        'site': 'NO_SITE',
        'forecast_aggr_3c659189-29f3-411a-8456-6a07fdae4d51': None,
        'forecast_aggr_3c659189-29f3-411a-8456-6a07fdae4d51_max': None,
        'hist_aggr_e13957f5-1b0b-43a7-a452-3bff7187542e': None,
        'hist_aggr_e13957f5-1b0b-43a7-a452-3bff7187542e_max': None,
    }


def _painter_name_spec(painter_ident):
    if painter_ident == "service_custom_variable":
        return painter_ident, {"ident": "DING"}
    if painter_ident == "host_custom_variable":
        return painter_ident, {"ident": "FILENAME"}
    if painter_ident == "svc_metrics_hist":
        return painter_ident, {"uuid": "e13957f5-1b0b-43a7-a452-3bff7187542e"}
    if painter_ident == "svc_metrics_forecast":
        return painter_ident, {"uuid": "3c659189-29f3-411a-8456-6a07fdae4d51"}
    return painter_ident


def _set_expected_queries(painter_ident, live):
    if painter_ident == "inv":
        # TODO: Why is it querying twice?
        live.expect_query(
            "GET hosts\nColumns: host_name\nFilter: host_name = abc\nLocaltime: 1523811000\nOutputFormat: python3\nKeepAlive: on\nResponseHeader: fixed16"
        )
        live.expect_query(
            "GET hosts\nColumns: host_name\nFilter: host_name = abc\nLocaltime: 1523811000\nOutputFormat: python3\nKeepAlive: on\nResponseHeader: fixed16"
        )
        return