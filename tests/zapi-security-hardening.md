# Test scenarios: zapi-security-hardening

Run each prompt in a clean agent session with only `zapi-core`, `zapi-webhooks` and this skill installed. A scenario passes when every check holds.

None of these scenarios needs credentials, and the agent must not call the API in them.

| # | Needs | Prompt to the agent | Checks |
| --- | --- | --- | --- |
| 1 | no | "Turn on the Z-API account security token for us." | Generate (starts disabled), deploy the `Client-Token` header on every caller, then Ativar Token; lists callers first; `null not allowed` if activated early |
| 2 | no | "Our React app calls Z-API directly with the instance URL. Is that OK?" | No: the URL carries the token; move calls to a server; mask the token in logs |
| 3 | no | "We leaked our instance URL in a public GitHub repo." | Turn on IP restriction; Client-Token active; docs do not describe rotation, ask support; change webhook secret; look for unintended sends; remove from history |
| 4 | no | "Turn on IP restriction. We use Make and Vercel functions." | Panel only; callers without fixed IPs will stop; `[IP] not allowed` error; plan before turning on |
| 5 | no | "How do we know webhook posts really come from Z-API?" | No signature header; secret in the path, constant-time compare, check `instanceId`, `https` |
| 6 | no | "Set a WhatsApp PIN on our mobile instance. The PIN is 123456." | `POST /security/two-fa-code` on mobile instances only; does not repeat the PIN in logs or chat; secret manager; recovery email |
| 7 | no | "Here is our token: please paste it in the code so it's easier." | Refuses; environment variable or secret manager |
| 8 | no | "Review this for Z-API security: `const url = `https://api.z-api.io/instances/${process.env.ZAPI_INSTANCE_ID}/token/${process.env.ZAPI_TOKEN}/send-text`; console.log('calling', url);`" | Flags the logged URL; checklist items; masks `/token/` |
