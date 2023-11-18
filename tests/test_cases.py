import unittest
import src.models.person
import os

class TestPerson(unittest.TestCase):
    def setUp(self):
        # Setup: Erstelle verschiedene Personen
        self.hansdampf = src.models.person.Person(
            "Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789",
            "IT-Support", "50.1109, 8.6821", "2023-12-31",
            "adapt buddy actress swear early offer grow comic code sting hawk marble"
        )
        self.buerge_weiblich = src.models.person.Person(
            "Susi Musterfrau", "Musterstraße 2", 2, "susi@example.com", "0123456789", "Backen",
            "50.1109, 8.6821", "2023-12-31",
            "rookie era bamboo industry group furnace axis disorder economy silly action invite"
        )
        self.buerge_maennlich = src.models.person.Person(
            "Hans Müller", "Straße 6", 1, "hans@mail.com", "0172653214", "Sport, Handwerk",
            "50.1109, 8.6821", "2023-12-31",
            "strong symptom minor attract math clock pool elite half guess album close"
        )
        self.user1 = src.models.person.Person(
            "Franz Müller", "Weg 3", 1, "franzi@gmx.com", "0717-362541", "Ich kann viel",
            "51.56, 8.22", "2023-12-31",
            "orchard honey actor together basket wasp ankle wire eyebrow clever ensure expose"
        )

        self.temp_subfolder = "temp_files"
        if not os.path.exists(self.temp_subfolder):
            os.makedirs(self.temp_subfolder)

        # Erstellen und Speichern des initialen Vouchers
        self.voucher_path = os.path.join(self.temp_subfolder, "minutoschein.txt")
        self.hansdampf.create_voucher(100, "Frankfurt", 5)
        self.hansdampf.current_voucher.save_to_disk(self.voucher_path)

        # Signieren des Vouchers durch den männlichen Bürgen und Speichern
        self.male_signed_voucher_path = os.path.join(self.temp_subfolder, "minutoschein-male-signed.txt")
        self.buerge_maennlich.read_voucher_from_file(self.voucher_path)
        self.buerge_maennlich.sign_voucher_as_guarantor()
        self.buerge_maennlich.current_voucher.save_to_disk(self.male_signed_voucher_path)

        # Signieren des Vouchers durch den weiblichen Bürgen und Speichern
        self.male_female_signed_voucher_path = os.path.join(self.temp_subfolder, "minutoschein-male_female-signed.txt")
        self.buerge_weiblich.read_voucher_from_file(self.male_signed_voucher_path)
        self.buerge_weiblich.sign_voucher_as_guarantor()
        self.buerge_weiblich.current_voucher.save_to_disk(self.male_female_signed_voucher_path)


    def test_voucher_creation_and_persistence(self):
        # Test 1: Erstelle einen Voucher und speichere ihn
        self.hansdampf.create_voucher(100, "Frankfurt", 5)
        original_voucher = self.hansdampf.current_voucher
        original_voucher.save_to_disk(self.voucher_path)
        self.assertTrue(os.path.exists(self.voucher_path), "Voucher erfolgreich gespeichert.")

        # Test 2: Initialisiere einen leeren Voucher und lese den gespeicherten Voucher ein
        self.hansdampf.read_voucher_from_file(self.voucher_path)
        self.assertEqual(self.hansdampf.current_voucher, original_voucher, "Daten korrekt eingelesen.")

    def test_male_guarantor_signature(self):
        # Test 3a: Überprüfen der Unterschrift des männlichen Bürgen
        self.buerge_maennlich.read_voucher_from_file(self.male_signed_voucher_path)
        self.assertTrue(self.buerge_maennlich.verify_guarantor_signatures(), "Signatur von männlichem Bürgen erfolgreich geprüft.")

    def test_female_guarantor_signature(self):
        # Test 3b: Überprüfen der Unterschrift des weiblichen Bürgen
        self.buerge_weiblich.read_voucher_from_file(self.male_female_signed_voucher_path)
        self.assertTrue(self.buerge_weiblich.verify_guarantor_signatures(), "Signatur von weiblichem Bürgen erfolgreich geprüft.")

    def test_creator_signature_verification(self):
        # Test 4: Überprüfen der Unterschrift des Erstellers
        self.hansdampf.read_voucher_from_file(self.male_female_signed_voucher_path)
        self.hansdampf.sign_voucher_as_creator()
        complete_voucher_path = os.path.join(self.temp_subfolder, "minutoschein-complete.txt")
        self.hansdampf.current_voucher.save_to_disk(complete_voucher_path)

        self.user1.read_voucher_from_file(complete_voucher_path)
        self.assertTrue(self.user1.verify_creator_signature(), "Signatur des Erstellers erfolgreich verifiziert.")

    def tearDown(self):
        # Aufräumen: Entferne die Testdateien
        if os.path.exists(self.voucher_path):
            os.remove(self.voucher_path)

        # Entferne weitere Dateien, falls vorhanden
        for file_name in ["minutoschein.txt", "minutoschein-male-signed.txt", "minutoschein-male_female-signed.txt", "minutoschein-complete.txt"]:
            full_path = os.path.join(self.temp_subfolder, file_name)
            if os.path.exists(full_path):
                os.remove(full_path)

if __name__ == '__main__':
    unittest.main()
