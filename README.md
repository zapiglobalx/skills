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
| Moving from WAHA to Omni | your WAHA server and `api.omni.z-api.io` | `omni-migration-from-waha` |
| Moving from Evolution API to Omni | your Evolution server and `api.omni.z-api.io` | `omni-migration-from-evolution-api` |

## Catalog

Version 1.5.0. Every skill links each endpoint, field and limit to its official page, and ships test scenarios in `tests/<name>.md`.

| Skill | What it teaches |
| --- | --- |
| [`zapi-core`](skills/zapi-core/SKILL.md) | Instance URL, token and Client-Token, commonly used endpoints, webhooks, responsible sending, and when to use the MCP Server. Read first for any Z-API task |
| [`zapi-instance`](skills/zapi-instance/SKILL.md) | Connecting and reconnecting, QR code and phone code, passkey and Z-API Conector, instance and device data, settings (name, photo, auto-read, calls, queue) |
| [`zapi-send-messages`](skills/zapi-send-messages/SKILL.md) | Text, image, audio, video, document, link, location, contact, reaction; reply, forward, edit, delete, pin, mark as read; `@lid`, formats, delays and responsible-sending rules |
| [`zapi-webhooks`](skills/zapi-webhooks/SKILL.md) | Every webhook type, configuration endpoints, filters, payloads, and treating end-user text as data |
| [`zapi-partner-instances`](skills/zapi-partner-instances/SKILL.md) | For Z-API integrator partners: creating, subscribing, listing, canceling and deleting customers' instances, calls, proxy and its failure webhook, the connection SDK inside the partner's product, and the post-paid cycle |
| [`zapi-business-catalog-and-labels`](skills/zapi-business-catalog-and-labels/SKILL.md) | WhatsApp Business app numbers: labels and notes on chats, products, cart and collections, sending a product or the catalog, and the business profile (description, websites, categories, opening hours) |
| [`zapi-newsletters-communities-status`](skills/zapi-newsletters-communities-status/SKILL.md) | WhatsApp channels (`@newsletter`), communities and their announcement group with the anti-scam protection, and posting and replying to status |
| [`zapi-calls`](skills/zapi-calls/SKILL.md) | WhatsApp calls: a short call with recorded audio, live voice and video through the call SDK, SIP for an existing PABX, call events with duration and recording, rejecting calls |
| [`zapi-security-hardening`](skills/zapi-security-hardening/SKILL.md) | Securing a Z-API integration: the token in the URL, turning on the Client-Token without an outage, IP restriction, two-factor login, webhook path secrets, the WhatsApp PIN on mobile instances, what to do after a leak |
| [`zapi-mobile-registration`](skills/zapi-mobile-registration/SKILL.md) | Registering the user's own number on a mobile instance (code, captcha, PIN, transfer), requesting a review of a banned number, recognizing a shadowban; no help evading bans |
| [`omni-core`](skills/omni-core/SKILL.md) | Secret Key, channels, sending, the 24-hour window and templates, webhooks, and HMAC verification. Read first for any Omni task |
| [`omni-messages`](skills/omni-messages/SKILL.md) | Free-form messages per channel: accepted types on each channel, the 24-hour window on official WhatsApp, delivery confirmation by webhook, cost |
| [`omni-templates`](skills/omni-templates/SKILL.md) | WABAs, template models, categories and cost, approval and its webhook, validation rules with error codes, sending with parameters |
| [`omni-migration-from-z-api`](skills/omni-migration-from-z-api/SKILL.md) | Inventory of the Z-API calls in your code, each route on the native Omni API, credential swap, webhook format with `payloadFormat` `Z_API`, QR code or official channel, moving the number, cutover and rollback, and what to do with code that still calls the old compatibility layer |
| [`omni-migration-from-waha`](skills/omni-migration-from-waha/SKILL.md) | Inventory of the WAHA calls and webhook handlers, sessions to channels, `sendText` and the other send routes, `@c.us` and `@lid` ids, events and payload fields, SHA-512 to Omni HMAC, QR code channel or official WhatsApp, moving the number, cutover and rollback |
| [`omni-migration-from-evolution-api`](skills/omni-migration-from-evolution-api/SKILL.md) | Inventory of the Evolution API calls, webhooks and built-in integrations (Chatwoot, Typebot), instances to channels, send routes, `remoteJid`, `messages.upsert` fields, `webhookByEvents` and `apikey` checks, QR code channel or official WhatsApp for Baileys and Cloud API numbers, cutover and rollback |
| [`omni-onboarding`](skills/omni-onboarding/SKILL.md) | Creating and connecting Omni channels: official WhatsApp through Embedded Signup, Cloud API or coexistence, moving a number from another provider, QR code, Instagram, Messenger and Telegram, the SDK and its allowed domains |
| [`omni-flows`](skills/omni-flows/SKILL.md) | WhatsApp Flows on the WABA: building the flow_json, creating, validating, fixing, publishing, replacing, deprecating and deleting a Flow |
| [`omni-choose-connection`](skills/omni-choose-connection/SKILL.md) | Choosing the Omni channel before creating it: official WhatsApp (Cloud API or coexistence) or QR code, Instagram, Messenger or Telegram, what each needs, costs and cannot do |
| [`omni-security-hardening`](skills/omni-security-hardening/SKILL.md) | Securing an Omni integration and workspace: Secret Key and leaks, IP restriction, roles, two-factor login, audit log, webhook signing secrets, letting an AI in through MCP, and a code review checklist |
| [`omni-reliability`](skills/omni-reliability/SKILL.md) | Keeping an Omni integration up in production: webhook retries, duplicates, order and downtime; channel disconnection reasons, billing and Meta restriction notices on the global webhook; sending without duplicates; what to alert on |
| [`omni-troubleshooting`](skills/omni-troubleshooting/SKILL.md) | Finding out why something in Omni does not work: refused calls, undelivered messages, status events, channel rules, template rejections and category changes, webhooks that stop receiving or verifying, and what to send support |
| [`omni-instagram`](skills/omni-instagram/SKILL.md) | Instagram Direct on Omni: which accounts can connect, the username as recipient, text and media limits, unsupported types and what to send instead, the 24-hour window and the human agent tag, no templates, adding Instagram to a WhatsApp bot |
| [`omni-otp-verification`](skills/omni-otp-verification/SKILL.md) | Verification codes on official WhatsApp: the AUTHENTICATION template (copy code, one-tap, zero-tap, expiry, send TTL), sending a fresh code, and a safe verify side (hashing, expiry, attempts, resend and abuse limits) |
| [`omni-marketing-campaigns`](skills/omni-marketing-campaigns/SKILL.md) | WhatsApp marketing campaigns on the official connection: opt-in and opt-out, choosing the template model (coupon, limited-time offer, carousel, products), Meta's cost, sending to a list in batches without duplicates, stopping on restrictions, measuring clicks |
| [`omni-gohighlevel`](skills/omni-gohighlevel/SKILL.md) | Messaging HighLevel contacts through Omni: picking contacts with consent through HighLevel's MCP server, appointment reminders with buttons, follow-ups, hand-off to a person, and recording each send on the contact. Works with HighLevel; not affiliated with or endorsed by HighLevel |
| [`omni-multichannel-replies`](skills/omni-multichannel-replies/SKILL.md) | One bot on several Omni channels: what each channel accepts, the fallback when it does not (lists, location, call buttons, stickers), identifiers and windows per channel, and why a `200` is not proof of delivery |
| [`omni-billing-and-account-health`](skills/omni-billing-and-account-health/SKILL.md) | What official WhatsApp costs (categories, free cases, the 2026 changes, BRL billing), Meta's payment method, Omni's billing events, restriction notices, and a check before any send to many people |
| [`omni-appointment-reminders`](skills/omni-appointment-reminders/SKILL.md) | Appointment reminders: the UTILITY template with Confirm, Reschedule and Cancel, payloads per appointment, free-form buttons inside the window or on the QR code channel, timing without duplicates, opt-out |
| [`omni-cart-recovery`](skills/omni-cart-recovery/SKILL.md) | Abandoned carts and post-purchase: which template model and category fits each moment (reminder, coupon, checkout button, Pix invoice, order updates), consent, timing and stopping rules |
| [`omni-migration-from-twilio`](skills/omni-migration-from-twilio/SKILL.md) | Moving WhatsApp from Twilio: sends, Content Templates, status callbacks, inbound fields and the signature check mapped to Omni, moving the number between providers in Meta's business portfolio, cutover and rollback |
| [`omni-mcp`](skills/omni-mcp/SKILL.md) | Connecting an AI client to Omni's MCP server: setup per client, the tools, who can create templates and flows through it, workspace rules, IP allowlist effects, revoking, and when to use REST instead |
| [`omni-whatsapp-calling`](skills/omni-whatsapp-calling/SKILL.md) | WhatsApp calling on Omni as documented today: the call permission request template and the customer's answer; placing calls is not in the docs yet |

