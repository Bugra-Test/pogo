# Virtual PoGo Plus V2

Android için temiz bir BLE peripheral/GATT test projesidir. Proje, telefonun BLE advertising yapmasını ve bir GATT servisinin yayınlanmasını sağlar.

> **Önemli:** Bu proje tek başına Pokémon GO'nun gerçek GO Plus cihazı tarafından doğrulanmasını garanti etmez. Gerçek cihaz protokolü ve cihaz-spesifik kimlik doğrulama materyali bu projeye dahil değildir.

## V2'de düzeltilenler

- Uygulama açılırken Java BLE sınıfı yüklenmez.
- BLE Java sınıfı yalnızca Başlat düğmesine basılınca yüklenir.
- Android 12+ Bluetooth izinleri uygulama içinde istenir.
- Gerçek `BluetoothLeAdvertiser.startAdvertising()` kullanılır.
- Gerçek `BluetoothGattServer` oluşturulur.
- BLE reklamı durdurulabilir.
- Java hataları Python tarafında yakalanır; mümkün olduğunca loading ekranında sessiz çökme yerine hata metni gösterilir.
- GitHub Actions ile APK üretimi eklenmiştir.
- Android API 36 / arm64-v8a hedeflenmiştir.

## GitHub'da APK oluşturma

1. Bu klasörü yeni bir GitHub repository'sine yükleyin.
2. `Actions` sekmesine girin.
3. `Build Android APK` workflow'unu seçin.
4. `Run workflow` ile çalıştırın.
5. İşlem tamamlanınca `VirtualPoGoPlus-V2-debug` artifact'ini indirin.

Workflow ayrıca `main` veya `master` branch'ine push yapıldığında otomatik çalışır.

## Telefonda test

1. APK'yı kurun.
2. Bluetooth'u açın.
3. Uygulamayı açın.
4. İstenen Bluetooth izinlerini verin.
5. `Sanal BLE Cihazını Başlat` düğmesine basın.
6. Bir BLE tarayıcı uygulamasından `Virtual-PoGo-Plus` cihazını arayın.

Android'in normal Bluetooth eşleştirme ekranı BLE GATT cihazlarını her zaman göstermeyebilir. Test için BLE scanner kullanılması önerilir.

## Test UUID'leri

Service:
`0000bbef-0000-1000-8000-00805f9b34fb`

RX:
`0000bbf0-0000-1000-8000-00805f9b34fb`

TX:
`0000bbf1-0000-1000-8000-00805f9b34fb`

RX/TX UUID'leri bu V2 projesinin test characteristic'leridir; gerçek GO Plus protokolü oldukları varsayılmamalıdır.

## Yerel derleme

Linux/WSL ortamında:

```bash
pip install "cython<3" buildozer
buildozer -v android debug
```

İlk derleme Android SDK/NDK bileşenlerini indirebilir ve uzun sürebilir.
