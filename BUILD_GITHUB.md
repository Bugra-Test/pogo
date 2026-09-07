# GitHub Actions hızlı kullanım

Repository'ye bütün dosyaları yükleyin.

`Actions` → `Build Android APK` → `Run workflow`

Başarılı işlemden sonra:

`Summary` → `Artifacts` → `VirtualPoGoPlus-V2-debug`

APK dosyasını buradan alın.

Eğer workflow `android.api` veya `android.ndk` satırlarında araç sürümü uyumsuzluğu verirse, hata logunu paylaşın; Python-for-Android/Buildozer sürümüne göre pinleme yapılabilir.

## "BLE başlatma hatası: ClassNotFoundException: ...BlePeripheral" hatası hakkında

Bu hata, `android_src/` altındaki özel Java sınıfının derlenen APK'ya dahil edilmediğini gösterir. Bunun en sık nedeni, Buildozer'ın `buildozer.spec` veya `android_src/` değişikliklerini var olan bir `.buildozer` derleme önbelleğine otomatik olarak yansıtmamasıdır.

Bu depo artık her GitHub Actions çalıştırmasında `.buildozer` ve `bin` klasörlerini derleme öncesi temizliyor, bu yüzden GitHub Actions üzerinden alınan yeni bir APK bu sorunu yaşamamalı.

Yerelde (kendi bilgisayarınızda) derliyorsanız ve `android_src/` içinde değişiklik yaptıysanız, her zaman şunu çalıştırın:

```
buildozer appclean
buildozer android debug
```

`android.api`/`android.ndk` değerleri de artık daha kararlı ve yaygın test edilmiş sürümlere (`34` / `25b`) sabitlendi; çok yeni sürümler bazı p4a gradle şablonlarıyla uyumsuz çalışabiliyor.

### Hata temiz bir yeniden derlemeden sonra bile devam ederse

`android.add_src`'nin kendisi bazı python-for-android sürümlerinde derleme sırasında hata vermeden, ama sınıfı APK'ya dahil etmeden sessizce başarısız olabiliyor (bilinen bir p4a davranışı). Bunu kesin olarak çözmek için depoya `p4a_hook.py` eklendi: bu, APK derlenmeden hemen önce çalışıp `android_src/` içindeki Java dosyalarını p4a'nın kendi sınıflarıyla birebir aynı klasöre (`src/main/java/...`) doğrudan kopyalar. Bu klasör Gradle'ın varsayılan ana kaynak kümesidir ve hiçbir şablona bağlı değildir, o yüzden atlanma ihtimali yoktur.

Yeni APK'yı test etmeden önce:

1. GitHub Actions derleme loglarında `[p4a_hook]` ile başlayan satırları arayın — `BlePeripheral.java` dosyasının kopyalandığını gösteren bir satır görmelisiniz. Görmüyorsanız log çıktısını paylaşın.
2. Telefonda **eski uygulamayı tamamen kaldırın**, sonra yeni indirilen APK'yı kurun (üzerine yükleme bazen eski sürümü güncellemeyebiliyor).
3. En son GitHub Actions çalıştırmasından (en yeni tarih/commit) indirdiğinizden emin olun.
