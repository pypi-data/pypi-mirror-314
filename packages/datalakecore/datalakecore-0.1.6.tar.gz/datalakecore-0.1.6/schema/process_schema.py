class ProcessSchema:
    def __init__(self,
                 transformation_id: str = None,
                 data_user_id: str = None
                 ) -> None:
        self.transformation_id = transformation_id
        self.data_user_id = data_user_id