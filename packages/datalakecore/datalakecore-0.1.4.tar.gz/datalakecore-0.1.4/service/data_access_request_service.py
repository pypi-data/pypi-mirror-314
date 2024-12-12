from model.data_access_request import DataAccessRequest

from repository.data_access_request_repository import DataAccessRequestRepository
from repository.policy_repository import PolicyRepository
from repository.approver_repository import ApproverRepository

from util.inconsistence_exception import InconsistenceException
from util.email import Email

from datetime import datetime
import pytz
import hashlib

class DataAccessRequestService:

    def __init__(self) -> None:
        self.sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')
        self.dataAccessRequestRepository = DataAccessRequestRepository()
        self.policyRepository = PolicyRepository()
        self.approverRepository = ApproverRepository()

    def save(self, obj: DataAccessRequest):

        if obj.database is None or len(obj.database) < 1:
            raise InconsistenceException("O atributo database deve ser informado!")
        
        if obj.table_name is None or len(obj.table_name) < 1:
            raise InconsistenceException("O atributo table_name deve ser informado!")
        
        if obj.arn_table is None or len(obj.arn_table) < 1:
            raise InconsistenceException("O atributo arn_table deve ser informado!")
                
        if obj.request_description is None or len(obj.request_description) < 1:
            raise InconsistenceException("O atributo request_description deve ser informado!")
        
        if obj.level_request is None or len(obj.level_request) < 1:
            raise InconsistenceException("O atributo level_request deve ser informado!")
        
        if obj.level_request not in ["PERSONAL", "GROUP"]:
            raise InconsistenceException("Os valores válidos para o atributo level_request são PERSONAL e GROUP!")
        
        if obj.group_name is None or len(obj.group_name) < 1:
            raise InconsistenceException("O atributo group_name deve ser informado!")

        if self.dataAccessRequestRepository.check_exists_request_awaiting_approval_for_user(obj):
            raise InconsistenceException("O usuário já possui uma solicitação para esta tabela com status de aguardando aprovação!")

        lst_da_attached = self.policyRepository.get_user_data_access_attached(obj.data_user_request)

        if len(list(filter(lambda x: x.upper() == obj.arn_table.upper(), lst_da_attached))) > 0:
            raise InconsistenceException("O usuário já possui acesso a esta tabela!")
        
        prefix = obj.arn_table.split("/")[0]
        layer = prefix.split("-")[4]
        sufix = obj.arn_table.split("/")[1]

        date_now = datetime.now(self.sao_paulo_timezone)
        obj.id = date_now.strftime("%Y%m%d%H%M%S")
        obj.dh_request = date_now
        obj.data_user_response = self.approverRepository.get_approver(layer, sufix)
        obj.dh_response = None
        obj.response_description = ""
        obj.level_response = ""
        obj.status = "AWAITING APPROVAL"
        obj.token = hashlib.sha512(bytes(obj.id, "utf-8")).hexdigest()
        obj.token_valid = True
        obj.dh_last_updated = date_now

        self.dataAccessRequestRepository.save(obj)

        link = f"http://sankhya-data-platform-ui.s3-website-sa-east-1.amazonaws.com/aprovacao?token={obj.token}"
        body = ("""
            <html>
                <head>
                	<style type='text/css'>
                		body {
                			font-family: 'Nunito', sans-serif;
                			padding: 15px;
                		}
                		h1 {
						    font-size: 24px;
						    margin-bottom: 0;
						    font-weight: 600;
						    color: #012970;
						}
						p {
							font-size: 16px;
						}
						.button {
							border-radius: 30px;
							background-color: #d5e9f5;
							width: 180px;
							text-align: center;
							padding-top: 15px;
							padding-bottom: 15px;
						}
                	</style>
                </head>
                <body>
                    <h1>Aprovar solicitação de acesso</h1><br/>
                    <p>
                        Olá <b><#1#></b>, como vai?<br/><br/>
                        A solicitação de acesso à tabela <b><#2#>.<#3#></b> enviada pelo colaborador <b><#4#></b> está aguardando a sua aprovação!<br/>
                        Por favor, clique no link abaixo para mais detalhes e avaliação.
                    <p/>

                    	<a href="<#5#>">
                    		<div class="button">
                    	        Acessar solicitação
                    	    </div>
                    	</a>
                    <p>
                    	Atenciosamente,
                    	<br/>
                    	Data Platform Team.
                    	<br/><br/>
                    	<b>Este é um email automático. Por favor, não responda.</b>
                    </p>
                </body>
            </html>
        """.replace("<#1#>", obj.data_user_response.user_name)
           .replace("<#2#>", obj.database)
           .replace("<#3#>", obj.table_name)
           .replace("<#4#>", obj.data_user_request.user_name)
           .replace("<#5#>", link)
        )

        Email().send(
            subject=f"Data Platform: Solicitação de acesso à dados - {obj.data_user_request.user_name} - Tabela {obj.database}.{obj.table_name}",
            destination=obj.data_user_response.user_email,
            body=body
        )

    def close_request(self, obj: DataAccessRequest):

        if obj.token is None or len(obj.token) < 1:
            raise InconsistenceException("O atributo token deve ser informado!")
        
        if obj.response_description is None or len(obj.response_description) < 1:
            raise InconsistenceException("O atributo response_description deve ser informado!")
        
        if obj.level_response is None or len(obj.level_response) < 1:
            raise InconsistenceException("O atributo level_response deve ser informado!")
        
        if obj.level_response not in ["PERSONAL", "GROUP"]:
            raise InconsistenceException("Os valores válidos para o atributo level_response são PERSONAL e GROUP!")
        
        if obj.status is None or len(obj.status) < 1:
            raise InconsistenceException("O atributo status deve ser informado!")
        
        if obj.status not in ["APPROVED", "DENIED"]:
            raise InconsistenceException("Os valores válidos para o atributo status são APPROVED e DENIED!")
        
        request = self.dataAccessRequestRepository.get_by_token(obj)

        if request is None:
            raise InconsistenceException("Não foi encontrada a requisição com o token informado!")
        
        if not request.token_valid:
            raise InconsistenceException("Este token não é mais válido.")
        
        date_now = datetime.now(self.sao_paulo_timezone)

        request.dh_response = date_now
        request.response_description = obj.response_description
        request.level_response = obj.level_response
        request.status = obj.status
        request.token_valid = False
        request.dh_last_updated = date_now

        self.dataAccessRequestRepository.save(request)

        if obj.status == "APPROVED":
            if obj.level_response == "PERSONAL":
                self.policyRepository.attach_policy_user(request)
            else:
                self.policyRepository.attach_policy_group(request)

    def get_by_id(self, obj: DataAccessRequest):

        if obj.id is None or len(obj.id) < 1:
            raise InconsistenceException("O atributo id deve ser informado!")
        
        request = self.dataAccessRequestRepository.get_by_id(obj)

        if request is None:
            raise InconsistenceException("Não foi encontrada a requisição com o id informado!")
        
        return request
    
    def get_by_token(self, obj: DataAccessRequest):

        if obj.token is None or len(obj.token) < 1:
            raise InconsistenceException("O atributo token deve ser informado!")
        
        request = self.dataAccessRequestRepository.get_by_token(obj)

        if request is None:
            raise InconsistenceException("Não foi encontrada a requisição com o token informado!")
        
        if not request.token_valid:
            raise InconsistenceException("Este token não é mais válido.")
        
        return request