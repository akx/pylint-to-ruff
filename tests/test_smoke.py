from pathlib import Path

from pylint_to_ruff.cli import cli

victim_dir = Path(__file__).parent / "victim"


def test_smoke(monkeypatch, capsys):
    monkeypatch.chdir(victim_dir)
    cli(argv=["--no-unsupported"])
    stdout, stderr = capsys.readouterr()
    assert not stderr
    assert "extend-select = [" in stdout
    assert "ignore = [" in stdout
    try:
        import tomllib
    except ImportError:
        pass
    else:
        assert tomllib.loads(stdout)
