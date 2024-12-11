
Followup to various-languages.t, a few more.


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
  > jsn.active_on = $TREE
  > jsn.language = json
  > jsn.tagfmt = dotted
  > lgst.active_on = $TREE
  > lgst.language = logstash
  > lgst.tagfmt = dotted
  > EOF

We need some repository for test.

  $ hg init $REPO

Let's move to repo:

  $ cd $REPO

and let's populate repository with all the files we need to patch
(and a few to be kept intact).

- JSON

  $ cat > $REPO/dummy.json <<EOF
  > {"name":"abcde",
  > "version":"1.0",
  > "items":["abcde.js"]}
  > EOF

  $ mkdir -p sub/dir

  $ cat > $REPO/sub/dir/another.json <<EOF
  > {
  >     "version":"1.0",
  >     "items":["abcde.js"],
  >     "child-with-unchanged": {
  >         "version": "0.1"
  >     }
  > }
  > EOF


- Logstash

  $ cat > $REPO/sth-version.conf <<'EOF'
  >    mutate {
  >        add_field  =>  { "[@metadata][version]" => "1.0" }
  >        gsub => { "message", "\n\n+", "\n" }
  >        add_field => { "[version]" => '1.0' }
  >    add_field => {'[yet][another][version]'=>"1.0"}
  >    }
  > EOF

  $ cat > $REPO/untouched.conf <<'EOF'
  >    mutate {
  >        add_field  =>  { "[@metadata][version]" => "1.0" }
  >    }
  > EOF

  $ cat > $REPO/sub/dir/version.conf <<'EOF'
  >    mutate {
  >        add_field  =>  { "[@metadata][version]" => "1.0" }
  >    }
  > EOF

OK, it's time to act. 

  $ cd $REPO

  $ hg add
  adding dummy.json
  adding sth-version.conf
  adding sub/dir/another.json
  adding sub/dir/version.conf
  adding untouched.conf
 
  $ hg commit -m "Initial commit"

  $ hg tag 1.2.3
  update_version: Version number in dummy.json set to 1.2.3. List of changes:
      Line 2
      < "version":"1.0",
      > "version":"1.2.3",
  update_version: Version number in sub/dir/another.json set to 1.2.3. List of changes:
      Line 2
      <     "version":"1.0",
      >     "version":"1.2.3",
  update_version: Version number in sth-version.conf set to 1.2.3. List of changes:
      Line 2
      <        add_field  =>  { "[@metadata][version]" => "1.0" }
      >        add_field  =>  { "[@metadata][version]" => "1.2.3" }
      Line 4
      <        add_field => { "[version]" => '1.0' }
      >        add_field => { "[version]" => '1.2.3' }
      Line 5
      <    add_field => {'[yet][another][version]'=>"1.0"}
      >    add_field => {'[yet][another][version]'=>"1.2.3"}
  update_version: Version number in sub/dir/version.conf set to 1.2.3. List of changes:
      Line 2
      <        add_field  =>  { "[@metadata][version]" => "1.0" }
      >        add_field  =>  { "[@metadata][version]" => "1.2.3" }

  $ hg status

  $ hg log
  Just Test <just.text@nowhere.com>: Added tag 1.2.3 for changeset * / .hgtags [tip] (glob)
  Just Test <just.text@nowhere.com>: Version number set to 1.2.3 / dummy.json sth-version.conf sub/dir/another.json sub/dir/version.conf [1.2.3]
  Just Test <just.text@nowhere.com>: Initial commit / dummy.json sth-version.conf sub/dir/another.json sub/dir/version.conf untouched.conf []

  $ cat dummy.json
  {"name":"abcde",
  "version":"1.2.3",
  "items":["abcde.js"]}

  $ cat sub/dir/another.json
  {
      "version":"1.2.3",
      "items":["abcde.js"],
      "child-with-unchanged": {
          "version": "0.1"
      }
  }

  $ cat sth-version.conf
     mutate {
         add_field  =>  { "[@metadata][version]" => "1.2.3" }
         gsub => { "message", "\n\n+", "\n" }
         add_field => { "[version]" => '1.2.3' }
     add_field => {'[yet][another][version]'=>"1.2.3"}
     }

  $ cat sub/dir/version.conf
     mutate {
         add_field  =>  { "[@metadata][version]" => "1.2.3" }
     }

  $ cat untouched.conf
     mutate {
         add_field  =>  { "[@metadata][version]" => "1.0" }
     }

And one more tag

  $ hg tag 7.0.1
  update_version: Version number in dummy.json set to 7.0.1. List of changes:
      Line 2
      < "version":"1.2.3",
      > "version":"7.0.1",
  update_version: Version number in sub/dir/another.json set to 7.0.1. List of changes:
      Line 2
      <     "version":"1.2.3",
      >     "version":"7.0.1",
  update_version: Version number in sth-version.conf set to 7.0.1. List of changes:
      Line 2
      <        add_field  =>  { "[@metadata][version]" => "1.2.3" }
      >        add_field  =>  { "[@metadata][version]" => "7.0.1" }
      Line 4
      <        add_field => { "[version]" => '1.2.3' }
      >        add_field => { "[version]" => '7.0.1' }
      Line 5
      <    add_field => {'[yet][another][version]'=>"1.2.3"}
      >    add_field => {'[yet][another][version]'=>"7.0.1"}
  update_version: Version number in sub/dir/version.conf set to 7.0.1. List of changes:
      Line 2
      <        add_field  =>  { "[@metadata][version]" => "1.2.3" }
      >        add_field  =>  { "[@metadata][version]" => "7.0.1" }

