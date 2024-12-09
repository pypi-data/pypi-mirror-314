""" Usage example """

from typing import Optional
from cyclarity_sdk.expert_builder import Runnable, BaseResultsModel
import time


class CanTestResult(BaseResultsModel):
    res_str: str


class canRunnableInstance(Runnable[CanTestResult]):
    desc: str
    cli_args: str
    _num: Optional[int] = 1  # not appear in the model_json_schema

    def setup(self):
        self.logger.info("setup")

    def run(self) -> CanTestResult:
        self.platform_api.send_test_report_description(
            "This is dummy description for test"
        )

        # simulate dummy reporting for test progress
        for percentage in range(101):
            self.platform_api.report_test_progress(percentage=percentage)
            time.sleep(0.01)

        return CanTestResult(res_str="success!")

    def teardown(self, exception_type, exception_value, traceback):
        self.logger.info("teardown")


# --- senity checks for runnable usage ---
# generates params schema from the runnable class attributes
print("\nParams schema - private members not included")
print(canRunnableInstance.model_json_schema())


# generate result schema
print("\nResult json schema:")
print(canRunnableInstance.generate_results_schema())

# Initiate runnable - option 1

# with canRunnableInstance(
#     desc="test", cli_args="-as -fsd -dsd"
# ) as runnable_instance:  # noqa
#     result: CanTestResult = runnable_instance()

#     # generates result json object
#     print("\nDirect running results: ")
#     print(result.model_dump_json())


# Initiate runnable - option 2
input = {
    "desc": "test",
    "cli_args": "-as -fsd -dsd",
}

with canRunnableInstance(**input) as runnable_instance:  # noqa
    result: CanTestResult = runnable_instance()

    # generates result json object
    print("\ndictionary running results: ")
    print(result.model_dump_json())
