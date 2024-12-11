#!/usr/bin/env python3

import logging
import re
from typing import List

logging.basicConfig()
log = logging.getLogger("vercompare")
log.setLevel(level=logging.INFO)

remap = {"rc": "-1", "beta": "-2", "alpha": "-3"}

needs_remap = re.compile(r"[A-Za-z-]+")


class Version:
    def __init__(self, version: List, comparable: bool):
        self.version = version
        self.comparable = comparable

        if not comparable:
            self.remap()

    def __str__(self):
        return ".".join(self.version)

    def len(self):
        return len(self.version)

    def extend(self, num):
        step = 0
        while step < num:
            self.version.append("0")
            step += 1

    def remap(self):
        i = 0
        while i < self.len():
            if self.version[i] in remap:
                log.debug(f"remapping {self.version[i]} to {remap[self.version[i]]}")
                self.version[i] = remap[self.version[i]]

            if len(self.version[i]) == 1 and self.version[i].isalpha():
                self.version[i] = _convert_character(self.version[i])

            i += 1


class ConversionException(Exception):
    def __init__(self, message):
        super().__init__(f"{message}")


def _convert_character(char: str) -> str:
    if len(char) != 1:
        raise ConversionException(f"got {len(char)} characters but needed 1")

    # We dont' need different conversions for upper and lower case
    char = char.lower()
    max_value = None
    if ord(char) >= ord("a") and ord(char) <= ord("z"):
        max_value = ord("z") + 1
    if max_value is None:
        raise ConversionException(f"{char} is out of range for conversion")

    # build a negative index where 'a' = -26, and 'z' = -1
    converted = (max_value - ord(char)) * -1
    log.debug(f"{char} converted to {converted}")

    # casting to str- the numerical comparisons will casts automatically, but
    # this is to preserve the .join('.) functionalit in the __str__ method
    return str(converted)


def _normalize(raw: str) -> Version:
    comparable = None
    norm = raw.lower().replace("rc", "rc-")
    norm = norm.lower().replace("-", ".")
    # replace characters with remap
    if needs_remap.search(norm):
        comparable = False
        log.debug(f"{norm} needs remapping")
    else:
        comparable = True
        log.debug(f"{norm} is ready to compare")

    parts = norm.split(".")
    ver = Version(parts, comparable)
    return ver


def _compare_states(version: str, fix: str, no_fix_ver: bool = False) -> bool:
    nver = _normalize(version)
    nfix = _normalize(fix)
    if nver.len() != nfix.len():
        if nver.len() > nfix.len():
            nfix.extend(nver.len() - nfix.len())
        else:
            nver.extend(nfix.len() - nver.len())

    if not no_fix_ver and nfix.version == nver.version:
        log.debug(f"version and fix are equal: {nver}, {nfix}")
        return True

    fixed = True

    i = 0
    while i < nfix.len():
        log.debug(f"Comparing version: {nver.version[i]} to fix: {nfix.version[i]}")
        if nver.version[i] < nfix.version[i]:
            log.debug(f"version less than fix: {nver}, {nfix}")
            fixed = False
            break
        i += 1

    if no_fix_ver and nfix.version == nver.version:
        log.debug(f"version equals fix, and fix is vuln: {nver}, {nfix}")
        fixed = False

    return fixed


def is_fixed(version: str, fix: str) -> bool:
    return _compare_states(version, fix)


def is_vuln(version: str, fix: str) -> bool:
    return not _compare_states(version, fix)


def vuln_no_fix(version: str, max_vuln_unfixed: str) -> bool:
    """
    use this function when the maximum published version is still vulnerable and
    the fixed version number is unknown.
    """
    return _compare_states(version, max_vuln_unfixed, no_fix_ver=True)


if __name__ == "__main__":
    ver = "1.2.3-rc1.1.a.0.1"
    fix = "1.2.3-rc1-1.a.0.1"
    print(is_fixed(ver, fix))
    print(vuln_no_fix(ver, fix))
