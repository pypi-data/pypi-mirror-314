from typer import Typer
from typer.params import Argument, Option

from ..config.load import load_config, read_json_config, write_json_config
from ..config.types import Alias, Config
from ..utils.cmd import print_command
from ..utils.console import console
from ..utils.helpers import wrap_raw_config
from ..utils.path import global_store, local_store

app = Typer()


@app.command(help="Manage command aliases.")
def alias(
    alias: str = Argument("", help="The alias to create or retrieve."),
    command: str = Argument("", help="The command to alias."),
    shell: bool = Option(False, "--shell", "-s", flag_value=True, help="Use shell to execute the command."),
    local: bool = Option(True, "--global", "-g", flag_value=False, help="Persistent alias in User's home directory instead of this python venv.", show_default=False),
):
    store = local_store if local else global_store
    config = wrap_raw_config(read_json_config(store)) if command else load_config()  # merge unless the verb is set

    match (alias, command):
        case ("", ""):
            if aliases := config["aliases"]:
                max_len = max(map(len, aliases))
                print()
                for alias, item in aliases.items():
                    if isinstance(item, dict):
                        cmd, shell = item["cmd"], item["shell"]
                    else:
                        cmd, shell = item, False
                    console.print(f" {alias.rjust(max_len)}: [{'green' if shell else 'blue' }]{cmd}")
                print()

        case (alias, ""):
            if isinstance(item := config["aliases"][alias], str):
                print_command(item)
            elif isinstance(item, dict):
                print_command(item["cmd"], item["shell"])

        case (alias, command):
            new_config: Config = dict(config) if isinstance(config, dict) else {}  # type: ignore
            item: Alias | str = {"cmd": command, "shell": shell} if shell else command
            if config["aliases"]:
                new_config["aliases"][alias] = item
            else:
                new_config["aliases"] = {alias: item}
            write_json_config(store, new_config)
