"""
This module describes how we handle org tracking in Sieve
"""
from typing import Any

org_handler = None


class OrgHandler:
    """
    This class handles organization management for approved Sieve organizations.
    """

    def __init__(self):
        self.vars = {}

    def get_organization_variable(self, key: str, default: Any = None) -> Any:
        """
        Get a variable for the organization, returning a default value if the key does not exist.

        :param key: The key for the variable
        :type key: str
        :param default: The default value to return if the key is not found
        :type default: Any
        :return: The value of the variable or the default value
        :rtype: Any
        """
        return self.vars.get(key, default)

    def get_organization_variables(self) -> dict:
        return self.vars

    def set_organization_variable(self, key: str, value: Any) -> None:
        """
        Set a variable for the organization.

        :param key: The key for the variable
        :type key: str
        :param value: The value to set for the variable
        :type value: Any
        """
        self.vars[key] = value

    def set_organization_variables(self, vars: dict) -> None:
        """
        Set multiple variables for the organization.

        :param vars: A dictionary of key-value pairs to set for the organization
        :type vars: dict
        """
        self.vars = vars

    def reset_organization_variables(self) -> None:
        """
        Reset all organization variables to an empty state.
        """
        self.set_organization_variables({})


def get_org_handler():
    global org_handler
    if org_handler is None:
        org_handler = OrgHandler()
    return org_handler


def get_organization_variable(key: str, default: Any = None) -> Any:
    """
    Get a variable for the organization, returning a default value if the key does not exist.

    :param key: The key for the variable
    :type key: str
    :param default: The default value to return if the key is not found
    :type default: Any
    :return: The value of the variable or the default value
    :rtype: Any
    """
    return get_org_handler().get_organization_variable(key, default)


def get_organization_variables() -> dict:
    """
    Get all variables for the organization.

    :return: A dictionary of all organization variables
    :rtype: dict
    """
    return get_org_handler().get_organization_variables()
