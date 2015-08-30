import argparse
from lxml import etree
from os.path import isfile

def manifest_permissions(manifest):
    """Extracts permissions in the manifest

    Extracts the permissions in the manifest file,
    and returns a set of permissions required by
    the manifest.
    IN: manifest, the root element of the manifest file
    OUT: a set of permission names
    """
    permset = {list(permission)[0].text for permission in list(manifest)
               if list(permission)[0].text.startswith("android.permission")}
    return permset

def code_permissions(code):
    """Extracts permissions in the code

    Extracts the permissions in the file produced from the code, and returns a
    set of permissions used in the code.
    IN: code, the root element of the code file
    OUT: a set of permission names
    """
    permset = set()
    for call in list(code):
        permissions = [permissions for permissions in list(call)
                       if permissions.tag == 'permissions'][0]
        permset |= {list(permission)[0].text for permission in permissions}
    return permset

def compare(manifest, code):
    """Compares manifest and code permissions

    Finds over- and under-specifications of permissions by comparing
    the permissions required by the manifest, and those actually used
    in the code
    IN: manifest, a set of permissions required by the manifest
    IN: code, a set of permissions required by the code
    OUT: a dict containing two sets: a set of over-specifications of
    permissions, and a set of under-specifications of permissions
    """
    over = manifest - code
    under = code - manifest
    result = {'over':over, 'under':under}
    return result

def prepare_output(result):
    """Produces an XML tree to output

    Takes the list of over- and under-specified permissions, and turns
    it into an XML tree.

    IN: result: a dictionary containing a list of over-specified
    permissions and a list of under-specified permission
    OUT: an XML tree representation of the input
    """
    root = etree.Element('comparison')
    over = etree.Element("over-specification")
    under = etree.Element("under-specification")

    for perm in result['over']:
        elt = etree.Element('permission')
        elt.text = perm
        over.append(elt)

    for perm in result['under']:
        elt = etree.Element('permission')
        elt.text = perm
        under.append(elt)

    root.append(over)
    root.append(under)
    tree = etree.ElementTree(root)
    return tree

def write(result, outfile):
    """Writes an XML tree into the output file"""
    out = open(outfile, 'wb')
    result.write(out, pretty_print=True)

parser = argparse.ArgumentParser()
parser.add_argument("manifest", help="permissions extracted from the manifest")
parser.add_argument("code", help="permissions extracted from the code")
parser.add_argument("output", help="output file")
args = parser.parse_args()

manifest_tree = etree.parse(args.manifest)
code_tree = etree.parse(args.code)
manifest_root = manifest_tree.getroot()
code_root = code_tree.getroot()

manifest_perms = manifest_permissions(manifest_root)
code_perms = code_permissions(code_root)
result = compare(manifest_perms, code_perms)

print(result)

output_tree = prepare_output(result)
write(output_tree, args.output)
