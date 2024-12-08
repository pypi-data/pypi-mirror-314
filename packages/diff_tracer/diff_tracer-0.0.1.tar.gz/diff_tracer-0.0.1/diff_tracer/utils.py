import json
import linecache
import os
import random
import shutil
from datetime import datetime
from typing import Any, List, NamedTuple

from .diff_match_patch import diff_match_patch

MAIN_FILE_NAME = "diff-tracer-main-info.txt"
TMP_FOLDER_NAME = "tmp-diff-tracer"
RESULT_FILE_PREFIX = "res"


class MainFileValues(NamedTuple):
    total_requests: int
    compared_requests: int
    different_results: int


class CompareResultsValues(NamedTuple):
    is_equal: bool
    diff_content: List[Any]


class Utils:
    def get_target_path(self) -> str:
        current_path = os.getcwd()
        return os.path.join(current_path, TMP_FOLDER_NAME)

    def get_main_file_path(self) -> str:
        target_path = self.get_target_path()
        os.makedirs(target_path, exist_ok=True)
        return os.path.join(target_path, MAIN_FILE_NAME)

    def get_main_file_value(self, key: str, line: int) -> int:
        main_info_file_path = self.get_main_file_path()
        value = int(
            (linecache.getline(main_info_file_path, line) or f"{key}=0")
            .replace("\n", "")
            .replace("\r", "")
            .replace(f"{key}=", "")
        )
        linecache.clearcache()
        return value

    def get_main_file_values(self) -> MainFileValues:
        total_requests = utils.get_main_file_value(key="total_requests", line=1)
        compared_requests = utils.get_main_file_value(key="compared_requests", line=2)
        different_results = utils.get_main_file_value(key="different_results", line=3)
        return MainFileValues(total_requests, compared_requests, different_results)

    def update_main_file(
        self, total_requests: int, compared_requests: int, different_results: int
    ) -> None:
        main_info_file_path = self.get_main_file_path()
        with open(main_info_file_path, "w") as wb:
            lines = [
                f"total_requests={str(total_requests)}\n",
                f"compared_requests={str(compared_requests)}\n",
                f"different_results={str(different_results)}\n",
            ]
            wb.writelines(lines)

    def create_diff_result_file(self, diff_content: List[Any]) -> None:
        html_content = diff_match_patch().diff_prettyHtml(diffs=diff_content)
        unique_id = random.randrange(1111, 9999, 4)
        today = datetime.now().strftime("%Y-%m-%d-%H-%M")
        file_name = f"{RESULT_FILE_PREFIX}-{today}-{str(unique_id)}.html"
        target_path = self.get_target_path()
        file_location = os.path.join(target_path, file_name)
        with open(file_location, "w") as buffer:
            buffer.write(html_content)

    def get_all_results_files(self) -> List[str]:
        target_path = self.get_target_path()
        result_files = []
        for file_name in os.listdir(target_path):
            if file_name.startswith(f"{RESULT_FILE_PREFIX}-") and file_name.endswith(
                ".html"
            ):
                result_files.append(file_name)
        return result_files

    def get_result_file_content(self, filename: str) -> str:
        target_path = self.get_target_path()
        file_location = os.path.join(target_path, filename)
        file_exists = os.path.isfile(file_location)
        if file_exists:
            with open(file_location, "r") as buffer:
                return buffer.read()
        return ""

    def check_if_should_compare(
        self, compared_requests: int, total_requests: int, percentage: int
    ) -> bool:
        percentage_of_total: int = round((compared_requests / total_requests) * 100)
        should_compare = percentage_of_total < percentage and random.random() < 0.5
        return should_compare

    def compare_results(
        self, current_result: Any, new_result: Any
    ) -> CompareResultsValues:
        # pretty print jsons
        formatted_current_result = json.dumps(
            json.loads(json.dumps(current_result)), indent=4
        )
        formatted_new_result = json.dumps(json.loads(json.dumps(new_result)), indent=4)
        # check differences
        diff_content = diff_match_patch().diff_main(
            text1=str(formatted_current_result), text2=str(formatted_new_result)
        )
        is_equal = len(diff_content) == 1
        return CompareResultsValues(is_equal, diff_content)

    def clear_saved_data(self) -> None:
        target_path = self.get_target_path()
        print(target_path)
        shutil.rmtree(target_path, ignore_errors=True)


utils = Utils()
