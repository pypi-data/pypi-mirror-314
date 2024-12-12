import time
from datetime import timedelta

from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions


def connect_to_couchbase(
    connection_string, db_username, db_password, retries=3, retry_delay=5
):
    """Connect to couchbase"""

    auth = PasswordAuthenticator(db_username, db_password)
    options = ClusterOptions(auth)
    connect_string = connection_string
    for attempt in range(retries):
        try:
            cluster = Cluster(connect_string, options)
            cluster.wait_until_ready(timedelta(seconds=20))
            return cluster

        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All connection attempts failed.")
                raise
