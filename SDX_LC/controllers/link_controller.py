import connexion
import six

from swagger_server import util
from swagger_server.models.link import Link  # noqa: E501


def add_link(body):  # noqa: E501
    """add a new link to the topology

     # noqa: E501

    :param body: link object that needs to be sent to the SDX LC
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Link.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"


def delete_link(node_id, api_key=None):  # noqa: E501
    """Deletes a link

     # noqa: E501

    :param node_id: ID of link to delete
    :type node_id: int
    :param api_key:
    :type api_key: str

    :rtype: None
    """
    return "do some magic!"


def get_link():  # noqa: E501
    """get an existing link

    ID of the link # noqa: E501


    :rtype: None
    """
    return "do some magic!"


def update_link(body):  # noqa: E501
    """Update an existing link

    ID of link that needs to be updated. # noqa: E501

    :param body: link object that needs to be sent to the SDX LC
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Link.from_dict(connexion.request.get_json())  # noqa: E501
    return "do some magic!"
