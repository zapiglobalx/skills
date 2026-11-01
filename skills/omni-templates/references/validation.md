# Template validation rules and error codes

Meta reviews a template after it is created, but refuses at once anything out of shape. These are the rules that come up most, all from https://developer.omni.z-api.io/templates/validation.md unless another link is given. Field meanings: https://developer.omni.z-api.io/templates/anatomy.md

## Character limits

| Field | Limit |
|---|---|
| Text header | 60 |
| Body | 1024 |
| Footer | 60 |
| Button text | 25 |
| Button URL | 2000 |
| Button phone | 20 |
| Coupon code | 20 |
| Offer text | 16 |
| Carousel card text | 160 |
| Template name | 512 |

The name takes lowercase letters, digits and underscore, and never changes.

## Line breaks

Only the body takes line breaks. In header, footer and button text, `\n`, `\r`, tabs and more than four spaces in a row are refused. In the body, avoid a blank line at the end and more than two breaks in a row.

## Variables

- **A variable cannot open or close the text** (header or body). `"{{nome}}, seu pedido saiu"` is refused with `2388299`; `"Olá {{nome}}, seu pedido saiu"` passes.
- **Every variable needs an example**, or Meta refuses with `missing expected field(s) (example)`, `2388043`.
  - Named: `"example": {"body_text_named_params": [{"param_name": "nome", "example": "Marina"}]}`
  - Positional: `"example": {"body_text": [["Marina", "1042"]]}`
- **Positional numbering is a sequence from 1.** `{{1}}` and `{{3}}` is refused; use `{{1}}` and `{{2}}`.
- **The header takes one variable.** A second one fails with `2388029`.
- **The footer takes no variable.** It is sent literally.
- **Short text with many variables is refused**, `2388293`. Meta does not publish the formula; the docs measured about three words of text per variable, plus one, from two variables up. Two variables with nothing between them are also usually refused.
- A URL button takes one variable, only at the end of the address: `https://sualoja.com/pedido/{{1}}`. Phone and coupon buttons take none.

## Buttons

| Rule | Limit |
|---|---|
| Buttons in total | 10 |
| URL buttons | 2 |
| Phone buttons | 1 |
| Coupon buttons | 1 |
| Quick replies | 10 |
| Buttons per carousel card | 2, or 1 on a product card |

- Quick replies must stay together, in one group, with the other buttons in another group. A quick reply between other types is refused.
- URLs need `http` or `https`.
- Phones need the international format with `+` and country code, for example `+5511988881234`. Otherwise: `(#192) ... is not a valid phone number`.
- On catalog, multi-product, single product, checkout, order details and authentication code, Meta writes the button label. `text` is still required, but another value fails with `2388153`, and the error says the right one:

| Button | `text` |
|---|---|
| `CATALOG` | `View catalog` |
| `MPM` | `View items` |
| `SPM` | `Ver` in a `pt_BR` template, `View` in others |
| `PAYMENT_REQUEST` | `Review and Pay` |
| `ORDER_DETAILS` | `Copy Pix code` |

## Carousel

- Media carousel: 2 to 10 cards, every card with media.
- Product carousel: exactly 2 cards at creation, up to 10 at send. Header `{"format": "PRODUCT"}` and one button, no card text. Otherwise `component of type BODY is required`, `2388045`.
- All cards have the same components and the same buttons in the same order.

## Media

| Format | Types | Size |
|---|---|---|
| Image | JPEG, PNG | 5 MB |
| Video | MP4, 3GPP | 16 MB |
| Document | PDF | 100 MB |

- The header sample is a handle from https://developer.omni.z-api.io/templates/upload-media.md, or a public link that Omni converts.
- A link read back from an existing template (`whatsapp.net`, `fbcdn.net`, `fbsbx.com`) is refused as a sample: `invalid media sample`, `2388215`.
- The link must download from a server, not only open in a browser. Otherwise `media download failed`, `380`.
- Header images show at 1.91:1; anything else is cropped from the center.

## Send validity

`message_send_ttl_seconds` per category: authentication 30 to 900, utility 30 to 43200, marketing 43200 to 2592000. `-1` means 30 days. In authentication the send validity cannot be shorter than the code's.

## Account limits

| Limit | Value |
|---|---|
| Templates per WABA | 250, or 6,000 with a verified portfolio and a number with an approved display name |
| Creations per hour, per WABA | 100 |

The name is unique per WABA and language. Repeating name and language returns `already exists`, also when the other one was deleted less than 30 days ago. Above 100 creations per hour, create in batches and wait; do not retry at once.

## Error codes

| Code | Message | Fix |
|---|---|---|
| `2388029` | The Header field can only have up to 1 variable(s) | Two variables in the header |
| `2388043` | missing expected field(s) (example) | Variable without example, or positional numbering out of sequence |
| `2388045` | component of type BODY is required | Body or second button on a product card |
| `2388153` | Text for button type 'X' cannot be modified | Fixed label changed |
| `2388158` | number of buttons exceeded the limit | Third button on a limited-time offer |
| `2388191` | URL is required at index 1 | Offer without its link button |
| `2388193` | Header type TEXT is not allowed | Text header on a limited-time offer |
| `2388215` | invalid media sample | Meta CDN link sent back |
| `2388293` | Parameters words ratio exceeds limit | Short text with many variables |
| `2388299` | Leading or trailing parameters not allowed | Variable at the start or end |
| `#192` | is not a valid phone number | Phone without country code |
| `380` | media download failed | Link the Meta server cannot download |

When Meta refuses, Omni returns Meta's original message with a `traceId`. Keep both for support. Error bodies: `400` comes as `{"error": "...", "value": {"errors": [{"name": "META_WHATSAPP_ERROR", "message": "...", "code": "..."}]}}` and `422` as `{"error": {"errors": [{"code": "100", "name": "META_WHATSAPP_ERROR", "subCode": "2388024", "message": "...", "description": "..."}]}}` (https://developer.omni.z-api.io/templates/create-template.md).
