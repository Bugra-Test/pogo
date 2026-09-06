from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

SERVICE_UUID = "0000bbef-0000-1000-8000-00805f9b34fb"
RX_UUID = "0000bbf0-0000-1000-8000-00805f9b34fb"
TX_UUID = "0000bbf1-0000-1000-8000-00805f9b34fb"


def android_ble_class():
    if platform != "android":
        raise RuntimeError("BLE yalnızca Android'de kullanılabilir.")
    from jnius import autoclass
    return autoclass("com.example.virtualpogoplus.BlePeripheral")


class VirtualPoGoPlusApp(App):
    def build(self):
        self.ble = None
        self.running = False
        self.status = Label(
            text="Durum: Hazır\nAndroid 12+ Bluetooth izinleri bekleniyor",
            halign="center",
            valign="middle",
            font_size="18sp",
        )
        self.status.bind(size=lambda *_: setattr(self.status, "text_size", self.status.size))

        self.button = Button(
            text="Sanal BLE Cihazını Başlat",
            size_hint_y=None,
            height=80,
            font_size="19sp",
        )
        self.button.bind(on_release=self.toggle)

        root = BoxLayout(orientation="vertical", padding=24, spacing=18)
        root.add_widget(self.status)
        root.add_widget(self.button)
        return root

    def on_start(self):
        if platform != "android":
            self.status.text = "Durum: Android cihaz gerekli"
            self.button.disabled = True
            return
        Clock.schedule_once(self.prepare_android, 0.25)

    def prepare_android(self, _dt):
        try:
            from android.permissions import request_permissions, Permission
            permissions = [
                Permission.BLUETOOTH_ADVERTISE,
                Permission.BLUETOOTH_CONNECT,
            ]
            # ACCESS_FINE_LOCATION yalnızca eski Android BLE tarama senaryolarında gerekir.
            # Advertising/GATT için Android 12+ tarafında Bluetooth izinleri esas alınır.
            request_permissions(permissions, self.permission_callback)
        except Exception as exc:
            self.status.text = f"İzin ekranı başlatılamadı:\n{type(exc).__name__}: {exc}"

    def permission_callback(self, permissions, grants):
        # Kullanıcı izin vermezse uygulama kapanmaz; ekranda açıklama gösterir.
        if all(grants):
            self.status.text = "Durum: Hazır\nBluetooth izinleri verildi."
        else:
            self.status.text = "Durum: Bluetooth izinleri eksik.\nAyarlar'dan izinleri verin."

    def toggle(self, _instance):
        if self.running:
            self.stop_ble()
        else:
            self.start_ble()

    def start_ble(self):
        try:
            BlePeripheral = android_ble_class()
            if self.ble is None:
                self.ble = BlePeripheral()

            result = self.ble.start(
                "Virtual-PoGo-Plus",
                SERVICE_UUID,
                RX_UUID,
                TX_UUID,
            )
            if result:
                self.running = True
                self.status.text = (
                    "Durum: BLE + GATT AKTİF\n"
                    "Cihaz adı: Virtual-PoGo-Plus\n"
                    "BLE tarayıcı ile arayabilirsiniz."
                )
                self.button.text = "Sanal Cihazı Durdur"
            else:
                self.status.text = "BLE başlatılamadı.\nLogcat çıktısını kontrol edin."
        except Exception as exc:
            self.status.text = f"BLE başlatma hatası:\n{type(exc).__name__}: {exc}"

    def stop_ble(self):
        try:
            if self.ble is not None:
                self.ble.stop()
            self.running = False
            self.status.text = "Durum: Durduruldu."
            self.button.text = "Sanal BLE Cihazını Başlat"
        except Exception as exc:
            self.status.text = f"Durdurma hatası:\n{type(exc).__name__}: {exc}"

    def on_stop(self):
        try:
            if self.ble is not None:
                self.ble.stop()
        except Exception:
            pass


if __name__ == "__main__":
    VirtualPoGoPlusApp().run()
