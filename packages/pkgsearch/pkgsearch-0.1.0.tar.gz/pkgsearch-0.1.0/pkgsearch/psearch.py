import requests
import json
import argparse
from packaging.version import Version, InvalidVersion
import pyperclip
from xml.etree import ElementTree

def get_pypi_versions(package_name):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return list(data["releases"].keys())
        return []
    except Exception as e:
        print(f"Error fetching PyPI versions: {e}")
        return []

def get_nuget_versions(package_name):
    try:
        url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            versions = data.get('versions', [])
            return versions
        return []
    except Exception as e:
        print(f"Error fetching NuGet versions: {e}")
        return []

def get_maven_versions(group_id, artifact_id):
    try:
        url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/maven-metadata.xml"
        response = requests.get(url)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            versions = [version.text for version in tree.findall(".//version")]
            return versions
        return []
    except Exception as e:
        print(f"Error fetching Maven versions: {e}")
        return []

def get_cargo_versions(package_name):
    try:
        url = f"https://crates.io/api/v1/crates/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            versions = [version["num"] for version in data["versions"]]
            return versions
        return []
    except Exception as e:
        print(f"Error fetching Cargo versions: {e}")
        return []

def get_go_versions(package_name):
    try:
        url = f"https://proxy.golang.org/{package_name}/@v/list"
        response = requests.get(url)
        if response.status_code == 200:
            versions = response.text.strip().split('\n')
            return versions
        return []
    except Exception as e:
        print(f"Error fetching Go versions: {e}")
        return []

def filter_versions(versions, lower_bound, upper_bound):
    filtered_versions = []
    for v in versions:
        try:
            parsed_version = Version(v)
            if (lower_bound is None or parsed_version >= Version(lower_bound)) and \
               (upper_bound is None or parsed_version <= Version(upper_bound)):
                filtered_versions.append(parsed_version)
        except InvalidVersion:
            continue  # Skip invalid versions without printing an error
    return sorted(filtered_versions)

def fetch_versions(args):
    if args.repository == "pypi":
        return get_pypi_versions(args.package)
    elif args.repository == "nuget":
        return get_nuget_versions(args.package)
    elif args.repository == "maven":
        group_id, artifact_id = args.package.split(":")
        return get_maven_versions(group_id, artifact_id)
    elif args.repository == "cargo":
        return get_cargo_versions(args.package)
    elif args.repository == "go":
        return get_go_versions(args.package)
    return []

def output_results(args, filtered_versions):
    filtered_versions_str = [str(v) for v in filtered_versions]
    if args.json:
        output = json.dumps({"package": args.package, "repository": args.repository, "versions": filtered_versions_str}, indent=4)
    else:
        output = f"Versions found for {args.package} in {args.repository}:\n" + "\n".join(filtered_versions_str)
    print(output)
    if not args.no_clipboard:
        pyperclip.copy(output)
        print("Results copied to clipboard.")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Search for package versions from various repositories")
    parser.add_argument("repository", choices=["pypi", "nuget", "maven", "cargo", "go"], help="The repository to search")
    parser.add_argument("package", help="The package name (or group_id:artifact_id for Maven)")
    parser.add_argument("--vr", nargs=2, metavar=('LOWER', 'UPPER'), help="The version range (lower bound and upper bound)")
    parser.add_argument("--json", action="store_true", help="Output the results in JSON format")
    parser.add_argument("--no-clipboard", action="store_true", help="Do not copy the results to the clipboard")
    return parser.parse_args()

def main():
    args = parse_arguments()
    lower_bound = args.vr[0] if args.vr else None
    upper_bound = args.vr[1] if args.vr else None

    versions = fetch_versions(args)
    if versions:
        filtered_versions = filter_versions(versions, lower_bound, upper_bound)
        output_results(args, filtered_versions)
    else:
        output = f"No versions found for {args.package} in {args.repository}"
        if args.json:
            output = json.dumps({"package": args.package, "repository": args.repository, "versions": []}, indent=4)
        print(output)
        if not args.no_clipboard:
            pyperclip.copy(output)
            print("Results copied to clipboard.")

if __name__ == "__main__":
    main()