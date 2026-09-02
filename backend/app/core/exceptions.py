from fastapi import HTTPException, status

class EntityNotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class DuplicateEntityException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedAccessException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials or unauthorized action"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
