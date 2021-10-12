#!/usr/bin/env bash
# Intel Copyright © 2021, Intel Corporation.

REMOTE_NAME="${1-origin}"
BASE_REF="${GITHUB_BASE_REF-main}"

REVISION_RANGE=remotes/$REMOTE_NAME/$BASE_REF..HEAD

# See https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitglossary.html#def_pathspec for help on PATHSPEC
PATHSPEC=':^**.md :^.prettierignore :^.gitignore :^.editorconfig :^.prettierrc :^assets/i18n/** :^**.png :^**.gif :^**.json :^**.xml :^**.yaml :^**.yml'

TMPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TMPDIR"' EXIT

cd ${GITHUB_WORKSPACE-$(git rev-parse --show-toplevel)}
if git log --format="%h" --author @intel.com $REVISION_RANGE | grep -q . ; then
  # This PR contains an Intel contribution
  git diff --name-only --diff-filter=MA $REVISION_RANGE  . $PATHSPEC > $TMPDIR/files_altered.txt
  (egrep --files-without-match  "©.*Intel" $(cat $TMPDIR/files_altered.txt) || true) > $TMPDIR/files_missing_copyright.txt
  find /dev/null $(cat $TMPDIR/files_missing_copyright.txt) ! -size 0 > $TMPDIR/nonempty_files_missing_copyright.txt

  if [[ -s $TMPDIR/nonempty_files_missing_copyright.txt ]]; then
    echo These files are missing a copyright message: >> /dev/stderr
    cat $TMPDIR/nonempty_files_missing_copyright.txt >> /dev/stderr
    exit 2
  fi
fi
