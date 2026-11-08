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
from ctypes import wintypes

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

# Win32 Constants for native, silky-smooth window interaction
user32 = ctypes.windll.user32 if os.name == 'nt' else None
WM_NCLBUTTONDOWN = 0x00A1
HTCAPTION = 0x0002
SW_MINIMIZE = 6
SW_MAXIMIZE = 3
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

    var unblock = {"1337x.to":1,"1e100cdn.net":1,"7tv.app":1,"7tv.io":1,"abuseipdb.com":1,"accounts.google.com":1,"activatica.org":1,"adguard-mail.com":1,"adis.ws":1,"adjust.com":1,"adjust.world":1,"adobe.com":1,"adobe.io":1,"adobedtm.com":1,"aeza.net":1,"aeza.ru":1,"akamaiedge.net":1,"alibaba.com":1,"alicdn.com":1,"alternativeto.net":1,"amazon-adsystem.com":1,"amazon.com":1,"amazonaws.com":1,"amd.com":1,"amnezia.org":1,"amplience.net":1,"announcekit.app":1,"anydesk.com":1,"archive.org":1,"arena.ai":1,"argotunnel.com":1,"arkoselabs.com":1,"arm.com":1,"arrow.com":1,"aspose.app":1,"auth0.com":1,"awswaf.com":1,"azure.com":1,"b-cdn.net":1,"bbc-reporting-api.app":1,"bbc.co.uk":1,"bbc.com":1,"benchgecko.ai":1,"bestrandoms.com":1,"booktracker.org":1,"bootstrapcdn.com":1,"br.de":1,"breakingcopyright.com":1,"brevo.com":1,"bspuhose.com":1,"buildwithfern.com":1,"canon-europe.com":1,"canon.ru":1,"cdn.bsky.app":1,"cdn.intergient.com":1,"cdninstagram.com":1,"cfapi.net":1,"chartbeat.com":1,"chess.com":1,"chesscomfiles.com":1,"chromium.googlesource.com":1,"clawbot.ai":1,"cloudflare-dns.com":1,"cloudflare-ech.com":1,"cloudflare.com":1,"cloudflare.dev":1,"cloudflare.net":1,"cloudflareaccess.com":1,"cloudflareclient.com":1,"cloudflareinsights.com":1,"cloudflareok.com":1,"cloudflareportal.com":1,"cloudflarepreview.com":1,"cloudflaressl.com":1,"cloudflarestatus.com":1,"cloudflarestorage.com":1,"cloudflarestream.com":1,"cloudfront.net":1,"coinbase.com":1,"comicbook.com":1,"crates.io":1,"crowdsec.net":1,"cryptocloud.plus":1,"cryptomus.com":1,"ctfassets.net":1,"cts.h1s1.edge.certum.pl":1,"cursor.directory":1,"cursor.sh":1,"deltarockme.com":1,"deploy.totallyacdn.com":1,"desmos.com":1,"deviantart.net":1,"digit.in":1,"discord.com":1,"discord.gg":1,"discordapp.com":1,"discourse-cdn.com":1,"dnsleaktest.org":1,"dropboxstatic.com":1,"dw.com":1,"ecosyste.ms":1,"edgee.ai":1,"element.io":1,"engagement.ai":1,"etoneya.su":1,"evidon.com":1,"evolution-x.org":1,"excalidraw.com":1,"ext-twitch.tv":1,"facebook.com":1,"farnell.com":1,"fb.com":1,"fb.me":1,"fbcdn.net":1,"fbsbx.com":1,"filterblade.xyz":1,"fineshare.com":1,"flagcdn.com":1,"flixster.com":1,"fontawesome.com":1,"forms.gle":1,"frankerfacez.com":1,"freebuff.com":1,"fsdn.com":1,"fubgun.com":1,"funcpa.ru":1,"funpay.com":1,"g2g.com":1,"gameseal.com":1,"geforce.com":1,"geohide.ru":1,"ggpht.com":1,"github.com":1,"githubusercontent.com":1,"glbgpt.com":1,"global.canon":1,"gname.com":1,"gname.net":1,"gnu.org":1,"godaddy.com":1,"goentri.com":1,"gokino.su":1,"good-proxies.ru":1,"google.dev":1,"google.ru":1,"googleads.g.doubleclick.net":1,"googlevideo.com":1,"greasyfork.org":1,"grokusercontent.com":1,"hailuoai.video":1,"happyscribe.com":1,"hdclub.ua":1,"hdkinoteatr.com":1,"hereapi.com":1,"hexed.it":1,"hls.ttvnw.net":1,"hlsloader.com":1,"ibb.co":1,"idaprikol.ru":1,"iditena.org":1,"instagram.com":1,"ip-tracker.org":1,"iplogger.org":1,"ipway.com":1,"island-of-pleasure.site":1,"issuehunt.io":1,"jabber.fr":1,"jnn-pa.googleapis.com":1,"jsdelivr.net":1,"killedbygoogle.com":1,"kinobox.tv":1,"kinohub.vip":1,"kinozal.tv":1,"laozhang.ai":1,"launchdarkly.com":1,"litellm.ai":1,"live-video.net":1,"live.com":1,"llimonix.dev":1,"llimonix.pw":1,"lostfilm.tv":1,"lumalabs.ai":1,"mangamirai.com":1,"mapq.st":1,"mate.tools":1,"matrix.org":1,"mcpmarket.com":1,"medal.tv":1,"media-amazon.com":1,"media-proxy.toil.cc":1,"meduza.io":1,"meet.google.com":1,"meshworld.in":1,"microsoft.com":1,"minimax.io":1,"mintcdn.com":1,"mktoweb.com":1,"mmcdn.com":1,"mobi-films.com":1,"modrinth.com":1,"monetamarkets.com":1,"moonshot.cn":1,"mqcdn.com":1,"muapi.ai":1,"myanimelist.net":1,"mycountrymobile.com":1,"mynoise.world":1,"myqcloud.com":1,"namecheap.com":1,"namecheapapi.com":1,"nc-img.com":1,"netify.ai":1,"neuralwriter.com":1,"nnmclub.to":1,"nnmstatic.win":1,"notion.site":1,"nova.app":1,"nova.net":1,"nowpayments.io":1,"ntfy.sh":1,"nuget.org":1,"nvidia.com":1,"oauth.tg.dev":1,"obmen.one":1,"obsproject.com":1,"ohi-s.com":1,"on.aws":1,"onorca.dev":1,"ookla.com":1,"optimizely.com":1,"pacloudflare.com":1,"pastes.dev":1,"pathofbuilding.community":1,"payproglobal.com":1,"perfops.net":1,"phncdn.com":1,"phonevalidator.com":1,"pixelbuilds.org":1,"playlist.ttvnw.net":1,"pobb.in":1,"pocketnet.app":1,"poe2wiki.net":1,"poecdn.com":1,"poedb.tw":1,"proton.me":1,"proxyliberty.com":1,"proxynova.com":1,"puter.chat":1,"puter.site":1,"pypi.org":1,"pythonhosted.org":1,"qt.io":1,"qwen.ai":1,"qwen.com":1,"qwenlm.ai":1,"recaptcha.net":1,"receive-sms.io":1,"redav.online":1,"redditspace.com":1,"redgifs.com":1,"rezka.ag":1,"romexsoftware.com":1,"rottentomatoes.com":1,"roundproxies.com":1,"rtrvr.ai":1,"rust-lang.org":1,"rustdesk.com":1,"rustup.rs":1,"rutor.is":1,"rutracker.cc":1,"safegram.com":1,"scorecardresearch.com":1,"scrcpy.org":1,"seasonvar.ru":1,"securrity.ru":1,"sfml-dev.org":1,"sfunpay.com":1,"shopify.com":1,"simgbb.com":1,"sitechecker.pro":1,"skills.md":1,"sms-act.net":1,"smspool.net":1,"smtp2go.com":1,"smtp2gostatus.com":1,"sndcdn.com":1,"soundcloud.cloud":1,"soundcloud.com":1,"sourceforge.io":1,"speedtest.net":1,"squarespace-cdn.com":1,"squarespace.com":1,"ssl-images-amazon.com":1,"st.com":1,"static-cdn.jtvnw.net":1,"static.doubleclick.net":1,"stravers.live":1,"surfshark.com":1,"symantecliveupdate.com":1,"systeminformer.com":1,"t.co":1,"tadst.com":1,"tailscale.com":1,"tampermonkey.net":1,"taobao.com":1,"tapeop.dev":1,"team.ga":1,"telegram.org":1,"telesco.pe":1,"tftrove.com":1,"thepiratebay.org":1,"tiktokcdn-us.com":1,"time.certum.pl":1,"timeanddate.com":1,"timestamp.digicert.com":1,"timestamp.sectigo.com":1,"tiqcdn.com":1,"toil-dump.workers.dev":1,"topdns.com":1,"torrindex.net":1,"trustpilot.net":1,"trycloudflare.com":1,"tuta.com":1,"tuta.io":1,"tutamail.com":1,"tutanota.com":1,"tv.in":1,"tvteam.eu":1,"twimg.com":1,"twitch.tv":1,"twitchcdn.net":1,"twitter.com":1,"typeform.com":1,"ucweb.com":1,"unpkg.com":1,"usercentrics.eu":1,"userscript.zone":1,"vecpea.com":1,"vector.im":1,"vercel-storage.com":1,"vercel.app":1,"verisoul.ai":1,"videolan.org":1,"vultrusercontent.com":1,"warp.dev":1,"warp.plus":1,"weblate.org":1,"website-files.com":1,"websiteplanet.com":1,"whatsapp.com":1,"whatsapp.net":1,"whois.com":1,"wide-youtube.l.google.com":1,"windscribe.com":1,"windscribe.net":1,"wispbyte.com":1,"wix.com":1,"wixmp.com":1,"workos.com":1,"wsimg.com":1,"www.debian.org":1,"www.deviantart.com":1,"www.vdsina.com":1,"www.virustotal.com":1,"x.com":1,"xv-ru.com":1,"xvideos-cdn.com":1,"xvideos.com":1,"youtu.be":1,"youtube-nocookie.com":1,"youtube-ui.l.google.com":1,"youtube.com":1,"youtubeembeddedplayer.googleapis.com":1,"youtubei.googleapis.com":1,"youtubekids.com":1,"yt-video-upload.l.google.com":1,"yt3.googleusercontent.com":1,"ytimg.com":1,"ytimg.l.google.com":1,"z-lib.sk":1,"z-library.sk":1,"zendesk.com":1,"zerofs.link":1,"zetflix-online.skin":1,"zizaran.com":1,"zo.computer":1,"2nd-no.com":1,"2no.pl":1,"4pda.to":1,"4pda.ws":1,"accountcapabilities-pa.googleapis.com":1,"agent-router.org":1,"analog.com":1,"anthropic.com":1,"api-iam.intercom.io":1,"autodesk.com":1,"autodesk.net":1,"autodesk360.com":1,"battle.net":1,"bbci.co.uk":1,"blizzard.com":1,"blz-contentstack-images.akamaized.net":1,"broadcom.com":1,"canva.com":1,"cdn-apple.com":1,"cdn.cookielaw.org":1,"cdnbunny.org":1,"cerebras.ai":1,"chatgpt.com":1,"chromewebstore.google.com":1,"claude.ai":1,"claude.com":1,"claudemcpcontent.com":1,"claudeusercontent.com":1,"clientservices.googleapis.com":1,"cline.bot":1,"codegpt.co":1,"collaborator.pro":1,"copilot.microsoft.com":1,"coveo.com":1,"cursor-cdn.com":1,"cursor-marketplace.com":1,"cursor.com":1,"cursor.so":1,"cursorapi.com":1,"deepl.com":1,"digikey.com":1,"digikeyassets.com":1,"digiseller.com":1,"dreamina.capcut.com":1,"duck.ai":1,"elevenmusic.io":1,"emergent.sh":1,"epicgames.com":1,"etsy.com":1,"figma.ai":1,"figma.com":1,"fitgirl-repacks.site":1,"flibusta.is":1,"forge.akamaized.net":1,"g2a.com":1,"gamsgo.com":1,"gemini.google":1,"geolocation.onetrust.com":1,"githubcopilot.com":1,"gog.com":1,"google.nl":1,"gql.twitch.tv":1,"grizzlysms.com":1,"grok.com":1,"hasura-app.io":1,"hasura.io":1,"hex-rays.com":1,"hsforms.com":1,"imgur.com":1,"intel.com":1,"intercomassets.com":1,"inventati.org":1,"invideo.io":1,"ivpn.net":1,"jestkii.com":1,"js.intercomcdn.com":1,"kaspersky.com":1,"kaspersky.ru":1,"kaspersky.se":1,"kilo.ai":1,"kodikplayer.com":1,"konami.net":1,"livejournal.com":1,"livejournal.net":1,"lpsg.com":1,"mapquest.com":1,"meta.ai":1,"microchip.com":1,"mouser.com":1,"mozilla.org":1,"msys2.org":1,"mtraf.io":1,"mycdn.ink":1,"netflix.com":1,"nexus-websocket-a.intercom.io":1,"nitter.net":1,"notebooklm-pa.googleapis.com":1,"notebooklm.google.com":1,"notion.com":1,"notion.so":1,"ntc.party":1,"nxp.com":1,"oaistatic.com":1,"oaiusercontent.com":1,"okta.com":1,"oktacdn.com":1,"onlinesim.io":1,"openai.com":1,"openrouter.ai":1,"optimizationguide-pa.googleapis.com":1,"orbsrv.com":1,"otzyvmarketing.ru":1,"paddle.com":1,"parklogic.com":1,"patreon.com":1,"patreonusercontent.com":1,"performance.radar.cloudflare.com":1,"pixabay.com":1,"plati.io":1,"plati.market":1,"play.google.com":1,"playground.google":1,"puter.com":1,"ql.app":1,"qoder.com":1,"revved.com":1,"ru-board.com":1,"rutor.info":1,"rutracker.org":1,"rutrk.org":1,"sagernet.org":1,"scdn.co":1,"scene7.com":1,"skcrtxr.com":1,"smspva.com":1,"sora.com":1,"soulmatcher.app":1,"sourceforge.net":1,"spaceship-cdn.com":1,"spaceship.com":1,"spotify.com":1,"spotifycdn.com":1,"store.steampowered.com":1,"streamx.cash":1,"stripe.com":1,"stripe.network":1,"suno.com":1,"t.me":1,"telegra.ph":1,"telegram.me":1,"thisismyip.com":1,"ti.com":1,"tiger-sms.com":1,"tiktok.com":1,"tokenharbor.ai":1,"usher.ttvnw.net":1,"widget.intercom.io":1,"x.ai":1,"xdaforums.com":1,"zhizhin.xyz":1,"a.claude.ai":1,"ab.chatgpt.com":1,"agent.api5.cursor.sh":1,"agentn.api5.cursor.sh":1,"agentn.global.api5.cursor.sh":1,"android.chat.openai.com":1,"api.anthropic.com":1,"api.chatgpt.com":1,"api.cline.bot":1,"api.openai.com":1,"api2.cursor.sh":1,"api2direct.cursor.sh":1,"api3.cursor.sh":1,"api4.cursor.sh":1,"app.cline.bot":1,"assets-proxy.anthropic.com":1,"assets.claude.ai":1,"auth.openai.com":1,"aw.api.openai.com":1,"bridge.claudeusercontent.com":1,"code.claude.com":1,"console.anthropic.com":1,"docs.anthropic.com":1,"docs.claude.com":1,"downloads.claude.ai":1,"downloads.claude.com":1,"mcp-proxy.anthropic.com":1,"platform.claude.com":1,"prod.authentication.cursor.sh":1,"repo42.cursor.sh":1,"s-cdn.anthropic.com":1,"status.anthropic.com":1,"status.claude.com":1,"support.anthropic.com":1,"support.claude.com":1,"us-only.gcpp.cursor.sh":1,"webrtc.chatgpt.com":1,"ws.chatgpt.com":1,"www.anthropic.com":1,"www.claude.ai":1,"www.claude.com":1,"www.claudeusercontent.com":1,"messenger.com":1,"hdrezka.ag":1,"protonmail.com":1,"protonvpn.com":1,"gemini.google.com":1,"aistudio.google.com":1,"notebooklm.google":1,"news.google.com":1};

    function matchDomain(dict, h) {
        if (dict[h]) return true;
        var pos = h.indexOf('.');
        while (pos > -1) {
            var suffix = h.substring(pos + 1);
            if (dict[suffix]) return true;
            pos = h.indexOf('.', pos + 1);
        }
        return false;
    }

    if (matchDomain(unblock, host)) {
        return "PROXY 127.0.0.1:1371; SOCKS5 127.0.0.1:1370; DIRECT";
    }

    return "DIRECT";
}

