from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from microshop.core.models.db_helper import db_helper
from microshop.api_v1.auth.dependencies import require_permission


router = APIRouter(tags=['Admin • User'])

@router.delete(
    '/user/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission('user:delete'))],
)
async def delete_data_user(user_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    result = await crud.delete_user(session=session, user_id=user_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')