
if __name__ == '__main__':
    import sys
    from . import runTests
    if runTests(*sys.argv[1:]):
        sys.exit(0)
    else:
        sys.exit(1)
