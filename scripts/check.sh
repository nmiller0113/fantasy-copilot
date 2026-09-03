#!/usr/bin/env bash
# Release validator for the Fantasy Copilot skill. Adapted from the K.I.S.S. validator.
#
# Run by a human before publishing. Never invoked by Claude, and SKILL.md does not
# reference it: a skill that tells the model to run a script to check the skill is
# theatre.
#
# Two authorities are mixed on purpose, and each check says which it enforces:
#   [spec]  the portable Agent Skills frontmatter spec (name charset, 1024 chars)
#   [house] this project's own rules, stricter than anything a loader enforces
#
#   ./scripts/check.sh          exit 0 clean, exit 1 on any FAIL, exit 2 cannot run
#                                 (wrong shell or bad usage)
#   ./scripts/check.sh --release  same, plus: the declared version must carry an
#                                 annotated tag on HEAD, the package directory must
#                                 be a repository root, and the working tree must be
#                                 clean (an untagged or half-committed version
#                                 cannot ship). Invoke it from anywhere; it cds.
#
# Needs bash, git and the usual POSIX tools (sed, grep, awk, head, sort, tr, basename,
# dirname).
#
# No pipefail: the leak scan pipes into `grep -q`, which exits at the first match
# and SIGPIPEs its producer. With pipefail that returns 141, the `if` goes false,
# and a genuinely leaking file prints "ok". Nothing here needs pipefail.
# Refuse any shell but bash in bash mode, loudly, exit 2 (cannot run). Under dash
# or ash the $'\r' CRLF probe below degrades to a literal string that never
# matches, so the gate would pass silently instead of failing. Bash invoked as
# sh (macOS /bin/sh is bash) sets BASH_VERSION but runs in POSIX mode, where the
# process substitutions below are syntax errors, so the mode is tested too.
if [ -z "${BASH_VERSION:-}" ] || shopt -qo posix 2>/dev/null; then
    printf 'FAIL  this validator needs bash; run: bash scripts/check.sh\n' >&2
    exit 2
fi
set -u

# Normalise the script's own path first: on Windows a caller can hand this file a
# backslash path (from cmd or PowerShell, or quoted at a Git Bash prompt), and
# dirname does not treat the backslash as a separator, which would cd to the
# repository's parent and blame a missing skill file instead of the path form.
self=${0//\\//}
cd "$(dirname "$self")/.." || { printf 'FAIL  cannot cd to package root\n' >&2; exit 1; }
SKILL="skills/fantasy-copilot/SKILL.md"
MANIFEST=".claude-plugin/plugin.json"
CHANGELOG="CHANGELOG.md"
release=0
case "${1:-}" in
    --release) release=1 ;;
    "") ;;
    *) printf 'usage: %s [--release]\n' "$0" >&2; exit 2 ;;
esac
fails=0
warns=0

fail() { printf 'FAIL  %s\n' "$1" >&2; fails=$((fails + 1)); }
warn() { printf 'WARN  %s\n' "$1" >&2; warns=$((warns + 1)); }
ok()   { printf 'ok    %s\n' "$1"; }
done_() { printf '\n%d fail, %d warn\n' "$fails" "$warns"; [ "$fails" -eq 0 ]; }

[ -f "$SKILL" ] || { fail "$SKILL not found"; done_; exit 1; }

# CRLF breaks every anchored match below, so rule it out before matching anything.
if grep -q $'\r' "$SKILL"; then
    fail "$SKILL has CRLF line endings; convert to LF (.gitattributes pins LF on checkout, but a clone made before it keeps its CRLF files until a fresh checkout)"
    done_; exit 1
fi

# --- frontmatter boundaries ---------------------------------------------------
head -n 1 "$SKILL" | grep -qE '^---[[:space:]]*$' || fail "line 1 must be '---'"
fm_end=$(awk 'NR>1 && /^---[[:space:]]*$/{print NR; exit}' "$SKILL")
[ -n "$fm_end" ] || { fail "frontmatter is never closed"; done_; exit 1; }
[ "$fm_end" -ge 3 ] || { fail "frontmatter is empty"; done_; exit 1; }
fm=$(sed -n "2,$((fm_end - 1))p" "$SKILL")
ok "frontmatter closes at line $fm_end"

# --- keys must be ones we recognise -------------------------------------------
allowed="name description license compatibility metadata allowed-tools when_to_use \
disable-model-invocation model context hooks version author"
while IFS= read -r key; do
    case " $allowed " in
        *" $key "*) ;;
        *) fail "unrecognised frontmatter key: $key" ;;
    esac
done < <(printf '%s\n' "$fm" | grep -oE '^[A-Za-z0-9_-]+:' | tr -d ':')

unquote() {
    local v=$1
    case $v in
        \"*\") v=${v#\"}; v=${v%\"} ;;
        \'*\') v=${v#\'}; v=${v%\'} ;;
    esac
    printf '%s' "$v"
}

