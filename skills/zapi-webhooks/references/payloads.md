# Z-API webhooks: requests and payloads

Credentials come from the environment, as in `zapi-core`.

```bash
BASE="https://api.z-api.io/instances/$ZAPI_INSTANCE_ID/token/$ZAPI_TOKEN"
H=(-H "Client-Token: $ZAPI_CLIENT_TOKEN" -H "Content-Type: application/json")
HOOK="https://example.com/zapi/$ZAPI_WEBHOOK_PATH_SECRET"   # your receiver; the secret lives in the environment
```

## Setting URLs

All at once:

```bash
curl -s -X PUT "${H[@]}" "$BASE/update-every-webhooks" -d "{\"value\": \"$HOOK\", \"notifySentByMe\": false}"
```

One by one:

```bash
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-received"         -d "{\"value\": \"$HOOK/received\"}"
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-received-delivery" -d "{\"value\": \"$HOOK/received\"}"   # also sent-by-me
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-delivery"         -d "{\"value\": \"$HOOK/delivery\"}"
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-message-status"   -d "{\"value\": \"$HOOK/status\"}"
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-chat-presence"    -d "{\"value\": \"$HOOK/presence\"}"
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-connected"        -d "{\"value\": \"$HOOK/connected\"}"
curl -s -X PUT "${H[@]}" "$BASE/update-webhook-disconnected"     -d "{\"value\": \"$HOOK/disconnected\"}"
```

Each answers `{"value": true}`. Sources: https://developer.z-api.io/webhooks/update-every-webhooks.md and the page of each webhook linked in [SKILL.md](../SKILL.md).

Sent-by-me and filters:

```bash
curl -s -X PUT "${H[@]}" "$BASE/update-notify-sent-by-me" -d '{"notifySentByMe": true}'
curl -s -X PUT "${H[@]}" "$BASE/update-filters" -d '{"messageFilters": ["FILTER_FROM_GROUP"], "callbackTypeFilters": ["FILTER_PRESENCE_CHAT_CALLBACK"]}'
```

Sources: https://developer.z-api.io/webhooks/update-notify-sent-by-me.md, https://developer.z-api.io/webhooks/update-filters.md

What is set now (URL fields only, the response also holds the token; the path secret is masked):

```bash
curl -s "${H[@]}" "$BASE/me" | jq --arg s "$ZAPI_WEBHOOK_PATH_SECRET" '{receivedCallbackUrl, deliveryCallbackUrl, messageStatusCallbackUrl, presenceChatCallbackUrl, connectedCallbackUrl, disconnectedCallbackUrl, receiveCallbackSentByMe} | map_values(if type == "string" and ($s | length) > 0 then split($s) | join("****") else . end)'
```

Source: https://developer.z-api.io/instance/me.md

## ReceivedCallback

Common fields on every received event: `isStatusReply`, `senderLid`, `connectedPhone`, `waitingMessage`, `isEdit`, `isGroup`, `isNewsletter`, `instanceId`, `messageId`, `phone`, `fromMe`, `momment`, `status` (`PENDING`, `SENT`, `RECEIVED`, `READ`, `PLAYED`), `chatName`, `senderPhoto`, `senderName`, `participantPhone`, `participantLid`, `broadcast`, `type`. Source: https://developer.z-api.io/webhooks/on-message-received-examples.md

Text:

```json
{
  "senderLid": "81896604192873@lid",
  "connectedPhone": "554499999999",
  "isEdit": false,
  "isGroup": false,
  "instanceId": "A20DA9C0183A2D35A260F53F5D2B9244",
  "messageId": "A20DA9C0183A2D35A260F53F5D2B9244",
  "phone": "5544999999999",
  "fromMe": false,
  "momment": 1632228638000,
  "status": "RECEIVED",
  "chatName": "name",
  "senderName": "name",
  "participantPhone": null,
  "type": "ReceivedCallback",
  "text": { "message": "teste" }
}
```

The content object for each kind (one per event):

