import argparse
import os
import sys

import pytest

import echoes_menu_mod_gui
from echoes_menu_mod_gui.gui import qt


def create_subparsers(root_parser):
    qt.create_subparsers(root_parser)


def _print_version(args):
    print("Menu Mod GUI {} from {}".format(
        echoes_menu_mod_gui.VERSION,
        os.path.dirname(echoes_menu_mod_gui.__file__)))


def _create_parser():
    parser = argparse.ArgumentParser()
    create_subparsers(parser.add_subparsers(dest="game"))
    parser.add_argument("--version", action="store_const",
                        const=_print_version, dest="func")
    return parser


def _run_args(args):
    if getattr(args, "func", None) is None:
        args.func = qt.run
    args.func(args)


def run_pytest(argv):
    sys.exit(pytest.main(argv[2:], plugins=[]))


def run_cli(argv):
    if len(argv) > 1 and argv[1] == "--pytest":
        run_pytest(argv)
    else:
        _run_args(_create_parser().parse_args(argv[1:]))