Coming next: chatbot on Omni; Omni with n8n and HubSpot; migrating to Omni from other WhatsApp API providers besides WAHA, Evolution API and Twilio.

## Credentials

Skills read credentials from environment variables and never write them into code:

| Skill | Variables |
| --- | --- |
| `zapi-core`, `zapi-instance`, `zapi-send-messages` | `ZAPI_INSTANCE_ID`, `ZAPI_TOKEN`, `ZAPI_CLIENT_TOKEN` |
| `zapi-webhooks` | the three above, plus `ZAPI_WEBHOOK_PATH_SECRET` (the secret in your webhook path) |
| `zapi-partner-instances` | `ZAPI_PARTNER_TOKEN` for partner routes; `ZAPI_CLIENT_TOKEN` and each instance's ID and token for the SDK token |
| `omni-core` | `OMNI_SECRET_KEY`, `OMNI_CHANNEL_ID`, `OMNI_WEBHOOK_SECRET` |
| `omni-messages` | `OMNI_SECRET_KEY`, `OMNI_CHANNEL_ID` |
| `omni-templates` | `OMNI_SECRET_KEY` |
| `omni-migration-from-z-api` | the Z-API and Omni variables above |
| `omni-migration-from-waha`, `omni-migration-from-evolution-api` | the Omni variables above; they read the WAHA or Evolution code and never call those servers |
| `omni-onboarding` | the Omni Secret Key on the backend and the Public Key in the connection SDK; a Telegram bot token when connecting Telegram |
| `omni-flows` | `OMNI_SECRET_KEY` |
| `omni-choose-connection` | none: it makes no API call |
| `omni-security-hardening` | none: every control is changed in the Omni panel |
| `omni-reliability` | `OMNI_SECRET_KEY`; the webhook secret on the receiver |
| `omni-troubleshooting` | `OMNI_SECRET_KEY` for the read-only checks |
| `omni-instagram` | `OMNI_SECRET_KEY` |
| `omni-otp-verification` | `OMNI_SECRET_KEY`; a secret of the user's app to hash codes |
| `omni-marketing-campaigns` | `OMNI_SECRET_KEY` |
| `omni-gohighlevel` | `OMNI_SECRET_KEY` and `OMNI_CHANNEL_ID`; the HighLevel side uses HighLevel's MCP server with OAuth, so no HighLevel key is stored |

