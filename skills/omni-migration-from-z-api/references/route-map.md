# Z-API routes on Z-API Omni

Read this after the inventory: one row per Z-API route the code calls. "Layer" is the compatibility layer at `https://zapi.omni.z-api.io/channels/{channelId}/token/{channelToken}`; "Native" is `https://api.omni.z-api.io`. Checked against the docs on 2026-10-19; if a page now says otherwise, the page wins.

Sources: the layer's [OpenAPI](https://developer.omni.z-api.io/pt/z-api/openapi.json) (16 routes), [reply message](https://developer.omni.z-api.io/z-api/messages/reply-message.md), [limitations of the official API](https://developer.omni.z-api.io/z-api/limitations.md), native [message types](https://developer.omni.z-api.io/messages/introduction.md).

## Sending

All layer routes keep the Z-API body and response (`zaapId`, `messageId`, `id`). On official WhatsApp they work only inside the 24-hour window ([messages in the layer](https://developer.omni.z-api.io/z-api/messages/introduction.md)).

| Z-API route | Layer | Native `content.type` (use `omni-messages`) |
|---|---|---|
| `POST /send-text` | Yes ([send text](https://developer.omni.z-api.io/z-api/messages/send-text.md)); `editMessageId` is listed there but editing is not supported (limitations) | `TEXT` |
| `POST /send-image` | Yes | `IMAGE` |
| `POST /send-audio` | Yes | `AUDIO` |
| `POST /send-video` | Yes | `VIDEO` |
| `POST /send-document/{extension}` | Yes | `DOCUMENT`, marked in development |
| `POST /send-sticker` | Yes | `STICKER` |
| `POST /send-link` | Yes | No link-preview type listed; send the link in a `TEXT` |
| `POST /send-contact` | Yes | `CONTACT` |
| `POST /send-reaction`, `POST /send-remove-reaction` | Yes | `REACTION`, marked in development |
| Reply (`messageId` in the body of a send) | Yes, on text, image, audio, video, document, sticker and contact ([reply message](https://developer.omni.z-api.io/z-api/messages/reply-message.md)); `privateAnswer` in groups is not supported | Not described for the native API |
| `POST /send-button-actions` | Yes | `INTERACTIVE_ACTION` (URL and call) |
| `POST /send-button-list` | Yes | `INTERACTIVE_BUTTON` (quick replies) |
| `POST /send-button-pix` | Yes | No native type listed |
| `POST /send-carousel` | Yes | No free-form type listed; carousels exist as templates (`omni-templates`) |
| `POST /send-catalog`, `POST /send-product` | Yes | `CATALOG`, `PRODUCT`, marked in development |
| `POST /send-location` | Not in the layer | `LOCATION` |
| `POST /send-poll` | Not supported on the official API | The QR code channel page says polls are supported, but no native poll page exists; do not invent a body |
| `POST /send-gif`, `POST /send-ptv`, `POST /forward-message`, `POST /pin-message`, `POST /send-event` | Not supported on the official API | None |
| `POST /send-button-otp` | Only as a template | `TEMPLATE` with the authentication model (`omni-templates`) |
| `DELETE /messages` | Not supported on the official API | None |
| `POST /read-message` | Not in the layer; not on the limitations page | Not described |

## Instance and connection

None of these are in the layer. Use the Omni panel or the native channel endpoints (`omni-core`).

| Z-API route | On Omni |
|---|---|
| `GET /status` | `GET /v1/channels/{channelId}`: check `phoneConnected` or `whatsappConnected` and `paymentStatus` ([get channel](https://developer.omni.z-api.io/channels/get-channel.md)) |
| `GET /qr-code`, `/qr-code/image`, `GET /phone-code/{phone}` | QR code channel: the connection SDK shows the QR code, or your own UI through `getQRCode` ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)). Official: Meta signup ([connect Meta WhatsApp](https://developer.omni.z-api.io/connect/meta-whatsapp.md)). No phone-code page |
| `GET /disconnect` | Documented only for `META_WHATSAPP` ([disconnect](https://developer.omni.z-api.io/channels/disconnect.md)) |
| `GET /restart`, instance settings (profile name, picture, auto-read, call rejection) | Not described |
| `POST /queue`, `DELETE /queue/{zaapId}` | Not described |

## Webhooks

| Z-API route | On Omni |
|---|---|
| `PUT /update-every-webhooks` and the per-event update routes | Layer: set the URL in the Omni dashboard. Native: `POST /v1/channels/{channelId}/webhooks` with `payloadFormat` `Z_API` to keep the Z-API payload ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)); ENTERPRISE role |

## Contacts, chats, groups, business, status, newsletters, communities, calls, privacy

Not supported on the official API, except some group and business-profile routes marked "in development". The full table, route by route, is on the [limitations](https://developer.omni.z-api.io/z-api/limitations.md) page. That page is about the official API; for a QR code channel the docs say nothing either way, so do not promise these routes there.

Includes `GET /phone-exists/{phone}`: not supported, so code that checked a number before sending needs another guard (for example, handle the failed status on the webhook).
