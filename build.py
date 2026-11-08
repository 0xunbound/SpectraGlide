"""
AetherNet Build & Packaging Orchestrator
Automates strategy compilation, file scrubbing, directory staging, and Inno Setup compilation.
"""

import os
import sys
import shutil
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
CORE_DIR = os.path.join(PROJECT_ROOT, "core")
INSTALLER_DIR = os.path.join(PROJECT_ROOT, "installer")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

INNO_SETUP_PATHS = [
    r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    r"C:\Program Files\Inno Setup 6\ISCC.exe",
    r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "ISCC.exe"
]

def find_iscc() -> str | None:
    for path in INNO_SETUP_PATHS:
        if os.path.exists(path):
            return path
        # Check PATH
        which_path = shutil.which(path)
        if which_path:
            return which_path
    return None

def step_generate_strategies():
    print("[1/4] Компиляция и оптимизация стратегий...")
    script = os.path.join(PROJECT_ROOT, "tools", "strategy_converter.py")
    res = subprocess.run([sys.executable, script, "--output-json", os.path.join(CONFIG_DIR, "strategies.json"), "--output-config-dir", CONFIG_DIR], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Ошибка компиляции стратегий:\n{res.stderr}")
        return False
    print("  -> strategies.json и правила хостов успешно обновлены.")
    return True

def step_prepare_staging():
    print("[2/4] Подготовка структуры директорий и бинарников...")
    os.makedirs(BIN_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # Note for user regarding driver and worker binaries
    worker_path = os.path.join(BIN_DIR, "core-worker.exe")
    driver_dll = os.path.join(BIN_DIR, "WinDivert.dll")
    driver_sys = os.path.join(BIN_DIR, "WinDivert64.sys")
    
    missing = []
    if not os.path.exists(worker_path):
        missing.append("core-worker.exe (переименованный рабочий бинарник winws)")
    if not os.path.exists(driver_dll):
        missing.append("WinDivert.dll")
    if not os.path.exists(driver_sys):
        missing.append("WinDivert64.sys")
        
    if missing:
        print("  [!] Внимание: Для полноценной сборки исполняемого ядра в папку 'bin/' поместите:")
        for m in missing:
            print(f"      - {m}")
        print("  -> Скрипт продолжит сборку установщика со всеми конфигурациями и диагностикой.")
    else:
        print("  -> Все бинарные компоненты и драйверы найдены в папке bin/.")
    return True

def step_compile_installer():
    print("[3/4] Поиск компилятора Inno Setup (ISCC)...")
    iscc = find_iscc()
    iss_file = os.path.join(INSTALLER_DIR, "setup.iss")
    
    if not iscc:
        print("  [-] Inno Setup 6 не обнаружен по стандартным путям.")
        print(f"      Скрипт сборщика сохранен: {iss_file}")
        print("      Установите Inno Setup 6 (https://jrsoftware.org/isdl.php)")
        print(f"      и скомпилируйте файл вручную или запустите: ISCC.exe \"{iss_file}\"")
        return False
        
    print(f"  [+] Найден компилятор: {iscc}")
    print("[4/4] Сборка дистрибутива AetherNet...")
    res = subprocess.run([iscc, iss_file], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\n[УСПЕХ] Готовый инсталлятор собран в папке:\n  {DIST_DIR}\\AetherNet_Setup_v2.0.exe")
        return True
    else:
        print(f"Ошибка компиляции Inno Setup:\n{res.stderr or res.stdout}")
        return False

def main():
    print("=" * 60)
    print("      AetherNet Build System (White-Label Packaging)")
    print("=" * 60)
    if not step_generate_strategies():
        return
    step_prepare_staging()
    step_compile_installer()
    print("=" * 60)

if __name__ == "__main__":
    main()
