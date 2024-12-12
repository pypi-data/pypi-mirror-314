#ifndef __COM_GITHUB_TARSA_TARSALZP_PRELUDE_STREAMS_HPP
#define __COM_GITHUB_TARSA_TARSALZP_PRELUDE_STREAMS_HPP

using namespace __shedskin__;
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __prelude__ {
namespace __Streams__ {

extern str *const_0, *const_1, *const_2;

class BufferedInputStream;
class BufferedOutputStreamWrapper;
class OutputStream;
class FileOutputStream;
class DelayedFileOutputStream;


extern str *__author__, *__name__;


extern class_ *cl_BufferedInputStream;
class BufferedInputStream : public pyobj {
public:
    static __ss_int Limit;

    file_binary *_input;
    __ss_int position;
    __ss_int limit;
    __array__::array<__ss_int> *buffer;

    BufferedInputStream() {}
    BufferedInputStream(file_binary *input) {
        this->__class__ = cl_BufferedInputStream;
        __init__(input);
    }
    static void __static__();
    void *__init__(file_binary *input);
    __ss_int readByte();
    void *close();
};

extern class_ *cl_BufferedOutputStreamWrapper;
class BufferedOutputStreamWrapper : public pyobj {
public:
    static __ss_int Limit;

    __ss_int position;
    OutputStream *outputStream;
    __array__::array<__ss_int> *buffer;
    __ss_int limit;

    BufferedOutputStreamWrapper() {}
    BufferedOutputStreamWrapper(OutputStream *outputStream) {
        this->__class__ = cl_BufferedOutputStreamWrapper;
        __init__(outputStream);
    }
    static void __static__();
    void *__init__(OutputStream *outputStream);
    void *writeByte(__ss_int octet);
    void *flush();
    void *close();
};

extern class_ *cl_OutputStream;
class OutputStream : public pyobj {
public:

    OutputStream() { this->__class__ = cl_OutputStream; }
    static void __static__();
    virtual void *writeByteArray(__array__::array<__ss_int> *byteArray) { return 0; };
    virtual void *close() { return 0; };
};

extern class_ *cl_FileOutputStream;
class FileOutputStream : public OutputStream {
public:
    file_binary *output;

    FileOutputStream() {}
    FileOutputStream(file_binary *fileHandle) {
        this->__class__ = cl_FileOutputStream;
        __init__(fileHandle);
    }
    void *__init__(file_binary *fileHandle);
    void *writeByteArray(__array__::array<__ss_int> *byteArray);
    void *close();
};

extern class_ *cl_DelayedFileOutputStream;
class DelayedFileOutputStream : public OutputStream {
public:
    file_binary *output;
    __ss_bool initialized;
    str *fileName;

    DelayedFileOutputStream() {}
    DelayedFileOutputStream(str *fileName) {
        this->__class__ = cl_DelayedFileOutputStream;
        __init__(fileName);
    }
    void *__init__(str *fileName);
    void *writeByteArray(__array__::array<__ss_int> *byteArray);
    void *close();
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
