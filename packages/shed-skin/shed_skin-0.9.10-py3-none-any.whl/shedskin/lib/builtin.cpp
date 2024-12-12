/* Copyright 2005-2011 Mark Dufour and contributors; License Expat (See LICENSE) */

#include "builtin.hpp"
#include "re.hpp"
#include <climits>
#include <cmath>
#include <numeric>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

namespace __shedskin__ {


class_ *cl_class_, *cl_none, *cl_str_, *cl_int_, *cl_bool, *cl_float_, *cl_complex, *cl_list, *cl_tuple, *cl_dict, *cl_set, *cl_object, *cl_rangeiter, *cl_xrange, *cl_bytes;

class_ *cl_stopiteration, *cl_assertionerror, *cl_eoferror, *cl_floatingpointerror, *cl_keyerror, *cl_indexerror, *cl_typeerror, *cl_valueerror, *cl_zerodivisionerror, *cl_keyboardinterrupt, *cl_memoryerror, *cl_nameerror, *cl_notimplementederror, *cl_oserror, *cl_overflowerror, *cl_runtimeerror, *cl_syntaxerror, *cl_systemerror, *cl_systemexit, *cl_filenotfounderror, *cl_arithmeticerror, *cl_lookuperror, *cl_exception, *cl_baseexception, *cl_pythonfinalizationerror;

str *sp, *nl, *__fmt_s, *__fmt_H, *__fmt_d;
bytes *bsp;

__GC_STRING ws, __fmtchars;
__GC_VECTOR(str *) __char_cache;
__GC_VECTOR(bytes *) __byte_cache;

__ss_bool True;
__ss_bool False;

str *__case_swap_cache;

char __str_cache[4000];

file *__ss_stdin, *__ss_stdout, *__ss_stderr;

#ifdef __SS_BIND
dict<void *, void *> *__ss_proxy;
#endif

void gc_warning_handler(char *, GC_word) {}

void __init() {
    GC_INIT();
    GC_set_warn_proc(gc_warning_handler);
#ifdef __SS_NOGC
    GC_disable();
#endif

#ifdef __SS_BIND
    Py_Initialize();
    __ss_proxy = new dict<void *, void *>();
#endif

    cl_class_ = new class_ ("class");
    cl_none = new class_("None");
    cl_str_ = new class_("str");
    cl_bytes = new class_("bytes");
    cl_int_ = new class_("int");
    cl_float_ = new class_("float");
    cl_list = new class_("list");
    cl_tuple = new class_("tuple");
    cl_dict = new class_("dict");
    cl_set = new class_("set");
    cl_object = new class_("object");
    cl_rangeiter = new class_("rangeiter");
    cl_complex = new class_("complex");
    cl_xrange = new class_("xrange");

    True.value = 1;
    False.value = 0;

    ws = " \n\r\t\f\v";
    __fmtchars = "#*-+ .0123456789hlL";
    sp = new str(" ");
    bsp = new bytes(" ");
    nl = new str("\n");
    __fmt_s = new str("%s");
    __fmt_H = new str("%H");
    __fmt_d = new str("%d");

    for(int i=0;i<256;i++) {
        char c = (char)i;
        str *charstr = new str(&c, 1);
        charstr->charcache = 1;
        __char_cache.push_back(charstr);
    }

    for(int i=0;i<256;i++) {
        char c = (char)i;
        bytes *charbytes = new bytes(&c, 1, 1);
//        charbytes->charcache = 1; // TODO add and use in bytes.__contains__
        __byte_cache.push_back(charbytes);
    }

    for(int i=0; i<1000; i++) {
        __str_cache[4*i] = '0' + (char)(i % 10);
        __str_cache[4*i+1] = '0' + (char)((i/10) % 10);
        __str_cache[4*i+2] = '0' + (char)((i/100) % 10);
    }

    __case_swap_cache = new str();
    for(int i=0; i<256; i++) {
        char c = (char)i;
        if(::islower(c))
            __case_swap_cache->unit += (char)::toupper(c);
        else
            __case_swap_cache->unit += (char)::tolower(c);
    }

    __ss_stdin = new file(stdin);
    __ss_stdin->name = new str("<stdin>");
    __ss_stdout = new file(stdout);
    __ss_stdout->name = new str("<stdout>");
    __ss_stderr = new file(stderr);
    __ss_stderr->name = new str("<stderr>");

    cl_baseexception = new class_("BaseException");
    cl_exception = new class_("Exception");
    cl_stopiteration = new class_("StopIteration");
    cl_assertionerror = new class_("AssertionError");
    cl_eoferror = new class_("EOFError");
    cl_floatingpointerror = new class_("FloatingPointError");
    cl_keyerror = new class_("KeyError");
    cl_indexerror = new class_("IndexError");
    cl_typeerror = new class_("TypeError");
    cl_filenotfounderror = new class_("FileNotFoundError");
    cl_valueerror = new class_("ValueError");
    cl_zerodivisionerror = new class_("ZeroDivisionError");
    cl_keyboardinterrupt = new class_("KeyboardInterrupt");
    cl_memoryerror = new class_("MemoryError");
    cl_nameerror = new class_("NameError");
    cl_notimplementederror = new class_("NotImplementedError");
    cl_pythonfinalizationerror = new class_("PythonFinalizationError");
    cl_oserror = new class_("OSError");
    cl_overflowerror = new class_("OverflowError");
    cl_runtimeerror = new class_("RuntimeError");
    cl_syntaxerror = new class_("SyntaxError");
    cl_systemerror = new class_("SystemError");
    cl_systemexit = new class_("SystemExit");
    cl_arithmeticerror = new class_("ArithmeticError");
    cl_lookuperror = new class_("LookupError");

}

class_::class_(const char *name) {
    this->__name__ = new str(name);
}

str *class_::__repr__() {
    return __add_strs(3, new str("<class "), __name__, new str(">"));
}

__ss_bool class_::__eq__(pyobj *c) {
    return __mbool(c == this);
}

#include "builtin/file.cpp"
#include "builtin/math.cpp"
#include "builtin/bool.cpp"
#include "builtin/complex.cpp"
#include "builtin/str.cpp"
#include "builtin/bytes.cpp"
#include "builtin/exception.cpp"
#include "builtin/function.cpp"
#include "builtin/format.cpp"


void __add_missing_newline() {
    if(__ss_stdout->options.lastchar != '\n')
        __ss_stdout->write(new str("\n"));
}

/* print traceback for uncaught exception, may only work for GCC */

void terminate_handler() {
    int code = 0;

    static bool terminating = false;
    if(terminating)
        abort();

    terminating = true;
    try
    {
        // rethrow to detect uncaught exception, will recursively
        // call terminate() if no exception is active (which is
        // detected above).
        throw;

    } catch (SystemExit *s) {
        __add_missing_newline(); /* XXX s->message -> stderr? */
        if(s->show_message)
            print_(0, False, __ss_stderr, NULL, NULL, s->message);
        code = s->code;

    } catch (BaseException *e) {
        __add_missing_newline();

#ifndef WIN32
#ifdef __SS_BACKTRACE
        print_traceback(stdout);
#endif
#endif

        str *s = __str(e);
        if(___bool(s))
            print_(0, False, NULL, NULL, NULL, __add_strs(3, e->__class__->__name__, new str(": "), s));
        else
            print_(0, False, NULL, NULL, NULL, e->__class__->__name__);
        code = 1;
    }

    std::exit(code);
}

/* starting and stopping */

void __start(void (*initfunc)()) {
    std::set_terminate(terminate_handler);
    initfunc();
    std::exit(0);
}

void __ss_exit(int code) {
    throw new SystemExit(code);
}

/* glue */

#ifdef __SS_BIND
template<> PyObject *__to_py(int32_t i) { return PyLong_FromLong(i); }
template<> PyObject *__to_py(int64_t i) { return PyLong_FromLongLong(i); }

#ifdef __SS_INT128
template<> PyObject *__to_py(__int128 i) {
    int num = 1;
    bool little_endian = (*(char *)&num == 1);
    return _PyLong_FromByteArray((const unsigned char *)&i, sizeof(i), little_endian, 1);
}

#endif
#ifdef WIN32
template<> PyObject *__to_py(long i) { return PyLong_FromLong(i); }
#endif
#ifdef __APPLE__
template<> PyObject *__to_py(long i) { return PyLong_FromLong(i); }
#endif
template<> PyObject *__to_py(__ss_bool i) { return PyBool_FromLong(i.value); }
template<> PyObject *__to_py(__ss_float d) { return PyFloat_FromDouble(d); }
template<> PyObject *__to_py(void *) { Py_INCREF(Py_None); return Py_None; }

void throw_exception() {
    PyObject *ptype, *pvalue, *ptraceback;
    PyErr_Fetch(&ptype, &pvalue, &ptraceback);
    char *pStrErrorMessage = PyBytes_AS_STRING(pvalue);
    throw new TypeError(new str(pStrErrorMessage));
}

template<> __ss_int __to_ss(PyObject *p) {
    if(PyLong_Check(p)) {
        __ss_int result;
#ifdef __SS_INT128
        int num = 1;
        bool little_endian = (*(char *)&num == 1);
        _PyLong_AsByteArray((PyLongObject *)p, (unsigned char *)&result, sizeof(__ss_int), little_endian, 1);
#else
        result = (__ss_int)PyLong_AsLongLong(p);
#endif
        if (result == -1 && PyErr_Occurred() != NULL) {
            throw_exception();
        }
        return result;
    }

    throw new TypeError(new str("error in conversion to Shed Skin (integer expected)"));
}

template<> __ss_bool __to_ss(PyObject *p) {
    if(!PyBool_Check(p))
        throw new TypeError(new str("error in conversion to Shed Skin (boolean expected)"));
    return (p==Py_True)?(__mbool(true)):(__mbool(false));
}

template<> __ss_float __to_ss(PyObject *p) {
    if(!PyLong_Check(p) and !PyFloat_Check(p))
        throw new TypeError(new str("error in conversion to Shed Skin (float or int expected)"));
    return PyFloat_AsDouble(p);
}

template<> void * __to_ss(PyObject *p) {
    if(p!=Py_None)
        throw new TypeError(new str("error in conversion to Shed Skin (None expected)"));
    return NULL;
}
#endif

template<> int __none() { throw new TypeError(new str("mixing None with int")); }
template<> __ss_float __none() { throw new TypeError(new str("mixing None with float")); }

/* pyobj */

str *pyobj::__str__() { return __repr__(); }

str *pyobj::__repr__() {
    std::stringstream stream;
    stream << "0x" << std::hex << reinterpret_cast<uintptr_t>(this);
    return __add_strs(5, new str("<"), __class__->__name__, new str(" object at "), new str(stream.str().c_str()), new str(">"));
}

long pyobj::__hash__() {
    return (intptr_t)this;
}

__ss_int pyobj::__cmp__(pyobj *p) {
    return __cmp<void *>(this, p);
}

__ss_bool pyobj::__eq__(pyobj *p) { return __mbool(this == p); }
__ss_bool pyobj::__ne__(pyobj *p) { return __mbool(!__eq__(p)); }

__ss_bool pyobj::__gt__(pyobj *p) { return __mbool(__cmp__(p) == 1); }
__ss_bool pyobj::__lt__(pyobj *p) { return __mbool(__cmp__(p) == -1); }
__ss_bool pyobj::__ge__(pyobj *p) { return __mbool(__cmp__(p) != -1); }
__ss_bool pyobj::__le__(pyobj *p) { return __mbool(__cmp__(p) != 1); }

pyobj *pyobj::__copy__() { return this; }
pyobj *pyobj::__deepcopy__(dict<void *, pyobj *> *) { return this; }

__ss_int pyobj::__len__() { return 1; } /* XXX exceptions? */
__ss_int pyobj::__int__() { return 0; }

__ss_bool pyobj::__nonzero__() { return __mbool(__len__() != 0); }

__ss_int pyobj::__index__() { throw new TypeError(new str("no such method: '__index__'")); }

/* object */

object::object() { this->__class__ = cl_object; }

#ifdef __SS_BIND
PyObject *__ss__newobj__(PyObject *, PyObject *args, PyObject *kwargs) {
    PyObject *cls = PyTuple_GetItem(args, 0);
    PyObject *__new__ = PyObject_GetAttrString(cls, "__new__");
    return PyObject_Call(__new__, args, kwargs);
}
#endif

/* slicing helper */

void slicenr(__ss_int x, __ss_int &l, __ss_int &u, __ss_int &s, __ss_int len) {
    if(x&4) {
        if (s == 0)
            __throw_slice_step_zero();
    } else
        s = 1;

    if (l>=len)
        l = len;
    else if (l<0) {
        l = len+l;
        if(l<0)
            l = 0;
    }
    if (u>=len)
        u = len;
    else if (u<0) {
        u = len+u;
        if(u<0)
            u = 0;
    }

    if(s<0) {
        if (!(x&1))
            l = len-1;
        if (!(x&2))
            u = -1;
    }
    else {
        if (!(x&1))
            l = 0;
        if (!(x&2))
            u = len;
    }
}

} // namespace __shedskin__
