import copy
import time

from faker import Faker
from typing import List
from src.services.crypto_utils import generate_seed
from src.services.utils import dprint
from src.models.person import Person
import random

fake = Faker()

class SimulationHelper:
    def __init__(self, print_info=False):
        """
        Initialize the SimulationHelper with optional print information.

        :param print_info: If set to True, additional information will be printed during simulation. Default is False.
        """
        self.num_persons = 0
        self.print_info = print_info
        # Using type annotations to specify the list type for enhanced code development
        self.persons: List[Person] = []
        self.services = [
            "IT Support", "Baking", "Sports", "Craftsmanship", "Gardening",
            "Teaching", "Photography", "Design", "Consulting", "Accounting",
            "Marketing", "Event Planning", "Cooking", "Music Lessons",
            "Web Development", "Physiotherapy", "Yoga Instruction", "Legal Advice",
            "Writing Services", "Pet Care", "Interior Design",
            "Driving School", "Tailoring", "Fitness Coaching", "Translations",
            "Graphic Design", "Personal Training", "Artistic Workshops",
            "House Cleaning", "Wedding Planning", "Event Management",
            "Car Repair", "Pet Training", "Computer Programming"
        ]
        self.transaction_counter = 0
        self.simulation_folder = None # folder for storing files of simulation

    def generate_person(self, index):
        """
        Generates a person with a gender based on the provided index (even index for female, odd for male).

        :param index: The index to determine the gender of the person.
        :return: A Person object with attributes based on the index.
        """
        if index % 2 == 0:  # Even index for female
            gender = 2
            name = fake.first_name_female() + " " + fake.last_name_female()
        else:  # Odd index for male
            gender = 1
            name = fake.first_name_male() + " " + fake.last_name_male()

        address = fake.street_address()
        email = fake.email()
        phone = fake.phone_number()
        service_offer = ", ".join(random.sample(self.services, random.randint(2, 4)))
        coordinates = f"{fake.latitude()}, {fake.longitude()}"
        seed = generate_seed()

        return Person(name, address, gender, email, phone, service_offer, coordinates, seed=seed)

    def generate_persons(self, num_persons):
        """
        Generates a specified number of persons, each with a gender based on their index position.

        :param num_persons: The number of persons to generate.
        """
        self.num_persons = num_persons
        for i in range(self.num_persons):
            self.persons.append(self.generate_person(i))

    def generate_voucher_for_person(self, creator, guarantor1, guarantor2, amount, years_valid):
        """
        Generates a voucher for a specified person, signed by two guarantors.

        :param creator: Index of the person for whom the voucher is created.
        :param guarantor1: Index of the first guarantor.
        :param guarantor2: Index of the second guarantor.
        :param amount: The amount for the voucher.
        :param years_valid: Number of years the voucher is valid.
        """
        v_creator = self.persons[creator]
        guarantor1 = self.persons[guarantor1]
        guarantor2 = self.persons[guarantor2]

        v_creator.create_voucher(amount, "Frankfurt", years_valid)
        virtual_vouchers = v_creator.save_voucher(simulation=True)

        guarantor1.read_voucher(virtual_vouchers, simulation=True)
        guarantor1.sign_voucher_as_guarantor()
        virtual_vouchers = guarantor1.save_voucher(simulation=True)

        guarantor2.read_voucher(virtual_vouchers, simulation=True)
        guarantor2.sign_voucher_as_guarantor()
        virtual_vouchers = guarantor2.save_voucher(simulation=True)

        # Verification of signatures and creator's signature
        v_creator.read_voucher_and_save_voucher(virtual_vouchers, simulation=True)
        assert v_creator.verify_guarantor_signatures(), "Guarantor signatures are not correct"
        v_creator.sign_voucher_as_creator()
        assert v_creator.verify_creator_signature(), "Creator's signature is not correct"
        if v_creator.current_voucher.verify_complete_voucher() and self.print_info:
            print(f"Voucher created for person[{creator}] with {amount}M")

    def send_amount(self, sender, receiver, amount):
        """
        Sends a specified amount of Minuto from one person to another.

        :param sender: Index of the sender in the persons list.
        :param receiver: Index of the receiver in the persons list.
        :param amount: The amount of Minuto to be sent.
        """
        transaction = self.persons[sender].send_amount(amount, self.persons[receiver].id)

        # To ensure independent transactions in the simulation, create a deep copy of the transaction.
        # This prevents referencing issues where changes to the copied transaction might unintentionally
        # affect the original transaction object. A deep copy creates a new, separate instance of the transaction.
        transaction_copy = copy.deepcopy(transaction)

        self.persons[receiver].receive_amount(transaction_copy)
        if not transaction_copy.transaction_successful:
            return
        if self.print_info:
            print(f"Person[{sender}] send {amount}M to Person[{receiver}]")
        self.transaction_counter += 1

    def simulate_transaction(self, number_of_transactions):
        """
        Simulates a specified number of transactions among persons.

        :param number_of_transactions: The number of transactions to simulate.
        """
        start_time = time.time()  # Start the timer

        # Compute initial total amount across all persons
        person_amounts = [person.get_amount_of_all_vouchers() for person in self.persons]
        total_start_amount = sum(person_amounts)

        for transaction_num in range(1, number_of_transactions + 1):
            potential_senders = [i for i, amount in enumerate(person_amounts) if amount > 0]
            if not potential_senders:
                print("No more senders with sufficient funds.")
                break

            sender = random.choice(potential_senders)
            receiver = random.choice([i for i in range(len(self.persons)) if i != sender])

            max_send_amount = min(person_amounts[sender], 100)
            amount_to_send = round(random.uniform(0.01, max_send_amount), 2)

            # Apply rounding down with 95% probability for amounts over 1
            if amount_to_send > 1 and random.random() < 0.95:
                amount_to_send = int(amount_to_send)

            self.send_amount(sender, receiver, amount_to_send)

            # Update the amounts in person_amounts list
            person_amounts[sender] -= amount_to_send
            person_amounts[receiver] += amount_to_send

            if self.print_info:
                print(f"Transaction {transaction_num}: Person[{sender}] sent {amount_to_send}M to Person[{receiver}]")

        end_time = time.time()
        if self.print_info:
            print(f"Simulation took {end_time - start_time} seconds.")

        # Verify the simulation results
        simulation_results_correct = True
        total_amount_after_simulation = sum(
            self.persons[i].get_amount_of_all_vouchers() for i in range(len(self.persons)))

        for i, (tracked_amount, real_amount) in enumerate(
                zip(person_amounts, [p.get_amount_of_all_vouchers() for p in self.persons])):
            if self.print_info:
                print(f"Person[{i}]: {round(tracked_amount, 2)}")
            if round(tracked_amount, 2) != round(real_amount, 2):
                print(f"Discrepancy for Person[{i}]. Expected: {round(tracked_amount, 2)}, Actual: {real_amount}")
                simulation_results_correct = False

        if round(total_start_amount, 2) != round(total_amount_after_simulation, 2):
            print(f"Inconsistent total amount. Start: {total_start_amount}, End: {total_amount_after_simulation}")
            simulation_results_correct = False

        return simulation_results_correct



    def save_vouchers(self, person_number, subfolder=None):
        """
        Saves all vouchers of a specified person to disk.

        :param person_number: Index of the person whose vouchers will be saved.
        """
        if self.simulation_folder and not subfolder: # when no subfolder use default simulation folder
            subfolder = self.simulation_folder

        self.persons[person_number].save_all_vouchers(fileprefix=f"Person{person_number}", prefix_only=True, subfolder=subfolder)

    def save_all_persons_vouchers(self, subfolder=None):
        """
        Saves vouchers of all persons in the simulation to disk.
        """
        for i, person in enumerate(self.persons):
            self.save_vouchers(i, subfolder)

    def print_all_user_vouchers(self):
        i = 0
        for person in self.persons:
            print(f"\nPerson[{i}] ", end='')
            person.list_vouchers()
            i += 1



