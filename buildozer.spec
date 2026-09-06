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

# Android 16 / API 36 hedefi
android.api = 36
android.minapi = 26
android.ndk = 28c
android.ndk_api = 26
android.accept_sdk_license = True
android.add_src = android_src
android.archs = arm64-v8a
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

