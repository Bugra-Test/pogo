from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission

    BlePeripheral = autoclass("com.example.virtualpogoplus.BlePeripheral")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    ANDROID_PERMS = [
        Permission.BLUETOOTH,
        Permission.BLUETOOTH_ADMIN,
        Permission.BLUETOOTH_ADVERTISE,
        Permission.BLUETOOTH_CONNECT,
        Permission.ACCESS_FINE_LOCATION,
    ]
else:
    BlePeripheral = None
    ANDROID_PERMS = []


class VirtualPoGoService:
    """BLE peripheral wrapper.

    A-mode: real BLE advertising + GATT server using a custom, documented UUID.
    B-mode: protocol/authentication scaffolding only. No proprietary credentials
    are embedded and no authentication bypass is attempted.
    """

    SERVICE_UUID = "7e400001-b5a3-f393-e0a9-e50e24dcca9e"
    RX_UUID = "7e400002-b5a3-f393-e0a9-e50e24dcca9e"
    TX_UUID = "7e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self):
        self.running = False
        self.connected = False
        self.peripheral = None

    def start(self):
        if platform != "android":
            raise RuntimeError("BLE peripheral mode requires Android.")
        activity = PythonActivity.mActivity
        self.peripheral = BlePeripheral(activity, "Virtual-PoGo-Plus", self.SERVICE_UUID, self.RX_UUID, self.TX_UUID)
        ok = self.peripheral.start()
        if not ok:
            raise RuntimeError("Android could not start BLE advertising/GATT server.")
        self.running = True
        return "BLE advertising + GATT server aktif"

    def stop(self):
        if self.peripheral is not None:
            self.peripheral.stop()
        self.running = False
        self.connected = False

    def send_demo_packet(self):
        if not self.running or self.peripheral is None:
            return False
        # Safe test payload for validating the GATT path.
        return bool(self.peripheral.notify(b"VPP:TEST"))


class PoGoAutoCatchApp(App):
    title = "Virtual PoGo Plus"

    def build(self):
        self.service = VirtualPoGoService()
        if platform == "android":
            try:
                request_permissions(ANDROID_PERMS)
            except Exception as exc:
                print("Permission request failed:", exc)

        root = BoxLayout(orientation="vertical", padding=24, spacing=16)
        self.status = Label(
            text="Durum: Beklemede\nBLE cihazı başlatılmadı.",
            halign="center",
            valign="middle",
        )
        root.add_widget(self.status)

        self.toggle = Button(text="Sanal BLE Cihazını Başlat", size_hint=(1, 0.25))
        self.toggle.bind(on_press=self.toggle_service)
        root.add_widget(self.toggle)

        self.test = Button(text="GATT Test Bildirimi Gönder", size_hint=(1, 0.2), disabled=True)
        self.test.bind(on_press=self.send_test)
        root.add_widget(self.test)
        return root

    def toggle_service(self, _):
        try:
            if not self.service.running:
                msg = self.service.start()
                self.status.text = "Durum: AKTİF\n" + msg + "\nCihaz adı: Virtual-PoGo-Plus"
                self.toggle.text = "Durdur"
                self.test.disabled = False
            else:
                self.service.stop()
                self.status.text = "Durum: Durduruldu"
                self.toggle.text = "Sanal BLE Cihazını Başlat"
                self.test.disabled = True
        except Exception as exc:
            self.status.text = "Hata:\n" + str(exc)

    def send_test(self, _):
        if self.service.send_demo_packet():
            self.status.text = "Durum: AKTİF\nTest bildirimi gönderildi (VPP:TEST)."
        else:
            self.status.text = "Test bildirimi gönderilemedi."


if __name__ == "__main__":
    PoGoAutoCatchApp().run()
