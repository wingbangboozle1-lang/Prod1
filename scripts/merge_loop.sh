#!/usr/bin/env bash
# Rebase this branch onto origin/main and merge its pull request, in one tight loop.
#
# Why a script: other sessions append to COORDINATION.md on every merge, so main
# moves while this branch is open and the pull request goes DIRTY each time.
# The fix is always the same three steps, and doing them by hand takes long
# enough for main to move again. This loop does them back to back.
#
# The conflict resolution rule is the same every time:
#   COORDINATION.md     -> keep upstream's text, append this session's section
#   data/decisions.json -> keep upstream's file, re-apply the four de-duplications
#   build_site.py       -> keep upstream's generator, re-add the duplicate gate
# Nothing from another session is discarded.

set -u
cd "$(dirname "$0")/.."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
PR=${1:-68}
MAX=${2:-12}

resolve_coordination() {
  python3 - <<'PY'
import subprocess
main = subprocess.check_output(['git','show',':2:COORDINATION.md']).decode()
mine = subprocess.check_output(['git','show',':3:COORDINATION.md']).decode()
marker = '## Session arena/942dddd0-prod1 claim (2026-11-20)'
sec = mine[mine.index(marker):] if marker in mine else ''
open('COORDINATION.md','w').write(main.rstrip('\n') + '\n\n' + sec.rstrip('\n') + '\n' if sec else main)
PY
}

resolve_data() {
  python3 - <<'PY'
import subprocess, json, collections
up = subprocess.check_output(['git','show',':2:data/decisions.json']).decode()
s = up
def span(text, name):
    i = text.index('"name": "%s"' % name); return i, text.index('"gate":', i)
i, j = span(s, 'Machinery and automation')
blk = s[i:j]
for id_ in ('SG-33', 'Q-02', 'Q-14'):
    blk = blk.replace('    "%s",\n' % id_, '').replace('    "%s"\n' % id_, '')
s = s[:i] + blk + s[j:]
i, j = span(s, 'Findability and one canonical site')
s = s[:i] + s[i:j].replace('    "SG-43",\n', '') + s[j:]
note_add = (" On 2026-11-20 session arena/942dddd0-prod1 removed the four legacy double classifications"
            " (SG-33, SG-43, Q-02, Q-14), so every board row now sits in exactly one theme, and"
            " build_site.py fails the build if any row is unclassified, unknown or classified twice.")
if 'arena/942dddd0-prod1' not in s:
    k = s.index('"note": "') + len('"note": "')
    import re
    m = re.search(r'",\n\s*"updated"', s[k:])
    s = s[:k + m.start()] + note_add + s[k + m.start():]
open('data/decisions.json','w').write(s)
d = json.loads(s)
c = collections.Counter()
for t in d['themes']:
    for i_ in t['sgs'] + t['qs']:
        c[i_] += 1
dups = {k: v for k, v in c.items() if v != 1}
if dups:
    raise SystemExit('de-duplication failed: %s' % dups)
print('decisions.json: %d ids, each mapped once' % len(c))
PY
}

resolve_generator() {
  python3 - <<'PY'
import subprocess
up = subprocess.check_output(['git','show',':2:build_site.py']).decode()
start = up.index('DEC = json.load(open("data/decisions.json"))')
end = up.index('SG_N = len([i for i in _board_ids if i.startswith("SG")])')
block = up[start:end]
block = block.replace(
  '_theme_ids = sorted(set(i for t in DEC["themes"] for i in t["sgs"] + t["qs"]))',
  '_theme_id_list = [i for t in DEC["themes"] for i in t["sgs"] + t["qs"]]\n'
  '_theme_counts = {i: _theme_id_list.count(i) for i in set(_theme_id_list)}\n'
  '_theme_ids = sorted(_theme_counts)')
block = block.replace('_unknown = [i for i in _theme_ids if i not in _board_ids]',
                      '_unknown = sorted(i for i in _theme_ids if i not in _board_ids)')
block = block.replace('_uncovered = [i for i in _board_ids if i not in _theme_ids]',
  '_uncovered = [i for i in _board_ids if i not in _theme_ids]\n'
  '_duplicated = sorted(i for i, n in _theme_counts.items() if n != 1)')
marker = ("if _uncovered:\n    print(\"warn: data/decisions.json has not triaged these board rows; they are listed on decisions.html \"\n"
          "          \"under 'Nobody has taken these' and stay open: \" + \", \".join(_uncovered))")
if marker not in block:
    raise SystemExit('upstream generator shape changed; resolve build_site.py by hand')
block = block.replace(marker, marker +
  '\nif _duplicated:\n'
  '    raise SystemExit("data/decisions.json classifies board ids more than once: " + ", ".join(_duplicated)\n'
  '                     + ". Keep each row in exactly one theme. A row in two themes counts twice against "\n'
  '                     "both themes on decisions.html, so the register\'s own numbers stop matching the board.")')
cur = open('build_site.py').read()
if '<<<<<<<' in cur:
    a = cur.index('<<<<<<< HEAD')
    b = cur.index('\n', cur.index('>>>>>>>')) + 1
    cur = cur[:a] + block + cur[b:]
open('build_site.py','w').write(cur)
PY
}

for attempt in $(seq 1 "$MAX"); do
  echo "=== attempt $attempt ==="
  git fetch origin main
  if git merge-base --is-ancestor origin/main HEAD; then
    echo "branch already contains origin/main"
  else
    git rebase origin/main >/dev/null 2>&1
    while git status --porcelain | grep -q '^UU'; do
      if git status --porcelain | grep -q 'COORDINATION.md'; then
        resolve_coordination
        git add COORDINATION.md
      fi
      if git status --porcelain | grep -q 'data/decisions.json'; then
        resolve_data
        git add data/decisions.json
      fi
      if git status --porcelain | grep -q 'build_site.py'; then
        resolve_generator
        git add build_site.py
      fi
      if git status --porcelain | grep -q 'decisions.html'; then
        git checkout origin/main -- decisions.html
        git add decisions.html
      fi
      GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || { echo "rebase stalled"; break; }
    done
    git status --porcelain | grep -q '^UU' && { echo "unresolved conflict"; break; }
    python3 build_site.py >/dev/null 2>&1 || { echo "build failed after rebase"; break; }
    git add -A
    git diff --cached --quiet || git commit --amend --no-edit >/dev/null 2>&1
    git push --force-with-lease origin "$BRANCH" >/dev/null 2>&1 || { echo "push failed"; break; }
    echo "rebased and pushed"
  fi

  sleep 8
  state=$(gh pr view "$PR" --json mergeableStateStatus --jq .mergeableStateStatus 2>/dev/null)
  echo "mergeableStateStatus=$state"
  if gh pr merge "$PR" --merge 2>&1 | tail -2; then
    if gh pr view "$PR" --json state --jq .state | grep -q MERGED; then
      echo "MERGED"
      exit 0
    fi
  fi
  echo "merge failed (main moved again); retrying"
done
echo "gave up after $MAX attempts"
exit 1
