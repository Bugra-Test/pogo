# Virtual PoGo Plus — A+B BLE project

Bu proje iki katmanlı bir mimari sunar:

- **A — gerçek BLE peripheral:** Android telefon BLE advertising yapar ve gerçek bir GATT server açar. Özel/test UUID'leri kullanır.
- **B — protokol/authentication iskeleti:** `protocol.py` ve `device_keys.example.json`, yasal olarak edinilmiş cihaz/protokol materyali ile daha ileri interoperabilite çalışması yapılabilmesi için ayrılmıştır. Pokémon GO'nun özel kimlik doğrulamasını atlatan anahtarlar veya sertifikalar projeye gömülü değildir.

## Gereksinimler

- Windows için WSL2/Ubuntu veya Linux önerilir.
- Python 3.11
- Java/OpenJDK 17
- Buildozer + python-for-android bağımlılıkları
- Android SDK/NDK (Buildozer otomatik yönetebilir)

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython==0.29.37
```

## APK oluşturma

Proje klasöründe:

```bash
buildozer android debug
```

İlk derleme uzun sürebilir. Başarılı olursa APK `bin/` klasöründe oluşur.

Release imzalama için kendi Android keystore'unuzu kullanın; debug APK üretimi ile release imzalama farklı işlemlerdir.

## Test

1. APK'yı Android telefona kurun.
2. Bluetooth'u açın.
3. Uygulamayı açın.
4. **Sanal BLE Cihazını Başlat** seçeneğine basın.
5. Başka bir BLE scanner ile `Virtual-PoGo-Plus` cihazını arayın.
6. Özel servis UUID'sine bağlanıp RX/TX characteristic'lerini test edin.

## Neden Pokémon GO'ya doğrudan bağlanmıyor?

Bir BLE cihazının aynı UUID'yi yayınlaması, onu otomatik olarak belirli bir ticari cihazın yerine geçirmez. Gerçek ürün protokolü, GATT davranışı ve kimlik doğrulama ayrıntıları gerekir. Bu repo bu kısmı bilinçli olarak **yer tutucu/interoperabilite iskeleti** olarak bırakır.

## Güvenli genişletme noktaları

- `BlePeripheral.java`: GATT callback ve bağlı cihaz yönetimi
- `protocol.py`: frame/packet kodlama ve doğrulama
- `device_keys.example.json`: kullanıcı tarafından yasal olarak sağlanan test materyali
- `main.py`: UI ve servis yaşam döngüsü
