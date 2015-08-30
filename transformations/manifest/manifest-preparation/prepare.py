import argparse
from lxml import etree
from os.path import isfile

def gettag(element):
    return element.tag

def sortbytag(elements):
    """Re-orders a list of elements in alphabetical order. If multiple elements appear in the list, their order is unspecified"""
    elements.sort(key=gettag)

def write(output, tree):
    outfile = open(output, 'wb')
    tree.write(outfile, pretty_print=True)

def sortelements(element):
    children = list(element)
    if (len(children) > 0):
        for child in children:
            sortelements(child)

    sortbytag(children)
    element[:] = [child for child in children]

def addemptychild(tree, element):
    etree.SubElement(element, "nothingHere")

def addemptychildren(tree, element):
    children = list(element)
    for child in children:
        addemptychildren(tree, child)
    if (len(children) == 0):
        addemptychild(tree, element)
    else:
        element[:] = [child for child in children]

def renamebifluxkeywords(element):
    if (element.tag == 'data'):
        element.tag = 'android-data'
    children = list(element)
    for child in children:
        renamebifluxkeywords(child)

def removeemptychildren(tree, element):
    children = list(element)
    for child in children:
        if (child.tag == "nothingHere"):
            children.remove(child)
        else:
            removeemptychildren(tree, child)
    element[:] = [child for child in children]

def renamekeywordstoandroid(element):
    if (element.tag == 'android-data'):
        element.tag = 'data'
    children = list(element)
    for child in children:
        renamekeywordstoandroid(child)

def name_attr_to_elt(element):
    """Turns a name attribute into a child element"""
    pass

def name_elt_to_attr(element):
    """Turns a child name element into an attribute"""
    pass

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--forward",
                    help="transform AndroidManifest to BiFluX-ready manifest",
                    action="store_true")
parser.add_argument("-b", "--backward",
                    help="transform BiFluX-ready manifest to AndroidManifest",
                    action="store_true")
parser.add_argument("input", help="input file")
parser.add_argument("output", help="output file")
args = parser.parse_args()

if args.forward == args.backward:
    print("Select either forward or backward transformation")
    quit()
if not(isfile(args.input)):
    print("Input file does not exist")
    quit()

tree = etree.parse(args.input)
root = tree.getroot()

if args.forward:
    addemptychildren(tree, root)
    renamebifluxkeywords(root)
    sortelements(root)

elif args.backward:
    removeemptychildren(tree, root)
    renamekeywordstoandroid(root)

write(args.output, tree)
