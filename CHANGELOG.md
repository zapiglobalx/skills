# Changelog

## 1.3.0

The Omni docs no longer describe the Z-API compatibility layer (`zapi.omni.z-api.io`): on 2026-11-12 the index lists no `z-api/` page, and those URLs, including the Z-API limitations page, open the general introduction.

- `omni-migration-from-z-api` 1.1.0: the migration targets the native API only. Every Z-API route maps to a native `content.type` or to "no equivalent"; channel support comes from the message support page; the layer stays only as a warning for code that already calls it (confirm with Omni support, then move to native). `OMNI_CHANNEL_TOKEN` is no longer needed; webhook creation no longer claims the ENTERPRISE role. Scenarios 3, 4 and 12 now cover the native path.
- `omni-core` 1.0.1: "Coming from the classic Z-API" points to `omni-migration-from-z-api` instead of the removed compatibility page.

## 1.2.0

- `omni-choose-connection`: asks who writes first, where the customers are, which number and which features, then recommends the Omni channel or mix of channels (official WhatsApp with Cloud API or coexistence, QR code, Instagram, Messenger, Telegram), with what each needs, costs on Meta's side and cannot do, and hands off to `omni-onboarding`. Makes no API call. Flags where the conversation-window and billing pages disagree.
- `omni-security-hardening`: the Omni panel's security controls (credentials, IP restriction, SDK domains, two-factor login, roles, audit log, webhook signing, MCP rules), who can change each one, what breaks when it is turned on and the order to apply them; what to do after a Secret Key leak; a code review checklist.
- `omni-reliability`: Omni's webhook delivery rules (5-second timeout, 7 attempts over 23 hours, delivery headers, order, alerts) turned into a receiver that answers fast and deduplicates; `CHANNEL_DISCONNECTED` with its reason codes, the `BILLING_*` events and `ACCOUNT_RESTRICTION` on the global webhook; sending without duplicates; what to alert on.
- `omni-troubleshooting`: a fixed order of checks (API answer, channel state, status events, channel rules, template, webhook) with the documented causes for each symptom, and what to collect for support.
- `omni-instagram`: account requirements, the username as recipient, the 1000-byte text limit and media limits, unsupported types and their replacements, the 24-hour window and the 7-day human agent tag, no templates or writing first, and adding Instagram to a WhatsApp bot.
- `omni-otp-verification`: the AUTHENTICATION template (copy code, one-tap, zero-tap, expiry, security notice, send TTL and what Meta refuses), sending a fresh code in body and button, and the verify side: generation, hashing, expiry, attempts, resend caps and number-pumping limits.
- `omni-marketing-campaigns`: consent and a way out first; the marketing template models and their rules (coupon, limited-time offer, media carousel, products, library); Meta's marketing cost; preparing the list; sending in small batches exactly once; stopping on restrictions; measuring clicks and opt-outs. Bulk sending on the QR code channel stays out.
- `zapi-partner-instances`: for integrator partners, the Partner-Token versus the Client-Token, the trial and post-paid cycle, create, subscribe, add calls, list, cancel and delete (one or up to 100), proxy and its failure webhook, and the connection SDK. Where a docs page gives no path, the skill says so and asks for it instead of guessing.
- Test scenarios: 11 in `tests/omni-choose-connection.md`, 12 in `tests/omni-security-hardening.md`, 10 in `tests/omni-instagram.md`, 9 in `tests/omni-otp-verification.md` 10 in `tests/omni-marketing-campaigns.md` and 10 in `tests/zapi-partner-instances.md` (no credentials); 11 in `tests/omni-reliability.md` and 12 in `tests/omni-troubleshooting.md` (one each reads the test channel).

## 1.1.0

Two new skills for moving to Z-API Omni from self-hosted WhatsApp APIs. Both ask which channel the user wants: the QR code channel (`Z_API_WHATSAPP`, the same model as WAHA and Baileys, no window or templates) or official WhatsApp (`META_WHATSAPP`).

- `omni-migration-from-waha`: inventory of WAHA routes, events and handlers; sessions to channels; send routes to `content.type`; `@c.us`, `@g.us` and `@lid`; webhook events and payload fields; WAHA's SHA-512 body HMAC to Omni's five-field HMAC-SHA256; retries, order and deduplication; number by the QR code channel, coexistence or Cloud API (the WAHA session drops when coexistence connects); cutover and rollback.
- `omni-migration-from-evolution-api`: inventory of Evolution API v2 routes, webhooks, event transports and built-in integrations; `WHATSAPP-BAILEYS` versus `WHATSAPP-BUSINESS`; send routes to `content.type`; `messages.upsert` fields; `webhookByEvents`, `webhookBase64` and the `apikey` body check; Chatwoot, Typebot and other bots; number by the QR code channel, coexistence, Cloud API or number migration; cutover, rollback and key rotation.
- 14 test scenarios each in `tests/`, with fixtures for the code inventory, the call rewrite and a webhook that tries to make the agent reveal keys.

## 1.0.0

First complete release: 10 skills, every claim linked to the official documentation, test scenarios in `tests/` and the harness that runs them confined.

- `zapi-core`: instance, credentials, most used endpoints, webhooks, responsible sending, MCP Server. Guide to using `phone-exists` and the queue (`POST /queue` with `pagingState`).
- `zapi-instance`: connect, reconnect, QR code and phone code, passkey and Z-API Conector, instance and device data, settings (name, photo, auto-read, calls, queue while the instance is disconnected), partners.
- `zapi-send-messages`: text, media, document, link, location, contact, reaction, reply, forward, edit, delete, pin, read; `@lid`; formats and delays; responsible sending rules.
- `zapi-webhooks`: every webhook type, configuration endpoints, filters, payloads and handling end-user text as data.
- `omni-core`: Secret Key, channels, sending, the 24-hour window and templates, webhooks and HMAC verification (Node.js and Python).
- `omni-messages`: free-form messages per channel (official WhatsApp and WhatsApp by QR code, Instagram, Messenger, Telegram), types accepted per channel, the 24-hour window, confirmation through the webhook, cost.
- `omni-templates`: WABAs, the template models, categories and cost, approval and its webhook, validation rules with error codes, sending with parameters.
- `omni-migration-from-z-api`: inventory of Z-API calls in the code, compatibility layer (`zapi.omni.z-api.io`) or native API, credential swap, webhook format, number change and the cutover and rollback plan.
- `omni-onboarding`: creating and connecting channels, official WhatsApp through Embedded Signup (Cloud API or coexistence), moving a number from another provider, QR code, Instagram, Messenger and Telegram, the SDK and its allowed domains.
- `omni-flows`: WhatsApp Flows on the WABA, from the flow_json to publishing, replacing, deprecating and deleting; sending a Flow as a message is not available in Omni yet.
- `scripts/validate.py`: frontmatter, folder name, size, internal and documentation links, scenario table, webhook notice, secrets in the text; `--online` checks every documentation link.
- `scripts/run-scenario.py`: runs a scenario in a clean, confined agent (sandbox, proxy, isolated HOME), with only the scenario's skills and clients pinned by manifest; in live scenarios, only messages to `TEST_PHONE` and a short list of reads, with credentials scrubbed from the response; transcript with every credential replaced by its name.
- Version `1.0.0` in `metadata.version` of all 10 skills.

## 0.1.1

- `zapi-core`: `POST /queue` instead of the obsolete `GET /queue`.

## 0.1.0

- `zapi-core`: instance, credentials, most used endpoints, webhooks, responsible sending, MCP Server.
- `omni-core`: Secret Key, channels, sending, the 24-hour window and templates, webhooks and HMAC verification (Node.js and Python).
