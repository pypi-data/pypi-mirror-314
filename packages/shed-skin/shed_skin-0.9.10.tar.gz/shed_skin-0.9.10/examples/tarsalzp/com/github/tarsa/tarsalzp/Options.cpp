#include "builtin.hpp"
#include "com/github/tarsa/tarsalzp/prelude/__init__.hpp"
#include "com/github/tarsa/tarsalzp/Options.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __Options__ {

str *const_0;

using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long;

str *__author__, *__name__;



/**
class Options
*/

class_ *cl_Options;

void *Options::__init__(__ss_int lzpLowContextLength, __ss_int lzpLowMaskSize, __ss_int lzpHighContextLength, __ss_int lzpHighMaskSize, __ss_int literalCoderOrder, __ss_int literalCoderInit, __ss_int literalCoderStep, __ss_int literalCoderLimit) {
    this->lzpLowContextLength = lzpLowContextLength;
    this->lzpLowMaskSize = lzpLowMaskSize;
    this->lzpHighContextLength = lzpHighContextLength;
    this->lzpHighMaskSize = lzpHighMaskSize;
    this->literalCoderOrder = literalCoderOrder;
    this->literalCoderInit = literalCoderInit;
    this->literalCoderStep = literalCoderStep;
    this->literalCoderLimit = literalCoderLimit;
    return NULL;
}

__ss_bool Options::isValid() {
    return ((((((((((((((((((((((((((((___bool((this->lzpLowContextLength>this->literalCoderOrder)))&(___bool((this->lzpLowContextLength<=this->lzpHighContextLength)))))&(___bool((this->lzpHighContextLength<=__ss_int(8))))))&(___bool((this->lzpLowMaskSize>=__ss_int(15))))))&(___bool((this->lzpLowMaskSize<=__ss_int(30))))))&(___bool((this->lzpHighMaskSize>=__ss_int(15))))))&(___bool((this->lzpHighMaskSize<=__ss_int(30))))))&(___bool((this->literalCoderOrder>=__ss_int(1))))))&(___bool((this->literalCoderOrder<=__ss_int(2))))))&(___bool((this->literalCoderInit>=__ss_int(1))))))&(___bool((this->literalCoderInit<=__ss_int(127))))))&(___bool((this->literalCoderStep>=__ss_int(1))))))&(___bool((this->literalCoderStep<=__ss_int(127))))))&(___bool((this->literalCoderLimit>=(this->literalCoderInit*__ss_int(256)))))))&(___bool((this->literalCoderLimit<=(__ss_int(32767)-this->literalCoderStep)))));
}

__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *Options::toPacked() {
    __ss_int a, b, c, d;

    a = ((this->lzpLowContextLength<<__ss_int(8))+this->lzpLowMaskSize);
    b = ((this->lzpHighContextLength<<__ss_int(8))+this->lzpHighMaskSize);
    c = ((((this->literalCoderOrder-__ss_int(1))<<__ss_int(15))+(this->literalCoderInit<<__ss_int(8)))+this->literalCoderStep);
    d = this->literalCoderLimit;
    return (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long(a, b, c, d));
}

Options *Options::fromPacked(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *packed) {
    __ss_int a, b, c, d;
    Options *options;

    a = packed->a;
    b = packed->b;
    c = packed->c;
    d = packed->d;
    options = (new Options((((a)&(__ss_int(65280)))>>__ss_int(8)), ((a)&(__ss_int(255))), (((b)&(__ss_int(65280)))>>__ss_int(8)), ((b)&(__ss_int(255))), ((((c)&(__ss_int(32768)))>>__ss_int(15))+__ss_int(1)), (((c)&(__ss_int(32512)))>>__ss_int(8)), ((c)&(__ss_int(255))), d));
    return ((options->isValid())?(options):(NULL));
}

Options *Options::getDefault() {
    __ss_int literalCoderInit, literalCoderLimit, literalCoderOrder, literalCoderStep, lzpHighContextLength, lzpHighMaskSize, lzpLowContextLength, lzpLowMaskSize;

    lzpLowContextLength = __ss_int(4);
    lzpLowMaskSize = __ss_int(24);
    lzpHighContextLength = __ss_int(8);
    lzpHighMaskSize = __ss_int(27);
    literalCoderOrder = __ss_int(2);
    literalCoderInit = __ss_int(1);
    literalCoderStep = __ss_int(60);
    literalCoderLimit = __ss_int(30000);
    return (new Options(lzpLowContextLength, lzpLowMaskSize, lzpHighContextLength, lzpHighMaskSize, literalCoderOrder, literalCoderInit, literalCoderStep, literalCoderLimit));
}


void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("Options");

    __author__ = const_0;
    cl_Options = new class_("Options");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

