# main.py
#from src.models.key import Key
#from src.models.minuto_voucher import MinutoVoucher
import src.models.person


def main():
    # Erstelle eine Person
    hansdampf = src.models.person.Person("Max Mustermann", "Musterstraße 1", 1, "max@example.com", "0123456789", "IT-Support", "50.1109, 8.6821",
                       "2023-12-31","adapt buddy actress swear early offer grow comic code sting hawk marble")
    buerge_weiblich = src.models.person.Person("Susi Musterfrau", "Musterstraße 2", 2, "susi@example.com", "0123456789", "Backen",
                             "50.1109, 8.6821", "2023-12-31", "rookie era bamboo industry group furnace axis disorder economy silly action invite")
    buerge_maennlich = src.models.person.Person("Hans Müller", "Straße 6", 1, "hans@mail.com", "0172653214", "Sport, Handwerk",
                              "50.1109, 8.6821", "2023-12-31", "strong symptom minor attract math clock pool elite half guess album close")

    # Erstelle einen MinutoVoucher mit dieser Person als Ersteller
    hansdampf.create_voucher(100, "Frankfurt", 5)
    hansdampf.current_voucher.save_to_disk("minutoschein.txt")
    print(hansdampf.current_voucher)

    #buerge_maennlich.init_empty_voucher()
    buerge_maennlich.read_voucher_from_file("minutoschein.txt")
    print(buerge_maennlich.current_voucher)

    buerge_maennlich.sign_voucher_as_guarantor(buerge_maennlich.current_voucher)
    print(buerge_maennlich.current_voucher)
    buerge_maennlich.current_voucher.save_to_disk("minutoschein-male-signed.txt")
    buerge_weiblich.read_voucher_from_file("minutoschein-male-signed.txt")
    print(buerge_weiblich.verify_guarantor_signatures(buerge_weiblich.current_voucher)) #assert here
    buerge_weiblich.sign_voucher_as_guarantor(buerge_weiblich.current_voucher)
    print(buerge_weiblich.current_voucher)
    buerge_weiblich.current_voucher.save_to_disk("minutoschein-male_female-signed.txt")
    hansdampf.read_voucher_from_file("minutoschein-male_female-signed.txt")
    print("check both guarantor signs: ", hansdampf.verify_guarantor_signatures(hansdampf.current_voucher))


    # todo signaturen der bürgen prüfen wenn beide unterschrieben haben
    # todo dann die signaturen der bürgen beim laden überprüfen
    # todo dann als schöpfer signieren
    # signatur des schöpfer prüfen (beim einlesen noch richtig einlesen da auch pubkey und signatur als liste gespeichert wird
    # todo dann den fertigen minutoschein prüfen inkl signatur des schöpfers
    #b1_load_voucher = MinutoVoucher.read_from_disk("../minutoschein.txt")
    #buerge_maennlich.sign_voucher_as_guarantor(b1_load_voucher)
    #b1_load_voucher.save_to_disk("minutoschein-b1.txt")



    #print(b1_load_voucher)

if __name__ == "__main__":
    main()











