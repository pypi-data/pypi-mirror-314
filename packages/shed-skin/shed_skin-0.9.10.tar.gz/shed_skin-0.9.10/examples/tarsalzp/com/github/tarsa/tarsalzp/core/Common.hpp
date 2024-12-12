#ifndef __COM_GITHUB_TARSA_TARSALZP_CORE_COMMON_HPP
#define __COM_GITHUB_TARSA_TARSALZP_CORE_COMMON_HPP

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
namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __core__ { /* XXX */
namespace __FsmGenerator__ { /* XXX */
class FsmGenerator;
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
namespace __Common__ {

extern str *const_0, *const_1, *const_2, *const_3;

class Common;


extern str *__author__, *__name__;


extern class_ *cl_Common;
class Common : public pyobj {
public:
    static __ss_int CostScale;
    static __array__::array<__ss_int> *StateTable;

    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream;
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream;
    __ss_int lzpLowContextLength;
    __ss_int lzpLowMaskSize;
    __ss_int lzpHighContextLength;
    __ss_int lzpHighMaskSize;
    __ss_int literalCoderOrder;
    __ss_int literalCoderInit;
    __ss_int literalCoderStep;
    __ss_int literalCoderLimit;
    __ss_int lzpLowMask;
    __ss_int lzpHighMask;
    __array__::array<__ss_int> *lzpLow;
    __ss_bool onlyLowLzp;
    __array__::array<__ss_int> *lzpHigh;
    __array__::array<__ss_int> *rangesSingle;
    __array__::array<__ss_int> *rangesGrouped;
    __array__::array<__ss_int> *rangesTotal;
    __ss_int recentCost;
    __array__::array<__ss_int> *apmLow;
    __array__::array<__ss_int> *apmHigh;
    __ss_int historyLow;
    __ss_int historyHigh;
    __ss_int historyLowMask;
    __ss_int historyHighMask;
    __ss_int lastLiteralCoderContext;
    __array__::array<__ss_int> *context;
    __ss_int contextIndex;
    __ss_int hashLow;
    __ss_int hashHigh;
    __array__::array<__ss_int> *precomputedHashes;

    Common() {}
    Common(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
        this->__class__ = cl_Common;
        __init__(inputStream, outputStream, options);
    }
    static void __static__();
    void *__init__(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options);
    void *updateContext(__ss_int input);
    void *computeLiteralCoderContext();
    void *computeHashesOnlyLowLzp();
    void *computeHashes();
    __ss_int getNextState(__ss_int state, __ss_bool match);
    __ss_int getLzpStateLow();
    __ss_int getLzpStateHigh();
    __ss_int getLzpPredictedSymbolLow();
    __ss_int getLzpPredictedSymbolHigh();
    void *updateLzpStateLow(__ss_int lzpStateLow, __ss_int input, __ss_bool match);
    void *updateLzpStateHigh(__ss_int lzpStateHigh, __ss_int input, __ss_bool match);
    __ss_int getApmLow(__ss_int state);
    __ss_int getApmHigh(__ss_int state);
    void *updateApmHistoryLow(__ss_bool match);
    void *updateApmHistoryHigh(__ss_bool match);
    void *updateApmLow(__ss_int state, __ss_bool match);
    void *updateApmHigh(__ss_int state, __ss_bool match);
    void *rescaleLiteralCoder();
    void *updateLiteralCoder(__ss_int index);
    __ss_bool useFixedProbabilities();
    void *updateRecentCost(__ss_int symbolFrequency, __ss_int totalFrequency);
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
