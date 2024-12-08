Dynamic message prefixes providing execution context.

*Latest release 20241208*:
Pfx.prefixify_exception: record the original message as {attr}_without_prefix, useful in warnings which themselves recite the prefix.

The primary facility here is `Pfx`,
a context manager which maintains a per thread stack of context prefixes.
There are also decorators for functions.
This stack is used to prefix logging messages and exception text with context.

Usage is like this:

    from cs.pfx import Pfx
    ...
    def parser(filename):
      with Pfx(filename):
        with open(filename) as f:
          for lineno, line in enumerate(f, 1):
            with Pfx(lineno):
              if line_is_invalid(line):
                raise ValueError("problem!")
              info("line = %r", line)

This produces log messages like:

    datafile: 1: line = 'foo\n'

and exception messages like:

    datafile: 17: problem!

which lets one put just the relevant complaint in exception and log
messages and get useful calling context on the output.
This does make for wordier logs and exceptions
but used with a little discretion produces far more debuggable results.

## <a name="Pfx"></a>Class `Pfx`

A context manager to maintain a per-thread stack of message prefixes.

*`Pfx.__init__(self, mark, *args, **kwargs)`*:
Initialise a new Pfx instance.

Parameters:
* `mark`: message prefix string
* `args`: if not empty, apply to the prefix string with `%`
* `absolute`: optional keyword argument, default `False`. If
  true, this message forms the base of the message prefixes;
  earlier prefixes will be suppressed.
* `loggers`: which loggers should receive log messages.
* `print`: if true, print the `mark` on entry to the `with` suite.
  This may be a `bool`, implying `print()` if `True`,
  a callable which works like `print()`,
  or a file-like object which implies using `print(...,file=print)`.

*Note*:
the `mark` and `args` are only combined if the `Pfx` instance gets used,
for example for logging or to annotate an exception.
Otherwise, they are not combined.
Therefore the values interpolated are as they are when the `Pfx` is used,
not necessarily as they were when the `Pfx` was created.
If the `args` are subject to change and you require the original values,
apply them to `mark` immediately, for example:

    with Pfx('message %s ...' % (arg1, arg2, ...)):

This is a bit more expensive as it incurs the formatting cost
whenever you enter the `with` clause.
The common usage is:

    with Pfx('message %s ...', arg1, arg2, ...):

*`Pfx.critical(self, msg, *args, **kwargs)`*:
Emit a critical log message.

*`Pfx.debug(self, msg, *args, **kwargs)`*:
Emit a debug log message.

*`Pfx.error(self, msg, *args, **kwargs)`*:
Emit an error log message.

*`Pfx.exception(self, msg, *args, **kwargs)`*:
Log an exception message to this Pfx's loggers.

*`Pfx.info(self, msg, *args, **kwargs)`*:
Emit an info log message.

*`Pfx.log(self, level, msg, *args, **kwargs)`*:
Log a message at an arbitrary log level to this Pfx's loggers.

*`Pfx.loggers`*:
Return the loggers to use for this Pfx instance.

*`Pfx.logto(self, new_loggers)`*:
Define the Loggers anew.

*`Pfx.partial(self, func, *a, **kw)`*:
Return a function that will run the supplied function `func`
within a surrounding `Pfx` context with the current mark string.

This is intended for deferred call facilities like
`Later` and `futures`.

*`Pfx.prefixify(text)`*:
Return `text` with the current prefix prepended.
Return `text` unchanged if it is not a string.

*`Pfx.prefixify_exception(e)`*:
Modify the supplied exception `e` with the current prefix.
Return `True` if modified, `False` if unable to modify.

*`Pfx.push(msg, *a)`*:
A new `Pfx(msg,*a)` onto the `Thread` stack.

*`Pfx.scope(msg=None, *a)`*:
Context manager to save the current `Thread`'s stack state
and to restore it on exit.

