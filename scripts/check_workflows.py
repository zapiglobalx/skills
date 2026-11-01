"""Checks every GitHub Actions workflow as YAML, not as text. Exit code 1 on any problem.

Run: python3 scripts/check_workflows.py                 # .github/workflows of this repository
     python3 scripts/check_workflows.py <folder>        # another folder of workflows
     python3 scripts/check_workflows.py --self-test     # the good and bad controls below

Refuses: a `uses` anywhere (step or reusable workflow) that is not owner/repo[/path]@<40 hex>; the
pull_request_target trigger in any form of `on` (string, list, mapping, quoted key, YAML 1.1 boolean key);
any reference to secrets in any key or value, after joining the lines of the text; a duplicate key in one
mapping (GitHub and PyYAML may read different copies); a file that is not valid YAML.
Needs PyYAML (pinned by hash in scripts/ci-requirements.txt).
"""

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PINNED_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(/[A-Za-z0-9_./-]+)?@[0-9a-f]{40}")
# "secrets" as a word anywhere in a joined string: secrets.X, secrets['X'], toJSON(secrets), secrets: inherit.
SECRETS_RE = re.compile(r"(?<![A-Za-z0-9_-])secrets(?![A-Za-z0-9_-])", re.IGNORECASE)
FORBIDDEN_TRIGGERS = {"pull_request_target"}


class StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses a key repeated in one mapping."""


def _no_duplicates(loader, node, deep=False):
    keys = []
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in keys:
            raise yaml.constructor.ConstructorError(None, None, f"duplicate key {key!r}", key_node.start_mark)
        keys.append(key)
    return loader.construct_mapping(node, deep)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)


def _walk(value, path=""):
    """Every (path, key, value) in the tree; keys are visited as values too."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield path, "<key>", k
            yield from _walk(v, f"{path}.{k}")
            yield path, k, v
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk(v, f"{path}[{i}]")


def _triggers(doc):
    """The trigger names of a workflow; `on` may be read by YAML 1.1 as the boolean True."""
    found = []
    for key in ("on", True):
        if isinstance(doc, dict) and key in doc:
            on = doc[key]
            if isinstance(on, str):
                found.append(on)
            elif isinstance(on, list):
                found += [str(x) for x in on]
            elif isinstance(on, dict):
                found += [str(x) for x in on]
            elif on is not None:
                found.append(repr(on))
    return found


def check_text(name, text):
    problems = []
    try:
        doc = yaml.load(text, Loader=StrictLoader)
    except yaml.YAMLError as e:
        return [f"{name}: not valid YAML ({str(e).splitlines()[0]})"]
    if not isinstance(doc, dict):
        return [f"{name}: not a workflow mapping"]
    for trig in _triggers(doc):
        if trig.strip().lower() in FORBIDDEN_TRIGGERS:
            problems.append(f"{name}: trigger {trig} is not allowed")
    for path, key, value in _walk(doc):
        if key == "uses":
            if not isinstance(value, str) or not PINNED_RE.fullmatch(value.strip()):
                problems.append(f"{name}{path}: uses {value!r} is not pinned to a full commit SHA")
        if isinstance(value, str) and SECRETS_RE.search(" ".join(value.split())):
            problems.append(f"{name}{path}: references secrets ({' '.join(value.split())[:60]!r})")
    return sorted(set(problems))


def check_folder(folder):
    files = sorted([*folder.glob("*.yml"), *folder.glob("*.yaml")])
    if not files:
        return [f"{folder}: no workflow found"]
    return [p for f in files for p in check_text(f.name, f.read_text(encoding="utf-8"))]


