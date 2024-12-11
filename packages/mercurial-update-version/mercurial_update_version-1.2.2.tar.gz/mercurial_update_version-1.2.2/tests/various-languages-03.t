

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
  > yml.active_on = $TREE
  > yml.language = yaml
  > yml.tagfmt = dotted
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository with all the files we need to patch
(and a few to be kept intact).

- JSON

  $ cat > $REPO/dummy.yaml <<EOF
  > name: something
  > version: 1.2
  > items:["abcde.js"]
  > extra:
  >    version: "9.9"
  > EOF

  $ mkdir -p sub/dir

  $ cat > $REPO/sub/dir/another.yaml <<EOF
  > # version: "0.0.0"
  > package_name: something
  > package_version: "1.3.2"
  > module:
  >   name: aaa
  >   version: 1.2.3
  >   package_version: "4.5.6"
  > EOF

  $ cat > $REPO/untouched.yaml <<EOF
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > # filler
  > name: something
  > version: "1.2"
  > EOF

OK, it's time to act. 

  $ cd $REPO

  $ hg add
  adding dummy.yaml
  adding sub/dir/another.yaml
  adding untouched.yaml

  $ hg commit -m "Initial commit"

  $ hg tag 11.22.33
  update_version: Version number in dummy.yaml set to 11.22.33. List of changes:
      Line 2
      < version: 1.2
      > version: 11.22.33
  update_version: Version number in sub/dir/another.yaml set to 11.22.33. List of changes:
      Line 3
      < package_version: "1.3.2"
      > package_version: "11.22.33"

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 11.22.33 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 11.22.33 / dummy.yaml sub/dir/another.yaml [11.22.33]
  Just Test <just.text@nowhere.com>: Initial commit / dummy.yaml sub/dir/another.yaml untouched.yaml []

  $ cat dummy.yaml
  name: something
  version: 11.22.33
  items:["abcde.js"]
  extra:
     version: "9.9"

  $ cat sub/dir/another.yaml
  # version: "0.0.0"
  package_name: something
  package_version: "11.22.33"
  module:
    name: aaa
    version: 1.2.3
    package_version: "4.5.6"

  $ cat untouched.yaml
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  # filler
  name: something
  version: "1.2"

And one more tag

  $ hg tag 7.0.1
  update_version: Version number in dummy.yaml set to 7.0.1. List of changes:
      Line 2
      < version: 11.22.33
      > version: 7.0.1
  update_version: Version number in sub/dir/another.yaml set to 7.0.1. List of changes:
      Line 3
      < package_version: "11.22.33"
      > package_version: "7.0.1"

