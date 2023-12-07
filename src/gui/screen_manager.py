# screenmanager.py
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


# for hot reload
#from kivymd.app import MDApp
from kivymd.tools.hotreload.app import MDApp


Builder.load_file('gui/gui_layout.kv')

# Definiere die verschiedenen Bildschirme
class DashboardScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class CreateVoucherScreen(Screen):
    pass

class PerformTransactionScreen(Screen):
    pass

class ReceiveTransactionScreen(Screen):
    pass

class VoucherListScreen(Screen):
    pass

# Hauptanwendung
class MyApp(MDApp):
    DEBUG = 1 # activate hot reload
    KV_FILES = ["gui/gui_layout.kv"]
    def build_app(self, first=False):
        self.theme_cls.primary_palette = "Blue"  # Setze das Farbschema

        # Erstelle den Screen Manager
        sm = ScreenManager()

        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CreateVoucherScreen(name='create_voucher'))
        sm.add_widget(PerformTransactionScreen(name='perform_transaction'))
        sm.add_widget(ReceiveTransactionScreen(name='receive_transaction'))
        sm.add_widget(VoucherListScreen(name='voucher_list'))

        sm.current = 'dashboard'
        return sm

if __name__ == '__main__':
    MyApp().run()
