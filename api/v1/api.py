from fastapi import APIRouter

from api.v1.endpoints import wallet

api_router = APIRouter()
api_router.include_router(wallet.router, prefix='/wallet', tags=['wallets'])