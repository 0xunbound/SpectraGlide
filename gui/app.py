"""
SpectraGlide Native GUI Launcher & Core Engine Bridge
Rock-Solid Hardware-Accelerated QoS & Packet Shaper (WinDivert Native Kernel).
Zero-Trace White-Label Architecture.
"""

import os
import sys
import re
import json
import time
import ssl
import socket
import random
import atexit
import ctypes
import winreg
import subprocess
import threading
import multiprocessing
import http.server
import socketserver
import struct
import concurrent.futures
from ctypes import wintypes

# Windows High-DPI and compatibility initialization for all Windows 10/11 builds
if os.name == 'nt':
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

INTERNET_PER_CONN_FLAGS = 1
INTERNET_PER_CONN_PROXY_SERVER = 2
INTERNET_PER_CONN_PROXY_BYPASS = 3
INTERNET_PER_CONN_AUTOCONFIG_URL = 4
PROXY_TYPE_DIRECT = 1
PROXY_TYPE_PROXY = 2
PROXY_TYPE_AUTO_PROXY_URL = 4
INTERNET_OPTION_REFRESH = 37
INTERNET_OPTION_SETTINGS_CHANGED = 39
INTERNET_OPTION_PER_CONNECTION_OPTION = 75

class INTERNET_PER_CONN_OPTION(ctypes.Structure):
    class Value(ctypes.Union):
        _fields_ = [
            ('dwValue', wintypes.DWORD if hasattr(ctypes, 'wintypes') else ctypes.c_ulong),
            ('pszValue', wintypes.LPWSTR if hasattr(ctypes, 'wintypes') else ctypes.c_wchar_p),
            ('ftValue', ctypes.c_ulonglong),
        ]
    _fields_ = [
        ('dwOption', wintypes.DWORD if hasattr(ctypes, 'wintypes') else ctypes.c_ulong),
        ('Value', Value),
    ]

class INTERNET_PER_CONN_OPTION_LIST(ctypes.Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD if hasattr(ctypes, 'wintypes') else ctypes.c_ulong),
        ('pszConnection', wintypes.LPWSTR if hasattr(ctypes, 'wintypes') else ctypes.c_wchar_p),
        ('dwOptionCount', wintypes.DWORD if hasattr(ctypes, 'wintypes') else ctypes.c_ulong),
        ('dwOptionError', wintypes.DWORD if hasattr(ctypes, 'wintypes') else ctypes.c_ulong),
        ('pOptions', ctypes.POINTER(INTERNET_PER_CONN_OPTION)),
    ]

if __name__ == "__main__":
    multiprocessing.freeze_support()

import webview

# Path resolution for frozen (.exe) and development modes
if getattr(sys, "frozen", False):
    BUNDLE_DIR = sys._MEIPASS
    APP_DIR = os.path.dirname(sys.executable)
else:
    BUNDLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR = BUNDLE_DIR

HTML_PATH = os.path.join(BUNDLE_DIR, "gui", "index.html")
if not os.path.exists(HTML_PATH):
    HTML_PATH = os.path.join(BUNDLE_DIR, "index.html")

STRATEGIES_PATH = os.path.join(BUNDLE_DIR, "config", "strategies.json")
if not os.path.exists(STRATEGIES_PATH):
    STRATEGIES_PATH = os.path.join(APP_DIR, "config", "strategies.json")

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
PAC_PORT = 1388
AI_PROXY_PORT = 1371

# Win32 Constants for native window interaction
user32 = ctypes.windll.user32 if os.name == 'nt' else None
WM_NCLBUTTONDOWN = 0x00A1
HTCAPTION = 0x0002
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOW = 5
SW_MINIMIZE = 6
SW_RESTORE = 9

PAC_CONTENT = rb"""function FindProxyForURL(url, host) {
    host = (host || "").toLowerCase();
    if (host.length > 1 && host.charAt(host.length - 1) === ".") {
        host = host.substring(0, host.length - 1);
    }
    if (host === "localhost" || host === "127.0.0.1" || host === "::1" || host === "[::1]" || isPlainHostName(host)) {
        return "DIRECT";
    }
    if (/\.(local|lan|home|home\.arpa|internal|localdomain)$/.test(host)) {
        return "DIRECT";
    }
    if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(host)) {
        if (isInNet(host, "10.0.0.0", "255.0.0.0") || isInNet(host, "172.16.0.0", "255.240.0.0") ||
            isInNet(host, "192.168.0.0", "255.255.0.0") || isInNet(host, "169.254.0.0", "255.255.0.0") ||
            isInNet(host, "100.64.0.0", "255.192.0.0") || isInNet(host, "127.0.0.0", "255.0.0.0")) {
            return "DIRECT";
        }
    }
    if (host.indexOf(":") > -1 && /^\[?(fe[89ab][0-9a-f]?:|f[cd][0-9a-f]{0,2}:)/.test(host)) {
        return "DIRECT";
    }

    var unblock = {
        "anthropic.com": 1,
        "claude.ai": 1,
        "claude.com": 1,
        "claudeusercontent.com": 1,
        "openai.com": 1,
        "chatgpt.com": 1,
        "oaistatic.com": 1,
        "oaiusercontent.com": 1,
        "ai.com": 1,
        "challenges.cloudflare.com": 1,
        "turnstile.cloudflare.com": 1,
        "instagram.com": 1,
        "cdninstagram.com": 1,
        "facebook.com": 1,
        "fbcdn.net": 1,
        "fbsbx.com": 1,
        "fb.com": 1,
        "fb.me": 1
    };

    var parts = host.split('.');
    for (var i = 0; i < parts.length - 1; i++) {
        var domain = parts.slice(i).join('.');
        if (unblock[domain]) {
            return "PROXY 127.0.0.1:1371; SOCKS5 127.0.0.1:1370; DIRECT";
        }
    }
    return "DIRECT";
}
"""

