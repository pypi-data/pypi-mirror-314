
Let's test whether proper files are updated with proper syntax.

Defining various locations:

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export PY_TREE1=$WORK_DIR/py_tree
  $ export PY_TREE2=$WORK_DIR/"py_tree 2"
  $ export PERL_TREE=$WORK_DIR/perl_tree
  $ export OTHER_TREE=$WORK_DIR/other_tree
  $ export PY_REPO_A=$PY_TREE1/repo_a
  $ export PY_REPO_B=$PY_TREE1/subdir/repo_b
  $ export PY_REPO_C="$PY_TREE2/subdir/repo_c"
  $ export PERL_REPO=$PERL_TREE/subdir/repo
  $ export JS_TREE=$WORK_DIR/js
  $ export JS_REPO=$JS_TREE/jrep1
  $ export OTHER_REPO=$OTHER_TREE/repo

First we need appropriate Mercurial configuration file (and variable
which ensures it is used).

  $ export HGRCPATH=$WORK_DIR/hgrc
  $ mkdir -p $HGRCPATH

  $ cat > $HGRCPATH/basic.rc << EOF
  > [ui]
  > username = Just Test <just.text@nowhere.com>
  > logtemplate = {author}: {desc} / {files} [{tags}]\n
  > [extensions]
  > mercurial_update_version =
  > hgext.convert = !
  > [update_version]
  > py_tree.active_on = $PY_TREE1, $PY_TREE2
  > py_tree.language = python
  > py_tree.tagfmt = dotted
  > perl_tree.active_on = $PERL_TREE
  > perl_tree.language = perl
  > perl_tree.tagfmt = pfx-dashed
  > js_tree.active_on = $JS_TREE
  > js_tree.language = javascript
  > js_tree.tagfmt = pfx-dotted
  > EOF

We need some repositories to test.

  $ hg init "$PY_REPO_A"
  $ hg init "$PY_REPO_B"
  $ hg init "$PY_REPO_C"
  $ hg init "$PERL_REPO"
  $ hg init "$OTHER_REPO"
  $ hg init "$JS_REPO"

and let's populate repositories a little bit.

  $ cat > $PY_REPO_A/setup.py <<EOF
  > # This is setup
  > VERSION = "0.0.0"
  > # here it ends
  > EOF

  $ mkdir $PY_REPO_A/src

  $ cat > $PY_REPO_A/src/untouched.py << 'EOF'
  > # This should not change
  > VERSION = "1.0"
  > # Neither this: $Name$
  > EOF

  $ cat > $PY_REPO_A/src/version.py << EOF
  > # This should change
  > VERSION = "1.0"
  > # But this not
  > VERSION = "unchanged"
  > # But this again
  > VERSION = "0.1"
  > EOF

  $ hg --cwd $PY_REPO_A add
  adding setup.py
  adding src/untouched.py
  adding src/version.py
  $ hg --cwd $PY_REPO_A commit -m "Initial commit"

For the sake of bugfixing:

  $ cat $PY_REPO_A/src/untouched.py
  # This should not change
  VERSION = "1.0"
  # Neither this: $Name$

Second:

  $ cat > $PY_REPO_B/__init__.py << EOF
  > # This should change
  > VERSION = "0.0"
  > EOF

  $ cat > $PY_REPO_B/something.pm << EOF
  > VERSION = "0.0"
  > VERSION = "0-0"
  > EOF

  $ hg --cwd $PY_REPO_B add
  adding __init__.py
  adding something.pm
  $ hg --cwd $PY_REPO_B commit -m "Initial commit"

And third:

  $ cat > "$PY_REPO_C/__init__.py" << EOF
  > VERSION = "0.0"
  > EOF

  $ hg --cwd "$PY_REPO_C" add
  adding __init__.py
  $ hg --cwd "$PY_REPO_C" commit -m "Initial commit"

