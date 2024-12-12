#include "builtin.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/prelude/__init__.hpp"
#include "com/github/tarsa/tarsalzp/Options.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Streams.hpp"
#include "com/github/tarsa/tarsalzp/core/Common.hpp"
#include "com/github/tarsa/tarsalzp/core/Decoder.hpp"
#include "com/github/tarsa/tarsalzp/core/Encoder.hpp"
#include "com/github/tarsa/tarsalzp/core/FsmGenerator.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __Common__ {

str *const_0, *const_1, *const_2, *const_3;

using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__FsmGenerator__::FsmGenerator;
using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Lg2__::Lg2;

str *__author__, *__name__;


class list_comp_0 : public __iter<__ss_int> {
public:
    __ss_int _, __11, __12;

    __ss_int lzpLowCount;
    int __last_yield;

    list_comp_0(__ss_int lzpLowCount);
    __ss_int __get_next();
};

class list_comp_1 : public __iter<__ss_int> {
public:
    __ss_int _, __13, __14;

    __ss_int lzpHighCount;
    int __last_yield;

    list_comp_1(__ss_int lzpHighCount);
    __ss_int __get_next();
};

class list_comp_2 : public __iter<__ss_int> {
public:
    __ss_int _, __15, __16;

    __ss_int literalCoderContextMaskSize;
    Common *self;
    int __last_yield;

    list_comp_2(__ss_int literalCoderContextMaskSize, Common *self);
    __ss_int __get_next();
};

class list_comp_3 : public __iter<__ss_int> {
public:
    __ss_int _, __17, __18;

    __ss_int literalCoderContextMaskSize;
    Common *self;
    int __last_yield;

    list_comp_3(__ss_int literalCoderContextMaskSize, Common *self);
    __ss_int __get_next();
};

class list_comp_4 : public __iter<__ss_int> {
public:
    __ss_int _, __19, __20;

    __ss_int literalCoderContextMaskSize;
    Common *self;
    int __last_yield;

    list_comp_4(__ss_int literalCoderContextMaskSize, Common *self);
    __ss_int __get_next();
};

class list_comp_5 : public __iter<__ss_int> {
public:
    __ss_int _, __21, __22;

    int __last_yield;

    list_comp_5();
    __ss_int __get_next();
};

class list_comp_6 : public __iter<__ss_int> {
public:
    __ss_int _, __23, __24;

    int __last_yield;

    list_comp_6();
    __ss_int __get_next();
};

class list_comp_7 : public __iter<__ss_int> {
public:
    __ss_int _, __25, __26;

    int __last_yield;

    list_comp_7();
    __ss_int __get_next();
};

class list_comp_8 : public __iter<__ss_int> {
public:
    __ss_int __27, __28, i;

    int __last_yield;

    list_comp_8();
    __ss_int __get_next();
};


list_comp_0::list_comp_0(__ss_int lzpLowCount) {
    this->lzpLowCount = lzpLowCount;
    __last_yield = -1;
}

__ss_int list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,lzpLowCount,1,11,12)
        __result = __ss_int(65461);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_1::list_comp_1(__ss_int lzpHighCount) {
    this->lzpHighCount = lzpHighCount;
    __last_yield = -1;
}

__ss_int list_comp_1::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,lzpHighCount,1,13,14)
        __result = __ss_int(65461);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_2::list_comp_2(__ss_int literalCoderContextMaskSize, Common *self) {
    this->literalCoderContextMaskSize = literalCoderContextMaskSize;
    this->self = self;
    __last_yield = -1;
}

__ss_int list_comp_2::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,(__ss_int(1)<<(literalCoderContextMaskSize+__ss_int(8))),1,15,16)
        __result = self->literalCoderInit;
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_3::list_comp_3(__ss_int literalCoderContextMaskSize, Common *self) {
    this->literalCoderContextMaskSize = literalCoderContextMaskSize;
    this->self = self;
    __last_yield = -1;
}

__ss_int list_comp_3::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,(__ss_int(1)<<(literalCoderContextMaskSize+__ss_int(4))),1,17,18)
        __result = (self->literalCoderInit*__ss_int(16));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_4::list_comp_4(__ss_int literalCoderContextMaskSize, Common *self) {
    this->literalCoderContextMaskSize = literalCoderContextMaskSize;
    this->self = self;
    __last_yield = -1;
}

__ss_int list_comp_4::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,(__ss_int(1)<<literalCoderContextMaskSize),1,19,20)
        __result = (self->literalCoderInit*__ss_int(256));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_5::list_comp_5() {
    __last_yield = -1;
}

__ss_int list_comp_5::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,(__ss_int(16)*__ss_int(256)),1,21,22)
        __result = __ss_int(16384);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_6::list_comp_6() {
    __last_yield = -1;
}

