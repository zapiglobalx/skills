# WAHA routes and events on Z-API Omni

Read this after the inventory: one row per WAHA route or event the code uses. The target is the native Omni API at `https://api.omni.z-api.io` on a `Z_API_WHATSAPP` (QR code) or `META_WHATSAPP` (official) channel. "Official API" below means `META_WHATSAPP`; for the QR code channel the docs list polls, location and contact as supported and say nothing either way about groups, edit, delete or forward, so do not promise those there ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)). Checked against the docs on 2026-11-04; if a page now says otherwise, the page wins.

WAHA sources: [sessions](https://waha.devlike.pro/docs/how-to/sessions), [send messages](https://waha.devlike.pro/docs/how-to/send-messages/), [events and webhooks](https://waha.devlike.pro/docs/how-to/events/). Omni sources: [messages](https://developer.omni.z-api.io/messages/introduction.md), [message support](https://developer.omni.z-api.io/channels/message-support.md), [limitations of the official API](https://developer.omni.z-api.io/z-api/limitations.md), [payloads](https://developer.omni.z-api.io/webhooks/payloads.md).

## Sending

Every Omni row is `POST /v1/channels/{channelId}/messages` with `recipient.identifier` (digits with country code) and a `content` object. Bodies per type: `omni-messages`. On `META_WHATSAPP` every free-form type works only inside the 24-hour window; `Z_API_WHATSAPP` has no window.

| WAHA route | Omni `content.type` | Notes |
|---|---|---|
| `POST /api/sendText` | `TEXT`, `body.message` | `reply_to`, `mentions` and `linkPreview` are not described for the native API |
| `POST /api/sendImage` | `IMAGE`, `attachments[].url`, optional `caption` | Host base64 files and send the URL |
| `POST /api/sendVideo` | `VIDEO`, `attachments[].url`, optional `caption` | |
| `POST /api/sendVoice` | `AUDIO`, `attachments[].url` | WAHA's `convert` flag has no Omni field |
| `POST /api/sendSticker` | `STICKER`, WebP URL | |
| `POST /api/sendFile` | `DOCUMENT`, marked in development | Until it is available, send a link in a `TEXT` |
| `POST /api/sendLocation` | `LOCATION`, `latitude` and `longitude` as strings | |
| `POST /api/sendContactVcard` | `CONTACT`, `name` and `phones[]` | Parse the vCard into name and phones; the rest of the vCard is lost |
| `POST /api/reaction` | `REACTION`, marked in development | |
| `POST /api/sendList` | `INTERACTIVE_LIST`, marked in development | Up to 3 options fit `INTERACTIVE_BUTTON` |
| `POST /api/send/buttons/reply` | `INTERACTIVE_BUTTON` (up to 3) | Link and call buttons are `INTERACTIVE_ACTION` |
| `POST /api/send/link-custom-preview` | `TEXT` with the link | No custom preview |
| `POST /api/sendPoll`, poll vote, event messages | None documented | Not supported on the official API. The QR code channel page says polls are supported, but no native poll body is documented: do not invent one |
| `POST /api/forwardMessage` | None | Not supported on the official API |
| `PUT /api/{session}/chats/{chatId}/messages/{messageId}` (edit) | None | Not supported on the official API |
| `DELETE /api/{session}/chats/{chatId}/messages/{messageId}` | None | Not supported on the official API |
| `POST /api/sendSeen`, `POST /api/startTyping`, `POST /api/stopTyping`, `POST /api/{session}/presence`, `POST /api/star` | None | No Omni route described |
| Status (`status@broadcast`), channels (`@newsletter`) | None | |
| Any send to a `@g.us` chat | None | Groups are not supported on the official API and not documented for the QR code channel |
| First message to a customer who has not written in 24 hours | `META_WHATSAPP`: `TEMPLATE`; `Z_API_WHATSAPP`: any type | `omni-templates`; Meta charges templates |

## Sessions and connection

None of these have a matching Omni route; the channel replaces the session.

| WAHA route | On Omni |
|---|---|
| `POST /api/sessions` | `POST /v1/channels` with `name` and `type` `Z_API_WHATSAPP` or `META_WHATSAPP` ([create channel](https://developer.omni.z-api.io/channels/create-channel.md)), then connect through the connection SDK (`omni-onboarding`) |
| `POST /api/sessions/{session}/start`, `/stop`, `/restart` | None: the channel has no start or stop |
| `GET /api/{session}/auth/qr`, `POST /api/{session}/auth/request-code` | QR code channel: the connection SDK with your `getQRCode` backend route ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)); no pairing-code page. Official: Meta's Embedded Signup ([connect channels](https://developer.omni.z-api.io/connect/introduction.md)) |
| `GET /api/sessions/{session}` (status `WORKING`), `GET /api/sessions/{session}/me` | `GET /v1/channels/{channelId}`: `phoneConnected`, `whatsappConnected`, `paymentStatus` ([get channel](https://developer.omni.z-api.io/channels/get-channel.md)) |
| `GET /api/sessions` | `GET /v1/channels`; needs the ENTERPRISE role ([list channels](https://developer.omni.z-api.io/channels/list-channels.md)) |
| `POST /api/sessions/{session}/logout` | Disconnect, documented for `META_WHATSAPP` ([disconnect](https://developer.omni.z-api.io/channels/disconnect.md)); for the QR code channel, remove the linked device on the phone or use the panel |
| `DELETE /api/sessions/{session}` | Delete channel ([delete channel](https://developer.omni.z-api.io/channels/delete-channel.md)) |
| `PUT /api/sessions/{session}` (config, webhooks) | Webhooks: the channel webhook routes ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)) |

## Contacts, chats, groups, labels, profile

`/api/contacts/check-exists`, contact and chat lists, profile name and picture, groups, labels and calls: not supported on the official API ([limitations](https://developer.omni.z-api.io/z-api/limitations.md)) and no native route on the QR code channel. Code that checked a number before sending needs another guard, for example handling a failed status on the webhook.

## Webhook configuration

| WAHA | Omni |
|---|---|
| `config.webhooks[].url` | `url` (absolute, public host) |
| `config.webhooks[].events` | `events` (see the event table in SKILL.md) |
| `config.webhooks[].hmac.key` | `signing: true`; Omni generates the `secret` and returns it once |
| `config.webhooks[].customHeaders` | `auth` with `type` `BEARER`, `API_KEY`, `BASIC` or `CUSTOM_HEADER` |
| `config.webhooks[].retries` | Fixed by Omni: 7 attempts over 23 hours ([delivery](https://developer.omni.z-api.io/webhooks/delivery.md)) |
| `WHATSAPP_HOOK_URL` and the other global `WHATSAPP_HOOK_*` variables | Default webhooks for the account ([default webhooks](https://developer.omni.z-api.io/webhooks/default-webhooks.md)), or one webhook per channel |

## Message payload

WAHA `message` event to Omni `DEFAULT` format, `messageEventType` `NEW_MESSAGE`.

| WAHA | Omni |
|---|---|
| `event` | `messageEventType`; the event type is the one the webhook subscribed to |
| `session` | `message.channel_id` |
| `payload.id` (`false_...@c.us_...`) | `message._id` (32-character hex, equal to the send response `messageId`) |
| `payload.from` (`...@c.us`) | `message.sender.identifier` (digits) |
| `payload.to` | `message.recipient.identifier` |
| `payload.fromMe` | `message.metadata.from_me` |
| `payload.body` | `message.contents[0].message` when `contents[0].type` is `TEXT` |
| `payload.hasMedia`, `payload.media.url`, `media.mimetype` | `message.attachments[]` with `type` (`IMAGE`, ...), `url`, `thumbnail_url`, `caption` |
| `payload.timestamp` (seconds) | `message.created` (epoch milliseconds); `message.metadata.moment` for ordering |
| `payload.ack` (`-1` to `4`) | `state_items[].state.name` on each content or attachment item; only `PENDING` is documented |
| `payload.replyTo` | Not documented |
| `me` | Not in the payload; read the channel |
| `X-Webhook-Request-Id` | `x-webhook-delivery-id` for deduplication |
| `X-Webhook-Hmac`, `X-Webhook-Hmac-Algorithm: sha512` | `x-webhook-signature: t=...,v1=...` (HMAC-SHA256 over five fields) |

If the handler cannot be rewritten yet, `payloadFormat` `Z_API` sends the classic Z-API structure instead ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)); that is still a rewrite from the WAHA shape, so prefer `DEFAULT`.