And perl one:

  $ cat > $PERL_REPO/__init__.py << 'EOF'
  > # This should not change
  > VERSION = "0.0"
  > VERSION = "0-0"
  > # Neither this: $Name$
  > EOF

  $ cat > $PERL_REPO/something.pm << EOF
  > # But this
  > VERSION = "0.0"
  > # should
  > VERSION = "0-0"
  > # be done
  > =head1 Blah
  > Version 0.0
  > =cut
  > EOF

  $ hg --cwd $PERL_REPO add
  adding __init__.py
  adding something.pm
  $ hg --cwd $PERL_REPO commit -m "Initial commit"

And js one:

  $ cat > $JS_REPO/package.json << EOF
  > {
  >   "name": "some-module",
  >   "version": "1.0.0",
  >   "description": "Blah blah",
  >   "main": "index.js",
  >   "scripts": {
  >     "test": "echo \"Error: no test specified\" && exit 1"
  >   },
  >   "author": "Johny de Bonny",
  >   "license": "UNLICENSED",
  >   "repository": "https://some/where",
  >   "dependencies": {
  >     "autosize": "^3.0.15",
  >     "handlebars": "^4.0.5",
  >     "jquery": "^2.2.0",
  >   }
  > }
  > EOF

  $ cat > $JS_REPO/other.json << EOF
  > {
  >   "name": "should not change",
  >   "version": "1.0.0",
  > }
  > EOF

  $ cat > $JS_REPO/version.js << EOF
  > // This is some file
  > const VERSION = '0.0';
  > EOF

  $ cat > $JS_REPO/should_not_change.js << EOF
  > // This is some file
  > const VERSION = '0.0';
  > EOF

  $ mkdir -p $JS_REPO/jssubdir
  $ cat > $JS_REPO/jssubdir/mod_version.js << EOF
  > /* blah blah */
  > var APP = '0.7.9';
  > var VERSION = "1.2.3";
  > EOF

  $ cat > $JS_REPO/jssubdir/sth-version.jsx << EOF
  > /* blah blah */
  > let VERSION = "1.2.3";
  > EOF

  $ hg --cwd $JS_REPO add
  adding jssubdir/mod_version.js
  adding jssubdir/sth-version.jsx
  adding other.json
  adding package.json
  adding should_not_change.js
  adding version.js
  $ hg --cwd $JS_REPO commit -m "Initial commit"

And other one:

  $ cat > $OTHER_REPO/__init__.py << EOF
  > VERSION = "0.0"
  > EOF

  $ cat > $OTHER_REPO/something.pm << EOF
  > VERSION = "0.0"
  > VERSION = "0-0"
  > EOF

  $ hg --cwd $OTHER_REPO add
  adding __init__.py
  adding something.pm
  $ hg --cwd $OTHER_REPO commit -m "Initial commit"


