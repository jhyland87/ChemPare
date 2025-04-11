# from chempare import suppliers
# import os

import chempare


# import webbrowser

# from pytest.fixtures import fixture


# def pytest_sessionfinish(session, exitstatus):
#     print("\n--- Test session finished ---")
#     print(f"Exit status: {exitstatus}")
#     # Add your custom actions here, e.g.,
#     # - Generating a summary report
#     # - Closing database connections
#     # - Cleaning up temporary files


# # Literal["session", "package", "module", "class", "function"]
# @fixture(autouse=True, scope='session')
# def my_session_fixture():
#     print("\n--- Test session setup ---")
#     yield
#     print("\n--- Test session teardown ---")


# @fixture(autouse=True, scope='function')
# def my_function_fixture():
#     print("\n--- Test function setup ---")
#     yield
#     print("\n--- Test function teardown ---")


# @fixture(autouse=True, scope='package')
# def my_package_fixture():
#     print("\n--- Test package setup ---")
#     yield
#     print("\n--- Test package teardown ---")


# @fixture(autouse=True, scope='class')
# def my_class_fixture():
#     print("\n--- Test class setup ---")
#     yield
#     print("\n--- Test class teardown ---")


# @fixture(autouse=True, scope='module')
# def my_module_fixture():
#     print("\n--- Test module setup ---")
#     yield
#     print("\n--- Test module teardown ---")


# def pytest_sessionfinish(session, exitstatus):
#     if os.environ.get('PYTEST_COV') == 'true':
#         # Code to run after all tests, specifically when coverage was measured
#         print("")
#         coverage_results = os.path.abspath("coverage-html/index.html")
#         print(f"Opening coerage file: {coverage_results}")

#         # try:
#         #     webbrowser.get("macosx").open(
#         #         f'file://{coverage_results}', new=0, autoraise=False
#         #     )  # "brave" might need adjustment based on OS and setup
#         # except webbrowser.Error:
#         #     print("Brave browser could not be found or opened.")
#         #     webbrowser.open(f'file://{coverage_results}', new=0, autoraise=False)
#         # # webbrowser.get('brave').open(f'file://{coverage_results}', new=0)


def pytest_report_header(config):
    chempare.called_from_test = True
    ret = ["project deps: chempare-0.0"]
    ret.append(f"chempare.called_from_test: {chempare.called_from_test}")
    if config.getoption("verbose") > 0:
        ret.extend([f"info1: Verbosity: {config.getoption('verbose')}"])
    return ret
