#include "builtin.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/core/FsmGenerator.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __FsmGenerator__ {

str *const_0, *const_1;

using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Lg2__::Lg2;

str *__author__, *__name__;


class list_comp_0 : public __iter<__ss_int> {
public:
    __ss_int _, __6, __7;

    int __last_yield;

    list_comp_0();
    __ss_int __get_next();
};


list_comp_0::list_comp_0() {
    __last_yield = -1;
}

__ss_int list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(_,0,__ss_int(512),1,6,7)
        __result = __ss_int(0);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

/**
class FsmGenerator
*/

class_ *cl_FsmGenerator;

void *FsmGenerator::__init__() {
    void *_;

    this->stateTable = (new __array__::array<__ss_int>(const_0, new list_comp_0()));
    this->LimitX = __ss_int(20);
    this->LimitY = __ss_int(20);
    this->p = __ss_int(0);
    this->freqMask = ((new list<__ss_int>(1,(-__ss_int(1)))))->__mul__(((((this->LimitX+__ss_int(1))*(this->LimitY+__ss_int(1)))*__ss_int(3))*__ss_int(3)));
    this->initStates(__ss_int(0), __ss_int(0), __ss_int(2), __ss_int(2));
    return NULL;
}

__ss_int FsmGenerator::divisor(__ss_int a, __ss_int b) {
    return (((Lg2::nLog2(b)>>__ss_int(3))+(Lg2::nLog2(__ss_int(1950))>>__ss_int(3)))-(__ss_int(12)<<__ss_int(11)));
}

__ss_int FsmGenerator::repeated(__ss_int a, __ss_int b) {
    return ((((___bool((b>__ss_int(0))))&(___bool((this->divisor(a, b)>__ss_int(1200))))))?(__floordiv(((a+__ss_int(1))*__ss_int(1950)),this->divisor(a, b))):((a+__ss_int(1))));
}

__ss_int FsmGenerator::opposite(__ss_int a, __ss_int b) {
    return ((((___bool((b>__ss_int(0))))&(___bool((this->divisor(a, b)>__ss_int(1200))))))?(__floordiv((b*__ss_int(1950)),this->divisor(a, b))):(b));
}

__ss_int FsmGenerator::initStates(__ss_int x, __ss_int y, __ss_int h1, __ss_int h0) {
    __ss_int c, index;
    list<__ss_int> *__8;
    __array__::array<__ss_int> *__10, *__9;

    x = ___min(2, __ss_int(0), x, this->LimitX);
    y = ___min(2, __ss_int(0), y, this->LimitY);
    index = ((((((y*(this->LimitX+__ss_int(1)))+x)*__ss_int(3))+h1)*__ss_int(3))+h0);
    if (((this->freqMask)->__getfast__(index)==(-__ss_int(1)))) {
        this->freqMask->__setitem__(index, this->p);
        c = this->p;
        this->p = (this->p+__ss_int(1));
        this->stateTable->__setitem__(((c*__ss_int(2))+__ss_int(0)), this->initStates(this->repeated(x, y), this->opposite(x, y), h0, __ss_int(0)));
        this->stateTable->__setitem__(((c*__ss_int(2))+__ss_int(1)), this->initStates(this->opposite(y, x), this->repeated(y, x), h0, __ss_int(1)));
    }
    return (this->freqMask)->__getfast__(index);
}

void __init() {
    const_0 = __char_cache[66];
    const_1 = new str("Piotr Tarsa");

    __name__ = new str("FsmGenerator");

    __author__ = const_1;
    cl_FsmGenerator = new class_("FsmGenerator");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

