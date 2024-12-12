#ifndef __COM_GITHUB_TARSA_TARSALZP_OPTIONS_HPP
#define __COM_GITHUB_TARSA_TARSALZP_OPTIONS_HPP

using namespace __shedskin__;

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
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __Options__ {

extern str *const_0;

class Options;


extern str *__author__, *__name__;


extern class_ *cl_Options;
class Options : public pyobj {
public:

    __ss_int lzpLowContextLength;
    __ss_int literalCoderOrder;
    __ss_int lzpLowMaskSize;
    __ss_int lzpHighContextLength;
    __ss_int literalCoderInit;
    __ss_int literalCoderStep;
    __ss_int literalCoderLimit;
    __ss_int lzpHighMaskSize;

    Options() {}
    Options(__ss_int lzpLowContextLength, __ss_int lzpLowMaskSize, __ss_int lzpHighContextLength, __ss_int lzpHighMaskSize, __ss_int literalCoderOrder, __ss_int literalCoderInit, __ss_int literalCoderStep, __ss_int literalCoderLimit) {
        this->__class__ = cl_Options;
        __init__(lzpLowContextLength, lzpLowMaskSize, lzpHighContextLength, lzpHighMaskSize, literalCoderOrder, literalCoderInit, literalCoderStep, literalCoderLimit);
    }
    void *__init__(__ss_int lzpLowContextLength, __ss_int lzpLowMaskSize, __ss_int lzpHighContextLength, __ss_int lzpHighMaskSize, __ss_int literalCoderOrder, __ss_int literalCoderInit, __ss_int literalCoderStep, __ss_int literalCoderLimit);
    __ss_bool isValid();
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *toPacked();
    static Options *fromPacked(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *packed);
    static Options *getDefault();
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
