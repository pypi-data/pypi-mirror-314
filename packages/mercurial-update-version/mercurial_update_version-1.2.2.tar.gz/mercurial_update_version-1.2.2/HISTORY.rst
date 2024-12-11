1.2.2
~~~~~~~~~~~~

For python maximal size of checked files increased to 128kB
(16kB happens to be to restrictive for some setup.py and __init__.py)


1.2.1
~~~~~~~~~~~~

Tested up to 6.8. Tests migrated tox → nox.

1.2.0
~~~~~~~~~~~~

Added yaml language (scanning for first key of version:, package_version:, or
module_version: in leading lines of .yml/.yaml files).

Tested against hg 6.0 (and some other newer mercurials).

1.1.1
~~~~~~~~~~~~

Fixing various links as Atlassian killed Bitbucket.
Testing against hg 5.3 and 5.4.

1.1.0
~~~~~~~~~~~~

Should work under python3-based Mercurial installs (without breaking
python2 support). 

Tested against hg 5.1 and 5.2. 

1.0.0
~~~~~~~~~~~~

Support for multiple rules in single-repo configuration case
(«prefix».active + «prefix».language + …).

Support for two new languages: logstash and json.

Formally tested against Mercurial 4.9.

Nicer version number.

0.8.4
~~~~~~~~~~~~

Tested against hg 4.8 (no changes needed).

0.8.3
~~~~~~~~~~~~~

Fixed incompatibility with hg 4.7 (which caused technical
error in case cvs keywords mode was in use).

0.8.2
~~~~~~~~~~~~~

Formally tested with hg 4.5 and 4.6, small 4.6 fixes.

0.8.0
~~~~~~~~~~~~~

#3 In case multiple tree definitions match given repo, all are
processed, instead of just the first one.

0.7.4
~~~~~~~~~~~~~

Updated links after bitbucket changes.

hg 4.1 and 4.2 added to tested versions.

Some tests (test-cvs*) were failing if executed between 10-th and 29-th
day of the month (buggy date regexp).

0.7.3
~~~~~~~~~~~~~~~~~~~~~

Better README formatting (released to get better presentation on PyPi)

0.7.2
~~~~~~~~~~~~~~~~~~~~~

Added C++ language support (const string VERSION, const char* VERSION 
and some similar, in files named version.hpp|hxx|cpp|cxx).

0.7.1
~~~~~~~~~~~~~~~~~~~~~

CVS keyword expansion was triggered always instead only when
appropriate (bug in 0.7.0). Also, some testfixes related to this
functionality.

0.7.0
~~~~~~~~~~~~~~~~~~~~~

Module can be used to emulate CVS keywords handling. Just set
expand_keywords=1 for directory (or directories set) and just before
tagging various $Keywords$ will be replaced (and commited).

0.6.2
~~~~~~~~~~~~~~~~~~~~~

Mercurial 4.0 compatibility (just testfixes)

0.6.1
~~~~~~~~~~~~~~~~~~~~~

Slightly liberated parsing in pfx-dashed mode, for example
blah20_1-17-3 (which previously was ignored as tag of non-matching
format) now is considered to mean version 1.17.3

0.6.0
~~~~~~~~~~~~~~~~~~~~~

#1 Hook can be enabled statically, so it really works under TortoiseHg
(I failed to find any way to dynamically enable hook under Tortoise).

0.5.4
~~~~~~~~~~~~~~~~~~~~~~

#2 Added support for javascript language (package.json and VERSION
   lines in *version.jsx?)

Fixed bug due to which extra newline was added after version number
in some cases.

0.5.3
~~~~~~~~~~~~~~~~~~~~~~

Forward compatibility to incoming Mercurial 3.8 (moved to current
cmdtable API).

Some test tweaks.

0.5.2
~~~~~~~~~~~~~~~~~~~~~~

ToX tests run for various mercurial versions (2.7 to 3.6).

Dropped update_version.py legacy module.

0.5.1
~~~~~~~~~~~~~~~~~~~~~~

Test requirements, drone.io badge, slight metadata fixes.

0.5.0
~~~~~~~~~~~~~~~~~~~~~~

Hook works for some hg tag -r REV cases: namely when the revision in
charge is equivalent to current repo revision.

Some tests written.

0.4.1
~~~~~~~~~~~~~~~~~~~~~~

Fixed setup bugs which could cause install problems (bad module name).

0.4.0
~~~~~~~~~~~~~~~~~~~~~~

Module renamed to mercurial_update_version to avoid name clashes.
Documentation updates.

0.3.3
~~~~~~~~~~~~~~~~~~~~~~~

Minimal Windows support (workaround for meu import, using windows-compatible
extension_utils).

0.3.2
~~~~~~~~~~~~~~~~~~~~~~~

Bugfix: With update_version active, hg tag failed when executed not in
repo root.

Bugfix: Calling hg tag with bad params (I tried hg tag -d 1.2.3) resulted in
update_version failure („unexpected arguments, pats=[]). Now it
ignores such cases.

Bugfix: Fixed invalid error messages shown on bad value of .tagfmt or
.language („Unknown tagfmt None” → „Unknown tagfmt blah”)

Bugfix: Various warnings, notes and debug messages lacked final
newline.

All messages issued by extension are now prefixed with
"update_version: ".

Message shown on bad tag format makes it clear that tag
was allowed.

0.3.1
~~~~~~~~~~~~~~~~~~~~~~~

Initial public release. Support for python and perl language
conventions, enabling per-repo or globally active_on.


