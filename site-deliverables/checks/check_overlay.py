#!/usr/bin/env python3
"""Checks for the bnbguy.io and term1000nator.com overlay files."""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/tmp/site-sources")
BNB = ROOT / "bnbguy"
TERM = ROOT / "term"
errors = []

def fail(msg):
    errors.append(msg)

def must_contain(text, needle, label):
    if needle not in text:
        fail(f"{label} missing {needle!r}")

def must_not(text, needle, label):
    if needle in text:
        fail(f"{label} still contains {needle!r}")

home = (BNB / "index.html").read_text()
wp = (BNB / "whitepaper" / "index.html").read_text()
term = (TERM / "index.html").read_text()
script = (TERM / "script.js").read_text()
css = (BNB / "styles.css").read_text()
orig_css = (SRC / "bnbguy/site/styles.css").read_text()
orig_home = (SRC / "bnbguy/site/index.html").read_text()
orig_term = (SRC / "term/site/index.html").read_text()
orig_script = (SRC / "term/site/script.js").read_text()

if not css.startswith(orig_css):
    fail("styles.css is not an append-only change of the deployed stylesheet")

# Snapshot arithmetic from the stated balances.
total = 65462.4621
dead = 50173.9648
zero = 589.6557
dead_pct = dead / total * 100
zero_pct = zero / total * 100
combined = (dead + zero) / total * 100
if abs(dead_pct - 76.645398) > 5e-7:
    fail(f"dead LP percent {dead_pct} != 76.645398")
if abs(zero_pct - 0.900754) > 5e-7:
    fail(f"zero LP percent {zero_pct} != 0.900754")
if abs(round(combined, 2) - 77.55) > 1e-9:
    fail(f"combined dead/zero rounded {combined} != 77.55")
if abs(50313855 / 1_000_000_000 * 100 - 5.0313855) > 1e-12:
    fail("token dead percent is not 5.0313855")
# Prior conditional 85.59 was bad arithmetic. 96.889 - 11.240 = 85.649, which
# rounds to 85.65. Both aggregates stay off the pages.
if abs((96.889 - 11.240) - 85.649) > 1e-9:
    fail("internal arithmetic note for the omitted 85.65 conditional failed")

required = [
    "132105546",
    "7 November 2026, 11:34:45 AEDT",
    "65,462.4621",
    "50,173.9648",
    "76.645398%",
    "589.6557",
    "0.900754%",
    "77.55%",
    "50,313,855",
    "5.0313855%",
    "5.03%",
    "1,000,000,000",
    "0xc8f14c26c32bc4bb51d41a6c7822a37bd7de5a9d",
    "0x22dc39bfd015e131e6393d9ec78ce7144188bd37",
    "0xe5fb46157e52a0616fee8d1a198b98c4a9409054",
    "0xf6c999ea7e4afb5593b87ac6bd09b5346419406c",
    "3,595.68",
    "7,357.68",
    "1,708.74",
    "1,303.1290",
    "owner() returned the dead address",
    "Withdrawal implementation not audited",
    "0x28f6267De2d654D407253aC41bffd24FD21ff985",
    "0xFb300ebF79ec2f0101161eaA8c7127C728e7a363",
    "no guaranteed revenue",
    "There is no guaranteed revenue",
    "no fixed burn schedule",
    "Dead and zero addresses",
    "Other contracts",
    "Funds available",
    "Add liquidity",
    "Burn received LP",
    "Publish links",
]
for label, text in (("homepage", home), ("whitepaper", wp)):
    for needle in required:
        must_contain(text, needle, label)
    for needle in (
        "96.89", "96.87", "83.04", "85.59", "85.65", "85.649",
        "4.88%", "48,844,715", "60,484", "4 Nov 2026", "2 November 2026",
        "permanently", "can never", "effectively burned", "Revenue Generated",
        "We promise", "0% tax confirmed", "honeypot detected",
        "Melbourne", "Last Updated: October",
    ):
        must_not(text, needle, label)

must_contain(wp, "339,853,710.1273", "whitepaper")
must_contain(wp, "72,417,127.6856", "whitepaper")
must_contain(wp, "99,000,000", "whitepaper")
must_contain(wp, "24 December 2027", "whitepaper")
must_contain(wp, "automated token scan", "whitepaper")
must_contain(wp, "not a full audit", "whitepaper")
must_contain(wp, "Future ideas: DAO governance", "whitepaper")
must_contain(wp, "does not create a partnership", "whitepaper")
must_contain(wp, "not repeated here as current balances", "whitepaper")
must_contain(wp, "WHITEPAPER 3.0" if False else "November 2026", "whitepaper")
must_contain(wp, "https://x.com/BNBguy_BSC", "whitepaper")
must_contain(wp, "https://t.me/bnb_guy", "whitepaper")
must_contain(wp, "https://www.binance.com/en/square/profile/BNBGUY_BSC", "whitepaper")
must_contain(wp, "https://pancakeswap.finance/swap?chain=bsc&amp;outputCurrency=0x28f6267De2d654D407253aC41bffd24FD21ff985", "whitepaper")
must_contain(home, "72,417,127.6856", "homepage")
must_contain(home, "https://x.com/BNBguy_BSC", "homepage")
must_contain(home, "https://t.me/bnb_guy", "homepage")
must_contain(home, "https://www.coingecko.com/en/coins/bnbguy", "homepage")
must_contain(home, "https://dexscreener.com/bsc/0xfb300ebf79ec2f0101161eaa8c7127c728e7a363", "homepage")
must_not(home, "60,484.36", "homepage")
must_not(home, "1,000 BNBGUY per eligible", "homepage")

