.. -*- mode: rst; compile-command: "rst2html README.rst README.html" -*-

=========================
Mercurial Update Version
=========================

No more manual version number editing.

Whenever you issue ``hg tag``, this extension scans your repository
for files containing various kinds of ``VERSION =`` lines, updates
those constants appropriately, commits the change, and only then tags
the release.

Functionality can be enabled per-repository or (via ``~/.hgrc``) for
many repositories at once (so you don't need to remember about
activating it on every created, or cloned repository).

.. contents::
   :local:
   :depth: 2

.. sectnum::

Enabling the extension
==========================

Install the extension as described below. Then either enable it
per-repository, or enable for many repositories at once.

Enabling per-repository
---------------------------

In repository ``.hg/hgrc`` write::

    [update_version]
    active = true
    language = python
    tagfmt = dotted

(of course using appropriate settings). Here:

- ``language`` implies version constants syntax, and sometimes
  restricts list of files scanned,

- ``tagfmt`` describes expected tag syntax (and how to extract
  actual version number from the tag).

For example, ``language = python`` means looking for ``setup.py``,
``__init__.py`` and ``version.py`` files anywhere inside the
repository, and updating lines looking like ``VERSION = "1.2.3"``,
while ``tagfmt = dotted`` means simple dotted numbers are used as
tags (``hg tag 1.0.9``).

Both languages and tag formats are configurable, extension brings
some sane defaults but they can be overridden, and new styles
can be defined. See below.

It is also possible to enable more than one language. For example,
to update numbers in both python, and javascript files, 
one can write in ``.hg/hgrc``::

    [update_version]
    py.active = true
    py.language = python
    py.tagfmt = dotted
    js.active = true
    js.language = javascript
    js.tagfmt = dotted

Name prefixes (``py`` and ``js`` in the sample above) are used only
to group the settings and are not important (use any name you like).
The ``tagfmt`` setting should usually be the same in all entries.


Enabling for many repositories at once
------------------------------------------------------

In ``~/.hgrc`` write something like::

    [update_version]
    pydev.active_on = ~/sources/pymodules, ~/work/python 
    pydev.language = python
    pydev.tagfmt = dotted
    myperl.active_on = ~/scripts, ~/work/scripts 
    myperl.language = perl
    myperl.tagfmt = dashed
    excvs.active_on = ~/legacy
    excvs.expand_keywords = 1

Name prefixes (``pydev`` and ``myperl``) are used only to group
three settings together (use any names you like).

In both cases:

- ``.active_on`` lists directory trees to which given rule can be applied
  (absolute paths, ``~`` and ``~user`` are allowed), 

- ``.language`` and ``.tagfmt`` define which language settings and which tag
  format to use for those directories.

- ``.expand_keywords`` enables CVS keyword expansion (replacement of ``$Name$`` and similar constructs). Note that it works differently than keyword extension, replacements are commited (so will always be present in the checked out code).

In case multiple directives match the same repo, all are processed, for example with::

    [update_version]
    pydev.active_on = ~/sources
    pydev.language = python
    pydev.tagfmt = dotted
    jsdev.active_on = ~/sources
    jsdev.language = javascript
    jsdev.tagfmt = dotted

in repo ``~/sources/myweb`` both python, and javascript files, will be processed.

Enabling for use in TortoiseHg
----------------------------------------------------

The setup above is not sufficient for tags created from TortoiseHg GUI
(via ``thg tag`` or tagging dialog of main TortoiseHg window). To get
those working, you must manually enable the update version hook. Add
to your ``~/.hgrc``::

   [hooks]
   pre-tag.update_version = python:mercurial_update_version.pre_tag_hook
  
Please, use exactly that name and value (it will be used by extension
to detect that you enabled the hook, so it need not be enabled again
under bare Mercurial).

The rest of the configuration remains the same.

.. note::

   Technical details: ``mercurial_update_version`` usually enables
   that hook by itself. Unfortunately under TortoiseHg dynamic hook
   activation does not work (THG has it's own command processing chain
   different from Mercurial core, and hook list is effectively frozen
   before extensions are able to impact it).


Using
============================================

After enabling the extension:

- ensure your code have some initial version variables
  (put sth. like ``VERSION = "0.0.0"`` in appropriate place(s))

- simply ``hg tag «appropriate-tag»``.

and your version constants will be updated, the change commited, and
only the resulting changeset tagged.

Version numbers are not updated when tag is placed by revision (``hg
tag -r «version-no» «tag»``), unless specified revision matches
currently checked out revision.

Tags not matching the expected pattern are ignored, just like local
tags (rarely used Mercurial feature).

The extension notifies you whether and what it does, for example::

  $ hg tag 2.0
  update_version: Version number in src/version.py set to 2.0. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.0"

or::

  $ hg tag -r 2 0.5.0
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)

Predefined languages
=============================================

The ``language`` setting defines:

