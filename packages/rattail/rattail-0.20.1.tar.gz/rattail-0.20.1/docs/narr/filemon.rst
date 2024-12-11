.. -*- coding: utf-8 -*-

File Monitor
============

The Rattail File Monitor provides a generic way to watch one or more specific
folders on a file system for incoming files, and perform one or more actions on
new files as they appear within the watched folder(s).  It is implemented as a
`daemon`_ on Linux and a `service`_ on Windows.

.. _`daemon`: http://en.wikipedia.org/wiki/Daemon_%28computing%29
.. _`service`: http://en.wikipedia.org/wiki/Windows_service


Why?
----

While there are probably many similar applications and libraries in existence
within the Python ecosystem (not to mention the computing world at large), the
main features which presumably distinguish the Rattail File Monitor are:

* It is more of an application than a library, but blurs this line slightly.

* It is written in Python, and (typically) expects your code to be also.

* It can be configured to watch for *disappearance* of "lock" files as opposed
  to *appearance* of files in general.

* It contains a configurable retry mechanism for file actions which do not at
  first succeed.

* It can be configured to stop processing all new files if a single file action
  fails.

Most generic file-watching *applications* may be declaratively told which
folder(s) to watch, and which action(s) to take when new files arrive.  Rattail
is not fundamentally different in this respect.  However most applications
require you to define the action(s) in terms of shell executables, with
optional command line parameters etc.

Most generic file-watching *libraries* require the developer to imperatively
define which folders to watch, and the library in turn will inform the
developer's code (via some sort of "event") when new files appear; the
developer's code must then respond to the event by invoking some explicit
action(s) on the new file.

The Rattail File Monitor blends these two approaches somewhat by allowing
declarative definition of both the watch and action aspects, but allowing
(currently, requiring) the action(s) to be defined in terms of Python
callables.  In spirit it is more of an application than a library, although of
course there is nothing preventing a developer from consuming its logic as a
library.  The goal, however, is to provide an *application* which frees the
developer from needing to write any watch/action "glue" code and yet allows him
to write simple Python code for any custom action(s) needed.

This goal in particular, as well as others listed above, are achieved by way of
a flexible configuration syntax.

.. note::
   The *ultimate* goal is to alleviate the need for a developer to write custom
   action logic at all (i.e. configuring the File Monitor to invoke
   pre-existing action logic instead), but that problem will likely never be
   truly solved, given the diversity of needs encountered in the retail world.
   However, "common" action logic is provided wherever possible.


Configuration
-------------

Configuration of the File Monitor must be defined within one or more INI-style
configuration files.  There are certain tricks which may be employed in order
to leverage multiple config files (namely config file `inheritance`_); however
in almost all cases the configuration specific to the File Monitor itself is
contained within a single file, since the File Monitor generally runs in the
context of a single application.  The remainder of this document will "ignore"
the config file inheritance idea and assume a single config file.

.. _`inheritance`: https://rattailproject.org/moin/Configuration#Inheritance_.2F_.22Chaining.22

There are essentially two levels to the File Monitor configuration syntax.  The
first level requires a simple list of "profile" names.  The second level
consists of the profile definitions.  The term "profile" here refers to a
conceptual pairing of which folder(s) to watch, and which action(s) to take
when new files appear within the folder(s), as well as semantics defining how
the watch/action logic should behave in general.  This will all be explained
along the way as we explore the syntax.

**Configuration Options Quick Links**

* :ref:`filemon-monitor`
* :ref:`filemon-profile-dirs`
* :ref:`filemon-profile-watchlocks`
* :ref:`filemon-profile-processexisting`
* :ref:`filemon-profile-stoperror`
* :ref:`filemon-profile-actions`
* :ref:`filemon-profile-action-func`
* :ref:`filemon-profile-action-class`
* :ref:`filemon-profile-action-args`
* :ref:`filemon-profile-action-kwargs`
* :ref:`filemon-profile-action-retry`


The "rattail.filemon" Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First of all, and just to clarify in case it isn't obvious, all configuration
options must be defined within the ``[rattail.filemon]`` section of the config
file, i.e.:

.. code-block:: ini

   [rattail.filemon]
   # options go here


.. _filemon-monitor:

The "monitor" Option
^^^^^^^^^^^^^^^^^^^^

The only option which is *always* required is the ``monitor`` option; however
other options will "become" required based on its value.  This option defines
which profiles are actually in effect.  The basic idea is similar to how the
``keys`` option of the ``[loggers]`` section works within the standard library
:mod:`python:logging` module's :ref:`python:logging-config-fileformat`.  (This
is mentioned for the benefit of those who are familiar, but knowledge of the
logging config syntax is not necessary here.)

