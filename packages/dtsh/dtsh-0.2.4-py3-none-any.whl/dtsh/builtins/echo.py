# Copyright (c) 2023 Christophe Dufaza <chris@openmarl.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Devicetree shell built-in "echo".

Print arbitrary text to output.
"""


from typing import Optional, Sequence

from enum import Enum

from rich.console import JustifyMethod
from rich.style import Style
from rich.errors import StyleSyntaxError

from dtsh.io import DTShOutput
from dtsh.shell import (
    DTSh,
    DTShCommand,
    DTShFlag,
    DTShArg,
    DTShParameter,
    DTShError,
    DTShCommandError,
)


from dtsh.rich.text import TextUtil
from dtsh.rich.tui import GridLayout


class DTShFlagNoNewline(DTShFlag):
    """Whether to negate the criterion chain."""

    BRIEF = "do not output the trailing newline"
    SHORTNAME = "n"


class DTShArgLineStyle(DTShArg):
    """Argument that set the display style."""

    BRIEF = "set display style"
    LONGNAME = "style"

    # Argument state: rich style.
    _style: Optional[Style]

    def __init__(self) -> None:
        super().__init__(argname="style")

    @property
    def style(self) -> Optional[Style]:
        """The display style."""
        return self._style

    def reset(self) -> None:
        """Reset this argument to its default value (zero).

        Overrides DTShOption.reset().
        """
        super().reset()
        self._style = None

    def parsed(self, value: Optional[str] = None) -> None:
        """Overrides DTShOption.parsed()."""
        super().parsed(value)
        try:
            self._style = Style.parse(self._raw or "")
        except StyleSyntaxError as e:
            raise DTShError(str(e)) from e


class DTShArgLineJustify(DTShArg):
    """Argument to justify the display line."""

    BRIEF = "justify display line"
    LONGNAME = "justify"

    METHODS: Sequence[str] = ["default", "left", "center", "right", "full"]

    # Argument state: rich justify method.
    _justify: Optional[str] = None

    def __init__(self) -> None:
        super().__init__(argname="method")

    @property
    def justify(self) -> Optional[str]:
        """The display line justify."""
        return self._justify

    def reset(self) -> None:
        """Reset this argument to its default value (zero).

        Overrides DTShOption.reset().
        """
        super().reset()
        self._justify = None

    def parsed(self, value: Optional[str] = None) -> None:
        """Overrides DTShOption.parsed()."""
        super().parsed(value)
        if self._raw not in DTShArgLineJustify.METHODS:
            raise DTShError(f"'{self._raw}' is not a valid justify method")
        self._justify = self._raw


class DTShParamDisplayLine(DTShParameter):
    """Display line parameter."""

    def __init__(self) -> None:
        super().__init__(
            name="string",
            multiplicity="?",
            brief="line to display",
        )

    @property
    def string(self) -> str:
        """The parameter value set by the command line.

        If unset, will answer an empty string means (any/all aliased nodes).
        """
        return self._raw[0] if self._raw else ""


class DTShBuiltinEcho(DTShCommand):
    """Devicetree shell built-in "echo"."""

    def __init__(self) -> None:
        """Command definition."""
        super().__init__(
            "echo",
            "display a line of text",
            [
                DTShFlagNoNewline(),
                DTShArgLineStyle(),
                DTShArgLineJustify(),
            ],
            DTShParamDisplayLine(),
        )

    def execute(self, argv: Sequence[str], sh: DTSh, out: DTShOutput) -> None:
        """Overrides DTShCommand.execute()."""
        super().execute(argv, sh, out)

        style: Optional[Style] = self.with_arg(DTShArgLineStyle).style
        justify: Optional[str] = self.with_arg(DTShArgLineJustify).justify

        txt = TextUtil.mk_text(
            self.with_param(DTShParamDisplayLine).string,
            style,
        )
        view = GridLayout(expand=True)
        # view._grid.columns[0].justify = "center"
        view.add_row(txt)
        out.write(view)
