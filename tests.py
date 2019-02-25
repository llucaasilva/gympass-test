from unittest import TestCase

from gympass import Gympass
from tests_dicts import test_make_dict_success, test_order_success, test_average_speed_success


class Tests(TestCase):

    log = '..\\gympass-test\\race_log.log'
    log_test = '..\\gympass-test\\race_log_test.log'
    log_test_2 = '..\\gympass-test\\race_log_test_2.log'
    gympass = Gympass()

    def test_make_dict_white_log(self, make_dict=gympass.make_dict(log_test)):
        self.assertEqual('O arquivo de log está em branco.', make_dict)

    def test_make_dict_success(self, make_dict=gympass.make_dict(log)):
        self.assertCountEqual(test_make_dict_success, make_dict)

    def test_order_white_log(self, order=gympass.order(log_test)):
        self.assertEqual('O arquivo de log está em branco.', order)

    def test_order_success(self, order=gympass.order(log)):
        self.assertCountEqual(test_order_success, order)

    def test_average_speed_white_log(self, average_speed=gympass.average_speed(log_test)):
        self.assertEqual('O arquivo de log está em branco.', average_speed)

    def test_average_speed_success(self, average_speed=gympass.average_speed(log)):
        self.assertEqual(test_average_speed_success, average_speed)

    def test_output_white_log(self, output=gympass.output(log_test)):
        self.assertEqual('O arquivo de log está em branco.', output)

    def test_output_success(self, output=gympass.output(log)):
        self.assertIsNot('O arquivo de log está em branco.', 'A corrida ainda não está finalizada, pois nenhum piloto '
                                                             'completou 4 (quatro) voltas ainda.', output)

    def test_output_unfinished(self, output=gympass.output(log_test_2)):
        self.assertEqual('A corrida ainda não está finalizada, pois nenhum piloto completou 4 (quatro) voltas ainda.',
                         output)
