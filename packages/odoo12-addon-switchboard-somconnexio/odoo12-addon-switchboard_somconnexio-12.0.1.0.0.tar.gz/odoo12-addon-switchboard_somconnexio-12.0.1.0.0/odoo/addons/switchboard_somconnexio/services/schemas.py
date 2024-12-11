from odoo.addons.somconnexio.services.schemas import (
    S_CONTRACT_CREATE as S_BASE_CONTRACT_CREATE,
    S_CONTRACT_SERVICE_INFO_CREATE,
)

S_SWITCHBOARD_CONTRACT_SERVICE_INFO_CREATE = {
    "phone_number_2": {"type": "string"},
    "mobile_phone_number": {"type": "string"},
    "icc": {"type": "string"},
    "agent_name": {"type": "string"},
    "agent_email": {"type": "string"},
    "extension": {"type": "string"},
    "MAC_CPE_SIP": {"type": "string"},
    "SIP_channel_name": {"type": "string"},
    "SIP_channel_password": {"type": "string"},
}

S_CONTRACT_CREATE = {
    **S_BASE_CONTRACT_CREATE,
    "switchboard_service_contract_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_SWITCHBOARD_CONTRACT_SERVICE_INFO_CREATE,
        },
    },
}
