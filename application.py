import json
from flask import Flask, request, render_template

from registry import Registry
from settings import APPLICATION_SETTINGS, ETHEREUM_SETTINGS

application = Flask(__name__)

certificates_for_verifying = []

@application.route("/", methods=["GET"])
def login_page():
    return render_template(
        "login.html",
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ]
    )

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
    owner = request.form.get("owner") or None
    private_key = request.form.get("private_key") or None
    registry_contract = Registry(owner)
    certificates = registry_contract.get_my_certificates()
    return render_template(
        "my_certificates.html",
        certificates=certificates,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner,
        private_key=private_key
    )

@application.route("/agent", methods=["POST"])
def agent_page():
    owner = request.form.get("owner") or None
    private_key = request.form.get("private_key") or None
    return render_template(
        "agent.html",
        certificates=certificates_for_verifying,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner,
        private_key=private_key
    )

@application.route("/create_certificate", methods=["GET", "POST"])
def create_certificate_page():
    owner = None
    if request.method == "GET":
        owner = request.args.get("owner")
    elif request.method == "POST":
        certificate_data = request.form.to_dict()
        registry_contract = Registry()
        registry_contract.set_time_of_destruction(certificate_data)
        certificates_for_verifying.append(certificate_data)
    return render_template(
        "create_certificate.html",
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner
    )

@application.route("/verify_certificate", methods=["POST"])
def verify_certificate_request():
    owner = request.form.get("owner")
    private_key = request.form.get("private_key")
    certificate_index = request.form.get("certificate_index")
    certificate_data = certificates_for_verifying[
        int(certificate_index)
    ]
    registry_contract = Registry(owner, private_key)
    registry_contract.verify_certificate(certificate_data)
    del certificates_for_verifying[int(certificate_index)]
    return render_template(
        "agent.html",
        certificates=certificates_for_verifying,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner,
        private_key=private_key
    )

@application.route("/transfer_certificate", methods=["POST"])
def transfer_certificate_request():
    owner = request.form.get("owner")
    private_key = request.form.get("private_key")
    certificate_id = int(request.form.get("certificate_id"))
    recipient = request.form.get("recipient")
    registry_contract = Registry(owner, private_key)
    registry_contract.transfer_certificate(certificate_id, recipient)
    certificates = registry_contract.get_my_certificates()
    return render_template(
        "my_certificates.html",
        certificates=certificates,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner,
        private_key=private_key
    )

@application.route("/redeem_certificate", methods=["POST"])
def redeem_certificate_request():
    owner = request.form.get("owner")
    private_key = request.form.get("private_key")
    certificate_id = int(request.form.get("certificate_id"))
    registry_contract = Registry(owner, private_key)
    registry_contract.redeem_certificate(certificate_id)
    certificates = registry_contract.get_my_certificates()
    return render_template(
        "my_certificates.html",
        certificates=certificates,
        smart_contract_address=ETHEREUM_SETTINGS[
            "REGISTRY_CONTRACT_ADDRESS"
        ],
        owner=owner,
        private_key=private_key
    )

if __name__ == "__main__":
    application.run(
        debug=True,
        host="0.0.0.0",
        port=APPLICATION_SETTINGS["PORT"]
    )
