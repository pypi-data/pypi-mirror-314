# This file is part of pdu-control
# Copyright (C) 2023 Safran
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import argparse
import configparser
from typing import Dict, List
from tabulate import tabulate
from .__pdu import choose_pdu
import argcomplete.completers
import argparse as ap


config_filepath = os.path.expanduser("~/.config/pducontrol/pdu_settings.cfg")


def get_credentials(args: argparse.Namespace) -> Dict:
    """Returns a username and a password. Checks the parsed arguments and
     then config file.

    Args:
        args: the previously parsed args
    Returns:
        A username/password combo if found, else an empty dict
    """
    if (args.user and args.password) is not None:
        return {"user": args.user, "password": args.password}
    else:
        config = configparser.ConfigParser()
        config.read(config_filepath)
        try:
            section = next(section for section in config.sections()
                           if config.get(section,
                                         "ip_address") == args.ip_address)
            user = config.get(section, "username")
            password = config.get(section, "password")

            return {"user": user, "password": password}

        except Exception:
            return {}


def handle_status(args, pdu) -> None:
    """Handles the status subcommand, outputs a table showing the state of all
    power outlets

    Args:
        args: the parsed command-line arguments
        pdu: a supported pdu class object
    """
    status = pdu.get_all_outlet_statuses()
    names = pdu.get_all_names()

    print(tabulate(zip(names, status), headers=["Unit", "status"]))


def outlet_to_index(names, outlet) -> int:
    """function to convert outlet name into an index allowing designation by
    outlet name in pdu control

    Args:
        names: list of outlet name for a given IP address
        outlet: given command-line argument to convert
    """
    try:
        return names.index(outlet) + 1
    except ValueError:
        try:
            return int(outlet)
        except ValueError:
            exit(f"{outlet} isn't a valid outlet name or index")


def do_handle_set_and_power_cycle(args, pdu, action) -> None:
    """Helper function to ease the implementation of the set and power_cycle
    subcommand handlers

    Keyword Arguments:
    args: the parsed command-line arguments
    pdu: a supported pdu class object
    action: callable performing the action on the targeted outlets
    """
    names = pdu.get_all_names()
    nb = pdu.get_total_outlets()

    for outlet in args.outlets.split(","):
        i = outlet_to_index(names, outlet)
        if i > nb:
            print(
                f"{nb} outlets available, but asked for setting outlet {i} "
                f"to {args.state}. Skipping",
                file=sys.stderr,
            )
            continue
        if i <= 0:
            print(
                f"Outlets are numbered starting from 1, but asked for "
                f"setting outlet {i} to {args.state}. Skipping",
                file=sys.stderr,
            )
            continue
        action(args, pdu, i)


def handle_set(args, pdu) -> None:
    """Handles the set subcommand, sets the state of all the outlets
    specified as arguments

    Keyword Arguments:
    args: the parsed command-line arguments
    pdu: a supported pdu class object
    """

    def action(a, p, o):
        p.toggle_outlet(o, a.state)

    do_handle_set_and_power_cycle(args, pdu, action)


def handle_power_cycle(args, pdu) -> None:
    """Handles the power_cycle subcommand, reboots all the outlets specified
    as arguments

    Keyword Arguments:
    args: the parsed command-line arguments
    pdu: a supported pdu class object
    """
    args.state = "reboot"

    def action(a, p, o):
        p.toggle_outlet(o, a.state)

    do_handle_set_and_power_cycle(args, pdu, action)


def handle_set_all(args, pdu) -> None:
    """Handles the set_all subcommand, changes state of all the outlets

    Args:
        args: the parsed command-line arguments
        pdu: a supported pdu class object
    """
    pdu.toggle_all_outlets(args.state)


def handle_power_cycle_all(args, pdu) -> None:
    """Handles the power_cycle_all subcommand, reboots all the outlets

    Args:
        args: the parsed command-line arguments
        pdu: a supported pdu class object
    """
    pdu.toggle_all_outlets("reboot")


def handle_get_name(args, pdu) -> None:
    """Handles the get_name subcommand, prints the name of the requested outlet

    Args:
        args: the parsed command-line arguments
        pdu: a supported pdu class object
    """
    if args.outlet == "all":
        name = pdu.get_all_names()
        outlets = [
            f"Outlet {i}:" for i in range(1, pdu.get_total_outlets() + 1)
        ]
        print(tabulate(zip(outlets, name), headers=["Outlet", "Name"]))
    else:
        nb = pdu.get_total_outlets()
        if int(args.outlet) > nb:
            print(
                f"{nb} outlets available, but asked for outlet"
                f" {args.outlet}. Skipping",
                file=sys.stderr,
            )
            return None
        name = pdu.get_name(args.outlet)
        outlet = f"Outlet {args.outlet}:"
        print(tabulate(zip([outlet], [name])))


