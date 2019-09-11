import abc
import contextlib
import typing

from . import machine


class Shell(machine.Machine):
    @abc.abstractmethod
    def _init_shell(self) -> typing.ContextManager:
        """
        Initialize this shell.

        An implementation of this method should return a context manager that,
        when entered, waits for the shell to appear on the channel and sets up
        any necessary options.  This might include deactivating line-editing,
        disabling the history, etc.

        The most comfortable way to implement this is using
        :py:func:`contextlib.contextmanager`:

        .. code-block:: python

            class Shell(tbot.machine.shell.Shell):
                @contextlib.contextmanager
                def _init_shell(self):
                    try:
                        # Wait for shell to appear
                        ...

                        # Setup options
                        ...

                        yield None
                    finally:
                        # Optionally destruct shell
                        ...
        """
        raise NotImplementedError("abstract method")

    @abc.abstractmethod
    def exec(self, *args: typing.Any) -> typing.Any:
        """
        Run a command using this shell.

        This is the only "common" interface tbot expects shells to implement.
        The exact semantics of running commands are up to the implementor.
        This especially includes the return value.

        :param \\*args: ``.exec()`` should take the command as one argument per
            command-line token.  For example:

            .. code-block:: python

                mach.exec("echo", "Hello", "World")

        :returns: The return value should in some way be related to the
            "output" of the command.  For
            :py:class:`~tbot.machine.linux.LinuxShell`, ``exec`` returns a
            tuple of the return code and console output: ``Tuple[int, str]``.
        """
        raise NotImplementedError("abstract method")


class RawShell(machine.Machine):
    """
    Absolute minimum shell implementation.

    :py:class:`RawShell` attempts to be a minimal shell implementation.  It
    does not make any assumptions about the other end.  It is used, for
    example, for raw board-console access which allows debugging before U-Boot
    is fully working.
    """

    @contextlib.contextmanager
    def _init_shell(self) -> typing.Iterator:
        yield None

    def exec(self, *args: str) -> None:
        """
        Just send ``" ".join(args)`` to the machine's channel.

        This minimal ``exec()`` implementation has no way of reading back the
        command output.
        """
        self.ch.sendline(" ".join(args), read_back=True)

    def interactive(self) -> None:
        """
        Connect tbot's stdio to this machine's channel.  This will allow
        interactive access to the machine.
        """
        self.ch.attach_interactive()
