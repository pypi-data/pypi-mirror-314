import logging
from typing import Any, Callable, Coroutine, TypeVar

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .utils import utils
from .view import template

# logging
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Prevent propagation to the root logger

# generics
T = TypeVar("T", bound=BaseModel)


def compare_sync(
    current_fn: Callable[[], T],
    new_fn: Callable[[], T],
    percentage: int,
) -> T:
    # make current production request
    current_result = current_fn()

    try:
        # get previous requests data
        total_requests, compared_requests, different_results = (
            utils.get_main_file_values()
        )

        # count current request
        total_requests += 1

        # check if should make second request to compare
        should_compare = utils.check_if_should_compare(
            compared_requests, total_requests, percentage
        )

        # handle new result if needed
        if should_compare:
            compared_requests += 1
            new_result = new_fn()

            # check differences
            is_equal, diff_content = utils.compare_results(current_result, new_result)

            if not is_equal:
                different_results += 1

                # save file with differences
                utils.create_diff_result_file(diff_content)

        # update main file on memory
        utils.update_main_file(total_requests, compared_requests, different_results)

        return current_result

    except Exception as err:
        logger.exception(err)
        return current_result


async def compare_async[T](
    current_fn: Callable[[], Coroutine[Any, Any, T]],
    new_fn: Callable[[], Coroutine[Any, Any, T]],
    percentage: int,
) -> T:
    # make current production request
    current_result = await current_fn()

    try:
        # get previous requests data
        total_requests, compared_requests, different_results = (
            utils.get_main_file_values()
        )

        # count current request
        total_requests += 1

        # check if should make second request to compare
        should_compare = utils.check_if_should_compare(
            compared_requests, total_requests, percentage
        )

        # handle new result if needed
        if should_compare:
            compared_requests += 1
            new_result = await new_fn()

            # check differences
            is_equal, diff_content = utils.compare_results(current_result, new_result)

            if not is_equal:
                different_results += 1

                # save file with differences
                utils.create_diff_result_file(diff_content)

        # update main file on memory
        utils.update_main_file(total_requests, compared_requests, different_results)

        return current_result

    except Exception as err:
        logger.exception(err)
        return current_result


def init_web_view(app: FastAPI, security_token: str) -> None:
    def create_endpoint() -> (
        Callable[[Request, str, str | None], Coroutine[Any, Any, HTMLResponse]]
    ):
        async def endpoint(
            request: Request, token: str, filename: str | None = None
        ) -> HTMLResponse:
            # check token to keep endpoint "hidden"
            if token != security_token:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Not found"}
                )

            # get requests numbers
            total_requests = utils.get_main_file_value(key="total_requests", line=1)
            compared_requests = utils.get_main_file_value(
                key="compared_requests", line=2
            )
            different_results = utils.get_main_file_value(
                key="different_results", line=3
            )

            # get result files
            result_files = utils.get_all_results_files()

            # get selected file content
            file_content: str = ""
            if filename:
                file_content = utils.get_result_file_content(filename)

            # return HTML
            html = template.render(
                token=token,
                total_requests=total_requests,
                compared_requests=compared_requests,
                different_results=different_results,
                result_files=result_files,
                filename=filename,
                file_content=file_content,
            )
            return HTMLResponse(html)

        return endpoint

    app.add_api_route(
        "/diff-tracer-view/{token}",
        create_endpoint(),
        methods=["GET"],
        response_class=HTMLResponse,
    )
