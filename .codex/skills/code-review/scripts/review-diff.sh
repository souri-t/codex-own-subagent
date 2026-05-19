#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"

if [[ -z "${target}" ]]; then
  if remote_head="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)"; then
    target="${remote_head}"
  elif git rev-parse --verify --quiet origin/main >/dev/null; then
    target="origin/main"
  elif git rev-parse --verify --quiet main >/dev/null; then
    target="main"
  else
    echo "Could not determine target branch. Pass it explicitly, for example: review-diff.sh origin/main" >&2
    exit 1
  fi
fi

if ! git rev-parse --verify --quiet "${target}" >/dev/null; then
  echo "Target branch not found: ${target}" >&2
  exit 1
fi

base="$(git merge-base HEAD "${target}")"

printf 'target branch: %s\n' "${target}"
printf 'merge base: %s\n' "${base}"
printf 'head: %s\n' "$(git rev-parse HEAD)"
printf '\ncommits:\n'
git log --oneline --no-merges "${base}..HEAD"
printf '\nstat:\n'
git diff --stat "${base}..HEAD"
printf '\nname-status:\n'
git diff --name-status "${base}..HEAD"
printf '\nreview commands:\n'
printf 'git diff --unified=80 %s..HEAD\n' "${base}"
printf 'git diff --name-only %s..HEAD\n' "${base}"
printf 'git log --oneline %s..HEAD\n' "${base}"
