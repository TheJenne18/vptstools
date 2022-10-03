# Simple Python script that:
# - Connects via SFTP to the BALTRAD server
# - For each VP file (pvol gets ignored), download the file from the server and upload it to the "aloft" S3 bucket

# Designed to be executed daily via a simple cronjob (files disappear after a few days on the BALTRAD server)
# Use a simple config file named config.ini. Create one by copying config.template.ini and filling in the values.
# If file already exists at destination => do nothing
import os
from ast import Tuple
import tempfile
from configparser import ConfigParser

import boto3
import paramiko

from vptstools.scripts.constants import CONFIG_FILE


def s3_key_exists(key: str, bucket: str, s3_client) -> bool:
    results = s3_client.list_objects(Bucket=bucket, Prefix=key)
    return "Contents" in results


def extract_metadata_from_filename(filename: str) -> Tuple[str, str, str, str]:
    """Extract the metadata from the filename (format such as 'fropo_vp_20220809T051000Z_0xb')

    All returned values are strings, month and days are 0-prefixed if they are single-digit.
    """
    elems = filename.split("_")
    radar_code = elems[0]
    timestamp = elems[2]

    year = timestamp[0:4]
    month_str = timestamp[4:6]
    day_str = timestamp[6:8]

    return radar_code, year, month_str, day_str


def main():
    print("1. Read configuration from file")
    config = ConfigParser()
    config.read(CONFIG_FILE)
    baltrad_server_host = config.get("baltrad_server", "host")
    baltrad_server_port = config.getint("baltrad_server", "port")
    baltrad_server_username = config.get("baltrad_server", "username")
    baltrad_server_password = config.get("baltrad_server", "password")
    baltrad_server_datadir = config.get("baltrad_server", "datadir")

    destination_bucket = config.get("destination_bucket", "name")

    print("2. Establish SFTP connection")
    paramiko.util.log_to_file("paramiko.log")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )  # necessary to avoid "Server 'hostname' not found in known_hosts error
    ssh.connect(
        baltrad_server_host,
        port=baltrad_server_port,
        username=baltrad_server_username,
        password=baltrad_server_password,
    )
    sftp = ssh.open_sftp()
    sftp.chdir(baltrad_server_datadir)

    print("3. Initialize S3/Boto3 client")
    session = boto3.Session(profile_name="prod")
    s3_client = session.client("s3")

    print("Initialization complete, we can loop on files on the SFTP server")
    for entry in sftp.listdir_iter():
        if "_vp_" in entry.filename:  # PVOLs and other files are ignored
            print(f"{entry.filename} is a VP file, we need to consider it... ", end="")

            radar_code, year, month_str, day_str = extract_metadata_from_filename(
                entry.filename
            )
            destination_key = f"baltrad/hdf5/{radar_code}/{year}/{month_str}/{day_str}/{entry.filename}"
            if not s3_key_exists(destination_key, destination_bucket, s3_client):
                print(
                    f"{destination_key} does not exist at {destination_bucket}, we need to transfer it...",
                    end="",
                )
                with tempfile.TemporaryDirectory() as tmpdirname:
                    tmp_file_path = os.path.join(tmpdirname, entry.filename)
                    sftp.get(entry.filename, tmp_file_path)
                    print("SFTP download completed. ", end="")
                    s3_client.upload_file(
                        tmp_file_path, destination_bucket, destination_key
                    )
                    print("Upload to S3 completed!")
            else:
                print(
                    f"{destination_key} already exists at {destination_bucket}, we skip it"
                )
    print("ALl done!")


if __name__ == "__main__":
    main()
