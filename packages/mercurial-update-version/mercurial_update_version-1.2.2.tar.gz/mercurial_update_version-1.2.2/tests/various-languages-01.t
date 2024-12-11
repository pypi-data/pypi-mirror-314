Attempt to verify all languages we have, and all syntaxes we have for
them. Simultaneously.

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
  > py.active_on = $TREE
  > py.language = python
  > py.tagfmt = dotted
  > js.active_on = $TREE
  > js.language = javascript
  > js.tagfmt = dotted
  > prl.active_on = $TREE
  > prl.language = perl
  > prl.tagfmt = dotted
  > cxx.active_on = $TREE
  > cxx.language = c++
  > cxx.tagfmt = dotted
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository with all the files we need to patch
(and a few to be kept intact).

- Python

  $ cat > $REPO/setup.py <<EOF
  > # This is setup
  > VERSION = "1.0"
  > # here it ends
  > EOF

  $ mkdir -p $REPO/src

  $ cat > $REPO/src/version.py << 'EOF'
  > VERSION = "1.0"
  > EOF

  $ cat > $REPO/src/__init__.py << 'EOF'
  > IRRE = "levant"
  > VERSION = "1.0"
  > # Good bye
  > EOF

  $ cat > $REPO/src/do_not_touch.py << 'EOF'
  > # This should not change:
  > VERSION = "1.0"
  > # Good bye
  > EOF


- Perl

  $ cat > $REPO/something.pm << 'EOF'
  > # This
  > our $VERSION = "0.00";
  > # should
  > my $VERSION = "0.0";
  > # be done
  > =head1 Blah
  > Version 0.0
  > =cut
  > EOF

  $ cat > $REPO/hello.pod << EOF
  > =head1 Hello
  > 
  > Well, hello.
  > 
  > Version 0.0
  > 
  > =cut
  > EOF

  $ cat > $REPO/dist.ini << EOF
  > name             = Blah
  > version          = 0.0
  > license          = Perl_5
  > 
  > [GatherDir]
  > include_dotfiles = 0
  > EOF


- JavaScript

  $ cat > $REPO/version.js << 'EOF'
  > /* This should be updated */
  > const VERSION = "1.0";
  > EOF

  $ cat > $REPO/package.json << 'EOF'
  > {"name":"abcde","description":"Some module",
  > "version":"1.0",
  > "main":"abcde.js"}
  > EOF

  $ mkdir -p $REPO/some/dir
  $ cat > $REPO/some/dir/item_version.jsx << 'EOF'
  > /* This should be updated too */
  > let VERSION = "1.0";
  > EOF

  $ cat > $REPO/other.js << 'EOF'
  > /* But this should not change */
  > VERSION = "1.0";
  > EOF


- C++

  $ cat > $REPO/version.hxx << 'EOF'
  > #include <string>
  > const string VERSION = "1.0";
  > EOF

  $ cat > $REPO/some/dir/version.cxx << 'EOF'
  > #include <string>
  > const char* VERSION = "1.0";
  > EOF

  $ cat > $REPO/do_not_touch_me.cxx << 'EOF'
  > /* Should not change */
  > const char* VERSION = "1.0";
  > EOF


