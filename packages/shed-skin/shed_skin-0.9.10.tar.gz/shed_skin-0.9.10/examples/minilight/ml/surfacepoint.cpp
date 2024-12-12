#include "builtin.hpp"
#include "time.hpp"
#include "re.hpp"
#include "math.hpp"
#include "random.hpp"
#include "ml/triangle.hpp"
#include "ml/vector3f.hpp"
#include "ml/surfacepoint.hpp"

namespace __ml__ {
namespace __surfacepoint__ {

using __math__::cos;
using __math__::sin;
using __math__::sqrt;
using __random__::random;

str *__name__;
__ss_float pi;
__ml__::__vector3f__::Vector3f *ONE, *ZERO;



/**
class SurfacePoint
*/

class_ *cl_SurfacePoint;

void *SurfacePoint::__init__(__ml__::__triangle__::Triangle *triangle, __ml__::__vector3f__::Vector3f *position) {
    this->triangle_ref = triangle;
    this->position = position->copy();
    return NULL;
}

__ml__::__vector3f__::Vector3f *SurfacePoint::get_emission(__ml__::__vector3f__::Vector3f *to_position, __ml__::__vector3f__::Vector3f *out_direction, __ss_bool is_solid_angle) {
    __ml__::__vector3f__::Vector3f *ray;
    __ss_float cos_area, distance2, solid_angle;
    __ss_bool __6, __7;

    ray = (to_position)->__sub__(this->position);
    distance2 = ray->dot(ray);
    cos_area = (out_direction->dot((this->triangle_ref)->normal)*(this->triangle_ref)->area);
    ASSERT(__AND(True, True, 6), 0);
    solid_angle = ((is_solid_angle)?((cos_area/___max(2, (__ss_float(__ss_int(0))), distance2, __ss_float(1e-06)))):(__ss_float(1.0)));
    return (((cos_area>__ss_float(0.0)))?(((this->triangle_ref)->emitivity)->__mul__(solid_angle)):(__ml__::__surfacepoint__::ZERO));
}

__ml__::__vector3f__::Vector3f *SurfacePoint::get_reflection(__ml__::__vector3f__::Vector3f *in_direction, __ml__::__vector3f__::Vector3f *in_radiance, __ml__::__vector3f__::Vector3f *out_direction) {
    __ss_float in_dot, out_dot;

    in_dot = in_direction->dot((this->triangle_ref)->normal);
    out_dot = out_direction->dot((this->triangle_ref)->normal);
    return ((((___bool((in_dot<__ss_float(0.0))))^(___bool((out_dot<__ss_float(0.0))))))?(__ml__::__surfacepoint__::ZERO):((in_radiance->mul((this->triangle_ref)->reflectivity))->__mul__((__abs(in_dot)/__ml__::__surfacepoint__::pi))));
}

tuple<__ml__::__vector3f__::Vector3f *> *SurfacePoint::get_next_direction(__ml__::__vector3f__::Vector3f *in_direction) {
    __ss_float _2pr1, reflectivity_mean, sr2, x, y, z;
    __ml__::__vector3f__::Vector3f *color, *normal, *out_direction, *tangent;

    reflectivity_mean = (((this->triangle_ref)->reflectivity)->dot(__ml__::__surfacepoint__::ONE)/__ss_float(3.0));
    if ((random()<reflectivity_mean)) {
        color = ((this->triangle_ref)->reflectivity)->__mul__((__ss_float(1.0)/reflectivity_mean));
        _2pr1 = ((__ml__::__surfacepoint__::pi*__ss_float(2.0))*random());
        sr2 = sqrt(random());
        x = (cos(_2pr1)*sr2);
        y = (sin(_2pr1)*sr2);
        z = sqrt((__ss_float(1.0)-(sr2*sr2)));
        normal = (this->triangle_ref)->normal;
        tangent = (this->triangle_ref)->tangent;
        if ((normal->dot(in_direction)<__ss_float(0.0))) {
            normal = (normal->__neg__());
        }
        out_direction = (((tangent)->__mul__(x))->__add__((normal->cross(tangent))->__mul__(y)))->__add__((normal)->__mul__(z));
        return (new tuple<__ml__::__vector3f__::Vector3f *>(2,out_direction,color));
    }
    else {
        return (new tuple<__ml__::__vector3f__::Vector3f *>(2,__ml__::__surfacepoint__::ZERO,__ml__::__surfacepoint__::ZERO));
    }
    return 0;
}

void __init() {
    __name__ = new str("surfacepoint");

    pi = __math__::pi;
    ONE = __ml__::__vector3f__::ONE;
    ZERO = __ml__::__vector3f__::ZERO;
    cl_SurfacePoint = new class_("SurfacePoint");
}

} // module namespace
} // module namespace