- which files to check and patch (by filename patterns)

- what is the appropriate constant format and name

The following languages are currently supported:

Python (``language=python``)
----------------------------

Look for files named ``setup.py``, ``__init__.py`` or
``version.py`` (anywhere inside repository). In those files,
update lines looking like::

    VERSION = '1.2.3'

(at least one dot - but can be more, both single and double-quotes
are supported, just like various spacing and indentation).

Inserted version number is formatted in the same way (as
dot-separated list of numbers).  Tag being placed should contain
at least two-part version number to be used.

Perl (``language=perl``)
-------------------------

Look for files named ``*.pl``, ``*.pm`` and ``*.pod`` around
repository. If found, look for lines like::

    our $VERSION = '1.00';
    my $VERSION = '11.72';
    use constant VERSION => '21.3374';

(exactly one dot expected, various spacing and indentation
allowed, double quotes allowed) and also::

    Version 1.23

(usually met in POD sections).

Also, look for ``dist.ini`` and if found, fix lines like::

    version = 0.02

Two kinds of tags numbers are supported. If tag contains two-item
version, it is left as is (tag ``1.0`` results in version ``1.0``,
dashed tag ``1-03`` brings ``1.03``). If tag has three parts,
first is left before the dot while second and third each get two
digits after the dot (tag ``1.7.2`` is translated into version
``1.0702``, tag ``17-0-9`` into ``17.0009``). Other tags are
invalid.

JavaScript (``language=javascript``)
-------------------------------------

Look for files named ``version.js``, ``version.jsx``, ``*_version.js``
and ``*_version.jsx``. In any of those, look for lines like::

     var VERSION = "1.2.3";
     const VERSION = "1.2.3";
     let VERSION = "1.2.3";

(final semicolons being optional).

Also look for ``package.json`` file(s) and if found, update line like::

    "version": "1.0.0",

(with or without semicolon, and with or without indentation). Note: this
is currently expected to be the sole item on the line, without other
keys.

JSON (``language=json``)
-------------------------------------

Check files named ``*.json`` for lines like::

    "version": "1.0.0",

(with or without semicolon, with or without indentation, with single or double quotes,
without other keys on the same line).

Contrary to most other languages, there are additional restrictions:

- checking is limited to first 30 lines of the file,

- only one (first) line of such form is modified.


YAML (``language=yaml``)
-------------------------------------

Check files named ``*.yaml`` or ``*.yml`` for lines like::

    version: "1.0.0"
    package_version: "1.0.0"
    module_version: "1.0.0"

(with or without quotes, with or without indentation).

Contrary to most other languages, there are additional restrictions:

- checking is limited to first 20 lines of the file,

- only one (first) matching line is modified.


Logstash (``language=logstash``)
---------------------------------------

Check files named ``*version*.conf`` (``conf`` extension and word
``version`` anywhere inside basename) for lines like::

    add_field => { "[version]" => "1.0.2" }

or mayhaps::

    add_field => { "[some][prefix][version]" => "1.0.2" }

(last - or only - part of the key must be ``[version]``, whitespace can be flexible
but whole line as such must be constructed as above).

I recommend using file like ``01-version.conf`` (named so it is
processed early), with content like::

    filter {
        mutate {
            add_field => { "[@metadata][myapp][version]" => "1.0.2" }
        }
    }

and then referring to this field (copying it, using inside formatted
strings) wherever needed in filters and outputs.


C++ (``language=c++``)
--------------------------

Look for files named ``version.hxx``, ``version.cxx``,
``version.hpp``, ``version.cpp``. Look for and update lines like::

      const string VERSION = "1.2.3";
      const char* VERSION = "1.2.3";
      const char VERSION[] = "1.2.3";
      string VERSION = "1.2.3";

*Support for further languages is planned, feel free to suggest them.*

Predefined tag formats
=============================

The following tag formats are supported.

Dot-separated numbers (``tagfmt=dotted``)
-----------------------------------------------

Tags like ``1.0``, ``1.0.3``, ``11.17.34``.

Dash-separated numbers (``tagfmt=dashed``)
-----------------------------------------------

Tags like ``1-0``, ``1-0-3``, ``11-17-34``.

Dotted with text prefix (``tagfmt=pfx-dotted``)
-------------------------------------------------

Tags like ``mylib-1.0`` or ``sth_11.3.17``:
alphanumeric string, dash or underscore,
then actual version as in ``dotted``.

Dashed with text prefix (``tagfmt=pfx-dashed``)
-------------------------------------------------

Tags like ``mylib-1-0`` or ``sth_11-3-17``:
alphanumeric string, dash or underscore,
then actual version as in ``dashed``. leading
part must not end with digit.

Keyword expansion
=======================

