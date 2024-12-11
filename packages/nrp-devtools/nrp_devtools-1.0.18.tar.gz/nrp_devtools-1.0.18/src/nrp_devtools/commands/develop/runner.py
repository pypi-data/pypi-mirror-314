import os
import shutil
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Optional

import click
import psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from nrp_devtools.commands.ui.assets import load_watched_paths
from nrp_devtools.commands.ui.link_assets import copy_assets_to_webpack_build_dir
from nrp_devtools.config import OARepoConfig


class Runner:
    python_server_process: Optional[subprocess.Popen] = None
    webpack_server_process: Optional[subprocess.Popen] = None
    file_copier: Optional["FileCopier"] = None

    def __init__(self, config: OARepoConfig):
        self.config = config

    def start_python_server(self, development_mode=False):
        click.secho("Starting python server", fg="yellow")
        environment = {}
        if development_mode:
            environment["FLASK_DEBUG"] = "1"
            environment["INVENIO_TEMPLATES_AUTO_RELOAD"] = "1"
        self.python_server_process = subprocess.Popen(
            [
                self.config.invenio_command,
                "run",
                "--cert",
                self.config.repository_dir / "docker" / "development.crt",
                "--key",
                self.config.repository_dir / "docker" / "development.key",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ, **environment},
            pipesize=100000,
        )
        self.python_reader_thread = threading.Thread(
            target=self._read_python_output, daemon=True
        )
        self.python_reader_thread.start()
        for i in range(5):
            time.sleep(2)
            if self.python_server_process.poll() is not None:
                click.secho(
                    "Python server failed to start. Fix the problem and type 'server' to reload",
                    fg="red",
                )
                self.python_server_process.wait()
                self.python_server_process = None
                time.sleep(10)
                break
        click.secho("Python server started", fg="green")

    def start_webpack_server(self):
        click.secho("Starting webpack server", fg="yellow")
        manifest_path = (
            self.config.invenio_instance_path / "static" / "dist" / "manifest.json"
        )
        if manifest_path.exists():
            manifest_path.unlink()

        self.webpack_server_process = subprocess.Popen(
            [
                "npm",
                "run",
                "start",
            ],
            cwd=self.config.invenio_instance_path / "assets",
            pass_fds=(sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno()),
        )
        # wait at most a minute for webpack to start
        for i in range(60):
            time.sleep(2)
            if self.webpack_server_process.poll() is not None:
                click.secho(
                    "Webpack server failed to start. Fix the problem and type 'ui' to reload",
                    fg="red",
                )
                self.webpack_server_process.wait()
                self.webpack_server_process = None
                time.sleep(10)
                break

            if manifest_path.exists():
                manifest_data = manifest_path.read_text()
                if '"status": "done"' in manifest_data:
                    click.secho("Webpack server is running", fg="green")
                    break
        click.secho("Webpack server started", fg="green")

    def start_file_watcher(self):
        click.secho("Starting file watcher", fg="yellow")
        self.file_copier = FileCopier(self.config)
        click.secho("File watcher started", fg="green")

    def stop(self):
        self.stop_python_server()
        self.stop_webpack_server()
        self.stop_file_watcher()

    def restart_python_server(self, development_mode=False):
        try:
            self.stop_python_server()
            self.start_python_server(development_mode=development_mode)
        except:
            traceback.print_exc()

    def restart_webpack_server(self):
        try:
            self.stop_webpack_server()
            self.stop_file_watcher()
            # just for being sure, link assets
            # (they might have changed and were not registered before)
            copy_assets_to_webpack_build_dir(self.config)
            self.start_file_watcher()
            self.start_webpack_server()
        except:
            traceback.print_exc()

    def stop_python_server(self):
        click.secho("Stopping python server", fg="yellow")
        if self.python_server_process:
            self.python_server_process.terminate()
            try:
                self.python_server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                click.secho(
                    "Python server did not stop in time, killing it", fg="yellow"
                )
                self._kill_process_tree(self.python_server_process)
            self.python_server_process = None

    def stop_webpack_server(self):
        click.secho("Stopping webpack server", fg="yellow")
        if self.webpack_server_process:
            self.webpack_server_process.terminate()
            try:
                self.webpack_server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                click.secho(
                    "Webpack server did not stop in time, killing it", fg="yellow"
                )
                self._kill_process_tree(self.webpack_server_process)
            self.webpack_server_process = None

    def stop_file_watcher(self):
        click.secho("Stopping file watcher", fg="yellow")
        if self.file_copier:
            self.file_copier.join()
            self.file_copier = None

    def _kill_process_tree(self, process_tree: subprocess.Popen):
        parent_pid = process_tree.pid
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()

    def _read_python_output(self):
        while True:
            try:
                if (
                    not self.python_server_process
                    or not self.python_server_process.stdout
                ):
                    break
                line: bytes = self.python_server_process.stdout.readline()
                if line:
                    for r in range(5):
                        try:
                            sys.stdout.buffer.write(line)
                        except:
                            time.sleep(0.1)
                            continue
                        try:
                            sys.stdout.buffer.flush()
                            break
                        except:
                            time.sleep(0.1)
            except:
                break


