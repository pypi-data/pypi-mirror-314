import logging
import datetime
import traceback

from .interface import Formatter
from .term import TermFormatter


class LogFormatter(logging.Formatter):
    DEFAULT_LEVEL_FMT_DICT = {
        logging.DEBUG:    TermFormatter.default().blue(),
        logging.INFO:     TermFormatter.blue().bold(),
        logging.WARNING:  TermFormatter.yellow().bold(),
        logging.ERROR:    TermFormatter.red().bold(),
        logging.CRITICAL: TermFormatter.red().bold(),
    }
    DEFAULT_DATE_FMT = TermFormatter.blue().bold()
    DEFAULT_LEVEL_FMT_DICT_NOCOLOR = {
        logging.DEBUG:    TermFormatter.default(),
        logging.INFO:     TermFormatter.default(),
        logging.WARNING:  TermFormatter.default(),
        logging.ERROR:    TermFormatter.default(),
        logging.CRITICAL: TermFormatter.default(),
    }
    DEFAULT_DATE_FMT_NOCOLOR = TermFormatter.default()

    def __init__(
        self,
        separator: str = " - ",
        use_color: bool = True,
        level_fmt_dict: dict[int,Formatter]|None = None,
        print_traceback: bool = False,
        traceback_level: int = logging.WARNING,
        block_dashes: int = 35,
        date_fmt: Formatter|None = None,
        date_strftime_fmt = "%H:%M:%S",
        add_name: bool = True,
        add_path: bool = False,
        pad_levelname: bool = True,
        before_message: str = ":"
    ):
        if level_fmt_dict is None:
            if use_color:
                level_fmt_dict = self.__class__.DEFAULT_LEVEL_FMT_DICT
            else:
                level_fmt_dict = self.__class__.DEFAULT_LEVEL_FMT_DICT_NOCOLOR
        if date_fmt is None:
            if use_color:
                date_fmt = self.__class__.DEFAULT_DATE_FMT
            else:
                date_fmt = self.__class__.DEFAULT_DATE_FMT_NOCOLOR

        self.separator = separator
        self.level_fmt_dict = level_fmt_dict
        self.print_traceback = print_traceback
        self.traceback_level = traceback_level
        self.block_dashes = block_dashes
        self.date_fmt = date_fmt
        self.date_strftime_fmt = date_strftime_fmt
        self.add_name = add_name
        self.add_path = add_path
        self.pad_levelname = pad_levelname
        self.before_message = before_message

    def _fmt_level(self, level: int, levelname: str) -> str:
        pad = ""
        if self.pad_levelname:
            pad = " " * (8 - len(levelname))
        try:
            formatter = self.level_fmt_dict[level]
            return f"[{formatter.fmt(levelname)}]{pad}"
        except Exception:
            return levelname

    def _fmt_date(self, posix_time: float) -> str:
        return self.date_fmt.fmt(
            datetime.datetime.fromtimestamp(posix_time).strftime(
                self.date_strftime_fmt
            )
        )

    def _dashline(self, msg: str) -> str:
        dash_str = "-" * self.block_dashes
        return f"{dash_str}{msg}{dash_str}"

    def _block(self, title: str, msg: str) -> str:
        if self.block_dashes <= 0:
            return [msg]
        return "\n" + "\n".join([
            self._dashline(f" BEGIN {title} "),
            msg,
            self._dashline(f"  END {title}  "),
        ])

    def format(self, record: logging.LogRecord) -> str:
        desc = [
            self._fmt_level(record.levelno, record.levelname),
            self._fmt_date(record.created),
        ]
        if self.add_name:
            desc.append(record.name)
        if self.add_path:
            desc.append(f"{record.pathname}:{record.funcName}:{record.lineno}")

        msg = ""
        try:
            msg = str(record.msg % record.args)
        except Exception:
            msg = str(record.msg)
        blurbs = [self.separator.join(desc) + self.before_message, msg]
        if all([
            self.print_traceback,
            record.levelno >= self.traceback_level
        ]):
            exc_str = traceback.format_exc()
            if not exc_str.startswith("NoneType: None"):
                blurbs.append(self._block("EXCEPTION", exc_str))

        return " ".join(blurbs)
