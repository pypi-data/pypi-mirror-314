#include "builtin.hpp"
#include "time.hpp"
#include "sys.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/prelude/__init__.hpp"
#include "com/github/tarsa/tarsalzp/Main.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"
#include "com/github/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/__init__.hpp"
#include "com/github/tarsa/tarsalzp/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/FsmGenerator.hpp"
#include "com/github/tarsa/tarsalzp/Options.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Streams.hpp"
#include "com/github/tarsa/tarsalzp/core/Common.hpp"
#include "com/github/tarsa/tarsalzp/core/Decoder.hpp"
#include "com/github/tarsa/tarsalzp/core/Encoder.hpp"
#include "com/github/tarsa/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/Coder.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"
#include "com/__init__.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __Main__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_40, *const_41, *const_42, *const_43, *const_44, *const_45, *const_5, *const_6, *const_7, *const_8, *const_9;

using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream;
using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper;
using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::OutputStream;
using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::FileOutputStream;
using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::DelayedFileOutputStream;
using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Coder__::Coder;
using __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options;
using __time__::time;

str *__author__, *__name__;
file *__ss_stderr;



/**
class Main
*/

class_ *cl_Main;

void *Main::err(str *string) {
    __com__::__github__::__tarsa__::__tarsalzp__::__Main__::__ss_stderr->write((string)->__add__(const_0));
    return NULL;
}

void *Main::printHelp() {
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options;

    this->err(const_1);
    this->err(const_2);
    this->err(const_3);
    this->err(const_4);
    this->err(const_5);
    this->err(const_6);
    this->err(const_7);
    this->err(const_8);
    this->err(const_9);
    this->err(const_10);
    options = Options::getDefault();
    this->err((const_11)->__add__(__str(options->lzpLowContextLength)));
    this->err((const_12)->__add__(__str(options->lzpLowMaskSize)));
    this->err((const_13)->__add__(__str(options->lzpHighContextLength)));
    this->err((const_14)->__add__(__str(options->lzpHighMaskSize)));
    this->err((const_15)->__add__(__str(options->literalCoderOrder)));
    this->err((const_16)->__add__(__str(options->literalCoderInit)));
    this->err((const_17)->__add__(__str(options->literalCoderStep)));
    this->err((const_18)->__add__(__str(options->literalCoderLimit)));
    return NULL;
}

dict<str *, str *> *Main::convertOptions(list<str *> *args) {
    dict<str *, str *> *optionsMap;
    str *arg;
    __ss_int __179, splitPoint;
    list<str *> *__177;
    __iter<str *> *__178;
    list<str *>::for_in_loop __180;

    optionsMap = (new dict<str *, str *>());

    FOR_IN(arg,args->__slice__(__ss_int(1), __ss_int(2), __ss_int(0), __ss_int(0)),177,179,180)
        splitPoint = arg->find(const_19);
        if ((splitPoint==(-__ss_int(1)))) {
            return NULL;
        }
        if ((optionsMap)->__contains__(arg->__slice__(__ss_int(2), __ss_int(0), splitPoint, __ss_int(0)))) {
            return NULL;
        }
        optionsMap->__setitem__(arg->__slice__(__ss_int(2), __ss_int(0), splitPoint, __ss_int(0)), arg->__slice__(__ss_int(1), (splitPoint+__ss_int(1)), __ss_int(0), __ss_int(0)));
    END_FOR

    return optionsMap;
}

