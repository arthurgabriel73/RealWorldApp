from fastapi import HTTPException, status


def email_already_registered() -> None:
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail='This username/email is already owned.')
