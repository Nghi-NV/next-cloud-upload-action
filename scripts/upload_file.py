#!/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import argparse

def uploadFile():
    name = os.environ.get('name')
    uploadPath = os.environ.get('uploadPath')
    local_file_path = os.environ.get('filePath')
    shareEnabled = os.environ.get('shareEnabled')
    next_cloud_url = os.environ.get('url')
    username = os.environ.get('username')
    password = os.environ.get('password')

    # check error input
    if not os.path.exists(local_file_path):
        print(f"File {local_file_path} not found")
        exit(1)

    if name == "":
        print("Name is invalid")
        exit(1)

    if not next_cloud_url.startswith("http"):
        print("URL is invalid")
        exit(1)

    remote_file_path = name
    if uploadPath != "":
        remote_file_path = uploadPath + "/" + name

    # Upload file
    upload_command = [
        "curl", "-u", f"{username}:{password}", "-T", local_file_path,
        f"{next_cloud_url}/remote.php/webdav/{remote_file_path}"
    ]
    subprocess.run(upload_command, check=True)

    if shareEnabled == "false":
        print(f"::set-output name=output_url::{next_cloud_url}/remote.php/webdav/{remote_file_path}")
        return

    # Create share link
    share_command = [
        "curl", "-u", f"{username}:{password}", "-X", "POST",
        "-d", f"path=/{remote_file_path}", "-d", "shareType=3", "-d", "permissions=1",
        f"{next_cloud_url}/ocs/v2.php/apps/files_sharing/api/v1/shares",
        "-H", "OCS-APIRequest: true"
    ]
    result = subprocess.run(share_command, check=True, capture_output=True, text=True)

    try:
        url = result.stdout.split("<url>")[1].split("</url>")[0]
        print(f"::set-output name=output_url::{url}")
    except:
        print("Error while sharing file", result.stdout)
        exit(1)

if __name__ == "__main__":
    uploadFile()