__ss_int list_comp_6::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,(__ss_int(16)*__ss_int(256)),1,23,24)
        __result = __ss_int(16384);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_7::list_comp_7() {
    __last_yield = -1;
}

__ss_int list_comp_7::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,__ss_int(8),1,25,26)
        __result = __ss_int(0);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_8::list_comp_8() {
    __last_yield = -1;
}

__ss_int list_comp_8::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(i,0,__ss_int(256),1,27,28)
        __result = ((((((__ss_int(2166136261)*__ss_int(16777619)))^(i))*__ss_int(16777619)))&(__ss_int(2147483647)));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

/**
class Common
*/

class_ *cl_Common;

void *Common::__init__(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
    __ss_int literalCoderContextMaskSize, lzpHighCount, lzpLowCount;
    void *_, *i;

    this->inputStream = inputStream;
    this->outputStream = outputStream;
    this->lzpLowContextLength = options->lzpLowContextLength;
    this->lzpLowMaskSize = options->lzpLowMaskSize;
    this->lzpHighContextLength = options->lzpHighContextLength;
    this->lzpHighMaskSize = options->lzpHighMaskSize;
    this->literalCoderOrder = options->literalCoderOrder;
    this->literalCoderInit = options->literalCoderInit;
    this->literalCoderStep = options->literalCoderStep;
    this->literalCoderLimit = options->literalCoderLimit;
    lzpLowCount = (__ss_int(1)<<this->lzpLowMaskSize);
    lzpHighCount = (__ss_int(1)<<this->lzpHighMaskSize);
    this->lzpLowMask = (lzpLowCount-__ss_int(1));
    this->lzpHighMask = (lzpHighCount-__ss_int(1));
    this->lzpLow = (new __array__::array<__ss_int>(const_0, new list_comp_0(lzpLowCount)));
    this->onlyLowLzp = ((___bool((this->lzpLowContextLength==this->lzpHighContextLength)))&(___bool((this->lzpLowMaskSize==this->lzpHighMaskSize))));
    if (this->onlyLowLzp) {
        this->lzpHigh = NULL;
    }
    else {
        this->lzpHigh = (new __array__::array<__ss_int>(const_0, new list_comp_1(lzpHighCount)));
    }
    literalCoderContextMaskSize = (__ss_int(8)*this->literalCoderOrder);
    this->rangesSingle = (new __array__::array<__ss_int>(const_0, new list_comp_2(literalCoderContextMaskSize, this)));
    this->rangesGrouped = (new __array__::array<__ss_int>(const_0, new list_comp_3(literalCoderContextMaskSize, this)));
    this->rangesTotal = (new __array__::array<__ss_int>(const_0, new list_comp_4(literalCoderContextMaskSize, this)));
    this->recentCost = (__ss_int(8)<<(Common::CostScale+__ss_int(14)));
    this->apmLow = (new __array__::array<__ss_int>(const_0, new list_comp_5()));
    if (this->onlyLowLzp) {
        this->apmHigh = NULL;
    }
    else {
        this->apmHigh = (new __array__::array<__ss_int>(const_0, new list_comp_6()));
    }
    this->historyLow = __ss_int(0);
    this->historyHigh = __ss_int(0);
    this->historyLowMask = __ss_int(15);
    this->historyHighMask = __ss_int(15);
    this->lastLiteralCoderContext = __ss_int(0);
    this->context = (new __array__::array<__ss_int>(const_1, new list_comp_7()));
    this->contextIndex = __ss_int(0);
    this->hashLow = __ss_int(0);
    this->hashHigh = __ss_int(0);
    this->precomputedHashes = (new __array__::array<__ss_int>(const_2, new list_comp_8()));
    return NULL;
}

void *Common::updateContext(__ss_int input) {
    __array__::array<__ss_int> *__29;

    this->contextIndex = (((this->contextIndex-__ss_int(1)))&(__ss_int(7)));
    this->context->__setitem__(this->contextIndex, input);
    return NULL;
}

void *Common::computeLiteralCoderContext() {
    this->lastLiteralCoderContext = (this->context)->__getfast__(this->contextIndex);
    if ((this->literalCoderOrder==__ss_int(2))) {
        this->lastLiteralCoderContext = ((this->lastLiteralCoderContext<<__ss_int(8))+(this->context)->__getfast__((((this->contextIndex+__ss_int(1)))&(__ss_int(7)))));
    }
    return NULL;
}

