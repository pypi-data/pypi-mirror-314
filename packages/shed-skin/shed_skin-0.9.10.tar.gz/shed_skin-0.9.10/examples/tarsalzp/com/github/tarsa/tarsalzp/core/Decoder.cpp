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
namespace __Decoder__ {

str *const_0, *const_1;

using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::Common;

str *__author__, *__name__;



/**
class Decoder
*/

class_ *cl_Decoder;

void *Decoder::__init__(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::Common::__init__(inputStream, outputStream, options);
    this->started = False;
    this->nextHighBit = __ss_int(0);
    this->rcBuffer = __ss_int(0);
    this->rcRange = __ss_int(0);
    return NULL;
}

__ss_int Decoder::inputByte() {
    __ss_int currentByte, inputByte;

    inputByte = (this->inputStream)->readByte();
    if ((inputByte==(-__ss_int(1)))) {
        throw ((new OSError(const_0)));
    }
    currentByte = ((inputByte>>__ss_int(1))+(this->nextHighBit<<__ss_int(7)));
    this->nextHighBit = ((inputByte)&(__ss_int(1)));
    return currentByte;
}

void *Decoder::init() {
    __ss_int __56, __57, i;

    this->rcBuffer = __ss_int(0);

    FAST_FOR(i,0,__ss_int(4),1,56,57)
        this->rcBuffer = ((this->rcBuffer<<__ss_int(8))+this->inputByte());
    END_FOR

    this->rcRange = __ss_int(2147483647);
    this->started = True;
    return NULL;
}

void *Decoder::normalize() {

    while ((this->rcRange<__ss_int(8388608))) {
        this->rcBuffer = ((this->rcBuffer<<__ss_int(8))+this->inputByte());
        this->rcRange = (this->rcRange<<__ss_int(8));
    }
    return NULL;
}

__ss_bool Decoder::decodeFlag(__ss_int probability) {
    __ss_int rcHelper;

    this->normalize();
    rcHelper = ((this->rcRange>>__ss_int(15))*probability);
    if ((rcHelper>this->rcBuffer)) {
        this->rcRange = rcHelper;
        return True;
    }
    else {
        this->rcRange = (this->rcRange-rcHelper);
        this->rcBuffer = (this->rcBuffer-rcHelper);
        return False;
    }
    return False;
}

__ss_bool Decoder::decodeSkewed() {
    this->normalize();
    if ((this->rcBuffer<(this->rcRange-__ss_int(1)))) {
        this->rcRange = (this->rcRange-__ss_int(1));
        return True;
    }
    else {
        this->rcBuffer = __ss_int(0);
        this->rcRange = __ss_int(1);
        return False;
    }
    return False;
}

__ss_int Decoder::decodeSingleOnlyLowLzp() {
    __ss_int lzpStateLow, modelLowFrequency, nextSymbol, predictedSymbolLow;
    __ss_bool matchLow;

    this->computeHashesOnlyLowLzp();
    lzpStateLow = this->getLzpStateLow();
    predictedSymbolLow = this->getLzpPredictedSymbolLow();
    modelLowFrequency = this->getApmLow(lzpStateLow);
    matchLow = this->decodeFlag(modelLowFrequency);
    this->updateApmLow(lzpStateLow, matchLow);
    nextSymbol = ((matchLow)?(predictedSymbolLow):(this->decodeSymbol(predictedSymbolLow)));
    this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
    this->updateContext(nextSymbol);
    return nextSymbol;
}

__ss_int Decoder::decodeSingle() {
    __ss_int lzpStateHigh, lzpStateLow, modelHighFrequency, modelLowFrequency, nextSymbol, predictedSymbolHigh, predictedSymbolLow;
    __ss_bool matchHigh, matchLow;

    this->computeHashes();
    lzpStateLow = this->getLzpStateLow();
    predictedSymbolLow = this->getLzpPredictedSymbolLow();
    modelLowFrequency = this->getApmLow(lzpStateLow);
    lzpStateHigh = this->getLzpStateHigh();
    predictedSymbolHigh = this->getLzpPredictedSymbolHigh();
    modelHighFrequency = this->getApmHigh(lzpStateHigh);
    if ((modelLowFrequency>=modelHighFrequency)) {
        matchLow = this->decodeFlag(modelLowFrequency);
        this->updateApmLow(lzpStateLow, matchLow);
        nextSymbol = ((matchLow)?(predictedSymbolLow):(this->decodeSymbol(predictedSymbolLow)));
        this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
        matchHigh = ___bool((nextSymbol==predictedSymbolHigh));
        this->updateApmHistoryHigh(matchHigh);
        this->updateLzpStateHigh(lzpStateHigh, nextSymbol, matchHigh);
    }
    else {
        matchHigh = this->decodeFlag(modelHighFrequency);
        this->updateApmHigh(lzpStateHigh, matchHigh);
        nextSymbol = ((matchHigh)?(predictedSymbolHigh):(this->decodeSymbol(predictedSymbolHigh)));
        this->updateLzpStateHigh(lzpStateHigh, nextSymbol, matchHigh);
        matchLow = ___bool((nextSymbol==predictedSymbolLow));
        this->updateApmHistoryLow(matchLow);
        this->updateLzpStateLow(lzpStateLow, nextSymbol, matchLow);
    }
    this->updateContext(nextSymbol);
    return nextSymbol;
}

__ss_int Decoder::decodeSymbol(__ss_int mispredictedSymbol) {
    __ss_int __60, __63, cumulativeFrequency, index, mispredictedSymbolFrequency, nextSymbol, rcHelper;
    __array__::array<__ss_int> *__58, *__59, *__61, *__62;

    this->normalize();
    this->computeLiteralCoderContext();
    if (__NOT(this->useFixedProbabilities())) {
        mispredictedSymbolFrequency = (this->rangesSingle)->__getfast__(((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol));
        this->rcRange = __floordiv(this->rcRange,((this->rangesTotal)->__getfast__(this->lastLiteralCoderContext)-mispredictedSymbolFrequency));
        this->rangesSingle->__setitem__(((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol), __ss_int(0));
        __59 = this->rangesGrouped;
        __60 = (((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol)>>__ss_int(4));
        __59->__setitem__(__60, (__59->__getfast__(__60)-mispredictedSymbolFrequency));
        rcHelper = __floordiv(this->rcBuffer,this->rcRange);
        cumulativeFrequency = rcHelper;
        index = (this->lastLiteralCoderContext<<__ss_int(4));

        while ((rcHelper>=(this->rangesGrouped)->__getfast__(index))) {
            rcHelper = (rcHelper-(this->rangesGrouped)->__getfast__(index));
            index = (index+__ss_int(1));
        }
        index = (index<<__ss_int(4));

        while ((rcHelper>=(this->rangesSingle)->__getfast__(index))) {
            rcHelper = (rcHelper-(this->rangesSingle)->__getfast__(index));
            index = (index+__ss_int(1));
        }
        this->rcBuffer = (this->rcBuffer-((cumulativeFrequency-rcHelper)*this->rcRange));
        this->rcRange = (this->rcRange*(this->rangesSingle)->__getfast__(index));
        nextSymbol = ((index)&(__ss_int(255)));
        this->rangesSingle->__setitem__(((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol), mispredictedSymbolFrequency);
        __62 = this->rangesGrouped;
        __63 = (((this->lastLiteralCoderContext<<__ss_int(8))+mispredictedSymbol)>>__ss_int(4));
        __62->__setitem__(__63, (__62->__getfast__(__63)+mispredictedSymbolFrequency));
    }
    else {
        this->rcRange = __floordiv(this->rcRange,__ss_int(255));
        rcHelper = __floordiv(this->rcBuffer,this->rcRange);
        this->rcBuffer = (this->rcBuffer-(rcHelper*this->rcRange));
        nextSymbol = (rcHelper+(((rcHelper>=mispredictedSymbol))?(__ss_int(1)):(__ss_int(0))));
        index = ((this->lastLiteralCoderContext<<__ss_int(8))+nextSymbol);
    }
    this->updateRecentCost((this->rangesSingle)->__getfast__(index), (this->rangesTotal)->__getfast__(this->lastLiteralCoderContext));
    this->updateLiteralCoder(index);
    return nextSymbol;
}

__ss_bool Decoder::decode(__ss_int limit) {
    __ss_bool endReached;
    __ss_int __64, __65, i, symbol;

    if (__NOT(this->started)) {
        this->init();
    }
    endReached = False;

    FAST_FOR(i,0,limit,1,64,65)
        endReached = __NOT(this->decodeSkewed());
        if (__NOT(endReached)) {
            symbol = ((this->onlyLowLzp)?(this->decodeSingleOnlyLowLzp()):(this->decodeSingle()));
            (this->outputStream)->writeByte(symbol);
        }
        else {
            break;
        }
    END_FOR

    return endReached;
}

void __init() {
    const_0 = new str("Unexpected end of file.");
    const_1 = new str("Piotr Tarsa");

    __name__ = new str("Decoder");

    __author__ = const_1;
    cl_Decoder = new class_("Decoder");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

