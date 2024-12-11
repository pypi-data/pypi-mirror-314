# LINODE-MGMT
The linode-mgmt is a python package that used to manage Linode ELK clusters.

To use this package and perform actions on linode, you will need to acquire a token.
Follow the following guideline to acquire one:
* Browse to https://www.linode.com/
* Click on your profile --> API Tokens
* Click on the `Create A Personal Access Token` button
* Fill in all your details and click on the `Create Token` button
* Keep the Token in a safe place

Note: This token will be used to communicate with the Linode API.

## Prerequisites

Prepare the python virtual environment

```bash
mkdir linode-mgmt ; cd linode-mgmt
python3.9 -m venv .
source bin/activate
```

Make sure the following packages are installed:
- pip==22.3.1
- setuptools==65.6.3

## Installation

```bash
pip install linode-mgmt
```

## Usage:
usage: linode-mgmt <resource> <action> [arguments]

Linode Management component

```
optional arguments:
  --help            show this help message and exit
  --version         shows program version
  --log-file NAME   log file name
  --verbose         if added will print more information
  --dry-run         used to test action without performing anything

required arguments:
  --token <TEXT>    a personal access token

resources:
    cluster
    node
    volume
    storage
    firewall
```

## Examples:

- To create a new cluster with 3 nodes in 'us-iad' region
ref: https://api.linode.com/v4/regions
```
linode-mgmt cluster create \
--token <token> \
--cluster <cluster> \
--region us-iad \
--node-count 3 \
--node-type g6-dedicated-56 \
--kube-version 1.30 \
--verbose
```

- To upgrade an existing cluster to a newer kubernetes version
ref: https://www.linode.com/docs/products/compute/kubernetes/guides/upgrade-kubernetes-version/?tabs=cloud-manager,linode-api
```
linode-mgmt cluster upgrade \
--token <token> \
--cluster <cluster> \
--kube-version 1.31 \
--verbose
```

- To delete a cluster
```
linode-mgmt cluster delete \
--token <token> \
--cluster <cluster> \
--verbose
```

- To get a cluster id
```
linode-mgmt cluster get-id \
--token <token> \
--cluster <cluster> \
--verbose
```

- To power on a specific node
```
linode-mgmt node poweron \
--token <token> \
--node lke87300-132938-63c003e48302 \
--verbose
```

- To power off a specific node
```
linode-mgmt node poweroff \
--token <token> \
--node lke87300-132938-63c003e48302 \
--verbose
```

- To restart a specific node
```
linode-mgmt node restart \
--token <token> \
--node lke87300-132938-63c003e48302 \
--verbose
```

- To get a node id
```
linode-mgmt node get-id \
--token <token> \
--node lke87300-132938-63c003e48302 \
--verbose
```

- To update a node with specific alert thresholds
```
linode-mgmt node update \
--token <token> \
--cluster <cluster> \
--node lke87300-132938-63c003e48302 \
--node-cpu-alert 
--verbose
```

- To delete a volume
```
linode-mgmt volume delete \
--token <token> \
--volume-name pvc1809b72cc85e4fa7 \
--verbose
```

- To create a new storage objects (bucket)
```
linode-mgmt storage create \
--token <token> \
--cluster <cluster> \
--bucket-name <bucket> \
--verbose
```

- To List all storage objects
```
linode-mgmt storage list \
--token <token> \
--cluster <cluster> \
--verbose
```

- To delete a storage objects
```
linode-mgmt storage delete \
--token <token> \
--cluster <cluster> \
--bucket-name <bucket> \
--verbose
```

- To get a firewall id
```
linode-mgmt firewall get-id \
--token <token> \
--firewall <firewall> \
--verbose
```

- To get a list of all firewalls
```
linode-mgmt firewall list \
--token <token> \
--verbose
```

- To add a node to a firewall
```
linode-mgmt firewall add-node \
--token <token> \
--node-name lke268293-471352-15cf7a690000 \
--firewall <firewall> \
--verbose
```