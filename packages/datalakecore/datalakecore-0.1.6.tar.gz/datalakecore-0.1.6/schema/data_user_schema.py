class DataUserSchema:
    def __init__(self,
                 id: str = None,
                 user_email: str = None,
                 user_identifier: str = None,
                 user_name: str = None,
                 aws_user_name: str = None,
                 aws_groups: list[str] = None,
                 active: bool = None,
                 password: str = None,
                 token: str = None
                 ) -> None:
        self.id = id
        self.user_email = user_email
        self.user_identifier = user_identifier
        self.user_name = user_name
        self.aws_user_name = aws_user_name
        self.aws_groups = aws_groups
        self.active = active
        self.password = password
        self.token = token