def handle_set_name(args, pdu) -> None:
    """Handles the set_name subcommand, sets the name of the requested outlet

    Args:
        args: the parsed command-line arguments
        pdu: a supported pdu class object
    """
    nb = pdu.get_total_outlets()
    if int(args.outlet) > nb:
        print(
            f"{nb} outlets available, but tried renaming outlet"
            f" {args.outlet}. Skipping",
            file=sys.stderr,
        )
        return None
    print(pdu.set_name(args.outlet, args.name))


def address_completer() -> List:
    """Argcomplete compatible completer function
    Returns a list of IPs from the config file"""
    config = configparser.ConfigParser()
    config.read(config_filepath)
    addresses = [config.get(section, "ip_address") for section in
                 config.sections()]
    return addresses


def complete_prefix(prefix, outlets) -> List:
    """Sub function used by name_completer function

    Args:
        prefix: user prompt before pressing tab
        outlets: outlet's name list

    Return a filtered list of outlet's name
    """
    split_prefix = prefix.split(',')
    pre = (
        ','.join(split_prefix[:-1])+','
        if len(split_prefix) > 1 else '')

    return [pre+outlet for outlet in outlets
            if outlet.startswith(split_prefix[-1])]


def name_completer(prefix, parsed_args, **kwargs) -> List:
    """Argcomplete compatible completer function

    Args:
        prefix: user prompt before pressing tab
        parsed_args : the parsed command-line arguments

    Return a list of outlet's name from given ip address
    """
    pdu = choose_pdu(parsed_args, get_credentials(parsed_args))
    if pdu is None:
        return []
    return complete_prefix(prefix, pdu.get_all_names())


# description for the program arguments parser and subparser, suitable for
# using with get_parser

parser_desc = {
    "description": (
        "Command-line utility for controlling power "
        "delivery units.\n"
        "In all commands, outlets are numbered starting from 1."
    ),
    "arguments": {
        "ip_address": {
            "help": "IP address of the power delivery unit",
        },
        "--user": {"help": "PDU user"},
        "--password": {"help": "PDU password"}
    },
    "completers": {
        "ip_address": argcomplete.completers.ChoicesCompleter(
            address_completer()),
        "outlets": name_completer,
    },
    "subparsers": {
        "help": "sub-command to invoke",
        "dest": "subparser_name",
        "list": {
            "status": {
                "help": "show the status of power outlets",
                "func": handle_status,
            },
            "set": {
                "help": "set the state of a list of outlets",
                "arguments": {
                    "outlets": {
                        "help": "comma-separated list of outlets",
                    },
                    "state": {
                        "help": (
                            "state to set the outlets to, can be one of "
                            "[on, off, reboot]"
                        ),
                        "choices": ["on", "off", "reboot"],
                    },
                },
                "func": handle_set,
            },
            "set_all": {
                "help": "set the state of a all the outlets at once",
                "arguments": {
                    "state": {
                        "help": (
                            "state to set the outlets to, can be one of "
                            "[on, off, reboot]"
                        ),
                        "choices": ["on", "off", "reboot"],
                    },
                },
                "func": handle_set_all,
            },
            "power_cycle": {
                "help": (
                    "set the state of a list of outlets to off, then to " "on"
                ),
                "arguments": {
                    "outlets": {
                        "help": "comma-separated list of outlets",
                    },
                },
                "func": handle_power_cycle,
            },
            "power_cycle_all": {
                "help": "set the state of all the outlets to off, then to on",
                "func": handle_power_cycle_all,
            },
            "get_name": {
                "help": "get the name of an outlet",
                "arguments": {
                    "outlet": {
                        "help": "outlet index or all",
                    },
                },
                "func": handle_get_name,
            },
            "set_name": {
                "help": "set the name of an outlet",
                "arguments": {
                    "outlet": {
                        "help": "outlet index",
                        "type": int,
                    },
                    "name": {
                        "help": "name to set to the outlet",
                    },
                },
                "func": handle_set_name,
            },
        },

    },
}


def get_parser(parser_desc=parser_desc) -> ap.ArgumentParser:
    """Generate an argparse parser out of its description

    Args:
        parser_desc: The description of the parser

    Returns:
        The instantiated parser
    """
    parser = ap.ArgumentParser(
        description=parser_desc["description"],
        formatter_class=ap.RawTextHelpFormatter,
    )
    subparsers = parser_desc["subparsers"]
    if "arguments" in parser_desc:
        for m, a in parser_desc["arguments"].items():
            action = parser.add_argument(m, **a)
            if "completers" in parser_desc and m in parser_desc["completers"]:
                action.completer = parser_desc["completers"][m]
    sp = parser.add_subparsers(
        help=subparsers["help"], dest=subparsers["dest"]
    )
    sp.required = True
    for n, p in subparsers["list"].items():
        subparser = sp.add_parser(n, help=p["help"])
        if "arguments" in p:
            for m, a in p["arguments"].items():
                action = subparser.add_argument(m, **a)
                if (
                    "completers" in parser_desc and
                    m in parser_desc["completers"]
                ):
                    action.completer = parser_desc["completers"][m]
        subparser.set_defaults(func=p["func"])

    return parser
