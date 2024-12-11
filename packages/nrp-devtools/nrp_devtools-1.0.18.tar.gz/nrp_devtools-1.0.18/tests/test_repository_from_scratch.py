import os
import subprocess

from .cmdline import CommandLineTester
import requests


#
# Note: the following tests must be run in the order in which they
# are defined, because they depend on each other.
#


def test_initialization(test_repository_dir):
    with CommandLineTester(
        "./nrp-installer.sh",
        test_repository_dir,
        environment={"LOCAL_NRP_TOOLS_LOCATION": os.getcwd()},
    ) as tester:
        tester.expect("Successfully installed pip")
        tester.expect("Please answer a few questions", timeout=60)

        tester.expect("Human name of the repository")
        tester.enter("Test Repository")
        tester.expect("Python package name of the whole repository")
        tester.enter("test_repository")
        tester.expect("OARepo version to use")
        tester.enter("")
        tester.expect("Python package name of the shared code")
        tester.enter("")
        tester.expect("Python package name of the ui code")
        tester.enter("")
        tester.expect("Your repository is now initialized")
        tester.wait_for_exit(timeout=10)


def test_build(absolute_test_repository_dir):
    subprocess.call(["ls", "-la"], cwd=absolute_test_repository_dir)

    with CommandLineTester(
        absolute_test_repository_dir / "nrp",
        "build",
        cwd=absolute_test_repository_dir,
    ) as tester:
        tester.expect("Building repository for production",
                      timeout=60)
        tester.expect("Successfully built the repository",
                      timeout=2400)


def test_check_requirements(absolute_test_repository_dir):
    with CommandLineTester(
        absolute_test_repository_dir / "nrp",
        "check",
        cwd=absolute_test_repository_dir,
    ) as tester:
        tester.expect("Checking repository requirements", timeout=60)
        tester.expect("Repository ready to be run", timeout=2400)


def test_ui_titlepage_running(absolute_test_repository_dir):
    with CommandLineTester(
        absolute_test_repository_dir / "nrp",
        "run",
        cwd=absolute_test_repository_dir,
    ) as tester:
        tester.expect("Starting python server", timeout=60)
        tester.expect("Python server started", timeout=60)
        data = requests.get('https://127.0.0.1:5000', allow_redirects=True, verify=False)
        data.raise_for_status()
        assert 'Test Repository' in data.text
        assert 'main id="main"' in data.text
        assert 'Powered by' in data.text
