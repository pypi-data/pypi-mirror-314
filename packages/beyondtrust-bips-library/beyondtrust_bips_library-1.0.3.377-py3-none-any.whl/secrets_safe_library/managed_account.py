"""ManagedAccount Module, all the logic to retrieve managed accounts from PS API"""

import logging

import requests
from cerberus import Validator

from secrets_safe_library import exceptions, secrets, utils


class ManagedAccount(secrets.Secrets):

    _authentication = None
    _logger = None
    _separator = None
    _sign_app_out_error_message = "Error in sign_app_out"

    def __init__(self, authentication, logger=None, separator="/"):
        self._authentication = authentication
        self._logger = logger

        # Schema rules used for validations
        self._schema = {
            "system_name": {"type": "string", "maxlength": 129},
            "account_name": {"type": "string", "maxlength": 246},
        }
        self._validator = Validator(self._schema)

        if len(separator.strip()) != 1:
            raise exceptions.LookupError(f"Invalid separator: {separator}")
        self._separator = separator

    def get_secret(self, path):
        """
        Get Managed account by path
        Arguments:
            path
        Returns:
            Retrieved managed account string
        """

        utils.print_log(
            self._logger,
            "Running get_secret method in ManagedAccount class",
            logging.DEBUG,
        )
        managed_account_dict = self.managed_account_flow([path])
        return managed_account_dict[path]

    def get_secret_with_metadata(self, path):
        """
        Get Managed account with metadata by path
        Arguments:
            path
        Returns:
             Retrieved managed account in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secret method in ManagedAccount class",
            logging.DEBUG,
        )
        managed_account_dict = self.managed_account_flow([path], get_metadata=True)
        return managed_account_dict

    def get_secrets(self, paths):
        """
        Get Managed accounts by paths
        Arguments:
            paths list
        Returns:
            Retrieved managed account in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secrets method in ManagedAccount class",
            logging.INFO,
        )
        managed_account_dict = self.managed_account_flow(paths)
        return managed_account_dict

    def get_secrets_with_metadata(self, paths):
        """
        Get Managed accounts with metadata by paths
        Arguments:
            paths list
        Returns:
            Retrieved managed account in dict format
        """

        utils.print_log(
            self._logger,
            "Running get_secrets method in ManagedAccount class",
            logging.INFO,
        )
        managed_account_dict = self.managed_account_flow(paths, get_metadata=True)
        return managed_account_dict

    def managed_account_flow(self, paths, get_metadata=False):
        """
        Mangaed account by path flow
        Arguments:
            paths list
        Returns:
            Response (Dict)
        """

        response = {}

        for path in paths:

            utils.print_log(
                self._logger,
                f"**************** managed account path: {path} ****************",
                logging.INFO,
            )
            data = path.split(self._separator)

            if len(data) != 2:
                raise exceptions.LookupError(
                    f"Invalid managed account path: {path}. Use '{self._separator}' as a delimiter: system_name{self._separator}managed_account_name"
                )

            system_name = data[0]
            managed_account_name = data[1]

            manage_account_response = self.get_managed_accounts(
                system_name, managed_account_name
            )

            if manage_account_response.status_code != 200:
                raise exceptions.LookupError(
                    f"Error getting the manage account, message: {manage_account_response.text}, statuscode: {manage_account_response.status_code}, system name: {system_name}, managed account name: {managed_account_name}"
                )

            manage_account = manage_account_response.json()

            if get_metadata:
                response[f"{path}-metadata"] = manage_account

            utils.print_log(
                self._logger, "Managed account info retrieved", logging.DEBUG
            )

            create_request_response = self.create_request(
                manage_account["SystemId"], manage_account["AccountId"]
            )

            if create_request_response.status_code not in (200, 201):
                if not self._authentication.sign_app_out():
                    utils.print_log(
                        self._logger, self._sign_app_out_error_message, logging.ERROR
                    )
                raise exceptions.LookupError(
                    f"Error creating the request, message: {create_request_response.text}, statuscode: {create_request_response.status_code}"
                )

            request_id = create_request_response.json()

            utils.print_log(
                self._logger,
                f"Request id retrieved: {'*' * len(str(request_id))}",
                logging.DEBUG,
            )

            if not request_id:
                raise exceptions.LookupError("Request Id not found")

            get_credential_by_request_id_response = self.get_credential_by_request_id(
                request_id
            )

            if get_credential_by_request_id_response.status_code != 200:
                if not self._authentication.sign_app_out():
                    utils.print_log(
                        self._logger, self._sign_app_out_error_message, logging.ERROR
                    )
                raise exceptions.LookupError(
                    f"Error getting the credential by request_id, message: {get_credential_by_request_id_response.text}, statuscode: {get_credential_by_request_id_response.status_code}"
                )

            credential = get_credential_by_request_id_response.json()

            response[path] = credential

            utils.print_log(
                self._logger, "Credential was successfully retrieved", logging.INFO
            )

            request_check_in_response = self.request_check_in(request_id)

            if request_check_in_response.status_code != 204:
                if not self._authentication.sign_app_out():
                    utils.print_log(
                        self._logger, self._sign_app_out_error_message, logging.ERROR
                    )
                raise exceptions.LookupError(
                    f"Error checking in the request, message: {request_check_in_response.text}, statuscode: {request_check_in_response.status_code}"
                )

            utils.print_log(self._logger, "Request checked in", logging.DEBUG)
        return response

    def get_managed_accounts(
        self, system_name: str, account_name: str
    ) -> requests.Response:
        """
        Get managed accounts by system name and account name
        Arguments:
            system_name (str): The name of the system where the account is managed.
            account_name (str): The name of the account to retrieve.

        Returns:
            requests.Response: A response object containing the managed account
                details.

        Raises:
            exceptions.OptionsError: If either system_name or account_name are not valid.
        """
        attributes = {"system_name": system_name, "account_name": account_name}
        if self._validator.validate(attributes, update=True):
            url = f"{self._authentication._api_url}/ManagedAccounts?systemName={system_name}&accountName={account_name}"
            utils.print_log(
                self._logger,
                f"Calling get_managed_accounts endpoint {url}",
                logging.DEBUG,
            )
            response = self._authentication._req.get(
                url,
                timeout=(
                    self._authentication._timeout_connection_seconds,
                    self._authentication._timeout_request_seconds,
                ),
            )
            return response
        else:
            raise exceptions.OptionsError(f"Please check: {self._validator.errors}")

    def create_request(self, system_id, account_id):
        """
        Create request by system id and account id
        Arguments:
            System id, Account id
        Returns:
            Request id
        """
        payload = {
            "SystemID": system_id,
            "AccountID": account_id,
            "DurationMinutes": 5,
            "Reason": "Secrets Safe Integration",
            "ConflictOption": "reuse",
        }

        url = f"{self._authentication._api_url}/Requests"
        utils.print_log(
            self._logger, f"Calling create_request endpoint: {url}", logging.DEBUG
        )
        response = self._authentication._req.post(
            url,
            json=payload,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )
        return response

    def get_credential_by_request_id(self, request_id):
        """
        Get Credential by request id
        Arguments:
            Request id
        Returns:
            Credential info
        """

        url = f"{self._authentication._api_url}/Credentials/{request_id}"
        print_url = (
            f"{self._authentication._api_url}/Credentials/{'*' * len(str(request_id))}"
        )

        utils.print_log(
            self._logger,
            f"Calling get_credential_by_request_id endpoint: {print_url}",
            logging.DEBUG,
        )
        response = self._authentication._req.get(
            url,
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )
        return response

    def request_check_in(self, request_id):
        """
        Expire request
        Arguments:
            Request id
        Returns:
            Informative text
        """
        url = f"{self._authentication._api_url}/Requests/{request_id}/checkin"
        print_url = f"{self._authentication._api_url}/Requests/{'*' * len(str(request_id))}/checkin"

        utils.print_log(
            self._logger,
            f"Calling request_check_in endpoint: {print_url}",
            logging.DEBUG,
        )
        response = self._authentication._req.put(
            url,
            json={},
            timeout=(
                self._authentication._timeout_connection_seconds,
                self._authentication._timeout_request_seconds,
            ),
        )
        return response