void *Common::computeHashesOnlyLowLzp() {
    __ss_int hash, i, localIndex;

    localIndex = (((this->contextIndex+__ss_int(1)))&(__ss_int(7)));
    hash = (this->precomputedHashes)->__getfast__((this->context)->__getfast__(this->contextIndex));
    i = __ss_int(1);

    while (True) {
        hash = ((hash)^((this->context)->__getfast__(localIndex)));
        localIndex = (((localIndex+__ss_int(1)))&(__ss_int(7)));
        i = (i+__ss_int(1));
        if ((i==this->lzpLowContextLength)) {
            break;
        }
        hash = (hash*__ss_int(16777619));
        hash = ((hash)&(__ss_int(1073741823)));
    }
    this->hashLow = ((hash)&(this->lzpLowMask));
    return NULL;
}

void *Common::computeHashes() {
    __ss_int hash, i, localIndex;

    localIndex = (((this->contextIndex+__ss_int(1)))&(__ss_int(7)));
    hash = (this->precomputedHashes)->__getfast__((this->context)->__getfast__(this->contextIndex));
    i = __ss_int(1);

    while (True) {
        hash = ((hash)^((this->context)->__getfast__(localIndex)));
        localIndex = (((localIndex+__ss_int(1)))&(__ss_int(7)));
        i = (i+__ss_int(1));
        if ((i==this->lzpLowContextLength)) {
            break;
        }
        hash = (hash*__ss_int(16777619));
        hash = ((hash)&(__ss_int(1073741823)));
    }
    this->hashLow = ((hash)&(this->lzpLowMask));

    while ((i<this->lzpHighContextLength)) {
        i = (i+__ss_int(1));
        hash = (hash*__ss_int(16777619));
        hash = ((hash)&(__ss_int(1073741823)));
        hash = ((hash)^((this->context)->__getfast__(localIndex)));
        localIndex = (((localIndex+__ss_int(1)))&(__ss_int(7)));
    }
    this->hashHigh = ((hash)&(this->lzpHighMask));
    return NULL;
}

__ss_int Common::getNextState(__ss_int state, __ss_bool match) {
    return (Common::StateTable)->__getfast__(((state*__ss_int(2))+((match)?(__ss_int(1)):(__ss_int(0)))));
}

__ss_int Common::getLzpStateLow() {
    return ((((this->lzpLow)->__getfast__(this->hashLow))&(__ss_int(65280)))>>__ss_int(8));
}

__ss_int Common::getLzpStateHigh() {
    return ((((this->lzpHigh)->__getfast__(this->hashHigh))&(__ss_int(65280)))>>__ss_int(8));
}

__ss_int Common::getLzpPredictedSymbolLow() {
    return (((this->lzpLow)->__getfast__(this->hashLow))&(__ss_int(255)));
}

__ss_int Common::getLzpPredictedSymbolHigh() {
    return (((this->lzpHigh)->__getfast__(this->hashHigh))&(__ss_int(255)));
}

void *Common::updateLzpStateLow(__ss_int lzpStateLow, __ss_int input, __ss_bool match) {
    __array__::array<__ss_int> *__30;

    this->lzpLow->__setitem__(this->hashLow, ((this->getNextState(lzpStateLow, match)<<__ss_int(8))+input));
    return NULL;
}

void *Common::updateLzpStateHigh(__ss_int lzpStateHigh, __ss_int input, __ss_bool match) {
    __array__::array<__ss_int> *__31;

    this->lzpHigh->__setitem__(this->hashHigh, ((this->getNextState(lzpStateHigh, match)<<__ss_int(8))+input));
    return NULL;
}

__ss_int Common::getApmLow(__ss_int state) {
    return (this->apmLow)->__getfast__(((this->historyLow<<__ss_int(8))+state));
}

__ss_int Common::getApmHigh(__ss_int state) {
    return (this->apmHigh)->__getfast__(((this->historyHigh<<__ss_int(8))+state));
}

void *Common::updateApmHistoryLow(__ss_bool match) {
    this->historyLow = ((((this->historyLow<<__ss_int(1))+((match)?(__ss_int(0)):(__ss_int(1)))))&(this->historyLowMask));
    return NULL;
}

void *Common::updateApmHistoryHigh(__ss_bool match) {
    this->historyHigh = ((((this->historyHigh<<__ss_int(1))+((match)?(__ss_int(0)):(__ss_int(1)))))&(this->historyHighMask));
    return NULL;
}

void *Common::updateApmLow(__ss_int state, __ss_bool match) {
    __ss_int __33, __35, index;
    __array__::array<__ss_int> *__32, *__34;

    index = ((this->historyLow<<__ss_int(8))+state);
    if (match) {
        __32 = this->apmLow;
        __33 = index;
        __32->__setitem__(__33, (__32->__getfast__(__33)+(((__ss_int(1)<<__ss_int(15))-(this->apmLow)->__getfast__(index))>>__ss_int(7))));
    }
    else {
        __34 = this->apmLow;
        __35 = index;
        __34->__setitem__(__35, (__34->__getfast__(__35)-((this->apmLow)->__getfast__(index)>>__ss_int(7))));
    }
    this->updateApmHistoryLow(match);
    return NULL;
}

