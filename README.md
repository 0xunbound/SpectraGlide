# SpectraGlide

> **Высокопроизводительный нативный оптимизатор сети Windows и QoS-акселератор для потокового видео 4K/8K, ультра-низкой задержки Discord VoIP и снятия региональных ограничений с ChatGPT, Claude и других мировых сервисов.**  
> *High-performance native Windows network optimizer and hardware-accelerated QoS utility for 4K/8K streaming, ultra-low latency Discord VoIP, and unblocking ChatGPT, Claude, and global services.*

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-blue.svg)](https://github.com/0xunbound/SpectraGlide)
[![Release](https://img.shields.io/badge/Release-v2.0-green.svg)](https://github.com/0xunbound/SpectraGlide/releases)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🌐 Выберите язык / Select Language
* [Русский](#русский)
* [English](#english)

---

<a name="русский"></a>
## 🇷🇺 Русский

**SpectraGlide** — это полностью автономный сетевой ускоритель для Windows, объединяющий управление пакетами на уровне ядра (WinDivert) и интеллектуальный двухуровневый шлюз маршрутизации для доступа к международным облачным сервисам и нейросетям без замедления остального трафика.

> 💡 **Примечание:** Данная версия оптимизирована для ChatGPT, Claude, Copilot, Discord, YouTube и заблокированных ресурсов (Instagram, RuTracker и др.). Если вам требуется поддержка Google Gemini с выделенным европейским шлюзом, используйте сборку `SpectraGlide-Gemini`.

### 🌟 Ключевые возможности

* **Управление в один клик (Zero-Configuration)**  
  Единственная кнопка «УСКОРИТЬ СЕТЬ». Никаких сложных режимов, переключателей и ручной настройки конфигураций.
* **Аппаратный QoS для YouTube 4K/8K и Twitch**  
  Оптимизация пакетов на уровне ядра Windows устраняет искусственное замедление (throttling) со стороны провайдеров. Видео воспроизводится в 4K 60fps без зависаний и задержек.
* **Ультра-низкий джиттер для Discord и WebRTC**  
  Пакетная приоритезация UDP-трафика для Discord Voice, игр и голосовых конференций. Предотвращает пропадание звука («кваканье») и разрывы соединения.
* **Двухуровневый стелс-шлюз для AI (ChatGPT, Claude, Copilot)**  
  Полный и бесперебойный доступ к мировым нейросетям без ошибок «App unavailable in your region»:
  * **Tier 1 (Транспорт):** Пользовательский WireGuard (WARP с обфускацией Amnezia `H1/H2`) преодолевает любые блокировки и ТСПУ провайдеров на порту `127.0.0.1:1370`.
  * **Tier 2 (Выход и маскировка):** Чистый IP-выход через прокси (`127.0.0.1:1371`), исключающий передачу заголовков `CF-Connecting-IP`. Cloudflare и AI-сервисы видят белый доверенный IP без ограничений.
* **Обход блокировок популярных ресурсов (Instagram, RuTracker, Notion и др.)**  
  Интеллектуальный PAC-маршрутизатор направляет заблокированные сайты через защищённый тоннель, оставляя весь остальной российский трафик нетронутым.
* **100% безопасность и невмешательство в систему**  
  SpectraGlide **не меняет** DNS-серверы сетевых карт через `netsh`, **не редактирует** файл `hosts` и не трогает локальные российские сервисы (банки, Госуслуги, VK работают напрямую на максимальной скорости). При выходе системный реестр полностью возвращается в исходное состояние.
* **Плавный интерфейс (90–144 FPS)**  
  Кастомный интерфейс на базе Microsoft WebView2 с аппаратным Win32-перетаскиванием окна, нулевой задержкой отклика и потреблением памяти менее 35 МБ.
* **Автономная самодиагностика**  
  Фоновый асинхронный монитор непрерывно замеряет отклик ключевых шлюзов с выводом реального пинга.

---

### 🚀 Быстрый старт

1. Скачайте архив релиза: [`SpectraGlide_v2.0.zip`](https://github.com/0xunbound/SpectraGlide/releases).
2. Распакуйте архив в любую удобную папку.
3. Запустите `SpectraGlide.exe` от имени **Администратора** (требуется для загрузки драйвера пакетного фильтра WinDivert).
4. Нажмите кнопку **«УСКОРИТЬ СЕТЬ»** — система мгновенно поднимет оптимизацию.

---

### 🏛 Архитектура решения

             [ Исходящий трафик Windows ]
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
[ Системный PAC-фильтр ]        [ WinDivert Kernel Filter ]
           │                               │
   (ChatGPT & Claude)             (YouTube 4K & Discord RTC)
           │                               │
           ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│ Tier 2: Exit Proxy  │         │ Пакетный десинхрони-│
│  (US/EU Чистый IP)  │         │ затор (Fake QUIC &  │
└──────────┬──────────┘         │ TCP Multi-Split)    │
           │                            │
           ▼                            │
┌─────────────────────┐                 │
│ Tier 1: WARP Tunnel │                 │
│ (Amnezia H1/H2 AWG) │                 │
└──────────┬──────────┘                 │
           │                            │
           └───────────────┬────────────┘
                           ▼
               [ Прямой свободный выход ]

               
---

<a name="english"></a>
## 🇬🇧 English

**SpectraGlide** is a fully autonomous Windows network accelerator combining kernel-level packet shaping (WinDivert) with a smart two-tier relay gateway to provide seamless access to international cloud platforms and AI ecosystems without affecting local traffic.

> 💡 **Note:** This version is tailored for ChatGPT, Claude, Copilot, Discord, YouTube, and general unblocking. If you need specialized Google Gemini support with a dedicated European gateway, use the `SpectraGlide-Gemini` edition.

### 🌟 Key Features

* **Zero-Configuration Autonomous Operation**  
  Single-button execution («BOOST NETWORK»). No confusing modes, manual configs, or technical hurdles.
* **4K/8K Video Streaming Acceleration**  
  Kernel-level packet desynchronization engineered for high-bitrate video streams (YouTube, Twitch). Eliminates ISP throttling and artificial buffering.
* **Ultra-Low Latency RTC & Voice Engine**  
  Prioritized UDP packet flow for Discord Voice, WebRTC, and competitive gaming. Eliminates robotic voice artifacts and jitter.
* **Two-Tier Stealth AI Gateway (ChatGPT, Claude, Copilot)**  
  Uninterrupted access to modern AI platforms, avoiding "App unavailable in your region" errors:
  * **Tier 1 (Transport):** Userspace WireGuard (WARP with Amnezia obfuscation `H1/H2`) bypasses deep packet inspection (DPI/TSPU) over `127.0.0.1:1370`.
  * **Tier 2 (Clean Exit & Header Scrubbing):** Clean egress via Proxy (`127.0.0.1:1371`), completely stripping `CF-Connecting-IP` headers so Cloudflare and AI providers recognize it as a legitimate connection.
* **Smart Domain Routing (Instagram, RuTracker, Notion, etc.)**  
  System PAC routing automatically handles restricted resources through the stealth tunnel while keeping local domestic traffic 100% direct.
* **100% Non-Intrusive & Clean**  
  SpectraGlide **does not modify** network adapter DNS servers via `netsh`, **does not alter** the `hosts` file, and routes domestic traffic directly with zero latency. All registry changes are cleanly reverted on exit.
* **Silky-Smooth Frameless UI (90–144 FPS)**  
  Modern Win32 frameless interface powered by Microsoft WebView2, featuring responsive hardware window dragging and minimal RAM footprint (< 35 MB).
* **Self-Healing Background Monitor**  
  Asynchronous health engine actively probes service endpoints and updates real-time latency indicators.

---

### 🚀 Quick Start

1. Download the latest release: [`SpectraGlide_v2.0.zip`](https://github.com/0xunbound/SpectraGlide/releases).
2. Extract the archive into any folder.
3. Run `SpectraGlide.exe` as **Administrator** (required for the WinDivert kernel-level driver).
4. Click **«УСКОРИТЬ СЕТЬ» (BOOST NETWORK)** — optimization is engaged in less than a second.

---

## 🛠 Сборка из исходников / Build from Source

### Требования / Requirements:
- Windows 10 / 11 (x64)
- Python 3.10+
- PyInstaller (`pip install pyinstaller`)

```bash
git clone https://github.com/0xunbound/SpectraGlide.git
cd SpectraGlide
pip install -r requirements.txt
python -m PyInstaller --clean SpectraGlide.spec
