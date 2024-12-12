#ifndef __COM_GITHUB_TARSA_TARSALZP_CORE_DECODER_HPP
#define __COM_GITHUB_TARSA_TARSALZP_CORE_DECODER_HPP

using namespace __shedskin__;

namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __Options__ { /* XXX */
class Options;
}
}
}
}
}
namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __prelude__ { /* XXX */
namespace __Streams__ { /* XXX */
class BufferedInputStream;
class BufferedOutputStreamWrapper;
class OutputStream;
class FileOutputStream;
class DelayedFileOutputStream;
}
}
}
}
}
}
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __Decoder__ {

extern str *const_0, *const_1;

class Decoder;


extern str *__author__, *__name__;


extern class_ *cl_Decoder;
class Decoder : public __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::Common {
public:
    __ss_int nextHighBit;
    __ss_int rcRange;
    __ss_int rcBuffer;
    __ss_bool started;

    Decoder() {}
    Decoder(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
        this->__class__ = cl_Decoder;
        __init__(inputStream, outputStream, options);
    }
    void *__init__(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options);
    __ss_int inputByte();
    void *init();
    void *normalize();
    __ss_bool decodeFlag(__ss_int probability);
    __ss_bool decodeSkewed();
    __ss_int decodeSingleOnlyLowLzp();
    __ss_int decodeSingle();
    __ss_int decodeSymbol(__ss_int mispredictedSymbol);
    __ss_bool decode(__ss_int limit);
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
