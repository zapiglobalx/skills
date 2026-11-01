# Z-API skills

Official [Z-API](https://developer.z-api.io) and [Z-API Omni](https://developer.omni.z-api.io) skills for AI agents. A skill is a folder containing a `SKILL.md` that teaches an agent how to perform a task: send a message, configure a webhook, or verify a signature. They work with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Windsurf, and any agent compatible with the `SKILL.md` format.

## Install

All skills:

```bash
npx skills add zapiglobalx/skills
```

A single skill:

```bash
npx skills add zapiglobalx/skills --skill zapi-send-messages
```

## Which one to use

| You use | API address | Start with |
| --- | --- | --- |
| Z-API (WhatsApp per instance, QR code connection) | `api.z-api.io` | `zapi-core` |
| Z-API Omni (official WhatsApp and QR code connection, Instagram, Messenger, Telegram) | `api.omni.z-api.io` | `omni-core` |
| Moving from Z-API to Omni | both | `omni-migration-from-z-api` |

## Catalog

Version 1.0.0. Every skill links each endpoint, field and limit to its official page, and ships test scenarios in `tests/<name>.md`.

| Skill | What it teaches |
| --- | --- |
| [`zapi-core`](skills/zapi-core/SKILL.md) | Instance URL, token and Client-Token, commonly used endpoints, webhooks, responsible sending, and when to use the MCP Server. Read first for any Z-API task |
| [`zapi-instance`](skills/zapi-instance/SKILL.md) | Connecting and reconnecting, QR code and phone code, passkey and Z-API Conector, instance and device data, settings (name, photo, auto-read, calls, queue) |
| [`zapi-send-messages`](skills/zapi-send-messages/SKILL.md) | Text, image, audio, video, document, link, location, contact, reaction; reply, forward, edit, delete, pin, mark as read; `@lid`, formats, delays and responsible-sending rules |
| [`zapi-webhooks`](skills/zapi-webhooks/SKILL.md) | Every webhook type, configuration endpoints, filters, payloads, and treating end-user text as data |
| [`omni-core`](skills/omni-core/SKILL.md) | Secret Key, channels, sending, the 24-hour window and templates, webhooks, and HMAC verification. Read first for any Omni task |
| [`omni-messages`](skills/omni-messages/SKILL.md) | Free-form messages per channel: accepted types on each channel, the 24-hour window on official WhatsApp, delivery confirmation by webhook, cost |
| [`omni-templates`](skills/omni-templates/SKILL.md) | WABAs, template models, categories and cost, approval and its webhook, validation rules with error codes, sending with parameters |
| [`omni-migration-from-z-api`](skills/omni-migration-from-z-api/SKILL.md) | Inventory of the Z-API calls in your code, compatibility layer or native API, credential swap, webhook format, moving the number, cutover and rollback |
| [`omni-onboarding`](skills/omni-onboarding/SKILL.md) | Creating and connecting Omni channels: official WhatsApp through Embedded Signup, Cloud API or coexistence, moving a number from another provider, QR code, Instagram, Messenger and Telegram, the SDK and its allowed domains |
| [`omni-flows`](skills/omni-flows/SKILL.md) | WhatsApp Flows on the WABA: building the flow_json, creating, validating, fixing, publishing, replacing, deprecating and deleting a Flow |

Coming next: chatbot on Omni; Omni with n8n, HubSpot and HighLevel; migrating to Omni from other WhatsApp API providers.

## Credentials

Skills read credentials from environment variables and never write them into code:

| Skill | Variables |
| --- | --- |
| `zapi-core`, `zapi-instance`, `zapi-send-messages` | `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN` |
| `zapi-webhooks` | the three above, plus `ZAPI_WEBHOOK_PATH_SECRET` (the secret in your webhook path) |
| `omni-core` | `OMNI_SECRET_KEY`, `OMNI_CHANNEL_ID`, `OMNI_WEBHOOK_SECRET` |
| `omni-messages` | `OMNI_SECRET_KEY`, `OMNI_CHANNEL_ID` |
| `omni-templates` | `OMNI_SECRET_KEY` |
| `omni-migration-from-z-api` | the Z-API and Omni variables above, plus `OMNI_CHANNEL_TOKEN` for the compatibility layer |
| `omni-onboarding` | the Omni Secret Key on the backend and the Public Key in the connection SDK; a Telegram bot token when connecting Telegram |
| `omni-flows` | `OMNI_SECRET_KEY` |

No skill routes traffic through a third-party service: the agent communicates directly with the Z-API API.

## Test

Every skill has scenarios in `tests/<name>.md`. `scripts/run-scenario.py` runs a scenario in a clean, confined agent with only that scenario's skills; scenarios marked **live**, **sends** or **account** need the test instance or account and only message `TEST_PHONE`. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Every new skill includes an official documentation source for each endpoint and test scenarios in `tests/`. CI checks formatting, links, and secrets on every pull request. Security issues: see [SECURITY.md](SECURITY.md).

## Summary

Install with `npx skills add zapiglobalx/skills`. Ten skills, version 1.0.0: `zapi-core`, `zapi-instance`, `zapi-send-messages` and `zapi-webhooks` for the classic Z-API (`api.z-api.io`); `omni-core`, `omni-messages`, `omni-templates`, `omni-onboarding` and `omni-flows` for Z-API Omni (`api.omni.z-api.io`); `omni-migration-from-z-api` to move from one to the other. Every claim in a skill links to the official docs, every skill ships test scenarios, and no skill routes your traffic through a third party. Credentials come from environment variables only. Security issues: see [SECURITY.md](SECURITY.md). Licensed under Apache-2.0.

## Trademarks

Z-API and Z-API Omni are trademarks of Z-API. WhatsApp, Instagram and Messenger are trademarks of Meta Platforms, Inc. Telegram and all other product names mentioned here are trademarks of their respective owners. These skills are published by the Z-API Omni team and are not affiliated with, sponsored by or endorsed by Meta or any other company named in them.
