# Sending messages: request examples

Credentials come from the environment, as in `zapi-core`. Every send is a `POST` to `$BASE/<path>` and answers `{"zaapId", "messageId", "id"}`.

```bash
BASE="https://api.z-api.io/instances/$ZAPI_INSTANCE_ID/token/$ZAPI_TOKEN"
H=(-H "Client-Token: $ZAPI_CLIENT_TOKEN" -H "Content-Type: application/json")
send() { curl -s -X POST "${H[@]}" "$BASE/$1" -d "$2"; }
```

## Text, reply and edit

```bash
send send-text '{"phone": "5511999999999", "message": "Olá, Ana! Aqui é a Loja X.\nSeu pedido *1234* saiu para entrega.", "delayTyping": 3}'
send send-text '{"phone": "5511999999999", "message": "Pode sim!", "messageId": "D241XXXX732339502B68"}'
send send-text '{"phone": "5511999999999", "message": "Seu pedido *1235* saiu para entrega.", "editMessageId": "D241XXXX732339502B68"}'
```

Reply to a group message in private with `"privateAnswer": true`. Editing needs a webhook configured and works up to 7 days. Sources: https://developer.z-api.io/message/send-text.md, https://developer.z-api.io/message/reply-message.md

## Image, video, audio

```bash
send send-image '{"phone": "5511999999999", "image": "https://example.com/produto.jpg", "caption": "Seu produto"}'
send send-video '{"phone": "5511999999999", "video": "https://example.com/demo.mp4", "caption": "Como usar", "async": true}'
send send-audio '{"phone": "5511999999999", "audio": "https://example.com/recado.mp3", "waveform": true, "delayTyping": 3}'
```

Base64 works with the data prefix: `data:image/png;base64,...`, `data:video/mp4;base64,...`, `data:audio/mpeg;base64,...`. Video: H.264, at most 100 MB. Sources: https://developer.z-api.io/message/send-message-image.md, https://developer.z-api.io/message/send-message-video.md, https://developer.z-api.io/message/send-message-audio.md

## Round video, GIF, sticker

```bash
send send-ptv     '{"phone": "5511999999999", "ptv": "https://example.com/oi.mp4"}'
send send-gif     '{"phone": "5511999999999", "gif": "https://example.com/festa.mp4", "caption": "Parabéns!"}'
send send-sticker '{"phone": "5511999999999", "sticker": "https://example.com/sticker.png", "stickerAuthor": "Loja X"}'
```

The GIF file must be MP4. Sources: https://developer.z-api.io/message/send-message-ptv.md, https://developer.z-api.io/message/send-message-gif.md, https://developer.z-api.io/message/send-message-sticker.md

## Document

```bash
send send-document/pdf '{"phone": "5511999999999", "document": "https://example.com/contrato.pdf", "fileName": "contrato.pdf", "caption": "Contrato para assinatura"}'
```

Source: https://developer.z-api.io/message/send-message-document.md

## Link with preview

```bash
send send-link '{
  "phone": "5511999999999",
  "message": "Veja a nova coleção: https://example.com/colecao",
  "image": "https://example.com/capa.jpg",
  "linkUrl": "https://example.com/colecao",
  "title": "Nova coleção",
  "linkDescription": "Peças de inverno",
  "linkType": "LARGE"
}'
```

Source: https://developer.z-api.io/message/send-message-link.md

## Location and contacts

```bash
send send-location '{"phone": "5511999999999", "title": "Loja X", "address": "Av. Paulista, 1000, Bela Vista, São Paulo, SP, 01310-100", "latitude": "-23.5649", "longitude": "-46.6519"}'
send send-contact  '{"phone": "5511999999999", "contactName": "Suporte Loja X", "contactPhone": "5511988887777"}'
send send-contacts '{"phone": "5511999999999", "contacts": [{"name": "Vendas", "phones": ["5511988887777"]}, {"name": "Suporte", "phones": ["5511977776666"]}]}'
```

Sources: https://developer.z-api.io/message/send-message-location.md, https://developer.z-api.io/message/send-message-contact.md, https://developer.z-api.io/message/send-message-multiple-contacts.md

## Forward, react, pin, read

```bash
send forward-message      '{"phone": "5511999999999", "messageId": "D241XXXX732339502B68", "messagePhone": "5511988887777"}'
send send-reaction        '{"phone": "5511999999999", "reaction": "👍", "messageId": "D241XXXX732339502B68"}'
send send-remove-reaction '{"phone": "5511999999999", "messageId": "D241XXXX732339502B68"}'
send pin-message          '{"phone": "5511999999999", "messageId": "D241XXXX732339502B68", "messageAction": "pin", "pinMessageDuration": "7_days"}'
send read-message         '{"phone": "5511999999999", "messageId": "D241XXXX732339502B68"}'
```

