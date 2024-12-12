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
namespace __Encoder__ {

str *const_0;

using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::Common;

str *__author__, *__name__;



/**
class Encoder
*/

class_ *cl_Encoder;

void *Encoder::__init__(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::Common::__init__(inputStream, outputStream, options);
    this->rcBuffer = __ss_int(0);
    this->rcRange = __ss_int(2147483647);
    this->xFFRunLength = __ss_int(0);
    this->lastOutputByte = __ss_int(0);
    this->delay = False;
    this->carry = False;
    return NULL;
}

void *Encoder::outputByte(__ss_int octet) {
    __ss_bool __111, __112;

    if (((octet!=__ss_int(255)) or this->carry)) {
        if (this->delay) {
            (this->outputStream)->writeByte((this->lastOutputByte+((this->carry)?(__ss_int(1)):(__ss_int(0)))));
        }

        while ((this->xFFRunLength>__ss_int(0))) {
            this->xFFRunLength = (this->xFFRunLength-__ss_int(1));
            (this->outputStream)->writeByte(((this->carry)?(__ss_int(0)):(__ss_int(255))));
        }
        this->lastOutputByte = octet;
        this->delay = True;
        this->carry = False;
    }
    else {
        this->xFFRunLength = (this->xFFRunLength+__ss_int(1));
    }
    return NULL;
}

void *Encoder::normalize() {

    while ((this->rcRange<__ss_int(8388608))) {
        this->outputByte((this->rcBuffer>>__ss_int(23)));
        this->rcBuffer = (((this->rcBuffer)&(__ss_int(8388607)))<<__ss_int(8));
        this->rcRange = (this->rcRange<<__ss_int(8));
    }
    return NULL;
}

void *Encoder::addWithCarry(__ss_int value) {
    __ss_int maskedBuffer;

    this->rcBuffer = (this->rcBuffer+value);
    maskedBuffer = ((this->rcBuffer)&(__ss_int(2147483647)));
    if ((this->rcBuffer!=maskedBuffer)) {
        this->carry = True;
    }
    this->rcBuffer = maskedBuffer;
    return NULL;
}

void *Encoder::encodeFlag(__ss_int probability, __ss_bool match) {
    __ss_int rcHelper;

    this->normalize();
    rcHelper = ((this->rcRange>>__ss_int(15))*probability);
    if (match) {
        this->rcRange = rcHelper;
    }
    else {
        this->addWithCarry(rcHelper);
        this->rcRange = (this->rcRange-rcHelper);
    }
    return NULL;
}

void *Encoder::encodeSkewed(__ss_bool flag) {
    this->normalize();
    if (flag) {
        this->rcRange = (this->rcRange-__ss_int(1));
    }
    else {
        this->addWithCarry((this->rcRange-__ss_int(1)));
        this->rcRange = __ss_int(1);
    }
    return NULL;
}

void *Encoder::encodeSingleOnlyLowLzp(__ss_int nextSymbol) {
    __ss_int lzpStateLow, modelLowFrequency, predictedSymbolLow;
    __ss_bool matchLow;

    this->computeHashesOnlyLowLzp();
    lzpStateLow = this->getLzpStateLow();
    predictedSymbolLow = this->getLzpPredictedSymbolLow();
    modelLowFrequency = this->getApmLow(lzpStateLow);
    matchLow = ___bool((nextSymbol==predictedSymbolLow));
    this->encodeFlag(modelLowFrequency, matchLow);
    this->updateApmLow(lzpStateLow, matchLow);
    this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
    if (__NOT(matchLow)) {
        this->encodeSymbol(nextSymbol, predictedSymbolLow);
    }
    this->updateContext(nextSymbol);
    return NULL;
}

void *Encoder::encodeSingle(__ss_int nextSymbol) {
    __ss_int lzpStateHigh, lzpStateLow, modelHighFrequency, modelLowFrequency, predictedSymbolHigh, predictedSymbolLow;
    __ss_bool matchHigh, matchLow;

    this->computeHashes();
    lzpStateLow = this->getLzpStateLow();
    predictedSymbolLow = this->getLzpPredictedSymbolLow();
    modelLowFrequency = this->getApmLow(lzpStateLow);
    lzpStateHigh = this->getLzpStateHigh();
    predictedSymbolHigh = this->getLzpPredictedSymbolHigh();
    modelHighFrequency = this->getApmHigh(lzpStateHigh);
    if ((modelLowFrequency>=modelHighFrequency)) {
        matchHigh = ___bool((nextSymbol==predictedSymbolHigh));
        this->updateApmHistoryHigh(matchHigh);
        this->updateLzpStateHigh(lzpStateHigh, nextSymbol, matchHigh);
        matchLow = ___bool((nextSymbol==predictedSymbolLow));
        this->encodeFlag(modelLowFrequency, matchLow);
        this->updateApmLow(lzpStateLow, matchLow);
        this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
        if (__NOT(matchLow)) {
            this->encodeSymbol(nextSymbol, predictedSymbolLow);
        }
    }
    else {
        matchLow = ___bool((nextSymbol==predictedSymbolLow));
        this->updateApmHistoryLow(matchLow);
        this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
        matchHigh = ___bool((nextSymbol==predictedSymbolHigh));
        this->encodeFlag(modelHighFrequency, matchHigh);
        this->updateApmHigh(lzpStateHigh, matchHigh);
        this->updateLzpStateHigh(lzpStateHigh, nextSymbol, matchHigh);
        if (__NOT(matchHigh)) {
            this->encodeSymbol(nextSymbol, predictedSymbolHigh);
        }
    }
    this->updateContext(nextSymbol);
    return NULL;
}

void *Encoder::encodeSymbol(__ss_int nextSymbol, __ss_int mispredictedSymbol) {
    __ss_int __113, __114, __115, __116, cumulativeExclusiveFrequency, index, indexPartial, mispredictedSymbolFrequency, rcHelper, symbolGroup;

    this->normalize();
    this->computeLiteralCoderContext();
    index = ((this->lastLiteralCoderContext<<__ss_int(8))+nextSymbol);
    if (__NOT(this->useFixedProbabilities())) {
        cumulativeExclusiveFrequency = __ss_int(0);
        symbolGroup = (index>>__ss_int(4));

        FAST_FOR(indexPartial,(this->lastLiteralCoderContext<<__ss_int(4)),symbolGroup,1,113,114)
            cumulativeExclusiveFrequency = (cumulativeExclusiveFrequency+(this->rangesGrouped)->__getfast__(indexPartial));
        END_FOR


        FAST_FOR(indexPartial,(symbolGroup<<__ss_int(4)),index,1,115,116)
            cumulativeExclusiveFrequency = (cumulativeExclusiveFrequency+(this->rangesSingle)->__getfast__(indexPartial));
        END_FOR

        mispredictedSymbolFrequency = (this->rangesSingle)->__getfast__(((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol));
        if ((nextSymbol>mispredictedSymbol)) {
            cumulativeExclusiveFrequency = (cumulativeExclusiveFrequency-mispredictedSymbolFrequency);
        }
        rcHelper = __floordiv(this->rcRange,((this->rangesTotal)->__getfast__(this->lastLiteralCoderContext)-mispredictedSymbolFrequency));
        this->addWithCarry((rcHelper*cumulativeExclusiveFrequency));
        this->rcRange = (rcHelper*(this->rangesSingle)->__getfast__(index));
    }
    else {
        this->rcRange = __floordiv(this->rcRange,__ss_int(255));
        this->addWithCarry((this->rcRange*(nextSymbol-(((nextSymbol>mispredictedSymbol))?(__ss_int(1)):(__ss_int(0))))));
    }
    this->updateRecentCost((this->rangesSingle)->__getfast__(index), (this->rangesTotal)->__getfast__(this->lastLiteralCoderContext));
    this->updateLiteralCoder(index);
    return NULL;
}

void *Encoder::flush() {
    __ss_int __117, __118, i;

    this->encodeSkewed(False);

    FAST_FOR(i,0,__ss_int(5),1,117,118)
        this->outputByte((((this->rcBuffer>>__ss_int(23)))&(__ss_int(255))));
        this->rcBuffer = (((this->rcBuffer)&(__ss_int(8388607)))<<__ss_int(8));
    END_FOR

    return NULL;
}

__ss_bool Encoder::encode(__ss_int limit) {
    __ss_bool endReached;
    __ss_int __119, __120, i, symbol;

    endReached = False;

    FAST_FOR(i,0,limit,1,119,120)
        symbol = (this->inputStream)->readByte();
        if ((symbol==(-__ss_int(1)))) {
            endReached = True;
            break;
        }
        this->encodeSkewed(True);
        if (this->onlyLowLzp) {
            this->encodeSingleOnlyLowLzp(symbol);
        }
        else {
            this->encodeSingle(symbol);
        }
    END_FOR

    return endReached;
}

void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("Encoder");

    __author__ = const_0;
    cl_Encoder = new class_("Encoder");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

