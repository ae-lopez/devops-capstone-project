"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Description: uses Account.all() method to return all accounts as a list of dict
    Parameters: none
    Returns: list of accounts, and return code HTTP_200_OK. empty list if no accounts exist
    """
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    # make a list of the account dicts
    account_list = [acc.serialize() for acc in accounts]
    # return the # of accounts to the log
    app.logger.info("Returning [%s] accounts", len(account_list))

    # return the list with a return code of status.HTTP_200_OK
    return jsonify(account_list), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Description: accepts an account_id and uses Account.find() to find the account
    Parameters: id (int)
    Returns: python dict w/ return code HTTP_200_OK if found, HTTP_404_NOT_FOUND else
    """
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {id} not found")

    return account.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Description: accepts an account_id and updates the account fields
    Parameters: id (int)
    Returns: python dict w/ return code HTTP_200_OK if found, HTTP_404_NOT_FOUND else
    """
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {id} not found")
    account.deserialize(request.get_json())
    account.update()  # update acc with new data
    return account.serialize(), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Description: accepts an account_id and deletes the account
    Parameters: id (int)
    Returns: empty str w/ return code HTTP_404_NOT_FOUND
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    # if account is not found, do nothing
    # if account is found, call delete() method
    if account:
        account.delete()

    # return empty str and 204 status code
    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