No skill routes traffic through a third-party service: the agent communicates directly with the Z-API API.

## Test

Every skill has scenarios in `tests/<name>.md`. `scripts/run-scenario.py` runs a scenario in a clean, confined agent with only that scenario's skills; scenarios marked **live**, **sends** or **account** need the test instance or account and only message `TEST_PHONE`. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Every new skill includes an official documentation source for each endpoint and test scenarios in `tests/`. CI checks formatting, links, and secrets on every pull request. Security issues: see [SECURITY.md](SECURITY.md).

## Summary

Install with `npx skills add zapiglobalx/skills`. Thirty-three skills, version 1.5.0: `zapi-core`, `zapi-instance`, `zapi-send-messages`, `zapi-webhooks`, `zapi-partner-instances`, `zapi-business-catalog-and-labels`, `zapi-newsletters-communities-status`, `zapi-calls`, `zapi-security-hardening` and `zapi-mobile-registration` for the classic Z-API (`api.z-api.io`); `omni-core`, `omni-messages`, `omni-templates`, `omni-onboarding`, `omni-flows`, `omni-choose-connection`, `omni-security-hardening`, `omni-reliability`, `omni-troubleshooting`, `omni-instagram`, `omni-otp-verification`, `omni-marketing-campaigns`, `omni-gohighlevel`, `omni-multichannel-replies`, `omni-billing-and-account-health`, `omni-appointment-reminders`, `omni-cart-recovery`, `omni-mcp` and `omni-whatsapp-calling` for Z-API Omni (`api.omni.z-api.io`); `omni-migration-from-z-api` to move from one to the other; `omni-migration-from-waha`, `omni-migration-from-evolution-api` and `omni-migration-from-twilio` to move from those APIs to Omni. Every claim in a skill links to the official docs, every skill ships test scenarios, and no skill routes your traffic through a third party. Credentials come from environment variables only. Security issues: see [SECURITY.md](SECURITY.md). Licensed under Apache-2.0.

## Trademarks

Z-API and Z-API Omni are trademarks of Z-API. WhatsApp, Instagram and Messenger are trademarks of Meta Platforms, Inc. Telegram and all other product names mentioned here are trademarks of their respective owners. These skills are published by the Z-API Omni team and are not affiliated with, sponsored by or endorsed by Meta or any other company named in them.
