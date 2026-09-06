# Virtual PoGo Plus — GitHub APK build

Bu sürüm GitHub Actions üzerinden APK üretmek için düzenlenmiştir.

## Neden önceki APK açılışta kapanıyordu?

Önceki projede `main.py` şu Java sınıfını daha uygulama başlarken yüklemeye çalışıyordu:

`com.example.virtualpogoplus.BlePeripheral`

Fakat yüklenen ZIP içinde `android_src/.../BlePeripheral.java` dosyası yoktu. Bu nedenle `autoclass()` başarısız olduğunda uygulama Kivy ekranını açamadan kapanabiliyordu.

Bu sürümde Java sınıfı gerçekten projeye dahil edilmiştir.

## Android sürümü uyarısı

`android.api = 36` kullanılır. Buildozer/p4a güncel Android API hedefiyle derleme yapar. Minimum API 26'dır.

## GitHub'da APK üretme

1. Bu klasörün tamamını bir GitHub repository'sine yükleyin.
2. `Actions` sekmesine girin.
3. `Build Android APK` workflow'unu seçin.
4. `Run workflow` ile elle başlatabilirsiniz.
5. İşlem bittiğinde workflow içindeki `VirtualPoGoPlus-debug` artifact'ini indirin.

Push yaptığınızda da workflow otomatik çalışır.

## Telefon testi

APK'yı kurduktan sonra:

1. Bluetooth'u açın.
2. Uygulamayı açın.
3. İstenen Bluetooth izinlerini verin.
4. `Sanal BLE Cihazını Başlat` düğmesine basın.
5. Başka bir BLE scanner ile `Virtual-PoGo-Plus` adını arayın.
6. Özel GATT servis UUID'si:
   `7e400001-b5a3-f393-e0a9-e50e24dcca9e`

## Önemli

Bu proje gerçek BLE peripheral + GATT test cihazıdır. Aynı UUID'yi kullanmak tek başına Pokémon GO Plus cihazının özel protokolünü veya kimlik doğrulamasını oluşturmaz. Gerçek ticari cihaz protokolünü taklit eden kimlik doğrulama/anahtar materyali bu projeye dahil edilmemiştir.

## Yerel debug

GitHub yerine WSL/Linux üzerinde test etmek isterseniz:

```bash
buildozer android debug deploy run logcat
```

Uygulama açılışta kapanırsa Android logcat'teki `FATAL EXCEPTION`, `AndroidRuntime` ve `Python` satırları asıl hata nedenini gösterir.