void *Main::encode(dict<str *, str *> *optionsMap) {
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream;
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream;
    __ss_bool standardInput, standardOutput;
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options;
    str *fileName, *key, *keyOriginal;
    file_binary *fileHandle;
    dict<str *, str *> *__181;
    __iter<str *> *__182;
    __ss_int __183;
    dict<str *, str *>::for_in_loop __184;

    inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream((__sys__::__ss_stdin)->buffer));
    outputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper(((__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::OutputStream *)((new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::FileOutputStream((__sys__::__ss_stdout)->buffer))))));
    standardInput = True;
    standardOutput = True;
    options = Options::getDefault();

    FOR_IN(keyOriginal,optionsMap,181,183,184)
        key = keyOriginal->lower();
        if (__eq(key, const_20)) {
            fileHandle = open_binary(optionsMap->__getitem__(keyOriginal), const_21);
            inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream(fileHandle));
            standardInput = False;
        }
        else if (__eq(key, const_22)) {
            fileName = optionsMap->__getitem__(keyOriginal);
            outputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper(((__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::OutputStream *)((new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::DelayedFileOutputStream(fileName))))));
            standardOutput = False;
        }
        else if (__eq(key, (const_23)->lower())) {
            options->lzpLowContextLength = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_24)->lower())) {
            options->lzpLowMaskSize = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_25)->lower())) {
            options->lzpHighContextLength = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_26)->lower())) {
            options->lzpHighMaskSize = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_27)->lower())) {
            options->literalCoderOrder = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_28)->lower())) {
            options->literalCoderInit = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_29)->lower())) {
            options->literalCoderStep = __int(optionsMap->__getitem__(keyOriginal));
        }
        else if (__eq(key, (const_30)->lower())) {
            options->literalCoderLimit = __int(optionsMap->__getitem__(keyOriginal));
        }
        else {
            this->err((const_31)->__add__(keyOriginal));
            return NULL;
        }
    END_FOR

    if (__NOT(options->isValid())) {
        this->err(const_32);
        return NULL;
    }
    Coder::encode(inputStream, outputStream, __ss_int(65536), options);
    outputStream->flush();
    if (__NOT(standardInput)) {
        inputStream->close();
    }
    if (__NOT(standardOutput)) {
        outputStream->close();
    }
    return 0;
}

void *Main::decode(dict<str *, str *> *optionsMap) {
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream;
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream;
    __ss_bool allDecoded, standardInput, standardOutput;
    str *fileName, *key, *keyOriginal;
    file_binary *fileHandle;
    dict<str *, str *> *__185;
    __iter<str *> *__186;
    __ss_int __187;
    dict<str *, str *>::for_in_loop __188;

    inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream((__sys__::__ss_stdin)->buffer));
    outputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper(((__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::OutputStream *)((new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::FileOutputStream((__sys__::__ss_stdout)->buffer))))));
    standardInput = True;
    standardOutput = True;

    FOR_IN(keyOriginal,optionsMap,185,187,188)
        key = keyOriginal->lower();
        if (__eq(key, const_20)) {
            fileHandle = open_binary(optionsMap->__getitem__(keyOriginal), const_21);
            inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream(fileHandle));
            standardInput = False;
        }
        else if (__eq(key, const_22)) {
            fileName = optionsMap->__getitem__(keyOriginal);
            outputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper(((__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::OutputStream *)((new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::DelayedFileOutputStream(fileName))))));
            standardOutput = False;
        }
        else {
            this->err((const_31)->__add__(keyOriginal));
            return NULL;
        }
    END_FOR

    Coder::decode(inputStream, outputStream, __ss_int(65536));
    outputStream->flush();
    allDecoded = ___bool((inputStream->readByte()==(-__ss_int(1))));
    if (__NOT(standardInput)) {
        inputStream->close();
    }
    if (__NOT(standardOutput)) {
        outputStream->close();
    }
    if (__NOT(allDecoded)) {
        throw ((new OSError(const_33)));
    }
    return 0;
}

void *Main::showOptions(dict<str *, str *> *optionsMap) {
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream;
    __ss_bool standardInput;
    str *key, *keyOriginal;
    file_binary *fileHandle;
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options;
    dict<str *, str *> *__189;
    __iter<str *> *__190;
    __ss_int __191;
    dict<str *, str *>::for_in_loop __192;

    inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream((__sys__::__ss_stdin)->buffer));
    standardInput = True;

    FOR_IN(keyOriginal,optionsMap,189,191,192)
        key = keyOriginal->lower();
        if (__eq(key, const_20)) {
            fileHandle = open_binary(optionsMap->__getitem__(keyOriginal), const_21);
            inputStream = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream(fileHandle));
            standardInput = False;
        }
        else {
            this->err((const_31)->__add__(keyOriginal));
            return NULL;
        }
    END_FOR

    options = Coder::getOptions(inputStream);
    this->err(repr(options));
    if (__NOT(standardInput)) {
        inputStream->close();
    }
    return 0;
}

