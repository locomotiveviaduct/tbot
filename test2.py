import typing
import tbot
from tbot.machine import linux


@tbot.testcase
def foo_bar() -> None:
    with tbot.acquire_lab() as lh:
        lh.exec0("lsb_release", "-a")


@tbot.testcase
def test_imports() -> None:
    with tbot.acquire_lab() as lh:
        path = linux.Path(lh, "/tmp")

        lh.exec0("ls", path)
        lh.exec0("readlink", "-f", lh.workdir)

        with tbot.acquire_board(lh) as bd:
            with tbot.acquire_uboot(bd) as ub:
                ub.tmp_cmd("version")
                tbot.log.message(f"{ub!r}")


@tbot.testcase
def reentrant() -> None:
    tbot.log.message("Calling clean ...")
    reentrant_pattern()

    tbot.log.message("Calling nested ...")
    with tbot.acquire_lab() as lh:
        reentrant_pattern(lh)


@tbot.testcase
def reentrant_pattern(
    lh: typing.Optional[linux.LabHost] = None,
) -> None:
    with lh or tbot.acquire_lab() as lh:
        lh.exec0("lsb_release", "-a")


if __name__ == "__main__":
    test_imports()