Setting ``expand_keywords=1`` enables CVS keyword expansion.  Source
will be scanned for CVS keywords like ``$Name$`` (or ``$Name: mytag_0.7.0 $``), ``$Revision$``, etc, and those will be appropriately updated. This change will be commited, making those changes permanent
(until they are replaced by newer tag). 

This is an alternative to standard keyword extension, which updates
those keywords on update (and causes various problems with merges,
edits, extension configuration, etc). With ``update_version``
approach, proper keyword values will be simply commited just before
tagging, so they will always be present in the checkout.

Note that the replacement is somewhat simplistic: the main purpose is
to get proper ``$Name$``, everything else (``$Revision$``, ``$Header$``
etc) gets populated with the data of last pre-tag changeset (calculating
true date or revision of last change per each file is possible, but would
be fairly costly).

Example configuration (``~/.hgrc``)::

   [update_version]
   cvsconverts.active_on = ~/devel/legacy ~/devel/libs
   cvsconverts.expand_keywords = 1

Custom languages
=============================

Not yet supported, but planned (defining new language by configuration
settings, or overriding some default language characteristics). The
general idea is to have some reasonable defaults built-in, but allow
reconfiguration.


Custom tag formats
=============================

Not yet supported, but planned (defining new tag format by
configuration settings).


Commands
=====================

``hg tag``
-----------

Extension mainly work by augmenting ``hg tag``, as described
above.


``hg tag_version_test``
------------------------

This is *dry run* check. The command::

    hg tag_version_test 1.0

lists which files would be checked, whether version lines were found
in them, and how would they be changed, but does not change anything.


Installation
==================

Linux/Unix (from PyPI)
---------------------------------------------

If you have working ``pip`` or ``easy_install``::

    pip install --user mercurial_update_version

or maybe::

    sudo pip install mercurial_update_version

(or use ``easy_install`` instead of ``pip``). Then activate by::

    [extensions]
    mercurial_update_version =

To upgrade, repeat the same command with ``--upgrade`` option, for
example::

    pip install --user --upgrade mercurial_update_version

Linux/Unix (from source)
---------------------------------------------

If you don't have ``pip``, or wish to follow development more closely:

- clone both this repository and `mercurial_extension_utils`_ and put
  them in the same directory, for example::

    cd ~/sources
    hg clone https://foss.heptapod.net/mercurial/mercurial-extension_utils/
    hg clone https://foss.heptapod.net/mercurial/mercurial-update_version/

- update to newest tags,

- activate by::

    [extensions]
    mercurial_update_version = ~/sources/mercurial-update_version/mercurial_update_version.py

To upgrade, pull and update.

See `mercurial_extension_utils`_ for longer description of this kind
of installation.

Windows
---------------------------------------------

If you have any Python installed, you may install with ``pip``::

    pip install mercurial_update_version

Still, as Mercurial (whether taken from TortoiseHg_, or own package)
uses it's own bundled Python, you must activate by specifying the path::

    [extensions]
    mercurial_update_version = C:/Python27/Lib/site-packages/mercurial_update_version.py
    ;; Or wherever pip installed it, depending on the version it can also be
    ;; sth like (replace john with proper username and 37 with proper version)
    ;; mercurial_update_version =  C:\Users\john\AppData\Local\Programs\Python\Python37\Lib\site-packages\mercurial_update_version.py

To upgrade to new version::

    pip install --upgrade mercurial_update_version

If you don't have any Python, clone repositories::

    cd c:\hgplugins
    hg clone https://foss.heptapod.net/mercurial/mercurial-extension_utils/
    hg clone https://foss.heptapod.net/mercurial/mercurial-update_version/

update to tagged versions and activate by path::

    [extensions]
    mercurial_update_version = C:/hgplugins/mercurial-update_version/mercurial_update_version.py
    ;; Or wherever you cloned

See `mercurial_extension_utils`_ documentation for more details on
Windows installation. 


History
==================================================

See `HISTORY.rst`_


Repository, bug reports, enhancement suggestions
===================================================

Development is tracked on HeptaPod, see 
https://foss.heptapod.net/mercurial/mercurial-update_version/

Use issue tracker there for bug reports and enhancement
suggestions.

Thanks to Octobus_ and `Clever Cloud`_ for hosting this service.

Additional notes
================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/UpdateVersionExtension

Check also `other Mercurial extensions I wrote`_.

.. _Octobus: https://octobus.net/
.. _Clever Cloud: https://www.clever-cloud.com/

.. _other Mercurial extensions I wrote: http://code.mekk.waw.pl/mercurial.html

.. _Mercurial: http://mercurial.selenic.com
.. _HISTORY.rst: https://foss.heptapod.net/mercurial/mercurial-update_version/src/tip/HISTORY.rst
.. _mercurial_extension_utils: https://foss.heptapod.net/mercurial/mercurial-extension_utils/
.. _TortoiseHg: http://tortoisehg.bitbucket.io/

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mercurial-update_version/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mercurial-update_version/latest
     :align: middle
