import unittest
import os
from simulationhelper import SimulationHelper
from src.services.utils import dprint


class TestPerson(unittest.TestCase):
    def setUp(self):
        simulation = SimulationHelper()
        simulation.generate_persons(4)
        self.test_person = simulation.persons

        self.temp_subfolder = "temp_files"
        if not os.path.exists(self.temp_subfolder):
            os.makedirs(self.temp_subfolder)
        simulation.generate_voucher_for_person(0, 1, 2, 100, 5)

        # Create and save the initial voucher
        self.voucher_file_name = "minutoschein.txt"
        self.test_person[0].create_voucher(100, "Frankfurt", 5)
        self.test_person[0].save_voucher(self.voucher_file_name, self.temp_subfolder)

        # Sign the voucher by the male guarantor and save
        self.male_signed_voucher_file_name = "minutoschein-male-signed.txt"
        self.test_person[1].read_voucher_and_save_voucher(self.voucher_file_name, self.temp_subfolder)
        self.test_person[1].sign_voucher_as_guarantor()
        self.test_person[1].save_voucher(self.male_signed_voucher_file_name, self.temp_subfolder)

        # Sign the voucher by the female guarantor and save
        self.male_female_signed_voucher_file_name = "minutoschein-male_female-signed.txt"
        self.test_person[2].read_voucher_and_save_voucher(self.male_signed_voucher_file_name, self.temp_subfolder)
        self.test_person[2].sign_voucher_as_guarantor()
        self.test_person[2].save_voucher(self.male_female_signed_voucher_file_name, self.temp_subfolder)

    def test_voucher_creation_and_persistence(self):
        # Test 1: Create a voucher and save it
        self.test_person[0].create_voucher(100, "Frankfurt", 5)
        original_voucher = self.test_person[0].current_voucher

        original_voucher.save_to_disk(self.voucher_file_name, self.temp_subfolder)
        full_voucher_path = os.path.join(os.getcwd(), self.temp_subfolder, self.voucher_file_name)
        self.assertTrue(os.path.exists(full_voucher_path), "Voucher successfully saved.")

        # Test 2: Initialize an empty voucher and read the saved voucher
        self.test_person[0].read_voucher_and_save_voucher(self.voucher_file_name, self.temp_subfolder)
        self.assertEqual(self.test_person[0].current_voucher, original_voucher, "Data correctly read.")

    def test_male_guarantor_signature(self):
        # Test 3a: Check the signature of the male guarantor
        self.test_person[1].read_voucher_and_save_voucher(self.male_signed_voucher_file_name, self.temp_subfolder)
        self.assertTrue(self.test_person[1].verify_guarantor_signatures(), "Signature of male guarantor successfully verified.")

    def test_female_guarantor_signature(self):
        # Test 3b: Check the signature of the female guarantor
        self.test_person[2].read_voucher_and_save_voucher(self.male_female_signed_voucher_file_name, self.temp_subfolder)
        self.assertTrue(self.test_person[2].verify_guarantor_signatures(), "Signature of female guarantor successfully verified.")

    def test_creator_signature_verification(self):
        # Test 4: Verify the signature of the creator
        self.test_person[0].read_voucher_and_save_voucher(self.male_female_signed_voucher_file_name, self.temp_subfolder)
        self.test_person[0].sign_voucher_as_creator()
        complete_voucher_file_name = "minutoschein-complete.txt"
        self.test_person[0].save_voucher(complete_voucher_file_name, self.temp_subfolder)

        self.test_person[3].read_voucher_and_save_voucher(complete_voucher_file_name, self.temp_subfolder)
        self.assertTrue(self.test_person[3].verify_creator_signature(), "Creator's signature successfully verified.")

    # def tearDown(self):
    #     # Cleanup: Remove test files
    #     for file_name in [self.voucher_file_name, self.male_signed_voucher_file_name, self.male_female_signed_voucher_file_name, "minutoschein-complete.txt"]:
    #         full_path = os.path.join(self.temp_subfolder, file_name)
    #         if os.path.exists(full_path):
    #             os.remove(full_path)

if __name__ == '__main__':
    unittest.main()
