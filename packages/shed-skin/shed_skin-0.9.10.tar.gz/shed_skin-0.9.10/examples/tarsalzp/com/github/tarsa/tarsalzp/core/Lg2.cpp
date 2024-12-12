#include "builtin.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __Lg2__ {

str *const_0;


str *__author__, *__name__;



/**
class Lg2
*/

class_ *cl_Lg2;

__ss_int Lg2::iLog2(__ss_int value) {
    if (((___bool((value>=__ss_int(256))))&(___bool((value<__ss_int(65536)))))) {
        return (__ss_int(8)+(Lg2::lgLut)->__getfast__((value>>__ss_int(8))));
    }
    else if ((value<__ss_int(256))) {
        return (Lg2::lgLut)->__getfast__(value);
    }
    else {
        return (__ss_int(16)+Lg2::iLog2((value>>__ss_int(16))));
    }
    return 0;
}

__ss_int Lg2::nLog2(__ss_int value) {
    /**
    Approximate logarithm base 2 scaled by 2^14, Works only for positive
    * values lower than 2^15.
    */
    __ss_int ilog, norm;

    ilog = Lg2::iLog2(value);
    norm = (value<<(__ss_int(14)-ilog));
    return (((ilog-__ss_int(1))<<__ss_int(14))+norm);
}

list<__ss_int> *Lg2::lgLut;
__ss_int Lg2::i;
__ss_int Lg2::__4;
__ss_int Lg2::__5;

void Lg2::__static__() {
    lgLut = (new list<__ss_int>(1,(-__ss_int(1))));

    FAST_FOR(i,__ss_int(1),__ss_int(256),1,4,5)
        lgLut->append((__ss_int(1)+lgLut->__getfast__(__floordiv(i,__ss_int(2)))));
    END_FOR

}

void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("Lg2");

    __author__ = const_0;
    cl_Lg2 = new class_("Lg2");
    Lg2::__static__();
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

