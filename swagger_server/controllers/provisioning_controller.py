import connexion
import six

from swagger_server import util
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.provisioning import Provisioning  # noqa: E501


def create_provisioning(body):  # noqa: E501
    """Send a new provisioning or update to SDX-LC

    Post a Provisioning from SDX-Controller # noqa: E501

    :param body: placed for adding or update a new provisioning
    :type body: dict | bytes

    :rtype: Provisioning
    """
    if connexion.request.is_json:
        body = Dict[str, Object].from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"
