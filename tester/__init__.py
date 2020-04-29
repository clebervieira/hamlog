import logging

'''
python test infrastructure
'''

_g_logging_defaultFormat = "%(asctime)s %(levelname)s - %(name)s::%(funcName)s()@%(lineno)d: %(message)s"

def _initializeLogging(filename = None, level = logging.DEBUG, format = _g_logging_defaultFormat):
    if filename:
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        logging.basicConfig(level=level, format=format, filename=filename)
    else:
        logging.basicConfig(level=level, format=format)

def runTests(*args):
    if len(args) == 0:
        print("usage:  tester [--log-level=LEVEL] [--iterations=ITERS] [--pkg=PKGNAME] [--continue|--abort] module[.class[.method]] ...".format(__name__))
        print("        --continue is the default behavior.")
        print("        Any part of the test argument(s) can be replaced with wildcards.")
        print("        Supported wildcards include:")
        print("           *       matches anything")
        print("           ?       matches any single character")
        print("           [seq]   matches any character in seq")
        print("           [!seq]  matches any character not in seq")
        print("\n        Examples:")
        print("           py -m tester basic")
        print("           -> runs all tests in tests/basic.py")
        print("\n           py -m tester basic.SimpleTests")
        print("           -> runs all 'test_' methods in the SimpleTests class in tests/basic.py")
        print("\n           py -m tester basic.SimpleTests.test_foo")
        print("           -> runs test_foo test in the SimpleTests class in tests/basic.py")
        print("\n           py -m tester basic.*.test_f*")
        print("           -> runs all tests that start with 'f' in tests/basic.py")
        print("\n           py -m tester 'basic.[!f]*'")
        print("           -> runs all tests in all test classes that _don't_ start with 'f' in tests/basic.py")
        return
    logLevel = logging.INFO
    for arg in args:
        if arg.startswith("--log-level="):
            logLevel = eval("logging.{}".format(arg.split('=')[-1]))
    _initializeLogging(level=logLevel)
    from .harness import Harness
    return Harness(args).run()
