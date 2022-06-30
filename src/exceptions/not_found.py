from fastapi import HTTPException, status


def user_not_found() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not found.')
