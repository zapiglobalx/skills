# Z-API instance: request examples

Credentials come from the environment, as in `zapi-core`. `BASE` is the instance base URL.

```bash
BASE="https://api.z-api.io/instances/$ZAPI_INSTANCE_ID/token/$ZAPI_TOKEN"
H=(-H "Client-Token: $ZAPI_CLIENT_TOKEN" -H "Content-Type: application/json")
```

## Status

```bash
curl -s "${H[@]}" "$BASE/status"
```

```json
{ "connected": false, "error": "You are not connected", "smartphoneConnected": false }
```

Source: https://developer.z-api.io/instance/status.md

## QR code as image

```bash
curl -s "${H[@]}" "$BASE/qr-code/image"
```

Either the image, ready for `<img src="...">`:

```json
{ "value": "data:image/png;base64,iVBOR..." }
```

or, when WhatsApp asks for a passkey, a challenge:

```json
{
  "challenge": {
    "allowCredentials": [],
    "challenge": "V275tRcRUu2XjHiF9a6GTKFaZj8G4W_EEuRwdW5zCAM",
    "extensions": { "uvm": true },
    "rpId": "whatsapp.com",
    "timeout": 600000,
    "userVerification": "required"
  }
}
```

Sources: https://developer.z-api.io/instance/qr-code-image.md, https://developer.z-api.io/instance/qr-code.md

## Phone code

```bash
curl -s "${H[@]}" "$BASE/phone-code/5511999999999"
```

```json
{ "value": "A1B2C3D4E5" }
```

The same `challenge` object can come back instead. Source: https://developer.z-api.io/instance/phone-code.md

## QR polling loop (Node.js, server side)

Follows the docs' advice: a new code every 10 to 20 seconds, stop after 3 tries ([get QR code](https://developer.z-api.io/instance/qrcode.md)).

```js
const base = `https://api.z-api.io/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_TOKEN}`;
const headers = { "Client-Token": process.env.ZAPI_CLIENT_TOKEN };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function pairByQr(showQr, { tries = 3, intervalMs = 15000 } = {}) {
  for (let i = 0; i < tries; i++) {
    const status = await (await fetch(`${base}/status`, { headers })).json();
    if (status.connected) return { connected: true };
    const qr = await (await fetch(`${base}/qr-code/image`, { headers })).json();
    if (qr.challenge) return { challenge: qr.challenge }; // passkey needed: use the Z-API Conector
    showQr(qr.value); // send only the image to the browser, never the base URL
    await sleep(intervalMs);
  }
  return { connected: false, expired: true }; // show a "new QR code" button
}
```

## Extension token

```bash
curl -s "${H[@]}" "$BASE/extension-token"
```

```json
{ "token": "FA48-HS63", "expiresAt": 1782851138085 }
```

`expiresAt` is Unix time in milliseconds; the code lasts up to 5 minutes. Source: https://developer.z-api.io/instance/extension-token.md

## Finish a passkey challenge

```bash
curl -s -X POST "${H[@]}" "$BASE/passkey-prologue" -d '{
  "id": "...",
  "rawId": "...",
  "type": "public-key",
  "response": { "authenticatorData": "...", "clientDataJSON": "...", "signature": "...", "userHandle": null },
  "clientExtensionResults": { "uvm": [] }
}'
```

```json
{ "success": true }
```

Failures: `{"success": false, "reason": "assertion (rawId + response) is required"}` and `{"success": false, "reason": "assertion fields must be strings"}`. Source: https://developer.z-api.io/instance/passkey-prologue.md

## Reset the challenge

```bash
curl -s -X POST "${H[@]}" "$BASE/reset-passkey-challenge"
```

`{"success": true}`, then call the QR endpoint again. Failure: `{"success": false, "error": "Failed to restart instance after challenge reset"}`. Source: https://developer.z-api.io/instance/reset-passkey-challenge.md

## Restart and disconnect

```bash
curl -s "${H[@]}" "$BASE/restart"      # {"value": true}, keeps the pairing
curl -s "${H[@]}" "$BASE/disconnect"   # {"value": true}, unpairs; ask first
```

Sources: https://developer.z-api.io/instance/restart.md, https://developer.z-api.io/instance/disconnect.md

## Instance data

```bash
curl -s "${H[@]}" "$BASE/me" | jq '{name, connected, paymentStatus, due, autoReadMessage, callRejectAuto, announcementGuard}'
```

Pick fields as above: the full response also has `token` and `proxyUrl`, which must not be shown. Source: https://developer.z-api.io/instance/me.md

## Device data

```bash
curl -s "${H[@]}" "$BASE/device"
```

```json
{
  "phone": "5511999999999",
  "imgUrl": "https://...",
  "about": "Recado do perfil do contato",
  "name": "Nome do usuário",
  "device": { "sessionName": "Z-API", "device_model": "Z-API" },
  "originalDevice": "iphone",
  "sessionId": 175,
  "isBusiness": false
}
```

Source: https://developer.z-api.io/instance/device.md

## Settings

Every setting is a `PUT` with a `value` body and answers `{"value": true}`.

```bash
curl -s -X PUT "${H[@]}" "$BASE/update-name"                -d '{"value": "Loja Centro"}'
curl -s -X PUT "${H[@]}" "$BASE/profile-name"               -d '{"value": "Loja Centro"}'
curl -s -X PUT "${H[@]}" "$BASE/profile-description"        -d '{"value": "Atendimento de 9h às 18h"}'
curl -s -X PUT "${H[@]}" "$BASE/profile-picture"            -d '{"value": "https://example.com/logo.jpg"}'
curl -s -X PUT "${H[@]}" "$BASE/update-auto-read-message"   -d '{"value": true}'
curl -s -X PUT "${H[@]}" "$BASE/update-auto-read-status"    -d '{"value": true}'
curl -s -X PUT "${H[@]}" "$BASE/update-call-reject-auto"    -d '{"value": true}'
curl -s -X PUT "${H[@]}" "$BASE/update-call-reject-message" -d '{"value": "Não atendemos ligações. Escreva aqui."}'
curl -s -X PUT "${H[@]}" "$BASE/update-announcement-guard"  -d '{"value": true}'
```

Queue behaviour while disconnected answers `{"success": true}`:

```bash
curl -s -X PUT "${H[@]}" "$BASE/update-queue-settings" -d '{"disableEnqueueWhenDisconnected": true}'
```

Sources: the settings rows in [SKILL.md](../SKILL.md), each linked to its docs page.

Methods and paths come from the request examples on each docs page and match the official n8n node (`@z-api/n8n-nodes-zapi` 0.1.8) where the node has them (`qr-code`, `qr-code/image`, `phone-code`, `device`, `disconnect`).
