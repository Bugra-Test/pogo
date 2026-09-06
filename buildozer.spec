[app]
title = Virtual PoGo Plus
package.name = virtualpogoplus
package.domain = com.example
source.dir = .
source.include_exts = py,json,md,java
source.exclude_dirs = .git,.github,.buildozer,bin,venv,.venv,__pycache__

version = 0.2.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Modern target: avoids the "built for an older Android version" warning
# on current Android releases.
android.api = 36
android.minapi = 26
android.ndk = 28c
android.ndk_api = 26
android.accept_sdk_license = True

# Java source is copied into the generated Android project.
android.add_src = android_src

# Android 12+ BLE permissions.
android.permissions = BLUETOOTH_ADVERTISE,BLUETOOTH_CONNECT

android.archs = arm64-v8a
android.allow_backup = False
android.enable_androidx = True
android.logcat_filters = *:S python:D AndroidRuntime:E VirtualPoGoPlus:D

[buildozer]
log_level = 2
warn_on_root = 1
