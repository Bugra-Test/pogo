"""python-for-android build hook.

`android.add_src` in buildozer.spec relies on python-for-android's Jinja
gradle template adding an extra `srcDir` entry to the `main` sourceSet.
This mechanism has proven unreliable across some p4a/AGP version
combinations (see e.g. kivy/python-for-android#1136) -- the build
succeeds, but the extra Java file silently never gets compiled in,
producing a runtime `ClassNotFoundException` from pyjnius even though
nothing looks wrong in the build log.

To make this bulletproof, this hook runs right before the Gradle/APK
build step and copies our custom Java sources *directly* into the same
`src/main/java/...` folder where p4a's own PythonActivity.java lives.
That folder is always part of the default Gradle sourceSet -- no
template, no extra config, no way to miss it.
"""

import os
import shutil


def before_apk_build(toolchain):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    src_root = os.path.join(project_dir, "android_src")
    dist_dir = toolchain._dist.dist_dir
    target_root = os.path.join(dist_dir, "src", "main", "java")

    if not os.path.isdir(src_root):
        print(f"[p4a_hook] UYARI: android_src klasoru bulunamadi: {src_root}")
        return

    copied = []
    for dirpath, _dirnames, filenames in os.walk(src_root):
        rel = os.path.relpath(dirpath, src_root)
        target_dir = target_root if rel == "." else os.path.join(target_root, rel)
        for fname in filenames:
            if not fname.endswith(".java"):
                continue
            os.makedirs(target_dir, exist_ok=True)
            src_file = os.path.join(dirpath, fname)
            dst_file = os.path.join(target_dir, fname)
            shutil.copy2(src_file, dst_file)
            copied.append(dst_file)

    if copied:
        print("[p4a_hook] Ozel Java kaynaklari dogrudan ana sourceSet'e kopyalandi:")
        for f in copied:
            print(f"[p4a_hook]   -> {f}")
    else:
        print(f"[p4a_hook] UYARI: {src_root} icinde .java dosyasi bulunamadi.")