So, an example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo, bar

   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mypackage.mymodule:myprocessingfunc

   bar.dirs = /another/path
   bar.actions = special
   bar.action.special.func = myothermodule:myspecialfunc

   baz.dirs = /some/other/path
   baz.actions = wtf
   baz.action.wtf.func = os:remove

Here we have two profile names listed in the ``monitor`` option: "foo" and
"bar".  However we actually have *three* profiles defined: "foo", "bar" and
"baz".  What this means is that when the File Monitor initializes, it will only
look for (and indeed, require) profile definitions for "foo" and "bar" but will
not even look at the "baz" profile.

Implied also is that all options which define the "foo" profile *must* be named
with a ``foo.`` prefix (and the "bar" profile options must be named with a
``bar.`` prefix).  Any other options present which are not prefixed with the
name of a profile given in the ``monitor`` option will be ignored (as is the
case with the ``baz.*`` options above).

One final point on the syntax of the ``monitor`` option: The value must be one
or more profile "names" (or "keys" or "prefixes" or however you like to think
of them), but in the case of multiple names, arbitrary whitespace and/or commas
are both valid separators.  In other words each of the following examples are
valid, and would yield the same result:

.. code-block:: ini

   monitor = foo, bar, baz

   monitor = foo,bar,baz

   monitor = foo bar baz

   monitor =
        foo
        bar
        baz

   monitor =
        foo,
        bar baz

Note in particular the last example, which uses a comma between the first two
options but not the last two.


.. _filemon-profile-dirs:

The Profile "dirs" Option
^^^^^^^^^^^^^^^^^^^^^^^^^

This option defines which folder(s) will be watched for new files, for a given
profile.  Its value must be one or more directory paths.  As with the "monitor"
option, if multiple paths are needed then they may be separated with arbitrary
whitespace and/or commas.  However any path which contains spaces must be
quoted.  So, some examples:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo

   # linux
   foo.dirs = /some/path/to/watch

   # linux, path with spaces
   foo.dirs = "/some/path with spaces/to watch"

   # linux, multiple paths
   foo.dirs = /some/path/to/watch, "/another/path with spaces"

   # linux, multiple paths
   foo.dirs =
        /some/path/to/watch
        "/another/path with spaces"

   # win32
   foo.dirs = C:\some\path\to\watch

   # win32, path with spaces
   foo.dirs = "C:\some\path with spaces\to watch"

   # win32, multiple paths
   foo.dirs = C:\some\path\to\watch, "C:\another\path with spaces"
   
   # win32, multiple paths
   foo.dirs =
        C:\some\path\to\watch
        "C:\another\path with spaces"

For a given profile, it is typical for there to be only one path defined in the
"dirs" option.  If multiple paths are defined, then of course each folder will
be watched, and when a new file appears in *any* of the watched folders then
the profile's configured action(s) will be invoked on the file.  I.e. there
will be no difference in behavior when files appear in one of the folders
versus another.  If you need different behaviors for different folders than
that is a clear sign that you need to define multiple *profiles*.


.. _filemon-profile-watchlocks:

The Profile "watch_locks" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Probably in most cases, the event which should trigger action(s) to be taken on
a file is the initial appearance of the file.  However there is another
possibility, which is to wait instead for the *disappearance* of a "lock" file
which is *associated* with the "real" file.  This deserves some explanation.

First of all it is important to understand that if the process(es) which is
causing the files to appear in the first place is external to your application
(i.e. the files are created by another application, outside of your control),
then there almost certainly will never *be* any "lock" files involved and so
you of course cannot watch for their disappearance.  If this is your situation
then the "watch_locks" option is not for you and you can safely skip this
section, since the default is *not* to watch for lock files.

The only situation in which lock files are known to be involved is one where
some Rattail-based application is intentionally using them to provide atomicity
when moving files from one location to another, etc.  Therefore in almost all
cases, if you need to watch for lock files it will be because *you* are
creating them in the first place, via :func:`rattail.files.locking_copy()` or
some similar mechanism.

If you *do* need to watch for the disappearance of lock files instead of the
appearance of files in general, then here is how you would configure it:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path, /another/path
   foo.watch_locks = true

Note that the behavior of watching for lock files will apply to all watched
folders within the profile definition.  Once again, if you need to watch for
lock files in one folder but not another, that means you need to define
multiple profiles.

The semantics of watching for new files, with and without the lock behavior, is
as follows:

If not watching for locks (the default), then as soon as a file first appears,
it will be added to the action queue for processing.

If watching for locks, then any new files which appear are ignored, and instead
whenever a file deletion occurs, *and* if the deleted file's path ends in
``.lock``, then that suffix is stripped and the resulting file path is added to
the action queue.


.. _filemon-profile-processexisting:

The Profile "process_existing" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, whenever the File Monitor is first started, any files which happen
to exist in the watched folder(s) will be immediately added to the processing
queue.  However in some cases this is *not* desirable.  For example if the
defined action(s) to not actually move the file out of the folder, then all
files will be *re-processed* whenever a restart occurs.

