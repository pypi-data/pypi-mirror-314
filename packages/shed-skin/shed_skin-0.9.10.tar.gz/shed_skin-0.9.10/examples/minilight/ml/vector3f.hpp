#ifndef __ML_VECTOR3F_HPP
#define __ML_VECTOR3F_HPP

using namespace __shedskin__;
namespace __ml__ {
namespace __vector3f__ {

extern str *const_0, *const_1;

class Vector3f;


extern str *__name__;
extern Vector3f *MAX, *ONE, *ZERO;


extern class_ *cl_Vector3f;
class Vector3f : public pyobj {
public:
    __ss_float x;
    __ss_float z;
    __ss_float y;

    Vector3f() {}
    Vector3f(__ss_float x, __ss_float y, __ss_float z) {
        this->__class__ = cl_Vector3f;
        __init__(x, y, z);
    }
    void *__init__(__ss_float x, __ss_float y, __ss_float z);
    list<__ss_float> *as_list();
    Vector3f *copy();
    __ss_float __getitem__(__ss_int key);
    Vector3f *__neg__();
    Vector3f *__add__(Vector3f *other);
    Vector3f *__sub__(Vector3f *other);
    Vector3f *__mul__(__ss_float other);
    Vector3f *mul(Vector3f *other);
    __ss_bool is_zero();
    __ss_float dot(Vector3f *other);
    Vector3f *unitize();
    Vector3f *cross(Vector3f *other);
    Vector3f *clamped(Vector3f *lo, Vector3f *hi);
};

void __init();
Vector3f *Vector3f_str(str *s);
Vector3f *Vector3f_seq(list<__ss_float> *seq);
Vector3f *Vector3f_scalar(__ss_float s);

} // module namespace
} // module namespace
#endif