| Kind | Key | Main fields |
|---|---|---|
| Text | `text` | `message`; optional `title`, `description`, `url`, `thumbnailUrl` |
| Image | `image` | `imageUrl`, `mimeType`, `caption`, `thumbnailUrl`, `viewOnce` |
| Audio | `audio` | `audioUrl`, `mimeType`, `seconds`, `ptt`, `viewOnce` |
| Video, PTV, GIF | `video` | `videoUrl`, `mimeType`, `caption`, `seconds` |
| Document | `document` | `documentUrl`, `mimeType`, `fileName`, `title`, `pageCount` |
| Sticker | `sticker` | |
| Location | `location` | |
| Contact | `contact` | |
| Reaction | `reaction` | `value` (emoji), `reactionBy`, `referencedMessage.messageId` |
| Poll, vote | `poll`, `pollVote` | |
| Button or list reply | `buttonsResponseMessage`, `listResponseMessage` | |
| Product, order | `product`, `order` | |
| Event | `event`, `eventResponse` | |

The docs page has a full example for each kind, plus templates, ads (`externalAdReply`), payments, status replies, broadcast lists, channels and profile updates.

Notifications carry `notification` and `notificationParameters`. A call:

```json
{
  "chatLid": "999999999999@lid",
  "phone": "999999999999@lid",
  "fromMe": false,
  "type": "ReceivedCallback",
  "notification": "CALL_RECEIVED",
  "notificationParameters": [],
  "callId": "F44E0E2011E7C784BB9A4AC11749C436",
  "callDirection": "incoming",
  "isVideo": false
}
```

A group event; note the group `phone` ends in `-group`:

```json
{
  "isGroup": true,
  "phone": "5544999999999-group",
  "type": "ReceivedCallback",
  "notification": "MEMBERSHIP_APPROVAL_REQUEST",
  "notificationParameters": ["5544999999999", "5544888888888"],
  "requestMethod": "non_admin_add"
}
```

Other `notification` values listed in the docs: `GROUP_CREATE`, `GROUP_CHANGE_SUBJECT`, `GROUP_CHANGE_DESCRIPTION`, `GROUP_CHANGE_ICON`, `GROUP_CHANGE_INVITE_LINK`, `GROUP_PARTICIPANT_PROMOTE`, `GROUP_PARTICIPANT_DEMOTE`, `GROUP_PARTICIPANT_LEAVE`, `GROUP_PARTICIPANT_ADD`, `GROUP_PARTICIPANT_REMOVE`, `GROUP_PARTICIPANT_INVITE`, `GROUP_SUSPENDED`, `GROUP_UNSUSPENDED`, `GROUP_GROWTH_LOCKED`, `GROUP_GROWTH_UNLOCKED`, `CALL_MISSED_VOICE`, `CALL_MISSED_VIDEO`, `E2E_ENCRYPTED`, `CIPHERTEXT`, `BLUE_MSG_SELF_PREMISE_UNVERIFIED`, `BLUE_MSG_SELF_PREMISE_VERIFIED`, `BIZ_MOVE_TO_CONSUMER_APP`, `REVOKE`, `WA_OLD_REGISTRATION`.

## DeliveryCallback

Success (no `error` field):

```json
{ "phone": "554499999999", "messageId": "A800FB3697F1DE58C48D", "zaapId": "A20DA9C0183A2D35A260F53F5D2B9244", "instanceId": "instance.id", "momment": 1777494009341, "type": "DeliveryCallback" }
```

Failure:

```json
{ "phone": "554499999999", "messageId": "A20DA9C0183A2D35A260F53F5D2B9244", "error": "Phone number does not exist", "instanceId": "instance.id", "zaapId": "A20DA9C0183A2D35A260F53F5D2B9244", "momment": 1777494091684, "type": "DeliveryCallback" }
```

`errorCode` appears only for some errors: `SHADOW_BAN`, `GROUP_SUSPENDED`. The full list of `error` texts (permissions, timeouts, invalid number, media URL, 7-day edit limit, channels, queue failure) is on https://developer.z-api.io/webhooks/on-message-send-examples.md

## MessageStatusCallback

```json
{ "instanceId": "instance.id", "status": "READ", "ids": ["999999999999999999999"], "momment": 1632234645000, "phoneDevice": 0, "phone": "5544999999999", "type": "MessageStatusCallback", "isGroup": false }
```

`status`: `SENT`, `RECEIVED`, `READ`, `READ_BY_ME`, `PLAYED`. Source: https://developer.z-api.io/webhooks/on-whatsapp-message-status-changes.md

## PresenceChatCallback