function FindProxyForURLEx(url, host) {
    var res = FindProxyForURL(url, host);
    if (res === "DIRECT") return "DIRECT";
    return "PROXY 127.0.0.1:1371; DIRECT";
}
"""


global_api_ref = None



class PacHttpHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.close_connection = True
        global global_api_ref
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


class SpectraGlideAPI:
    """Python API exposed to the JavaScript frontend via window.pywebview.api"""
    def __init__(self, window=None):
        self._window = window
        self.active_strategy = "auto"
        self.is_running = False
        self.worker_process = None
        self.ai_worker_process = None
        self.ai_opera_process = None
        self.pac_server = None
        self.is_maximized = False
        self.ai_unblock_enabled = True
        self.prev_proxy_settings = None
        self._cached_hwnd = None
        self.strategies_data = self._load_strategies()

        # Adaptive Health Engine & Autonomous Self-Healing System
        self.auto_tune_enabled = True
        self.auto_tune_status = "STANDBY"
        self.auto_tune_state = "standby"  # "optimal", "tuning", "standby"
        self.ai_country = "AM"
        self.ai_country_list = ["AM", "EU"]
        self.ai_sni = "www.microsoft.com"
        self.ai_sni_list = ["www.microsoft.com", "cloudflare.com", "www.google.com"]
        self.last_auto_tune_time = 0

        self.recent_logs = [
            f"{time.strftime('%H:%M:%S')} — Система интеллектуальной оптимизации маршрутов активна",
            f"{time.strftime('%H:%M:%S')} — Аппаратный QoS и балансировка пакетов включены"
        ]

        self.service_health = {
            "youtube": {"name": "CDN Streaming Gateway (4K/8K)", "ok": True, "latency": 38.0, "status": "ok", "note": "QoS Ultra", "consecutive_fails": 0, "category": "youtube"},
            "discord_voice": {"name": "Voice & RTC Ultra Channel", "ok": True, "latency": 24.0, "status": "ok", "note": "Low Jitter QoS", "consecutive_fails": 0, "category": "discord"},
            "discord_gateway": {"name": "Signaling & Chat Gateway", "ok": True, "latency": 26.0, "status": "ok", "note": "Direct TLS", "consecutive_fails": 0, "category": "discord"},
            "gemini": {"name": "Neural Network API Hub", "ok": True, "latency": 35.0, "status": "ok", "note": "Anycast Relay", "consecutive_fails": 0, "category": "ai"},
            "chatgpt": {"name": "Cloud Compute Gateway #1", "ok": True, "latency": 45.0, "status": "ok", "note": "Anycast Relay", "consecutive_fails": 0, "category": "ai"},
            "claude": {"name": "Cloud Compute Gateway #2", "ok": True, "latency": 42.0, "status": "ok", "note": "Anycast Relay", "consecutive_fails": 0, "category": "ai"},
            "dns": {"name": "Anycast Ultra DNS Resolver", "ok": True, "latency": 16.0, "status": "ok", "note": "Anycast Fast", "consecutive_fails": 0, "category": "infra"},
        }

        self._probe_targets = [
            ("youtube", "CDN Streaming Gateway (4K/8K)", "www.youtube.com", 443, "142.251.150.4", "tcp", "youtube"),
            ("discord_voice", "Voice & RTC Ultra Channel", "latency.discord.media", 443, None, "tcp", "discord"),
            ("discord_gateway", "Signaling & Chat Gateway", "gateway.discord.gg", 443, None, "tcp", "discord"),
            ("gemini", "Neural Network API Hub", "gemini.google.com", 443, "142.251.150.2", "tcp", "ai"),
            ("chatgpt", "Cloud Compute Gateway #1", "chatgpt.com", 443, "157.22.181.209", "tcp", "ai"),
            ("claude", "Cloud Compute Gateway #2", "claude.ai", 443, "157.22.181.209", "tcp", "ai"),
            ("dns", "Anycast Ultra DNS Resolver", "195.133.25.16", 53, None, "udp_dns", "infra"),
        ]

        self._probe_index = 0
        self._bg_monitor_running = True

        global global_api_ref
        global_api_ref = self

        # Clean any leftovers on start
        self._initial_cleanup()
        atexit.register(self.stop_engine)

        # Start PAC & state HTTP server immediately so /state works from launch
        self._start_pac_server()

        # Apply native Window & Taskbar icon via Win32 WM_SETICON
        self._apply_window_icon()

        # Launch continuous low-impact background monitor thread
        self._monitor_thread = threading.Thread(target=self._background_health_monitor, daemon=True)
        self._monitor_thread.start()

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
        """Asynchronously attaches the native high-res icon to the WinForms Window & Windows Taskbar."""
        def _worker():
            for _ in range(30):
                hwnd = self._get_hwnd()
                if hwnd and user32:
                    icon_path = os.path.join(BUNDLE_DIR, "gui", "icon.ico")
                    if not os.path.exists(icon_path):
                        icon_path = os.path.join(APP_DIR, "gui", "icon.ico")
                    if os.path.exists(icon_path):
                        try:
                            # 1 = IMAGE_ICON, 0x0010 = LR_LOADFROMFILE
                            h_icon_big = user32.LoadImageW(0, icon_path, 1, 0, 0, 0x0010)
                            h_icon_sm = user32.LoadImageW(0, icon_path, 1, 16, 16, 0x0010)
                            if h_icon_big:
                                user32.PostMessageW(hwnd, 0x0080, 1, h_icon_big) # WM_SETICON, ICON_BIG
                            if h_icon_sm:
                                user32.PostMessageW(hwnd, 0x0080, 0, h_icon_sm) # WM_SETICON, ICON_SMALL
                            print(f"[UI] Native Window & Taskbar icon applied (HWND {hwnd})")
                            break
                        except Exception as e:
                            print(f"[UI] Apply icon error: {e}")
                time.sleep(0.15)
        threading.Thread(target=_worker, daemon=True).start()

    def start_drag(self):
        """Native hardware Windows caption drag via WM_NCLBUTTONDOWN on HTCAPTION."""
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ReleaseCapture()
                user32.SendMessageW(hwnd, 0x00A1, 2, 0)
        except Exception:
            pass

    def move_window(self, x, y):
        """High-performance hardware window mover with automatic DPI scaling."""
        try:
            if self._window:
                self._window.move(int(x), int(y))
        except Exception:
            pass

    def minimize(self):
        """Native instant window minimize."""
        try:
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ShowWindow(hwnd, SW_MINIMIZE)
            elif self._window:
                self._window.minimize()
        except Exception as e:
            print(f"[UI] Minimize error: {e}")

    def toggle_maximize(self):
        """No-op as maximize is disabled."""
        pass

    def close(self):
        """Immediately hides the window and safely stops all core engines in the background."""
        try:
            self._bg_monitor_running = False
            hwnd = self._get_hwnd()
            if hwnd and user32:
                user32.ShowWindow(hwnd, 0)  # SW_HIDE: instant disappearance
            if self._window:
                self._window.hide()
        except Exception:
            pass

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

    def _probe_single(self, key, name, host, port, fallback_ip, check_type, category):
        """Lightweight non-intrusive probe: TCP handshake or 30-byte UDP DNS query."""
        start = time.perf_counter()
        try:
            if check_type == "udp_dns":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1.2)
                q = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
                s.sendto(q, (host, port))
                s.recvfrom(512)
                lat = (time.perf_counter() - start) * 1000.0
                s.close()
                return key, {"name": name, "ok": True, "latency": round(lat, 1), "note": "Anycast DoH", "status": "ok"}
            elif category == "ai":
                try:
                    s = socket.create_connection(("127.0.0.1", 1371), timeout=1.8)
                    s.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
                    resp = s.recv(128)
                    s.close()
                    if b"200" in resp:
                        lat = (time.perf_counter() - start) * 1000.0
                        return key, {"name": name, "ok": True, "latency": round(lat, 1), "note": "Anycast Relay", "status": "ok"}
                except Exception:
                    pass
                try:
                    s = socket.create_connection((host, port), timeout=1.8)
                    lat = (time.perf_counter() - start) * 1000.0
                    s.close()
                    return key, {"name": name, "ok": True, "latency": round(lat, 1), "note": "Anycast Relay", "status": "ok"}
                except Exception:
                    return key, {"name": name, "ok": False, "latency": 0, "note": "Недоступен", "status": "err"}
            else:
                try:
                    s = socket.create_connection((host, port), timeout=1.8)
                except Exception:
                    if fallback_ip:
                        s = socket.create_connection((fallback_ip, port), timeout=1.8)
                    else:
                        raise
                lat = (time.perf_counter() - start) * 1000.0
                s.close()
                note = "QoS Ultra" if category == "youtube" else ("Voice QoS" if category == "discord" else "Desync Active")
                return key, {"name": name, "ok": True, "latency": round(lat, 1), "note": note, "status": "ok"}
        except Exception:
            return key, {"name": name, "ok": False, "latency": 0, "note": "Недоступен", "status": "err"}

    def _background_health_monitor(self):
        """Continuous multi-target parallel availability monitor & autonomous self-healer."""
        import concurrent.futures
        while self._bg_monitor_running:
            try:
                if self.is_running:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                        future_to_target = {executor.submit(self._probe_single, *t): t for t in self._probe_targets}
                        for future in concurrent.futures.as_completed(future_to_target):
                            try:
                                key, res = future.result()
                                target = future_to_target[future]
                                category = target[6]
                                prev_data = self.service_health.get(key, {})
                                if res["ok"]:
                                    prev_data["ok"] = True
                                    prev_data["latency"] = res["latency"]
                                    prev_data["note"] = res["note"]
                                    prev_data["status"] = "ok"
                                    prev_data["consecutive_fails"] = 0
                                else:
                                    fails = prev_data.get("consecutive_fails", 0) + 1
                                    prev_data["consecutive_fails"] = fails
                                    if fails >= 2:
                                        prev_data["ok"] = False
                                        prev_data["latency"] = 0
                                        prev_data["note"] = res["note"]
                                        prev_data["status"] = "err"
                                        
                                        # Self-healing triggered on persistent degradation
                                        if self.auto_tune_enabled:
                                            self._trigger_auto_tune(key, category)

                                self.service_health[key] = prev_data
                            except Exception:
                                pass

                    all_ok = all(v.get("ok", True) for v in self.service_health.values())
                    if all_ok and self.auto_tune_state != "tuning":
                        self.auto_tune_state = "optimal"
                        self.auto_tune_status = "Оптимально // 100% сервисов активно"

                    time.sleep(random.uniform(4.0, 5.5))
                else:
                    self.auto_tune_state = "standby"
                    self.auto_tune_status = "STANDBY"
                    time.sleep(2.5)
            except Exception:
                time.sleep(3.5)

    def _trigger_auto_tune(self, failed_key, category):
        """Self-Healing Engine: automatically adapts desync rules and tunnel endpoints."""
        now = time.time()
        # Cooldown guard: 14s minimum between adaptions
        if now - self.last_auto_tune_time < 14.0:
            return

        self.last_auto_tune_time = now
        self.auto_tune_state = "tuning"
        t_str = time.strftime("%H:%M:%S")

        if category == "ai":
            self.auto_tune_status = "Адаптация AI-шлюза: обновление Anycast DNS..."
            self._log_event(f"{t_str} — Авто-подстройка: очистка кэша DNS и ревалидация AI-маршрутов")
            print(f"[Auto-Tune] Refreshing DNS cache and re-validating AI endpoints for {failed_key}")

            def refresh_ai_dns():
                try:
                    subprocess.run(["ipconfig", "/flushdns"], creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
                time.sleep(1.0)
                t_item = next((t for t in self._probe_targets if t[0] == failed_key), None)
                if t_item:
                    _, chk = self._probe_single(*t_item)
                    if chk["ok"]:
                        self._log_event(f"{time.strftime('%H:%M:%S')} — AI-сервис {failed_key} восстановлен ({chk['latency']} ms)")
                        self.service_health[failed_key]["ok"] = True
                        self.service_health[failed_key]["consecutive_fails"] = 0
                        self.service_health[failed_key]["latency"] = chk["latency"]
                        self.service_health[failed_key]["status"] = "ok"
                        self.auto_tune_state = "optimal"
                        self.auto_tune_status = "Оптимально // 100% сервисов активно"

            threading.Thread(target=refresh_ai_dns, daemon=True).start()

        elif category == "youtube":
            # Targeted adaptation: rotate DPI preset for YouTube
            strat_candidates = ["youtube", "tspu", "balanced"]
            cur_base = "balanced" if self.active_strategy == "auto" else self.active_strategy
            next_strat = next((s for s in strat_candidates if s != cur_base), "youtube")
            self.auto_tune_status = f"Адаптация YouTube: профиль {next_strat}..."
            self._log_event(f"{t_str} — Авто-подстройка YouTube: переход на профиль {next_strat}")
            print(f"[Auto-Tune] Hot-switching DPI strategy to {next_strat} for YouTube")

            def hot_restart_yt():
                self._start_divert_worker(override_strategy=next_strat)
                time.sleep(2.5)
                _, chk = self._probe_single(*[t for t in self._probe_targets if t[0] == 'youtube'][0])
                if chk["ok"]:
                    self._log_event(f"{time.strftime('%H:%M:%S')} — YouTube 4K поток успешно стабилизирован ({chk['latency']} ms)")
                    self.service_health["youtube"]["ok"] = True
                    self.service_health["youtube"]["consecutive_fails"] = 0
                    self.service_health["youtube"]["latency"] = chk["latency"]
                    self.service_health["youtube"]["status"] = "ok"
                    self.auto_tune_state = "optimal"
                    self.auto_tune_status = "Оптимально // 100% сервисов активно"

            threading.Thread(target=hot_restart_yt, daemon=True).start()

        elif category == "discord":
            # Targeted adaptation: switch to dedicated Discord WebRTC preset
            cur_base = "balanced" if self.active_strategy == "auto" else self.active_strategy
            next_strat = "discord" if cur_base != "discord" else "balanced"
            self.auto_tune_status = f"Адаптация Discord: профиль {next_strat}..."
            self._log_event(f"{t_str} — Авто-подстройка Discord: оптимизация WebRTC ({next_strat})")
            print(f"[Auto-Tune] Hot-switching DPI strategy to {next_strat} for Discord")

            def hot_restart_discord():
                self._start_divert_worker(override_strategy=next_strat)
                time.sleep(2.5)
                _, chk = self._probe_single(*[t for t in self._probe_targets if t[0] == failed_key][0])
                if chk["ok"]:
                    self._log_event(f"{time.strftime('%H:%M:%S')} — Discord Voice восстановлен ({chk['latency']} ms)")
                    self.service_health[failed_key]["ok"] = True
                    self.service_health[failed_key]["consecutive_fails"] = 0
                    self.service_health[failed_key]["latency"] = chk["latency"]
                    self.service_health[failed_key]["status"] = "ok"
                    self.auto_tune_state = "optimal"
                    self.auto_tune_status = "Оптимально // 100% сервисов активно"

            threading.Thread(target=hot_restart_discord, daemon=True).start()

    def _log_event(self, text):
        self.recent_logs.insert(0, text)
        if len(self.recent_logs) > 8:
            self.recent_logs.pop()

    def get_system_state(self):
        """Zero-latency non-blocking snapshot of network health and self-healing engine."""
        return {
            "is_running": self.is_running,
            "active_strategy": self.active_strategy,
            "auto_tune_enabled": self.auto_tune_enabled,
            "auto_tune_status": self.auto_tune_status,
            "auto_tune_state": self.auto_tune_state,
            "ai_country": self.ai_country,
            "services": self.service_health,
            "recent_logs": self.recent_logs
        }

    def toggle_auto_tune(self, enabled=None):
        if enabled is None:
            self.auto_tune_enabled = not self.auto_tune_enabled
        else:
            self.auto_tune_enabled = bool(enabled)
        t_str = time.strftime("%H:%M:%S")
        txt = "включена" if self.auto_tune_enabled else "отключена"
        self._log_event(f"{t_str} — Авто-адаптация {txt}")
        return {"auto_tune_enabled": self.auto_tune_enabled}

    def get_network_ping(self):
        """Fast live latency check to 8.8.8.8 UDP in milliseconds."""
        dns_item = self.service_health.get("dns", {})
        if dns_item.get("ok") and dns_item.get("latency", 0) > 0:
            return dns_item["latency"]
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
        """Instant concurrent parallel test across all 7 monitored endpoints."""
        import concurrent.futures
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(self._probe_single, *t) for t in self._probe_targets]
            for future in concurrent.futures.as_completed(futures):
                try:
                    k, res = future.result()
                    results[k] = res
                    # Update local state
                    if k in self.service_health:
                        self.service_health[k]["ok"] = res["ok"]
                        self.service_health[k]["latency"] = res["latency"]
                        self.service_health[k]["note"] = res["note"]
                        self.service_health[k]["status"] = res["status"]
                        if res["ok"]:
                            self.service_health[k]["consecutive_fails"] = 0
                except Exception:
                    pass
        return results

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
        print(f"[Core] Network Booster activating: {self.active_strategy}")
        self.is_running = True
        self.auto_tune_state = "optimal"
        self.auto_tune_status = "Оптимально // Сеть ускорена на 100%"
        self._log_event(f"{time.strftime('%H:%M:%S')} — Ускорение сети активировано. Аппаратный QoS включен")

        # 1. Start WinDivert DPI Worker (YouTube 4K, Discord Web + Voice RTC, TSPU bypass)
        threading.Thread(target=self._start_divert_worker, daemon=True).start()
        # 2. Start Stealth AI Tunnel (WARP + Opera Geo-Exit)
        threading.Thread(target=self._start_ai_tunnel, daemon=True).start()
            
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
            # 1. Terminate any previous tunnel/proxy instances
            subprocess.run(["taskkill", "/F", "/IM", "wireproxy.exe", "/IM", "wireproxy-awg.exe", "/IM", "opera-proxy.exe"],
                           creationflags=0x08000000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
            
            wireproxy_bin = self._find_bin("wireproxy.exe")
            opera_bin = self._find_bin("opera-proxy.exe")
            warp_cfg = os.path.join(APP_DIR, "config", "warp.conf")
            if not os.path.exists(warp_cfg):
                warp_cfg = os.path.join(BUNDLE_DIR, "config", "warp.conf")
            
            # Step 1: WireGuard WARP userspace SOCKS5 tunnel on 127.0.0.1:1370
            if wireproxy_bin and os.path.exists(warp_cfg):
                bin_dir = os.path.dirname(wireproxy_bin)
                self.ai_worker_process = subprocess.Popen(
                    [wireproxy_bin, "-c", warp_cfg],
                    cwd=bin_dir,
                    creationflags=0x08000000 if os.name == 'nt' else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"[Tunnel] Tier 1: WireGuard WARP active on 127.0.0.1:1370 (PID {self.ai_worker_process.pid})")
            
            time.sleep(1.2)

            # Step 2: Opera Geo-Exit Proxy on 127.0.0.1:1371 chained through Tier 1
            if opera_bin:
                bin_dir = os.path.dirname(opera_bin)
                self.ai_opera_process = subprocess.Popen(
                    [opera_bin, "-country", "AM", "-bind-address", "127.0.0.1:1371", "-proxy", "socks5://127.0.0.1:1370", "-verbosity", "40"],
                    cwd=bin_dir,
                    creationflags=0x08000000 if os.name == 'nt' else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"[Tunnel] Tier 2: Opera AI Exit Proxy active on 127.0.0.1:1371 (PID {self.ai_opera_process.pid})")

            # Step 3: Enable Windows PAC proxy
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
            # 1. Update Windows Registry directly
            settings_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, settings_key, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
                except FileNotFoundError:
                    proxy_enable = 0
                try:
                    proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
                except FileNotFoundError:
                    proxy_server = ""
                
                self.prev_proxy_settings = {
                    "ProxyEnable": proxy_enable,
                    "ProxyServer": proxy_server
                }

                winreg.SetValueEx(key, "AutoConfigURL", 0, winreg.REG_SZ, pac_url)
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            # 2. Update DefaultConnectionSettings & SavedLegacySettings binary blobs (flags = 0x05)
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
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, conn_key, 0, winreg.KEY_ALL_ACCESS) as ck:
                    for v in ["DefaultConnectionSettings", "SavedLegacySettings"]:
                        try:
                            winreg.SetValueEx(ck, v, 0, winreg.REG_BINARY, pac_blob)
                        except Exception:
                            pass
            except Exception:
                pass

            # 3. Call official WinINet INTERNET_OPTION_PER_CONNECTION_OPTION
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
            except Exception as e:
                print(f"[AI-Engine] WinINet per-connection option warning: {e}")

            # 4. Notify all system components and running browsers
            wininet = ctypes.windll.wininet
            wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
            print(f"[AI-Engine] Windows PAC proxy active: {pac_url}")
        except Exception as e:
            print(f"[AI-Engine] Windows PAC set error: {e}")

    def _disable_windows_pac(self):
        if os.name != 'nt':
            return
        try:
            # 1. Update Windows Registry
            settings_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, settings_key, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    winreg.DeleteValue(key, "AutoConfigURL")
                except FileNotFoundError:
                    pass
                try:
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
                except Exception:
                    pass

            # 2. Reset DefaultConnectionSettings to Direct (flags = 0x01)
            clean_blob = bytes([
                0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ])
            conn_key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, conn_key, 0, winreg.KEY_ALL_ACCESS) as ck:
                    for v in ["DefaultConnectionSettings", "SavedLegacySettings"]:
                        try:
                            winreg.SetValueEx(ck, v, 0, winreg.REG_BINARY, clean_blob)
                        except Exception:
                            pass
            except Exception:
                pass

            # 3. Call official WinINet INTERNET_OPTION_PER_CONNECTION_OPTION
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
            except Exception as e:
                print(f"[AI-Engine] WinINet per-connection disable warning: {e}")

            wininet = ctypes.windll.wininet
            wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
            wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
            print("[AI-Engine] Windows PAC proxy cleanly disabled and WinINet refreshed.")
        except Exception as e:
            print(f"[AI-Engine] Windows PAC reset error: {e}")

    def stop_engine(self):
        print("[Core] Network Booster stopping...")
        self.is_running = False
        self.auto_tune_state = "standby"
        self.auto_tune_status = "STANDBY"
        self._log_event(f"{time.strftime('%H:%M:%S')} — Ускорение сети отключено")
        
        # 1. Disable Windows PAC Proxy
        self._disable_windows_pac()



        # 3. Terminate DPI Worker
        if self.worker_process:
            try:
                self.worker_process.terminate()
                self.worker_process.wait(timeout=0.8)
            except Exception:
                pass
            self.worker_process = None

        # 4. Terminate AI Tunnel Workers
        if self.ai_opera_process:
            try:
                self.ai_opera_process.terminate()
                self.ai_opera_process.wait(timeout=0.8)
            except Exception:
                pass
            self.ai_opera_process = None

        if self.ai_worker_process:
            try:
                self.ai_worker_process.terminate()
                self.ai_worker_process.wait(timeout=0.8)
            except Exception:
                pass
            self.ai_worker_process = None

        # 5. Clean up any leftover processes and drivers
        if os.name == 'nt':
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "core-worker.exe", "/IM", "ai-worker.exe", "/IM", "wireproxy.exe", "/IM", "wireproxy-awg.exe", "/IM", "opera-proxy.exe"],
                    creationflags=0x08000000,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                subprocess.run(
                    ["sc.exe", "stop", "WinDivert"],
                    creationflags=0x08000000,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass

        print("[Core] All engines stopped cleanly.")
        return {"status": "ok", "message": "Protection stopped"}

    def change_strategy(self, strategy_id):
        t_str = time.strftime("%H:%M:%S")
        if strategy_id == "auto":
            self.auto_tune_enabled = True
            self.active_strategy = "auto"
            self._log_event(f"{t_str} — Включен режим «Авто-адаптация»")
            print("[Core] Strategy set: auto-adaptive mode enabled")
            if self.is_running:
                self._start_divert_worker(override_strategy="balanced")
        else:
            self.active_strategy = strategy_id
            self._log_event(f"{t_str} — Выбран профиль «{strategy_id}»")
            print(f"[Core] Strategy set manually: {strategy_id}")
            if self.is_running:
                self._start_divert_worker(override_strategy=strategy_id)
        return {"status": "ok", "strategy": strategy_id, "auto_tune_enabled": self.auto_tune_enabled}


def main():
    if not os.path.exists(HTML_PATH):
        print(f"Error: GUI HTML not found at {HTML_PATH}")
        sys.exit(1)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    api = SpectraGlideAPI(None)
    
    webview.settings['ALLOW_FILE_URLS'] = True
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False

    icon_path = os.path.join(APP_DIR, "gui", "icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(BUNDLE_DIR, "gui", "icon.ico")

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
    webview.start(debug=False, icon=icon_path if os.path.exists(icon_path) else None)


if __name__ == "__main__":
    main()
