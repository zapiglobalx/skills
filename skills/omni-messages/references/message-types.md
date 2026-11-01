# Z-API Omni request bodies by message type

Every body goes to `POST https://api.omni.z-api.io/v1/channels/{channelId}/messages` with `Authorization: Bearer $OMNI_SECRET_KEY` and `Content-Type: application/json`. Every success returns `{"messageId": "..."}`.

```bash
URL="https://api.omni.z-api.io/v1/channels/$OMNI_CHANNEL_ID/messages"
H=(-H "Authorization: Bearer $OMNI_SECRET_KEY" -H "Content-Type: application/json")
curl -s -X POST "${H[@]}" "$URL" -d @body.json
```

Before sending on official WhatsApp, check the 24-hour window (see SKILL.md).

## TEXT

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": { "type": "TEXT", "body": { "message": "Olá! Bem-vindo." } }
}
```

Source: https://developer.omni.z-api.io/messages/send-text.md

## IMAGE

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "IMAGE",
    "attachments": [{ "url": "https://example.com/produto.jpg", "caption": "Seu produto" }]
  }
}
```

`caption` is optional. Source: https://developer.omni.z-api.io/messages/send-image.md

## AUDIO

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": { "type": "AUDIO", "attachments": [{ "url": "https://example.com/audio.ogg" }] }
}
```

Source: https://developer.omni.z-api.io/messages/send-audio.md

## VIDEO

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "VIDEO",
    "attachments": [{ "url": "https://example.com/video.mp4", "caption": "Confira" }]
  }
}
```

`caption` is optional. Source: https://developer.omni.z-api.io/messages/send-video.md

## STICKER

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": { "type": "STICKER", "attachments": [{ "url": "https://example.com/sticker.webp" }] }
}
```

The file is WebP. Instagram and Messenger refuse your own file; send an image there. Source: https://developer.omni.z-api.io/messages/send-sticker.md

## CONTACT

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "CONTACT",
    "attachments": [{ "name": "Atendimento Loja", "phones": ["5511888888888"] }]
  }
}
```

`name` and `phones` are required. Not available on Instagram or Messenger. Source: https://developer.omni.z-api.io/messages/send-contact.md

## LOCATION

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "LOCATION",
    "attachments": [{
      "name": "Loja Centro",
      "address": "Av. Paulista, 1000 - São Paulo - SP",
      "latitude": "-23.5650",
      "longitude": "-46.6520"
    }]
  }
}
```

`latitude` and `longitude` are strings. The API does not validate them, but WhatsApp needs them to place the pin. `name` and `address` are optional. Not available on Instagram or Messenger. Source: https://developer.omni.z-api.io/messages/send-location.md

## INTERACTIVE_BUTTON (quick replies)

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "INTERACTIVE_BUTTON",
    "body": { "message": "Como você avalia nosso atendimento?" },
    "attachments": [
      { "id": "1", "title": "Ótimo" },
      { "id": "2", "title": "Bom" },
      { "id": "3", "title": "Regular" }
    ]
  }
}
```

Up to 3 buttons. To show media above the text, add `body.thumbnail` (image or video URL) and `body.mimeType` (for example `image/jpeg` or `video/mp4`). The customer's tap comes back through the webhook. Source: https://developer.omni.z-api.io/messages/send-interactive-button.md

## INTERACTIVE_ACTION (link and call)

```json
{
  "recipient": { "identifier": "5511999999999" },
  "content": {
    "type": "INTERACTIVE_ACTION",
    "header": { "message": "Loja" },
    "body": { "message": "Como podemos ajudar?" },
    "footer": { "message": "Escolha uma opção" },
    "attachments": [
      { "id": "1", "title": "Visite nosso site", "name": "URL", "url": "https://example.com" },
      { "id": "2", "title": "Fale conosco", "name": "CALL", "phones": ["5511999999999"] }
    ]
  }
}
```

`body`, and `id`, `title` and `name` on each button, are required. `header` and `footer` are optional. On Instagram and Telegram only `URL` works. Source: https://developer.omni.z-api.io/messages/send-interactive-action.md

## Reading the confirmation

The webhook event for a sent message carries the same id as `message._id`, `metadata.from_me: true`, and each content item has `state_items[]` with a `state.name` (for example `PENDING`). Source: https://developer.omni.z-api.io/webhooks/payloads.md
