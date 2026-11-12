# Changelog

## 1.2.0

- `omni-choose-connection`: asks who writes first, where the customers are, which number and which features, then recommends the Omni channel or mix of channels (official WhatsApp with Cloud API or coexistence, QR code, Instagram, Messenger, Telegram), with what each needs, costs on Meta's side and cannot do, and hands off to `omni-onboarding`. Makes no API call. Flags where the conversation-window and billing pages disagree.
- 11 test scenarios in `tests/omni-choose-connection.md`, none with credentials.

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
