#include "builtin.hpp"
#include "math.hpp"
#include "ml/vector3f.hpp"

namespace __ml__ {
namespace __vector3f__ {

str *const_0, *const_1;

using __math__::sqrt;

str *__name__;
Vector3f *MAX, *ONE, *ZERO;



Vector3f *Vector3f_str(str *s) {
    list<str *> *split;

    split = ((s->lstrip(const_0))->rstrip(const_1))->split();
    return (new Vector3f(__float(split->__getfast__(__ss_int(0))), __float(split->__getfast__(__ss_int(1))), __float(split->__getfast__(__ss_int(2)))));
}

Vector3f *Vector3f_seq(list<__ss_float> *seq) {
    return (new Vector3f(seq->__getfast__(__ss_int(0)), seq->__getfast__(__ss_int(1)), seq->__getfast__(__ss_int(2))));
}

Vector3f *Vector3f_scalar(__ss_float s) {
    return (new Vector3f(s, s, s));
}

/**
class Vector3f
*/

class_ *cl_Vector3f;

void *Vector3f::__init__(__ss_float x, __ss_float y, __ss_float z) {
    __ss_float __0, __1, __2;

    __0 = x;
    __1 = y;
    __2 = z;
    this->x = __0;
    this->y = __1;
    this->z = __2;
    return NULL;
}

list<__ss_float> *Vector3f::as_list() {
    return (new list<__ss_float>(3,this->x,this->y,this->z));
}

Vector3f *Vector3f::copy() {
    return (new Vector3f(this->x, this->y, this->z));
}

__ss_float Vector3f::__getitem__(__ss_int key) {
    if ((key==__ss_int(2))) {
        return this->z;
    }
    else if ((key==__ss_int(1))) {
        return this->y;
    }
    else {
        return this->x;
    }
    return 0;
}

Vector3f *Vector3f::__neg__() {
    return (new Vector3f((-this->x), (-this->y), (-this->z)));
}

Vector3f *Vector3f::__add__(Vector3f *other) {
    return (new Vector3f((this->x+other->x), (this->y+other->y), (this->z+other->z)));
}

Vector3f *Vector3f::__sub__(Vector3f *other) {
    return (new Vector3f((this->x-other->x), (this->y-other->y), (this->z-other->z)));
}

Vector3f *Vector3f::__mul__(__ss_float other) {
    return (new Vector3f((this->x*other), (this->y*other), (this->z*other)));
}

Vector3f *Vector3f::mul(Vector3f *other) {
    return (new Vector3f((this->x*other->x), (this->y*other->y), (this->z*other->z)));
}

__ss_bool Vector3f::is_zero() {
    __ss_bool __3, __4, __5;

    return __AND(___bool((this->x==__ss_float(0.0))), __AND(___bool((this->y==__ss_float(0.0))), ___bool((this->z==__ss_float(0.0))), 4), 3);
}

__ss_float Vector3f::dot(Vector3f *other) {
    return (((this->x*other->x)+(this->y*other->y))+(this->z*other->z));
}

Vector3f *Vector3f::unitize() {
    __ss_float length, one_over_length;

    length = sqrt((((this->x*this->x)+(this->y*this->y))+(this->z*this->z)));
    one_over_length = (((length!=__ss_float(0.0)))?((__ss_float(1.0)/length)):(__ss_float(0.0)));
    return (new Vector3f((this->x*one_over_length), (this->y*one_over_length), (this->z*one_over_length)));
}

Vector3f *Vector3f::cross(Vector3f *other) {
    return (new Vector3f(((this->y*other->z)-(this->z*other->y)), ((this->z*other->x)-(this->x*other->z)), ((this->x*other->y)-(this->y*other->x))));
}

Vector3f *Vector3f::clamped(Vector3f *lo, Vector3f *hi) {
    return (new Vector3f(___min(2, (__ss_float(__ss_int(0))), ___max(2, (__ss_float(__ss_int(0))), this->x, lo->x), hi->x), ___min(2, (__ss_float(__ss_int(0))), ___max(2, (__ss_float(__ss_int(0))), this->y, lo->y), hi->y), ___min(2, (__ss_float(__ss_int(0))), ___max(2, (__ss_float(__ss_int(0))), this->z, lo->z), hi->z)));
}

void __init() {
    const_0 = new str(" (");
    const_1 = new str(") ");

    __name__ = new str("vector3f");

    cl_Vector3f = new class_("Vector3f");
    ZERO = Vector3f_scalar(__ss_float(0.0));
    ONE = Vector3f_scalar(__ss_float(1.0));
    MAX = Vector3f_scalar(__ss_float(1.797e+308));
}

} // module namespace
} // module namespace

