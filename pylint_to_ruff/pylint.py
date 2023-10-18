import dataclasses
import os.path
import subprocess
import sys
from collections import namedtuple


class PylintMessage(namedtuple("_PylintMessage", ["name", "code"])):
    pass


@dataclasses.dataclass(frozen=True)
class PylintMessageConfig:
    enabled: set[PylintMessage] = dataclasses.field(default_factory=set)
    disabled: set[PylintMessage] = dataclasses.field(default_factory=set)
    non_emittable: set[PylintMessage] = dataclasses.field(default_factory=set)


def parse_pylint_msg_spec(spec: str) -> PylintMessage:
    name, _, code = spec.strip(")").partition(" (")
    return PylintMessage(name, code)


def get_pylint_message_control_output(working_directory: str, pylint_bin: str) -> PylintMessageConfig:
    pmc = PylintMessageConfig()
    current = None
    command = [pylint_bin, "--list-msgs-enabled"]
    pylintrc_file = os.path.join(working_directory, ".pylintrc")
    if os.path.isfile(pylintrc_file):
        command += ["--rcfile", pylintrc_file]
    for line in subprocess.check_output(
        command,
        cwd=working_directory,
        encoding="utf-8",
    ).splitlines():
        line = line.rstrip()  # noqa: PLW2901
        if not line:
            continue
        if line.startswith("Enabled messages"):
            current = pmc.enabled
            continue
        if line.startswith("Disabled messages"):
            current = pmc.disabled
            continue
        if line.startswith("Non-emittable messages"):
            current = pmc.non_emittable
            continue
        if line.startswith("  "):
            current.add(parse_pylint_msg_spec(line[2:]))
            continue
        else:
            print(f"Unknown line in pylint output: {line!r}", file=sys.stderr)

    return pmc