void *Main::dispatchCommand(list<str *> *args) {
    str *command;
    dict<str *, str *> *optionsMap;

    command = args->__getfast__(__ss_int(1));
    optionsMap = this->convertOptions(args);
    if ((optionsMap==NULL)) {
        this->err(const_34);
    }
    else if (__eq(const_35, command->lower())) {
        this->encode(optionsMap);
    }
    else if (__eq(const_36, command->lower())) {
        this->decode(optionsMap);
    }
    else if (__eq((const_37)->lower(), command->lower())) {
        this->showOptions(optionsMap);
    }
    else {
        this->err((const_38)->__add__(command));
    }
    return NULL;
}

void *Main::run(list<str *> *args) {
    this->err(const_39);
    this->err(const_40);
    this->err(const_41);
    if ((len(args)==__ss_int(1))) {
        this->printHelp();
    }
    else {
        try {
            this->dispatchCommand(args);
        } catch (MemoryError *) {
            this->err(const_42);
        }
    }
    return NULL;
}

void *Main::__ss_main() {
    __ss_float start;

    start = time();
    this->run(__sys__::argv);
    this->err(__add_strs(3, const_43, __str((time()-start)), const_44));
    return NULL;
}

void __init() {
    const_0 = __char_cache[10];
    const_1 = new str("Syntax: command [option=value]*");
    const_2 = new str("Commands:");
    const_3 = new str("\t[no command]  - print help and show GUI");
    const_4 = new str("\tencode        - encode input");
    const_5 = new str("\tdecode        - decode compressed stream");
    const_6 = new str("\tshowOptions   - read and show compression options only");
    const_7 = new str("General options:");
    const_8 = new str("\tfi=fileName   - read from file `fileName` (all modes)");
    const_9 = new str("\tfo=fileName   - write to file `fileName` (encode and decode)");
    const_10 = new str("Encoding only options (with default values):");
    const_11 = new str("\tlzpLowContextLength=");
    const_12 = new str("\tlzpLowMaskSize=");
    const_13 = new str("\tlzpHighContextLength=");
    const_14 = new str("\tlzpHighMaskSize=");
    const_15 = new str("\tliteralCoderOrder=");
    const_16 = new str("\tliteralCoderInit=");
    const_17 = new str("\tliteralCoderStep=");
    const_18 = new str("\tliteralCoderLimit=");
    const_19 = __char_cache[61];
    const_20 = new str("fi");
    const_21 = new str("rb");
    const_22 = new str("fo");
    const_23 = new str("lzpLowContextLength");
    const_24 = new str("lzpLowMaskSize");
    const_25 = new str("lzpHighContextLength");
    const_26 = new str("lzpHighMaskSize");
    const_27 = new str("literalCoderOrder");
    const_28 = new str("literalCoderInit");
    const_29 = new str("literalCoderStep");
    const_30 = new str("literalCoderLimit");
    const_31 = new str("Not suitable or unknown option: ");
    const_32 = new str("Wrong encoding options combination.");
    const_33 = new str("Not entire input was decoded.");
    const_34 = new str("Duplicated or wrongly formatted options.");
    const_35 = new str("encode");
    const_36 = new str("decode");
    const_37 = new str("showOptions");
    const_38 = new str("Unknown command: ");
    const_39 = new str("TarsaLZP");
    const_40 = new str("Author: Piotr Tarsa");
    const_41 = new str("");
    const_42 = new str("Out of memory error - try lowering mask sizes.");
    const_43 = new str("Time taken: ");
    const_44 = __char_cache[115];
    const_45 = new str("Piotr Tarsa");

    __name__ = new str("Main");

    __ss_stderr = __sys__::__ss_stderr;
    __author__ = const_45;
    cl_Main = new class_("Main");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