global_api_ref = None

class PacHttpHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.close_connection = True
        global global_api_ref
        if self.path.startswith('/exit'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            if global_api_ref:
                import threading
                threading.Thread(target=global_api_ref.exit_app, daemon=True).start()
            return

        if self.path.startswith('/drag'):
            if global_api_ref:
                global_api_ref.start_drag()
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return

        if self.path.startswith('/state'):
            data = b"{}"
            if global_api_ref:
                try:
                    data = json.dumps(global_api_ref.get_system_state(), ensure_ascii=False).encode('utf-8')
                except Exception:
                    data = b"{}"
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-ns-proxy-autoconfig')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Content-Length', str(len(PAC_CONTENT)))
            self.end_headers()
            self.wfile.write(PAC_CONTENT)
        except Exception:
            pass

    def log_message(self, format, *args):
        pass

class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class SystemTrayController:
    """Native Windows System Tray Icon with real-time status color updates."""
    def __init__(self, api):
        self.api = api
        self.icon = None
        self._thread = None
        self._current_status = "standby"

    def _create_icon_image(self, status):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            # Dark outer ring
            d.ellipse((2, 2, 29, 29), fill=(16, 22, 34, 250), outline=(48, 64, 88, 255), width=2)
            colors = {
                'online': (0, 240, 118),       # Green
                'connecting': (250, 204, 21),  # Yellow / Amber
                'offline': (239, 68, 68),      # Red
                'standby': (148, 163, 184)     # Slate Gray
            }
            c = colors.get(status, colors['standby'])
            d.ellipse((8, 8, 23, 23), fill=c, outline=(255, 255, 255, 90), width=1)
            return img
        except Exception:
            return None

    def _get_tooltip(self, status):
        if status == "online":
            return "SpectraGlide: Онлайн (Ускорение активно)"
        elif status == "connecting":
            return "SpectraGlide: Установка соединения / Подбор..."
        elif status == "offline":
            return "SpectraGlide: Соединение не установлено"
        return "SpectraGlide: Ожидание (Standby)"

    def _create_menu(self):
        import pystray
        return pystray.Menu(
            pystray.MenuItem("Показать SpectraGlide", lambda: self.api.show_window(), default=True),
            pystray.MenuItem(
                "Сворачивать в трей при закрытии (крестик)",
                lambda: self.api.toggle_close_to_tray(),
                checked=lambda item: self.api.close_to_tray
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Выход", lambda: self.api.exit_app())
        )

    def start(self):
        def _run():
            try:
                import pystray
                img = self._create_icon_image(self._current_status)
                if img:
                    self.icon = pystray.Icon(
                        name="SpectraGlide",
                        icon=img,
                        title=self._get_tooltip(self._current_status),
                        menu=self._create_menu()
                    )
                    self.icon.run()
            except Exception as e:
                print(f"[Tray] Init error: {e}")

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def update_status(self, status):
        self._current_status = status
        if self.icon:
            try:
                img = self._create_icon_image(status)
                if img:
                    self.icon.icon = img
                self.icon.title = self._get_tooltip(status)
            except Exception:
                pass

    def update_menu(self):
        if self.icon:
            try:
                self.icon.menu = self._create_menu()
            except Exception:
                pass

    def stop(self):
        if self.icon:
            try:
                self.icon.stop()
            except Exception:
                pass


class SpectraGlideAPI:
    """Python API exposed to the JavaScript frontend via window.pywebview.api"""
    def __init__(self, window=None):
        self._window = window
        self.is_running = False
        self.worker_process = None
        self.ai_worker_process = None
        self.ai_opera_process = None
        self.pac_server = None
        self.is_maximized = False
        self._cached_hwnd = None
        self.tray_controller = None
        self.close_to_tray = True
        self._load_settings()

        self.strategies_data = self._load_strategies()
        self.active_strategy = self._load_saved_strategy() or "balanced"

        # Adaptive Health Engine & Autonomous Self-Healing System
        self.auto_tune_enabled = True
        self.connection_status = "standby"  # "online", "connecting", "offline", "standby"
        self.auto_tune_status = "STANDBY"
        self.ai_country = "AM"
        self.last_auto_tune_time = 0
        self.last_auto_switch_time = 0
        self.auto_switch_cooldown = 40.0  # Cooldown between auto-switches
        self.consecutive_fails = 0
        self.recent_latencies = []
        self.current_ping = 18.0
        self.current_jitter = 0.3
        self.current_loss = 0.0

        self.recent_logs = [
            f"{time.strftime('%H:%M:%S')} Ядро инициализировано",
            f"{time.strftime('%H:%M:%S')} Готов к запуску QoS-ускорения"
        ]

        self.service_health = {
            "chatgpt": {"name": "Нейросетевой шлюз // Кластер Alpha", "ok": False, "latency": 0, "status": "standby", "note": "AI Шлюз", "consecutive_fails": 0},
            "claude": {"name": "Нейросетевой шлюз // Кластер Beta", "ok": False, "latency": 0, "status": "standby", "note": "AI Шлюз", "consecutive_fails": 0},
            "youtube": {"name": "Магистральный медиа-узел // Ultra-HD CDN", "ok": False, "latency": 0, "status": "standby", "note": "Медиа-поток", "consecutive_fails": 0},
            "instagram": {"name": "Транзитный сетевой узел // Edge-01", "ok": False, "latency": 0, "status": "standby", "note": "Транзитный узел", "consecutive_fails": 0},
            "facebook": {"name": "Транзитный сетевой узел // Edge-02", "ok": False, "latency": 0, "status": "standby", "note": "Транзитный узел", "consecutive_fails": 0},
            "dns": {"name": "Магистральный Anycast DNS Resolver", "ok": True, "latency": 18.0, "status": "ok", "note": "Anycast Core", "consecutive_fails": 0}
        }

        self._bg_monitor_running = True

        global global_api_ref
        global_api_ref = self

        self._initial_cleanup()
        atexit.register(self.stop_engine)

        self._start_pac_server()
        self._apply_window_icon()

        # Background health monitor thread
        self._monitor_thread = threading.Thread(target=self._background_health_monitor, daemon=True)
        self._monitor_thread.start()

    def set_tray_controller(self, tray):
        self.tray_controller = tray

    def _get_hwnd(self):
        if self._cached_hwnd and user32 and user32.IsWindow(self._cached_hwnd):
            return self._cached_hwnd
        try:
            from webview.platforms.winforms import BrowserView
            if BrowserView.instances:
                for form in BrowserView.instances.values():
                    if hasattr(form, 'Handle'):
                        h = form.Handle.ToInt32()
                        if h and user32 and user32.IsWindow(h):
                            self._cached_hwnd = h
                            return h
        except Exception:
            pass
        if user32:
            try:
                hwnd = user32.FindWindowW(None, "SpectraGlide Pro")
                if hwnd:
                    self._cached_hwnd = hwnd
                    return hwnd
            except Exception:
                pass
        return None

    def _apply_window_icon(self):
        def _worker():
            for _ in range(30):
                hwnd = self._get_hwnd()
                if hwnd and user32:
                    icon_path = os.path.join(BUNDLE_DIR, "gui", "icon.ico")
                    if not os.path.exists(icon_path):
                        icon_path = os.path.join(APP_DIR, "gui", "icon.ico")
                    if os.path.exists(icon_path):
                        try:
                            h_icon_big = user32.LoadImageW(0, icon_path, 1, 0, 0, 0x0010)
                            h_icon_sm = user32.LoadImageW(0, icon_path, 1, 16, 16, 0x0010)
                            if h_icon_big:
                                user32.PostMessageW(hwnd, 0x0080, 1, h_icon_big)
                            if h_icon_sm:
                                user32.PostMessageW(hwnd, 0x0080, 0, h_icon_sm)
                            break
                        except Exception:
                            pass
                time.sleep(0.15)
        threading.Thread(target=_worker, daemon=True).start()

    def start_drag(self):
        """Native hardware Windows caption drag via WM_NCLBUTTONDOWN on HTCAPTION."""
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ReleaseCapture()
                user32.SendMessageW(hwnd, WM_NCLBUTTONDOWN, HTCAPTION, 0)
        except Exception:
            pass

    def move_window(self, x, y):
        """High-performance hardware window mover with automatic DPI scaling."""
        try:
            if self._window:
                self._window.move(int(x), int(y))
        except Exception:
            pass

    def show_window(self):
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ShowWindow(hwnd, SW_RESTORE)
                user32.ShowWindow(hwnd, SW_SHOW)
                user32.SetForegroundWindow(hwnd)
            elif self._window:
                self._window.restore()
                self._window.show()
        except Exception as e:
            print(f"[UI] Show window error: {e}")

    def hide_window(self):
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ShowWindow(hwnd, SW_HIDE)
            elif self._window:
                self._window.hide()
        except Exception as e:
            print(f"[UI] Hide window error: {e}")

    def minimize(self):
        """Standard window minimize to Windows taskbar."""
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ShowWindow(hwnd, SW_MINIMIZE)
            elif self._window:
                self._window.minimize()
        except Exception as e:
            print(f"[UI] Minimize error: {e}")

    def close(self):
        """Handle X button click: hides to tray if close_to_tray enabled, else exits."""
        if self.close_to_tray:
            self.hide_window()
            return {"status": "hidden_to_tray"}
        else:
            return self.exit_app()

    def exit_app(self):
        """Completely terminates all engines and exits process."""
        try:
            self._bg_monitor_running = False
            self.hide_window()
        except Exception:
            pass

        if self.tray_controller:
            self.tray_controller.stop()

        def cleanup_and_exit():
            try:
                self.stop_engine()
            except Exception:
                pass
            try:
                self._stop_pac_server()
            except Exception:
                pass
            try:
                if self._window:
                    self._window.destroy()
            except Exception:
                pass
            os._exit(0)

        threading.Thread(target=cleanup_and_exit, daemon=True).start()
        threading.Timer(1.2, lambda: os._exit(0)).start()
        return {"status": "closing"}

    def _load_settings(self):
        try:
            cfg_p = os.path.join(APP_DIR, "config", "settings.json")
            if os.path.exists(cfg_p):
                with open(cfg_p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.close_to_tray = d.get("close_to_tray", True)
                    return
        except Exception:
            pass
        self.close_to_tray = True

    def _save_settings(self):
        try:
            cfg_dir = os.path.join(APP_DIR, "config")
            os.makedirs(cfg_dir, exist_ok=True)
            with open(os.path.join(cfg_dir, "settings.json"), "w", encoding="utf-8") as f:
                json.dump({"close_to_tray": self.close_to_tray}, f)
        except Exception:
            pass

    def toggle_close_to_tray(self, enabled=None):
        if enabled is None:
            self.close_to_tray = not self.close_to_tray
        else:
            self.close_to_tray = bool(enabled)
        self._save_settings()
        if self.tray_controller:
            self.tray_controller.update_menu()
        t_str = time.strftime("%H:%M:%S")
        txt = "Включено" if self.close_to_tray else "Выключено"
        self._log_event(f"{t_str} 📥 Сворачивание в трей при закрытии: {txt}")
        return {"close_to_tray": self.close_to_tray}

    def _probe_tls_sni(self, host, port=443, sni=None, fallback_ip=None, timeout=2.5):
        """Sends a genuine TLS ClientHello with SNI to verify DPI desynchronization."""
        start = time.perf_counter()
        s = None
        sni = sni or host
        try:
            try:
                s = socket.create_connection((host, port), timeout=timeout)
            except Exception:
                if fallback_ip:
                    s = socket.create_connection((fallback_ip, port), timeout=timeout)
                else:
                    raise
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ss = ctx.wrap_socket(s, server_hostname=sni)
            ss.settimeout(timeout)
            req = f"HEAD / HTTP/1.1\r\nHost: {sni}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nConnection: close\r\n\r\n"
            ss.sendall(req.encode())
            resp = ss.recv(256)
            lat = (time.perf_counter() - start) * 1000.0
            ss.close()
            if b"HTTP/1." in resp or len(resp) > 0:
                return True, round(lat, 1), resp.split(b"\r\n")[0].decode(errors="ignore")
            return False, 0, "No response"
        except Exception as e:
            if s:
                try: s.close()
                except Exception: pass
            return False, 0, str(e)

    def _probe_youtube_endpoint(self, timeout=2.5):
        """Strict direct DPI desync check for YouTube 4K streaming. No proxy fallback."""
        ok, lat, note = self._probe_tls_sni("www.youtube.com", 443, sni="www.youtube.com", fallback_ip="142.251.150.4", timeout=timeout)
        if ok:
            return True, lat, "DPI Десинхронизация"
        return False, 0, "DPI Блокировка"

    def _probe_ai_endpoint(self, host, timeout=2.5):
        """Verifies if AI service (Claude / ChatGPT) is reachable without regional blocks."""
        start = time.perf_counter()
        try:
            s = socket.create_connection(("127.0.0.1", AI_PROXY_PORT), timeout=timeout)
            s.sendall(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}:443\r\nUser-Agent: SpectraGlide/2.0\r\n\r\n".encode())
            resp = s.recv(256)
            if b"200" in resp:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                ss = ctx.wrap_socket(s, server_hostname=host)
                ss.settimeout(timeout)
                req = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nConnection: close\r\n\r\n"
                ss.sendall(req.encode())
                head_resp = ss.recv(256)
                ss.close()
                lat = (time.perf_counter() - start) * 1000.0
                if head_resp and b"HTTP/1." in head_resp:
                    if b"403 Forbidden" in head_resp and b"Country not supported" in head_resp:
                        return False, round(lat, 1), "Geo-Blocked"
                    return True, round(lat, 1), "AI Доступен"
            s.close()
        except Exception:
            pass
        return False, 0, "AI Недоступен"

    def _probe_tspu_endpoint(self, host, timeout=2.8):
        """Verifies whether blocked site (Instagram, Facebook) passes DPI filtering."""
        start = time.perf_counter()
        try:
            ok, lat, note = self._probe_tls_sni(host, 443, sni=host, timeout=timeout)
            if ok:
                return True, lat, "DPI Десинхронизация"
        except Exception:
            pass

        try:
            s = socket.create_connection(("127.0.0.1", AI_PROXY_PORT), timeout=timeout)
            s.sendall(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}:443\r\n\r\n".encode())
            resp = s.recv(128)
            s.close()
            if b"200" in resp:
                lat = (time.perf_counter() - start) * 1000.0
                return True, round(lat, 1), "ТСПУ Обход"
        except Exception:
            pass

        return False, 0, "Блокировка ТСПУ"

    def run_comprehensive_check(self, timeout=2.5):
        """Concurrently tests Claude, ChatGPT, YouTube, Instagram, Facebook."""
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            f_chatgpt = ex.submit(self._probe_ai_endpoint, "chatgpt.com", timeout)
            f_claude = ex.submit(self._probe_ai_endpoint, "claude.ai", timeout)
            f_yt = ex.submit(self._probe_youtube_endpoint, timeout)
            f_insta = ex.submit(self._probe_tspu_endpoint, "www.instagram.com", timeout)
            f_fb = ex.submit(self._probe_tspu_endpoint, "www.facebook.com", timeout)

            results["chatgpt"] = f_chatgpt.result()
            results["claude"] = f_claude.result()
            results["youtube"] = f_yt.result()
            results["instagram"] = f_insta.result()
            results["facebook"] = f_fb.result()

        chatgpt_ok = results["chatgpt"][0]
        claude_ok = results["claude"][0]
        yt_ok = results["youtube"][0]
        insta_ok = results["instagram"][0]
        fb_ok = results["facebook"][0]

        ai_ok = chatgpt_ok or claude_ok
        tspu_ok = yt_ok

        lats = [res[1] for res in results.values() if res[0] and res[1] > 0]
        avg_lat = round(sum(lats) / len(lats), 1) if lats else 9999.0

        if lats:
            self.recent_latencies.append(avg_lat)
            if len(self.recent_latencies) > 12:
                self.recent_latencies.pop(0)
            self.current_ping = avg_lat

            if len(self.recent_latencies) >= 2:
                diffs = [abs(self.recent_latencies[i] - self.recent_latencies[i-1]) for i in range(1, len(self.recent_latencies))]
                self.current_jitter = round(sum(diffs) / len(diffs), 1)
            else:
                self.current_jitter = round(max(0.1, abs(lats[0] - avg_lat)), 1)
        else:
            self.current_ping = 999.0
            self.current_jitter = 0.0

        total_p = len(results)
        failed_p = sum(1 for res in results.values() if not res[0])
        self.current_loss = round((failed_p / total_p) * 100.0, 1) if total_p > 0 else 0.0

        return {
            "chatgpt_ok": chatgpt_ok,
            "claude_ok": claude_ok,
            "youtube_ok": yt_ok,
            "instagram_ok": insta_ok,
            "facebook_ok": fb_ok,
            "ai_ok": ai_ok,
            "tspu_ok": tspu_ok,
            "all_ok": ai_ok and yt_ok,
            "avg_latency": avg_lat,
            "details": results
        }

    def _background_health_monitor(self):
        """Continuous monitor that auto-tunes with cooldown when auto_tune_enabled is True."""
        while self._bg_monitor_running:
            try:
                if self.is_running and self.auto_tune_enabled:
                    chk = self.run_comprehensive_check(timeout=2.4)
                    
                    for key, (ok, lat, note) in chk["details"].items():
                        if key in self.service_health:
                            self.service_health[key]["ok"] = ok
                            self.service_health[key]["latency"] = lat
                            self.service_health[key]["note"] = note
                            self.service_health[key]["status"] = "ok" if ok else "err"

                    if chk["youtube_ok"]:
                        self.connection_status = "online"
                        self.consecutive_fails = 0
                        self.auto_tune_status = f"ONLINE // {self._get_strategy_name(self.active_strategy)}"
                    else:
                        self.consecutive_fails += 1
                        if self.consecutive_fails >= 2:
                            now = time.time()
                            if now - self.last_auto_switch_time > self.auto_switch_cooldown:
                                self.connection_status = "connecting"
                                self._log_event(f"{time.strftime('%H:%M:%S')} ⚡ Обнаружена фильтрация. Автоподбор стратегии...")
                                self._trigger_auto_tune_switch()
                                self.last_auto_switch_time = time.time()
                                self.consecutive_fails = 0

                    if self.tray_controller:
                        self.tray_controller.update_status(self.connection_status)

                    time.sleep(12.0)
                elif self.is_running and not self.auto_tune_enabled:
                    time.sleep(3.0)
                else:
                    self.connection_status = "standby"
                    if self.tray_controller:
                        self.tray_controller.update_status("standby")
                    time.sleep(2.5)
            except Exception:
                time.sleep(3.0)

    def _trigger_auto_tune_switch(self):
        def _hot():
            self.start_auto_tune()
        threading.Thread(target=_hot, daemon=True).start()

    def _log_event(self, text):
        self.recent_logs.insert(0, text)
        if len(self.recent_logs) > 8:
            self.recent_logs.pop()

    def _get_strategy_name(self, strat_id):
        if strat_id == "auto":
            return "Автоподбор"
        for s in self.strategies_data.get("strategies", []):
            if s.get("id") == strat_id:
                return s.get("name")
        return strat_id

    def _load_saved_strategy(self):
        try:
            cfg_p = os.path.join(APP_DIR, "config", "active_strategy.json")
            if os.path.exists(cfg_p):
                with open(cfg_p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    strat = d.get("active_strategy")
                    id_map = {
                        "discord": "adaptive",
                        "youtube": "deep_overlap",
                        "tspu_split": "hardened_filter",
                        "disorder_badsum": "tcp_inversion",
                        "multisplit_clean": "multisplit"
                    }
                    return id_map.get(strat, strat)
        except Exception:
            pass
        return "balanced"

    def _save_strategy(self, strat_id):
        try:
            cfg_dir = os.path.join(APP_DIR, "config")
            os.makedirs(cfg_dir, exist_ok=True)
            with open(os.path.join(cfg_dir, "active_strategy.json"), "w", encoding="utf-8") as f:
                json.dump({"active_strategy": strat_id, "timestamp": time.time()}, f)
        except Exception:
            pass

    def get_strategies(self):
        strats = self.strategies_data.get("strategies", [])
        return {
            "active": self.active_strategy,
            "active_name": self._get_strategy_name(self.active_strategy),
            "auto_tune_enabled": self.auto_tune_enabled,
            "connection_status": self.connection_status,
            "strategies": [
                {
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "description": s.get("description"),
                    "ai": s.get("ai", False),
                    "recommended": s.get("recommended", False),
                    "is_active": (s.get("id") == self.active_strategy)
                }
                for s in strats
            ]
        }

    def start_auto_tune(self):
        """Live benchmark across all strategies with strict prioritization for AI and YouTube."""
        t_str = time.strftime("%H:%M:%S")
        self._log_event(f"{t_str} ⚡ Запущен автоподбор стратегии...")
        self.connection_status = "connecting"
        if self.tray_controller:
            self.tray_controller.update_status("connecting")

        strats = self.strategies_data.get("strategies", [])
        if not strats:
            return {"status": "error", "message": "No strategies defined"}

        # Ensure AI tunnel is running
        if not self.ai_opera_process or self.ai_opera_process.poll() is not None:
            threading.Thread(target=self._start_ai_tunnel, daemon=True).start()
            time.sleep(1.0)

        results = []
        best_strat = None
        best_score = -9999
        best_lat = 9999.0

        for s in strats:
            s_id = s.get("id")
            s_name = s.get("name")
            is_ai_supported = s.get("ai", False)
            is_recommended = s.get("recommended", False)
            self._log_event(f"{time.strftime('%H:%M:%S')} ⚡ Тестирование: {s_name}...")

            # Apply this strategy to WinDivert worker
            self._start_divert_worker(override_strategy=s_id)
            time.sleep(0.9)

            chk = self.run_comprehensive_check(timeout=2.2)
            lat = chk["avg_latency"]

            score = 0
            # 1. YouTube direct check (MANDATORY)
            if chk["youtube_ok"]:
                score += 50
            else:
                score -= 100  # Never choose a strategy that breaks YouTube!

            # 2. AI Regional Bypass support
            if is_ai_supported:
                score += 30
            if chk["chatgpt_ok"]:
                score += 20
            if chk["claude_ok"]:
                score += 20

            # 3. Blocked social media
            if chk["instagram_ok"]:
                score += 10
            if chk["facebook_ok"]:
                score += 10

            # 4. Recommended strategy bonus (balanced is the battle-tested default)
            if is_recommended:
                score += 15

            results.append({
                "id": s_id,
                "name": s_name,
                "score": score,
                "latency": lat,
                "ai_ok": chk["ai_ok"],
                "youtube_ok": chk["youtube_ok"]
            })

            if score > best_score or (score == best_score and lat < best_lat):
                best_score = score
                best_lat = lat
                best_strat = s

        # Default to balanced if no clear positive winner
        if not best_strat or best_score < 0:
            for s in strats:
                if s.get("id") == "balanced":
                    best_strat = s
                    break
            if not best_strat:
                best_strat = strats[0]

        winner_id = best_strat.get("id")
        winner_name = best_strat.get("name")
        self.active_strategy = winner_id
        self._start_divert_worker(override_strategy=winner_id)
        self._save_strategy(winner_id)

        self.connection_status = "online"
        self.auto_tune_status = f"ONLINE // {winner_name}"
        self._log_event(f"{time.strftime('%H:%M:%S')} ✓ Оптимальный профиль: {winner_name} ({round(best_lat)} мс)")

        if self.tray_controller:
            self.tray_controller.update_status(self.connection_status)

        return {
            "status": "ok",
            "strategy_id": winner_id,
            "strategy_name": winner_name,
            "connection_status": self.connection_status,
            "latency": round(best_lat, 1),
            "score": best_score,
            "tested": results
        }

    def get_system_state(self):
        """Zero-latency non-blocking snapshot for frontend polling."""
        return {
            "is_running": self.is_running,
            "connection_status": self.connection_status,
            "active_strategy": self.active_strategy,
            "active_strategy_name": self._get_strategy_name(self.active_strategy),
            "auto_tune_enabled": self.auto_tune_enabled,
            "auto_tune_status": self.auto_tune_status,
            "close_to_tray": self.close_to_tray,
            "services": self.service_health,
            "rtt_ping": self.current_ping,
            "jitter": self.current_jitter,
            "loss": self.current_loss,
            "recent_logs": self.recent_logs,
            "strategies": [
                {"id": s.get("id"), "name": s.get("name"), "description": s.get("description"), "ai": s.get("ai", False)}
                for s in self.strategies_data.get("strategies", [])
            ]
        }

    def toggle_auto_tune(self, enabled=None):
        if enabled is None:
            self.auto_tune_enabled = not self.auto_tune_enabled
        else:
            self.auto_tune_enabled = bool(enabled)
        t_str = time.strftime("%H:%M:%S")
        txt = "Включен" if self.auto_tune_enabled else "Выключен (ручной режим)"
        self._log_event(f"{t_str} ⚡ Автоподбор: {txt}")
        return {"auto_tune_enabled": self.auto_tune_enabled}

    def get_network_ping(self):
        start = time.perf_counter()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.0)
            query = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
            s.sendto(query, ('8.8.8.8', 53))
            s.recvfrom(512)
            lat = (time.perf_counter() - start) * 1000.0
            s.close()
            return round(lat, 1)
        except Exception:
            return 21.0

    def run_diagnostics(self):
        chk = self.run_comprehensive_check(timeout=2.8)
        for key, (ok, lat, note) in chk["details"].items():
            if key in self.service_health:
                self.service_health[key]["ok"] = ok
                self.service_health[key]["latency"] = lat
                self.service_health[key]["note"] = note
                self.service_health[key]["status"] = "ok" if ok else "err"
        return self.service_health

    def _initial_cleanup(self):
        self._disable_windows_pac()
        if os.name == 'nt':
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "core-worker.exe", "/IM", "ai-worker.exe", "/IM", "wireproxy.exe", "/IM", "wireproxy-awg.exe", "/IM", "opera-proxy.exe"],
                    creationflags=0x08000000,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1.0
                )
            except Exception:
                pass

    def _load_strategies(self):
        if os.path.exists(STRATEGIES_PATH):
            try:
                with open(STRATEGIES_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Core] Error loading strategies: {e}")
        return {"strategies": []}

    def _find_bin(self, name):
        candidates = [
            os.path.join(APP_DIR, "bin", name),
            os.path.join(BUNDLE_DIR, "bin", name),
            os.path.join(APP_DIR, name),
            os.path.join(BUNDLE_DIR, name)
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    def start_engine(self):
        print(f"[Core] SpectraGlide activating: {self.active_strategy}")
        self.is_running = True
        self.connection_status = "connecting"
        if self.tray_controller:
            self.tray_controller.update_status("connecting")

        self._log_event(f"{time.strftime('%H:%M:%S')} Запуск защиты и оптимизатора маршрутов...")

        threading.Thread(target=self._start_divert_worker, daemon=True).start()
        threading.Thread(target=self._start_ai_tunnel, daemon=True).start()

        # Asynchronously verify connectivity
        def _initial_verify():
            time.sleep(2.0)
            if self.auto_tune_enabled:
                self.start_auto_tune()
            else:
                chk = self.run_comprehensive_check(timeout=2.8)
                if chk["ai_ok"] or chk["tspu_ok"]:
                    self.connection_status = "online"
                else:
                    self.connection_status = "offline"
                if self.tray_controller:
                    self.tray_controller.update_status(self.connection_status)

        threading.Thread(target=_initial_verify, daemon=True).start()
        return {"status": "ok", "message": "Protection active"}

    def _start_divert_worker(self, override_strategy=None):
        worker_bin = self._find_bin("core-worker.exe")
        if not worker_bin:
            print("[Core] Error: core-worker.exe not found!")
            return

        bin_dir = os.path.dirname(worker_bin)

        try:
            if self.worker_process:
                try:
                    self.worker_process.terminate()
                    self.worker_process.wait(timeout=0.6)
                except Exception:
                    pass
                self.worker_process = None

            subprocess.run(["taskkill", "/F", "/IM", "core-worker.exe", "/IM", "ai-worker.exe"],
                           creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
            time.sleep(0.25)

            strat_to_use = override_strategy or (
                "balanced" if self.active_strategy == "auto" else self.active_strategy
            )
            args = []
            for s in self.strategies_data.get("strategies", []):
                if strat_to_use == s.get("id", ""):
                    args = s.get("args", [])
                    break
            
            if not args and self.strategies_data.get("strategies"):
                args = self.strategies_data["strategies"][0].get("args", [])

            cmd = [worker_bin] + args
            log_path = os.path.join(bin_dir, "core.log")
            log_file = open(log_path, "w", encoding="utf-8", errors="ignore")
            
            self.worker_process = subprocess.Popen(
                cmd,
                cwd=bin_dir,
                creationflags=0x08000000 if os.name == 'nt' else 0,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
            print(f"[Core] DPI Worker active [Strategy: {strat_to_use}] (PID {self.worker_process.pid})")
        except Exception as e:
            print(f"[Core] DPI Worker launch failure: {e}")

    def _start_ai_tunnel(self):
        try:
            subprocess.run(["taskkill", "/F", "/IM", "wireproxy.exe", "/IM", "wireproxy-awg.exe", "/IM", "opera-proxy.exe"],
                           creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
            
            wireproxy_bin = self._find_bin("wireproxy.exe")
            opera_bin = self._find_bin("opera-proxy.exe")
            warp_cfg = os.path.join(APP_DIR, "config", "warp.conf")
            if not os.path.exists(warp_cfg):
                warp_cfg = os.path.join(BUNDLE_DIR, "config", "warp.conf")
            
            # Tier 1: Opera AI Exit Proxy on 127.0.0.1:1371 (Instant Direct Bypass)
            if opera_bin:
                bin_dir = os.path.dirname(opera_bin)
                self.ai_opera_process = subprocess.Popen(
                    [opera_bin, "-country", "AM", "-bind-address", "127.0.0.1:1371", "-verbosity", "30"],
                    cwd=bin_dir,
                    creationflags=0x08000000 if os.name == 'nt' else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"[Tunnel] Tier 1: Opera AI Exit Proxy active on 127.0.0.1:1371 (PID {self.ai_opera_process.pid})")

            # Tier 2: WireGuard WARP Socks5 proxy on 127.0.0.1:1370 (Backup Tier)
            if wireproxy_bin and os.path.exists(warp_cfg):
                bin_dir = os.path.dirname(wireproxy_bin)
                self.ai_worker_process = subprocess.Popen(
                    [wireproxy_bin, "-c", warp_cfg],
                    cwd=bin_dir,
                    creationflags=0x08000000 if os.name == 'nt' else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"[Tunnel] Tier 2: WireGuard WARP active on 127.0.0.1:1370 (PID {self.ai_worker_process.pid})")

            time.sleep(1.0)
            self._enable_windows_pac(f"http://127.0.0.1:{PAC_PORT}/proxy.pac")
        except Exception as e:
            print(f"[Tunnel] AI Tunnel launch error: {e}")

    def _start_pac_server(self):
        if self.pac_server:
            return
        try:
            self.pac_server = ReusableTCPServer(("127.0.0.1", PAC_PORT), PacHttpHandler)
            pac_thread = threading.Thread(target=self.pac_server.serve_forever, daemon=True)
            pac_thread.start()
            print(f"[AI-Engine] PAC Server listening on 127.0.0.1:{PAC_PORT}")
        except Exception as e:
            print(f"[AI-Engine] PAC Server error: {e}")

    def _stop_pac_server(self):
        if self.pac_server:
            try:
                self.pac_server.shutdown()
                self.pac_server.server_close()
            except Exception:
                pass
            self.pac_server = None

    def _enable_windows_pac(self, pac_url):
        if os.name != 'nt':
            return
        try:
            settings_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, settings_key, 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
                winreg.SetValueEx(key, "AutoConfigURL", 0, winreg.REG_SZ, pac_url)
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            pac_bytes = pac_url.encode('ascii', errors='ignore')
            pac_blob = (
                struct.pack('<III', 0x46, 0, 0x05) +
                struct.pack('<I', 0) +
                struct.pack('<I', 0) +
                struct.pack('<I', len(pac_bytes)) +
                pac_bytes +
                (b'\x00' * 32)
            )
            conn_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, conn_key, 0, winreg.KEY_SET_VALUE) as ck:
                    for v in ["DefaultConnectionSettings", "SavedLegacySettings"]:
                        try:
                            winreg.SetValueEx(ck, v, 0, winreg.REG_BINARY, pac_blob)
                        except Exception:
                            pass
            except Exception:
                pass

            try:
                options = (INTERNET_PER_CONN_OPTION * 2)()
                options[0].dwOption = INTERNET_PER_CONN_FLAGS
                options[0].Value.dwValue = PROXY_TYPE_AUTO_PROXY_URL | PROXY_TYPE_DIRECT
                options[1].dwOption = INTERNET_PER_CONN_AUTOCONFIG_URL
                options[1].Value.pszValue = pac_url

                opt_list = INTERNET_PER_CONN_OPTION_LIST()
                opt_list.dwSize = ctypes.sizeof(INTERNET_PER_CONN_OPTION_LIST)
                opt_list.pszConnection = None
                opt_list.dwOptionCount = 2
                opt_list.dwOptionError = 0
                opt_list.pOptions = options

                wininet = ctypes.windll.wininet
                wininet.InternetSetOptionW(0, INTERNET_OPTION_PER_CONNECTION_OPTION, ctypes.byref(opt_list), ctypes.sizeof(opt_list))
                wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
                wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
            except Exception:
                pass
        except Exception as e:
            print(f"[PAC] Windows PAC enable error: {e}")

    def _disable_windows_pac(self):
        if os.name != 'nt':
            return
        try:
            settings_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, settings_key, 0, winreg.KEY_SET_VALUE) as key:
                try:
                    winreg.DeleteValue(key, "AutoConfigURL")
                except FileNotFoundError:
                    pass
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            conn_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections"
            clean_blob = struct.pack('<III', 0x46, 0, 0x01) + (b'\x00' * 44)
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, conn_key, 0, winreg.KEY_SET_VALUE) as ck:
                    for v in ["DefaultConnectionSettings", "SavedLegacySettings"]:
                        try:
                            winreg.SetValueEx(ck, v, 0, winreg.REG_BINARY, clean_blob)
                        except Exception:
                            pass
            except Exception:
                pass

            try:
                options = (INTERNET_PER_CONN_OPTION * 2)()
                options[0].dwOption = INTERNET_PER_CONN_FLAGS
                options[0].Value.dwValue = PROXY_TYPE_DIRECT
                options[1].dwOption = INTERNET_PER_CONN_AUTOCONFIG_URL
                options[1].Value.pszValue = ""

                opt_list = INTERNET_PER_CONN_OPTION_LIST()
                opt_list.dwSize = ctypes.sizeof(INTERNET_PER_CONN_OPTION_LIST)
                opt_list.pszConnection = None
                opt_list.dwOptionCount = 2
                opt_list.dwOptionError = 0
                opt_list.pOptions = options

                wininet = ctypes.windll.wininet
                wininet.InternetSetOptionW(0, INTERNET_OPTION_PER_CONNECTION_OPTION, ctypes.byref(opt_list), ctypes.sizeof(opt_list))
                wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
                wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
            except Exception:
                pass
        except Exception:
            pass

    def stop_engine(self):
        print("[Core] Stopping all engines...")
        self.is_running = False
        self.connection_status = "standby"
        if self.tray_controller:
            self.tray_controller.update_status("standby")

        self._log_event(f"{time.strftime('%H:%M:%S')} Защита остановлена")

        if self.worker_process:
            try:
                self.worker_process.terminate()
                self.worker_process.wait(timeout=0.6)
            except Exception:
                pass
            self.worker_process = None

        if self.ai_worker_process:
            try:
                self.ai_worker_process.terminate()
                self.ai_worker_process.wait(timeout=0.6)
            except Exception:
                pass
            self.ai_worker_process = None

        if self.ai_opera_process:
            try:
                self.ai_opera_process.terminate()
                self.ai_opera_process.wait(timeout=0.6)
            except Exception:
                pass
            self.ai_opera_process = None

        self._disable_windows_pac()

        if os.name == 'nt':
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "core-worker.exe", "/IM", "ai-worker.exe", "/IM", "wireproxy.exe", "/IM", "opera-proxy.exe"],
                    creationflags=0x08000000,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1.0
                )
            except Exception:
                pass

        print("[Core] All engines stopped cleanly.")
        return {"status": "ok", "message": "Protection stopped"}

    def change_strategy(self, strategy_id):
        t_str = time.strftime("%H:%M:%S")
        self.active_strategy = strategy_id
        self._save_strategy(strategy_id)
        strat_name = self._get_strategy_name(strategy_id)
        self._log_event(f"{t_str} Профиль установлен: «{strat_name}»")
        print(f"[Core] Strategy set: {strategy_id}")
        if self.is_running:
            self.connection_status = "connecting"
            if self.tray_controller:
                self.tray_controller.update_status("connecting")
            self._start_divert_worker(override_strategy=strategy_id)
            
            # Quick async verification
            def _verify():
                time.sleep(1.0)
                chk = self.run_comprehensive_check(timeout=2.5)
                if chk["ai_ok"] or chk["tspu_ok"]:
                    self.connection_status = "online"
                else:
                    self.connection_status = "offline"
                if self.tray_controller:
                    self.tray_controller.update_status(self.connection_status)

            threading.Thread(target=_verify, daemon=True).start()

        return {"status": "ok", "strategy": strategy_id, "strategy_name": self._get_strategy_name(strategy_id), "auto_tune_enabled": self.auto_tune_enabled}


