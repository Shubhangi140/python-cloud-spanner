import argparse
import base64
import datetime
import decimal
import json
import logging
import time

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

OPERATION_TIMEOUT_SECONDS = 240
def create_instance(instance_id):

    spanner_client = spanner.Client()

    config_name = "{}/instanceConfigs/regional-us-central1".format(
        spanner_client.project_name
    )

    instance = spanner_client.instance(
        instance_id,
        configuration_name=config_name,
        display_name="instance1",
        node_count=1,
        labels={
            "cloud_spanner_samples": "true",
            "sample_name": "create_instance",
            "created": str(int(time.time())),
        },
    )

    operation = instance.create()

    print("Waiting for operation to complete...")
    operation.result(OPERATION_TIMEOUT_SECONDS)

    print("Created instance {}".format(instance_id))

# spanner_list_instance_configs
def list_instance_config():
    spanner_client = spanner.Client()
    configs = spanner_client.list_instance_configs()
    for config in configs:
        print(
            "Available leader options for instance config {}: {}".format(
                config.name, config.leader_options
            )
        )