class FileCopier:
    class Handler(FileSystemEventHandler):
        def __init__(self, source_path: Path, target_path: Path, watcher):
            self.source_root_path = source_path
            self.target_root_path = target_path
            self.watcher = watcher
            print(f"Watching {source_path} -> {target_path}")

        def on_closed(self, event):
            if event.is_directory:
                return

            try:
                time.sleep(0.01)
                self.copy_file(event.src_path, self.make_target_path(event.src_path))
            except:
                traceback.print_exc()

        def on_modified(self, event):
            if event.is_directory:
                return

            try:
                time.sleep(0.1)
                self.copy_file(event.src_path, self.make_target_path(event.src_path))
            except:
                traceback.print_exc()

        def on_moved(self, event):
            try:
                time.sleep(0.01)
                self.remove_file(event.src_path, self.make_target_path(event.src_path))
                self.copy_file(event.dest_path, self.make_target_path(event.dest_path))
            except:
                traceback.print_exc()

        def on_created(self, event):
            """When a new directory is created, add a watch for it"""
            if event.is_directory:
                self.watcher.schedule(
                    type(self)(
                        event.src_path,
                        self.make_target_path(event.src_path),
                        self.watcher,
                    ),
                    event.src_path,
                    recursive=True,
                )

        def on_deleted(self, event):
            try:
                time.sleep(0.01)
                self.remove_file(event.src_path, self.make_target_path(event.src_path))
            except:
                traceback.print_exc()

        def make_target_path(self, source_path):
            return self.target_root_path / Path(source_path).relative_to(
                self.source_root_path
            )

        def copy_file(self, source_path, target_path):
            if str(source_path).endswith("~"):
                return
            print(f"Copying {source_path} to {target_path}")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(source_path, target_path)

        def remove_file(self, source_path, target_path):
            print(f"Removing {target_path}")
            if target_path.exists():
                target_path.unlink()

    def __init__(self, config):
        self.config = config
        static = (config.ui_dir / "static").resolve()

        self.watched_paths = load_watched_paths(
            config.invenio_instance_path / "watch.list.json",
            [f"{static}=static"],
        )
        print(self.watched_paths)

        self.watcher = Observer()
        static_target_path = self.config.invenio_instance_path / "static"
        assets_target_path = self.config.invenio_instance_path / "assets"

        for path, kind in self.watched_paths.items():
            path = Path(path).resolve()
            if not path.exists():
                click.secho(f">>>> Watcher error:", fg="red")
                click.secho(f">>>>", fg="red")
                click.secho(
                    f">>>> Path {path} does not exist, will not watch it!", fg="red"
                )
                click.secho(f">>>>", fg="red")
                click.secho(f">>>>", fg="red")
                continue

            if kind == "static":
                self.watcher.schedule(
                    self.Handler(path, static_target_path, self.watcher),
                    str(path),
                    recursive=True,
                )
            elif kind == "assets":
                self.watcher.schedule(
                    self.Handler(path, assets_target_path, self.watcher),
                    str(path),
                    recursive=True,
                )
        self.watcher.start()

    def join(self):
        try:
            self.watcher.stop()
            self.watcher.join(10)
        except:
            print("Could not stop watcher thread but continuing anyway")
