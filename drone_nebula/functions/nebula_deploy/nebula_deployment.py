from typing import Optional
from NebulaPythonSDK import Nebula


class NebulaDeploy:

    def __init__(self, host: Optional[str] = "127.0.0.1", username: Optional[str] = None,
                 password: Optional[str] = None, token: Optional[str] = None, port: int = 80, protocol: str = "http"):
        """Init the nebula api connection object

            Arguments:
                host -- the hostname of the nebula host, defaults to 127.0.0.1
                username -- the username to connect to nebula with, defaults to None
                password -- the password to connect to nebula with, defaults to None
                token -- the token to connect to nebula with, defaults to None
                port --the port of the nebula host, defaults to 80
                protocol -- the protocol of the nebula host, "http" or "https", default to "http"
        """
        self.nebula_connection = Nebula(host=host, username=username, password=password, token=token, port=port,
                                        protocol=protocol)

    def check_nebula_app_exists(self, job_name: str) -> bool:
        """Checks if a given nebula jobs exists or not & raise an error if it can't tell

            Arguments:
                job_name -- a string to apply the templating to without a prefixed slash (/)
            Returns:
                True if the job exists, False if it's not
        """
        response = self.nebula_connection.list_app_info(job_name)
        if response["status_code"] == 200:
            return True
        elif response["status_code"] == 403:
            return False
        else:
            print(response)
            print("failed checking nebula app status")
            raise Exception

    def create_nebula_app(self, job_json: dict) -> dict:
        """creates a nebula jobs & raise an error if it can't

            Arguments:
                job_json -- a dict of the job JSON description (string because it's taken directly from a file)
            Returns:
                response_json -- the response JSON returned from nebula
        """
        response = self.nebula_connection.create_app(job_json["app_name"], job_json)
        if response["status_code"] == 200:
            return response
        else:
            print(response)
            print("failed creating nebula app")
            raise Exception

    def update_nebula_app(self, job_json: dict) -> dict:
        """Updates a nebula jobs & raise an error if it can't

            Arguments:
                job_json -- a dict of the job JSON description (string because it's taken directly from a file)
            Returns:
                response_json -- the response JSON returned from nebula
        """
        response = self.nebula_connection.update_app(job_json["app_name"], job_json, force_all=True)
        if response["status_code"] == 202:
            return response
        else:
            print(response)
            print("failed updating nebula app")
            raise Exception

    def create_or_update_nebula_app(self, job_json: dict) -> dict:
        """Creates a nebula job if it does not exist or updates a nebula jobs if it does exist

            Arguments:
                job_json -- a dict of the job JSON description
            Returns:
                response_json -- the response JSON returned from nebula
        """
        job_exists = self.check_nebula_app_exists(job_json["app_name"])

        if job_exists is False:
            response_json = self.create_nebula_app(job_json)
        elif job_exists is True:
            response_json = self.update_nebula_app(job_json)

        return response_json
