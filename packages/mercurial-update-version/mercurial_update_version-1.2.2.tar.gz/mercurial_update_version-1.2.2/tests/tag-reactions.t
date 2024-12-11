We will test reactions to various tag placing methods.

Let's define test locations

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export PY_TREE=$WORK_DIR/py_tree
  $ export REPO=$PY_TREE/repo

and appropriate Mercurial configuration file

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Just Test <just.text@nowhere.com>
  > logtemplate = {author}: {desc} / {files} [{tags}]\n
  > [extensions]
  > mercurial_update_version =
  > [update_version]
  > py_tree.active_on = $PY_TREE
  > py_tree.language = python
  > py_tree.tagfmt = dotted
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository a little bit.

  $ cat > $REPO/setup.py <<EOF
  > # This is setup
  > VERSION = "1.0"
  > # here it ends
  > EOF

  $ mkdir $REPO/src

  $ cat > $REPO/src/untouched.py << 'EOF'
  > # This should not change
  > VERSION = "1.0"
  > # Neither this: $Name$
  > EOF

  $ hg --cwd $REPO add
  adding setup.py
  adding src/untouched.py
  $ hg --cwd $REPO commit -m "Initial commit"

  $ cat > $REPO/src/version.py << EOF
  > # This should change
  > VERSION = "1.0"
  > EOF

  $ hg --cwd $REPO add
  adding src/version.py
  $ hg --cwd $REPO commit -m "Second commit"

Invalid tags should not impact anything:

  $ hg tag ugly
  update_version: Invalid tag format: ugly (expected dotted, for example 1.3.11). Version not updated (but tag created).
  update_version: no files changed

  $ hg tag 1-2-3
  update_version: Invalid tag format: 1-2-3 (expected dotted, for example 1.3.11). Version not updated (but tag created).
  update_version: no files changed

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat setup.py src/version.py
  # This is setup
  VERSION = "1.0"
  # here it ends
  # This should change
  VERSION = "1.0"

Neither local tags

  $ hg tag --local 77.77.77
  update_version: ignoring local tag (version number not updated)

  $ cat setup.py
  # This is setup
  VERSION = "1.0"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "1.0"

Nothing happens when the proper version is already there:

  $ hg tag 1.0
  update_version: Line 2 in setup.py already contains proper version number
  update_version: Line 2 in src/version.py already contains proper version number
  update_version: no files changed

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 1.0 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [1.0 77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat setup.py
  # This is setup
  VERSION = "1.0"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "1.0"

Nor tags on non-tip (well, non-current)

  $ hg tag -r 1 2.3.4
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.3.4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [1.0 77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.3.4 ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat setup.py
  # This is setup
  VERSION = "1.0"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "1.0"

Also re-tagging with the same tag needs no support

  $ hg tag 2.0
  update_version: Version number in setup.py set to 2.0. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.0"
  update_version: Version number in src/version.py set to 2.0. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.0"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.0 / setup.py src/version.py [2.0]
  Just Test <just.text@nowhere.com>: Added tag 2.3.4 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [1.0 77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.3.4 ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat setup.py
  # This is setup
  VERSION = "2.0"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "2.0"

  $ echo "XXX" >> setup.py
  $ hg commit -m "Dummy X"

  $ hg tag -f 2.0
  update_version: Line 2 in setup.py already contains proper version number
  update_version: Line 2 in src/version.py already contains proper version number
  update_version: no files changed

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Dummy X / setup.py [2.0]
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.0 / setup.py src/version.py []
  Just Test <just.text@nowhere.com>: Added tag 2.3.4 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [1.0 77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.3.4 ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat setup.py
  # This is setup
  VERSION = "2.0"
  # here it ends
  XXX

  $ cat src/version.py
  # This should change
  VERSION = "2.0"

To make sure, let's see what happens when we stay outside repo root

  $ cd $REPO/src
  $ hg tag 2.1
  update_version: Version number in setup.py set to 2.1. List of changes:
      Line 2
      < VERSION = "2.0"
      > VERSION = "2.1"
  update_version: Version number in src/version.py set to 2.1. List of changes:
      Line 2
      < VERSION = "2.0"
      > VERSION = "2.1"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.1 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.1 / setup.py src/version.py [2.1]
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Dummy X / setup.py [2.0]
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.0 / setup.py src/version.py []
  Just Test <just.text@nowhere.com>: Added tag 2.3.4 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1.0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Added tag 1-2-3 for changeset * / .hgtags [1.0 77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Added tag ugly for changeset * / .hgtags [1-2-3] (glob)
  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.3.4 ugly]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []

  $ cat ../setup.py
  # This is setup
  VERSION = "2.1"
  # here it ends
  XXX

  $ cat version.py
  # This should change
  VERSION = "2.1"

TODO: tag -r tip 

TODO: (or -r ‹tip-revision›)
