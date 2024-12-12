from ..compat import Self


class TermFormatter:
    def __init__(self,
        color: int|None = None,
        style: int|None = None
    ):
        self.color = color
        self.style = style
        self._formatter = None

    def _create_formatter(self):
        esc_code = "\033["
        color = "" if self.color is None else str(self.color)
        style = "" if self.style is None else f";{self.style}"
        if color == "" and style == "":
            self._formatter = lambda s: s
        else:
            self._formatter = lambda s: f"{esc_code}{color}{style}m{s}{esc_code}0m"

    def fmt(self, input: str) -> str:
        if self._formatter is None:
            self._create_formatter()
        return self._formatter(input)

    def bold(self) -> Self:
        return TermFormatter(
            color = self.color,
            style = 1
        )

    @classmethod
    def default(cls) -> Self:
        return TermFormatter()

    @classmethod
    def red(cls) -> Self:
        return TermFormatter(color = 31)

    @classmethod
    def green(cls) -> Self:
        return TermFormatter(color = 32)

    @classmethod
    def yellow(cls) -> Self:
        return TermFormatter(color = 33)

    @classmethod
    def blue(cls) -> Self:
        return TermFormatter(color = 34)

    @classmethod
    def cyan(cls) -> Self:
        return TermFormatter(color = 37)
