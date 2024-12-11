import os
import select
import sys
import time

import click

from nrp_devtools.config import OARepoConfig

from .runner import Runner


def show_menu(server: bool, ui: bool, development_mode: bool):
    click.secho("")
    click.secho("")
    if development_mode:
        click.secho("Development server is running", fg="green")
    else:
        click.secho("Production server is running", fg="yellow")
    click.secho("")
    click.secho("=======================================")
    click.secho("")
    if server:
        click.secho("1 or server     - restart python server", fg="green")
    if ui and development_mode:
        click.secho("2 or ui         - restart webpack server", fg="green")

    click.secho("0 or stop       - stop the server (Ctrl-C also works)", fg="red")
    click.secho("")
    click.secho("")


def timedInput(prompt, timeout):
    try:
        os.set_blocking(sys.stdin.fileno(), False)

        start_time = time.time()
        print(prompt, end="", flush=True)
        choice = ""
        while True:
            remaining_time = timeout - (time.time() - start_time)
            if remaining_time <= 0:
                return (choice, True)

            is_data = select.select([sys.stdin], [], [], remaining_time) == (
                [sys.stdin],
                [],
                [],
            )

            while is_data:
                for input_char in sys.stdin.read():
                    if input_char in ("\n", "\r"):
                        return (choice, False)
                    else:
                        choice += input_char

                is_data = select.select([sys.stdin], [], [], 0.01) == (
                    [sys.stdin],
                    [],
                    [],
                )

            time.sleep(
                0.5
            )  # sanity check, if the select returns immediately, sleep a bit
    finally:
        os.set_blocking(sys.stdin.fileno(), True)


def run_develop_controller(
    config: OARepoConfig, runner: Runner, server=True, ui=True, development_mode=False
):
    while True:
        show_menu(server, ui, development_mode)
        (choice, timed_out) = timedInput(prompt="Your choice: ", timeout=60)
        if timed_out:
            continue
        choice = choice.strip()
        print("Got choice", choice)
        if choice in ("0", "stop"):
            runner.stop()
            break
        elif choice in ("1", "server"):
            runner.restart_python_server(development_mode=development_mode)
        elif choice in ("2", "ui"):
            runner.restart_webpack_server()
