import requests
from pcli import db
from pcli.util.organization import generate_organization_header
from pcli.responses import (
    DefaultApiException,
    NoOrganizationException,
    AuthenticationFailedException
)

def get_organization(organization_data: dict):
    try:
        response = requests.get(db.get("perian_endpoint") + "/organization", headers=generate_organization_header(organization_data))
        response = response.json()

        if response['status_code'] is not 200:
            raise Exception(response)

        return response

    except Exception as e:
        if "The given organization could not be found." in str(e):
            raise NoOrganizationException("We could not validate your login information. Please check your login data.")
        if "Invalid API token" in str(e):
            raise AuthenticationFailedException("We could not validate your login information. Please check your login data.")
        raise DefaultApiException(DefaultApiException.detail + "\n\n" + str(e))