OK, it's time to act. 

  $ cd $REPO

  $ hg add
  adding dist.ini
  adding do_not_touch_me.cxx
  adding hello.pod
  adding other.js
  adding package.json
  adding setup.py
  adding some/dir/item_version.jsx
  adding some/dir/version.cxx
  adding something.pm
  adding src/__init__.py
  adding src/do_not_touch.py
  adding src/version.py
  adding version.hxx
  adding version.js

  $ hg commit -m "Initial commit"

  $ hg tag 1.2.3
  update_version: Version number in setup.py set to 1.2.3. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "1.2.3"
  update_version: Version number in src/__init__.py set to 1.2.3. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "1.2.3"
  update_version: Version number in src/version.py set to 1.2.3. List of changes:
      Line 1
      < VERSION = "1.0"
      > VERSION = "1.2.3"
  update_version: Version number in package.json set to 1.2.3. List of changes:
      Line 2
      < "version":"1.0",
      > "version":"1.2.3",
  update_version: Version number in some/dir/item_version.jsx set to 1.2.3. List of changes:
      Line 2
      < let VERSION = "1.0";
      > let VERSION = "1.2.3";
  update_version: Version number in version.js set to 1.2.3. List of changes:
      Line 2
      < const VERSION = "1.0";
      > const VERSION = "1.2.3";
  update_version: Version number in dist.ini set to 1.0203. List of changes:
      Line 2
      < version          = 0.0
      > version          = 1.0203
  update_version: Version number in hello.pod set to 1.0203. List of changes:
      Line 5
      < Version 0.0
      > Version 1.0203
  update_version: Version number in something.pm set to 1.0203. List of changes:
      Line 2
      < our $VERSION = "0.00";
      > our $VERSION = "1.0203";
      Line 4
      < my $VERSION = "0.0";
      > my $VERSION = "1.0203";
      Line 7
      < Version 0.0
      > Version 1.0203
  update_version: Version number in some/dir/version.cxx set to 1.2.3. List of changes:
      Line 2
      < const char* VERSION = "1.0";
      > const char* VERSION = "1.2.3";
  update_version: Version number in version.hxx set to 1.2.3. List of changes:
      Line 2
      < const string VERSION = "1.0";
      > const string VERSION = "1.2.3";

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 1.2.3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.2.3 / dist.ini hello.pod package.json setup.py some/dir/item_version.jsx some/dir/version.cxx something.pm src/__init__.py src/version.py version.hxx version.js [1.2.3]
  Just Test <just.text@nowhere.com>: Initial commit / .* (re)

  $ cat setup.py
  # This is setup
  VERSION = "1.2.3"
  # here it ends

  $ cat src/version.py
  VERSION = "1.2.3"

  $ cat src/__init__.py
  IRRE = "levant"
  VERSION = "1.2.3"
  # Good bye

  $ cat src/do_not_touch.py
  # This should not change:
  VERSION = "1.0"
  # Good bye

  $ cat something.pm
  # This
  our $VERSION = "1.0203";
  # should
  my $VERSION = "1.0203";
  # be done
  =head1 Blah
  Version 1.0203
  =cut

  $ cat dist.ini
  name             = Blah
  version          = 1.0203
  license          = Perl_5
  
  [GatherDir]
  include_dotfiles = 0

  $ cat version.js
  /* This should be updated */
  const VERSION = "1.2.3";

  $ cat package.json
  {"name":"abcde","description":"Some module",
  "version":"1.2.3",
  "main":"abcde.js"}

  $ mkdir -p $REPO/some/dir
  $ cat some/dir/item_version.jsx
  /* This should be updated too */
  let VERSION = "1.2.3";

  $ cat other.js
  /* But this should not change */
  VERSION = "1.0";







  $ hg tag_version_test 4.5.7
  update_version: using python language rules and dotted tag format
  update_version: using javascript language rules and dotted tag format
  update_version: using perl language rules and dotted tag format
  update_version: using c++ language rules and dotted tag format
  update_version: Version number in setup.py set to 4.5.7. List of changes:
      Line 2
      < VERSION = "1.2.3"
      > VERSION = "4.5.7"
  update_version: Version number in src/__init__.py set to 4.5.7. List of changes:
      Line 2
      < VERSION = "1.2.3"
      > VERSION = "4.5.7"
  update_version: Version number in src/version.py set to 4.5.7. List of changes:
      Line 1
      < VERSION = "1.2.3"
      > VERSION = "4.5.7"
  update_version: Version number in package.json set to 4.5.7. List of changes:
      Line 2
      < "version":"1.2.3",
      > "version":"4.5.7",
  update_version: Version number in some/dir/item_version.jsx set to 4.5.7. List of changes:
      Line 2
      < let VERSION = "1.2.3";
      > let VERSION = "4.5.7";
  update_version: Version number in version.js set to 4.5.7. List of changes:
      Line 2
      < const VERSION = "1.2.3";
      > const VERSION = "4.5.7";
  update_version: Version number in dist.ini set to 4.0507. List of changes:
      Line 2
      < version          = 1.0203
      > version          = 4.0507
  update_version: Version number in hello.pod set to 4.0507. List of changes:
      Line 5
      < Version 1.0203
      > Version 4.0507
  update_version: Version number in something.pm set to 4.0507. List of changes:
      Line 2
      < our $VERSION = "1.0203";
      > our $VERSION = "4.0507";
      Line 4
      < my $VERSION = "1.0203";
      > my $VERSION = "4.0507";
      Line 7
      < Version 1.0203
      > Version 4.0507
  update_version: Version number in some/dir/version.cxx set to 4.5.7. List of changes:
      Line 2
      < const char* VERSION = "1.2.3";
      > const char* VERSION = "4.5.7";
  update_version: Version number in version.hxx set to 4.5.7. List of changes:
      Line 2
      < const string VERSION = "1.2.3";
      > const string VERSION = "4.5.7";

