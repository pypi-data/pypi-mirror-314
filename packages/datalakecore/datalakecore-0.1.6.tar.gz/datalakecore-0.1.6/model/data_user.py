class DataUser:
    def __init__(self,
                 id: str = None,
                 user_email: str = None,
                 user_identifier: str = None,
                 user_name: str = None,
                 aws_user_name: str = None,
                 aws_groups: list[str] = None,
                 group_name: str = None,
                 aws_access_key_id: str = None,
                 aws_secret_access_key: str = None,
                 active: bool = None
                 ) -> None:
        self.id = id
        self.user_email = user_email
        self.user_identifier = user_identifier
        self.user_name = user_name
        self.aws_user_name = aws_user_name
        self.aws_groups = aws_groups
        self.group_name = group_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.active = active