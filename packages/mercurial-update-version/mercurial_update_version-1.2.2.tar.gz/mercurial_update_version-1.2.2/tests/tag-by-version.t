Approach to tags placed by revision.

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

We need some repository for the test

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository a little bit.

  $ cat > setup.py <<EOF
  > # This is setup
  > VERSION = "1.0"
  > # here it ends
  > EOF

  $ mkdir src

  $ cat > src/untouched.py << EOF
  > # This should not change
  > VERSION = "1.0"
  > EOF

  $ hg add
  adding setup.py
  adding src/untouched.py
  $ hg commit -m "Initial commit"

  $ cat > src/version.py << EOF
  > # This should change
  > VERSION = "1.0"
  > EOF

  $ hg add
  adding src/version.py
  $ hg commit -m "Second commit"

  $ cat > src/something.py << EOF
  > # Some file
  > EOF
  $ hg add
  adding src/something.py
  $ hg commit -m "Third commit"

Non-tip tag is ignored by extension

  $ hg tag -r 1   2.0
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)

  $ hg status

  $ hg log --graph
  @  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [tip] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Third commit / src/something.py []
  |
  o  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.0]
  |
  o  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []
  

  $ cat setup.py
  # This is setup
  VERSION = "1.0"
  # here it ends

  $ cat  src/version.py
  # This should change
  VERSION = "1.0"

But tag -r tip should work

  $ hg tag -r tip   2.1
  update_version: Version number in setup.py set to 2.1. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.1"
  update_version: Version number in src/version.py set to 2.1. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.1"

  $ hg status

  $ hg log --graph
  @  Just Test <just.text@nowhere.com>: Added tag 2.1 for changeset * / .hgtags [tip] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Version number set to 2.1 / setup.py src/version.py [2.1]
  |
  o  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Third commit / src/something.py []
  |
  o  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.0]
  |
  o  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []
  

  $ cat setup.py
  # This is setup
  VERSION = "2.1"
  # here it ends

  $ cat  src/version.py
  # This should change
  VERSION = "2.1"

And even tag -r «tip-revision»

  $ TIP_REV=`hg log -r tip --template '{node}'`
  $ hg tag -r $TIP_REV   2.2
  update_version: Version number in setup.py set to 2.2. List of changes:
      Line 2
      < VERSION = "2.1"
      > VERSION = "2.2"
  update_version: Version number in src/version.py set to 2.2. List of changes:
      Line 2
      < VERSION = "2.1"
      > VERSION = "2.2"

  $ hg status

  $ hg log --graph
  @  Just Test <just.text@nowhere.com>: Added tag 2.2 for changeset * / .hgtags [tip] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Version number set to 2.2 / setup.py src/version.py [2.2]
  |
  o  Just Test <just.text@nowhere.com>: Added tag 2.1 for changeset * / .hgtags [] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Version number set to 2.1 / setup.py src/version.py [2.1]
  |
  o  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Third commit / src/something.py []
  |
  o  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.0]
  |
  o  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []
  

  $ cat setup.py
  # This is setup
  VERSION = "2.2"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "2.2"

Finally let's check case when we are not on tip:

  $ hg update -r 3
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved

Attempt to tag by tip should be rejected:

  $ hg tag -r tip 0.9
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)
  abort: (working directory is )?not at a branch head \(use -f to force\) (re)
  [255]

  $ hg tag -f -r tip 0.9
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)

  $ hg status

  $ hg log --graph
  @  Just Test <just.text@nowhere.com>: Added tag 0.9 for changeset * / .hgtags [tip] (glob)
  |
  | o  Just Test <just.text@nowhere.com>: Added tag 2.2 for changeset * / .hgtags [0.9] (glob)
  | |
  | o  Just Test <just.text@nowhere.com>: Version number set to 2.2 / setup.py src/version.py [2.2]
  | |
  | o  Just Test <just.text@nowhere.com>: Added tag 2.1 for changeset * / .hgtags [] (glob)
  | |
  | o  Just Test <just.text@nowhere.com>: Version number set to 2.1 / setup.py src/version.py [2.1]
  |/
  o  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Third commit / src/something.py []
  |
  o  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.0]
  |
  o  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []
  

  $ cat setup.py
  # This is setup
  VERSION = "1.0"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "1.0"

But attempt to tag by this very revision should work:

  $ hg up -r 4
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg tag -r 4 5.9
  update_version: Version number in setup.py set to 5.9. List of changes:
      Line 2
      < VERSION = "2.1"
      > VERSION = "5.9"
  update_version: Version number in src/version.py set to 5.9. List of changes:
      Line 2
      < VERSION = "2.1"
      > VERSION = "5.9"
  created new head

  $ hg status

  $ hg log --graph
  @  Just Test <just.text@nowhere.com>: Added tag 5.9 for changeset * / .hgtags [tip] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Version number set to 5.9 / setup.py src/version.py [5.9]
  |
  | o  Just Test <just.text@nowhere.com>: Added tag 0.9 for changeset * / .hgtags [] (glob)
  | |
  | | o  Just Test <just.text@nowhere.com>: Added tag 2.2 for changeset * / .hgtags [0.9] (glob)
  | | |
  | | o  Just Test <just.text@nowhere.com>: Version number set to 2.2 / setup.py src/version.py [2.2]
  | | |
  +---o  Just Test <just.text@nowhere.com>: Added tag 2.1 for changeset * / .hgtags [] (glob)
  | |
  o |  Just Test <just.text@nowhere.com>: Version number set to 2.1 / setup.py src/version.py [2.1]
  |/
  o  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [] (glob)
  |
  o  Just Test <just.text@nowhere.com>: Third commit / src/something.py []
  |
  o  Just Test <just.text@nowhere.com>: Second commit / src/version.py [2.0]
  |
  o  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py []
  

  $ cat setup.py
  # This is setup
  VERSION = "5.9"
  # here it ends

  $ cat src/version.py
  # This should change
  VERSION = "5.9"
