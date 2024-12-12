from repository.glue_connection_repository import GlueConnectionRepository

class GlueConnectionService:
    
    def __init__(self) -> None:
        self.glueConnectionRepository = GlueConnectionRepository()

    def get_all(self):
        return self.glueConnectionRepository.get_all()