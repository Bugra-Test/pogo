[app]
title = Virtual PoGo Plus
package.name = virtualpogoplus
package.domain = com.example
source.dir = .
source.include_exts = py,json,md,java
version = 0.1.0
requirements = python3,kivy,certifi,chardet,filetype,idna,requests,six,urllib3
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 26
android.ndk = 27c
android.accept_sdk_license = True
android.add_src = android_src
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_ADVERTISE,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = False
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
