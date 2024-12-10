import unittest
import datetime
from bubot.buject.User.User import User
from bubot_helpers.Helper import async_test
from src.Bubot.Helpers.Сryptography.Certificate import Cert
from bubot.core.DataBase.Mongo import Mongo as Storage


class TestUser(unittest.TestCase):
    cert_org = {
        'serial_number': '41381978065561091994731324769538318095',
        'begin': datetime.datetime(2019, 5, 15, 6, 50, 3),
        'end': datetime.datetime(2020, 8, 15, 6, 50, 3),
        'subject_street': 'линия.Починки 8-я, 20',
        'subject_ST': '76 Ярославская область',
        'subject_L': 'г.Ярославль',
        'subject_Country': 'RU',
        'subject_GN': 'Михаил Александрович',
        'subject_SN': 'Разговоров',
        'subject_CN': 'ООО "БУСИНКА"',
        'subject_T': 'Директор',
        'subject_OU': '0',
        'subject_O': 'ООО "БУСИНКА"',
        'subject_E': '1338833@gmail.com',
        'subject_INN': '007604140564',
        'subject_SNILS': '05387858712',
        'subject_OGRN': '1087604016818'
    }
    cert_man = {
        'serial_number': '36065066082418996484377233615206272122',
        'begin': datetime.datetime(2019, 2, 5, 11, 6, 35),
        'end': datetime.datetime(2020, 5, 5, 11, 6, 35),
        'subject_ST': '76 Ярославская область',
        'subject_L': 'Ярославль',
        'subject_Country': 'RU',
        'subject_GN': 'Михаил Александрович',
        'subject_SN': 'Разговоров',
        'subject_CN': 'Разговоров Михаил Александрович',
        'subject_E': 'razgovorov@tensor.ru',
        'subject_INN': '760201520536',
        'subject_SNILS': '05387858712'
    }

    @async_test
    async def test_create(self):

        storage = await Storage.connect()
        user = User(storage)
        cert = Cert(data=self.cert_org)
        await user.find_by_cert(cert, True)
        pass

