from src.models.person import Person
from src.models.key import Key
from src.models.minuto_voucher import MinutoVoucher

def main():
    # Erstelle eine Person
    hansdampf = Person(Key("adapt buddy actress swear early offer grow comic code sting hawk marble"), "Max Mustermann",
                       "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support", "50.1109, 8.6821",
                       "2023-12-31")
    buerge_weiblich = Person(Key("rookie era bamboo industry group furnace axis disorder economy silly action invite"),
                             "Susi Musterfrau", "Musterstraße 2", 2, "susi@example.com", "0123456789", "Backen",
                             "50.1109, 8.6821", "2023-12-31")
    buerge_maennlich = Person(Key("strong symptom minor attract math clock pool elite half guess album close"),
                              "Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support",
                              "50.1109, 8.6821", "2023-12-31")

    # Erstelle einen MinutoVoucher mit dieser Person als Ersteller
    voucher = hansdampf.create_voucher(100, "Frankfurt", "2028")
    voucher.save_to_disk("minutoschein.txt")

    b1_load_voucher = MinutoVoucher.read_from_disk("minutoschein.txt")
    buerge_maennlich.sign_voucher_as_guarantor(b1_load_voucher)
    b1_load_voucher.save_to_disk("minutoschein-b1.txt")

    print(voucher)
    print(b1_load_voucher)

if __name__ == "__main__":
    main()











