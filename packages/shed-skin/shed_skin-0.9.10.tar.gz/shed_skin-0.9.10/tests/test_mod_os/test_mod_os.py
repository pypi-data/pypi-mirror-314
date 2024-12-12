import os


#def test_popen():
#    # https://github.com/shedskin/shedskin/issues/191
#    assert os.popen("echo Hello World").read() == 'Hello World\n'


def test_getcwd():
    os.getcwd()


def test_env():
    os.environ['bert'] = 'value'
#    assert os.getenv('bert') == 'value'  # TODO

    os.putenv('bert', 'value2') # does not change os.environ


def test_urandom():
    bts = os.urandom(10)
    assert len(bts) == 10
    assert bts.__class__.__name__ == 'bytes'


def test_posix():
    assert os.curdir == '.'
    assert os.pardir == '..'
    assert os.sep == '/'
    assert os.altsep is None
    assert os.extsep == '.'
    assert os.pathsep == ':'
    assert os.defpath == '/bin:/usr/bin'
    assert os.linesep == '\n'
    assert os.devnull == '/dev/null'


def test_rdwr():
    fd = os.open('/dev/null', os.O_RDWR)
    assert os.write(fd, b'blah') == 4
    assert os.read(fd, 10) == b''
    os.close(fd)


def test_system():
    assert os.system('ls') == 0


def test_exceptions():
    try:
        os.chdir("ontehunoe")
    except FileNotFoundError as e:
        assert e.errno == 2
        assert e.filename == "ontehunoe"


def test_all():
    test_getcwd()
    test_exceptions()
#    test_popen() # windows?

    if os.name == 'posix':  # TODO 'nt'
        test_posix()
        test_env()
        test_rdwr()
        test_system()
        test_urandom()


if __name__ == '__main__':
    test_all()
