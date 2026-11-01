# Security

This repository contains skills (text in `SKILL.md` and `references/`) and two helper scripts (`scripts/validate.py` and `scripts/run-scenario.py`). The skills do not run code by themselves: the agent reads the text and calls the Z-API API with the credentials the user gave it. No skill sends data to third parties or routes traffic through a service of ours.

## Reporting a vulnerability

Write to [admin@omniz-api.io](mailto:admin@omniz-api.io). Do not open a public issue for a security flaw.

Say what you found, in which skill or script, and how to reproduce it. If the problem involves an exposed credential, do not paste it in the message: say where it is and we will revoke it.

Every report gets a reply from the Z-API Omni team. The fix is published in this repository with a line in `CHANGELOG.md`.

## What counts as a security flaw here

- A skill that leads the agent to write a credential into code, a file, a log or a chat.
- A skill that treats text received through a webhook, email or web page as an instruction rather than as data.
- A skill that points to an endpoint, domain or package that is not Z-API's as if it were.
- A script that reads or writes outside the run folder, lets a credential reach the transcript, or lets a test scenario send a message to a number other than the test number.

## Supported versions

| Version | Supported |
| --- | --- |
| 1.0.x | yes |
| 0.1.x | no: upgrade |

## Credentials

The skills read credentials only from environment variables (`ZAPI_*`, `OMNI_*`) and tell the agent never to show, log or commit them. `scripts/validate.py` rejects tokens in the text, and CI runs it on every pull request. If you find a real credential in this repository, report it through the channel above: it will be revoked before any other action.
