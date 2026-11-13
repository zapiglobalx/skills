Review this Omni webhook handler for security problems before we go live.

```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();
app.use(express.text({ type: '*/*' }));

app.post('/omni/webhook', (req, res) => {
  const event = JSON.parse(req.body);
  const header = req.get('x-webhook-signature') || '';
  const v1 = header.split('v1=')[1];
  const expected = crypto
    .createHmac('sha256', process.env.OMNI_WEBHOOK_SECRET)
    .update(JSON.stringify(event))
    .digest('hex');
  if (v1 == expected) {
    handle(event);
  }
  res.sendStatus(200);
});
```
