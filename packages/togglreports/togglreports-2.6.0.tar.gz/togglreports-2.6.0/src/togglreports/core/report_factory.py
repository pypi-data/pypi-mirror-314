""" Factory for creating reports """

from typing import Callable

from togglreports.core.protocols import ReportPlugin


PLUGINS: dict[str, Callable[..., ReportPlugin]] = {}


def register(report_name: str, report_class: Callable[[], ReportPlugin]) -> None:
    """ Register report class """
    PLUGINS[report_name] = report_class


def unregister(report_name: str) -> None:
    """ Unregister report class """
    PLUGINS.pop(report_name, None)


def create_report(report_name: str, *args, **kwargs) -> None:
    """ Create report """
    try:
        report_class = PLUGINS[report_name]
    except KeyError as err:
        raise KeyError(f"Report {report_name} does not exist") from err

    report_class(*args, **kwargs).export()

    return None
