#ifndef __ML_SURFACEPOINT_HPP
#define __ML_SURFACEPOINT_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __triangle__ { /* XXX */
class Triangle;
}
}
namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ {
namespace __surfacepoint__ {

class SurfacePoint;

typedef __ss_float (*lambda0)(void *, void *, void *, void *, void *);
typedef __ss_float (*lambda1)(void *, void *, void *, void *, void *);

extern str *__name__;
extern __ss_float pi;
extern __ml__::__vector3f__::Vector3f *ONE, *ZERO;


extern class_ *cl_SurfacePoint;
class SurfacePoint : public pyobj {
public:
    __ml__::__vector3f__::Vector3f *position;
    __ml__::__triangle__::Triangle *triangle_ref;

    SurfacePoint() {}
    SurfacePoint(__ml__::__triangle__::Triangle *triangle, __ml__::__vector3f__::Vector3f *position) {
        this->__class__ = cl_SurfacePoint;
        __init__(triangle, position);
    }
    void *__init__(__ml__::__triangle__::Triangle *triangle, __ml__::__vector3f__::Vector3f *position);
    __ml__::__vector3f__::Vector3f *get_emission(__ml__::__vector3f__::Vector3f *to_position, __ml__::__vector3f__::Vector3f *out_direction, __ss_bool is_solid_angle);
    __ml__::__vector3f__::Vector3f *get_reflection(__ml__::__vector3f__::Vector3f *in_direction, __ml__::__vector3f__::Vector3f *in_radiance, __ml__::__vector3f__::Vector3f *out_direction);
    tuple<__ml__::__vector3f__::Vector3f *> *get_next_direction(__ml__::__vector3f__::Vector3f *in_direction);
};

void __init();

} // module namespace
} // module namespace
#endif