It is for this type of situation that the "process_existing" option exists:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.process_existing = false

Technically the value of this option could be anything supported by the
:meth:`rattail.config.RattailConfig.getbool()` method, but in practice it is
conventionally set to "false" or else omitted entirely (as it is enabled by
default).

Note also that this option applies at the *profile* level, and is not specific
to any particular watched folder.  If you need different behavior for different
folders, you must define additional profiles for each.

Finally, it may (or may not, depending on your situation) be important to
understand that if this option is enabled, then whenever the File Monitor
restarts it will add all existing files to the processing queue *in order of
their last modification time*.  The idea here is to (at least attempt) to
maintain the original sequence in which files arrived in the folder.  See also
:ref:`filemon-profile-stoperror` for a related option.


.. _filemon-profile-stoperror:

The Profile "stop_on_error" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, correct processing of files requires that they be processed in
the precise order of arrival.  Most often this is *not* a requirement, but if
it is for you, then you must consider what might happen if one file fails to
process.  This situation is the reason for the "stop_on_error" option.

The idea here is that if a single file fails, then all processing should stop
for the entire monitor profile to which the action belonged.  I.e., any new
files which appear from that moment on will *not* have any actions invoked on
them.  This means that whatever caused the original failure must be addressed
by *you* and then you must restart the File Monitor.  See also the related
:ref:`filemon-profile-processexisting` option.

There are probably more caveats to mention, e.g. it also is assumed that you
have a way to be notified when a failure occurs.  Again, this is not a common
need so it is assumed that those who do need it understand the implications.

An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mymodule:my_processor_function
   foo.stop_on_error = true

You'll notice that this is option applies at the *profile* level and not at the
action level.  As of this writing, the action-level granularity has not been
needed, although it may be added in the future.

Technically the value of this option could be anything supported by the
:meth:`rattail.config.RattailConfig.getbool()` method, but in practice it is
conventionally set to "true" or else omitted entirely (as it is disabled by
default).


.. _filemon-profile-actions:

The Profile "actions" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This option is somewhat like the main "monitor" option, in that it defines one
or more action "names" (or "keys" or "prefixes"), each of which represents a
particular action to invoke on new files (and the details of which will require
further definition, to be provided by additional options).  The sequence of
these names matters (assuming there is more than one), because it will
determine the order in which the actions should be invoked.  The action name(s)
need not bear any resemblance to the name of the actual function (etc.) which
is to be invoked.  Some examples:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path

   foo.actions = process

   foo.actions = copy, delete

   foo.actions =
        copy_to_server_A
        copy_to_server_B
        process_locally
        backup

Again, and despite the above examples which are not complete, specifying an
action name within a profile's "actions" option means you must then define the
action further.  The remainder of this document explains how.


.. _filemon-profile-action-func:

The Profile Action "func" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In almost all cases, an action which is to be invoked on new files will be a
Python *function*.

.. note::
   As of this writing, there is only one other possibility, which is for the
   action to be a Python callable *class*.  See
   :ref:`filemon-profile-action-class` for more information.

For each action named in :ref:`filemon-profile-actions`, the invocation of
which will be to call a Python *function*, a "func" option must be defined.
The value of this option must be a "spec" which indicates the function name and
the Python module in which it is contained.  An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mypackage.mymodule:my_processor_function

.. note::
   While the "actions" option defines one or more action names, each named
   action is further defined with options which contain an "action" (no "s")
   prefix.

.. note::
   There must be a colon (":") separating the module path from the function
   name.

In this example we have defined an action named "process" and defined a
function for the action, which is the ``my_processor_function`` function from
the ``mypackage.mymodule`` module.  At runtime, invocation will be equivalent
to the following Python code (where ``file_path`` is the absolute path of the
new file discovered by the monitor):

.. code-block:: python

   from mypackage.mymodule import my_processor_function
   my_processor_function(file_path)

It is possible to specify additional positional and keyword arguments to the
function when calling it; see :ref:`filemon-profile-action-args` and
:ref:`filemon-profile-action-kwargs` for more information.


.. _filemon-profile-action-class:

The Profile Action "class" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, an action which is to be invoked on new files will be a Python
*class*.  More precisely, the class will be instantiated, and the instance will
be called at invocation time.

.. note::
   As of this writing, there is only one other possibility, which is for the
   action to be a Python callable *function*.  See
   :ref:`filemon-profile-action-func` for more information.

For each action named in :ref:`filemon-profile-actions`, the invocation of
which will be to call a Python *class*, a "class" option must be defined.  The
value of this option must be a "spec" which indicates the class name and the
Python module in which it is contained.  An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.class = mypackage.mymodule:MyProcessorClass

