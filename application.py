from flask import Flask, request, render_template

application = Flask(__name__)

@application.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")

@application.route("/certificates", methods=["GET"])
def certificates_page():
    return render_template("certificates.html")

@application.route("/my_certificates", methods=["POST"])
def my_certificates_page():
    return render_template("my_certificates.html")

if __name__ == "__main__":
    application.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
