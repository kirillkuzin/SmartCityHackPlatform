from flask import Flask, request, render_template

from registry import Registry
from settings import APPLICATION_SETTINGS, ETHEREUM_SETTINGS

application = Flask(__name__)

@application.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")

@application.route("/certificates", methods=["GET"])
def certificates_page():
    registry_contract = Registry()
    certificates = registry_contract.get_all_certificates()
    return render_template(
        "certificates.html",
        certificates=certificates,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ]
    )

@application.route("/my_certificates", methods=["POST"])
def my_certificates_page():
    return render_template("my_certificates.html")

if __name__ == "__main__":
    application.run(
        debug=True,
        host="0.0.0.0",
        port=APPLICATION_SETTINGS["PORT"]
    )
