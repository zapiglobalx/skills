"""Checks every skill in skills/ before merge. Exit code 1 on any problem.

Run: python3 scripts/validate.py
     python3 scripts/validate.py --online      # also fetch every docs link
     python3 scripts/validate.py --self-test   # offline tests of the link fetcher
"""

import http.server
import pathlib
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC_HOSTS = ("developer.z-api.io", "developer.omni.z-api.io")
NAME_RE = re.compile(r"^(zapi|omni)-[a-z0-9]+(-[a-z0-9]+)*$")
# The host must end right there, so "developer.z-api.io@other-host" or "developer.z-api.io.other-host" never matches.
DOC_URL_RE = re.compile(r"https://developer\.(?:omni\.)?z-api\.io(?=[/\s)`\"'<>]|$)[^\s)`\"'<>]*")
# Signals that a skill sends messages, and the page that says how to send without getting the number blocked.
SENDS_RE = re.compile(r"/send-|/messages\b")
BEST_PRACTICES = "developer.z-api.io/tips/best-practices"
# Long hex or base64-looking strings next to a credential word, or a Bearer token with a real value.
# The word may end a longer name (OMNI_SECRET_KEY, secretKey), be a quoted key as in JSON or a Python dict
# ({"Client-Token": "..."}), have escaped quotes as in a notebook cell ({\"token\": \"...\"}), or use => and backticks.
SECRET_RES = [
    re.compile(r"(?i)(client-token|secret|token|api[_-]?key|password|passwd)[A-Za-z_-]*\\?[\"'`]?\s*(?:[:=]|=>)\s*\\?[\"'`]?[A-Za-z0-9+/_-]{24,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{24,}"),
    # Z-API puts the instance token in the URL path: /token/<value>.
    re.compile(r"/token/[A-Za-z0-9]{16,}"),
]
ALLOWED_SECRET_SNIPPETS = ("0" * 24,)
MAX_LINES = 500
# Limits from the Agent Skills specification: https://agentskills.io/specification
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields, current = {}, None
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line[0] not in " \t" and ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            fields[current] = value.strip().strip('"')
        elif current:
            sub = line.strip()
            if ":" in sub:
                k, v = sub.split(":", 1)
                fields[f"{current}.{k.strip()}"] = v.strip().strip('"')
    return fields


def check_skill(folder, warnings):
    errors = []
    skill_md = folder / "SKILL.md"
    if not skill_md.exists():
        return [f"{folder.name}: missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        return [f"{folder.name}: SKILL.md has no frontmatter"]
    body = text.split("\n---\n", 1)[1]
    name = fm.get("name", "")
    if name != folder.name:
        errors.append(f"{folder.name}: name '{name}' must match the folder")
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        errors.append(f"{folder.name}: name must start with zapi- or omni-, use lowercase and hyphens, and have at most {MAX_NAME} characters")
    desc = fm.get("description", "")
    if not 40 <= len(desc) <= MAX_DESCRIPTION:
        errors.append(f"{folder.name}: description must have 40 to {MAX_DESCRIPTION} characters")
    if len(fm.get("compatibility", "")) > MAX_COMPATIBILITY:
        errors.append(f"{folder.name}: compatibility must have at most {MAX_COMPATIBILITY} characters")
    if fm.get("license") != "Apache-2.0":
        errors.append(f"{folder.name}: license must be Apache-2.0")
    if not fm.get("metadata.version"):
        errors.append(f"{folder.name}: metadata.version is required")
    if text.count("\n") > MAX_LINES:
        errors.append(f"{folder.name}: SKILL.md over {MAX_LINES} lines; move detail to references/")
    if not any(host in text for host in DOC_HOSTS):
        errors.append(f"{folder.name}: SKILL.md must link to the official docs")
    tests = ROOT / "tests" / f"{folder.name}.md"
    if not tests.exists():
        errors.append(f"{folder.name}: missing tests/{folder.name}.md")
    elif not re.search(r"^\|\s*1\s*\|", tests.read_text(encoding="utf-8"), re.M):
        errors.append(f"{folder.name}: tests/{folder.name}.md has no scenario table (start from templates/tests.template.md)")
    for rel in re.findall(r"\]\(((?:references|scripts|assets)/[^)#]+)\)", text):
        if not (folder / rel).exists():
            errors.append(f"{folder.name}: broken link {rel}")
    if re.search(r"(?i)webhook", body) and not re.search(r"(?i)never\b.{0,20}\binstructions", body):
        errors.append(f"{folder.name}: mentions webhooks but does not say webhook text is data, never instructions")
    if SENDS_RE.search(body) and BEST_PRACTICES not in body:
        warnings.append(f"{folder.name}: sends messages but does not link to {BEST_PRACTICES}")
    return errors


def check_secrets():
    errors = []
    # Every file except binaries: a token in a .txt, .env, .toml or .mjs under assets/ counts too.
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        data = path.read_bytes()
        if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
            text = data.decode("utf-16", errors="ignore")
        elif b"\0" in data[:8192]:
            continue
        else:
            text = data.decode("utf-8", errors="ignore")
        for n, line in enumerate(text.splitlines(), 1):
            # Remove the allowed placeholder and test the rest, so a real token on the same line is still caught.
            for s in ALLOWED_SECRET_SNIPPETS:
                line = line.replace(s, "")
            if any(r.search(line) for r in SECRET_RES):
                errors.append(f"{path.relative_to(ROOT)}:{n}: looks like a secret")
    return errors


def doc_urls():
    urls = set()
    for path in [*(ROOT / "skills").rglob("*.md"), *(ROOT / "tests").glob("*.md")]:
        for url in DOC_URL_RE.findall(path.read_text(encoding="utf-8")):
            urls.add(url.rstrip(".,:;"))
    return sorted(urls)


class OffDocsRedirect(urllib.error.URLError):
    """A docs link redirected somewhere other than the docs. Counts as a failure and is never followed."""


def on_docs(url):
    """True only for https on one of DOC_HOSTS, default port, no user in the URL."""
    u = urllib.parse.urlsplit(url)
    try:
        port = u.port
    except ValueError:
        return False
    return (u.scheme == "https" and u.hostname in DOC_HOSTS and port in (None, 443)
            and u.username is None and u.password is None)


class DocsOnlyRedirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only when its target is on the docs; anything else raises before any connection.
    Checked on every hop, so a docs page that redirects to another docs page that redirects away still fails."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not on_docs(newurl):
            raise OffDocsRedirect(f"redirect {code} outside the docs to {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def docs_opener():
    return urllib.request.build_opener(DocsOnlyRedirects)


def check_url(url, opener, tries=3, pause=2):
    """The final status of one docs link: 200, 404, another code, or why it failed."""
    status = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "zapi-skills-validate"})
            with opener.open(req, timeout=20) as resp:
                status = resp.status
        except OffDocsRedirect as e:
            return str(e.reason)
        except urllib.error.HTTPError as e:
            status = e.code
        except (urllib.error.URLError, TimeoutError) as e:
            status = str(e)
        if status == 200 or status == 404:
            break
        time.sleep(pause * (attempt + 1))
    return status


