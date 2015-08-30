# Preparing AndroidManifest.xml for transformation

Currently, BiFluX cannot deal with the way Android Manifests are written. The issues are minor, nothing that cannot be solved by using a script to make minor adjustments to the manifest, that do not destroy any meaningful information. The script can also be used to perform the opposite, i.e. turn a biflux-formatted manifest into a valid AndroidManifest.xml. Essentially, this is a bidirectional transformation that prepares a file for another bidirectional transformation.

We hope that BiFluX will eventually be able to support Android Manifests fully, but until then, we use this script.

## Issues with manifests

There are three issues:

+ the <data> element is a keyword in BiFluX, so we can't use it. The script renames <data> elements into <android-data> elements. The reverse operation is obvious.
+ the order of elements is important for an XML file to conform to a DTD. To solve this issue, the script reorders elements in alphabetic order. Since the order of elements does not matter for Android Manifests, there is no reverse operation.
+ empty elements with attributes are not well supported by BiFluX. The script adds an empty element without any attributes as a child of elements with attributes. The reverse operation removes those empty attributes.

## Usage

The script is simple to use:

### AndroidManifest to biflux-ready manifest

prepare.py -f <androidmanifest> <biflux-manifest>

### biflux-ready manifest to AndroidManifest

prepare.py -b <biflux-manifest> <androidmanifest>

## Requirements

The script uses Python's lxml library. It has been tested with Python 2.7 and 3.4.
