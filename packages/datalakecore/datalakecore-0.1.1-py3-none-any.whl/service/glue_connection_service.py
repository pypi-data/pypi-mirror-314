from repository.glue_connection_repository import GlueConnectionRepository

class GlueConnectionService:
    
    def __init__(self, dynamodb) -> None:
        self.dynamodb = dynamodb
        self.glueConnectionRepository = GlueConnectionRepository(self.dynamodb)

    def get_all(self):
        return self.glueConnectionRepository.get_all()