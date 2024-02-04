# test_cases.py
import unittest
import os
from tests.models.simulationhelper import SimulationHelper
from tests.services.utils import modify_voucher, compare_and_highlight_differences
from src.models.minuto_voucher import VoucherStatus

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

    def test_transaction(self):
        """
        Test the transaction simulation.
        """
        sim = SimulationHelper()
        sim.simulation_folder = 'simulation'
        sim.generate_persons(5)
        sim.generate_voucher_for_person(0, 1, 2, 1000, 5)
        sim.generate_voucher_for_person(1, 3, 4, 1000, 5)

        # Simulate transactions and assert the result is True
        result = sim.simulate_transaction(20)
        self.assertTrue(result, "Transaction simulation returned True.")

    def test_corruption_of_vouchers(self):
        # Testing the corruption of vouchers in different scenarios to ensure robustness
        from src.models.minuto_voucher import MinutoVoucher
        sim = SimulationHelper(print_info=False)
        sim.simulation_folder = 'simulation'  # speicherort
        sim.generate_persons(3)  # anzahl der personen die erstellt werden
        sim.generate_voucher_for_person(0, 1, 2, 100, 5)

        sim.send_amount(0, 1, 50)
        sim.send_amount(1, 2, 50)
        sim.send_amount(2, 1, 50)
        sim.send_amount(1, 2, 22.2)

        original_voucher_dict = sim.persons[2].voucherlist[VoucherStatus.OTHER.value][0].save_to_disk(simulation=True)

        # complete random voucher modification of one single char
        for i in range(20):
            modified_voucher_dict = modify_voucher(original_voucher_dict, "all")
            corrupt_voucher = MinutoVoucher()
            corrupt_voucher = corrupt_voucher.read_from_file(modified_voucher_dict, simulation=True)
            if corrupt_voucher.verify_complete_voucher() == True:
                compare_and_highlight_differences(original_voucher_dict,modified_voucher_dict)

            assert corrupt_voucher.verify_complete_voucher() == False

        # random modification only voucher part (one single char)
        for i in range(20):
            modified_voucher_dict = modify_voucher(original_voucher_dict, "voucher")
            corrupt_voucher = MinutoVoucher()
            corrupt_voucher = corrupt_voucher.read_from_file(modified_voucher_dict, simulation=True)

            assert corrupt_voucher.verify_creator_signature() == False
            assert corrupt_voucher.verify_complete_voucher() == False

        # random modification only guarantor_signatures part (one single char), all tests should fail
        for i in range(20):
            modified_voucher_dict = modify_voucher(original_voucher_dict, "guarantor")
            corrupt_voucher = MinutoVoucher()
            corrupt_voucher = corrupt_voucher.read_from_file(modified_voucher_dict, simulation=True)
            # todo somtimes check fails. (determine what was modified)
            assert corrupt_voucher.verify_all_guarantor_signatures() == False
            assert corrupt_voucher.verify_complete_voucher() == False

        # random modification only transactions part (one single char)
        for i in range(20):
            modified_voucher_dict = modify_voucher(original_voucher_dict, "transactions")
            corrupt_voucher = MinutoVoucher()
            corrupt_voucher = corrupt_voucher.read_from_file(modified_voucher_dict, simulation=True)
            assert corrupt_voucher.verify_all_guarantor_signatures() == True
            assert corrupt_voucher.verify_creator_signature() == True
            assert corrupt_voucher.verify_all_transactions() == False
            assert corrupt_voucher.verify_complete_voucher() == False

    def test_double_spending_detection(self):
        """
        Test the detection of double spending within the transaction simulation.
        This involves creating a simulation with multiple persons and vouchers, simulating
        transactions, including attempts at double spending, and then checking if the
        simulation accurately identifies the double spenders.
        """
        sim = SimulationHelper()
        sim.simulation_folder = 'simulation'  # Storage location
        sim.generate_persons(7)  # Create 7 persons

        sim.generate_voucher_for_person(0, 1, 2, 100, 5)

        sim.send_amount(0, 1, 50)

        sim_dspender_ids = []
        # 3 ids (persons) do double spending
        sim_dspender_ids += [sim.send_amount_double_spend(0, 4, 49, 5, 48)]
        sim_dspender_ids += [sim.send_amount_double_spend(1, 2, 47, 3, 46)]
        sim_dspender_ids += [sim.send_amount_double_spend(2, 3, 45, 4, 44)]

        # simulation 30 random transactions
        sim.simulate_transaction(30)

        # Check for double spenders in all persons
        dspender = []
        for person in sim.persons:
            dspender += person.check_double_spending()

        dspender_ids = list(set([item['double_spender_id'] for item in dspender]))

        # Assert that the identified double spenders match the expected ones
        self.assertEqual(sorted(dspender_ids), sorted(sim_dspender_ids),
                         "Detected double spenders should match expected ones.")

    def test_encryption_decryption(self):
        """
        Test the encryption and decryption process of vouchers using Diffie-Hellman key exchange.
        This includes generating persons and vouchers, encrypting a voucher, saving it to a file,
        then decrypting it and verifying the integrity of the decrypted data.
        """
        from src.models.minuto_voucher import MinutoVoucher
        from src.models.secure_file_handler import SecureFileHandler

        sim = SimulationHelper()
        sim.simulation_folder = 'simulation'  # Storage location
        sim.generate_persons(7)  # Create 7 persons
        sim.generate_voucher_for_person(0, 1, 2, 100, 5)

        sim.send_amount(0, 1, 50)

        filehandler = SecureFileHandler()

        # Test encryption with password
        filehandler.encrypt_and_save(sim.persons[1].voucherlist[VoucherStatus.OTHER.value][0], "secure_voucher.txt", "mypassword")
        decrypted_data = filehandler.decrypt_and_load("secure_voucher.txt", "mypassword", MinutoVoucher)
        self.assertTrue(decrypted_data.verify_complete_voucher())
        self.assertEqual(sim.persons[1].voucherlist[VoucherStatus.OTHER.value][0], decrypted_data)


        # Test encryption with Diffie-Hellman key exchange
        filehandler.encrypt_with_shared_secret_and_save(sim.persons[1].voucherlist[VoucherStatus.OTHER.value][0], "secure_voucher2.txt",
                                                        sim.persons[2].id, sim.persons[1].id, sim.persons[1].key.private_key)

        decrypted_data = filehandler.decrypt_with_shared_secret_and_load("secure_voucher2.txt", sim.persons[1].id, sim.persons[2].id,
                                                                         sim.persons[2].key.private_key, MinutoVoucher)

        # Verify the integrity of the decrypted data
        self.assertTrue(
            decrypted_data.verify_complete_voucher(),
            "Decrypted data should be verified as complete."
        )

        # Assert that the original data and decrypted data are equal
        self.assertEqual(
            sim.persons[1].voucherlist[VoucherStatus.OTHER.value][0],
            decrypted_data,
            "Original and decrypted vouchers should be identical."
        )

    # def tearDown(self):
    #     # Cleanup: Remove test files
    #     for file_name in [self.voucher_file_name, self.male_signed_voucher_file_name, self.male_female_signed_voucher_file_name, "minutoschein-complete.txt"]:
    #         full_path = os.path.join(self.temp_subfolder, file_name)
    #         if os.path.exists(full_path):
    #             os.remove(full_path)

if __name__ == '__main__':
    unittest.main()
