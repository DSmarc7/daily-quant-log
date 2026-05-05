# Setup

## 1. Push this folder to GitHub

```bash
cd daily-quant-log
git init
git add .
git commit -m "init: daily quant log"
git branch -M main
git remote add origin https://github.com/DSmarc7/daily-quant-log.git
git push -u origin main
```

(Create the empty repo on github.com first — public is fine, and free for unlimited Actions minutes.)

## 2. Configure the daily Action (IMPORTANT)

For commits made by GitHub Actions to count on **your** contribution graph, the commit author email must match a verified email on your GitHub account.

**Step A — find your noreply email:**
1. Go to https://github.com/settings/emails
2. Look for the line: `<your-id>+DSmarc7@users.noreply.github.com`
3. Copy it.

**Step B — paste it into the workflow:**

Open `.github/workflows/market-tracker.yml` and replace the placeholder on the `git config user.email` line with your noreply email.

**Step C — verify it works:**

Go to the **Actions** tab on your GitHub repo → click "Daily market snapshot" → click "Run workflow". Wait ~1 min, then check that:
- A new commit appeared on `main`
- The commit shows your avatar (not the bot's)
- After a few minutes, the contribution shows on your profile graph

If the commit shows the GitHub Actions bot avatar instead of yours, the email is wrong — fix and re-run.

## 3. LeetCode → GitHub auto-push (LeetHub)

For your daily LeetCode habit, install the **LeetHub v2** browser extension:

- Chrome/Edge: search "LeetHub v2" in the extension store, install it.
- Authorize it to access GitHub, point it to this repo (or a separate `leetcode` repo if you prefer).
- Set the folder structure preference to match `leetcode/<problem-number>-<problem-name>/`.

After that, every time you submit an Accepted solution on LeetCode, it auto-pushes to your repo with the problem statement as README and your code in the right language. Zero manual work.

**Recommended workflow:** let LeetHub auto-push the solution, then come back later in the day and add a `notes.md` next to it for problems worth remembering — that's what makes the repo actually useful for revision and impressive for recruiters. See `leetcode/_template/notes.md`.

## 4. Daily TIL

No automation here on purpose — the value is in writing it yourself. Workflow:

```bash
# adapt to today's date
cp til/_template.md til/2026/05/2026-05-06-my-topic.md
# write it, then:
git add til/ && git commit -m "til: my-topic" && git push
```

You can ask Claude (or Claude Code) to help draft TIL entries on a topic you want to learn — it pairs well with structured study.

## 5. Local market tracker (optional)

If you want to test the tracker locally before relying on Actions:

```bash
cd market-tracker
pip install -r requirements.txt
python tracker.py
```

You should see new rows appended in `data/indices.csv`, `data/crypto.csv`, `data/fx.csv`, and a fresh `LATEST.md` at the repo root.
