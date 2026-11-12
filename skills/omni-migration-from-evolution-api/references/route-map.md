# Evolution API routes and events on Z-API Omni

Read this after the inventory: one row per Evolution route, event or integration the code uses. The target is the native Omni API at `https://api.omni.z-api.io` on a `Z_API_WHATSAPP` (QR code) or `META_WHATSAPP` (official) channel. "Official API" below means `META_WHATSAPP`; for the QR code channel the docs list polls, location and contact as supported and say nothing either way about groups, status, edit, delete or forward, so do not promise those there ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)). Route names follow Evolution API v2; v1 code uses other bodies, so read the body in the code. Checked against the docs on 2026-11-04; if a page now says otherwise, the page wins.

Evolution sources: [send text](https://doc.evolution-api.com/v2/api-reference/message-controller/send-text), [send media](https://doc.evolution-api.com/v2/api-reference/message-controller/send-media), [create instance](https://doc.evolution-api.com/v2/api-reference/instance-controller/create-instance-basic), [set webhook](https://doc.evolution-api.com/v2/api-reference/webhook/set), [webhooks](https://doc.evolution-api.com/v2/en/configuration/webhooks). Routes without a link below are listed by name for the inventory; check their body in the user's code or in their server's API reference. Omni sources: [messages](https://developer.omni.z-api.io/messages/introduction.md), [message support](https://developer.omni.z-api.io/channels/message-support.md), [limitations of the official API](https://developer.omni.z-api.io/z-api/limitations.md), [payloads](https://developer.omni.z-api.io/webhooks/payloads.md).

## Sending

Every Omni row is `POST /v1/channels/{channelId}/messages` with `recipient.identifier` (digits with country code) and a `content` object. Bodies per type: `omni-messages`. On `META_WHATSAPP` every free-form type works only inside the 24-hour window; `Z_API_WHATSAPP` has no window.

| Evolution route | Omni `content.type` | Notes |
|---|---|---|
| `POST /message/sendText/{instance}` | `TEXT`, `body.message` | `delay`, `quoted`, `linkPreview`, `mentioned`, `mentionsEveryOne` are not described for the native API |
| `POST /message/sendMedia/{instance}`, `mediatype` `image` | `IMAGE`, `attachments[].url`, optional `caption` | Host base64 `media` and send the URL; `mimetype` and `fileName` have no field in the Omni image body |
| `POST /message/sendMedia/{instance}`, `mediatype` `video` | `VIDEO`, `attachments[].url`, optional `caption` | |
| `POST /message/sendMedia/{instance}`, `mediatype` `document` | `DOCUMENT`, marked in development | Until it is available, send a link in a `TEXT` |
| `POST /message/sendWhatsAppAudio/{instance}` | `AUDIO`, `attachments[].url` | |
| `POST /message/sendSticker/{instance}` | `STICKER`, WebP URL | |
| `POST /message/sendLocation/{instance}` | `LOCATION`, `latitude` and `longitude` as strings | |
| `POST /message/sendContact/{instance}` | `CONTACT`, `name` and `phones[]` | One attachment per contact |
| `POST /message/sendReaction/{instance}` | `REACTION`, marked in development | |
| `POST /message/sendList/{instance}` | `INTERACTIVE_LIST`, marked in development | Up to 3 options fit `INTERACTIVE_BUTTON` |
| `POST /message/sendButtons/{instance}` | `INTERACTIVE_BUTTON` (up to 3 replies) or `INTERACTIVE_ACTION` (link and call) | |
| `POST /message/sendTemplate/{instance}` (`WHATSAPP-BUSINESS`) | `TEMPLATE` | `omni-templates`; the template must be approved on the WABA Omni connects |
| `POST /message/sendPoll/{instance}` | None documented | Not supported on the official API. The QR code channel page says polls are supported, but no native poll body is documented: do not invent one |
| `POST /message/sendStatus/{instance}` | None | |
| Any send to a `@g.us` chat | None | Groups are not supported on the official API and not documented for the QR code channel |
| First message to a customer who has not written in 24 hours | `META_WHATSAPP`: `TEMPLATE`; `Z_API_WHATSAPP`: any type | Meta charges templates |

## Chat, group, profile, label, call

| Evolution route | On Omni |
|---|---|
| `POST /chat/whatsappNumbers/{instance}` | None; handle a failed status on the webhook instead |
| `POST /chat/markMessageAsRead/{instance}`, `POST /chat/sendPresence/{instance}` | None described |
| `DELETE /chat/deleteMessageForEveryone/{instance}`, `POST /chat/updateMessage/{instance}` | None: delete and edit are not supported on the official API and have no native route on the QR code channel |
| `POST /chat/findMessages`, `findChats`, `findContacts`, `fetchProfilePictureUrl`, `archiveChat` | None: keep your own message store from the webhook |
| `/group/*`, `/profile/*`, `/label/*`, `/call/*`, `/settings/set` | Not supported on the official API ([limitations](https://developer.omni.z-api.io/z-api/limitations.md)); no native route on the QR code channel |

## Instances and connection

The channel replaces the instance.

| Evolution route | On Omni |
|---|---|
| `POST /instance/create` | `POST /v1/channels` with `name` and `type` `Z_API_WHATSAPP` or `META_WHATSAPP` ([create channel](https://developer.omni.z-api.io/channels/create-channel.md)), then connect through the connection SDK (`omni-onboarding`) |
| `GET /instance/connect/{instance}` (QR code, pairing code) | QR code channel: the connection SDK with your `getQRCode` backend route ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)); no pairing-code page. Official: Meta's Embedded Signup ([connect channels](https://developer.omni.z-api.io/connect/introduction.md)) |
| `GET /instance/connectionState/{instance}` (`open`, `close`, `connecting`) | `GET /v1/channels/{channelId}`: `phoneConnected`, `whatsappConnected`, `paymentStatus` ([get channel](https://developer.omni.z-api.io/channels/get-channel.md)) |
| `GET /instance/fetchInstances` | `GET /v1/channels`; needs the ENTERPRISE role ([list channels](https://developer.omni.z-api.io/channels/list-channels.md)) |
| `PUT /instance/restart/{instance}` | None |
| `DELETE /instance/logout/{instance}` | Disconnect, documented for `META_WHATSAPP` ([disconnect](https://developer.omni.z-api.io/channels/disconnect.md)); for the QR code channel, remove the linked device on the phone or use the panel |
| `DELETE /instance/delete/{instance}` | Delete channel ([delete channel](https://developer.omni.z-api.io/channels/delete-channel.md)) |

## Webhook configuration

| Evolution | Omni |
|---|---|
| `POST /webhook/set/{instance}` | `POST /v1/channels/{channelId}/webhooks` ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)) |
| `GET /webhook/find/{instance}` | `GET /v1/channels/{channelId}/webhooks` ([list webhooks](https://developer.omni.z-api.io/webhooks/list-webhooks.md)) |
| `enabled: false` | Update the webhook `status` ([update webhook](https://developer.omni.z-api.io/webhooks/update-webhook.md)) or delete it |
| `events` (`MESSAGES_UPSERT`, ...) | `events` (see the event table in SKILL.md) |
| `webhookByEvents` | One `url` per webhook; create several webhooks if routing was by path |
| `webhookBase64` | None: media comes as `url` |
| Custom headers, `jwt_key` | `auth` with `type` `BEARER`, `API_KEY`, `BASIC` or `CUSTOM_HEADER`, plus `signing: true` |
| `WEBHOOK_GLOBAL_URL` and the other `WEBHOOK_GLOBAL_*` / `WEBHOOK_EVENTS_*` variables | Default webhooks for the account ([default webhooks](https://developer.omni.z-api.io/webhooks/default-webhooks.md)), or one webhook per channel |
| RabbitMQ, SQS, WebSocket | None: webhook only |

## Message payload

Evolution `messages.upsert` to Omni `DEFAULT` format, `messageEventType` `NEW_MESSAGE`.

| Evolution | Omni |
|---|---|
| `event` (`messages.upsert`) | `messageEventType`; the event type is the one the webhook subscribed to |
| `instance` | `message.channel_id` |
| `data.key.id` | `message._id` (32-character hex, equal to the send response `messageId`) |
| `data.key.remoteJid` (`...@s.whatsapp.net`) | `message.sender.identifier` (digits) on a received message |
| `data.key.fromMe` | `message.metadata.from_me` |
| `data.pushName` | `message.sender.name` |
| `data.message.conversation`, `data.message.extendedTextMessage.text` | `message.contents[0].message` when `contents[0].type` is `TEXT` |
| `data.message.imageMessage`, `videoMessage`, `audioMessage`, `documentMessage`, `stickerMessage` | `message.attachments[]` with `type`, `url`, `thumbnail_url`, `caption` |
| `data.messageType` | `contents[].type` or `attachments[].type` |
| `data.messageTimestamp` (seconds) | `message.created` (epoch milliseconds); `message.metadata.moment` for ordering |
| `data.status` | `state_items[].state.name` on each content or attachment item; only `PENDING` is documented |
| `date_time`, `server_url`, `sender`, `destination` | None; delivery headers carry `x-webhook-delivery-id`, `x-webhook-event-id`, `x-webhook-attempt` ([delivery](https://developer.omni.z-api.io/webhooks/delivery.md)) |
| `apikey` | None. Never authenticate on a body field; verify `x-webhook-signature` |

If the handler cannot be rewritten yet, `payloadFormat` `Z_API` sends the classic Z-API structure instead ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)); that is still a rewrite from the Evolution shape, so prefer `DEFAULT`.
