Let's test case of multiple languages and CVS keywords on the same repo.

Let's define test locations

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export TREE=$WORK_DIR/tree
  $ export REPO=$TREE/repo

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
  > py_tree.active_on = $TREE
  > py_tree.language = python
  > py_tree.tagfmt = dotted
  > js_tree.active_on = $TREE
  > js_tree.language = javascript
  > js_tree.tagfmt = dotted
  > excvs_tree.active_on = $TREE
  > excvs_tree.expand_keywords = 1
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository a little bit.

  $ cat > $REPO/setup.py <<EOF
  > # This is setup
  > VERSION = "1.0"
  > # and CVS
  > NAME = "\$Name\$"
  > # here it ends
  > EOF

  $ mkdir $REPO/src

  $ cat > $REPO/src/version.py << 'EOF'
  > VERSION = "1.0"
  > EOF

  $ mkdir $REPO/js

  $ cat > $REPO/js/version.js << 'EOF'
  > const VERSION = "1.0";
  > EOF

  $ cat > $REPO/setup.cxx <<'EOF'
  > // This is some file
  > // $Name$
  > // $Revision$
  > //
  > // Let's try again, using constants and expanded versions
  > const string Name = "$Name: ver_1-3-7 $";
  > // here it ends
  > EOF

  $ hg --cwd $REPO add
  adding js/version.js
  adding setup.cxx
  adding setup.py
  adding src/version.py

  $ hg --cwd $REPO commit -m "Initial commit"

  $ cd $REPO

  $ hg tag 1.2.3
  update_version: Version number in setup.py set to 1.2.3. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "1.2.3"
  update_version: Version number in src/version.py set to 1.2.3. List of changes:
      Line 1
      < VERSION = "1.0"
      > VERSION = "1.2.3"
  update_version: Version number in js/version.js set to 1.2.3. List of changes:
      Line 1
      < const VERSION = "1.0";
      > const VERSION = "1.2.3";
  update_version: CVS keywords expanded in setup.cxx setup.py

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 1.2.3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.2.3 / js/version.js setup.cxx setup.py src/version.py [1.2.3]
  Just Test <just.text@nowhere.com>: Initial commit / js/version.js setup.cxx setup.py src/version.py []

  $ cat setup.py
  # This is setup
  VERSION = "1.2.3"
  # and CVS
  NAME = "$Name: 1.2.3 $"
  # here it ends

  $ cat src/version.py
  VERSION = "1.2.3"

  $ cat js/version.js
  const VERSION = "1.2.3";

  $ cat setup.cxx
  // This is some file
  // $Name: 1.2.3 $
  // $Revision: * $ (glob)
  //
  // Let's try again, using constants and expanded versions
  const string Name = "$Name: 1.2.3 $";
  // here it ends

  $ hg tag_version_test 4.5.7
  update_version: using python language rules and dotted tag format
  update_version: using javascript language rules and dotted tag format
  update_version: expanding CVS keywords
  update_version: Version number in setup.py set to 4.5.7. List of changes:
      Line 2
      < VERSION = "1.2.3"
      > VERSION = "4.5.7"
  update_version: Version number in src/version.py set to 4.5.7. List of changes:
      Line 1
      < VERSION = "1.2.3"
      > VERSION = "4.5.7"
  update_version: Version number in js/version.js set to 4.5.7. List of changes:
      Line 1
      < const VERSION = "1.2.3";
      > const VERSION = "4.5.7";
  update_version: CVS keywords expanded in setup.cxx setup.py

