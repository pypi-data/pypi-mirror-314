from model.data_user import DataUser
from service.data_user_service import DataUserService
from util.unauthorized_exception import UnauthorizedException
import requests

def get_current_user(event, dynamodb):

    headers = event["headers"]
    if headers is None: UnauthorizedException("Não autorizado!") 

    token = headers.get("authorization")
    if token is None: UnauthorizedException("Token não encontrado!")

    url = 'https://account-api.sankhya.com.br/validate-session'
    body = {
        "token": token.replace("Bearer ", "")
    }
    response = requests.post(url, json = body)
    resp_json = response.json()

    if response.status_code != 200:
        raise UnauthorizedException(resp_json.get("response").get("message"))

    usr = DataUserService(dynamodb).get_by_user_identifier(
        DataUser(
            user_identifier=str(resp_json.get("data").get("user_id"))
        )
    )

    if usr is None:
        raise UnauthorizedException("Usuario não encontrado!")
    
    if not usr.active:
        raise UnauthorizedException("Usuario não está ativo!")

    return usr