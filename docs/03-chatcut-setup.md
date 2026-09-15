# ChatCut plugin — setup notes (chatcut.io/claude)

What was done in this session, following https://chatcut.io/claude:

```bash
claude plugin marketplace add https://github.com/ChatCut-Inc/agent-plugin.git#main   # marketplace "chatcut-inc" added
claude plugin install chatcut@chatcut-inc                                            # v1.10.12, scope: user, enabled
claude plugin list                                                                   # shows chatcut@chatcut-inc ✓ enabled
```

Requirement met: Claude Code 2.1.210 or newer (this environment runs 2.1.271).

## Authentication (needs a browser — not possible headless)

The plugin's MCP server (`plugin:chatcut:chatcut`) is OAuth-protected. Its login helper was started:

```bash
sh "$CLAUDE_PLUGIN_ROOT/skills/chatcut-plugin-basics-claude/login-chatcut.sh"   # logs to /tmp/chatcut-login.log
```

It printed an authorization URL of the form
`https://api.chatcut.io/auth/mcp/authorize?...&redirect_uri=http%3A%2F%2Flocalhost%3A61192%2Fcallback...`
and waits for the browser redirect. In a remote container nobody can complete that redirect, so the
ChatCut tools stay unauthenticated here. To finish on a machine with a browser:

1. `claude plugin marketplace add https://github.com/ChatCut-Inc/agent-plugin.git#main`
2. `claude plugin install chatcut@chatcut-inc`
3. In Claude Code run `/mcp`, choose `plugin:chatcut:chatcut` → **Authenticate**, sign in.
4. Verify: `claude mcp get plugin:chatcut:chatcut` → connected; `/tmp/chatcut-login.log` ends with
   `Authenticated with 'plugin:chatcut:chatcut'`.
5. Start a **new** session and mention ChatCut in the first message — the tools load only then.

## What ChatCut would be used for in this project

The plugin bundles skills for video editing, motion graphics, captions, voice, music and export.
Once authenticated, the natural next step is: import `renders/is-oto-overview.mp4` (or the raw
screenshots + `audio/mix.mp3`) into a ChatCut project, add burned-in Russian captions from
`pipeline/script.json`, and let the team refine cuts in the ChatCut editor. Until then the cut is
produced with Higgsfield's Higgsedit (see `pipeline/build_edit.py`).