def section(html, start_id, next_marker):
    i = html.index(start_id)
    j = html.index(next_marker, i)
    return html[i:j]

if section(home, 'id="watch"', "<!-- ROADMAP -->") != section(orig_home, 'id="watch"', "<!-- ROADMAP -->"):
    fail("Watch section changed")
videos = re.findall(r"/v/bnbguy-[^\"?]+\.(?:mp4|jpg)", home)
orig_videos = re.findall(r"/v/bnbguy-[^\"?]+\.(?:mp4|jpg)", orig_home)
if videos != orig_videos:
    fail(f"BNBGUY video list changed: {len(videos)} vs {len(orig_videos)}")

cover = BNB / "whitepaper/images/bnbguy-whitepaper-cover.jpg"
prepared = SRC / "bnbguy/prepared-november/bnbguy-whitepaper-3-november-2026-cover.jpg"
if hashlib.sha256(cover.read_bytes()).hexdigest() != hashlib.sha256(prepared.read_bytes()).hexdigest():
    fail("cover jpg is not the prepared November cover")
for name in ("bnbguy-whitepaper-image-1.jpg", "bnbguy-whitepaper-image-2.jpg"):
    new_b = (BNB / "whitepaper/images" / name).read_bytes()
    old_b = (SRC / "bnbguy/site/whitepaper/images" / name).read_bytes()
    if new_b == old_b:
        fail(f"{name} was not replaced")
    if b"96.87" in new_b or b"Revenue Generated" in new_b:
        fail(f"{name} still embeds a stale claim")

# TERM
if "last-updated" in script or "querySelectorAll('.log .log-ts')" in script:
    fail("TERM script still overwrites the chapter date into Last updated")
must_contain(term, "<dt>Latest chapter</dt>\n        <dd>2026-11-04</dd>", "term")
must_contain(term, "<dt>Count checked</dt>\n        <dd>2026-11-07 — 132 sent, 868 remaining</dd>", "term")
must_not(term, "Last updated", "term")
must_contain(term, "Australian Navy veteran", "term")
must_not(term, "Melbourne", "term")
must_contain(term, "New chapter videos post on Sundays.", "term")
must_contain(term, "one chapter on X and Medium each Wednesday", "term")
must_contain(term, "https://x.com/TERM1000NATOR/status/2117816140928069914", "term")
ids = re.findall(r"https://x.com/TERM1000NATOR/status/(\d+)", term)
orig_ids = re.findall(r"https://x.com/TERM1000NATOR/status/(\d+)", orig_term)
if ids != orig_ids:
    fail(f"TERM status links changed ({len(ids)} hrefs, {len(set(ids))} unique)")
if len(set(ids)) != 42 or len(ids) != 52:
    fail(f"expected 52 hrefs / 42 unique TERM posts, got {len(ids)} / {len(set(ids))}")
if re.findall(r"/v/ch[12]\.(?:mp4|jpg)", term) != re.findall(r"/v/ch[12]\.(?:mp4|jpg)", orig_term):
    fail("TERM ch1/ch2 videos changed")
ch3 = re.search(r'<figure class="vid">\s*<video[^>]*>\s*<source src="/v/ch3\.mp4".*?</figure>', term, re.S)
if not ch3:
    fail("TERM Chapter 3 video card missing /v/ch3.mp4")
elif "Chapter 3: The Missing Variable" not in ch3.group(0) or "You’ve saved the hardware. And left the operating system behind." not in ch3.group(0) or "x.com/" in ch3.group(0):
    fail("TERM Chapter 3 card title, caption, or X link is wrong")
if term.count("132 sent, 868 remaining") < 2:
    fail("TERM 132/868 count was changed")
if "NOAH'S ARK 2.0 &mdash; Book Two, Chapter 3" not in term:
    fail("Book Two Chapter 3 latest post was replaced")
if "868" not in term or "132 sent" not in term:
    fail("TERM count missing")

# Nothing in the deliverable should be a worker or v/* media blob.
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("checks/"):
        continue
    if path.name == "worker.js" or rel.startswith("v/") or "/v/" in rel:
        fail(f"deliverable includes forbidden path {rel}")

if errors:
    print("FAILED")
    print("\n".join(errors))
    sys.exit(1)
print("OK")
print(f"dead {dead_pct:.6f}% zero {zero_pct:.6f}% combined {combined:.4f}% token 5.0313855%")
print(f"TERM posts unique={len(set(ids))} hrefs={len(ids)} videos kept")
print(f"BNBGUY watch files={len(videos)}")
