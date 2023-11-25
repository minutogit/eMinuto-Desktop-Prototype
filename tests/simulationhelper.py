from faker import Faker
from src.services.crypto_utils import generate_seed
from src.services.utils import dprint
import src.models.person
import random

fake = Faker()

class SimulationHelper:
    def __init__(self,print_info = False):
        self.num_persons = 0
        self.print_info = print_info
        self.persons = []
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

    def generate_person(self, index):
        """
        Generate a person with gender based on the index: even for female, odd for male.
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

        return src.models.person.Person(name, address, gender, email, phone, service_offer, coordinates, seed=seed)

    def generate_persons(self, num_persons):
        """
        Generate a list of persons with specified number. Each person's gender is determined based on their index.
        """
        self.num_persons = num_persons
        for i in range(self.num_persons):
            self.persons.append(self.generate_person(i))

    def generate_voucher_for_person(self, person_number, guarantor1_num, guarantor2_num, amount, years_valid):
        """
        Generate a voucher for a specified person and have it signed by two guarantors.
        """
        # Voucher creation and signing by guarantors
        creator = self.persons[person_number]
        guarantor1 = self.persons[guarantor1_num]
        guarantor2 = self.persons[guarantor2_num]

        creator.create_voucher(amount, "Frankfurt", years_valid)
        virtual_vouchers = creator.save_voucher(virtual=True)

        guarantor1.read_voucher(virtual_vouchers, virtual=True)
        guarantor1.sign_voucher_as_guarantor()
        virtual_vouchers = guarantor1.save_voucher(virtual=True)

        guarantor2.read_voucher(virtual_vouchers, virtual=True)
        guarantor2.sign_voucher_as_guarantor()
        virtual_vouchers = guarantor2.save_voucher(virtual=True)

        # Verification of signatures and creator's signature
        creator.read_voucher_and_save_voucher(virtual_vouchers, virtual=True)
        assert creator.verify_guarantor_signatures(), "Guarantor signatures are not correct"
        creator.sign_voucher_as_creator()
        assert creator.verify_creator_signature(), "Creator's signature is not correct"
        if creator.current_voucher.verify_complete_voucher() and self.print_info:
            print(f"Voucher created for person[{person_number}] with {amount}M")

    def send_minuto_to_person(self, sender_number, receiver_number, amount):
        transaction = self.persons[sender_number].send_amount(amount, self.persons[receiver_number].id)
        self.persons[receiver_number].receive_amount(transaction)
        if not transaction.transaction_successful:
            return
        if self.print_info:
            print(f"Person[{sender_number}] send {amount}M to Person[{receiver_number}]")
        self.transaction_counter += 1