SCALAR=""
scalar_or_die() {
    local key=$1 raw
    SCALAR=""
    raw=$(printf '%s\n' "$fm" | sed -n "s/^$key[[:space:]]*:[[:space:]]*//p" | head -n 1)
    case $raw in
        '>'*|'|'*) fail "$key: is a block scalar; keep it on one line"; return 1 ;;
    esac
    if [ -z "$raw" ]; then
        fail "$key: has no value on its own line; keep it on one line"
        return 1
    fi
    raw=$(unquote "$raw")
    case $raw in
        *[![:space:]]*) ;;
        *) fail "$key: is empty or whitespace only"; return 1 ;;
    esac
    SCALAR=$raw
}

# --- name ---------------------------------------------------------------------
if scalar_or_die name; then
    name=$SCALAR
    printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$' \
        || fail "name '$name' must be lowercase letters, numbers and hyphens [spec]"
    [ ${#name} -le 64 ] || fail "name is ${#name} chars, spec limit is 64"
    [ "$name" = "$(basename "$PWD")" ] \
        || warn "name '$name' does not match directory '$(basename "$PWD")'"
    ok "name: $name"
fi

# --- description: the field that decides whether the skill ever loads ----------
if scalar_or_die description; then
    desc=$SCALAR
    n=${#desc}
    if   [ "$n" -gt 1024 ]; then fail "description is $n chars, spec limit is 1024"
    elif [ "$n" -gt 500 ];  then warn "description is $n chars, house target is 500"
    else ok "description: $n chars"
    fi
fi

# --- body length [house] ------------------------------------------------------
lines=$(awk 'END{print NR}' "$SKILL")
body=$((lines - fm_end))
if   [ "$body" -gt 500 ]; then fail "body is $body lines, best-practice ceiling is 500"
elif [ "$body" -gt 200 ]; then warn "body is $body lines, house target is 200"
else ok "body: $body lines"
fi

# --- no code in SKILL.md [house] ----------------------------------------------
if grep -qE '^[[:space:]]*(```|~~~)' "$SKILL"; then
    fail "SKILL.md contains a code fence; instructions belong here, code in scripts/"
else
    ok "no code fences in SKILL.md"
fi

# --- referenced companion files exist -----------------------------------------
while IFS= read -r ref; do
    while [ "${ref%[.,;:)]}" != "$ref" ]; do ref=${ref%[.,;:)]}; done
    # scripts/ lives at the package root; references/ and assets/ live beside SKILL.md
    [ -e "$ref" ] || [ -e "${SKILL%/SKILL.md}/$ref" ] || fail "SKILL.md references '$ref', which does not exist"
done < <(grep -oE '(\./)?(scripts|references|assets)/[A-Za-z0-9._/-]+' "$SKILL" | sort -u)

# --- publishable: user-agnostic and leak-free ---------------------------------
# Modest by design. This catches the leaks that actually happen (a pasted path,
# a host, an address); it is not a general secret scanner and is not claimed to be.
for f in "$SKILL" README.md "$CHANGELOG" "${SKILL%/SKILL.md}"/references/*.md scripts/*.py; do
    [ -f "$f" ] || continue
    if grep -q $'\r' "$f"; then
        fail "$f has CRLF line endings; convert to LF"
        continue
    fi
    # TRAVERSAL FIRST, BEFORE ANY MASKING. A published skill has no legitimate
    # use for a relative parent segment in a path, so any occurrence is a finding
    # rather than something to mask around.
    if grep -qE '\.\./' "$f"; then
        fail "$f contains a '../' path segment; it can smuggle a local path past the mask"
    fi
    # ~/.claude/ is the documented install location, so it is masked before the
    # scan rather than exempted after it: every OTHER tilde path still trips.
    # Path shapes cover Unix (/home/, /Users/, ~/), Windows drive (C:\) and UNC
    # (\\server\share): a maintainer on any OS can leak a local path.
    if sed 's|~/\.claude/\([A-Za-z]\)|INSTALLDIR/\1|g' "$f" | grep -E '(/home/|/Users/|~/|\b[A-Za-z]:\\|\\\\[A-Za-z0-9._-]+\\|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\b([a-z0-9-]+\.)+(local|lan|internal)\b|\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b)' >/dev/null; then
        fail "$f contains a local path, address, internal hostname, or IP"
    else
        ok "$f: no local paths, addresses or hosts"
    fi
    if grep -q '—' "$f"; then
        fail "$f contains em dashes [house]"
    fi
    # [house] This plugin must stay user-agnostic. The check asserts a SHAPE, not
    # a list of known-bad strings: fantasy host league and team ids are digit runs
    # of 5+ digits, and nothing this skill legitimately says needs a number that
    # long (scores, rounds, years and percentages are all 4 digits or fewer). A
    # denylist of the author's own leagues would prove only that those exact
    # strings are absent, and shipping such a list would itself publish them.
    # HONEST COVERAGE NOTE: this catches numeric ids of any league, past or
    # future. It does NOT catch a league or team NAME in prose; names are
    # ordinary words and no scan can prove one is absent. Whoever publishes must
    # still read the shipped files end to end before pushing.
    if grep -qE '[0-9]{5,}' "$f"; then
        fail "$f contains a 5+ digit number; league/team ids are findings, shorten or remove [house]"
    else
        ok "$f: no id-shaped digit runs"
    fi
done

# --- shipped scripts parse [house] --------------------------------------------
# A Python script that does not parse is shipped broken. Python is optional for the
# plugin's users, so a validator host without it gets a WARN, not a FAIL.
for py in scripts/*.py; do
    [ -f "$py" ] || continue
    if command -v python3 >/dev/null 2>&1; then
        # ast.parse, not py_compile: it writes no __pycache__. The FAIL carries the
        # error's own line number, which SyntaxError puts in its message.
        if err=$(python3 -c 'import ast, sys
try:
    ast.parse(open(sys.argv[1], encoding="utf-8").read(), sys.argv[1])
except SyntaxError as e:
    sys.exit(f"{type(e).__name__} at line {e.lineno}: {e.msg}")' "$py" 2>&1); then
            ok "$py parses"
        else
            fail "$py does not parse: $(printf '%s' "$err" | tail -n 1)"
        fi
    else
        warn "python3 not found; $py not parse-checked"
    fi
done

# --- version is real: manifest, changelog entry, tag [house] -------------------
# A version number is a claim; the tag is the evidence. At build time the tag may
# not exist yet (you tag the commit that declares the version), so its absence is a
# WARN. With --release it is a FAIL: an untagged version cannot ship.
version=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$MANIFEST" 2>/dev/null | head -n 1)
if [ -z "$version" ]; then
    fail "$MANIFEST has no readable \"version\" field"
else
    if printf '%s' "$version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        ok "version: $version"
    else
        fail "version '$version' is not MAJOR.MINOR.PATCH"
    fi
    if [ -f "$CHANGELOG" ]; then
        if grep -qE "^## \[$version\]" "$CHANGELOG"; then
            ok "$CHANGELOG has an entry for $version"
        else
            fail "$CHANGELOG has no '## [$version]' entry; write it before releasing"
        fi
    else
        fail "no $CHANGELOG"
    fi
    # The tag must belong to THIS repository, not one that happens to enclose the
    # directory, and it must be annotated: a lightweight tag carries no date or
    # message of its own, and is the shape a forgotten -a produces.
    # --show-prefix is empty exactly at the root, through symlinked paths too, where
    # comparing --show-toplevel against $PWD wrongly fails (/tmp vs /private/tmp).
    atroot=0
    if git rev-parse --show-toplevel >/dev/null 2>&1 \
        && [ -z "$(git rev-parse --show-prefix 2>/dev/null)" ]; then
        atroot=1
    fi
    if [ "$atroot" -ne 1 ]; then
        if [ "$release" -eq 1 ]; then
            fail "not at the root of a git repository; tags cannot be verified"
        else
            warn "not at the root of a git repository; tag check skipped"
        fi
    elif git rev-parse -q --verify "refs/tags/v$version" >/dev/null 2>&1; then
        tagged=$(git rev-parse "refs/tags/v$version^{commit}")
        kind=$(git cat-file -t "refs/tags/v$version" 2>/dev/null)
        if [ "$kind" != "tag" ]; then
            fail "tag v$version is lightweight; delete it and re-tag with git tag -a"
        elif [ "$tagged" = "$(git rev-parse HEAD)" ]; then
            ok "annotated tag v$version points at HEAD"
        elif [ "$release" -eq 1 ]; then
            fail "tag v$version exists but does not point at HEAD; bump the version or move nothing"
        else
            warn "tag v$version exists on another commit; this checkout is not the released $version"
        fi
    elif [ "$release" -eq 1 ]; then
        fail "no tag v$version; tag the commit that declares $version before releasing"
    else
        warn "no tag v$version yet (fine at build time; required at release)"
    fi
    # What the gate validated must be what the tag points at.
    if [ "$release" -eq 1 ] && [ "$atroot" -eq 1 ]; then
        if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            fail "working tree is not clean; the files checked are not the files tagged"
        else
            ok "working tree clean"
        fi
    fi
fi

# --- files a published package must carry -------------------------------------
if [ -f LICENSE ]; then
    ok "LICENSE present"
else
    if printf '%s\n' "$fm" | grep -qE '^license[[:space:]]*:'; then
        fail "no LICENSE file, but the frontmatter declares one"
    else
        fail "no LICENSE file"
    fi
fi

done_
