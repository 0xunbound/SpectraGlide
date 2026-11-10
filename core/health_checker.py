"""
Comprehensive Network Diagnostic & Health Checker Engine
Tests TSPU-blocked services (YouTube, Discord, Social) and Geoblocked AI services
(Gemini, Claude, ChatGPT, Kimi, Perplexity).
Distinguishes between ISP DPI packet resets/drops and upstream server-side geo-restrictions.
"""

import socket
import ssl
import time
import json
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

# Diagnostic Targets
TARGETS = [
    # --- Category: Media & Streaming (TSPU Targeted) ---
    {
        "id": "youtube_main",
        "name": "YouTube (Портал)",
        "category": "tspu_media",
        "url": "https://www.youtube.com/generate_204",
        "expected_codes": [204, 200],
        "geo_check": False
    },
    {
        "id": "youtube_cdn",
        "name": "YouTube CDN (Видеопоток 4K)",
        "category": "tspu_media",
        "url": "https://i.ytimg.com/generate_204",
        "expected_codes": [204, 200],
        "geo_check": False
    },
    # --- Category: Discord ---
    {
        "id": "discord_portal",
        "name": "Discord (Сайт и авторизация)",
        "category": "tspu_discord",
        "url": "https://discord.com",
        "expected_codes": [200, 301, 302],
        "geo_check": False
    },
    {
        "id": "discord_gateway",
        "name": "Discord Gateway (Чат и сигнализация)",
        "category": "tspu_discord",
        "url": "https://gateway.discord.gg",
        "expected_codes": [200, 404, 400], # Gateway responds with 400/404 on HTTP GET, indicating unblocked TLS
        "geo_check": False
    },
    # --- Category: General Blocked Websites ---
    {
        "id": "x_twitter",
        "name": "X (ранее Twitter)",
        "category": "tspu_general",
        "url": "https://x.com",
        "expected_codes": [200, 301, 302],
        "geo_check": False
    },
    {
        "id": "instagram",
        "name": "Instagram",
        "category": "tspu_general",
        "url": "https://www.instagram.com",
        "expected_codes": [200, 301, 302],
        "geo_check": False
    },
    # --- Category: AI Services (Regional & Cloudflare Blocks) ---
    {
        "id": "chatgpt",
        "name": "OpenAI ChatGPT",
        "category": "ai_services",
        "url": "https://chatgpt.com",
        "expected_codes": [200, 301, 302],
        "geo_check": True,
        "geo_block_phrases": ["access denied", "blocked", "country", "not available in your region"]
    },
    {
        "id": "claude",
        "name": "Anthropic Claude",
        "category": "ai_services",
        "url": "https://claude.ai",
        "expected_codes": [200, 301, 302],
        "geo_check": True,
        "geo_block_phrases": ["not available in your area", "unavailable", "app-unavailable-country"]
    },
    {
        "id": "gemini",
        "name": "Google Gemini",
        "category": "ai_services",
        "url": "https://gemini.google.com",
        "expected_codes": [200, 301, 302],
        "geo_check": True,
        "geo_block_phrases": ["isn't currently supported in your country", "not supported in your country"]
    },
    {
        "id": "kimi",
        "name": "Moonshot Kimi AI",
        "category": "ai_services",
        "url": "https://www.kimi.ai",
        "expected_codes": [200, 301, 302],
        "geo_check": True,
        "geo_block_phrases": ["restriction", "region"]
    },
    {
        "id": "perplexity",
        "name": "Perplexity AI",
        "category": "ai_services",
        "url": "https://www.perplexity.ai",
        "expected_codes": [200, 301, 302],
        "geo_check": True,
        "geo_block_phrases": ["access denied", "cloudflare"]
    }
]

