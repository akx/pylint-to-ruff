import argparse
import io

from pylint_to_ruff.pylint import get_pylint_message_control_output
from pylint_to_ruff.ruff import get_ruffverse


def cli(*, argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "wd",
        type=str,
        help="Working directory",
        default=".",
        nargs="?",
    )
    ap.add_argument(
        "--no-explain",
        action="store_true",
        default=False,
        help="Don't print explanation comments",
    )
    ap.add_argument(
        "--no-unsupported",
        action="store_true",
        default=False,
        help="Don't print commented-out unsupported rules",
    )
    ap.add_argument(
        "--pylint-bin",
        type=str,
        default="pylint",
        help="Full path to pylint if not on path",
    )

    args = ap.parse_args(argv)
    wd = args.wd
    pmc = get_pylint_message_control_output(wd, args.pylint_bin)
    ruffverse = get_ruffverse()
    config = get_ruff_config_segment(
        pmc,
        ruffverse,
        explain=not args.no_explain,
        print_unsupported=not args.no_unsupported,
    )
    print(config)


def _format_rule(code: str, explanation: str, *, commented_out: bool = False, explain: bool) -> str:
    if not explain:
        explanation = ""
    line = f'"{code}",'
    if explanation:
        line += f"  # {explanation}"
    if commented_out:
        line = f"# {line}"
    return f"  {line}"


def get_ruff_config_segment(pmc, ruffverse, *, explain: bool, print_unsupported: bool) -> str:
    sio = io.StringIO()
    for name, m_set in [
        ("extend-select", pmc.enabled),
        ("ignore", pmc.disabled),
    ]:
        if not m_set:
            continue
        print(f"{name} = [", file=sio)
        for m in sorted(m_set, key=lambda m: m.code):
            pl_code = f"PL{m.code}"
            ruff_codes = ruffverse.get_ruff_equivalent_codes(m)
            if ruff_codes:
                for ruff_code in sorted(ruff_codes):
                    print(_format_rule(ruff_code, m.name, explain=explain), file=sio)
            else:
                if not print_unsupported:
                    continue
                print(_format_rule(pl_code, m.name, commented_out=True, explain=explain), file=sio)
        print("]\n", file=sio)
    return sio.getvalue()