.. note::
   While the "actions" option defines one or more action names, each named
   action is further defined with options which contain an "action" (no "s")
   prefix.

.. note::
   There must be a colon (":") separating the module path from the class name.

In this example we have defined an action named "process" and defined a class
for the action, which is the ``MyProcessorClass`` function from the
``mypackage.mymodule`` module.  At runtime, invocation will be (sort of)
equivalent to the following Python code (where ``file_path`` is the absolute
path of the new file discovered by the monitor):

.. code-block:: python

   from mypackage.mymodule import MyProcessorClass
   instance = MyProcessorClass()
   instance(file_path)

It is possible to specify additional positional and keyword arguments to the
class instance when calling it; see :ref:`filemon-profile-action-args` and
:ref:`filemon-profile-action-kwargs` for more information.


.. _filemon-profile-action-args:

The Profile Action "args" Option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regardless of whether you have defined the action callable as a function or a
class, you may specify extra positional arguments to be passed to the
callable.  This is accomplished by an "args" option which is prefixed by the
action name.

Its value is interpreted as a "list" of one or more values, each separated by
whitespace and/or comma.  See :ref:`filemon-profile-dirs` for some more
examples of how the parsing of this works; the main point is that if you need
to specify a "single" value which contains spaces, it must be quoted.

An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mymodule:my_processor_function
   foo.action.process.args = /some/other/path, 42, True

   # or, using another syntax:
   foo.action.process.args =
        /some/other/path
        42
        True

The above will result in the following logic at runtime:

.. code-block:: python

   from mymodule import my_processor_function
   my_processor_function(file_path, u'/some/other/path', u'42', u'True')

.. note::
   In all cases these extra arguments will be passed to the callable as unicode
   strings.  The File Monitor will make no effort to coerce them to any other
   type; this burden rests on the callable if it is needed.


.. _filemon-profile-action-kwargs:

The Profile Action "kwarg" Option(s)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regardless of whether you have defined the action callable as a function or a
class, you may specify extra keyword arguments to be passed to the callable.
This is accomplished by one or more "kwarg" options, each of which is prefixed
by the action name, and the word "kwarg", and ending in the keyword itself.

Its value is read as a single unicode string with no interpretation, unlike the
"args" option described above.

An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mymodule:my_processor_function
   foo.action.process.kwarg.something = /some/other/path
   foo.action.process.kwarg.another = 42

The above will result in the following logic at runtime:

.. code-block:: python

   from mymodule import my_processor_function
   my_processor_function(file_path, something=u'/some/other/path', another=u'42')

.. note::
   As with the "args" option above, no type coercion will be done on keyword
   argument values.

Finally, note that the "args" and "kwarg" option(s) may be mixed:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mymodule:my_processor_function
   foo.action.process.args = /some/other/path
   foo.action.process.kwarg.something = 42

The above will result in this logic:

.. code-block:: python

   from mymodule import my_processor_function
   my_processor_function(file_path, u'/some/other/path', something=u'42')


.. _filemon-profile-action-retry:

The Profile Action "retry" Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, all actions are attempted only once.  Should the action fail, any
*subsequent* actions (if there would be any) for *that particular file* will be
skipped.

.. note::
   It is possible to forego all processing for any *other* files as well, if
   this is desired; see :ref:`filemon-profile-stoperror` for more information.

If any particular action should be considered "retryable" then this may be
declared via the "retry_attempts" and "retry_delay" options.  These should be
self-explanatory; the "retry_attempts" defines how many attempts are allowed
for a given action for a given file, and "retry_delay" defines how long to wait
(in seconds) between the attempts.

An example:

.. code-block:: ini

   [rattail.filemon]
   monitor = foo
   foo.dirs = /some/path
   foo.actions = process
   foo.action.process.func = mymodule:my_processor_function
   foo.action.retry_attempts = 3
   foo.action.retry_delay = 5

In the above example, ``my_processor_function()`` will be called once in all
cases; if the first call fails, then the File Monitor will wait 5 seconds and
then call it again.  If the second call fails, another pause of 5 seconds will
happen before calling the third time.  If the call fails *again* (i.e. for the
third time) then the File Monitor will give up on the file.  At this point the
logic is no different than if a non-retryable action had failed the first time;
i.e. any subsequent actions will be skipped for the file, etc.

The determination of whether an action "fails" is simply based on the
occurrence of an unhandled exception.  Since there are different types of
exceptions, the retry logic tries to play it "safe" and assume that all
"retryable" failures should correspond to the same exception type.  I.e. if the
first call fails with an exception of one type, then while attempting the
second call, a *different* exception type is raised, the File Monitor will
consider it an utter failure and *not* retry again.

.. note::
   The default "retry_attempts" value for all actions is one (1).  The default
   "retry_delay" value for all actions is zero (0).
