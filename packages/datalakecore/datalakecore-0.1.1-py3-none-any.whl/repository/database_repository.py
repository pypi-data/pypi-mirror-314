from model.database import Database

class DatabaseRepository:

    def __init__(self, client) -> None:
        self.client = client

    def get_all(self):
        response = self.client.get_databases(
            ResourceShareType='ALL',
            AttributesToGet=['NAME']
        )
        lst = []
        for item in response["DatabaseList"]:
            lst.append(
                Database(
                    name=item["Name"]
                )
            )
        return lst