[app]
title = Virtual PoGo Plus V2
package.name = virtualpogoplus
package.domain = com.example
source.dir = .
source.include_exts = py,json,md,java
version = 0.2.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

# Kararlı ve iyi test edilmiş API/NDK sürümleri.
# NOT: Çok yeni/az test edilmiş android.api veya android.ndk sürümleri,
# python-for-android'in gradle şablonlarıyla uyumsuzluk riskini artırır ve
# android.add_src ile eklenen özel Java sınıflarının derlemeye dahil
# edilmemesine (ClassNotFoundException) yol açabilir.
android.api = 34
android.minapi = 26
android.ndk = 25b
android.ndk_api = 26
android.accept_sdk_license = True

# ÖNEMLİ: android_src/ altındaki Java dosyaları paket hiyerarşisini
# yansıtmalıdır (bu projede: android_src/com/example/virtualpogoplus/...).
# Bu ayar doğrudur, ANCAK Buildozer, buildozer.spec/android_src
# değişikliklerini var olan bir .buildozer derleme önbelleğine OTOMATİK
# YANSITMAZ. android_src/ içeriğini veya bu dosyayı değiştirdikten sonra
# MUTLAKA önce temiz bir derleme yapın, yoksa yeni Java sınıfı APK'ya
# eklenmeden eski önbellek kullanılmaya devam eder ve pyjnius çalışma
# zamanında "Didn't find class" hatası verir:
#   buildozer appclean
#   buildozer android debug
android.add_src = android_src
android.archs = arm64-v8a

# BlePeripheral.java gibi özel Java sınıflarının derlemeye kesin olarak
# dahil edilmesini garantiler (android.add_src'in bazı p4a sürümlerinde
# sessizce çalışmaması ihtimaline karşı). p4a_hook.py, build.py'ın
# APK'yı derlemesinden hemen önce çalışır ve android_src/ içeriğini
# doğrudan p4a'nın kendi Java kaynaklarıyla aynı klasöre kopyalar.
p4a.hook = p4a_hook.py
android.allow_backup = False

# Android 12+ BLE izinleri
android.permissions = BLUETOOTH_ADVERTISE,BLUETOOTH_CONNECT

# Python-for-Android giriş noktası
android.entrypoint = org.kivy.android.PythonActivity

# Daha yeni Android sürümlerinde uygulamanın açılışta çökmesini azaltmak için
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1

