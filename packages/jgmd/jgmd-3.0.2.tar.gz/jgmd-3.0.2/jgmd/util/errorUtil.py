import traceback
from datetime import datetime
from typing import Callable, Tuple


def exceptionToStr(e: Exception) -> str:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"Exception was thrown at {current_time}:\n{''.join(traceback.format_exception(None, e, e.__traceback__))}"
    return error_message


def getErrorHandlingDecorators(
    onError: Callable[[str], None]
) -> Tuple[Callable, Callable]:
    def handleError(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = exceptionToStr(e)
                onError(error_message)

        return wrapper

    def handleErrorAsync(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_message = exceptionToStr(e)
                onError(error_message)

        return wrapper

    return handleError, handleErrorAsync
