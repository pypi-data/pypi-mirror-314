from model.table_analytics import TableAnalytics
from datetime import datetime
from repository.data_domain_repository import DataDomainRepository
from repository.data_user_repository import DataUserRepository


class TableAnalyticsRepository:

    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.dataDomainRepository = DataDomainRepository(dynamodb)
        self.dataUserRepository = DataUserRepository(dynamodb)

    def get_actives(self):
        resp = self.dynamodb.execute_statement(
           Statement=f"select * from table_analytics where active = true"
        )
        return self.__read(resp)
    
    def get_by_id(self, id):
        resp = self.dynamodb.execute_statement(
           Statement=f"select * from table_analytics where id=?",
           Parameters=[{"S": id}]
        )
        return self.__read(resp)
    
    def get_by_domain_id(self, lst):
        in_clausule = ""
        sep = ""
        for x in lst:
            in_clausule += sep + f"'{x.data_domain_id}'"
            sep = ","
        resp = self.dynamodb.execute_statement(
           Statement=f"select * from table_analytics where data_domain_id in ({in_clausule})"
        )
        return self.__read(resp)

    def update(self, table):
        self.dynamodb.execute_statement(
            Statement=f"""update table_analytics 
                             set last_execution = '{table.last_execution.strftime("%Y-%m-%d %H:%M:%S")}'
                           where id = '{table.id}'
                             and data_domain_id = '{table.data_domain.id}'"""
            )

    def check_exists(self, obj: TableAnalytics):
        resp = self.dynamodb.execute_statement(
           Statement="SELECT * FROM table_analytics WHERE name=? and data_domain_id=? and id!=?",
           Parameters=[{"S": obj.name},
                       {"S": obj.data_domain.id},
                       {"S": obj.id}]
        )
        return True if len(resp['Items']) > 0 else False

    def save(self, obj: TableAnalytics):
        self.dynamodb.put_item(
            TableName="table_analytics", 
            Item={
                "id": {"S": obj.id},
                "data_domain_id": {"S": obj.data_domain.id},
                "data_user_id": {"S": obj.data_user.id},
                "env": {"S": obj.env},
                "query": {"S": obj.query},
                "name": {"S": obj.name},
                "last_execution": {"S": obj.last_execution.strftime("%Y-%m-%d %H:%M:%S")},
                "active": {"BOOL": obj.active}
            }
        )

    def __read(self, resp):
        lst_domains = self.dataDomainRepository.get_all()
        lst_users = self.dataUserRepository.get_all()
        lst =[]
        for item in resp['Items']:
            lst.append(
                TableAnalytics(
                    id=item["id"]["S"],
                    data_domain=list(filter(lambda x: (x.id == item["data_domain_id"]["S"]), lst_domains))[0],
                    data_user=list(filter(lambda x: (x.id == item["data_user_id"]["S"]), lst_users))[0],
                    env=item["env"]["S"],
                    query=item["query"]["S"],
                    name=item["name"]["S"],
                    last_execution=datetime.strptime(item["last_execution"]["S"], "%Y-%m-%d %H:%M:%S") if len(item["last_execution"]["S"]) > 0 else None,
                    active=item["active"]["BOOL"]
                )
            )
        return lst