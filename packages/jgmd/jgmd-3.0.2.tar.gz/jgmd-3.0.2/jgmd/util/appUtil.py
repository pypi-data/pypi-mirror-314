from typing import List, Callable

from ..logging import FreeTextLogger, LogLevel
from .errorUtil import getErrorHandlingDecorators

class AppLogger:
    debugLogger: FreeTextLogger
    errorLogger: FreeTextLogger

    @staticmethod
    def init(logLevel:LogLevel=LogLevel.CRITICAL, logDirectory:str="./logs", debugLogFileName:str="debug.log", errorLogFileName="error.log",printToConsole=True) -> None:
        AppLogger.debugLogger = FreeTextLogger(
            logDirectory=logDirectory,
            fileName=debugLogFileName,
            logLevel=logLevel,
            printToConsole=printToConsole,
        )
        AppLogger.errorLogger = FreeTextLogger(
            logDirectory=logDirectory,
            fileName=errorLogFileName,
            logLevel=LogLevel[logLevel],
            printToConsole=printToConsole,
        )
    @staticmethod
    def clearLogs():
        AppLogger.debugLogger.clearLog()
        AppLogger.errorLogger.clearLog()


class AppErrors:
    errors: List[str] = []
    handleError: Callable[[Callable], Callable]
    handleErrorAsync: Callable[[Callable], Callable]

    @staticmethod
    def init() -> None:
        handleError, handleErrorAsync = getErrorHandlingDecorators(AppErrors.onAppError)
        AppErrors.handleError = handleError
        AppErrors.handleErrorAsync = handleErrorAsync

    @staticmethod
    def onAppError(errorStr: str):
        AppLogger.errorLogger.logError(lambda: errorStr)
        AppErrors.errors.append(errorStr)

    @staticmethod
    def onEventError(event: str, errorStr: str):
        AppLogger.errorLogger.logError(
            lambda: f"Error during event={event}:\n{errorStr}"
        )
        AppErrors.errors.append(errorStr)

    @staticmethod
    def hasErrors():
        return len(AppErrors.errors) > 0