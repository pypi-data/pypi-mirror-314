from pcli import db
from pcli.responses import NoOrganizationException


def validate_organization():
    organization_data = db.get("organization")

    if not organization_data:
        raise NoOrganizationException(
            "You are currently not logged in. Please login in to your account (command: 'perian login')."
        )

    return organization_data


def generate_organization_header(organization_data: dict):
    return {
        "X-PERIAN-AUTH-ORG": organization_data["name"],
        "Authorization": "Bearer " + organization_data["token"],
    }
