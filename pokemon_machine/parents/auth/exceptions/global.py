from exceptions.base import AppException

DATA_ALREADY_EXISTS_CODE = 409
FAILED_INSERT_DATA_CODE = 500
VERIFICATION_FAILED_CODE = 401
DATA_NOT_FOUND_CODE = 404

class DataAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="Data already exists",
            status_code=DATA_ALREADY_EXISTS_CODE,
        )


class FailedInsertDataException(AppException):
    def __init__(self):
        super().__init__(
            message="Failed to insert data",
            status_code=FAILED_INSERT_DATA_CODE,
        )


class VerificationFailedException(AppException):
    def __init__(self):
        super().__init__(
            message="Verification failed",
            status_code=VERIFICATION_FAILED_CODE,
        )

class DataNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Data not found",
            status_code=DATA_NOT_FOUND_CODE,
        )


class UniversalProblemException(AppException):
    def __init__(self, message: str = "An unexpected problem occurred", status_code: int = 500):
        super().__init__(message=message, status_code=status_code)
