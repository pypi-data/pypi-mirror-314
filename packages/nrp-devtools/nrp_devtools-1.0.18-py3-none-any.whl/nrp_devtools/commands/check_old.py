from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.utils import run_cmdline


def check_imagemagick_callable(config):
    try:
        run_cmdline("convert", "--version", grab_stdout=True, raise_exception=True)
    except:
        check_failed(
            "ImageMagick is not callable. Please install ImageMagick on your system."
        )
