// Verify the x-webhook-signature header of a Z-API Omni webhook.
// Follows https://developer.omni.z-api.io/webhooks/signature.md:
// HMAC-SHA256 over "t\ntopic\npartition\noffset\nbody", hex, constant-time compare,
// timestamp tolerance of 300 seconds. Use the raw body (express.raw({ type: 'application/json' })),
// decompressed if the request was gzipped.

const crypto = require("node:crypto");
const zlib = require("node:zlib");

const TOLERANCE_SECONDS = 300;

function verify(headers, rawBody, secret, now = Date.now() / 1000) {
  const h = Object.fromEntries(Object.entries(headers).map(([k, v]) => [k.toLowerCase(), v]));
  const signature = h["x-webhook-signature"];
  const idempotency = h["x-idempotency-key"];
  if (!signature || !idempotency) return false;

  let body = Buffer.from(rawBody);
  if ((h["content-encoding"] || "").toLowerCase() === "gzip") body = zlib.gunzipSync(body);

  const parts = Object.fromEntries(signature.split(",").map((p) => p.split("=", 2)));
  const t = parts.t;
  const v1 = parts.v1;
  if (!t || !v1 || !/^\d+$/.test(t)) return false;
  if (Math.abs(now - Number(t)) > TOLERANCE_SECONDS) return false;

  // topic may itself contain ":", so take partition and offset from the right
  const pieces = idempotency.split(":");
  if (pieces.length < 3) return false;
  const offset = pieces.pop();
  const partition = pieces.pop();
  const topic = pieces.join(":");

  const canonical = Buffer.concat([Buffer.from([t, topic, partition, offset].join("\n") + "\n"), body]);
  const expected = crypto.createHmac("sha256", secret).update(canonical).digest();
  const received = Buffer.from(v1, "hex");
  return received.length === expected.length && crypto.timingSafeEqual(expected, received);
}

module.exports = { verify };

if (require.main === module) {
  // Self-test with a made-up secret and payload.
  const secret = "0".repeat(64);
  const body = Buffer.from('{"messageEventType":"NEW_MESSAGE"}');
  const t = String(Math.floor(Date.now() / 1000));
  const canonical = Buffer.concat([Buffer.from([t, "messages", "3", "42"].join("\n") + "\n"), body]);
  const v1 = crypto.createHmac("sha256", secret).update(canonical).digest("hex");
  const headers = { "X-Webhook-Signature": `t=${t},v1=${v1}`, "X-Idempotency-Key": "messages:3:42" };
  console.assert(verify(headers, body, secret), "valid signature rejected");
  console.assert(!verify(headers, Buffer.concat([body, Buffer.from(" ")]), secret), "tampered body accepted");
  console.assert(!verify(headers, body, secret, Number(t) + 301), "stale timestamp accepted");
  console.log("ok");
}
