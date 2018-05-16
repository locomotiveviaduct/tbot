"""
Testcase to setup a toolchain environment
-----------------------------------------
"""
import typing
import tbot
from tbot import tc

@tbot.testcase
def toolchain_get(tb: tbot.TBot, *, name: typing.Optional[str] = None) -> tc.Toolchain:
    """
    Get a toolchain and ensure it exists

    :param name: Name of the toolchain, defaults to ``tb.config["board.toolchain"]``
    :type name: str
    :returns: The toolchain meta object to be passed to testcases that need a toolchain
    :rtype: Toolchain
    """
    name = name or tb.config["board.toolchain"]
    if tb.config[f"toolchains.{name}", None] is None:
        raise tc.UnknownToolchainException(repr(name))
    tbot.log.debug(f"Toolchain '{name}' exists")
    return tc.Toolchain(name)

@tbot.testcase
def toolchain_env(tb: tbot.TBot, *,
                  toolchain: tc.Toolchain,
                  and_then: typing.Union[str, typing.Callable],
                  params: typing.Optional[typing.Dict[str, typing.Any]] = None) -> None:
    """
    Setup a toolchain environment and call a testcase inside

    :param toolchain: Which toolchain to use
    :type toolchain: Toolchain
    :param and_then: What testcase to call inside the env
    :type and_then: str or typing.Callable
    :param params: Parameters for the testcase
    :type params: dict
    """
    if params is None:
        params = dict()

    # We don't need to check if the toolchain exists because it has to
    # (You can't create a Toolchain() object without it existing)

    toolchain_script = tb.config[f"toolchains.{toolchain}.env_setup_script"]

    tbot.log.debug(f"Setting up '{toolchain}' toolchain")

    tbot.log.doc(f"""Setup the `{toolchain}` toolchain by calling its env script:
""")

    # Create an env shell
    with tb.machine(tbot.machine.MachineLabEnv()) as tb:
        tb.shell.exec0(f"unset LD_LIBRARY_PATH")
        tb.shell.exec0(f"source {toolchain_script}")

        tb.call(and_then, **params)
