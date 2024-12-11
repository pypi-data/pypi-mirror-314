#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file name: args.py
author: Shlomi Ben-David <shlomi.ben.david@gmail.com>
description: This module used to manage all the command line arguments
"""
import argparse
import os
from linode_mgmt.__version__ import __version__

PROG = 'linode-mgmt'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION = __version__


def get_cli_args():
    """
    Get command line arguments

    :return: command line arguments object
    """
    optional_arguments_parser = argparse.ArgumentParser(add_help=False)
    optional_arguments_group = \
        optional_arguments_parser.add_argument_group(title='optional arguments')
    optional_arguments_group.add_argument(
        '--help', action='help', default=argparse.SUPPRESS,
        help="show this help message and exit"
    )
    optional_arguments_group.add_argument(
        '--version', action='version',
        version=f"%(prog)s v{VERSION}",
        help="shows program version"
    )
    optional_arguments_group.add_argument(
        '--log-file', metavar='NAME', dest='log_file',
        help="log file name"
    )
    optional_arguments_group.add_argument(
        '--verbose', action='store_true',
        help="if added will print more information"
    )
    optional_arguments_group.add_argument(
        'console', action='store_true', default=True,
        help=argparse.SUPPRESS
    )
    optional_arguments_group.add_argument(
        '--dry-run', action='store_true', dest='noop',
        help="used to test action without performing anything"
    )

    # required
    required_arguments_parser = argparse.ArgumentParser(add_help=False)
    required_arguments_group = \
        required_arguments_parser.add_argument_group(title='required arguments')
    required_arguments_group.add_argument(
        '--token', metavar='<TEXT>',
        help="a personal access token"
    )

    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Linode Management component",
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s <resource> <action> [arguments]",
        add_help=False,
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    resources_sub_parser = parser.add_subparsers(
        metavar='', title='resources', prog=PROG,
    )

    # ---- CLUSTER ----
    cluster_parser = resources_sub_parser.add_parser(
        'cluster', help="", add_help=False,
        usage="%(prog)s <actions> [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    cluster_group = cluster_parser.add_argument_group(title='resource arguments')
    cluster_group.add_argument(
        'resource', const='cluster', default='cluster', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_sub_parser = cluster_parser.add_subparsers(
        metavar='', title='actions', prog=f"{PROG} cluster",
    )
    cluster_create_parser = cluster_sub_parser.add_parser(
        'create', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    cluster_create_group = cluster_create_parser.add_argument_group(title='action arguments')
    cluster_create_group.add_argument(
        'action', const='create', default='create', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_create_group.add_argument(
        '--cluster', metavar='<NAME>', required=True,
        help="a cluster name"
    )
    cluster_create_group.add_argument(
        # ref: https://cloud.linode.com/api/v4/regions
        '--region', metavar='<NAME>', default='us-central',
        help="a region name (default: us-east)"
    )
    cluster_create_group.add_argument(
        '--kernel', metavar='<NAME>', default='linode/grub2',
        help="a kernel name (default: linode/grub2)"
    )
    cluster_create_group.add_argument(
        '--kube-version', metavar='<VERSION>', default='1.28',
        help="a kubernetes version (default: 1.28)"
    )
    cluster_create_group.add_argument(
        '--node-count', metavar='<NUMBER>', default=3, type=int,
        help="number of nodes (default: 3)"
    )
    default_node_type = 'g7-dedicated-56'
    cluster_create_group.add_argument(
        # ref: https://api.linode.com/v4/linode/types
        '--node-type', metavar='<NAME>', default=default_node_type,
        help=f"node type (default: {default_node_type})"
    )
    cluster_create_group.add_argument(
        '--high-availability', action='store_true',
        help=f"a high availability control plane"
    )
    cluster_update_parser = cluster_sub_parser.add_parser(
        'update', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    cluster_update_group = cluster_update_parser.add_argument_group(title='action arguments')
    cluster_update_group.add_argument(
        'action', const='update', default='update', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_update_group.add_argument(
        '--cluster', metavar='<NAME>', required=True,
        help="a cluster name"
    )
    cluster_update_group.add_argument(
        '--node-count', metavar='<NUMBER>', type=int, required=True,
        help="number of nodes"
    )
    cluster_update_group.add_argument(
        '--pool-id', metavar='<NUMBER>', type=int,
        help="pull id number (if not specified, it will effect all pools)"
    )
    cluster_upgrade_parser = cluster_sub_parser.add_parser(
        'upgrade', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    cluster_upgrade_group = cluster_upgrade_parser.add_argument_group(title='action arguments')
    cluster_upgrade_group.add_argument(
        'action', const='upgrade', default='upgrade', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_upgrade_group.add_argument(
        '--cluster', metavar='<NAME>', required=True,
        help="a cluster name"
    )
    cluster_upgrade_group.add_argument(
        '--kube-version', metavar='<VERSION>', required=True,
        help="a kubernetes version (format: '1.26')"
    )
    cluster_upgrade_group.add_argument(
        '--high-availability', action='store_true',
        help=f"a high availability control plane"
    )
    cluster_upgrade_group.add_argument(
        '--threshold', metavar='<NUMBER>', type=int,
        help="a node threshold to upgrade (calculated as percentage, 90 == 90%)"
    )
    cluster_upgrade_group.add_argument(
        '--wait-time', metavar='<NUMBER>', type=int,
        help="how much time to wait between an upgrade nodes cycle"
    )
    cluster_get_id_parser = cluster_sub_parser.add_parser(
        'get-id', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    cluster_get_id_group = cluster_get_id_parser.add_argument_group(title='action arguments')
    cluster_get_id_group.add_argument(
        'action', const='get-id', default='get-id', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_get_id_group.add_argument(
        '--cluster', metavar='<NAME>', required=True,
        help="a cluster name"
    )
    cluster_delete_parser = cluster_sub_parser.add_parser(
        'delete', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    cluster_delete_group = cluster_delete_parser.add_argument_group(title='action arguments')
    cluster_delete_group.add_argument(
        'action', const='delete', default='delete', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    cluster_delete_group.add_argument(
        '--cluster', metavar='<NAME>', required=True,
        help="a cluster name"
    )

    # ---- NODE ----
    node_parser = resources_sub_parser.add_parser(
        'node', help="", add_help=False,
        usage="%(prog)s <actions> [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    node_group = node_parser.add_argument_group(title='resource arguments')
    node_group.add_argument(
        'resource', const='node', default='node', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_sub_parser = node_parser.add_subparsers(
        metavar='', title='actions', prog=f"{PROG} node",
    )
    node_get_id_parser = node_sub_parser.add_parser(
        'get-id', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    node_get_id_group = node_get_id_parser.add_argument_group(title='action arguments')
    node_get_id_group.add_argument(
        'action', const='get-id', default='get-id', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_get_id_group.add_argument(
        '--node-name', metavar='<NAME>', required=True,
        help="a node name"
    )
    node_poweroff_parser = node_sub_parser.add_parser(
        'poweroff', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    node_poweroff_group = node_poweroff_parser.add_argument_group(title='action arguments')
    node_poweroff_group.add_argument(
        'action', const='poweroff', default='poweroff', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_poweroff_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name (required only when using the --all flag)"
    )
    node_poweroff_group.add_argument(
        '--node-name', metavar='<NAME>',
        help="a node name (used only when updating a disk on a specific node)"
    )
    node_poweroff_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will poweroff all nodes"
    )
    node_poweron_parser = node_sub_parser.add_parser(
        'poweron', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    node_poweron_group = node_poweron_parser.add_argument_group(title='action arguments')
    node_poweron_group.add_argument(
        'action', const='poweron', default='poweron', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_poweron_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name (required only when using the --all flag)"
    )
    node_poweron_group.add_argument(
        '--node-name', metavar='<NAME>',
        help="a node name (used only when updating a disk on a specific node)"
    )
    node_poweron_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will poweron all nodes"
    )
    node_restart_parser = node_sub_parser.add_parser(
        'restart', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    node_restart_group = node_restart_parser.add_argument_group(title='action arguments')
    node_restart_group.add_argument(
        'action', const='restart', default='restart', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_restart_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name (required only when using the --all flag)"
    )
    node_restart_group.add_argument(
        '--node-name', metavar='<NAME>',
        help="a node name (used only when updating a disk on a specific node)"
    )
    node_restart_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will restart all nodes"
    )
    node_update_parser = node_sub_parser.add_parser(
        'update', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    node_update_group = node_update_parser.add_argument_group(title='action arguments')
    node_update_group.add_argument(
        'action', const='update', default='update', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    node_update_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name (required only when using the --all flag)"
    )
    node_update_group.add_argument(
        '--node-name', metavar='<NAME>',
        help="a node name (used only when updating a disk on a specific node)"
    )
    node_update_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will update all nodes"
    )
    node_update_group.add_argument(
        '--node-cpu-alert', metavar='<NUMBER>', default=0,
        help="a node cpu usage alert threshold (default: 0)"
    )
    node_update_group.add_argument(
        '--node-network-in-alert', metavar='<NUMBER>', default=0,
        help="a node incoming traffic alert threshold (default: 0)"
    )
    node_update_group.add_argument(
        '--node-network-out-alert', metavar='<NUMBER>', default=0,
        help="a node outgoing traffic alert threshold (default: 0)"
    )
    node_update_group.add_argument(
        '--node-transfer-quota-alert', metavar='<NUMBER>', default=0,
        help="a node outgoing traffic alert threshold (default: 0)"
    )
    node_update_group.add_argument(
        '--node-io-alert', metavar='<NUMBER>', default=0,
        help="a node io alert threshold (default: 0)"
    )

    # ---- VOLUME ----
    volume_parser = resources_sub_parser.add_parser(
        'volume', help="", add_help=False,
        usage="%(prog)s <actions> [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    volume_group = volume_parser.add_argument_group(title='resource arguments')
    volume_group.add_argument(
        'resource', const='volume', default='volume', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    volume_sub_parser = volume_parser.add_subparsers(
        metavar='', title='actions', prog=f"{PROG} volume",
    )
    volume_list_parser = volume_sub_parser.add_parser(
        'list', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    volume_list_group = volume_list_parser.add_argument_group(title='action arguments')
    volume_list_group.add_argument(
        'action', const='list', default='list', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )

    volume_delete_parser = volume_sub_parser.add_parser(
        'delete', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    volume_delete_group = volume_delete_parser.add_argument_group(title='action arguments')
    volume_delete_group.add_argument(
        'action', const='delete', default='delete', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    volume_delete_group.add_argument(
        '--volume-name', metavar='<NAME>',
        help="a volume name"
    )
    volume_delete_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will delete all volumes"
    )

    # ---- STORAGE ----
    storage_parser = resources_sub_parser.add_parser(
        'storage', help="", add_help=False,
        usage="%(prog)s <actions> [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    storage_group = storage_parser.add_argument_group(title='resource arguments')
    storage_group.add_argument(
        'resource', const='storage', default='storage', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    storage_sub_parser = storage_parser.add_subparsers(
        metavar='', title='actions', prog=f"{PROG} storage",
    )
    storage_list_parser = storage_sub_parser.add_parser(
        'list', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    storage_list_group = storage_list_parser.add_argument_group(title='action arguments')
    storage_list_group.add_argument(
        'action', const='list', default='list', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )

    storage_delete_parser = storage_sub_parser.add_parser(
        'delete', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    storage_delete_group = storage_delete_parser.add_argument_group(title='action arguments')
    storage_delete_group.add_argument(
        'action', const='delete', default='delete', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    storage_delete_group.add_argument(
        '--bucket-name', metavar='<NAME>', required=True,
        help="a bucket name"
    )
    storage_delete_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name"
    )
    storage_delete_group.add_argument(
        # ref: https://cloud.linode.com/api/v4/regions
        '--region', metavar='<NAME>',
        help="a region name"
    )

    storage_create_parser = storage_sub_parser.add_parser(
        'create', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    storage_create_group = storage_create_parser.add_argument_group(title='action arguments')
    storage_create_group.add_argument(
        'action', const='create', default='create', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    storage_create_group.add_argument(
        '--bucket-name', metavar='<NAME>', required=True,
        help="a bucket name"
    )
    storage_create_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name"
    )
    storage_create_group.add_argument(
        # ref: https://cloud.linode.com/api/v4/regions
        '--region', metavar='<NAME>',
        help="a region name"
    )

    # ---- FIREWALL ----
    firewall_parser = resources_sub_parser.add_parser(
        'firewall', help="", add_help=False,
        usage="%(prog)s <actions> [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser
        ]
    )
    firewall_group = firewall_parser.add_argument_group(title='resource arguments')
    firewall_group.add_argument(
        'resource', const='firewall', default='firewall', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    firewall_sub_parser = firewall_parser.add_subparsers(
        metavar='', title='actions', prog=f"{PROG} firewall",
    )
    firewall_get_id_parser = firewall_sub_parser.add_parser(
        'get-id', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    firewall_get_id_group = firewall_get_id_parser.add_argument_group(title='action arguments')
    firewall_get_id_group.add_argument(
        'action', const='get-id', default='get-id', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    firewall_get_id_group.add_argument(
        '--firewall', metavar='<NAME>', required=True,
        help="a firewall name"
    )
    firewall_list_parser = firewall_sub_parser.add_parser(
        'list', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    firewall_list_group = firewall_list_parser.add_argument_group(title='action arguments')
    firewall_list_group.add_argument(
        'action', const='list', default='list', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    firewall_add_node_parser = firewall_sub_parser.add_parser(
        'add-node', help="", add_help=False,
        usage="%(prog)s [arguments]",
        parents=[
            optional_arguments_parser,
            required_arguments_parser,
        ]
    )
    firewall_add_node_group = firewall_add_node_parser.add_argument_group(title='action arguments')
    firewall_add_node_group.add_argument(
        'action', const='add-node', default='add-node', nargs='?',
        help=argparse.SUPPRESS,  # This argument should be hidden
    )
    firewall_add_node_group.add_argument(
        '--cluster', metavar='<NAME>',
        help="a cluster name (required only when using the --all flag)"
    )
    firewall_add_node_group.add_argument(
        '--firewall', metavar='<NAME>', required=True,
        help="a firewall name"
    )
    firewall_add_node_group.add_argument(
        '--node-name', metavar='<NAME>',
        help="a node name"
    )
    firewall_add_node_group.add_argument(
        '--all', action='store_true', default=False,
        help="when added will add all cluster nodes to the firewall"
    )

    args = parser.parse_args()

    for _arg in ['token', 'action', 'resource']:
        if not getattr(args, _arg, None):
            _arg = _arg if _arg == 'action' else f"--{_arg}"
            raise Exception(f"\nERROR: {_arg} argument is required.")

    return args