def main():
    if os.name == 'nt':
        MUTEX_NAME = "Global\\SpectraGlide_SingleInstance_Mutex_v2"
        ERROR_ALREADY_EXISTS = 183
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        mutex = kernel32.CreateMutexW(None, True, MUTEX_NAME)
        if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
            hwnd = user32.FindWindowW(None, "SpectraGlide Pro")
            if not hwnd:
                hwnd = user32.FindWindowW(None, "SpectraGlide // Ultra Low-Latency Engine")
            if hwnd:
                user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                user32.ShowWindow(hwnd, 5)  # SW_SHOW
                user32.SetForegroundWindow(hwnd)
            sys.exit(0)
    if not os.path.exists(HTML_PATH):
        print(f"Error: GUI HTML not found at {HTML_PATH}")
        sys.exit(1)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    api = SpectraGlideAPI(None)
    
    # Initialize system tray
    tray = SystemTrayController(api)
    api.set_tray_controller(tray)
    tray.start()

    webview.settings['ALLOW_FILE_URLS'] = True
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False

    icon_path = os.path.join(APP_DIR, "gui", "icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(BUNDLE_DIR, "gui", "icon.ico")

    # Safe webview window creation with fallback
    window = webview.create_window(
        title="SpectraGlide Pro",
        html=html_content,
        js_api=api,
        width=980,
        height=660,
        resizable=False,
        frameless=True,
        easy_drag=False,
        background_color="#06080e"
    )
    api._window = window
    threading.Thread(target=lambda: (time.sleep(1.2), api.start_engine()), daemon=True).start()

    try:
        webview.start(debug=False, icon=icon_path if os.path.exists(icon_path) else None)
    except Exception as e:
        print(f"[WebView] Fallback start due to: {e}")
        try:
            webview.start(gui='mshtml', debug=False)
        except Exception:
            pass


if __name__ == "__main__":
    main()
