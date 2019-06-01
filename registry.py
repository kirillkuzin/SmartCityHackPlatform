import time
from datetime import datetime, timedelta

from web3 import Web3

from ethereum_core import Ethereum

class Registry(Ethereum):
    ENERGY_TYPES = [
        "Energy of sun",
        "Wind energy",
        "Water energy"
        "Geothermal energy",
        "Low potential thermal energy",
        "Biomass",
        "Biogas",
        "Gas"
    ]

    def verify_certificate(self, certificate_data):
        self.__set_energy_type(certificate_data)
        self.__set_timestamps(certificate_data)
        tx = self.build_tx().create_certificate(
            certificate_data["owner"],
            certificate_data["generating_object"],
            int(certificate_data["energy_type"]),
            int(certificate_data["amount_of_energy"]),
            int(certificate_data["time_of_start_of_production_period"]),
            int(certificate_data["time_of_stop_of_production_period"]),
            int(certificate_data["time_of_destruction"])
        )
        hash = self.send_eth_transaction(tx)

    def transfer_certificate(self, certificate_id, recipient):
        recipient = Web3.toChecksumAddress(recipient)
        tx = self.build_tx().transfer_certificate(
            certificate_id,
            recipient
        )
        hash = self.send_eth_transaction(tx)

    def redeem_certificate(self, certificate_id):
        tx = self.build_tx().redeem_certificate(certificate_id)
        hash = self.send_eth_transaction(tx)

    def set_time_of_destruction(self, certificate_data):
        time_of_destruction = datetime.now() + timedelta(days=1095)
        certificate_data.update({
            "time_of_destruction": \
                f"{time_of_destruction:%Y-%m-%d}"
        })

    def get_all_certificates(self):
        last_certificate_id = self.__get_last_certificate_id()
        certificates = []
        for id in range(last_certificate_id):
            certificate = self.__get_certificate(id)
            certificates.append(certificate)
        return certificates

    def get_my_certificates(self):
        certificates = self.get_all_certificates()
        my_certificates = [certificate for certificate in \
            certificates if certificate["owner"] == self.public_key]
        return my_certificates

    def __get_certificate(self, certificate_id):
        certificate_data = \
           self.registry_contract.call().get_certificate(certificate_id)
        time_of_start_of_production_period = self.__from_timestamp(
            certificate_data[4]
        )
        time_of_stop_of_production_period = self.__from_timestamp(
            certificate_data[5]
        )
        time_of_destruction = self.__from_timestamp(
            certificate_data[6]
        )
        redeemed = "No"
        if certificate_data[7]:
            redeemed = "Yes"
        certificate = {
            "certificate_id": certificate_id,
            "owner": certificate_data[0],
            "generating_object": certificate_data[1],
            "energy_type": self.ENERGY_TYPES[certificate_data[2]],
            "amount_of_energy": certificate_data[3],
            "time_of_start_of_production_period": \
                time_of_start_of_production_period,
            "time_of_stop_of_production_period": \
                time_of_stop_of_production_period,
            "time_of_destruction": time_of_destruction,
            "redeemed": redeemed
        }
        return certificate

    def __get_last_certificate_id(self):
        return self.registry_contract.call().last_certificate_id()

    def __set_timestamps(self, certificate_data):
        time_of_start_of_production_period = \
            self.__to_timestamp(
                certificate_data["time_of_start_of_production_period"]
            )
        time_of_stop_of_production_period = \
            self.__to_timestamp(
                certificate_data["time_of_stop_of_production_period"]
            )
        time_of_destruction = \
            self.__to_timestamp(
                certificate_data["time_of_destruction"]
            )
        certificate_data.update({
            "time_of_start_of_production_period": \
                time_of_start_of_production_period,
            "time_of_stop_of_production_period": \
                time_of_stop_of_production_period,
            "time_of_destruction": time_of_destruction
        })

    def __set_energy_type(self, certificate_data):
        index = 0
        for energy_type in self.ENERGY_TYPES:
            if certificate_data["energy_type"] == energy_type:
                certificate_data.update({
                    "energy_type": index
                })
            index += 1

    def __from_timestamp(self, timestamp):
        correct_datetime = datetime.utcfromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d')
        return correct_datetime

    def __to_timestamp(self, date):
        timestamp = time.mktime(time.strptime(date, "%Y-%m-%d"))
        return int(timestamp)
