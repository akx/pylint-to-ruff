import dataclasses
import json
import subprocess
from functools import cached_property

from pylint_to_ruff.pylint import PylintMessage
from pylint_to_ruff.ruff_aliases import RUFF_ALIASES


@dataclasses.dataclass(frozen=True)
class Ruffverse:
    rules: dict[str, dict] = dataclasses.field(default_factory=dict)

    @cached_property
    def known_pylint_rules_by_code(self) -> dict[str, dict]:
        return {code[2:]: rule for code, rule in self.rules.items() if code.startswith("PL")}

    @cached_property
    def name_to_code(self) -> dict[str, str]:
        return {rule["name"]: code for code, rule in self.rules.items()}

    def get_ruff_equivalent_codes(self, m: PylintMessage) -> set[str]:
        pl_code = f"PL{m.code}"
        if pl_code in self.known_pylint_rules_by_code:
            return {pl_code}
        if m.name in self.name_to_code:
            return {self.name_to_code[m.name]}
        if pl_code in RUFF_ALIASES:
            return RUFF_ALIASES[pl_code]
        return set()


def get_ruffverse() -> Ruffverse:
    rules_output = subprocess.check_output(
        ["ruff", "rule", "--output-format=json", "--all"],
        encoding="utf-8",
    )
    rules = {rule["code"]: rule for rule in json.loads(rules_output)}
    return Ruffverse(rules=rules)
