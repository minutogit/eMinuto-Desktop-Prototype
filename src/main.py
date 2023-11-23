# main.py
import src.models.person


def main():
    # Erstelle eine Person
    hansdampf = src.models.person.Person("Hans Dampf", "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support", "50.1109, 8.6821",
                       "2023-12-31","adapt buddy actress swear early offer grow comic code sting hawk marble")
    buerge_weiblich = src.models.person.Person("Susi Musterfrau", "Musterstraße 2", 2, "susi@example.com", "0123456789", "Backen",
                             "50.1109, 8.6821", "2023-12-31", "rookie era bamboo industry group furnace axis disorder economy silly action invite")
    buerge_maennlich = src.models.person.Person("Hans Müller", "Straße 6", 1, "hans@mail.com", "0172653214", "Sport, Handwerk",
                              "50.1109, 8.6821", "2023-12-31", "strong symptom minor attract math clock pool elite half guess album close")

    user1 = src.models.person.Person("Franz Müller", "Weg 3", 1, "franzi@gmx.com", "0717-362541", "ICh kann vil",
                              "51.56, 8.22", "2023-12-31", "orchard honey actor together basket wasp ankle wire eyebrow clever ensure expose")


    # Erstelle einen MinutoVoucher mit dieser Person als Ersteller
    hansdampf.create_voucher(100, "Frankfurt", 5)
    hansdampf.current_voucher.save_to_disk("minutoschein.txt")
    print(hansdampf.current_voucher)
    buerge_maennlich.read_voucher_from_file("minutoschein.txt")

    buerge_maennlich.sign_voucher_as_guarantor()
    print(buerge_maennlich.current_voucher)
    buerge_maennlich.current_voucher.save_to_disk("minutoschein-male-signed.txt")

    buerge_weiblich.read_voucher_from_file("minutoschein-male-signed.txt")
    print(buerge_weiblich.verify_guarantor_signatures()) #assert here
    buerge_weiblich.sign_voucher_as_guarantor()
    print(buerge_weiblich.current_voucher)
    buerge_weiblich.current_voucher.save_to_disk("minutoschein-male_female-signed.txt")

    hansdampf.read_voucher_from_file("minutoschein-male_female-signed.txt")
    print("both guarantor signs ok? ", hansdampf.verify_guarantor_signatures())
    hansdampf.sign_voucher_as_creator()
    print("creator signature ok? ",hansdampf.verify_creator_signature())
    hansdampf.send_amount(33, 'MC22m5UFhMczBb3mnmxhH5o6kqv5e1RpmFL2Y2ibciRKbwfXhNM')
    hansdampf.current_voucher.save_to_disk("minutoschein-complete.txt")

    buerge_maennlich.read_voucher_from_file("minutoschein-complete.txt")
    buerge_maennlich.send_amount(32, 'MCbcUb8Tg6xtCFL6WhDv1uXgyC4LjvkV9BR53hn1MowLpYPGPp')
    buerge_maennlich.current_voucher.save_to_disk("minutoschein-complete.txt")

    user1.read_voucher_from_file("minutoschein-complete.txt")
    #print(user1.current_voucher)
    print("verify_initial_transaction: ",user1.current_voucher.verify_initial_transaction())
    print(user1.current_voucher.verify_all_transactions())
    print("user1 cerator sign ok? ",user1.verify_creator_signature())


if __name__ == "__main__":
    main()











