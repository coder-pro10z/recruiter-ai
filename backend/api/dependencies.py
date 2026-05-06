from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated

DBDep = Annotated[AsyncSession, Depends(get_db)]
