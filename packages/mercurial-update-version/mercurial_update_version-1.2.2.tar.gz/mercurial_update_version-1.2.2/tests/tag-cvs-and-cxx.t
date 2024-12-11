
Let's test mixing CVS keywords and normal constants in the same code.

Let's define test locations

  $ WORK_DIR=${WORK_DIR-`pwd`/work}
  $ rm -rf $WORK_DIR

  $ export EXCVS_TREE=$WORK_DIR/excvs_tree
  $ export REPO=$EXCVS_TREE/repo

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
  > excvs_tree.active_on = $EXCVS_TREE
  > excvs_tree.expand_keywords = 1
  > excvs_tree.language = c++
  > excvs_tree.tagfmt = pfx-dashed
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository a little bit.

  $ cat > $REPO/somefile.cxx <<'EOF'
  > // This is some file
  > // $Name$
  > // $Date$
  > // $Header$
  > // $Id$
  > // $Revision$
  > // $Source$
  > //
  > // This should not chane
  > const string VERSION = "unchanged";
  > EOF

  $ mkdir -p $REPO/src

  $ cat > $REPO/src/version.cxx <<'EOF'
  > // Another file
  > // $Name$
  > // But this should
  > const string VERSION = "1.0.2";
  > const string VERSION("1.0.2");
  > const char *VERSION = "1.0.2";
  > const  char*  VERSION = "1.0.2";
  > string VERSION = "1.0.2";
  > // And this should not
  > const string VER = "1.0.2";
  > const string VER("1.0.2");
  > const char *VER = "1.0.2";
  > // here it ends
  > EOF

  $ cat > $REPO/src/untouched.cxx <<'EOF'
  > // This should not change
  > string VERSION = "1.0";
  > EOF

  $ hg --cwd $REPO add
  adding somefile.cxx
  adding src/untouched.cxx
  adding src/version.cxx

  $ hg --cwd $REPO commit -m "Initial commit"

  $ cat > $REPO/src/version.hxx <<'EOF'
  > // Yet another things to change
  > const string VERSION = "1.0.2";
  > EOF

  $ cat > $REPO/src/version.hpp <<'EOF'
  > // Yet another things to change
  > const string VERSION = "1.0";
  > char VERSION[] = "1.2.3";
  > EOF

  $ cat > $REPO/src/version.cpp <<'EOF'
  > // Yet another things to change
  > const string VERSION = "1.0";
  > const char VERSION[] = "1.2.3";
  > EOF

  $ hg --cwd $REPO add
  adding src/version.cpp
  adding src/version.hpp
  adding src/version.hxx
  $ hg --cwd $REPO commit -m "Second commit"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Second commit / src/version.cpp src/version.hpp src/version.hxx [tip]
  Just Test <just.text@nowhere.com>: Initial commit / somefile.cxx src/untouched.cxx src/version.cxx []

Let's tag:

  $ hg tag ver_1-1-0
  update_version: Version number in src/version.cpp set to 1.1.0. List of changes:
      Line 2
      < const string VERSION = "1.0";
      > const string VERSION = "1.1.0";
      Line 3
      < const char VERSION[] = "1.2.3";
      > const char VERSION[] = "1.1.0";
  update_version: Version number in src/version.cxx set to 1.1.0. List of changes:
      Line 4
      < const string VERSION = "1.0.2";
      > const string VERSION = "1.1.0";
      Line 5
      < const string VERSION("1.0.2");
      > const string VERSION("1.1.0");
      Line 6
      < const char *VERSION = "1.0.2";
      > const char *VERSION = "1.1.0";
      Line 7
      < const  char*  VERSION = "1.0.2";
      > const  char*  VERSION = "1.1.0";
      Line 8
      < string VERSION = "1.0.2";
      > string VERSION = "1.1.0";
  update_version: Version number in src/version.hpp set to 1.1.0. List of changes:
      Line 2
      < const string VERSION = "1.0";
      > const string VERSION = "1.1.0";
      Line 3
      < char VERSION[] = "1.2.3";
      > char VERSION[] = "1.1.0";
  update_version: Version number in src/version.hxx set to 1.1.0. List of changes:
      Line 2
      < const string VERSION = "1.0.2";
      > const string VERSION = "1.1.0";
  update_version: CVS keywords expanded in somefile.cxx src/version.cxx

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-1-0 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.1.0 / somefile.cxx src/version.cpp src/version.cxx src/version.hpp src/version.hxx [ver_1-1-0]
  Just Test <just.text@nowhere.com>: Second commit / src/version.cpp src/version.hpp src/version.hxx []
  Just Test <just.text@nowhere.com>: Initial commit / somefile.cxx src/untouched.cxx src/version.cxx []

