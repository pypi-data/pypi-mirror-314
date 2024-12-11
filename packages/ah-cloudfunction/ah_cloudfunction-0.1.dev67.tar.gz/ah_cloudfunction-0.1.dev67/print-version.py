# print("py-exec")
import setuptools_scm
import argparse
import os
import sys
import subprocess
from google.cloud import artifactregistry_v1
from google.api_core.exceptions import NotFound

def get_version(appName):
    #setup_dir = os.path.join(script_dir, appName)
    version = setuptools_scm.get_version(root=appName,local_scheme="no-local-version")
    print(version)
    return version

def check_version_exists(version, package):
    try:
        client = artifactregistry_v1.ArtifactRegistryClient()
        name = f"{package}/versions/{version}"
        print(name)
        response = client.get_version(name=name)
        return True
    except NotFound:
        return False

if __name__ == "__main__":
    print("AH branch execution")
    # Check if version is provided as input
    parser = argparse.ArgumentParser(description='Check if a version exists in Google Artifact Registry.')
    parser.add_argument('--version', type=str, default='', help='The release version .')
    parser.add_argument('--project', type=str, default='thdp-hds-shrd-artifacts-25d4', help='The Google Cloud project ID.')
    parser.add_argument('--location', type=str, default='northamerica-northeast1', help='The location of the repository.')
    parser.add_argument('--repo', type=str, default='th-hds-shared-artifactory', help='The name of the repository.')
    parser.add_argument('--appname', type=str, default='thdp-hds-cloud-functions', help='The name of the package.')

    args = parser.parse_args()
    print("args: ", args)
    if args.version:
        print("Checking if Release version exists or not")
        new_version = args.version.replace("release-v", "")
    else:
        print("Checking if Snapshot version exists or not")
        # Get the version
        new_version = get_version(args.appname)
        
    print(f"Version: {new_version}")
    # Define package path
    gcp_base_path = f"projects/{args.project}/locations/{args.location}/repositories/{args.repo}/packages"
    package = f"{gcp_base_path}/{args.appname}"
    print(f"PACKAGE: {package}")

    # Check if version exists in Google Artifactory
    version_exists = check_version_exists(new_version, package)


 # Save the result to GitHub environment
    if version_exists:
        print(f"Version {new_version} exists in Google Artifactory.")
        print("::set-output name=VERSION_EXISTS::true")
        with open('version.txt', 'w') as version_file:
            version_file.write(new_version)
    else:
        print(f"Version {new_version} does not exist in Google Artifactory.")
        print("::set-output name=VERSION_EXISTS::false")

 
    sys.exit(0)
