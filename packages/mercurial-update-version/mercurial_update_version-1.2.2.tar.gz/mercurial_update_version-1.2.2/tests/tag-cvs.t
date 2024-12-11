We will test reactions to various tag placing methods.

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
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository a little bit.

  $ cat > $REPO/setup.cxx <<'EOF'
  > // This is some file
  > // $Name$
  > // $Date$
  > // $Header$
  > // $Id$
  > // $Revision$
  > // $Source$
  > //
  > // Let's try again, using constants and expanded versions
  > const string Name = "$Name: ver_1-3-7 $";
  > const string Date = "$Date: 2003/11/20 21:17:14 $";
  > const string Header = "$Header: /some/where/sth.cxx,v 1.3 1999/12/23 21:59:22 markd Exp $";
  > const string Id = "$Id: keyword.html,v 1.3 1999/12/23 21:59:22 markd Exp $";
  > const string Rev = "$Revision: 1.3 $";
  > const string Source = "$Source: /some/where/sth.cxx,v $";
  > //
  > // here it ends
  > EOF

  $ mkdir $REPO/src

  $ cat > $REPO/src/another.cxx <<'EOF'
  > // Another file
  > // $Date$
  > // $Header$
  > // $Id$
  > // $Name$
  > // $Revision$
  > // $Source$
  > // Let's try again, using constants and expanded versions
  > const string Id = "$Id: keyword.html,v 1.3 1999/12/23 21:59:22 markd Exp $";
  > const string Rev = "$Revision: 1.3 $";
  > const string Source = "$Source: /some/where/sth.cxx,v $";
  > const string Name = "$Name: ver_1-3-7 $";
  > const string Date = "$Date: 2003/11/20 21:17:14 $";
  > const string Header = "$Header: /some/where/sth.cxx,v 1.3 1999/12/23 21:59:22 markd Exp $";
  > // here it ends
  > EOF

  $ cat > $REPO/src/untouched.cxx <<'EOF'
  > // This should not change
  > VERSION = "1.0";
  > EOF

  $ hg --cwd $REPO add
  adding setup.cxx
  adding src/another.cxx
  adding src/untouched.cxx
  $ hg --cwd $REPO commit -m "Initial commit"

  $ cat > $REPO/src/third.cxx <<'EOF'
  > // This is some file
  > // $Date$
  > // $Name$
  > // $Revision$
  > EOF

  $ hg --cwd $REPO add
  adding src/third.cxx
  $ hg --cwd $REPO commit -m "Second commit"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx [tip]
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

Let's tag:

  $ hg tag ver_1-0-2
  update_version: CVS keywords expanded in setup.cxx src/another.cxx src/third.cxx

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-2 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-2 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-2]
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx []
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

  $ cat setup.cxx
  // This is some file
  // $Name: ver_1-0-2 $
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: setup.cxx,v $
  //
  // Let's try again, using constants and expanded versions
  const string Name = "$Name: ver_1-0-2 $";
  const string Date = "\$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$"; (re)
  const string Header = "\$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Id = "\$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Rev = "\$Revision: [a-f0-9]{12} \$"; (re)
  const string Source = "$Source: setup.cxx,v $";
  //
  // here it ends

  $ cat src/third.cxx
  // This is some file
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // $Name: ver_1-0-2 $
  // \$Revision: [a-f0-9]{12} \$ (re)

  $ cat src/untouched.cxx
  // This should not change
  VERSION = "1.0";

  $ cat src/another.cxx
  // Another file
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: src/another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // $Name: ver_1-0-2 $
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: src/another.cxx,v $
  // Let's try again, using constants and expanded versions
  const string Id = "\$Id: another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Rev = "\$Revision: [a-f0-9]{12} \$"; (re)
  const string Source = "$Source: src/another.cxx,v $";
  const string Name = "$Name: ver_1-0-2 $";
  const string Date = "\$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$"; (re)
  const string Header = "\$Header: src/another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  // here it ends

And again:

  $ hg tag ver_1-0-4
  update_version: CVS keywords expanded in setup.cxx src/another.cxx src/third.cxx

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-4]
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-2 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-2 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-2]
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx []
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

  $ cat setup.cxx
  // This is some file
  // $Name: ver_1-0-4 $
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: setup.cxx,v $
  //
  // Let's try again, using constants and expanded versions
  const string Name = "$Name: ver_1-0-4 $";
  const string Date = "\$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$"; (re)
  const string Header = "\$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Id = "\$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Rev = "\$Revision: [a-f0-9]{12} \$"; (re)
  const string Source = "$Source: setup.cxx,v $";
  //
  // here it ends

  $ cat src/third.cxx
  // This is some file
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // $Name: ver_1-0-4 $
  // \$Revision: [a-f0-9]{12} \$ (re)

  $ cat src/untouched.cxx
  // This should not change
  VERSION = "1.0";

  $ cat src/another.cxx
  // Another file
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: src/another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // $Name: ver_1-0-4 $
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: src/another.cxx,v $
  // Let's try again, using constants and expanded versions
  const string Id = "\$Id: another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Rev = "\$Revision: [a-f0-9]{12} \$"; (re)
  const string Source = "$Source: src/another.cxx,v $";
  const string Name = "$Name: ver_1-0-4 $";
  const string Date = "\$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$"; (re)
  const string Header = "\$Header: src/another.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  // here it ends

Local tags shouldn't work:

  $ hg tag --local 77.77.77
  update_version: ignoring local tag (version number not updated)

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [77.77.77 tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-4]
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-2 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-2 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-2]
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx []
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

Re-tagging unchanged files

  $ hg tag -f ver_1-0-4
  update_version: CVS keywords expanded in setup.cxx src/another.cxx src/third.cxx

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-4]
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx []
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-2 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-2 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-2]
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx []
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

But later on:

  $ echo "XXX" >> setup.cxx
  $ hg commit -m "Dummy X"

  $ hg tag -f 2.0
  update_version: CVS keywords expanded in setup.cxx src/another.cxx src/third.cxx
 
  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 2.0 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 2.0 / setup.cxx src/another.cxx src/third.cxx [2.0]
  Just Test <just.text@nowhere.com>: Dummy X / setup.cxx []
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-4]
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-4 for changeset * / .hgtags [77.77.77] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-4 / setup.cxx src/another.cxx src/third.cxx []
  Just Test <just.text@nowhere.com>: Added tag ver_1-0-2 for changeset * / .hgtags [] (glob)
  Just Test <just.text@nowhere.com>: Version number set to ver_1-0-2 / setup.cxx src/another.cxx src/third.cxx [ver_1-0-2]
  Just Test <just.text@nowhere.com>: Second commit / src/third.cxx []
  Just Test <just.text@nowhere.com>: Initial commit / setup.cxx src/another.cxx src/untouched.cxx []

  $ cat setup.cxx
  // This is some file
  // $Name: 2.0 $
  // \$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$ (re)
  // \$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$ (re)
  // \$Revision: [a-f0-9]{12} \$ (re)
  // $Source: setup.cxx,v $
  //
  // Let's try again, using constants and expanded versions
  const string Name = "$Name: 2.0 $";
  const string Date = "\$Date: 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} \$"; (re)
  const string Header = "\$Header: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Id = "\$Id: setup.cxx,v [a-f0-9]{12} 2\d{3}/[01]\d/[0-3]\d [012]\d:\d{2}:\d{2} just Exp \$"; (re)
  const string Rev = "\$Revision: [a-f0-9]{12} \$"; (re)
  const string Source = "$Source: setup.cxx,v $";
  //
  // here it ends
  XXX