"""Check a WhatsApp Flow's flow_json against the rules the Omni docs list, before calling the API.

Rules from https://developer.omni.z-api.io/flows/components.md ("Regras que a Meta valida"):
screen IDs in capital letters and underscore only, SUCCESS reserved, unique; field names in lowercase
letters, digits and underscore, unique within a screen; a footer on every screen; navigate goes to a
screen that exists and is not itself; complete only on a final screen and every final screen uses it;
at least one final screen; data_exchange needs endpoint_uri; version 6.0 to 7.1.
Final screens are marked "terminal": true, as in https://developer.omni.z-api.io/flows/create-flow.md
The rules on choice options (at least one, each with ID and text, IDs unique) are not checked: the docs
do not name the option keys.

Run: python3 check_flow.py flow.json [--endpoint-uri URL]   # exit 1 on any problem
     python3 check_flow.py                                  # self-test
"""

import json
import re
import sys

VERSIONS = {"6.0", "6.1", "6.2", "6.3", "7.0", "7.1"}
SCREEN_RE = re.compile(r"[A-Z_]+")
FIELD_RE = re.compile(r"[a-z0-9_]+")
INPUTS = {"TextInput", "TextArea", "DatePicker", "Dropdown", "RadioButtonsGroup", "CheckboxGroup", "OptIn"}


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def check(flow, endpoint_uri=None):
    problems = []
    if not isinstance(flow, dict):
        return ["flow_json is not a JSON object"]
    if str(flow.get("version")) not in VERSIONS:
        problems.append(f"version {flow.get('version')!r} is not one of {sorted(VERSIONS)}")
    screens = flow.get("screens") or []
    if not isinstance(screens, list):
        return problems + ["screens is not a list"]
    for i, s in enumerate(screens):
        if not isinstance(s, dict):
            problems.append(f"screen {i} is not a JSON object")
    screens = [s for s in screens if isinstance(s, dict)]
    ids = [s.get("id") for s in screens]
    if not screens:
        problems.append("no screens")
    for sid in ids:
        if not isinstance(sid, str) or not SCREEN_RE.fullmatch(sid):
            problems.append(f"screen id {sid!r}: capital letters and underscore only, no digits")
        elif sid == "SUCCESS":
            problems.append("screen id SUCCESS is reserved")
    for sid in sorted({i for i in ids if isinstance(i, str) and ids.count(i) > 1}):
        problems.append(f"screen id {sid!r} is used twice")
    if not any(s.get("terminal") is True for s in screens):
        problems.append("no final screen (\"terminal\": true)")
    for s in screens:
        sid = s.get("id") if isinstance(s.get("id"), str) else repr(s.get("id"))
        nodes = list(walk(s.get("layout", {})))
        names = [n.get("name") for n in nodes if isinstance(n.get("type"), str) and n.get("type") in INPUTS]
        for name in names:
            if not isinstance(name, str) or not FIELD_RE.fullmatch(name):
                problems.append(f"{sid}: field name {name!r}: lowercase letters, digits and underscore only")
        for name in sorted({n for n in names if isinstance(n, str) and names.count(n) > 1}):
            problems.append(f"{sid}: field name {name!r} is used twice on the screen")
        if not any(n.get("type") == "Footer" for n in nodes):
            problems.append(f"{sid}: no footer")
        actions = [n["on-click-action"] for n in nodes if isinstance(n.get("on-click-action"), dict)]
        names_used = [a.get("name") for a in actions]
        for a in actions:
            if a.get("name") == "navigate":
                nxt = (a.get("next") or {}).get("name")
                if nxt == sid:
                    problems.append(f"{sid}: navigates to itself")
                elif nxt not in ids:
                    problems.append(f"{sid}: navigates to {nxt!r}, which does not exist")
            if a.get("name") == "data_exchange" and not endpoint_uri:
                problems.append(f"{sid}: data_exchange needs endpoint_uri")
        final = s.get("terminal") is True
        if "complete" in names_used and not final:
            problems.append(f"{sid}: uses complete but is not a final screen")
        if final and "complete" not in names_used:
            problems.append(f"{sid}: final screen without complete")
    return problems


VALID = {
    "version": "7.0",
    "routing_model": {"WELCOME": ["DONE"], "DONE": []},
    "screens": [
        {"id": "WELCOME", "title": "Agendamento", "layout": {"type": "SingleColumnLayout", "children": [
            {"type": "Form", "name": "form", "children": [
                {"type": "TextInput", "name": "nome", "label": "Seu nome", "input-type": "text", "required": True},
                {"type": "DatePicker", "name": "data", "label": "Data"},
                {"type": "Footer", "label": "Continuar",
                 "on-click-action": {"name": "navigate", "next": {"type": "screen", "name": "DONE"}, "payload": {}}}]}]}},
        {"id": "DONE", "title": "Pronto", "terminal": True, "success": True, "layout": {"type": "SingleColumnLayout", "children": [
            {"type": "TextBody", "text": "Agendamento confirmado."},
            {"type": "Footer", "label": "Fechar", "on-click-action": {"name": "complete", "payload": {}}}]}},
    ],
}


