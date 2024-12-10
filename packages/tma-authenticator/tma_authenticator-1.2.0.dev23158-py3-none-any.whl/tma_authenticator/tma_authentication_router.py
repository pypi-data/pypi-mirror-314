import base64
import json

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .users import UserDB
from .token import TokenResponse, Token
from .storage_provider import StorageProvider


class TMAAuthenticationRouter(APIRouter):
    admin_password: str
    storage_provider: StorageProvider

    def __init__(self, admin_password: str, storage_provider: StorageProvider):
        super().__init__(prefix='/token', tags=['Authorization'], responses={404: {"description": "Not found"}})
        self.admin_password = admin_password
        self.storage_provider = storage_provider

        @self.post('/',
                   summary='Create user authorization token.',
                   response_model=TokenResponse,
                   tags=["Authorization"])
        @self.post('',
                   summary='Create user authorization token.',
                   response_model=TokenResponse,
                   tags=["Authorization"])
        async def retrieve_access_token(token_data: OAuth2PasswordRequestForm = Depends()):
            return await self.create_access_token(token_data=token_data)

    async def create_access_token(self, token_data: OAuth2PasswordRequestForm) -> TokenResponse:
        if not token_data.username.isdigit():
            raise HTTPException(status_code=400, detail='username should be integer.')
        if token_data.password != self.admin_password:
            raise HTTPException(status_code=403, detail=f'Invalid credentials.')
        tg_id = int(token_data.username)

        db_user = await self.storage_provider.retrieve_user(search_query={'tg_id': tg_id})
        if db_user:
            user = UserDB(**db_user)
        else:
            user = UserDB(
                tg_id=tg_id,
                username=token_data.username,
                first_name='admin',
                last_name='admin',
                tg_language='en'
            )

        # TODO: This is not safe for Client Side services. This token MUST be used only for internal services.
        token_model = Token(first_name=user.first_name,
                      last_name=user.last_name,
                      username=user.username,
                      tg_id=user.tg_id,
                      tg_language=user.tg_language,
                      initData=token_data.password)
        token = json.dumps(token_model.model_dump(mode='json'))
        encoded_token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return TokenResponse(access_token=encoded_token)