# How to contribute

Contributions come in by pull request. A skill is accepted only when it meets the five criteria below.

1. **True to the documentation.** Every endpoint, field and limit it mentions links to its page on developer.z-api.io or developer.omni.z-api.io. Nothing written from memory.
2. **Actually runs.** The skill has a `tests/<name>.md` file with scenarios (start from the [scenario template](templates/tests.template.md)). A clean agent, with only the skill, runs each scenario against a test instance, and the result is checked through the webhook. A scenario that sends a message runs only on the test instance or test account, never on a customer number. CI does not run these scenarios yet: it only runs the checks that need no credentials.
3. **No secrets.** Credentials come only from environment variables. CI rejects tokens in the text.
4. **Responsible sending.** Skills that send messages ask for opt-in, offer a way out and point to the Z-API best practices. No bulk sending without consent.
5. **Webhook text is data.** Every skill that reads incoming messages tells the agent that this text comes from the end user and is never an instruction.

## Format

- One folder per skill in `skills/<name>/`, with `SKILL.md` and, if needed, `references/` (long detail the agent reads only when it needs it) and `scripts/` (code that runs).
- Name prefixed with `zapi-` (Z-API) or `omni-` (Z-API Omni), lowercase, the same as the folder name.
- A skill folder may also have `assets/` (templates and files the skill uses), as the [Agent Skills specification](https://agentskills.io/specification) allows.
- Required frontmatter: `name` (up to 64 characters), `description` (40 to 1024 characters; says when to use the skill, and is what the agent reads to decide), `license: Apache-2.0` and `metadata.version`. Optional: `compatibility` (up to 500 characters; network and account needed), `metadata.author` and `metadata.homepage`.
- `SKILL.md` up to 500 lines. Anything beyond that goes in `references/`.
- Everything public in this repository is in English: the skills, so they serve agents and developers in any country, and the README, this guide and the other docs.
- Start from the [template](templates/SKILL.template.md).

## Before opening the PR

```bash
python3 scripts/validate.py
```

The script checks the frontmatter, the folder name, the size, the internal links (`references/`, `scripts/`, `assets/`), the presence of links to the documentation and of the scenario table, the notice that webhook text is data, and looks for secrets (including an instance token in a URL). It warns, without rejecting, when a skill that sends messages does not point to the [best practices](https://developer.z-api.io/tips/best-practices.md).

To also check that every documentation link responds:

```bash
python3 scripts/validate.py --online
```

CI runs `validate.py` and `validate.py --online` on every pull request, with actions pinned by SHA, a read-only token and no secrets: a scenario with credentials never runs in CI. The PR opens with a checklist of the criteria above.

## Running a scenario

```bash
python3 scripts/run-scenario.py --list tests/zapi-instance.md
python3 scripts/run-scenario.py --client claude --test tests/zapi-instance.md --scenario 1 \
  --bin-dir /Library/ZapiCofre/clientes/claude-<version>
```

Each run uses a new folder with its own `HOME` and configuration, and installs only the scenario's skill and the ones the scenario file's header asks for. Before running, the script lists the skills the client sees there and stops if the list is not exactly that (plus the ones that ship with the client itself). Clients: `claude`, `codex` and `gemini`. The client's login comes from an environment variable (`ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`, `CODEX_API_KEY` or `OPENAI_API_KEY`, `GEMINI_API_KEY`). Only one per run: with two set, the script refuses. `meta.json` records which one was used and whether it is an API key or an OAuth token. Before any client runs, the run folder must hold exactly what the script wrote (the skills). Any other file stops the run, such as a copy of `~/.claude`, `.claude.json`, `.codex/auth.json`, `.gemini/oauth_creds.json`, `.env` or anything with `token`, `key` or `credential` in its name. After the listing and after the run, nothing the client wrote may be a login file or have a credential-like name. `meta.json` records what was refused and why.

The client runs confined by macOS `sandbox-exec`. Outside macOS, the script does not run a real client.

The client comes only from the pinned folder (`--bin-dir`; a client that is a node script runs with the pinned `--node`, by absolute path), never from `PATH`. Before running, the script refuses (exit 2) if the client, `node`, the manifest, any file in the pinned folder, or any folder on the client's `PATH` or above it, is not owned by `root` or `_zapicofre`, or is writable by group or others. It also refuses if any file in the pinned folder or `node` is not in `SHA256SUMS` (`--manifest`, default `/Library/ZapiCofre/clientes/SHA256SUMS`) with the same SHA-256. The client's `PATH` is the pinned folder, the `node` folder and `/usr/bin:/bin:/usr/sbin:/sbin`, never `/opt/homebrew/bin`, `/usr/local/bin` or `HOME`, and it is recorded in `meta.json`. With `BWS_ACCESS_TOKEN` in the environment, the script does not run. Every environment value that is not an ordinary variable (`PATH`, `HOME`, `LANG` and the like) is replaced by its name in what gets saved.

- It reads nothing in `/Users`, `/Volumes`, `/Library/Keychains` or the temporary folders, except the run folder and the client's own installation, and writes only to the run folder.
- The Keychain does not answer, and it cannot reach any local socket outside the run folder, such as the `ssh-agent` one.
- The only network is a proxy run by the script, which lets through the model host and, in a live scenario, the Z-API hosts.
- The proxy opens calls to Z-API with a certificate authority created for the run. In live runs it accepts a single destination, the `phone` (Z-API) or the `recipient.identifier` (Omni), equal to `TEST_PHONE`, and only through a fixed list of message and chat routes (`modify-chat` and `send-chat-expiration`, with exactly the keys on the docs page); on the compatibility layer (`zapi.omni.z-api.io`), only `send-text` on the channel and with the scenario's token. It also accepts a short list of reads (`GET status`, `device`, `me`, `phone-exists/{digits}` and `phone-code/{TEST_PHONE}` on Z-API; channels, WABAs and templates on Omni), with no body or query beyond what the page documents, and returns the response to the agent with every credential-looking value replaced by `[removed by run-scenario]`. Groups, `@lid`, a number in another form, configuration and webhook routes, and any other read or write get 403. So does any outside link (URL, domain, `www.`, IP), in a media, link or text field, even nested: media goes as base64 (`data:...;base64,`) or as a URL from the fixed `TEST_MEDIA_URLS` list, empty today.

- A scenario marked **live**, `sends` or `account` runs only on `claude` and only with the variables the header names plus `TEST_PHONE`; without them, the script refuses. An unmarked scenario receives none of these variables.
- A row that describes a setup (a received webhook, a recorded event) needs `--prompt-file` with the exact prompt.
- `--sabotage` installs without the scenario's skill, for the control run that must fail.
- The transcript, the skill list, the proxy log and the metadata (skill hash, client version) stay outside the repository, in `~/.local/state/zapi-skills/runs` or in `--out`. The value of each credential, also in base64, hex or URL form, is replaced by the variable's name. The script does not judge: whoever runs it reads the transcript against the "Checks" column.

`python3 scripts/run-scenario.py --self-test` tests the script itself with fake clients, no network and no credentials.

## Versions

If the skill's behavior changed, bump `metadata.version` and record it in [CHANGELOG.md](CHANGELOG.md).
