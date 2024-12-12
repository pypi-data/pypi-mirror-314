class UploadSchema:
    def __init__(self,
                 domain_id: str = None,
                 filename: str = None,
                 filecontent: any = None,
                 user_id: str = None
                 ) -> None:
        self.domain_id = domain_id
        self.filename = filename
        self.filecontent = filecontent
        self.user_id = user_id