# Z-API request examples

All examples read credentials from the environment. `BASE` is the instance base URL.

```bash
BASE="https://api.z-api.io/instances/$ZAPI_INSTANCE_ID/token/$ZAPI_TOKEN"
H=(-H "Client-Token: $ZAPI_CLIENT_TOKEN" -H "Content-Type: application/json")
```

## Instance status

```bash
curl -s "${H[@]}" "$BASE/status"
```

```json
{ "connected": true, "error": "You are already connected", "smartphoneConnected": true }
```

Other documented `error` values: `You need to restore the session`, `You are not connected`. Source: https://developer.z-api.io/instance/status.md

## Send text

```bash
curl -s -X POST "${H[@]}" "$BASE/send-text" \
  -d '{"phone": "5511999999999", "message": "Olá! Pedido *1234* confirmado.", "delayTyping": 2}'
```

```json
{ "zaapId": "3999984263738042930CD6ECDE9VDWSA", "messageId": "D241XXXX732339502B68", "id": "D241XXXX732339502B68" }
```

Source: https://developer.z-api.io/message/send-text.md

## Send image

```bash
curl -s -X POST "${H[@]}" "$BASE/send-image" \
  -d '{"phone": "5511999999999", "image": "https://example.com/produto.jpg", "caption": "Seu produto"}'
```

Source: https://developer.z-api.io/message/send-message-image.md

## Send document

The file extension goes in the path.

```bash
curl -s -X POST "${H[@]}" "$BASE/send-document/pdf" \
  -d '{"phone": "5511999999999", "document": "https://example.com/boleto.pdf", "fileName": "boleto.pdf"}'
```

Source: https://developer.z-api.io/message/send-message-document.md

## Number has WhatsApp?

```bash
curl -s "${H[@]}" "$BASE/phone-exists/5511999999999"
```

Source: https://developer.z-api.io/contacts/get-iswhatsapp.md

## Node.js

```js
const base = `https://api.z-api.io/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_TOKEN}`;

export async function sendText(phone, message) {
  const res = await fetch(`${base}/send-text`, {
    method: "POST",
    headers: { "Client-Token": process.env.ZAPI_CLIENT_TOKEN, "Content-Type": "application/json" },
    body: JSON.stringify({ phone, message }),
  });
  if (!res.ok) throw new Error(`Z-API ${res.status}: ${await res.text()}`);
  return res.json(); // { zaapId, messageId, id }
}
```

## Python

```python
import os, requests

BASE = f"https://api.z-api.io/instances/{os.environ['ZAPI_INSTANCE_ID']}/token/{os.environ['ZAPI_TOKEN']}"
HEADERS = {"Client-Token": os.environ["ZAPI_CLIENT_TOKEN"], "Content-Type": "application/json"}

def send_text(phone: str, message: str) -> dict:
    r = requests.post(f"{BASE}/send-text", json={"phone": phone, "message": message}, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()  # {"zaapId", "messageId", "id"}
```

Endpoint paths and methods in this file match the official Z-API n8n node (`@z-api/n8n-nodes-zapi` 0.1.8) and the docs pages linked above.
