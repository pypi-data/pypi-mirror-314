#ifndef __ML_TRIANGLE_HPP
#define __ML_TRIANGLE_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ {
namespace __triangle__ {

extern str *const_0;

class Triangle;

typedef void *(*lambda0)(void *, void *, void *, void *, void *);

extern str *__name__;
extern __re__::re_object *SEARCH;
extern __ss_float TOLERANCE;
extern __ml__::__vector3f__::Vector3f *MAX, *ONE, *ZERO;


extern class_ *cl_Triangle;
class Triangle : public pyobj {
public:
    __ml__::__vector3f__::Vector3f *emitivity;
    __ss_float area;
    list<__ml__::__vector3f__::Vector3f *> *vertexs;
    __ml__::__vector3f__::Vector3f *edge0;
    __ml__::__vector3f__::Vector3f *tangent;
    list<__ss_float> *bound;
    __ml__::__vector3f__::Vector3f *edge3;
    __ml__::__vector3f__::Vector3f *normal;
    __ml__::__vector3f__::Vector3f *reflectivity;

    Triangle() {}
    Triangle(file *in_stream) {
        this->__class__ = cl_Triangle;
        __init__(in_stream);
    }
    void *__init__(file *in_stream);
    list<__ss_float> *get_bound();
    __ss_float get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction);
    __ml__::__vector3f__::Vector3f *get_sample_point();
};

void __init();

} // module namespace
} // module namespace
#endif
