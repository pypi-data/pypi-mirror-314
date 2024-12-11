#
# Copyright (c) 2022 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
#

from .cli import cli


def package_main() -> None:
    cli(prog_name="nrf-regtool")


if __name__ == "__main__":
    package_main()
