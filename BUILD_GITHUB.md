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
