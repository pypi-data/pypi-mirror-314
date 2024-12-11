import os
import subprocess
import sys
import traceback
from functools import wraps
from pathlib import Path
from typing import Callable, Union

import caseconverter
import click
from cookiecutter.main import cookiecutter

from nrp_devtools.config import OARepoConfig


def run_cookiecutter(
    output_dir,
    template: Path,
    extra_context=None,
):
    cookiecutter(
        str(template),
        no_input=True,
        extra_context=extra_context,
        overwrite_if_exists=False,
        output_dir=output_dir,
        # keep_project_on_failure=False,
    )


def run_cmdline(
    *cmdline,
    cwd=".",
    environ=None,
    check_only=False,
    grab_stdout=False,
    grab_stderr=False,
    discard_output=False,
    raise_exception=False,
    no_input=False,
    no_environment=False,
):
    if no_environment:
        env = {
        }
    else:
        env = os.environ.copy()

    for k, v in OARepoConfig.global_environment().items():
        if k not in env:
            env[k] = v

    for k, v in (environ or {}).items():
        if v is None:
            env.pop(k, None)
        else:
            env[k] = v

    cwd = Path(cwd).absolute()
    cmdline = [str(x) for x in cmdline]

    click.secho(f"Running {' '.join(cmdline)}", fg="blue", err=True)
    click.secho(f"    inside {cwd}", fg="blue", err=True)

    try:
        kwargs = {}
        if no_input:
            kwargs["stdin"] = subprocess.DEVNULL
        if grab_stdout or grab_stderr or discard_output:
            if grab_stdout or discard_output:
                kwargs["stdout"] = subprocess.PIPE
            if grab_stderr or discard_output:
                kwargs["stderr"] = subprocess.PIPE

            ret = subprocess.run(
                cmdline,
                check=True,
                cwd=cwd,
                env=env,
                **kwargs,
            )
            ret = (ret.stdout or b"") + b"\n" + (ret.stderr or b"")
        else:
            ret = subprocess.call(cmdline, cwd=cwd, env=env, **kwargs)
            if ret:
                raise subprocess.CalledProcessError(ret, cmdline)
    except subprocess.CalledProcessError as e:
        if check_only:
            return False
        click.secho(f"Error running {' '.join(cmdline)}", fg="red", err=True)
        if e.stdout:
            click.secho(e.stdout.decode("utf-8"), fg="red", err=True)
        if e.stderr:
            click.secho(e.stderr.decode("utf-8"), fg="red", err=True)
        if raise_exception:
            raise
        sys.exit(e.returncode)

    click.secho(f"Finished running {' '.join(cmdline)}", fg="green", err=True)
    click.secho(f"    inside {cwd}", fg="green", err=True)

    if grab_stdout:
        return ret.decode("utf-8").strip()

    return True


def call_pip(venv_dir, *args, **kwargs):
    return run_cmdline(
        venv_dir / "bin" / "pip",
        *args,
        **{
            "raise_exception": True,
            "no_environment": True,
            **kwargs,
        },
    )


def install_python_modules(config, venv_dir, *modules):
    run_cmdline(
        os.environ.get("PYTHON", config.python),
        "-m",
        "venv",
        str(venv_dir),
        cwd=config.repository_dir,
        raise_exception=True,
        no_environment=True,
    )

    call_pip(
        venv_dir,
        "install",
        "-U",
        "--no-input",
        *modules,
        no_environment=True,
        raise_exception=True,
    )


def run_steps(config, steps, step_commands, continue_on_errors=False):
    steps = steps or []
    steps = [x.strip() for step in steps for x in step.split(",") if x.strip()]
    errors = []
    for idx, fun in enumerate(step_commands):
        function_name = fun.__name__
        if not steps or function_name in steps or str(idx + 1) in steps:
            try:
                fun(config=config)
            except KeyboardInterrupt:
                raise
            except BaseException as e:
                if continue_on_errors:
                    errors.append(e)
                else:
                    raise
    if errors:
        raise errors[0]


def make_step(
    fun,
    *global_args,
    _if: Union[bool, Callable[[OARepoConfig], bool]] = True,
    _swallow_errors=False,
    name=None,
    **global_kwargs,
):
    @wraps(fun)
    def step(config, **kwargs):
        should_call = _if if not callable(_if) else _if(config)
        if should_call:
            try:
                fun(config, *global_args, **global_kwargs, **kwargs)
            except KeyboardInterrupt:
                raise
            except BaseException as e:
                if _swallow_errors:
                    click.secho(
                        f"Error running {fun.__name__}: {e}", fg="red", err=True
                    )
                else:
                    raise
    if name:
        step.__name__ = name
    return step


def no_args(fun, name=None):
    @wraps(fun)
    def _no_args(*args, **kwargs):
        fun()
    _no_args.__name__ = name or getattr(fun, "__name__", "no_args")

    return _no_args


def run_fixup(check_function, fix_function, fix=True, name=None, **global_kwargs):
    @wraps(check_function)
    def _run_fixup(config, **kwargs):
        try:
            check_function(
                config, fast_fail=True, will_fix=fix, **kwargs, **global_kwargs
            )
        except:
            if global_kwargs.get("verbose"):
                traceback.print_exc()
            if not fix:
                raise
            fix_function(config, **kwargs, **global_kwargs)
            check_function(
                config, fast_fail=False, will_fix=False, **kwargs, **global_kwargs
            )
    if name:
        _run_fixup.__name__ = name
    return _run_fixup


def capitalize_name(name):
    capitalized_name = caseconverter.camelcase(name)
    return capitalized_name[0].upper() + capitalized_name[1:]