And some testing:

  $ cat src/version.cxx
  // Another file
  // $Name: ver_1-1-0 $
  // But this should
  const string VERSION = "1.1.0";
  const string VERSION("1.1.0");
  const char *VERSION = "1.1.0";
  const  char*  VERSION = "1.1.0";
  string VERSION = "1.1.0";
  // And this should not
  const string VER = "1.0.2";
  const string VER("1.0.2");
  const char *VER = "1.0.2";
  // here it ends

  $ cat src/version.hxx
  // Yet another things to change
  const string VERSION = "1.1.0";

  $ cat src/version.cpp
  // Yet another things to change
  const string VERSION = "1.1.0";
  const char VERSION[] = "1.1.0";

  $ cat src/version.hpp
  // Yet another things to change
  const string VERSION = "1.1.0";
  char VERSION[] = "1.1.0";

  $ cat src/untouched.cxx
  // This should not change
  string VERSION = "1.0";

  $ cat somefile.cxx
  // This is some file
  // $Name: ver_1-1-0 $
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: somefile.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: somefile.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: somefile.cxx,v $
  //
  // This should not chane
  const string VERSION = "unchanged";

And again:

  $ hg tag ver_1-0-4
  update_version: Version number in src/version.cpp set to 1.0.4. List of changes:
      Line 2
      < const string VERSION = "1.1.0";
      > const string VERSION = "1.0.4";
      Line 3
      < const char VERSION[] = "1.1.0";
      > const char VERSION[] = "1.0.4";
  update_version: Version number in src/version.cxx set to 1.0.4. List of changes:
      Line 4
      < const string VERSION = "1.1.0";
      > const string VERSION = "1.0.4";
      Line 5
      < const string VERSION("1.1.0");
      > const string VERSION("1.0.4");
      Line 6
      < const char *VERSION = "1.1.0";
      > const char *VERSION = "1.0.4";
      Line 7
      < const  char*  VERSION = "1.1.0";
      > const  char*  VERSION = "1.0.4";
      Line 8
      < string VERSION = "1.1.0";
      > string VERSION = "1.0.4";
  update_version: Version number in src/version.hpp set to 1.0.4. List of changes:
      Line 2
      < const string VERSION = "1.1.0";
      > const string VERSION = "1.0.4";
      Line 3
      < char VERSION[] = "1.1.0";
      > char VERSION[] = "1.0.4";
  update_version: Version number in src/version.hxx set to 1.0.4. List of changes:
      Line 2
      < const string VERSION = "1.1.0";
      > const string VERSION = "1.0.4";
  update_version: CVS keywords expanded in somefile.cxx src/version.cxx

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.0.4 / somefile.cxx src/version.cpp src/version.cxx src/version.hpp src/version.hxx [ver_1-0-4]
  Just Test <just.text@nowhere.com>: Added tag ver_1-1-0 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.1.0 / somefile.cxx src/version.cpp src/version.cxx src/version.hpp src/version.hxx [ver_1-1-0]
  Just Test <just.text@nowhere.com>: Second commit / src/version.cpp src/version.hpp src/version.hxx []
  Just Test <just.text@nowhere.com>: Initial commit / somefile.cxx src/untouched.cxx src/version.cxx []

  $ cat somefile.cxx
  // This is some file
  // $Name: ver_1-0-4 $
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: somefile.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: somefile.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: somefile.cxx,v $
  //
  // This should not chane
  const string VERSION = "unchanged";

  $ cat src/version.cxx
  // Another file
  // $Name: ver_1-0-4 $
  // But this should
  const string VERSION = "1.0.4";
  const string VERSION("1.0.4");
  const char *VERSION = "1.0.4";
  const  char*  VERSION = "1.0.4";
  string VERSION = "1.0.4";
  // And this should not
  const string VER = "1.0.2";
  const string VER("1.0.2");
  const char *VER = "1.0.2";
  // here it ends

  $ cat src/version.hxx
  // Yet another things to change
  const string VERSION = "1.0.4";

  $ cat src/version.cpp
  // Yet another things to change
  const string VERSION = "1.0.4";
  const char VERSION[] = "1.0.4";

  $ cat src/version.hpp
  // Yet another things to change
  const string VERSION = "1.0.4";
  char VERSION[] = "1.0.4";

  $ cat src/untouched.cxx
  // This should not change
  string VERSION = "1.0";

