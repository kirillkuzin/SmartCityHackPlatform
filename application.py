from flask import Flask, request, render_template

from registry import Registry
from settings import APPLICATION_SETTINGS, ETHEREUM_SETTINGS

application = Flask(__name__)

certificates_for_verifying = []

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

@application.route("/my_certificates", methods=["GET"])
def my_certificates_page():
    public_key = "0x126F0De2008F0c593b1a3ec6F684B1715c77B7B0"
    registry_contract = Registry(public_key)
    certificates = registry_contract.get_my_certificates()
    return render_template(
        "my_certificates.html",
        certificates=certificates,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ]
    )

@application.route("/agent", methods=["GET"])
def agent_page():
    return render_template(
        "agent.html",
        certificates=certificates_for_verifying,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ]
    )

@application.route("/create_certificate", methods=["GET","POST"])
def create_certificate_page():
    if request.method == "POST":
        certificate_data = request.get_json()
        certificates_for_verifying.append(certificate_data)
    return render_template("create_certificate.html")

if __name__ == "__main__":
    application.run(
        debug=True,
        host="0.0.0.0",
        port=APPLICATION_SETTINGS["PORT"]
    )
