from datetime import datetime

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

    def get_all_certificates(self):
        last_certificate_id = self.__get_last_certificate_id()
        certificates = []
        for id in range(last_certificate_id):
            certificate = self.__get_certificate(id)
            certificates.append(certificate)
        return certificates

    def get_my_certificates(self):
        pass

    def __get_certificate(self, certificate_id):
        certificate_data = \
         self.registry_contract.call().get_certificate(certificate_id)
        time_of_start_of_production_period = self.__from_timestamp(
            certificate_data[4]
        )
        time_of_stop_of_production_period = self.__from_timestamp()
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

    def __from_timestamp(self, timestamp):
        datetime = datetime.utcfromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d %H:%M:%S')
        return datetime
