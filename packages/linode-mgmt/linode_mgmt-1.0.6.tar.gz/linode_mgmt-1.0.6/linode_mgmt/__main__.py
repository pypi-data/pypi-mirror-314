#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
name: linode_mgmt.py
author: Shlomi Ben-David <shlomi.ben.david@gmail.com>
"""
import math

import linode_api4.errors
from linode_api4 import LinodeClient, LKECluster
import sys
import logging
from linode_mgmt.args import get_cli_args, VERSION
from pylib3 import init_logging
import inspect
from time import sleep

logger = logging.getLogger(__name__)
logging.getLogger('kubernetes.client.rest').setLevel('WARNING')


# ---- FLAGS ----
cluster_creation = False
disk_modifications = True
config_modifications = True


class LinodeMGMT(object):
    """Linode Management Class"""
    def __init__(self, token):
        """
        Initialization function

        :param str token: a personal API token
        """
        self.client = LinodeClient(token)

    def get_cluster(self, cluster):
        """
        Get a cluster per a specific label

        :param str cluster: a cluster name
        :returns: cluster object or None
        """
        logger.info(f"Getting '{cluster}' cluster details")
        clusters = self.client.lke.clusters()
        for _cluster in clusters or []:
            if cluster == _cluster.label:
                return _cluster

        logger.warning(f"Cluster '{cluster}' does not exist.")
        return

    def get_nodes(self, cluster=None, pool_id=None):
        """
        Get cluster nodes

        :param int pool_id: pool id number
        :param str cluster: a cluster name (which configured as a label)
        :returns list of nodes or an empty list
        """
        logger.info("Getting nodes")
        nodes = []
        if cluster:
            cluster = self.get_cluster(cluster=cluster)
            logger.debug(f"number of pools: {cluster.pools.total_items}")
            for pool in cluster.pools:
                logger.debug(f"pool_id: {pool.id}")
                if pool_id and pool_id == pool.id:
                    return [i.instance for i in pool.nodes]

                if isinstance(pool.nodes, list):
                    nodes += [i.instance for i in pool.nodes]
        else:
            nodes = self.client.linode.instances()
            nodes = list(nodes) if nodes else []

        logger.debug(f"number of nodes: {len(nodes)}")
        logger.debug(f"nodes: {nodes}")
        return nodes

    def get_node_id(self, node_name):
        """
        Gets node id

        :param str node_name: a node name
        returns: (int) node's id number or None
        """
        logger.info(f"Getting '{node_name}' node id")
        nodes = self.client.linode.instances()
        for node in nodes:
            if node.label != node_name:
                continue

            logger.debug(f"node_id: {node.id}")
            return node.id

    def get_node(self, node_name):
        """
        Get the node instance object from the passed node name

        :param str node_name: a node name (label)
        :returns (obj) node instance or None
        """
        logger.info(f"Getting {node_name} node instance object")
        nodes = self.client.linode.instances()
        if not nodes:
            logger.debug("Could not find any nodes!!!")
            return

        for node in nodes:
            _node_name = node.label
            if _node_name != node_name:
                continue

            logger.debug(f"node_name: {_node_name}")
            return node

    def create_cluster(
            self, cluster, node_count=None, node_type=None,
            kube_version=None, kernel=None, region=None,
            high_availability=None, node_pool_limit=100):
        """
        Creates or Updates a cluster

        :param str cluster: a cluster name (which configured as a label)
        :param int node_count: number of nodes
        :param str node_type: node type
        :param str kube_version: a kubernetes version
        :param str kernel: a kernel name
        :param str region: a region name
        :param bool high_availability: a high availability control plane
        :param int node_pool_limit: a limit of number of nodes in a pool (must be between 1-100)
        """
        logger.info(f"Creating '{cluster}' cluster")
        _cluster = self.get_cluster(cluster=cluster)
        if _cluster:
            logger.warning(f"Cluster '{cluster}' already exist, nothing to do!!!")
            return

        full_node_pools = 1
        partial_nodes = 0
        node_pools = []
        multiple_node_pools = False
        if node_count > node_pool_limit:
            multiple_node_pools = True
            full_node_pools = round(node_count / node_pool_limit)
            partial_nodes = node_count - (full_node_pools * node_pool_limit)

        logger.debug(f"node_count: {node_count}")
        logger.debug(f"full_node_pools: {full_node_pools}")
        logger.debug(f"partial_nodes: {partial_nodes}")

        if multiple_node_pools:
            while full_node_pools > 0:
                node_pools.append(self.client.lke.node_pool(node_type, node_pool_limit))
                full_node_pools -= 1

            if partial_nodes:
                node_pools.append(self.client.lke.node_pool(node_type, partial_nodes))
        else:
            node_pools.append(self.client.lke.node_pool(node_type, node_count))

        self.client.lke.cluster_create(
            region=region,
            label=cluster,
            node_pools=node_pools,
            kube_version=kube_version,
            kernel=kernel,
            control_plane={"high_availability": high_availability}
        )
        logger.info(f"Cluster '{cluster}' creation bootstrapped successfully")

    def delete_cluster(self, cluster):
        """
        Deletes a cluster

        :param str cluster: a cluster name (which configured as a label)
        """
        logger.info(f"Deleting '{cluster}' cluster")
        _cluster = self.get_cluster(cluster=cluster)
        if not cluster or not isinstance(_cluster, LKECluster):
            logger.warning(f"Cluster '{cluster}' does not exist, nothing to do!!!")
            return

        api_endpoint = f"/lke/clusters/{_cluster.id}"
        logger.debug(f"api_endpoint: {api_endpoint}")

        response = self.client.delete(api_endpoint)
        if response:
            logger.debug(f"response: {response}")
        logger.info(f"Cluster '{cluster}' deleted successfully")

    def update_cluster(self, cluster, node_count, pool_id=None):
        """
        Updates existing cluster by increasing/decreasing the node number

        :param str cluster: a cluster name (which configured as a label)
        :param int node_count: number of nodes
        :param int pool_id: pool id number
        """
        logger.info(f"Updating '{cluster}' cluster nodes")
        _cluster = self.get_cluster(cluster=cluster)
        if not _cluster or not isinstance(_cluster, LKECluster):
            logger.warning(f"Cluster '{cluster}' does not exist, aborting...")
            return

        pools = getattr(_cluster, 'pools', [])
        cluster_pools = []
        for pool in pools:
            logger.debug(f"cluster pool_id: {pool.id}")
            cluster_pools.append(pool.id)
            if pool_id and pool_id != pool.id:
                logger.debug(f"requested pool_id: {pool_id}")
                continue

            api_endpoint = f"/lke/clusters/{_cluster.id}/pools/{pool.id}"
            logger.debug(f"api_endpoint: {api_endpoint}")
            data = {"count": node_count}
            logger.debug(f"data: {data}")
            self.client.put(api_endpoint, data=data)
            logger.info(f"Cluster '{cluster}' nodes in {pool.id} pool updated successfully")

        if pool_id and pool_id not in cluster_pools:
            logger.warning(f"No such pool id ({pool_id})")

    def upgrade_cluster(
            self, cluster, kube_version, high_availability, threshold=None, wait_time=None
    ):
        """
        Upgrade existing cluster in recycle mode.
        This recycles each worker node on a rolling basis so that only one node is down at any particular moment.
        In the highest level of detail, each worker node is independently drained and cordoned one at a time.

        :param str cluster: a cluster name (which configured as a label)
        :param str kube_version: a kubernetes version
        :param bool high_availability: a high availability control plane
        :param int threshold: a node threshold to upgrade (calculated as percentage)
        :param int wait_time: how much time to wait between an upgrade nodes cycle
        """
        logger.info(f"Upgrading '{cluster}' cluster")
        _cluster = self.get_cluster(cluster=cluster)
        if not _cluster or not isinstance(_cluster, LKECluster):
            logger.warning(f"Cluster '{cluster}' does not exist, aborting...")
            return

        logger.info("Step 1/2 - upgrading the control plane")
        api_endpoint = f"/lke/clusters/{_cluster.id}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        data = {
            "k8s_version": kube_version,
            "control_plane": {"high_availability": high_availability}
        }
        logger.debug(f"data: {data}")
        response = self.client.put(api_endpoint, data=data)
        if not response:
            logger.error("Failed to upgrade the control plane")
            return
        logger.debug(f"response: {response}")

        logger.info("Step 2/2 - upgrading the worker nodes")
        logger.debug(f"threshold: {threshold}")
        if not threshold:
            logger.info(f"Recycling all nodes")
            api_endpoint = f"/lke/clusters/{_cluster.id}/recycle"
            logger.debug(f"api_endpoint: {api_endpoint}")
            self.client.post(api_endpoint)
        else:
            wait_time = wait_time or 60
            nodes = self.get_nodes(cluster=cluster)
            logger.debug(f"wait_time: {wait_time}")
            nodes_to_recycle = math.floor(len(nodes) * threshold / 100)
            logger.debug(f"nodes_to_recycle: {nodes_to_recycle}")
            count = 0
            for node in nodes:
                logger.info(f"Recycling {node.id} node")
                api_endpoint = f"/lke/clusters/{_cluster.id}/nodes/{node.id}/recycle"
                logger.debug(f"api_endpoint: {api_endpoint}")
                self.client.post(api_endpoint)

                count += 1
                if count == nodes_to_recycle:
                    count = 0
                    logger.debug(f"waiting {wait_time} seconds for the next cycle")
                    sleep(wait_time)

        logger.info(f"Cluster '{cluster}' upgrade executed successfully")

    def get_cluster_id(self, cluster):
        """
        Get cluster id

        :param str cluster: a cluster name (which configured as a label)
        returns: (int) cluster's id number or None
        """
        logger.info(f"Getting '{cluster}' cluster id")
        _cluster = self.get_cluster(cluster=cluster)
        if not _cluster or not isinstance(_cluster, LKECluster):
            logger.warning(f"Cluster '{cluster}' does not exist, aborting...")
            return

        logger.info(f"cluster_id: {_cluster.id}")
        return _cluster.id

    def get_volumes(self):
        """
        Gets all volumes

        :returns: list with all volumes
        """
        logger.debug("Getting all volumes")
        volumes = self.client.volumes()
        logger.debug(f"volumes: {volumes}")
        return volumes or []

    def list_volumes(self):
        """
        list all volumes
        """
        logger.info("Listing all volumes")
        volumes = self.get_volumes()
        for volume in volumes:
            logger.debug("-" * 80)
            logger.debug(f"volume name: {volume.label}")
            logger.debug(f"volume id: {volume.id}")
            logger.debug(f"attached to: {volume.linode_id}")
            logger.debug(f"size: {volume.size}")
            logger.debug(f"region: {volume.region}")

    def delete_volume(self, volume_name=None, all=None):
        """
        Deletes volume

        :param str volume_name: a volume name
        :param bool all: used to delete all volumes
        """
        logger.info(f"Deleting volume(s)")
        volumes = self.get_volumes()
        for volume in volumes:
            _volume_name = volume.label
            if not all and volume_name and volume_name != _volume_name:
                continue

            if not volume.linode_id and _volume_name.startswith('pvc'):
                logger.debug("-" * 80)
                logger.debug(f"Deleting {_volume_name} volume")
                logger.debug(f"attached to: {volume.linode_id}")
                api_endpoint = f"/volumes/{volume.id}"
                logger.debug(f"api_endpoint: {api_endpoint}")
                self.client.delete(api_endpoint)
                logger.info(f"Volume '{_volume_name}' deleted successfully")

    def poweroff_node(self, node=None, node_name=None):
        """
        Power Off a node

        :param obj node: node instance object
        :param str node_name: a node name
        """
        node = node or self.get_node(node_name=node_name)
        if not node:
            logger.warning(f"Can't find {node_name} node to power it off, aborting...")
            return

        logger.info(f"Powering Off '{node.label}' node")
        try:
            if node.shutdown():
                logger.info(f"Node '{node.label}' successfully turned off.")
        except linode_api4.errors.ApiError as err:
            logger.error(f"Failed to power off '{node.label}' node ({err.errors})")

    def poweroff_all_nodes(self, cluster):
        """
        Power off all nodes

        :param str cluster: a cluster name (which configured as a label)
        """
        logger.info(f"Powering off all {cluster} cluster nodes")
        nodes = self.get_nodes(cluster=cluster)
        if not nodes:
            logger.warning(f"Could not find any nodes in {cluster} cluster, aborting...")
            return

        for node in nodes:
            # instance = Instance(self.client, node.instance_id)
            if node.status == "not_ready":
                logger.info(f"Instance '{node.label}' is not ready, skipping...")
                continue
            self.poweroff_node(node=node)

    def poweron_restart_node(self, node=None, node_name=None):
        """
        Power On / Restart a node

        :param obj node: node instance object
        :param str node_name: a node name
        """
        node = node or self.get_node(node_name=node_name)
        if not node:
            logger.debug(f"Can't find {node_name} node to power it on / restart, aborting...")
            return

        logger.info(f"Powering On / Restarting  '{node.label}' node")
        try:
            if node.reboot():
                logger.info(f"Node '{node.label}' successfully turned on / restarted!")
        except linode_api4.errors.ApiError as err:
            logger.error(f"Failed to power on / restart '{node.label}' node ({err.errors})")

    def poweron_restart_all_nodes(self, cluster):
        """
        Power on / restart all nodes

        :param str cluster: a cluster name (which configured as a label)
        """
        logger.info(f"Powering on / Restarting all {cluster} cluster nodes")
        nodes = self.get_nodes(cluster=cluster)
        if not nodes:
            logger.warning(f"Could not find any nodes in {cluster} cluster, aborting...")
            return

        for node in nodes:
            if node.status == "not_ready":
                logger.warning(f"Node '{node.label}' is not ready, skipping...")
                continue
            self.poweron_restart_node(node=node)

    def update_node(
            self, node=None, node_name=None,
            node_cpu_alert=None, node_network_in_alert=None,
            node_network_out_alert=None, node_transfer_quota_alert=None,
            node_io_alert=None
    ):
        """
        update a node

        :param obj node: a node instance object
        :param str node_name: a node name
        :param int node_cpu_alert: a node cpu usage alert threshold
        :param int node_network_in_alert: a node incoming traffic alert threshold
        :param int node_network_out_alert: a node outgoing traffic alert threshold
        :param int node_transfer_quota_alert: a node outgoing traffic alert threshold
        :param int node_io_alert: a node io alert threshold
        """
        node = node or self.get_node(node_name=node_name)
        if not node:
            logger.debug(f"Can't find {node_name} node, aborting...")
            return

        logger.info(f"Updating '{node.label}' node")
        api_endpoint = f"/linode/instances/{node.id}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        data = {
            "alerts": {
                "cpu": node_cpu_alert or 0,
                "network_in": node_network_in_alert or 0,
                "network_out": node_network_out_alert or 0,
                "transfer_quota": node_transfer_quota_alert or 0,
                "io": node_io_alert or 0
            }
        }
        logger.debug(f"data: {data}")
        result = self.client.put(api_endpoint, data=data)
        if result:
            logger.debug(f"Node '{node.label}' updated successfully")
            logger.debug(f"result: {result}")

    def update_all_nodes(
            self, cluster, node_cpu_alert=None, node_network_in_alert=None,
            node_network_out_alert=None, node_transfer_quota_alert=None,
            node_io_alert=None
    ):
        """
        Update all nodes

        :param str cluster: a cluster name (which configured as a label)
        :param int node_cpu_alert: a node cpu usage alert threshold
        :param int node_network_in_alert: a node incoming traffic alert threshold
        :param int node_network_out_alert: a node outgoing traffic alert threshold
        :param int node_transfer_quota_alert: a node outgoing traffic alert threshold
        :param int node_io_alert: a node io alert threshold
        """
        logger.info(f"Updating all {cluster} nodes")
        nodes = self.get_nodes(cluster=cluster)
        if not nodes:
            logger.warning(f"Could not find any nodes in {cluster} cluster, aborting...")
            return

        kwargs = {
            'node_cpu_alert': node_cpu_alert,
            'node_network_in_alert': node_network_in_alert,
            'node_network_out_alert': node_network_out_alert,
            'node_transfer_quota_alert': node_transfer_quota_alert,
            'node_io_alert': node_io_alert
        }
        for node in nodes:
            if node.status == "not_ready":
                logger.warning(f"Node '{node.label}' is not ready, skipping...")
                continue

            self.update_node(node=node, **kwargs)

    def get_storage_cluster(self, cluster=None, region=None):
        """
        Get the storage cluster per provided cluster/region
        If no cluster/region provided the first storage cluster will be provided automatically

        :param str cluster: a cluster name (which configured as a label)
        :param str region: a region id
        :returns: storage bucket object or None
        """
        logger.info(f"Getting storage cluster")
        _cluster = self.get_cluster(cluster=cluster) if cluster else None
        region_id = _cluster.region.id if _cluster else region
        logger.debug(f"region_id: {region_id}")
        storage_clusters = self.client.object_storage.clusters()
        for storage_cluster in storage_clusters:
            if region_id and region_id not in storage_cluster.id:
                continue

            logger.debug(f"storage_cluster: {storage_cluster.id}")
            return storage_cluster

    def create_storage(self, bucket_name, cluster=None, region=None):
        """
        Creates or Updates a storage bucket

        :param str cluster: a cluster name (which configured as a label)
        :param str region: a region id
        :param str bucket_name: a bucket name
        """
        logger.info(f"Creating '{bucket_name}' bucket")
        storage_cluster = self.get_storage_cluster(cluster=cluster, region=region)
        if not storage_cluster:
            logger.warning("Could not find a storage cluster, aborting...")
            return

        self.client.object_storage.bucket_create(
            cluster_or_region=storage_cluster,
            label=bucket_name
        )
        logger.debug(f"Storage '{bucket_name}' created successfully")

    def delete_storage(self, bucket_name, cluster=None, region=None):
        """
        Deletes a storage bucket

        :param str cluster: a cluster name (which configured as a label)
        :param str region: a region id
        :param str bucket_name: a bucket name
        """
        logger.info(f"Deleting '{bucket_name}' bucket")
        storage_cluster = self.get_storage_cluster(cluster=cluster, region=region)
        if not storage_cluster:
            logger.warning("Could not find storage cluster")
            return

        api_endpoint = f"/object-storage/buckets/{storage_cluster.id}/{bucket_name}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        try:
            self.client.delete(api_endpoint)
        except Exception as err:
            if err and getattr(err, 'status') == 404:
                raise Exception(f"Bucket '{bucket_name}' does not exist ({getattr(err, 'status', 'Unknown')})")

        logger.debug(f"Storage '{bucket_name}' deleted successfully")

    def list_storage(self):
        """
        list all storage objects
        """
        logger.info("Listing all storage objects")
        buckets = self.client.object_storage.buckets()
        for bucket in buckets:
            logger.debug("-" * 80)
            logger.debug(f"bucket name: {bucket.label}")
            logger.debug(f"bucket id: {bucket.id}")
            logger.debug(f"hostname: {bucket.hostname}")
            logger.debug(f"cluster: {bucket.cluster}")
            logger.debug(f"objects: {bucket.objects}")
            logger.debug(f"size: {bucket.size}")

    def get_firewall_id(self, firewall):
        """
        Get firewall id

        :param str firewall: a firewall name
        returns: (int) firewall's id number or None
        """
        logger.info(f"Getting '{firewall}' firewall id")
        firewalls = self.client.networking.firewalls()
        for _firewall in firewalls:
            if _firewall.label != firewall:
                continue

            logger.debug(f"firewall_id: {_firewall.id}")
            return _firewall.id

    def get_firewalls(self):
        """
        Gets all firewalls

        :returns: list with all firewalls
        """
        logger.debug("Getting all firewalls")
        firewalls = self.client.networking.firewalls()
        logger.debug(f"firewalls: {firewalls}")
        return firewalls or []

    def list_firewalls(self):
        """
        list all firewalls
        """
        logger.info("Listing all firewalls")
        firewalls = self.get_firewalls()
        for firewall in firewalls:
            logger.debug("-" * 80)
            logger.debug(f"firewall name: {firewall.label}")
            logger.debug(f"firewall id: {firewall.id}")
            logger.debug(f"status: {firewall.status}")
            logger.debug(f"devices: {firewall.devices}")

    def add_node_to_firewall(self, node_name, firewall):
        """
        Adds node to a firewall

        :param str node_name: a node name
        :param str firewall: a firewall name
        """
        logger.info(f"Adding {node_name} node to {firewall} firewall")
        node_id = self.get_node_id(node_name=node_name)
        if not node_id:
            logger.warning(f"Could not find {node_name} node, aborting...")
            return

        firewall_id = self.get_firewall_id(firewall=firewall)
        if not firewall_id:
            logger.warning(f"Could not find {firewall} firewall, aborting...")
            return

        data = {
            "id": node_id,
            "type": "linode"
        }

        api_endpoint = f"/networking/firewalls/{firewall_id}/devices"
        logger.debug(f"api_endpoint: {api_endpoint}")
        try:
            response = self.client.post(api_endpoint, data=data)
            if response:
                logger.debug(f"response: {response}")
        except Exception as err:
            errors = getattr(err, 'errors', [])
            msg = "Too many active firewalls attached to Linode"
            logger.warning(f"{err}")
            if err and getattr(err, 'status') == 400 and msg in errors[-1]:
                return

        logger.info(f"Node {node_name} was successfully added to {firewall} firewall!")

    def add_all_nodes_to_firewall(self, cluster, firewall):
        """
        Adds all nodes to a firewall

        :param str firewall: a firewall name
        :param str cluster: a cluster name
        """
        logger.info(f"Adding all '{cluster}' cluster nodes to a '{firewall}' firewall")
        nodes = self.get_nodes(cluster=cluster)
        if not nodes:
            logger.warning(f"Could not find any nodes in {cluster} cluster, aborting...")
            return

        for node in nodes:
            node_name = node.label
            self.add_node_to_firewall(node_name=node_name, firewall=firewall)

    def get_func(self, action, resource, all):
        """
        Get a function based on the passed action/resource

        :param str action: action name (i.e., update, create)
        :param str resource: resource name (i.e., cluster)
        :param bool all: used to select a function that will be implemented on all items in the resource
        :return: func object
        """
        if not action:
            return

        cluster_action_to_func_mapper = {
            'create': self.create_cluster,
            'update': self.update_cluster,
            'upgrade': self.upgrade_cluster,
            'get-id': self.get_cluster_id,
            'delete': self.delete_cluster
        }

        node_action_to_func_mapper = {
            'get-id': self.get_node_id,
            'poweron': self.poweron_restart_all_nodes if all else self.poweron_restart_node,
            'poweroff': self.poweroff_all_nodes if all else self.poweroff_node,
            'restart': self.poweron_restart_all_nodes if all else self.poweron_restart_node,
            'update': self.update_all_nodes if all else self.update_node
        }

        volume_action_to_func_mapper = {
            'list': self.list_volumes,
            'delete': self.delete_volume
        }

        storage_action_to_func_mapper = {
            'list': self.list_storage,
            'delete': self.delete_storage,
            'create': self.create_storage
        }

        firewall_action_to_func_mapper = {
            'get-id': self.get_firewall_id,
            'list': self.list_firewalls,
            'add-node': self.add_all_nodes_to_firewall if all else self.add_node_to_firewall,
            # 'delete': self.delete_firewall,
            # 'create': self.create_firewall
        }

        resource_to_func_mapper = {
            'cluster': cluster_action_to_func_mapper.get(action),
            'node': node_action_to_func_mapper.get(action),
            'volume': volume_action_to_func_mapper.get(action),
            'storage': storage_action_to_func_mapper.get(action),
            'firewall': firewall_action_to_func_mapper.get(action)
        }

        return resource_to_func_mapper.get(resource)


def main():
    """ MAIN FUNCTION """

    try:
        # get app arguments
        args = get_cli_args()

        # initialize logger
        init_logging(
            log_file=args.log_file or '',
            verbose=args.verbose,
            console=args.console,
            info='green', debug='cyan'
        )

        logger.info(f"Linode Management (version: {VERSION})")
        client = LinodeMGMT(token=args.token)

        func = client.get_func(args.action, getattr(args, 'resource', None), getattr(args, 'all', None))
        if not func:
            raise Exception("No such action/resource")

        kwargs = {}
        func_args = inspect.getfullargspec(func).args
        for key in func_args:
            if key == 'self':
                continue

            if key == 'args':
                kwargs = {'args': args}
                break

            if getattr(args, key, None):
                kwargs[key] = getattr(args, key)

        func(**kwargs)

    except Exception as err:
        logger.error(err.message) \
            if hasattr(err, 'message') else logger.error(err)
        return 1


if __name__ == '__main__':
    sys.exit(main())