This is to aid long suites which progressively add `Pfx` context
as the suite progresses, example:

    for item in items:
        with Pfx.scope("item %s", item):
            db_row = db.get(item)
            Pfx.push("db_row = %r", db_row)
            matches = db.lookup(db_row.category)
            if not matches:
                continue
            Pfx.push("%d matches", len(matches):
            ... etc etc ...

*`Pfx.umark`*:
Return the unicode message mark for use with this Pfx.

This is used by Pfx._state.prefix to compute the full prefix.

*`Pfx.warning(self, msg, *args, **kwargs)`*:
Emit a warning log message.

## <a name="pfx"></a>`pfx(*da, **dkw)`

General purpose @pfx for generators, methods etc.

Parameters:
* `func`: the function or generator function to decorate
* `message`: optional prefix to use instead of the function name
* `message_args`: optional arguments to embed in the preifx using `%`

Example usage:

    @pfx
    def f(....):
        ....

## <a name="pfx_call"></a>`pfx_call(func, *a, **kw)`

Call `func(*a,**kw)` within an enclosing `Pfx` context manager
reciting the function name and arguments.

Example:

    >>> import os
    >>> pfx_call(os.rename, "oldname", "newname")

## <a name="pfx_iter"></a>`pfx_iter(tag, iterable)`

Wrapper for iterables to prefix exceptions with `tag`.

## <a name="pfx_method"></a>`pfx_method(*da, **dkw)`

Decorator to provide a `Pfx` context for an instance method prefixing
*classname.methodname*.

If `use_str` is true (default `False`)
use `str(self)` instead of `classname`.

If `with_args` is true (default `False`)
include the specified arguments in the `Pfx` context.
If `with_args` is `True`, this includes all the arguments.
Otherwise `with_args` should be a sequence of argument references:
an `int` specifies one of the positional arguments
and a string specifies one of the keyword arguments.

Examples:

    class O:
        # just use "O.foo"
        @pfx_method
        def foo(self, .....):
            ....
        # use the value of self instead of the class name
        @pfx_method(use_str=True)
        def foo2(self, .....):
            ....
        # include all the arguments
        @pfx_method(with_args=True)
        def foo3(self, a, b, c, *, x=1, y):
            ....
        # include the "b", "c" and "x" arguments
        @pfx_method(with_args=[1,2,'x'])
        def foo3(self, a, b, c, *, x=1, y):
            ....

## <a name="PfxCallInfo"></a>Class `PfxCallInfo(Pfx)`

Subclass of Pfx to insert current function and caller into messages.

## <a name="pfxprint"></a>`pfxprint(*a, print_func=None, **kw)`

Call `print()` with the current prefix.

The optional keyword parameter `print_func`
provides an alternative function to the builtin `print()`.

## <a name="PfxThread"></a>`PfxThread(target, **kw)`

Factory function returning a `Thread`
which presents the current prefix as context.

## <a name="prefix"></a>`prefix()`

Return the current Pfx prefix.

## <a name="PrePfx"></a>`PrePfx(tag, *args)`

Push a temporary value for Pfx._state._ur_prefix to enloundenify messages.

## <a name="unpfx"></a>`unpfx(s, sep=None)`

Strip the leading prefix from the string `s`
using the prefix delimiter `sep`
(default from `DEFAULT_SEPARATOR`: `': '`).

This is a simple hack to support reporting error messages
which have had a prefix applied,
and fails accordingly if the base message itself contains the separator.

## <a name="XP"></a>`XP(msg, *args, **kwargs)`

Variation on `cs.x.X`
which prefixes the message with the current Pfx prefix.

## <a name="XX"></a>`XX(prepfx, msg, *args, **kwargs)`

Trite wrapper for `XP()` to transiently insert a leading prefix string.

Example:

    XX("NOTE!", "some message")

# Release Log



*Release 20241208*:
Pfx.prefixify_exception: record the original message as {attr}_without_prefix, useful in warnings which themselves recite the prefix.

*Release 20240630*:
@pfx_method: fix access to class name when the target is a class.

*Release 20240412*:
Pfx.prefixify_exception: bugfix prefixification of sequences.

*Release 20240326*:
* Pfx.prefixify_exception: sanity check the types of the prefixed attributes, aids debugging.
* Pfx.prefixify_exception: do not modify .message if it is not a string.

*Release 20230604*:
@pfx_method: handle methods with no __name__ (generally a misuse of the decorator).

*Release 20230331*:
PfxThread: use HasThreadState.Thread, make target mandatory.

*Release 20221118*:
pkg_tags: cs.py.func: update PyPI release: set pypi.release='20221118' [IGNORE]

*Release 20220918*:
* Drop _PfxThreadState.raise_needs_prefix, supplant with more reliable special exception attribute.
* Pfx.__exit__: include more detail in (suppressed) "message not prefixed" message.
* Pfx.__exit__: more elaborate logic for exc_value.args.

*Release 20220523*:
Pfx.umask: promote self.mark directly to ustr.

*Release 20220429*:
* New Pfx.scope() context manager and Pfx.push(msg,*a) nonindenting Pfx push.
* pfxprint: new optional print_func keyword parameter.

*Release 20220227*:
* Pfx.prefixify: change OSError.args action: prefixify the first string.
* XP: use DEFAULT_SEPARATOR on both paths.

*Release 20211031*:
Pfx.prefixify_exception: skip attributes which are None.

*Release 20210913*:
Pfx: do not fiddle with LookupError.args[0], it is the key.

*Release 20210906*:
* New pfxprint which calls print() with the current prefix.
* Pfx.prefixify_exception: catch unexpected OSError.args value and report.
* @pfx: use pfx_call if there is no presupplied message argument.

*Release 20210801*:
Bugfix for @pfx.

*Release 20210731*:
* Pfx.__exit__: special handling for some exception types.
* New pfx_call(func,*a,**kw) function to concisely wrap single function calls.

*Release 20210717*:
@pfx_method: new optional decorator argument "with_args" to include some or all arguments in the Pfx context.

*Release 20201227*:
* Pfx: new print=False option to issue a print() or other call on entry to the with-suite eg with Pfx(....,print=verbose).
* Pfx: print= now also accepts a file-like object.

*Release 20201105*:
@pfx: bugfix for generator functions.

*Release 20201025*:
* Refactor @pfx using @cs.deco.contextdecorator.
* New unpfx() function, a crude hack to strip an applpied cs.pfx prefix from a string.
* XP: just shim cs.x.X as callers expect, toss dubious extra functionality.
* exception(): plumb keyword arguments.

*Release 20200517*:
* @pfx: handle normal functions and also generators, improve behaviour with the wrapped docstring.
* @pfx_method: @pfx for methods.
* @pfxtag obsoleted by new @pfx.

*Release 20191004*:
@pfx_method: new optional `use_str` parameter to use str(self) instead of type(self).__name__; now requires @cs.deco.decorator

*Release 20190905*:
* Pfx.__exit__: simplify prefixify_exc() logic, prefixify all suitable attributes.
* New @pfx_method decorator for instance methods.

*Release 20190607*:
Pfx.__exit__ improved exception attribute handling.

*Release 20190403*:
Debugging aid: Pfx.umark: emit stack traceback on format conversion error.

*Release 20190327*:
* @pfx: set __name__ on the wrapper function.
* Bugfix some references to the internal prefixify function.

*Release 20190324*:
Pfx.__exit__: apply the prefix to all the standard attributes where present, improves some message behaviour for some exception types.

*Release 20181231*:
Bugfix for an infinite regress.

*Release 20181109*:
* Update @contextmanager formalism to use try/finally for the cleanup phase.
* New decorator @gen to manage Pfx state across generator iterations; pretty clunky.
* Better fallback handling.
* Some docstring updates.

*Release 20170910*:
Slight linting.

*Release 20170903.1*:
corrections to the module docstring

*Release 20170903*:
Initial release for PyPI.
