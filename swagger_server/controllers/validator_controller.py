"""Decorator to validate a REST endpoint input. """
import logging
from pathlib import Path

import connexion

# from swagger_server import util
from openapi_core import create_spec
from openapi_core.contrib.flask import FlaskOpenAPIRequest
from openapi_core.validation.request.validators import RequestValidator
from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename

# from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.validator import Validator  # noqa: E501


def get_validate(body):  # noqa: E501
    """Send a new topology validation or update

    Post a topology validation # noqa: E501

    :param body: placed for adding or update a new validation
    :type body: dict | bytes

    :rtype: Validator
    """
    logging.info(" ################## Validate openapi spec. ####################")
    app_dir = Path(__file__).parent
    logging.info(app_dir)
    yml_file = app_dir / "swagger.yaml"
    spec_dict, _ = read_from_filename(yml_file)
    if validate_spec(spec_dict) and connexion.request.is_json:
        logging.info("########## schema defined in the openapi.yml file ##########")
        spec = create_spec(spec_dict)
        validator = RequestValidator(spec)
        body = validator.from_dict(connexion.request.get_json())  # noqa: E501
        openapi_request = FlaskOpenAPIRequest(body)
        result = validator.validate(openapi_request)
        error_response = {}
        if result.errors:
            errors = result.errors[0]
            if hasattr(errors, "schema_errors"):
                schema_errors = errors.schema_errors[0]
                error_response = {
                    "error_message": schema_errors.message,
                    "error_validator": schema_errors.validator,
                    "error_validator_value": schema_errors.validator_value,
                    "error_path": list(schema_errors.path),
                    "error_schema": schema_errors.schema,
                    "error_schema_path": list(schema_errors.schema_path),
                }
            else:
                error_response = {"errors": errors}
            return (error_response, 400)
    return (body, 200)
