from typing import Optional, TypedDict
from bruce_models import GuardianApi

class Session:
    """
    Represents a Session in Nextspace.
    You will find the JSession data-model and all related API communication here.
    """

    class JSession(TypedDict):
        """
        Represents the JSON structure of a Session.
        """
        # The session ID. Used to authenticate requests.
        ID: str

    @staticmethod
    def login(api: GuardianApi, username: str, password: str, account_id: Optional[str] = "") -> JSession:
        """
        Performs a login with credentials.
        If no username is provided, it is treated as a token login.
        An account is optional to specify what account permissions should be returned and associated with the session.
        """
        if not password or len(password) < 1:
            raise ValueError("You must provide a password to authenticate.")
        
        body = {
            "account": account_id,
            "login": username,
            "password": password
        }
        return api.POST("login", body)
    
    @staticmethod
    def logout(api: GuardianApi) -> None:
        """
        Performs a logout.
        The session attached to the API instance will be invalidated.
        """
        return api.POST("logout")