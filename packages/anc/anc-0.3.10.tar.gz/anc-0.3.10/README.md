# ANC CLI Tool

## Overview
The ANC CLI tool is a comprehensive command line interface designed to facilitate the management of various resources within the company. Initially, it supports managing datasets and their versions, enabling users to interact seamlessly with a remote server for fetching, listing, and adding datasets.

## Installation

```bash
# Instructions for installing the ANC CLI tool
sudo pip install anc

```

## Dataset
- **Fetch Datasets**: Retrieve specific versions of datasets from a remote server.
- **List Versions**: View all available versions of a dataset.
- **Add Datasets**: Upload new datasets along with their versions and descriptions to the remote server.

### Usage

#### list
```bash

anc ds list 
# Or you can specify a dataset name.
anc ds list -n <dataset name>

```

#### get
```bash

# According to the above list result, you can download the specific version dataset.
# Ensure that the destination path for downloads is a permanent storage location(e.g. /mnt/weka/xxx). Currently, downloading data to local storage is not permitted.
anc ds get cifar-10-batches-py -v 1.0

```

#### add
```bash

# Upload a specific version of a dataset. The dataset name will be determined based on the file or folder name extracted from the specified path.
# Ensure that the dataset is stored in a permanent location recognized by the server (e.g., /mnt/weka/xxx).
anc ds add /mnt/weka/xug/dvc_temp/cifar-10-batches-py -v 1.0

```