from schema.upload_schema import UploadSchema
from service.domain_service import DomainService
from util.unauthorized_exception import UnauthorizedException
import util.client as client

import base64
import re

class UploadService:

    def __init__(self) -> None:
        self.domainService = DomainService()
        self.s3 = client.s3_client

    def upload(self, obj: UploadSchema):
        lst_domains = self.domainService.get_by_user_id(obj.user_id)
        lst_filtered = list(filter(lambda x: x.id == obj.domain_id, lst_domains))
        if len(lst_filtered) < 1:
            raise UnauthorizedException("Este usuário não tem permissão para incluir arquivos neste domínio")
        domain = lst_filtered[0]
        emoji_pattern = re.compile("["
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251" 
                           "]+", flags=re.UNICODE)
        
        decode_content = base64.b64decode(obj.filecontent)
        string_removed = emoji_pattern.sub(r'', decode_content.decode('utf-8'))
        no_extension = obj.filename.split(".")[0]
        self.s3.put_object(Bucket="prod-sankhya-data-platform-analytics",Key=f"{domain.domain_name}/{no_extension}/{obj.filename}",Body=string_removed)