def check_links():
    errors = []
    opener = docs_opener()
    for url in doc_urls():
        if not on_docs(url):
            errors.append(f"not a docs link {url}")
            continue
        status = check_url(url, opener)
        if status != 200:
            errors.append(f"dead link {url}: {status}")
    return errors


def self_test():
    """Offline: two local servers; the first redirects, the second stands for a host outside the docs."""
    failures = []

    def expect(name, ok):
        print(("ok   " if ok else "FAIL ") + name)
        if not ok:
            failures.append(name)

    hits = {"first": [], "outside": []}

    def server(name, location=None):
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                hits[name].append(self.path)
                if location:
                    self.send_response(302)
                    self.send_header("Location", location(self.path))
                else:
                    self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, *a):
                pass
        srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        return srv

    outside = server("outside")
    out_url = f"http://127.0.0.1:{outside.server_port}"
    targets = {"/meta": "https://www.facebook.com/business/help", "/local": out_url + "/x",
               "/http": "http://developer.z-api.io/x", "/user": "https://developer.z-api.io@www.facebook.com/x",
               "/port": "https://developer.z-api.io:8443/x", "/suffix": "https://developer.z-api.io.evil.example/x",
               "/rel-outside": "//www.facebook.com/x"}
    first = server("first", lambda path: targets[path])
    base = f"http://127.0.0.1:{first.server_port}"
    opener = docs_opener()
    for path, target in targets.items():
        status = check_url(base + path, opener, tries=3, pause=0)
        expect(f"redirect to {target} fails without being followed ({status})",
               isinstance(status, str) and status.startswith("redirect 302 outside the docs"))
    expect(f"the host outside the docs received nothing ({hits['outside']})", hits["outside"] == [])
    expect(f"each refused link was asked once, no retry ({len(hits['first'])} of {len(targets)})", len(hits["first"]) == len(targets))
    handler = DocsOnlyRedirects()
    req = urllib.request.Request("https://developer.z-api.io/a.md")
    for target in ("https://developer.z-api.io/b.md", "https://developer.omni.z-api.io/c.md", "https://DEVELOPER.Z-API.IO:443/d.md"):
        nxt = handler.redirect_request(req, None, 301, "Moved", {}, target)
        expect(f"redirect inside the docs is followed: {target}", isinstance(nxt, urllib.request.Request) and nxt.full_url == target)
    ok_hosts = all(on_docs(u) for u in ("https://developer.z-api.io/x", "https://developer.omni.z-api.io/x"))
    bad_hosts = [u for u in ("http://developer.z-api.io/x", "https://z-api.io/x", "https://developer.z-api.io.evil/x",
                             "https://evil/developer.z-api.io", "https://u:p@developer.z-api.io/x", "https://developer.z-api.io:99999/x")
                 if on_docs(u)]
    expect(f"on_docs: both docs hosts pass; http, the apex, a suffix, a path, a user and a bad port fail ({bad_hosts})",
           ok_hosts and not bad_hosts)
    first.shutdown(); outside.shutdown()
    print(f"self-test: {len(failures)} failures")
    return 1 if failures else 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    warnings = []
    errors = [e for s in skills for e in check_skill(s, warnings)] + check_secrets()
    names = {s.name for s in skills}
    warnings += [f"tests/{t.name} has no skill" for t in (ROOT / "tests").glob("*.md") if t.stem not in names]
    if "--online" in sys.argv:
        errors += check_links()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(skills)} skills checked, {len(errors)} problems, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
