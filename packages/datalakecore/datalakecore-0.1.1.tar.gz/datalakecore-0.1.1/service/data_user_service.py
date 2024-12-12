from model.data_user import DataUser
from model.data_access_request import DataAccessRequest

from repository.data_user_repository import DataUserRepository
from repository.data_access_request_repository import DataAccessRequestRepository
from repository.policy_repository import PolicyRepository

from schema.data_user_schema import DataUserSchema

from util.inconsistence_exception import InconsistenceException

import requests
from datetime import datetime

class DataUserService:

    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.dataUserRepository = DataUserRepository(self.dynamodb)
        self.dataAccessRequestRepository = DataAccessRequestRepository(self.dynamodb)
        self.policyRepository = PolicyRepository()

    def login(self, obj: DataUserSchema):
        
        if obj.user_email is None or len(obj.user_email) < 1:
            raise InconsistenceException("Por favor, informe o campo email")
        if obj.password is None or len(obj.password) < 1:
            raise InconsistenceException("Por favor, informe o campo senha")
        
        url = 'https://account-api.sankhya.com.br/authentication'
        body = {
            "application_id": "9",
            "username": obj.user_email,
            "password": obj.password
        }
        response = requests.post(url, json = body)
        resp_json = response.json()

        if response.status_code != 200:
            raise InconsistenceException(resp_json.get("response").get("message"))

        usr = self.dataUserRepository.get_by_user_email(obj)
        if usr is None:
            raise InconsistenceException("Este usuário não possui permissão para acessar o portal da plataforma de dados!")
        
        usr.user_identifier = str(resp_json.get("data").get("id"))
        if resp_json.get("data").get("status") == "ativo":
            usr.active = True
        else:
            usr.active = False
        self.dataUserRepository.update(usr)

        return DataUserSchema(
            id=usr.id,
            user_email=usr.user_email,
            user_identifier=usr.user_identifier,
            user_name=usr.user_name,
            aws_user_name=usr.aws_user_name,
            active=usr.active,
            token=resp_json.get("data").get("access_token")
        )
    
    def save(self, obj: DataUser):

        if obj.user_name is None or len(obj.user_name) < 1:
            raise InconsistenceException("Por favor, informe o campo user_name.")
        
        if obj.user_email is None or len(obj.user_email) < 1:
            raise InconsistenceException("Por favor, informe o campo user_email.")
        
        usr = self.dataUserRepository.get_by_user_email(obj)
        if usr is not None:
            raise InconsistenceException("Já existe um usuário cadastrado com o email informado.")
        
        obj.id = datetime.now().strftime("%Y%m%d%H%M%S")
        obj.user_identifier = ""
        obj.aws_user_name = obj.user_email
        obj.active = True
        self.dataUserRepository.save(obj)
        return obj

    def add_user_to_group(self, obj: DataUser):

        if obj.id is None or len(obj.id) < 1:
            raise InconsistenceException("Por favor, informe o campo id.")
        
        if obj.group_name is None or len(obj.group_name) < 1:
            raise InconsistenceException("Por favor, informe o campo group_name.")
        
        usr = self.dataUserRepository.get_by_id(obj)

        if usr is None:
            raise InconsistenceException("Usuário não encontrado com o id informado.")
        
        usr.group_name = obj.group_name
        self.dataUserRepository.add_user_to_group(usr)
        
        lst = self.dataAccessRequestRepository.get_by_approved_groups(
            DataAccessRequest(
                group_name=obj.group_name
            )
        )

        self.policyRepository.attach_all_policies_to_user(lst, usr)
    
    def get_by_user_identifier(self, obj: DataUserSchema):
        usr = self.dataUserRepository.get_by_user_identifier(obj)
        if usr is None: return None
        return DataUserSchema(
            id=usr.id,
            user_email=usr.user_email,
            user_identifier=usr.user_identifier,
            user_name=usr.user_name,
            aws_user_name=usr.aws_user_name,
            active=usr.active
        )