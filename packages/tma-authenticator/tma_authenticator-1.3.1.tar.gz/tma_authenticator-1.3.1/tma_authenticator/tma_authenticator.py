import base64
import json
import hashlib
import hmac
from typing import List, TypeVar, Callable, Optional
from aiocache import cached, caches # type: ignore
from urllib.parse import unquote
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .users import User, UserDB
from .storage_provider import StorageProvider
from .tma_authentication_router import TMAAuthenticationRouter


T = TypeVar('T', bound=BaseModel)

class TMAAuthenticator():
    bot_token: str
    admin_password: str
    storage_provider: StorageProvider
    authentication_router: TMAAuthenticationRouter
    user_model: Callable[..., T]

    def __init__(self,
                 bot_token: str,
                 admin_password: str,
                 storage_provider: StorageProvider,
                 user_model: Optional[Callable[..., T]] = None):
        self.bot_token = bot_token
        self.admin_password = admin_password
        self.storage_provider = storage_provider
        self.authenticator_router_provider = TMAAuthenticationRouter(
            admin_password=self.admin_password,
            storage_provider=self.storage_provider
        )
        self.user_model = user_model or UserDB # type: ignore

    @property # type: ignore
    def authentication_router(self): # type: ignore
        return self.authenticator_router_provider

    async def oauth_verify_token(self, Authorization: str = Depends(OAuth2PasswordBearer(tokenUrl="/token/"))):
        return await self.verify_token(authorization=Authorization)


    async def refresh_user_cache(self, cache_key: str):
        """
        Invalidates the cached verify_token result for the given authorization and optional extra_tokens_validation.
        Call this method after updating the user's data to force cache renewal.
        """

        # Delete the cache entry so the next token verification will recompute and refresh the user data.
        cache = caches.get('default')
        await cache.delete(cache_key)

    @cached(
        key_builder=lambda f, *args,
                           **kwargs: f"{kwargs['authorization']}:{hashlib.sha256(json.dumps(kwargs.get('extra_tokens_validation') or []).encode()).hexdigest()}",
        ttl=300,
        alias="default"
    )
    async def verify_token(self,
                           authorization: str,
                           extra_tokens_validation: Optional[List[str]] = None) -> T:
        cache_key = f"{authorization}:{hashlib.sha256(json.dumps(extra_tokens_validation or []).encode()).hexdigest()}"
        try:
            decoded_bytes = base64.b64decode(authorization)
            decoded_data = json.loads(decoded_bytes.decode('utf-8'))

            user = User(**decoded_data)
            # Admin login without user updating in the DB.
            if decoded_data['initData'] != self.admin_password:
                valid = self.is_valid_user_info(
                    web_app_data=decoded_data['initData'],
                    bot_token=self.bot_token,
                    extra_tokens_validation=extra_tokens_validation
                )
                if not valid:
                    raise HTTPException(status_code=401,
                                        detail="Invalid credentials.",
                                        headers={"Authorization": "Bearer"})

                user_tg_language = self.get_user_tg_language(user_init_data=decoded_data['initData'])
                user.tg_language = user_tg_language
                user = User(**user.model_dump())

                db_user = await self.storage_provider.retrieve_user(search_query={'tg_id': user.tg_id})
                if not db_user:
                    insert_id = await self.storage_provider.insert_user(
                        user_data=user.model_dump()
                    )
                    return self.user_model(id=str(insert_id), **user.model_dump(), cache_key=cache_key)
                else:
                    attributes_to_compare = ['tg_language', 'first_name', 'last_name', 'username']
                    for attr in attributes_to_compare:
                        if getattr(user, attr) != db_user.get(attr):
                            await self.storage_provider.update_user(
                                id=db_user['id'],
                                update_data={
                                    'tg_language': user.tg_language,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'username': user.username
                                }
                            )
                            break
                    return self.user_model(**db_user, cache_key=cache_key)
            else:
                db_user = await self.storage_provider.retrieve_user(search_query={'tg_id': user.tg_id})
                if db_user:
                    return self.user_model(**db_user, cache_key=cache_key)
                else:
                    raise HTTPException(status_code=404,
                                        detail=f"User to impersonalize was not found {user.tg_id}",
                                        headers={"Authorization": "Bearer"})
        except HTTPException as err:
            raise err
        except Exception as err:
            raise HTTPException(status_code=401,
                                detail=f"Could not validate credentials. {err}",
                                headers={"Authorization": "Bearer"})

    def is_valid_user_info(self,
                           web_app_data,
                           bot_token: str,
                           extra_tokens_validation: Optional[List[str]] = None
    ) -> bool:
        try:
            data_check_string = unquote(web_app_data)
            data_check_arr = data_check_string.split('&')
            needle = 'hash='
            hash_item = next((item for item in data_check_arr if item.startswith(needle)), '')
            tg_hash = hash_item[len(needle):]
            data_check_arr.remove(hash_item)
            data_check_arr.sort()
            data_check_string = "\n".join(data_check_arr)
            secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
            calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

            if calculated_hash != tg_hash:
                if extra_tokens_validation:
                    for token in extra_tokens_validation:
                        valid = self.is_valid_user_info(web_app_data=web_app_data, bot_token=token)
                        if valid:
                            return True
                return False
        except Exception as e:
            return False
        return True

    def get_user_tg_language(self, user_init_data: str) -> str:
        try:
            if user_init_data == self.admin_password:
                # TODO: в этом аттрибуте может скрываться админ пароль, язык не сможем получить
                return 'admin'

            decoded_user_init_data = unquote(user_init_data)
            decoded_user_init_data = unquote(decoded_user_init_data)

            user_data_dict = self.get_user_data_dict(unquote_user_data=decoded_user_init_data)

            return user_data_dict['language_code']
        except Exception as err:
            return ''

    def get_user_data_dict(self, unquote_user_data: str) -> dict:
        start_index_value = 'user='
        end_index_value = '&chat_instance=' if 'start_param' in unquote_user_data else '&auth_date='

        start_index = unquote_user_data.find(start_index_value) + len(start_index_value)
        end_index = unquote_user_data.find(end_index_value)
        user_data_string = unquote_user_data[start_index:end_index]
        return json.loads(user_data_string)