def self_test():
    def broken(change):
        flow = json.loads(json.dumps(VALID))
        change(flow)
        return check(flow)

    welcome = lambda f: f["screens"][0]
    done = lambda f: f["screens"][1]
    form = lambda f: welcome(f)["layout"]["children"][0]["children"]
    cases = [
        ("valid flow accepted", check(VALID), None),
        ("digit in screen id", broken(lambda f: welcome(f).update(id="TELA_2")), "capital letters"),
        ("lowercase screen id", broken(lambda f: welcome(f).update(id="Welcome")), "capital letters"),
        ("screen id with a trailing newline", broken(lambda f: (welcome(f).update(id="WELCOME\n"), f["routing_model"].update({"WELCOME\n": ["DONE"]}))), "capital letters"),
        ("SUCCESS reserved", broken(lambda f: done(f).update(id="SUCCESS")), "reserved"),
        ("duplicate screen id", broken(lambda f: done(f).update(id="WELCOME")), "used twice"),
        ("bad field name", broken(lambda f: form(f)[0].update(name="nome-completo")), "lowercase letters"),
        ("field name with a trailing newline", broken(lambda f: form(f)[0].update(name="nome\n")), "lowercase letters"),
        ("duplicate field", broken(lambda f: form(f)[1].update(name="nome")), "used twice on the screen"),
        ("no footer", broken(lambda f: done(f)["layout"]["children"].pop()), "no footer"),
        ("navigate to missing screen", broken(lambda f: form(f)[2]["on-click-action"]["next"].update(name="FIM")), "does not exist"),
        ("navigate to itself", broken(lambda f: form(f)[2]["on-click-action"]["next"].update(name="WELCOME")), "itself"),
        ("no final screen", broken(lambda f: done(f).pop("terminal")), "no final screen"),
        ("complete on a non-final screen", broken(lambda f: form(f)[2].update({"on-click-action": {"name": "complete", "payload": {}}})), "not a final screen"),
        ("final screen without complete", broken(lambda f: done(f)["layout"]["children"][1]["on-click-action"].update(name="navigate", next={"type": "screen", "name": "WELCOME"})), "without complete"),
        ("data_exchange without endpoint_uri", broken(lambda f: form(f)[2].update({"on-click-action": {"name": "data_exchange", "payload": {}}})), "endpoint_uri"),
        ("version 5.0", broken(lambda f: f.update(version="5.0")), "version"),
        ("screen that is not an object", broken(lambda f: f["screens"].append("DONE")), "not a JSON object"),
        ("unhashable screen id", broken(lambda f: done(f).update(id=["DONE"])), "capital letters"),
        ("unhashable field name", broken(lambda f: form(f)[0].update(name=["nome"])), "lowercase letters"),
        ("flow_json not an object", check([]), "not a JSON object"),
    ]
    failures = 0
    for label, problems, expected in cases:
        ok = not problems if expected is None else any(expected in p for p in problems)
        if not ok:
            failures += 1
            print(f"FAIL {label}: {problems}")
    # data_exchange with endpoint_uri is fine: the rule must not refuse too much.
    flow = json.loads(json.dumps(VALID))
    flow["screens"][0]["layout"]["children"][0]["children"][2]["on-click-action"] = {"name": "data_exchange", "payload": {}}
    if any("endpoint_uri" in p for p in check(flow, endpoint_uri="https://example.com/flow")):
        failures += 1
        print("FAIL data_exchange with endpoint_uri refused")
    if failures:
        sys.exit(1)
    print("ok")


def main(argv):
    if len(argv) == 1:
        return self_test()
    endpoint = None
    if "--endpoint-uri" in argv:
        i = argv.index("--endpoint-uri")
        if i + 1 >= len(argv):
            print("--endpoint-uri needs a URL")
            sys.exit(2)
        endpoint = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) < 2:
        print("usage: check_flow.py flow.json [--endpoint-uri URL]")
        sys.exit(2)
    with open(argv[1], encoding="utf-8") as f:
        flow = json.load(f)
    if isinstance(flow, dict) and isinstance(flow.get("flow_json"), str):
        endpoint = endpoint or flow.get("endpoint_uri")
        flow = json.loads(flow["flow_json"])
    problems = check(flow, endpoint)
    for p in problems:
        print(p)
    print(f"{len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main(sys.argv)
