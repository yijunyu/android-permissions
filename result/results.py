import argparse
from lxml import etree
from os.path import isfile, isdir
import csv
import os
import re

def write_results(output, results):
    """Write results to CSV file

    output is a file
    results is a list of dictionaries, each element representing a row.
    """
    with open(output, 'wb') as csvfile:
        fieldnames = ['app_name', 'sdk_version', 'over', 'under', 'errors']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='&')

        writer.writeheader()
        for app in results:
            for line in app:
                writer.writerow(line)

def collect_all_versions(directory):
    """Collects data in aggregate of each version, for each app.

    Returns a list of dictionaries
    directory is the directory in which the data resides (doubles as the name)
    """
    name = directory
    print("[%s] collecting app data" % name)
    version = "all"
    file = "comparison_all.xml"
    data = etree.parse('{0}/{1}/{2}'.format(base_path, name, file)).getroot()
    collected = [collect_version_data(name, version, data)]
    return collected

def collect_app_data(directory):
    """Collects data from all versions of an app. Returns a list of dictionaries

    directory is the directory in which the data resides (doubles as the name)
    """
    name = directory
    print("[%s] collecting app data" % name)
    p = re.compile('comparison_[0-9|.]+.xml')
    files = [file for file in os.listdir(directory) if p.match(file)]
    print("[%s] Found %s versions" % (name, len(files)))
    collected = []
    for file in files:
        version = file.lstrip("comparisn_").rstrip("xml.")
        data = etree.parse('{0}/{1}/{2}'.format(base_path, name, file)).getroot()
        collected.append(collect_version_data(name, version, data))
    return collected

def collect_version_data(name, version, data):
    """Collects data from a particular version of an app. Returns a dictionary

    name is the name of the app
    version is the Android SDK version number
    data is an lxml elements representing the root of the comparison file for a
    specific version
    """
    print("[%s] collecting results for version %s" % (name, version))
    row = {'app_name' : name, 'sdk_version' : version}
    over = list(data.find('over-specification'))
    under = list(data.find('under-specification'))
    row['over'] = len(over)
    print('[{0}][{1}] found {2} over-specified permissions'.format(name, version, len(over)))
    row['under'] = len(under)
    print('[{0}][{1}] found {2} under-specified permissions'.format(name, version, len(under)))
    row['errors'] = len(set(over) & set(under))
    print('[{0}][{1}] found {2} errors'.format(name, version, len(set(over) & set(under))))
    return row

parser = argparse.ArgumentParser()
parser.add_argument("directory",
                    help="the directory in which all the results are found. Results are in subdirectories named after an app")
parser.add_argument("output", help="the output file")
parser.add_argument("allversions",
                    help="output for data aggregated across all versions")
args = parser.parse_args()

if not isdir(args.directory):
    print("Could not find directory %s", args.directory)
    exit

base_path = args.directory
print("Analysing results in %s" % base_path)
apps = [directory for directory in os.listdir(base_path)
        if isdir(directory)]
all_data = [collect_app_data(app) for app in apps]
all_versions = [collect_all_versions(app) for app in apps
                if isfile('{0}/{1}/comparison_all.xml'.format(base_path, app))]
write_results(args.output, all_data)
write_results(args.allversions, all_versions)
