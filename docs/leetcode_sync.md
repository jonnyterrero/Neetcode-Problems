# LeetCode Auto-Sync

Profile: <https://leetcode.com/u/jterrero16/>

Unlike NeetCode, **LeetCode has no first-party GitHub sync**. The
community fills the gap with browser extensions. Two active options:

| Extension | Store | Notes |
|---|---|---|
| **LeetHub v2** | Chrome / Edge Web Store — search "LeetHub v2" | Most popular; auto-pushes on Accepted. |
| **LeetSync** | Chrome Web Store — search "LeetSync" | Similar behavior; different maintainer. |

## Recommended: keep LeetCode in a SEPARATE repo

Point the extension at a new repository (e.g. `leetcode-solutions`), not
this one. Reasons:

- Their folder layouts don't match NeetCode's, so they would pollute
  `Data Structures & Algorithms/`.
- Auto-committed files often use formats that the Ruff/mypy config in
  this repo doesn't expect, which would break CI here.
- Keeps NeetCode Sync, LeetCode auto-sync, and your manual practice
  cleanly separated.

## One-time setup

1. Create the new repo on GitHub (public or private).
2. Install the extension from the Web Store.
3. Click the extension icon → **Authenticate with GitHub**.
4. Grant write access to the new repo only.
5. Solve a problem on leetcode.com → click **Submit** → on Accepted,
   the extension pushes to the new repo.

## How to keep the LeetCode repo visible from this one

Two options, in order of simplicity:

### Just link it (recommended)

Add a bullet to the top of `README.md`:

```markdown
- **LeetCode solutions:** <https://github.com/jonnyterrero/leetcode-solutions>
```

Done. No submodule complexity.

### Git submodule (advanced)

Only if you want to browse LeetCode solutions inside a checkout of this
repo:

```bash
git submodule add https://github.com/jonnyterrero/leetcode-solutions leetcode-solutions
git commit -m "chore: add leetcode-solutions as a submodule"
git push
```

Downside: submodules add extra `git` steps (`git submodule update
--init` after fresh clones). For a personal learning workflow the
overhead is usually not worth it.

## Security note

Both extensions handle a GitHub OAuth token. Before installing:

- Check the extension's source repository (both are on GitHub).
- Check the last-updated date and open-issues count.
- Only authorize write access to the LeetCode repo — not to your entire
  account.

If either extension asks for more permissions than that, walk away.

## Tracking manually-solved LeetCode problems here anyway

Even with auto-sync running to a separate repo, you may want a tracker
row *here* so your review queue includes LeetCode work. Do:

```bash
python scripts/create_problem.py \
  --name "Container With Most Water" \
  --source leetcode --topic two-pointers --difficulty medium \
  --url "https://leetcode.com/problems/container-with-most-water/"
```

Then link back to the auto-synced solution in the generated `NOTES.md`.
