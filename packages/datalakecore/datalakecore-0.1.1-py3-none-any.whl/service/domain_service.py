from model.data_domain import DataDomain
from model.data_domain_user import DataDomainUser

from repository.data_domain_repository import DataDomainRepository
from repository.data_domain_user_repository import DataDomainUserRepository

class DomainService:
    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.dataDomainRepository = DataDomainRepository(self.dynamodb)
        self.dataDomainUserRepository = DataDomainUserRepository(self.dynamodb)

    def get_by_user_id(self, data_user_id):
        lst_domains = self.dataDomainUserRepository.get_by_data_user_id(
            DataDomainUser(data_user_id=data_user_id))
        lst = []
        for item in lst_domains:
            domain = self.dataDomainRepository.get_by_id(
                DataDomain(id=item.data_domain_id))
            lst.append(domain)
        return lst