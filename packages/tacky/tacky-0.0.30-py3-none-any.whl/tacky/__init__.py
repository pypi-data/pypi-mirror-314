
import sys
import os
import objc

import argparse

from Foundation import NSString, NSUTF8StringEncoding, NSBundle
from AppKit import NSPasteboard, NSPasteboardItem

def main():
    parser = argparse.ArgumentParser(prog = "tacky")
    subparsers = parser.add_subparsers()

    copy_parser = subparsers.add_parser("copy")
    copy_parser.set_defaults(func = cli_copy)
    copy_parser.add_argument(
            '-i','--item',
            action = 'append',
            nargs = 2,
            metavar = ('uti_type', 'file'),
            help = 'help:')

    paste_parser = subparsers.add_parser("paste")
    paste_parser.set_defaults(func = cli_paste)
    paste_parser.add_argument(
            '-u','--uti',
            action = 'store',
            help = 'help:')

    paste_parser.add_argument(
            '-l','--list',
            action = 'store_true',
            help = 'help:')

    args = parser.parse_args()
    if len(vars(args)) > 0:
        args.func(args)
    else:
        parser.print_help()

# CLI functions, print to stdout

def cli_copy(args):
    copy([(uti_from_argument(e[0]), e[1]) for e in args.item])

def cli_paste(args):
    if args.list:
        cli_list_uti()
    elif args.uti:
        paste(args.uti)

def cli_list_uti():
    uti_types = list_uti()
    for t in uti_types:
        print(t)

# Module methods, used in both CLI and import as module

def copy(entries):
    """
    given a list of uti-path pairs, write the data for each file to the
    pasteboard under the uti type.

    if a file is "-", read its contents from stdin.
    """

    pb = NSPasteboard.generalPasteboard()
    types = [e[0] for e in entries]
    # We're certain this is necessary, no idea why
    pb.declareTypes_owner_(types, None)

    stdin_data = None

    for (uti, path) in entries:
        if path == '-':
            if stdin_data is None:
                stdin_data = sys.stdin.buffer.read()

            write_pasteboard(pb, stdin_data, uti)
        else:
            with open(path, 'rb') as f:
                value = f.read()
                write_pasteboard(pb, value, uti)

def write_pasteboard(pb, value, uti):
    """
    write a specific uti-value pair to the given pb
    """

    pb.setData_forType_(value, uti)

def paste(uti):
    """
    print out the contents of the given UTI from the pasteboard
    """

    uti = uti_from_argument(uti)
    pb = NSPasteboard.generalPasteboard()
    for p in pb.pasteboardItems():
        for t in p.types():
            if t == uti:
                print(p.stringForType_(uti))
                return

def uti_from_argument(uti_type):
    uti_value = uti_type

    # Supports referring to constants in addition to proper types
    # e.g., kUTTypePDF which would map to com.adobe.pdf
    # load the constants from the framework if this is a special apple UTI
    if uti_type.startswith('kUTType') or uti_type.startswith('NSPasteboardType'):
        bundle = NSBundle.bundleWithIdentifier_("com.apple.AppKit")
        objc.loadBundleVariables(bundle, globals(), [(uti_type, b'@')])
        uti_value = globals()[uti_type]

    return uti_value

def list_uti():
    """
    prints out a list of uti types currently on the pb
    """

    pb = NSPasteboard.generalPasteboard()
    return [NSString.stringWithString_(t).nsstring() for p in pb.pasteboardItems() for t in p.types()]

if __name__ == "__main__":
    main()

