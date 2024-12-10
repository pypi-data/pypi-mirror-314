# -*- coding: utf-8 -*-
import datetime
import importlib
import logging
import re
from pathlib import Path
from typing import Callable, Dict, Optional, TypeVar, Union

import torch
from packaging.version import Version
from typing_extensions import TypeIs

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


def exists(val: Union[_T, None]) -> TypeIs[_T]:
    return val is not None


def default(val: Union[_T, None], d: Union[_T, Callable[[], _T]]) -> _T:
    if exists(val):
        return val
    return d() if callable(d) else d


def to_camel(text):
    text = text.capitalize()
    text = re.sub(r"(?!^)_([a-zA-Z])", lambda m: m.group(1).upper(), text)
    text = text.replace("Tts", "TTS")
    text = text.replace("vc", "VC")
    return text


def find_module(module_path: str, module_name: str) -> object:
    module_name = module_name.lower()
    module = importlib.import_module(module_path + "." + module_name)
    class_name = to_camel(module_name)
    return getattr(module, class_name)


def import_class(module_path: str) -> object:
    """Import a class from a module path.

    Args:
        module_path (str): The module path of the class.

    Returns:
        object: The imported class.
    """
    class_name = module_path.split(".")[-1]
    module_path = ".".join(module_path.split(".")[:-1])
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_import_path(obj: object) -> str:
    """Get the import path of a class.

    Args:
        obj (object): The class object.

    Returns:
        str: The import path of the class.
    """
    return ".".join([type(obj).__module__, type(obj).__name__])


def format_aux_input(def_args: Dict, kwargs: Dict) -> Dict:
    """Format kwargs to hande auxilary inputs to models.

    Args:
        def_args (Dict): A dictionary of argument names and their default values if not defined in `kwargs`.
        kwargs (Dict): A `dict` or `kwargs` that includes auxilary inputs to the model.

    Returns:
        Dict: arguments with formatted auxilary inputs.
    """
    kwargs = kwargs.copy()
    for name in def_args:
        if name not in kwargs or kwargs[name] is None:
            kwargs[name] = def_args[name]
    return kwargs


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%y%m%d-%H%M%S")


class ConsoleFormatter(logging.Formatter):
    """Custom formatter that prints logging.INFO messages without the level name.

    Source: https://stackoverflow.com/a/62488520
    """

    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)


def setup_logger(
    logger_name: str,
    level: int = logging.INFO,
    *,
    formatter: Optional[logging.Formatter] = None,
    screen: bool = False,
    tofile: bool = False,
    log_dir: str = "logs",
    log_name: str = "log",
) -> None:
    lg = logging.getLogger(logger_name)
    if formatter is None:
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(levelname)-8s - %(name)s: %(message)s", datefmt="%y-%m-%d %H:%M:%S"
        )
    lg.setLevel(level)
    if tofile:
        Path(log_dir).mkdir(exist_ok=True, parents=True)
        log_file = Path(log_dir) / f"{log_name}_{get_timestamp()}.log"
        fh = logging.FileHandler(log_file, mode="w")
        fh.setFormatter(formatter)
        lg.addHandler(fh)
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        lg.addHandler(sh)


def is_pytorch_at_least_2_4() -> bool:
    """Check if the installed Pytorch version is 2.4 or higher."""
    return Version(torch.__version__) >= Version("2.4")
