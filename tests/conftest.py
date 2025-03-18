# from chempare import suppliers
import chempare


def pytest_report_header(config):
    chempare.called_from_test = True
    ret = ["project deps: chempare-0.1"]
    ret.append(f"chempare.called_from_test: {chempare.called_from_test}")
    if config.getoption("verbose") > 0:
        ret.extend([f"info1: Verbosity: {config.getoption('verbose')}"])
    return ret