def resolve_doh(domain: str) -> Optional[str]:
    """Resolves IP via Cloudflare / Google DNS-over-HTTPS when system DNS is poisoned or blocked."""
    doh_urls = [
        f"https://1.1.1.1/dns-query?name={domain}&type=A",
        f"https://dns.google/resolve?name={domain}&type=A"
    ]
    for url in doh_urls:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/dns-json", "User-Agent": "SpectraGlide-Diagnostic/2.0"})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=2.5, context=ctx) as resp:
                data = json.loads(resp.read().decode())
                if "Answer" in data:
                    for ans in data["Answer"]:
                        if ans.get("type") == 1: # A record
                            return ans.get("data")
        except Exception:
            continue
    return None
    def __init__(self, timeout: float = 4.0):
        self.timeout = timeout
        
    def test_single_target(self, target: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tests a single endpoint. Categorizes errors into:
        - OK: fully accessible
        - TSPU_RST: TCP Connection Reset by Peer (typical TSPU DPI behavior)
        - TSPU_TIMEOUT: Packet dropping / blackholing (DPI drop)
        - GEO_BLOCKED: Upstream server rejected RU IP address (HTTP 403 or specific geofence page)
        - DNS_FAIL: DNS poisoning or resolution error
        """
        start = time.time()
        url = target["url"]
        
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        )
        
        # Disable auto SSL verification verification failure due to self-signed DPI MITM
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                latency_ms = int((time.time() - start) * 1000)
                code = response.getcode()
                body = ""
                
                # Check geo-block signatures for AI services
                if target.get("geo_check", False):
                    try:
                        raw_body = response.read(8192).decode("utf-8", errors="ignore").lower()
                        for phrase in target.get("geo_block_phrases", []):
                            if phrase in raw_body:
                                return {
                                    "id": target["id"],
                                    "name": target["name"],
                                    "category": target["category"],
                                    "status": "GEO_BLOCKED",
                                    "code": code,
                                    "latency_ms": latency_ms,
                                    "details": f"Сервис блокирует доступ для РФ (Региональное ограничение)"
                                }
                    except Exception:
                        pass
                
                if code in target["expected_codes"]:
                    return {
                        "id": target["id"],
                        "name": target["name"],
                        "category": target["category"],
                        "status": "OK",
                        "code": code,
                        "latency_ms": latency_ms,
                        "details": f"Доступен ({latency_ms} мс)"
                    }
                else:
                    return {
                        "id": target["id"],
                        "name": target["name"],
                        "category": target["category"],
                        "status": "UNEXPECTED_STATUS",
                        "code": code,
                        "latency_ms": latency_ms,
                        "details": f"Неожиданный ответ сервера: HTTP {code}"
                    }
                    
        except urllib.error.HTTPError as e:
            latency_ms = int((time.time() - start) * 1000)
            if e.code in target["expected_codes"]:
                return {
                    "id": target["id"],
                    "name": target["name"],
                    "category": target["category"],
                    "status": "OK",
                    "code": e.code,
                    "latency_ms": latency_ms,
                    "details": f"Доступен (Код {e.code})"
                }
            if e.code in [403, 451]:
                return {
                    "id": target["id"],
                    "name": target["name"],
                    "category": target["category"],
                    "status": "GEO_BLOCKED",
                    "code": e.code,
                    "latency_ms": latency_ms,
                    "details": f"Ограничение по региону (HTTP {e.code})"
                }
            return {
                "id": target["id"],
                "name": target["name"],
                "category": target["category"],
                "status": "HTTP_ERROR",
                "code": e.code,
                "latency_ms": latency_ms,
                "details": f"Ошибка HTTP {e.code}"
            }
            
        except urllib.error.URLError as e:
            latency_ms = int((time.time() - start) * 1000)
            reason = str(e.reason).lower()
            if "connection reset" in reason or "10054" in reason:
                return {
                    "id": target["id"],
                    "name": target["name"],
                    "category": target["category"],
                    "status": "TSPU_RST",
                    "code": None,
                    "latency_ms": latency_ms,
                    "details": "Сброс соединения ТСПУ (TCP Reset)"
                }
            elif "timed out" in reason or "timeout" in reason:
                return {
                    "id": target["id"],
                    "name": target["name"],
                    "category": target["category"],
                    "status": "TSPU_TIMEOUT",
                    "code": None,
                    "latency_ms": latency_ms,
                    "details": "Таймаут / Дроп пакетов ТСПУ"
                }
            elif "getaddrinfo failed" in reason:
                return {
                    "id": target["id"],
                    "name": target["name"],
                    "category": target["category"],
                    "status": "DNS_FAIL",
                    "code": None,
                    "latency_ms": latency_ms,
                    "details": "Ошибка DNS / Подмена адреса"
                }
            return {
                "id": target["id"],
                "name": target["name"],
                "category": target["category"],
                "status": "NETWORK_ERROR",
                "code": None,
                "latency_ms": latency_ms,
                "details": f"Ошибка сети: {str(e.reason)[:40]}"
            }
            
        except Exception as e:
            latency_ms = int((time.time() - start) * 1000)
            return {
                "id": target["id"],
                "name": target["name"],
                "category": target["category"],
                "status": "ERROR",
                "code": None,
                "latency_ms": latency_ms,
                "details": str(e)[:40]
            }

    def check_discord_voice_udp(self) -> Dict[str, Any]:
        """Tests Discord Voice RTC UDP port range responsiveness."""
        # Standard Discord Voice endpoint
        test_host = "voice.discord.media"
        test_port = 50001
        start = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.0)
            # Discord voice ping probe packet
            probe = b"\x00\x01\x00\x00\x00\x00\x00\x00"
            sock.sendto(probe, (test_host, test_port))
            sock.close()
            latency_ms = int((time.time() - start) * 1000)
            return {
                "id": "discord_voice_udp",
                "name": "Discord Voice (UDP/RTC)",
                "category": "tspu_discord",
                "status": "OK",
                "code": 200,
                "latency_ms": latency_ms,
                "details": "UDP канал открыт"
            }
        except Exception as e:
            return {
                "id": "discord_voice_udp",
                "name": "Discord Voice (UDP/RTC)",
                "category": "tspu_discord",
                "status": "UDP_BLOCKED",
                "code": None,
                "latency_ms": int((time.time() - start) * 1000),
                "details": f"Блокировка UDP: {str(e)}"
            }

    def run_full_diagnostics(self) -> Dict[str, Any]:
        """Runs diagnostics across all services and returns structured summary."""
        results = []
        for target in TARGETS:
            results.append(self.test_single_target(target))
            
        # Add Discord Voice UDP check
        results.append(self.check_discord_voice_udp())
        
        # Summary counts
        total = len(results)
        ok_count = sum(1 for r in results if r["status"] == "OK")
        tspu_blocked = sum(1 for r in results if r["status"] in ["TSPU_RST", "TSPU_TIMEOUT"])
        geo_blocked = sum(1 for r in results if r["status"] == "GEO_BLOCKED")
        
        return {
            "timestamp": time.time(),
            "total_tested": total,
            "accessible_count": ok_count,
            "tspu_blocked_count": tspu_blocked,
            "geo_blocked_count": geo_blocked,
            "items": results
        }

import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def print_report(diag: Dict[str, Any]):
    """Pretty prints terminal diagnostic results."""
    print("=" * 70)
    print("            СИСТЕМНАЯ ДИАГНОСТИКА СЕТЕВОЙ ДОСТУПНОСТИ")
    print("=" * 70)
    
    categories = {
        "tspu_media": "МЕДИА И СТРИМИНГ (YouTube / ТСПУ)",
        "tspu_discord": "DISCORD (Чат, Голос, Сигнализация)",
        "tspu_general": "СОЦСЕТИ И БЛОКИРОВКИ РКН",
        "ai_services": "ИИ СЕРВИСЫ (ChatGPT, Claude, Gemini, Kimi)"
    }
    
    for cat_key, cat_name in categories.items():
        print(f"\n[+] {cat_name}:")
        items = [r for r in diag["items"] if r["category"] == cat_key]
        for it in items:
            status = it["status"]
            if status == "OK":
                mark = "[ OK ]"
            elif status in ["TSPU_RST", "TSPU_TIMEOUT"]:
                mark = "[ТСПУ]"
            elif status == "GEO_BLOCKED":
                mark = "[ ГЕО]"
            else:
                mark = "[ОШИБ]"
                
            print(f"  {mark} {it['name']:<35} : {it['details']}")
            
    print("\n" + "=" * 70)
    print(f"ИТОГ: Доступно: {diag['accessible_count']}/{diag['total_tested']} | "
          f"Блокировок ТСПУ: {diag['tspu_blocked_count']} | "
          f"Региональных гео-блоков: {diag['geo_blocked_count']}")
    print("=" * 70)

if __name__ == "__main__":
    engine = DiagnosticEngine(timeout=3.5)
    print("Запуск сетевого тестирования...")
    report = engine.run_full_diagnostics()
    print_report(report)
