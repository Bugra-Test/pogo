# Windows'ta APK derleme

Buildozer doğrudan Windows üzerinde en sorunsuz seçenek değildir. WSL2 + Ubuntu kullanın.

PowerShell (Yönetici):

```powershell
wsl --install -d Ubuntu
```

Ubuntu içinde temel paketleri kurup proje klasörünü WSL dosya sistemine kopyalayın. Sonra README'deki Python/Buildozer komutlarını çalıştırın.

APK çıktısı:

```text
bin/virtualpogoplus-0.1.0-arm64-v8a_armeabi-v7a-debug.apk
```

Dosya adı Buildozer sürümüne göre küçük farklılık gösterebilir; kesin konum `bin/` klasörüdür.
