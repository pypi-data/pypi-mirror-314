import sys
from typing import Optional
from inspect import getdoc
import logging
from argparse import Action, RawDescriptionHelpFormatter
import jsonargparse
from .runnable import Runnable


def _configure_runner_logging(runner: Runnable, verbose_logging: bool):
    """
    This function configure the logging of arunnable to print INFO messages to the stdout without prefixes.
    In addition DEBUG messages are suppressed unless verbose_logging is on.

    This help runnables to run from CLI with better prints if run from CLI.
    """
    class InfoFilter(logging.Filter):
        def filter(self, record):
            return record.levelno == logging.INFO

    class NoInfoFilter(logging.Filter):
        def filter(self, record):
            return record.levelno != logging.INFO

    class LessVerboseFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.INFO:
                return record.getMessage()  # Only the message, no prefix
            else:
                return super(LessVerboseFormatter, self).format(record)

    for handler in runner.logger.handlers:
        if hasattr(handler, 'stream') and handler.stream == sys.stdout:
            handler.addFilter(NoInfoFilter())
            if not verbose_logging and handler.level < logging.INFO:
                handler.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    if verbose_logging:
        stdout_handler.setLevel(logging.DEBUG)
    else:
        stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(InfoFilter())
    stdout_handler.setFormatter(LessVerboseFormatter())

    runner.logger.addHandler(stdout_handler)


def run_from_cli(runnable: type[Runnable], cli_args: Optional[str] = None):
    """running runnables from to command line.
    Add the following line to the end of your runnable script:
        if __name__ == '__main__':
            from cyclarity_sdk.expert_builder import run_from_cli
            run_from_cli(<<RunnableName>>)
    (replace <<RunnableName>> with the runnable class to execute)

    This function also allow to create a config file and to create a schema for params/results from the cli.

    Args:
        runnable (Runnable): The runnable type to run from the command line
        cli_args (Optional[str]): the cli args to run the runnable with. If not specified the args will come from the cli.
    """
    import shlex

    # Custom action for --get_schema
    class GetSchemaAction(Action):
        def __call__(self, parser, namespace, values, option_string=None):
            import json
            IN_PARAMS_FILENAME = "in_params.json"
            OUT_PARAMS_FILENAME = "out_params.json"

            in_params = runnable.generate_params_schema()
            out_params = runnable.generate_results_schema()
            with open(IN_PARAMS_FILENAME, 'w') as f:
                json.dump(in_params, f, indent=4)
                print(
                    f"The runnable input parameters schema was written to {IN_PARAMS_FILENAME}")
            with open(OUT_PARAMS_FILENAME, 'w') as f:
                json.dump(out_params, f, indent=4)
                print(
                    f"The runnable output parameters schema was written to {OUT_PARAMS_FILENAME}")
            parser.exit()  # Stop parsing here

    run_from_cli_fields = ["config", "get_schema", "verbose_logging"]

    parser = jsonargparse.ArgumentParser(
        description=getdoc(runnable),
        formatter_class=RawDescriptionHelpFormatter
    )
    if any(f in runnable.model_fields for f in run_from_cli_fields):
        print(
            f"[WARNING]: fields in the tested runnable cannot include any of the fields {run_from_cli_fields}")
        print("Running without additional run from cli capabilities...")
        verbose_args = None
    else:
        parser.add_argument("--config", action="config")
        parser.add_argument("--get_schema", nargs=0, action=GetSchemaAction)

        if "v" not in runnable.model_fields and "V" not in runnable.model_fields:
            verbose_args = ("-v", "--verbose_logging")
        else:
            verbose_args = ("--verbose_logging")

    parser.add_argument(*verbose_args, action="store_true")
    parser.add_class_arguments(runnable)

    args_list = None
    if cli_args:
        args_list = shlex.split(cli_args)

    args = parser.parse_args(args_list)
    instances = parser.instantiate_classes(args)

    runner = runnable(**instances)

    _configure_runner_logging(runner, args.get('verbose_logging', False))

    with runner:
        results = runner()
        print(results)
