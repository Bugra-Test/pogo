from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions, check_permission, Permission
    BlePeripheral = autoclass("com.example.virtualpogoplus.BlePeripheral")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
else:
    BlePeripheral = None
    PythonActivity = None

ANDROID_PERMS = []
if platform == "android":
    # Android 12+ requires these for BLE advertising/connection.
    ANDROID_PERMS = [
        Permission.BLUETOOTH_ADVERTISE,
        Permission.BLUETOOTH_CONNECT,
    ]


class VirtualPoGoService:
    SERVICE_UUID = "7e400001-b5a3-f393-e0a9-e50e24dcca9e"
    RX_UUID = "7e400002-b5a3-f393-e0a9-e50e24dcca9e"
    TX_UUID = "7e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self):
        self.running = False
        self.peripheral = None

    def start(self):
        if platform != "android":
            raise RuntimeError("BLE peripheral mode requires Android.")

        request_permissions(ANDROID_PERMS)

        # Permission dialogs are asynchronous on Android. If the user has not
        # granted them yet, start() may be retried from the UI.
        for perm in ANDROID_PERMS:
            if not check_permission(perm):
                raise RuntimeError("Bluetooth izni verilmedi. İzinleri verip tekrar deneyin.")

        activity = PythonActivity.mActivity
        self.peripheral = BlePeripheral(
            activity,
            "Virtual-PoGo-Plus",
            self.SERVICE_UUID,
            self.RX_UUID,
            self.TX_UUID,
        )
        if not self.peripheral.start():
            self.peripheral = None
            raise RuntimeError(
                "BLE başlatılamadı. Bluetooth açık ve cihaz BLE Peripheral destekliyor mu?"
            )
        self.running = True
        return "BLE Advertising + GATT aktif"

    def stop(self):
        if self.peripheral is not None:
            self.peripheral.stop()
        self.peripheral = None
        self.running = False


class PoGoAutoCatchApp(App):
    title = "Virtual PoGo Plus"

    def build(self):
        self.service = VirtualPoGoService()

        root = BoxLayout(orientation="vertical", padding=24, spacing=16)
        self.status = Label(
            text="Durum: Beklemede\nBLE cihazı başlatılmadı.",
            halign="center",
            valign="middle",
        )
        root.add_widget(self.status)

        self.toggle = Button(
            text="Sanal BLE Cihazını Başlat",
            size_hint=(1, 0.25),
        )
        self.toggle.bind(on_press=self.toggle_service)
        root.add_widget(self.toggle)

        return root

    def toggle_service(self, _):
        try:
            if not self.service.running:
                msg = self.service.start()
                self.status.text = "Durum: AKTİF\n" + msg + "\nAd: Virtual-PoGo-Plus"
                self.toggle.text = "Durdur"
            else:
                self.service.stop()
                self.status.text = "Durum: Durduruldu"
                self.toggle.text = "Sanal BLE Cihazını Başlat"
        except Exception as exc:
            self.status.text = "Hata:\n" + str(exc)

    def on_stop(self):
        try:
            self.service.stop()
        except Exception:
            pass


if __name__ == "__main__":
    PoGoAutoCatchApp().run()
