#ifndef __COM_GITHUB_TARSA_TARSALZP_CORE_CODER_HPP
#define __COM_GITHUB_TARSA_TARSALZP_CORE_CODER_HPP

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
namespace __Long__ { /* XXX */
class Long;
}
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
namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __core__ { /* XXX */
namespace __Decoder__ { /* XXX */
class Decoder;
}
}
}
}
}
}
namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __core__ { /* XXX */
namespace __Encoder__ { /* XXX */
class Encoder;
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
namespace __Coder__ {

extern str *const_0, *const_1, *const_2, *const_3, *const_4;

class Coder;


extern str *__author__, *__name__;


extern class_ *cl_Coder;
class Coder : public pyobj {
public:
    static __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *HeaderValue;

    Coder() { this->__class__ = cl_Coder; }
    static void __static__();
    static __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *getOptions(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream);
    static __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *getOptionsHeaderless(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream);
    static void *checkInterval(__ss_int intervalLength);
    static void *decode(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength);
    static void *decodeRaw(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options);
    static void *encode(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options);
    static void *doEncode(__com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::Encoder *encoder, __ss_int intervalLength);
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
