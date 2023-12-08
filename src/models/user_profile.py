class UserProfile:
    def __init__(self):
        # Diese Methode wird aufgerufen, wenn ein UserProfile-Objekt erstellt wird.
        # Hier können Sie die Initialisierung des Profils durchführen, z.B. das Laden aus einer Datei.
        self.person = None
        self.balance = 0
        self.transaction_pin = None
        self.seed_words = None
        self.data_folder = 'data'
        self.profile_filename = 'userprofile.dat'

    def create_new_profile(self, name, address, gender, email, phone, service_offer, coordinates, seed=None):
        # Diese Methode erstellt ein neues Profil mit den gegebenen Parametern.
        # Sie könnten hier auch zusätzliche Parameter wie Kontostand, Transaktions-PIN usw. hinzufügen.
        from person import Person  # Importieren der Person-Klasse
        self.person = Person(name, address, gender, email, phone, service_offer, coordinates, seed)
        # Setzen Sie hier auch die anderen Attribute wie balance, transaction_pin, etc.

    def update_balance(self, new_balance):
        # Diese Methode aktualisiert den Kontostand des Benutzers.
        self.balance = new_balance
        # Fügen Sie hier die Logik hinzu, um den neuen Kontostand zu speichern, z.B. in einer Datei oder Datenbank.


    def update_profile(self, **kwargs):
        # Diese Methode kann verwendet werden, um verschiedene Attribute des Profils zu aktualisieren.
        for key, value in kwargs.items():
            if hasattr(self.person, key):
                setattr(self.person, key, value)
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Attribut {key} existiert nicht im UserProfile oder Person.")

    def profile_exists(self):

        return False