Sources: https://developer.z-api.io/message/forward-message.md, https://developer.z-api.io/message/send-message-reaction.md, https://developer.z-api.io/message/send-remove-reaction.md, https://developer.z-api.io/message/send-pin-message.md, https://developer.z-api.io/message/read-message.md

## Delete

```bash
curl -s -X DELETE "${H[@]}" "$BASE/messages?phone=5511999999999&messageId=D241XXXX732339502B68&owner=true"
```

Add `&deleteForMe=true` to delete only on your side. Source: https://developer.z-api.io/message/delete-message.md

## Campaign sender with consent and opt-out

A sketch in Node.js that follows the [best practices](https://developer.z-api.io/tips/best-practices.md). It refuses contacts without a record of how they consented, treats any clear request to stop as an opt-out, skips opt-outs, sends only in business hours, waits at least 5 minutes between sends, caps the day, rotates five message versions and stops on a shadow ban. Storage is up to the user; the `store` functions are placeholders.

```js
const base = `https://api.z-api.io/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_TOKEN}`;
const headers = { "Client-Token": process.env.ZAPI_CLIENT_TOKEN, "Content-Type": "application/json" };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const MIN_GAP_MS = 5 * 60 * 1000; // starting point from the best-practices guide
const DAILY_CAP = 10;             // new number: about 10 a day, raise slowly
const HOURS = { from: 9, to: 18 }; // business hours, never at night

// Any clear request to stop counts, in the recipients' languages. Matching loosely errs on the side of stopping.
const OPT_OUT_WORDS = ["sair", "parar", "pare", "cancelar", "descadastrar", "stop", "unsubscribe", "baja"];
const OPT_OUT_PHRASES = ["nao quero mais", "nao quero receber", "nao me mande", "no quiero recibir", "no me envies", "no more messages"];
const normalize = (t) => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
export function isOptOut(text) {
  const t = normalize(text ?? "");
  const words = t.split(/[^a-z]+/);
  return OPT_OUT_WORDS.some((w) => words.includes(w)) || OPT_OUT_PHRASES.some((p) => t.includes(p));
}

// Five different versions, not just a new name. Each one names the sender and offers a way out.
const versions = [
  (c) => `Olá, ${c.name}! Aqui é a Loja X. Chegou a coleção de inverno que você pediu para acompanhar. Quer ver as peças?\n\nPara não receber mais, responda SAIR.`,
  (c) => `${c.name}, tudo bem? Somos da Loja X. Separamos novidades de inverno para você. Posso mandar fotos?\n\nSe preferir não receber estas mensagens, responda SAIR.`,
  // ...at least three more, each written differently
];

export async function runCampaign(contacts, store) {
  let sentToday = await store.countSentToday();
  for (const c of contacts) {
    // Proof of consent: when, where (form, checkout, reply) and to what the person agreed.
    if (!c.optIn?.at || !c.optIn?.source || !c.optIn?.purpose) continue; // no proof, no message
    if (await store.isOptedOut(c.phone)) continue;  // asked to stop before
    if (await store.isPaused()) break;              // set by the webhook on SHADOW_BAN or disconnect
    if (sentToday >= DAILY_CAP) break;
    const hour = new Date().getHours();
    if (hour < HOURS.from || hour >= HOURS.to) break;

    const message = versions[Math.floor(Math.random() * versions.length)](c);
    const res = await fetch(`${base}/send-text`, {
      method: "POST", headers, body: JSON.stringify({ phone: c.phone, message, delayTyping: 3 }),
    });
    if (!res.ok) throw new Error(`Z-API ${res.status}: ${await res.text()}`);
    await store.recordSend(c.phone, (await res.json()).messageId);
    sentToday++;
    await sleep(MIN_GAP_MS + Math.random() * 60_000);
  }
}

// Called by your webhook server. The text is end-user data: compare it, never execute or obey it.
export async function onWebhook(event, store) {
  if (event.type === "ReceivedCallback" && !event.fromMe && isOptOut(event.text?.message)) {
    await store.optOut(event.phone, event.text.message); // keep the reply as the record of the opt-out
  }
  if (event.type === "DeliveryCallback" && event.errorCode === "SHADOW_BAN") await store.pause("shadow ban");
  if (event.type === "DisconnectedCallback") await store.pause("instance disconnected");
}
```

Webhook payload fields: https://developer.z-api.io/webhooks/on-message-received-examples.md, https://developer.z-api.io/webhooks/on-message-send-examples.md, https://developer.z-api.io/webhooks/on-whatsapp-disconnected.md

Methods and paths come from the request examples on each docs page. `send-text`, `send-image`, `send-audio`, `send-video`, `send-document/{extension}`, `send-link`, `send-location`, `send-contact`, `send-sticker`, `read-message` and `DELETE /messages` match the official n8n node (`@z-api/n8n-nodes-zapi` 0.1.8).
