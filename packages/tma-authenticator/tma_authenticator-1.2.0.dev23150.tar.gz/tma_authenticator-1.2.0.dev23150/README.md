


## How to use

### 1. `authorization.py`
```python

from tma_authenticator.tma_authentication_router import TMAAuthenticationRouter
from tma_authenticator.tma_authenticator import TMAAuthenticator

from database.users import UsersDatabase
from config import TELEGRAM_BOT_TOKEN, IMPERSONATE_ADMIN_PASSWORD

user_database: UsersDatabase = UsersDatabase()
authenticator = TMAAuthenticator(TELEGRAM_BOT_TOKEN, IMPERSONATE_ADMIN_PASSWORD, user_database)
authentication_router = authenticator.authentication_router
    
```