#!/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import argparse

def uploadFile():
    parser = argparse.ArgumentParser(description='Upload file to server')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--uploadPath', type=str, help='uploadPath', required=True)
    parser.add_argument('--filePath', type=str, help='filePath', required=True)
    parser.add_argument('--url', type=str, help='url', required=True)
    parser.add_argument('--username', type=str, help='username', required=True)
    parser.add_argument('--password', type=str, help='password', required=True)
    args = parser.parse_args()

    # check error input
    if not os.path.exists(args.filePath):
        print(f"File {args.filePath} not found")
        exit(1)

    if args.name == "":
        print("Name is invalid")
        exit(1)

    if not args.url.startswith("http"):
        print("URL is invalid")
        exit(1)

    username = args.username
    password = args.password
    local_file_path = args.filePath
    remote_file_path = args.uploadPath + "/" + args.name
    next_cloud_url = args.url

    # Upload file
    upload_command = [
        "curl", "-u", f"{username}:{password}", "-T", local_file_path,
        f"{next_cloud_url}/remote.php/webdav/{remote_file_path}"
    ]
    subprocess.run(upload_command, check=True)

    # Create share link
    share_command = [
        "curl", "-u", f"{username}:{password}", "-X", "POST",
        "-d", f"path=/{remote_file_path}", "-d", "shareType=3", "-d", "permissions=1",
        f"{next_cloud_url}/ocs/v2.php/apps/files_sharing/api/v1/shares",
        "-H", "OCS-APIRequest: true"
    ]
    result = subprocess.run(share_command, check=True, capture_output=True, text=True)
    url = result.stdout.split("<url>")[1].split("</url>")[0]

    print(url)

if __name__ == "__main__":
    uploadFile()