void *Common::updateApmHigh(__ss_int state, __ss_bool match) {
    __ss_int __37, __39, index;
    __array__::array<__ss_int> *__36, *__38;

    index = ((this->historyHigh<<__ss_int(8))+state);
    if (match) {
        __36 = this->apmHigh;
        __37 = index;
        __36->__setitem__(__37, (__36->__getfast__(__37)+(((__ss_int(1)<<__ss_int(15))-(this->apmHigh)->__getfast__(index))>>__ss_int(7))));
    }
    else {
        __38 = this->apmHigh;
        __39 = index;
        __38->__setitem__(__39, (__38->__getfast__(__39)-((this->apmHigh)->__getfast__(index)>>__ss_int(7))));
    }
    this->updateApmHistoryHigh(match);
    return NULL;
}

void *Common::rescaleLiteralCoder() {
    __ss_int __40, __41, __43, __44, __45, __46, __47, groupCurrent, groupFrequency, indexCurrent, totalFrequency;
    __array__::array<__ss_int> *__42, *__48, *__49;


    FAST_FOR(indexCurrent,(this->lastLiteralCoderContext<<__ss_int(8)),((this->lastLiteralCoderContext+__ss_int(1))<<__ss_int(8)),1,40,41)
        __42 = this->rangesSingle;
        __43 = indexCurrent;
        __42->__setitem__(__43, (__42->__getfast__(__43)-((this->rangesSingle)->__getfast__(indexCurrent)>>__ss_int(1))));
    END_FOR

    totalFrequency = __ss_int(0);

    FAST_FOR(groupCurrent,(this->lastLiteralCoderContext<<__ss_int(4)),((this->lastLiteralCoderContext+__ss_int(1))<<__ss_int(4)),1,44,45)
        groupFrequency = __ss_int(0);

        FAST_FOR(indexCurrent,(groupCurrent<<__ss_int(4)),((groupCurrent+__ss_int(1))<<__ss_int(4)),1,46,47)
            groupFrequency = (groupFrequency+(this->rangesSingle)->__getfast__(indexCurrent));
        END_FOR

        this->rangesGrouped->__setitem__(groupCurrent, groupFrequency);
        totalFrequency = (totalFrequency+groupFrequency);
    END_FOR

    this->rangesTotal->__setitem__(this->lastLiteralCoderContext, totalFrequency);
    return NULL;
}

void *Common::updateLiteralCoder(__ss_int index) {
    __array__::array<__ss_int> *__50, *__52, *__54;
    __ss_int __51, __53, __55;

    __50 = this->rangesSingle;
    __51 = index;
    __50->__setitem__(__51, (__50->__getfast__(__51)+this->literalCoderStep));
    __52 = this->rangesGrouped;
    __53 = (index>>__ss_int(4));
    __52->__setitem__(__53, (__52->__getfast__(__53)+this->literalCoderStep));
    __54 = this->rangesTotal;
    __55 = this->lastLiteralCoderContext;
    __54->__setitem__(__55, (__54->__getfast__(__55)+this->literalCoderStep));
    if (((this->rangesTotal)->__getfast__(this->lastLiteralCoderContext)>this->literalCoderLimit)) {
        this->rescaleLiteralCoder();
    }
    return NULL;
}

__ss_bool Common::useFixedProbabilities() {
    return ___bool((this->recentCost>(__ss_int(8)<<(Common::CostScale+__ss_int(14)))));
}

void *Common::updateRecentCost(__ss_int symbolFrequency, __ss_int totalFrequency) {
    this->recentCost = (this->recentCost-(this->recentCost>>Common::CostScale));
    this->recentCost = (this->recentCost+Lg2::nLog2(totalFrequency));
    this->recentCost = (this->recentCost-Lg2::nLog2(symbolFrequency));
    return NULL;
}

__ss_int Common::CostScale;
__array__::array<__ss_int> *Common::StateTable;

void Common::__static__() {
    CostScale = __ss_int(7);
    StateTable = ((new __com__::__github__::__tarsa__::__tarsalzp__::__core__::__FsmGenerator__::FsmGenerator(1)))->stateTable;
}

void __init() {
    const_0 = __char_cache[72];
    const_1 = __char_cache[66];
    const_2 = __char_cache[108];
    const_3 = new str("Piotr Tarsa");

    __name__ = new str("Common");

    __author__ = const_3;
    cl_Common = new class_("Common");
    Common::__static__();
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

