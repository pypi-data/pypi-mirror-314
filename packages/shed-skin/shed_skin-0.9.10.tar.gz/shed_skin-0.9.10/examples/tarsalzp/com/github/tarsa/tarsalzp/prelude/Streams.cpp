#include "builtin.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Streams.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __prelude__ {
namespace __Streams__ {

str *const_0, *const_1, *const_2;


str *__author__, *__name__;


class list_comp_0 : public __iter<__ss_int> {
public:
    __ss_int _, __1, __2;

    int __last_yield;

    list_comp_0();
    __ss_int __get_next();
};


list_comp_0::list_comp_0() {
    __last_yield = -1;
}

__ss_int list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,BufferedOutputStreamWrapper::Limit,1,1,2)
        __result = __ss_int(0);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

/**
class BufferedInputStream
*/

class_ *cl_BufferedInputStream;

void *BufferedInputStream::__init__(file_binary *input) {
    this->_input = input;
    this->buffer = NULL;
    this->position = __ss_int(0);
    this->limit = __ss_int(0);
    return NULL;
}

__ss_int BufferedInputStream::readByte() {
    __ss_int result;


    while ((this->position==this->limit)) {
        this->position = __ss_int(0);
        this->buffer = (new __array__::array<__ss_int>(const_0));
        try {
            (this->buffer)->fromfile(this->_input, BufferedInputStream::Limit);
        } catch (EOFError *) {
        }
        this->limit = len(this->buffer);
        if (__NOT(this->limit)) {
            return (-__ss_int(1));
        }
    }
    result = (this->buffer)->__getfast__(this->position);
    this->position = (this->position+__ss_int(1));
    return result;
}

void *BufferedInputStream::close() {
    (this->_input)->close();
    return NULL;
}

__ss_int BufferedInputStream::Limit;

void BufferedInputStream::__static__() {
    Limit = __ss_int(65536);
}

/**
class BufferedOutputStreamWrapper
*/

class_ *cl_BufferedOutputStreamWrapper;

void *BufferedOutputStreamWrapper::__init__(OutputStream *outputStream) {
    void *_;

    this->outputStream = outputStream;
    this->buffer = (new __array__::array<__ss_int>(const_0, new list_comp_0()));
    this->position = __ss_int(0);
    this->limit = len(this->buffer);
    return NULL;
}

void *BufferedOutputStreamWrapper::writeByte(__ss_int octet) {
    __array__::array<__ss_int> *__3;

    if ((this->position==this->limit)) {
        this->flush();
    }
    this->buffer->__setitem__(this->position, octet);
    this->position = (this->position+__ss_int(1));
    return NULL;
}

void *BufferedOutputStreamWrapper::flush() {
    (this->outputStream)->writeByteArray((this->buffer)->__slice__(__ss_int(2), __ss_int(0), this->position, __ss_int(0)));
    this->position = __ss_int(0);
    return NULL;
}

void *BufferedOutputStreamWrapper::close() {
    (this->outputStream)->close();
    return NULL;
}

__ss_int BufferedOutputStreamWrapper::Limit;

void BufferedOutputStreamWrapper::__static__() {
    Limit = __ss_int(65536);
}

/**
class OutputStream
*/

class_ *cl_OutputStream;

void OutputStream::__static__() {
}

/**
class FileOutputStream
*/

class_ *cl_FileOutputStream;

void *FileOutputStream::__init__(file_binary *fileHandle) {
    this->output = fileHandle;
    return NULL;
}

void *FileOutputStream::writeByteArray(__array__::array<__ss_int> *byteArray) {
    byteArray->tofile(this->output);
    return NULL;
}

void *FileOutputStream::close() {
    (this->output)->close();
    return NULL;
}

/**
class DelayedFileOutputStream
*/

class_ *cl_DelayedFileOutputStream;

void *DelayedFileOutputStream::__init__(str *fileName) {
    this->fileName = fileName;
    this->initialized = False;
    this->output = NULL;
    return NULL;
}

void *DelayedFileOutputStream::writeByteArray(__array__::array<__ss_int> *byteArray) {
    if (__NOT(this->initialized)) {
        this->initialized = True;
        this->output = open_binary(this->fileName, const_1);
    }
    byteArray->tofile(this->output);
    return NULL;
}

void *DelayedFileOutputStream::close() {
    if (this->initialized) {
        (this->output)->close();
    }
    return NULL;
}

void __init() {
    const_0 = __char_cache[66];
    const_1 = new str("w+b");
    const_2 = new str("Piotr Tarsa");

    __name__ = new str("Streams");

    __author__ = const_2;
    cl_BufferedInputStream = new class_("BufferedInputStream");
    BufferedInputStream::__static__();
    cl_BufferedOutputStreamWrapper = new class_("BufferedOutputStreamWrapper");
    BufferedOutputStreamWrapper::__static__();
    cl_OutputStream = new class_("OutputStream");
    OutputStream::__static__();
    cl_FileOutputStream = new class_("FileOutputStream");
    cl_DelayedFileOutputStream = new class_("DelayedFileOutputStream");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

