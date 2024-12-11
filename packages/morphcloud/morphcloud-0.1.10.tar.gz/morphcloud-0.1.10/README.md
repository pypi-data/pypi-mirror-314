# MorphCloud Python SDK 

## Overview

MorphCloud is a platform designed to spin up remote AI devboxes we call runtimes. It provides a suite of code intelligence tools and a Python SDK to manage, create, delete, and interact with runtime instances.

## Setup Guide

### Prerequisites

Python 3.8 or higher

Go to [https//:cloud.morph.so](https://cloud.morph.so/web/api-keys), log in with the provided credentials and create an API key.

Set the API key as an environment variable  `MORPH_API_KEY`.

### Installation

```
pip install git+https://github.com/morph-labs/morph-python-sdk.git
```

Export the API key:

```
export MORPH_API_KEY="your-api-key"
```

## Quick Start

To start using MorphCloud, you can create and manage runtime instances using the provided classes and methods. Here's a basic example to create a runtime instance:

```py
from morphcloud.api import MorphClient

client = MorphClient()


snapshot = client.snapshot.create()
runtime = client.runtime.create(snapshot_id=snapshot.id)

runtime.exec("echo 'Hello, World!'")
```

## Command Line Interface

The SDK also provides a command line interface to interact with the MorphCloud API. You can use the CLI to create, delete, and manage runtime instances.

```bash
morphcloud snapshot list
morphcloud runtime create
```
