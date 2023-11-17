import unittest
import src.models.person
import os

class TestPerson(unittest.TestCase):
    def setUp(self):
        # Setup: Erstelle eine Person
        self.hansdampf = src.models.person.Person(
            "Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789",
            "IT-Support", "50.1109, 8.6821", "2023-12-31",
            "adapt buddy actress swear early offer grow comic code sting hawk marble"
        )
        self.temp_subfolder = "temp_files"
        self.voucher_path = os.path.join(self.temp_subfolder, "testvoucher.txt")

    def test_voucher_creation_and_persistence(self):
        # Test 1: Erstelle einen Voucher und speichere ihn
        self.hansdampf.create_voucher(100, "Frankfurt", "2028")
        original_voucher = self.hansdampf.current_voucher
        original_voucher.save_to_disk(self.voucher_path)
        # Überprüfen, ob die Datei existiert
        self.assertTrue(os.path.exists(self.voucher_path))

        # Test 2: Initialisiere einen leeren Voucher und lese den gespeicherten Voucher ein
        self.hansdampf.init_empty_voucher()
        self.hansdampf.read_voucher_from_file(self.voucher_path)

        # Überprüfen, ob der eingelesene Voucher mit dem originalen übereinstimmt
        self.assertEqual(self.hansdampf.current_voucher, original_voucher)

    def tearDown(self):
        # Aufräumen: Entferne die Testdatei
        os.remove(self.voucher_path)

if __name__ == '__main__':
    unittest.main()
