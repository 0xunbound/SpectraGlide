"""
Strategy Converter & Optimizer
Converts legacy .bat configurations into a structured, optimized JSON profiles database.
Strips all legacy project names, normalizes parameters, and optimizes desync techniques.
"""

import os
import re
import json
import argparse
from typing import Dict, List, Any

# Forbidden / legacy strings to strip completely from all configs, names, and logs
SCRUB_PATTERNS = [
    r"(?i)zapret",
    r"(?i)flowseal",
    r"(?i)bol[-_]?van",
    r"(?i)nova",
    r"(?i)confeden",
    r"(?i)goodbyedpi",
    r"(?i)valdikss",
    r"(?i)winws"
]

def scrub_text(text: str, replacement: str = "core") -> str:
    """Removes all legacy project mentions."""
    res = text
    for pattern in SCRUB_PATTERNS:
        res = re.sub(pattern, replacement, res)
    return res

def clean_command_line(cmd: str) -> List[str]:
    """Cleans a raw command line from batch scripts into an array of sanitized arguments."""
    # Remove executable name (e.g. winws.exe, start ..., %~dp0...)
    cmd = re.sub(r'^(?:start\s+""\s+)?(?:"[^"]*"|\S+)\s*', '', cmd.strip())
    # Remove comments and pauses
    cmd = re.sub(r'rem\s+.*$', '', cmd, flags=re.IGNORECASE)
    
    # Split into tokens preserving quotes
    tokens = []
    current = []
    in_quotes = False
    for char in cmd:
        if char == '"':
            in_quotes = not in_quotes
        elif char.isspace() and not in_quotes:
            if current:
                token = "".join(current).strip()
                if token and token != "^":
                    tokens.append(token)
                current = []
            continue
        elif char == '^':
            continue
        current.append(char)
        
    if current:
        token = "".join(current).strip()
        if token and token != "^":
            tokens.append(token)
            
    # Clean tokens from legacy path prefixes (%~dp0, etc.)
    cleaned = []
    for t in tokens:
        t = re.sub(r'%~dp0\w*\\?', '', t)
        t = re.sub(r'%BIN%\\?', '', t)
        t = scrub_text(t)
        if t:
            cleaned.append(t)
            
    return cleaned

def get_optimized_presets() -> List[Dict[str, Any]]:
    """
    Returns curated, battle-tested modern strategies optimized for Russian TSPU DPI (2025-2026).
    Combines Discord Voice UDP fixes, YouTube 4K TLS split/fake injection, and clean fallback modes.
    """
    return [
        {
            "id": "strategy_balanced_default",
            "name": "Сбалансированный (Рекомендуемый)",
            "description": "Универсальный профиль для YouTube 4K, Discord (чат и голос) и большинства заблокированных сайтов.",
            "recommended": True,
            "target_services": ["youtube", "discord_chat", "discord_voice", "general_web"],
            "requires_admin": True,
            "args": [
                "--wf-tcp=80,443",
                "--wf-udp=443,50000-65535",
                # Discord Voice / WebRTC UDP Fix
                "--filter-udp=50000-65535",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=4",
                "--dpi-desync-cutoff=d3",
                "--dpi-desync-any-protocol",
                "--new",
                # YouTube QUIC (HTTP/3) bypass
                "--filter-udp=443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                "--new",
                # TCP TLS Desync (YouTube, Discord Signaling, Web)
                "--filter-tcp=80,443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake,split2",
                "--dpi-desync-split-pos=1",
                "--dpi-desync-autottl=2",
                "--dpi-desync-fooling=md5sig",
                "--dpi-desync-repeats=2"
            ]
        },
        {
            "id": "strategy_discord_voice_priority",
            "name": "Discord Voice Ultra (Приоритет голосовых каналов)",
            "description": "Специализированная десинхронизация UDP-пакетов без потерь для серверов Discord RTC.",
            "recommended": False,
            "target_services": ["discord_voice", "discord_chat"],
            "requires_admin": True,
            "args": [
                "--wf-tcp=80,443",
                "--wf-udp=50000-65535",
                "--filter-udp=50000-65535",
                "--dpi-desync=fake",
                "--dpi-desync-any-protocol",
                "--dpi-desync-cutoff=d4",
                "--new",
                "--filter-tcp=80,443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake,split2",
                "--dpi-desync-split-pos=midsld",
                "--dpi-desync-autottl=2"
            ]
        },
        {
            "id": "strategy_youtube_seqovl",
            "name": "YouTube 4K Heavy (Sequence Overlap)",
            "description": "Метод наложения порядковых номеров TCP (seqovl) для провайдеров с агрессивным подавлением потокового видео.",
            "recommended": False,
            "target_services": ["youtube", "googlevideo"],
            "requires_admin": True,
            "args": [
                "--wf-tcp=80,443",
                "--wf-udp=443",
                "--filter-udp=443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake",
                "--new",
                "--filter-tcp=443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake,split2",
                "--dpi-desync-split-seqovl=336",
                "--dpi-desync-split-pos=2",
                "--dpi-desync-fooling=badseq,md5sig",
                "--dpi-desync-autottl=2"
            ]
        },
        {
            "id": "strategy_deep_tspu_disorder",
            "name": "Глубокий обход ТСПУ (Disorder + Multidisorder)",
            "description": "Изменение порядка следования пакетов данных и контрольных сумм для обхода жестких фильтраций.",
            "recommended": False,
            "target_services": ["youtube", "discord_chat", "general_web"],
            "requires_admin": True,
            "args": [
                "--wf-tcp=80,443",
                "--wf-udp=443,50000-65535",
                "--filter-udp=50000-65535",
                "--dpi-desync=fake",
                "--dpi-desync-cutoff=d2",
                "--new",
                "--filter-tcp=80,443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=disorder2",
                "--dpi-desync-split-pos=1",
                "--dpi-desync-fooling=badsum"
            ]
        },
        {
            "id": "strategy_ai_and_geo_relay",
            "name": "Smart Proxy & AI Services (Двухуровневый режим)",
            "description": "Локальный обход ТСПУ для медиа + перенаправление геоблокировок (ChatGPT, Claude, Gemini, Kimi) через прокси/релей.",
            "recommended": False,
            "target_services": ["chatgpt", "claude", "gemini", "kimi", "youtube", "discord_chat"],
            "requires_admin": True,
            "routing_mode": "hybrid",
            "proxy_fallback": "127.0.0.1:10808",
            "args": [
                "--wf-tcp=80,443",
                "--wf-udp=443,50000-65535",
                "--filter-udp=50000-65535",
                "--dpi-desync=fake",
                "--new",
                "--filter-tcp=80,443",
                "--hostlist=rules-core.txt",
                "--dpi-desync=fake,split2",
                "--dpi-desync-split-pos=1",
                "--dpi-desync-autottl=2"
            ]
        }
    ]