GOOD = """
name: ok
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0
      - run: echo "${{ github.ref }}"
  b:
    uses: owner/repo/.github/workflows/x.yml@0123456789abcdef0123456789abcdef01234567
"""
BASE = "name: x\non: [push]\njobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n"
GOOD_MORE = {
    "on as a string": "name: x\non: push\njobs: {}\n",
    "on as a list with pull_request": "name: x\non: [push, pull_request, workflow_dispatch]\njobs: {}\n",
    "pull_request with types": "name: x\non:\n  pull_request:\n    types: [opened, synchronize]\njobs: {}\n",
    "words that only contain secret": BASE + "      - run: echo secret_name secretsauce my-secrets-file\n",
    "github.token is not a stored secret": BASE + "      - run: echo\n        env:\n          T: ${{ github.token }}\n",
    "uses with a path inside the repo": BASE + "      - uses: github/codeql-action/init@0123456789abcdef0123456789abcdef01234567\n",
}
BAD = {
    # The three forms from the code review of 5c48bab.
    "quoted uses key with a tag": BASE + '      - "uses": actions/setup-node@v4\n',
    "on as a flow mapping with pull_request_target": 'name: x\non: {pull_request_target: {}}\njobs: {}\n',
    "secrets expression split over lines": BASE + "      - run: echo\n        env:\n          T: ${{\n            secrets.ZAPI_TOKEN\n            }}\n",
    # Others.
    "uses with a tag": BASE + "      - uses: actions/setup-node@v4\n",
    "uses with a short SHA": BASE + "      - uses: actions/checkout@11d5960\n",
    "uses with an uppercase SHA": BASE + "      - uses: actions/checkout@11D5960A326750D5838078E36CF38B85AF677262\n",
    "uses with a branch": BASE + "      - uses: actions/checkout@main\n",
    "uses a docker image": BASE + "      - uses: docker://alpine:3.20\n",
    "uses a local action": BASE + "      - uses: ./.github/actions/x\n",
    "reusable workflow with a tag": "name: x\non: [push]\njobs:\n  a:\n    uses: o/r/.github/workflows/w.yml@v1\n",
    "uses through an anchor": "name: x\non: [push]\nx-step: &s {uses: actions/cache@v4}\njobs:\n  a:\n    runs-on: u\n    steps: [*s]\n",
    "uses in a block scalar is still a string": BASE + "      - uses: >-\n          actions/setup-node@v4\n",
    "pull_request_target as a string": "name: x\non: pull_request_target\njobs: {}\n",
    "pull_request_target in a list": "name: x\non: [push, pull_request_target]\njobs: {}\n",
    "pull_request_target quoted in a list": 'name: x\non: [push, "pull_request_target"]\njobs: {}\n',
    "pull_request_target as a block key": "name: x\non:\n  pull_request_target:\n    types: [opened]\njobs: {}\n",
    "quoted on key": 'name: x\n"on":\n  pull_request_target:\njobs: {}\n',
    "On as a YAML 1.1 boolean key": "name: x\nOn: [pull_request_target]\njobs: {}\n",
    "secrets with a dot": BASE + "      - run: echo\n        env:\n          T: ${{ secrets.ZAPI_TOKEN }}\n",
    "secrets indexed": BASE + "      - run: echo\n        env:\n          T: ${{ secrets['ZAPI_TOKEN'] }}\n",
    "secrets in toJSON": BASE + "      - run: echo '${{ toJSON(secrets) }}'\n",
    "secrets inherit": "name: x\non: [push]\njobs:\n  a:\n    uses: o/r/.github/workflows/w.yml@0123456789abcdef0123456789abcdef01234567\n    secrets: inherit\n",
    "secrets in a with input": BASE + "      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262\n        with:\n          token: ${{ secrets.GITHUB_TOKEN }}\n",
    "SECRETS in uppercase": BASE + "      - run: echo ${{ SECRETS.X }}\n",
    "secrets in a block scalar run": BASE + "      - run: |\n          echo ${{\n          secrets.X }}\n",
    "duplicate on key (good last)": "name: x\non: pull_request_target\non: push\njobs: {}\n",
    "not valid YAML": "name: x\non: [push\n",
    "not a mapping": "- a\n- b\n",
}


def self_test():
    failures = []

    def expect(name, ok):
        print(("ok   " if ok else "FAIL ") + name)
        if not ok:
            failures.append(name)

    good = check_text("good", GOOD)
    expect(f"good control passes ({good})", good == [])
    for name, text in GOOD_MORE.items():
        problems = check_text("good", text)
        expect(f"good control passes: {name} ({problems})", problems == [])
    own = check_folder(ROOT / ".github" / "workflows")
    expect(f"this repository's workflows pass ({own})", own == [])
    for name, text in BAD.items():
        problems = check_text("bad", text)
        expect(f"bad control refused: {name} ({problems[:1]})", bool(problems))
    print(f"self-test: {len(failures)} failures, {2 + len(GOOD_MORE)} good controls, {len(BAD)} bad controls")
    return 1 if failures else 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    folder = pathlib.Path(args[0]) if args else ROOT / ".github" / "workflows"
    problems = check_folder(folder)
    for p in problems:
        print(f"error: {p}")
    print(f"{folder}: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
