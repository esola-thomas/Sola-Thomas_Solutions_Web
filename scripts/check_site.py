#!/usr/bin/env python3
"""Static checks for the public site (static_site/).

Enforces the standards in .claude/rules/website-standards.md that a machine can check:
retired content, unapproved claims, page metadata, image attributes, local links, and the
service request form contract. Run before every commit and in the deploy workflow.

    python3 scripts/check_site.py          # check, exit 1 on failure
    python3 scripts/check_site.py --hook   # Claude Code PostToolUse hook mode (exit 2 on failure)
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "static_site"
CONTRACT = ROOT / "docs" / "service-request-contract.md"

# Retired business lines and contact details. Must never reappear on the public site.
RETIRED = [
    r"info@solathomas\.com",
    r"\bnationwide\b",
    r"\bmelbourne\b",
    r"\bhome services\b",
    r"\bbusiness (it )?services\b",
    r"\bIT (services|solutions|support)\b",
]

# Claims that need documented owner evidence before they can be published. To publish one,
# record the evidence in .claude/rules/website-standards.md (Approved facts) and add an
# exact-phrase entry to APPROVED_CLAIM_PHRASES.
UNAPPROVED_CLAIMS = [
    r"\blicensed\b",
    r"\binsured\b",
    r"\bbonded\b",
    r"\bcertified\b",
    r"\bcertification\b",
    r"\bguarantee[ds]?\b",
    r"\btestimonial",
    r"\btrusted by\b",
    r"\baward",
    r"\b#1\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bindustry[- ]leading\b",
    r"\bleading provider\b",
    r"\bwithin \d+ (minutes|hours)\b",
    r"\bsame[- ]day\b",
    r"\b\d+\+? (customers|stations|sites|clients)\b",
    r"\b(revolutioniz|cutting[- ]edge|seamless|unlock|empower|next[- ]generation|world[- ]class)",
]
APPROVED_CLAIM_PHRASES = []

CANONICAL_EXEMPT = {"404.html"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs), self.getpos()[0]))
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def visible_text(page):
    parts = list(page.text)
    for tag, attrs, _ in page.tags:
        for key in ("alt", "title", "aria-label", "placeholder", "content"):
            if attrs.get(key):
                parts.append(attrs[key])
    return " ".join(parts)


def check_text(name, text, errors):
    for pattern in RETIRED:
        m = re.search(pattern, text, re.I)
        if m:
            errors.append(f"{name}: retired content '{m.group(0)}' (Gilbarco-only site; see website-standards.md)")
    stripped = text
    for phrase in APPROVED_CLAIM_PHRASES:
        stripped = stripped.replace(phrase, "")
    for pattern in UNAPPROVED_CLAIMS:
        m = re.search(pattern, stripped, re.I)
        if m:
            errors.append(f"{name}: unapproved claim or generic copy '{m.group(0)}' (needs owner evidence; see website-standards.md)")


def resolve_local(page_path, ref):
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref or ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
        return None
    if ref.startswith("/"):
        target = SITE / ref.lstrip("/")
    else:
        target = (page_path.parent / ref).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target


def check_page(path, errors):
    name = str(path.relative_to(ROOT))
    raw = path.read_text(encoding="utf-8")
    page = PageParser()
    page.feed(raw)
    tags = page.tags

    def find(tag, **want):
        return [a for t, a, _ in tags if t == tag and all(a.get(k) == v for k, v in want.items())]

    html = find("html")
    if not html or not html[0].get("lang"):
        errors.append(f"{name}: <html> needs a lang attribute")
    if not find("title"):
        errors.append(f"{name}: missing <title>")
    if not find("meta", name="viewport"):
        errors.append(f"{name}: missing viewport meta")
    if not find("meta", name="description") and path.name not in CANONICAL_EXEMPT:
        errors.append(f"{name}: missing meta description")
    if path.name not in CANONICAL_EXEMPT and not find("link", rel="canonical"):
        errors.append(f"{name}: missing canonical link")
    h1 = [1 for t, _, _ in tags if t == "h1"]
    if len(h1) != 1:
        errors.append(f"{name}: expected exactly one <h1>, found {len(h1)}")

    base = find("base")
    for tag, attrs, line in tags:
        if tag == "img":
            if "alt" not in attrs:
                errors.append(f"{name}:{line}: <img> missing alt")
            if not (attrs.get("width") and attrs.get("height")):
                errors.append(f"{name}:{line}: <img> missing width/height (layout shift)")
        if tag == "a" and attrs.get("target") == "_blank" and "noopener" not in (attrs.get("rel") or ""):
            errors.append(f"{name}:{line}: target=_blank without rel=noopener")
        for key in ("href", "src"):
            ref = attrs.get(key)
            if not ref or tag in ("base",):
                continue
            if base and not ref.startswith(("/", "http", "mailto:", "tel:", "#", "data:")):
                ref = "/" + ref
            if ref.startswith("#"):
                continue
            target = resolve_local(path, ref)
            if target is not None and not target.exists():
                errors.append(f"{name}:{line}: broken local reference {attrs.get(key)}")

    check_text(name, visible_text(page), errors)
    return page


def check_contract(errors):
    form_path = SITE / "service-request.html"
    if not CONTRACT.exists() or not form_path.exists():
        errors.append("service request form or docs/service-request-contract.md is missing")
        return
    section = CONTRACT.read_text(encoding="utf-8").split("## Customer fields", 1)[-1].split("## ", 1)[0]
    fields = re.findall(r"^\| `([a-z_]+)` \| (yes|no|always) \|", section, re.M)
    form = form_path.read_text(encoding="utf-8")
    for field, required in fields:
        m = re.search(r'<(input|select|textarea)\b[^>]*\bname="%s"[^>]*>' % re.escape(field), form)
        if not m:
            errors.append(f"service-request.html: contract field '{field}' missing from the form")
            continue
        if required == "yes" and "required" not in m.group(0):
            errors.append(f"service-request.html: contract field '{field}' must be required")


def run():
    errors = []
    for path in sorted(SITE.rglob("*.html")):
        check_page(path, errors)
    for path in sorted(SITE.rglob("*")):
        if path.suffix in (".js", ".txt", ".xml", ".svg"):
            for pattern in RETIRED[:1]:
                if re.search(pattern, path.read_text(encoding="utf-8", errors="ignore"), re.I):
                    errors.append(f"{path.relative_to(ROOT)}: retired contact '{pattern}'")
    check_contract(errors)
    return errors


def main():
    hook = "--hook" in sys.argv
    if hook:
        try:
            event = json.load(sys.stdin)
        except ValueError:
            event = {}
        file_path = (event.get("tool_input") or {}).get("file_path", "")
        if "static_site" not in file_path and "service-request-contract" not in file_path:
            return 0
    errors = run()
    if not errors:
        if not hook:
            print("check_site: OK")
        return 0
    out = sys.stderr if hook else sys.stdout
    print("check_site: %d problem(s)" % len(errors), file=out)
    for e in errors:
        print("  - " + e, file=out)
    return 2 if hook else 1


if __name__ == "__main__":
    sys.exit(main())
