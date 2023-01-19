from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.wallet_model import WalletModel
from core.deps import get_session

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
#fim do Bypass

router = APIRouter()

#POST wallet
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=WalletModel)
async def post_wallet(wallet: WalletModel, db: AsyncSession = Depends(get_session)):
    new_wallet = WalletModel(id=wallet.id,
                            name=wallet.name, description=wallet.description, 
                            user_id=wallet.id)
    
    db.add(new_wallet)
    await db.commit()

    return new_wallet

#GET WALLET
@router.get('/', response_model=List[WalletModel])
async def get_wallets(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WalletModel)
        result = await session.execute(query)
        wallets: List[WalletModel] = result.scalars().all()

        return wallets

# GET wallet
@router.get('/{wallet_id}', response_model=WalletModel, status_code=status.HTTP_200_OK)
async def get_curso(wallet_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WalletModel).filter(WalletModel.id == wallet_id)
        result = await session.execute(query)
        wallet: WalletModel = result.scalar_one_or_none()

        if wallet:
            return wallet
        else:
            raise HTTPException(detail='Carteira não encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)

