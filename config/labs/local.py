import pathlib
import getpass
from tbot.config import Config

#pylint: disable=line-too-long
def config(cfg: Config) -> None:
    """ Localhost lab config """
    username = getpass.getuser()
    home = pathlib.Path.home()
    cfg["lab"] = {
        "name": "local",
        "hostname": "localhost",
        "user": username,
        "keyfile": home / ".ssh" / "id_rsa",
    }

    cfg["tbot"] = {
        "workdir": pathlib.PurePosixPath(home) / "tbotdir",
    }

    cfg["tftp"] = {
        "rootdir": pathlib.PurePosixPath("/tmp/tftp"),
        "tbotsubdir": pathlib.PurePosixPath("tbot"),
    }

    cfg["uboot"] = {
        "repository": "git://git.denx.de/u-boot.git",
        "test.use_venv": True,
    }

    # Change this to your sdk location
    sdk_base_path = pathlib.Path.home() / "Documents" / "sdk"
    cfg["toolchains.cortexa8hf-neon"] = {
        "path": sdk_base_path / "sysroots/x86_64-pokysdk-linux" / "usr" / "bin" / "arm-poky-linux-gnueabi",
        "env_setup_script": sdk_base_path / "environment-setup-cortexa8hf-neon-poky-linux-gnueabi",
        "prefix": "arm-poky-linux-gnueabi-",
    }
