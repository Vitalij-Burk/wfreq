from src.cli import CLI


def test_short_input():
    cli = CLI()
    args = cli.init_emulator(["-p", "~/code/projects/wfreq", "-rf", "the,here,where", "-f", "5", "-r", "5", "-minl", "3", "-maxl", "10", "-maxr", "3", "-a", "true"])
    assert args.path == "~/code/projects/wfreq"
    assert args.red_flags == "the,here,where"
    assert args.frequent == "5"
    assert args.rare == "5"
    assert args.min_length == "3"
    assert args.max_length == "10"
    assert args.max_repeat == "3"
    assert args.artifacts == "true"


def test_full_input():
    cli = CLI()
    args = cli.init_emulator(["--path", "~/code/projects/wfreq", "--red_flags", "the,here,where", "--frequent", "5", "--rare", "5", "--min_length", "3", "--max_length", "10", "--max_repeat", "3", "--artifacts", "true"])
    assert args.path == "~/code/projects/wfreq"
    assert args.red_flags == "the,here,where"
    assert args.frequent == "5"
    assert args.rare == "5"
    assert args.min_length == "3"
    assert args.max_length == "10"
    assert args.max_repeat == "3"
    assert args.artifacts == "true"

