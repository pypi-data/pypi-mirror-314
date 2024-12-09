# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2024 Michał Góral.


import argparse
import logging as log
import sys
from decimal import Decimal, DecimalException
from functools import singledispatch
from typing import List

from i3ipc import Connection

from i3a import __version__ as version

DEFAULT_SCALES = "1,1.25,1.5,1.75,2"


def prepare_args():
    parser = argparse.ArgumentParser(
        description="i3a-scale-cycle - cycle defined list of scale factors"
    )

    excl = parser.add_mutually_exclusive_group()

    excl.add_argument("--next", action="store_true", help="cycle to the next scale")
    excl.add_argument("--prev", action="store_true", help="cycle to the previous scale")

    parser.add_argument(
        "-f",
        "--scale-factors",
        default=DEFAULT_SCALES,
        help=f"comma-separated list of scale factors which will be cycled; default: {DEFAULT_SCALES}",
    )
    parser.add_argument(
        "-o",
        "--outputs",
        action="append",
        default=[],
        help="list of outputs; can be used many times; default: all available outputs",
    )

    return parser.parse_args()


def parse_scales(scales: str) -> List[Decimal]:
    ret = []
    err = False
    for factor in scales.split(","):
        try:
            ret.append(Decimal(factor.strip()))
        except (ValueError, DecimalException):
            log.error("Invalid scale factor: '%s'", factor)
            err = True

    if not ret:
        log.error("No scale factors set")
        err = True

    if err:
        sys.exit(1)

    return ret


def advance_scale(scales: List[Decimal], current: Decimal, n: int) -> Decimal:
    try:
        i = scales.index(current)
    except ValueError:
        return scales[0]

    return scales[(i + n) % len(scales)]


@singledispatch
def to_dec(n):
    return Decimal(n)


@to_dec.register
def _(f: float):
    # This preserves 3 numbers of precision, without all of the fuckupery when we pass
    # ordinary float to Decimal() constructor. For the record, i3/sway report floats
    # in the output of "get_output" message.
    return Decimal(int(f * 1000)) / 1000


def get_current_scales(i3: Connection):
    return {
        outp.name: to_dec(outp.scale)
        for outp in i3.get_outputs()
        if outp.scale is not None
    }


def main():
    log.basicConfig(format="%(message)s", level=log.INFO)
    args = prepare_args()

    i3 = Connection()
    current = get_current_scales(i3)
    args.outputs = args.outputs or current.keys()

    err = 0
    if args.next or args.prev:
        scales = parse_scales(args.scale_factors)
        n = 1 if args.next else -1

        for outp in args.outputs:
            try:
                scale = current.get(outp, Decimal("1.0"))
            except KeyError:
                log.error("No such output: %s", outp)
                err = 1

            next_scale = advance_scale(scales, scale, n)
            log.debug(f"Setting {outp} to {str(next_scale)}")
            i3.command(f"output {outp} scale {str(next_scale)}")

        # update cache
        current = get_current_scales(i3)

    for outp in args.outputs:
        try:
            scale = current[outp]
        except KeyError:
            scale = "unknown output"
            err = 1

        print(f"{outp}: {scale}")

    return err
