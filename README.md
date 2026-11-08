# ⚡ SpectraGlide // Ultra Low-Latency Network Engine

> Lightweight Windows network accelerator engineered to eliminate packet jitter, stabilize Discord WebRTC voice channels, and remove 4K/8K media stream buffering bottlenecks.

![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-00f076?style=flat-square&logo=windows)
![Architecture](https://img.shields.io/badge/Arch-x64-00f2fe?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-white?style=flat-square)

---

### 💡 Why SpectraGlide?

Many residential ISPs and regional backbone hops suffer from queue degradation and aggressive bufferbloat. This causes annoying robotic voice cutouts in Discord, latency spikes in competitive games, and constant stuttering when trying to watch 1440p/4K streams.

Standard VPNs often make things worse by routing *all* your bandwidth through bloated third-party servers, increasing ping and slowing down your connection.

**SpectraGlide takes a different approach:**
It operates locally at the Windows kernel packet filter layer combined with an intelligent local relay:
1. **Equalizes TCP/UDP packet timing:** Prioritizes voice and real-time WebRTC packets for crystal-clear audio.
2. **Normalizes stream packet fragmentation:** Smooths out TLS/QUIC packet bursts so high-resolution video streams don't choke on provider buffers.
3. **Adaptive Route Self-Healing:** Periodically runs lightweight, passive health checks against global cloud backbones and automatically adapts the optimization profile without interrupting active sessions.

---

### ✨ Features

- **Zero-Configuration:** Launch the app, hit "START ACCELERATION", and you're good to go.
- **Autonomous Tuning:** Automatically detects connection degradation and hot-switches packet shaping profiles under the hood.
- **Built-in Live Sonar:** Real-time ping gauge showing true round-trip response times to key worldwide backbones.
- **Ultra-Responsive Dark UI:** Hardware-accelerated WebView2 frontend with an animated waveform visualizer and glassmorphic aesthetic.
- **100% Portable:** Single self-contained package. No Python installation, node.js, or runtime runtimes required.

---

### 🚀 Quick Start

1. Head over to **[Releases](../../releases)** and grab the latest `SpectraGlide_v2.0.zip`.
2. Extract the archive anywhere you like (e.g., your Desktop or `C:\Program Files`).
3. Run `SpectraGlide.exe` as Administrator *(required to attach the local Windows network packet filtering driver)*.
4. Click **«START ACCELERATION»**.

> **Pro Tip:** The default "Balanced" preset is tuned for 99% of daily usage. If you're hopping into competitive gaming or voice-heavy sessions, switch over to the *Discord Voice Ultra* profile.

---

### 🛠 Architecture Overview

- **Core Packet Shaper:** Low-level Windows packet filter that normalizes transport-layer stream frames and prevents ISP transit bottlenecking.
- **Smart Relay Hub:** Internal high-speed PAC router that cleanly dispatches cloud compute, AI, and API endpoints through optimal routing paths.
- **Lightweight Shell:** Clean Win32 shell paired with modern EdgeChromium WebView2 — zero Electron memory bloat.

---

### ❓ FAQ

**Q: Does this throttle my download speeds or torrents?**  
A: No. SpectraGlide only normalizes handshake metadata and media stream frames. Your high-bandwidth traffic (Steam downloads, file transfers, torrents) continues flowing directly at full ISP wire speed.

**Q: Do I need an external VPN account?**  
A: No. Everything runs completely locally on your machine with zero external subscriptions.

**Q: How do I completely uninstall / revert changes?**  
A: Just click "STOP" in the app or close the window. The packet driver unhooks cleanly from memory and all Windows network settings instantly return to their defaults.

---

### 📄 License
Released under the [MIT License](LICENSE).
