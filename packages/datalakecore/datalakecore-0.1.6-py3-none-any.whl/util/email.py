import boto3
import json
import smtplib
from email.mime.text import MIMEText

class Email:

    def __init__(self) -> None:
        session = boto3.session.Session()
        self.client_secretsmanager = session.client(
            service_name='secretsmanager',
            region_name="sa-east-1"
        )

    def send(self, subject: str, destination: str, body: str):
        account, password = self.__get_keys()
        html_message = MIMEText(body, 'html')
        html_message['Subject'] = subject
        html_message['From'] = account
        html_message['To'] = destination
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(account, password)
            server.sendmail(account, destination, html_message.as_string())

    def __get_keys(self):
         get_secret_value_response = self.client_secretsmanager.get_secret_value(
            SecretId="credential-data-platform-google-account"
         )
         values = json.loads(get_secret_value_response['SecretString'])
         return values.get("account"), values.get("password")