from math import log
from string import (
    ascii_letters,
    ascii_lowercase,
    ascii_uppercase,
    digits,
    printable,
    punctuation,
)
import secrets
import argparse
from typing import List


hexdigits = digits + ascii_letters[:6]
Hexdigits = hexdigits.upper()
candidate_dict = {
    "u": ascii_uppercase,
    "l": ascii_lowercase,
    "d": digits,
    "p": punctuation,
    "h": hexdigits,
    "H": Hexdigits,
    "a": printable,
}
candidate_default = ["u", "l", "d"]

candidate = ""
for x in candidate_default:
    candidate += candidate_dict[x]


def strength(length, clen):
    return int(log(clen**length, 2))


def random_string(length, candidate=candidate):
    ret = [secrets.choice(candidate) for _ in range(length)]
    return "".join(ret)


def wash_cddt(cddt: List[str]):
    cddt = sorted(set(cddt))
    exclusive = sorted(["a", "H", "h"])
    for x in exclusive:
        if x in cddt:
            cddt = [x]
            break
    return cddt


def g_candidate(cddt):
    cddt = wash_cddt(cddt)
    candidate_lst = []
    for x in cddt:
        candidate_lst.append(candidate_dict[x])
    candidate = "".join(candidate_lst)
    return candidate


def int2rs(x, candidate=candidate, length=None):
    l = len(candidate)
    ret = []
    while x > 0:
        x, r = divmod(x, l)
        ret.append(candidate[r])
    if length and len(ret) < length:
        lack = length - len(ret)
        ret.append(candidate[0] * lack)
    return "".join(ret[::-1])


def rs2int(rs, candidate=candidate):
    l = len(candidate)
    ret = 0
    weight = 1
    for x in rs[::-1]:
        ret += candidate.index(x) * weight
        weight *= l
    return ret


def add_length(parser):
    parser.add_argument(
        "-l",
        "--length",
        help="length of the generated random string.",
        type=int,
        default=10,
    )


def add_candidate(parser):
    parser.add_argument(
        "-c",
        "--candidate",
        help="""candidate characters,
        u for uppercase,
        l for lowercase,
        d for digist,
        p for punctuation,
        h[H] for hex
        a for all printable.""",
        choices=candidate_dict.keys(),
        nargs="+",
        action="extend",
    )


def add_strength(parser):
    parser.add_argument(
        "-s",
        "--strength",
        help="evaluate the strength of an random string.",
        action="store_true",
    )


def cli_rs2int():
    parser = argparse.ArgumentParser(
        description="""Convert a random string to an integer."""
    )
    parser.add_argument("rs", help="an random string.")
    # add_length(parser)
    add_candidate(parser)
    add_strength(parser)
    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = candidate_default
    # PART generate candidate
    candidate = g_candidate(args.candidate)

    output = []
    # PART rs2int
    x = rs2int(args.rs)
    output.append(f"{x}")

    # PART strength
    if args.strength:
        output.append(f"strength:{strength(args.length,len(candidate))}")

    print("\n".join(output))


def cli_int2rs():
    parser = argparse.ArgumentParser(
        description="""Convert an integer to a random string."""
    )
    parser.add_argument("x", help="integer.", type=int)
    # add_length(parser)
    add_candidate(parser)
    add_strength(parser)
    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = candidate_default
    # PART generate candidate
    candidate = g_candidate(args.candidate)

    output = []
    # PART int2rs
    rs = int2rs(args.x)
    output.append(f"{rs}")

    # PART strength
    if args.strength:
        output.append(f"strength:{strength(args.length,len(candidate))}")

    print("\n".join(output))


def cli_rs():
    parser = argparse.ArgumentParser(description="""generate a secret random string.""")
    add_length(parser)
    add_candidate(parser)
    add_strength(parser)

    args = parser.parse_args()
    if args.candidate is None:
        args.candidate = candidate_default

    # PART generate candidate
    candidate = g_candidate(args.candidate)

    # PART generate an random string
    output = []
    rs = random_string(args.length, candidate)
    output.append(f"{rs}")

    # PART strengt
    if args.strength:
        output.append(f"strength:{strength(args.length,len(candidate))}")

    print("\n".join(output))


if __name__ == "__main__":
    length = 20
    s = random_string(length)
    strength = strength(length, len(candidate))
    print(s, strength)
    print(hexdigits)
    x = rs2int(s)
    y = int2rs(x)
    assert s == y
    print(s, x, y)