def convert_bat_file(bat_path: str) -> Dict[str, Any]:
    """Parses a single .bat file and returns an extracted strategy dict."""
    with open(bat_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    base_name = os.path.splitext(os.path.basename(bat_path))[0]
    clean_name = scrub_text(base_name, replacement="Mode").replace("_", " ").title()
    
    # Extract line running the binary
    engine_line = ""
    for line in content.splitlines():
        line_clean = line.strip()
        if any(bin_name in line_clean.lower() for bin_name in ["winws", "core-worker", "worker"]):
            engine_line = line_clean
            break
            
    args = clean_command_line(engine_line) if engine_line else []
    
    return {
        "id": f"imported_{base_name.lower()}",
        "name": clean_name,
        "description": f"Импортированная конфигурация из {base_name}",
        "recommended": False,
        "target_services": ["general_web"],
        "requires_admin": True,
        "args": args
    }

def generate_default_hostlists(output_dir: str):
    """Generates sanitized hostlists for TSPU blocked services and AI services."""
    core_hosts = [
        # YouTube & Google CDN
        "youtube.com",
        "www.youtube.com",
        "googlevideo.com",
        "ytimg.com",
        "ggpht.com",
        "gvt1.com",
        "youtubei.googleapis.com",
        "yt3.ggpht.com",
        "wide-youtube.l.google.com",
        
        # Discord
        "discord.com",
        "www.discord.com",
        "discordapp.com",
        "discord.gg",
        "discord.media",
        "discordapp.net",
        "gateway.discord.gg",
        "cdn.discordapp.com",
        
        # Blocked Social / Media
        "instagram.com",
        "cdninstagram.com",
        "facebook.com",
        "fbcdn.net",
        "twitter.com",
        "x.com",
        "twimg.com",
        "t.co",
        "notion.so",
        
        # Generic & Dev
        "rutracker.org",
        "ntc.party",
        "medium.com"
    ]
    
    ai_hosts = [
        # OpenAI / ChatGPT
        "chatgpt.com",
        "openai.com",
        "api.openai.com",
        "auth0.openai.com",
        "challenges.cloudflare.com",
        "cdn.oaistatic.com",
        
        # Anthropic Claude
        "claude.ai",
        "anthropic.com",
        "api.anthropic.com",
        
        # Google Gemini
        "gemini.google.com",
        "generativelanguage.googleapis.com",
        "alkalimakersuite-pa.clients6.google.com",
        
        # Moonshot Kimi
        "kimi.ai",
        "moonshot.cn",
        "kimi.moonshot.cn",
        
        # Perplexity & Copilot
        "perplexity.ai",
        "copilot.microsoft.com"
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    core_path = os.path.join(output_dir, "rules-core.txt")
    with open(core_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(core_hosts)) + "\n")
        
    ai_path = os.path.join(output_dir, "rules-ai.txt")
    with open(ai_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(ai_hosts)) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Strategy Converter and Optimizer")
    parser.add_argument("--input-bat-dir", help="Directory with legacy .bat scripts to import (optional)")
    parser.add_argument("--output-json", default="config/strategies.json", help="Path to output strategies.json")
    parser.add_argument("--output-config-dir", default="config", help="Path to config directory for hostlists")
    args = parser.parse_args()
    
    strategies = get_optimized_presets()
    
    if args.input_bat_dir and os.path.exists(args.input_bat_dir):
        for root, _, files in os.walk(args.input_bat_dir):
            for file in files:
                if file.lower().endswith(".bat") and not any(k in file.lower() for k in ["service_install", "service_remove", "blockcheck"]):
                    bat_path = os.path.join(root, file)
                    converted = convert_bat_file(bat_path)
                    if converted["args"]:
                        strategies.append(converted)
                        
    os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump({"version": "2.0.0", "strategies": strategies}, f, indent=2, ensure_ascii=False)
        
    generate_default_hostlists(args.output_config_dir)
    print(f"Successfully generated {len(strategies)} optimized strategies in {args.output_json}")
    print(f"Rules generated in {args.output_config_dir}/rules-core.txt and rules-ai.txt")

if __name__ == "__main__":
    main()
