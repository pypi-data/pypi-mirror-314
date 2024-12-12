from model.data_access_request import DataAccessRequest
from model.data_user import DataUser

import util.client as client

import json

class PolicyRepository:

    def __init__(self) -> None:
        self.iam_client = client.iam_client
        
    def get_user_data_access_attached(self, user: DataUser):
        lstP = self.__get_all_data_policies(user.aws_user_name)
        return self.__get_user_files_attached(lstP)
        
    def attach_policy_group(self, data: DataAccessRequest):
        group_details = self.iam_client.get_group(
            GroupName=data.group_name
        )
        for user in group_details['Users']:
            self.__define_data_access_policies_for_user(data.arn_table, user['UserName'])

    def attach_policy_user(self, data: DataAccessRequest):
        self.__define_data_access_policies_for_user(data.arn_table, data.data_user_request.aws_user_name)

    def attach_all_policies_to_user(self, lst: list[DataAccessRequest], usr: DataUser):
        lstF = []
        for item in lst:
            lstF.append(item.arn_table)
        self.__define_access_by_list(lstF, usr.aws_user_name)

    def __define_data_access_policies_for_user(self, arn_table: str, aws_user_name: str):
        lstP = self.__get_all_data_policies(aws_user_name)
        lstF = self.__get_user_files_attached(lstP)

        if len(list(filter(lambda x: x.upper() == arn_table.upper(), lstF))) > 0:
            return
        else:
            lstF.append(arn_table)

        self.__detach_user_policy(lstP, aws_user_name)
        self.__delete_policies(lstP)
        self.__define_access_by_list(lstF, aws_user_name)

    def __get_all_data_policies(self, aws_user_name: str):
        response = self.iam_client.list_policies(
            Scope="Local",
            OnlyAttached=False,
            MaxItems=999
        )
        lst = []
        for item in response.get("Policies"):
            if f"policy_data_{aws_user_name}" in item.get("PolicyName"):
                lst.append((item.get("PolicyName"), item.get("Arn"), item.get("DefaultVersionId")))
        return lst
    
    def __get_user_files_attached(self, lstP):
        lst = []
        for item in lstP:
            policy_version = self.iam_client.get_policy_version(
                PolicyArn = item[1], 
                VersionId = item[2]
            )
            statement = policy_version['PolicyVersion']['Document']['Statement']
            if len(statement) > 0:
                for resource in statement[0]["Resource"]:
                    lst.append(resource)
        return lst
    
    def __detach_user_policy(self, lstP, aws_user_name: str):
        for item in lstP:
            self.iam_client.detach_user_policy(
                UserName=aws_user_name,
                PolicyArn=item[1]
            )

    def __delete_policies(self, lstP):
        for item in lstP:
            response = self.iam_client.list_policy_versions(
                PolicyArn=item[1]
            )
            for versions in response.get("Versions"):
                if not versions.get("IsDefaultVersion"):
                    self.iam_client.delete_policy_version(
                        PolicyArn=item[1],
                        VersionId=versions.get("VersionId")
                    )
            self.iam_client.delete_policy(
                PolicyArn=item[1]
            )

    def __define_access_by_list(self, lstF, aws_user_name):
        document = None
        temp = None
        index = 0
        lst_arn = []
        for item in lstF:
            if document is None:
               document = self.__get_policy_template()
               temp = self.__get_policy_template()
            temp["Statement"][0]["Resource"].append(item)   
            if len(json.dumps(temp, separators=(',', ':'))) <= 6144:
                document["Statement"][0]["Resource"].append(item)
            else:
                index += 1
                lst_arn.append(
                    self.__create_policy(
                        policy_name=f"policy_data_{aws_user_name}_{index}",
                        document=document
                    )
                )
                document = None
                temp = None
                document = self.__get_policy_template()
                temp = self.__get_policy_template()
                temp["Statement"][0]["Resource"].append(item)
                document["Statement"][0]["Resource"].append(item)

        if document is not None:
            index += 1
            lst_arn.append(
                self.__create_policy(
                    policy_name=f"policy_data_{aws_user_name}_{index}",
                    document=document
                )
            )
        for item in lst_arn:
            self.iam_client.attach_user_policy(
                UserName=aws_user_name,
                PolicyArn=item
            )

    def __create_policy(self, policy_name: str, document):
        response = self.iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(document),
            Description="Policy de controle de acessos à dados do usuário"
        )
        return response.get("Policy").get("Arn")

    def __get_policy_template(self):
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Resource": [],
                    "Sid": "AllowUserToReadObject"
                }
            ]
        }