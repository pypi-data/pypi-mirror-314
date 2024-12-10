# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Oxford Quantum Circuits Ltd
import argparse
import os.path
import sys
from getpass import getpass

from compiler_config.config import CompilerConfig

from qcaas_client.client import OQCClient, QPUTask


class OQCCommands:
    parser = argparse.ArgumentParser(
        description="OQC Cloud Client CLI.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-u", "--url", default="http://localhost:4000")
    parser.add_argument("-t", "--auth_token", help="Authentication token.")
    parser.add_argument("-q", "--qpu_id", type=str, default=None)

    subparsers = parser.add_subparsers(dest="command", help="Command to execute.")
    _run_qasm = subparsers.add_parser(
        "run_qasm",
        help="Submit and run QASM file on OQC Cloud.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _run_qasm.add_argument("-p", "--path", default=os.getcwd())
    _run_qasm.add_argument("-f", "--file", action="append", default=[])
    _run_qasm.add_argument("-s", "--shots", type=int, default=1000)
    _run_qasm.add_argument(
        "-o",
        "--output",
        default="BinaryCount",
        choices=["Raw", "Binary", "BinaryCount"],
    )

    basic_qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
rx(0.01) q[0];
measure q[0]->c[0];
"""

    def __init__(self, args):
        self.args = self.validate_run(args)
        self.qc = OQCClient(
            url=self.args.url, authentication_token=self.args.auth_token
        )

    @staticmethod
    def read_program(program_filename):
        if not os.path.exists(program_filename):
            raise ValueError(f"{program_filename} doesn't exist as a path.")

        with open(program_filename, "r") as f:
            program = f.read()
        return program

    def run_qasm(self, args):
        tasks = []  # an array of {program, metadata} objects that define a TASK

        config = CompilerConfig()
        config.results_format.binary_count()
        if args.output == "Binary":
            config.results_format.binary()
        elif args.output == "Raw":
            config.results_format.raw()

        config.repeats = args.shots
        for filename in args.file:
            program = OQCCommands.read_program(os.path.join(args.path, filename))
            tasks.append(QPUTask(program, config))

        # If we have no tasks just default with a very basic QASM program.
        if not any(tasks):
            tasks.append(QPUTask(OQCCommands.basic_qasm, config))

        sys.stdout.write("Executing tasks...\n")
        results = self.qc.execute_tasks(tasks, qpu_id=args.qpu_id)
        for res in results:
            if res.has_errored():
                sys.stdout.write(str(res.error_details.error_message) + "\n")
            else:
                sys.stdout.write(str(res.result) + "\n")

    @staticmethod
    def validate_run(args):
        if args.command is None:
            args.command = "run_qasm"
            args.path = getattr(args, "path", os.path.dirname(__file__))
            args.file = getattr(args, "file", [])
            args.shots = getattr(args, "shots", 1000)
            args.output = getattr(args, "output", "BinaryCount")
            args.qpu_id = getattr(args, "qpu_id", None)

        if args.auth_token is None:
            args.auth_token = getpass("Auth Token: ")

        return args


def run(args):
    oqc_commands = OQCCommands(args)

    sys.stdout.write(f"Attempting to connect to {args.url}\n")
    if args.command == "run_qasm":
        oqc_commands.run_qasm(args=args)
    else:
        args.print_help()


def main():
    args = OQCCommands.parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