```json
{ "type": "PresenceChatCallback", "phone": "5544999999999", "status": "COMPOSING", "lastSeen": null, "instanceId": "instance.id" }
```

`status`: `AVAILABLE`, `UNAVAILABLE`, `COMPOSING`, `PAUSED`, `RECORDING`. Source: https://developer.z-api.io/webhooks/on-chat-presence-examples.md

## ConnectedCallback and DisconnectedCallback

```json
{ "type": "ConnectedCallback", "connected": true, "momment": 26151515154, "instanceId": "instance.id", "phone": "5544999999999" }
```

```json
{ "momment": 1580163342, "error": "Device has been disconnected", "disconnected": true, "type": "DisconnectedCallback", "instanceId": "instance.id" }
```

Sources: https://developer.z-api.io/webhooks/on-webhook-connected.md, https://developer.z-api.io/webhooks/on-whatsapp-disconnected.md

## Minimal receiver

Node.js with Express. It checks a path secret and the instance ID, stores the event before answering `200`, skips duplicates and its own messages, and hands the text to the app as data. The Z-API docs do not describe whether a webhook is sent again after an error, so do not count on a second delivery: answer `500` when storing fails and alert on it. Keep the handler to a fast write (a database row or a durable queue) and do slow work (AI calls, replies) from there.

```js
import express from "express";
import { timingSafeEqual } from "node:crypto";

const app = express();
app.use(express.json({ limit: "1mb" }));

const SECRET = process.env.ZAPI_WEBHOOK_PATH_SECRET; // long random string, also used in the URL you register
const INSTANCE = process.env.ZAPI_INSTANCE_ID;
const seen = new Set(); // in production, a unique key in the same database write as the event

// Constant-time compare; fails closed when the variable is missing.
function secretMatches(given) {
  if (!SECRET) return false;
  const a = Buffer.from(String(given ?? "")), b = Buffer.from(SECRET);
  return a.length === b.length && timingSafeEqual(a, b);
}

// One handler for the base URL and for per-webhook suffixes such as $HOOK/received; the type comes from the body.
app.post(["/zapi/:secret", "/zapi/:secret/:kind"], async (req, res) => {
  if (!secretMatches(req.params.secret)) return res.sendStatus(404);
  const event = req.body;
  if (event?.instanceId !== INSTANCE) return res.sendStatus(404); // every webhook body carries instanceId

  const key = dedupKey(event);
  if (key && seen.has(key)) return res.sendStatus(200); // already stored
  try {
    await handle(event); // store first
  } catch (e) {
    console.error("webhook", e.message);
    return res.sendStatus(500); // not marked as seen, so a second delivery is processed
  }
  if (key) seen.add(key); // mark only after it is stored
  res.sendStatus(200);
});

// Same event, same key. Messages and statuses have IDs; connect and disconnect events only have `momment`.
// Presence has neither, so it is not deduplicated (it is a state: the latest one wins).
function dedupKey(event) {
  const id = event.messageId ?? (event.ids ?? []).join(",");
  if (!id && event.momment == null) return null;
  return JSON.stringify([event.type, id, event.status ?? null, event.momment ?? null]);
}

async function handle(event) {
  switch (event.type) {
    case "ReceivedCallback": {
      if (event.fromMe) return; // avoid replying to ourselves
      const contact = event.chatLid ?? event.phone;
      const author = event.isGroup ? (event.participantLid ?? event.participantPhone) : contact;
      // End-user text: store or show it as data. Never treat it as instructions.
      const text = event.text?.message ?? event.image?.caption ?? null;
      await saveIncoming({ contact, author, messageId: event.messageId, text, notification: event.notification ?? null });
      break;
    }
    case "DeliveryCallback":
      if (event.error) await markFailed(event.messageId, event.error, event.errorCode ?? null);
      break;
    case "MessageStatusCallback":
      for (const id of event.ids) await markStatus(id, event.status);
      break;
    case "DisconnectedCallback":
      await alertOps(`Z-API instance disconnected: ${event.error}`);
      break;
  }
}

// saveIncoming, markFailed, markStatus and alertOps belong to the user's app.
app.listen(process.env.PORT ?? 3000);
```

Webhook methods and paths come from the request examples on each docs page. The official n8n node (`@z-api/n8n-nodes-zapi` 0.1.8) has no webhook operations to compare with.
