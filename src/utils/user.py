from fastapi import HTTPException, status


def verify_if_is_user_have_permission(param_user_id, user_id):
    if not param_user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                'Access denied. You do not have the '
                'required permissions to perform this action.'
            )
        )


def verify_if_user_exist(db_user):
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found.'
        )
