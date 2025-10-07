from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from core.constants import DUPLICATE_ARTICLES, INTEGRITY_ERROR, ERROR_INTERNAL, WITHOUT_OPTIONS


class InvalidOptionFilterException(Exception):
    pass


def bad_request_handler(request: Request, exc: InvalidOptionFilterException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": WITHOUT_OPTIONS}
    )

def integrity_error_handler(request: Request, exc: IntegrityError):
    if "unique_title_author" in str(exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": DUPLICATE_ARTICLES}
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": INTEGRITY_ERROR}
    )

def internal_error_server(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"{ERROR_INTERNAL}{exc}"}
    )