Let's try proper tagging on all those repositories:

  $ hg --cwd $PY_REPO_A tag 1.0.1
  update_version: Version number in setup.py set to 1.0.1. List of changes:
      Line 2
      < VERSION = "0.0.0"
      > VERSION = "1.0.1"
  update_version: Version number in src/version.py set to 1.0.1. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "1.0.1"
      Line 6
      < VERSION = "0.1"
      > VERSION = "1.0.1"

  $ hg --cwd $PY_REPO_A status

  $ hg --cwd $PY_REPO_A log
  Just Test <just.text@nowhere.com>: Added tag 1.0.1 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.0.1 / setup.py src/version.py [1.0.1]
  Just Test <just.text@nowhere.com>: Initial commit / setup.py src/untouched.py src/version.py []

  $ cat $PY_REPO_A/setup.py
  # This is setup
  VERSION = "1.0.1"
  # here it ends

  $ cat $PY_REPO_A/src/untouched.py
  # This should not change
  VERSION = "1.0"
  # Neither this: $Name$

  $ cat $PY_REPO_A/src/version.py
  # This should change
  VERSION = "1.0.1"
  # But this not
  VERSION = "unchanged"
  # But this again
  VERSION = "1.0.1"


  $ cd $PY_REPO_B

  $ hg tag 2.3
  update_version: Version number in __init__.py set to 2.3. List of changes:
      Line 2
      < VERSION = "0.0"
      > VERSION = "2.3"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.3 / __init__.py [2.3]
  Just Test <just.text@nowhere.com>: Initial commit / __init__.py something.pm []

  $ cat __init__.py
  # This should change
  VERSION = "2.3"

  $ cat something.pm
  VERSION = "0.0"
  VERSION = "0-0"


  $ cd "$PY_REPO_C"

  $ hg tag 0.0.7.2

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 0.0.7.2 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Initial commit / __init__.py [0.0.7.2]

  $ cat __init__.py
  VERSION = "0.0"


  $ cd $PERL_REPO

  $ hg tag mylib_0-3
  update_version: Version number in something.pm set to 0.3. List of changes:
      Line 7
      < Version 0.0
      > Version 0.3

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag mylib_0-3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 0.3 / something.pm [mylib_0-3]
  Just Test <just.text@nowhere.com>: Initial commit / __init__.py something.pm []

  $ cat __init__.py
  # This should not change
  VERSION = "0.0"
  VERSION = "0-0"
  # Neither this: $Name$

  $ cat something.pm
  # But this
  VERSION = "0.0"
  # should
  VERSION = "0-0"
  # be done
  =head1 Blah
  Version 0.3
  =cut

  $ hg tag mylib_71-143
  update_version: Version number in something.pm set to 71.143. List of changes:
      Line 7
      < Version 0.3
      > Version 71.143

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag mylib_71-143 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 71.143 / something.pm [mylib_71-143]
  Just Test <just.text@nowhere.com>: Added tag mylib_0-3 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 0.3 / something.pm [mylib_0-3]
  Just Test <just.text@nowhere.com>: Initial commit / __init__.py something.pm []

  $ cd $OTHER_REPO

  $ hg tag mylib_0-3

  $ hg tag 0.4

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 0.4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Added tag mylib_0-3 for changeset * / .hgtags [0.4] (glob)
  Just Test <just.text@nowhere.com>: Initial commit / __init__.py something.pm [mylib_0-3]

  $ cat __init__.py
  VERSION = "0.0"

  $ cat something.pm
  VERSION = "0.0"
  VERSION = "0-0"



  $ cd $JS_REPO

  $ hg tag mylib-0.7.4
  update_version: Version number in jssubdir/mod_version.js set to 0.7.4. List of changes:
      Line 3
      < var VERSION = "1.2.3";
      > var VERSION = "0.7.4";
  update_version: Version number in jssubdir/sth-version.jsx set to 0.7.4. List of changes:
      Line 2
      < let VERSION = "1.2.3";
      > let VERSION = "0.7.4";
  update_version: Version number in package.json set to 0.7.4. List of changes:
      Line 3
      <   "version": "1.0.0",
      >   "version": "0.7.4",
  update_version: Version number in version.js set to 0.7.4. List of changes:
      Line 2
      < const VERSION = '0.0';
      > const VERSION = '0.7.4';

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag mylib-0.7.4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 0.7.4 / jssubdir/mod_version.js jssubdir/sth-version.jsx package.json version.js [mylib-0.7.4]
  Just Test <just.text@nowhere.com>: Initial commit / jssubdir/mod_version.js jssubdir/sth-version.jsx other.json package.json should_not_change.js version.js []

  $ cat package.json
  {
    "name": "some-module",
    "version": "0.7.4",
    "description": "Blah blah",
    "main": "index.js",
    "scripts": {
      "test": "echo \"Error: no test specified\" && exit 1"
    },
    "author": "Johny de Bonny",
    "license": "UNLICENSED",
    "repository": "https://some/where",
    "dependencies": {
      "autosize": "^3.0.15",
      "handlebars": "^4.0.5",
      "jquery": "^2.2.0",
    }
  }

  $ cat other.json
  {
    "name": "should not change",
    "version": "1.0.0",
  }

  $ cat version.js
  // This is some file
  const VERSION = '0.7.4';

  $ cat should_not_change.js
  // This is some file
  const VERSION = '0.0';

  $ cat jssubdir/mod_version.js
  /* blah blah */
  var APP = '0.7.9';
  var VERSION = "0.7.4";

  $ cat jssubdir/sth-version.jsx
  /* blah blah */
  let VERSION = "0.7.4";

