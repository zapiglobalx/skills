# Z-API routes on Z-API Omni

Read this after the inventory: one row per Z-API route the code calls. Every Omni row is the native API at `https://api.omni.z-api.io`. Checked against the docs on 2026-11-12; if a page now says otherwise, the page wins.

Sources: native [message types](https://developer.omni.z-api.io/messages/introduction.md), [message support](https://developer.omni.z-api.io/channels/message-support.md) (what each channel accepts, with a WhatsApp Web column for the QR code channel), [create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md). The Z-API compatibility-layer pages (`z-api/...`) and the Z-API limitations page are no longer in the Omni docs: do not cite them.

## Sending

Every row is `POST /v1/channels/{channelId}/messages` with `recipient.identifier` (digits with country code) and a `content` object; the response is `{"messageId": "..."}` instead of Z-API's `zaapId`, `messageId` and `id`. Bodies per type: `omni-messages`. On `META_WHATSAPP` every free-form type works only inside the 24-hour window; `Z_API_WHATSAPP` has no window.

| Z-API route | Native `content.type` | Notes |
|---|---|---|
| `POST /send-text` | `TEXT`, `body.message` | `editMessageId` has no native field; no edit route is documented |
| `POST /send-image` | `IMAGE`, `attachments[].url`, optional `caption` | Host base64 images and send the URL |
| `POST /send-audio` | `AUDIO`, `attachments[].url` | |
| `POST /send-video` | `VIDEO`, `attachments[].url`, optional `caption` | |
| `POST /send-document/{extension}` | `DOCUMENT`, marked in development | Until it is available, send a link in a `TEXT` |
| `POST /send-sticker` | `STICKER`, WebP URL | |
| `POST /send-link` | `TEXT` with the link | No link-preview type listed |
| `POST /send-location` | `LOCATION`, `latitude` and `longitude` as strings | |
| `POST /send-contact` | `CONTACT`, `name` and `phones[]` | |
| `POST /send-reaction`, `POST /send-remove-reaction` | `REACTION`, marked in development | |
| Reply (`messageId` in the body of a send) | Not described for the native API | Drop it and say so |
| `POST /send-button-actions` | `INTERACTIVE_ACTION` (URL and call) | |
| `POST /send-button-list` | `INTERACTIVE_BUTTON` (up to 3 quick replies) | Longer lists: `INTERACTIVE_LIST`, marked in development |
| `POST /send-button-pix` | None listed | |
| `POST /send-carousel` | No free-form type; carousels exist as templates (`omni-templates`) | |
| `POST /send-catalog`, `POST /send-product` | `CATALOG`, `PRODUCT`, marked in development | |
| `POST /send-poll` | None documented | Not supported on `META_WHATSAPP`; the QR code channel supports polls ([message support](https://developer.omni.z-api.io/channels/message-support.md)), but no native poll body is documented: do not invent one |
| `POST /send-button-otp` | `TEMPLATE` with the authentication model (`omni-templates`) | Official only |
| `DELETE /messages` | None | The API cannot delete a sent message on any channel ([message support](https://developer.omni.z-api.io/channels/message-support.md)) |
| `POST /send-gif`, `POST /send-ptv`, `POST /forward-message`, `POST /pin-message`, `POST /send-event`, `POST /read-message` | None | No native route documented |
| First message to a customer who has not written in 24 hours | `META_WHATSAPP`: `TEMPLATE`; `Z_API_WHATSAPP`: any type | Meta charges templates |

## Instance and connection

The channel replaces the instance. Use the Omni panel or the native channel endpoints (`omni-core`, `omni-onboarding`).

| Z-API route | On Omni |
|---|---|
| `GET /status` | `GET /v1/channels/{channelId}`: check `phoneConnected` or `whatsappConnected` and `paymentStatus` ([get channel](https://developer.omni.z-api.io/channels/get-channel.md)) |
| `GET /qr-code`, `/qr-code/image`, `GET /phone-code/{phone}` | QR code channel: the connection SDK with your `getQRCode` backend route ([connect WhatsApp Web](https://developer.omni.z-api.io/connect/whatsapp-web.md)). Official: Meta signup ([connect Meta WhatsApp](https://developer.omni.z-api.io/connect/meta-whatsapp.md)). No phone-code page |
| `GET /disconnect` | Documented only for `META_WHATSAPP` ([disconnect](https://developer.omni.z-api.io/channels/disconnect.md)) |
| `GET /restart`, instance settings (profile name, picture, auto-read, call rejection) | Not described |
| `POST /queue`, `DELETE /queue/{zaapId}` | Not described |

## Webhooks

| Z-API route | On Omni |
|---|---|
| `PUT /update-every-webhooks` and the per-event update routes | `POST /v1/channels/{channelId}/webhooks` with `payloadFormat` `Z_API` to keep the Z-API payload ([create webhook](https://developer.omni.z-api.io/webhooks/create-webhook.md)) |

## Contacts, chats, groups, business, status, newsletters, communities, calls, privacy

No native route is documented for any of these on either channel. [Message support](https://developer.omni.z-api.io/channels/message-support.md) does not mention groups; do not promise them.

Includes `GET /phone-exists/{phone}`: no equivalent, so code that checked a number before sending needs another guard (for example, handle the failed status on the webhook).
