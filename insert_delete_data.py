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


# spanner_insert_data
def insert_data(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table="Singers",
            columns=("SingerId", "FirstName", "LastName"),
            values=[
                (1, u"Marc", u"Richards"),
                (2, u"Catalina", u"Smith"),
                (3, u"Alice", u"Trentor"),
                (4, u"Lea", u"Martin"),
                (5, u"David", u"Lomond"),
            ],
        )

        batch.insert(
            table="Albums",
            columns=("SingerId", "AlbumId", "AlbumTitle"),
            values=[
                (1, 1, u"Total Junk"),
                (1, 2, u"Go, Go, Go"),
                (2, 1, u"Green"),
                (2, 2, u"Forever Hold Your Peace"),
                (2, 3, u"Terrified"),
            ],
        )

    print("Inserted data.")


# spanner_delete_data
def delete_data(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    albums_to_delete = spanner.KeySet(keys=[[2, 1], [2, 3]])

    singers_range = spanner.KeyRange(start_closed=[3], end_open=[5])
    singers_to_delete = spanner.KeySet(ranges=[singers_range])

    remaining_singers = spanner.KeySet(all_=True)

    with database.batch() as batch:
        batch.delete("Albums", albums_to_delete)
        batch.delete("Singers", singers_to_delete)
        batch.delete("Singers", remaining_singers)

    print("Deleted data.")
