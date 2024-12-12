#include "builtin.hpp"
#include "time.hpp"
#include "math.hpp"
#include "re.hpp"
#include "random.hpp"
#include "ml/spatialindex.hpp"
#include "ml/surfacepoint.hpp"
#include "ml/triangle.hpp"
#include "ml/raytracer.hpp"
#include "ml/vector3f.hpp"
#include "ml/scene.hpp"

namespace __ml__ {
namespace __raytracer__ {

using __ml__::__surfacepoint__::SurfacePoint;

str *__name__;
__ml__::__vector3f__::Vector3f *ZERO;


__ml__::__triangle__::Triangle * default_0;

/**
class RayTracer
*/

class_ *cl_RayTracer;

void *RayTracer::__init__(__ml__::__scene__::Scene *scene) {
    this->scene_ref = scene;
    return NULL;
}

__ml__::__vector3f__::Vector3f *RayTracer::get_radiance(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit) {
    __ml__::__triangle__::Triangle *hit_ref;
    __ml__::__vector3f__::Vector3f *color, *hit_position, *illumination, *local_emission, *next_direction, *reflection;
    __ml__::__surfacepoint__::SurfacePoint *surface_point;
    tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *__8;
    tuple<__ml__::__vector3f__::Vector3f *> *__9;

    __8 = (this->scene_ref)->get_intersection(ray_origin, ray_direction, last_hit);
    __unpack_check(__8, 2);
    hit_ref = __8->__getfirst__();
    hit_position = __8->__getsecond__();
    if (___bool(hit_ref)) {
        surface_point = (new __ml__::__surfacepoint__::SurfacePoint(hit_ref, hit_position));
        local_emission = ((___bool(last_hit))?(__ml__::__raytracer__::ZERO):(surface_point->get_emission(ray_origin, (ray_direction->__neg__()), False)));
        illumination = this->sample_emitters(ray_direction, surface_point);
        __9 = surface_point->get_next_direction((ray_direction->__neg__()));
        __unpack_check(__9, 2);
        next_direction = __9->__getfirst__();
        color = __9->__getsecond__();
        reflection = ((next_direction->is_zero())?(__ml__::__raytracer__::ZERO):(color->mul(this->get_radiance(surface_point->position, next_direction, surface_point->triangle_ref))));
        return ((reflection)->__add__(illumination))->__add__(local_emission);
    }
    else {
        return (this->scene_ref)->get_default_emission((ray_direction->__neg__()));
    }
    return 0;
}

__ml__::__vector3f__::Vector3f *RayTracer::sample_emitters(__ml__::__vector3f__::Vector3f *ray_direction, __ml__::__surfacepoint__::SurfacePoint *surface_point) {
    __ml__::__vector3f__::Vector3f *emission_in, *emit_direction, *emitter_position, *p;
    __ml__::__triangle__::Triangle *emitter_ref, *hit_ref;
    tuple2<__ml__::__vector3f__::Vector3f *, __ml__::__triangle__::Triangle *> *__10;
    tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *__11;
    __ss_bool __12, __13;

    __10 = (this->scene_ref)->get_emitter();
    __unpack_check(__10, 2);
    emitter_position = __10->__getfirst__();
    emitter_ref = __10->__getsecond__();
    if (___bool(emitter_ref)) {
        emit_direction = ((emitter_position)->__sub__(surface_point->position))->unitize();
        __11 = (this->scene_ref)->get_intersection(surface_point->position, emit_direction, surface_point->triangle_ref);
        __unpack_check(__11, 2);
        hit_ref = __11->__getfirst__();
        p = __11->__getsecond__();
        emission_in = ((__OR(__NOT(___bool(hit_ref)), ___bool(__eq(emitter_ref, hit_ref)), 12))?(((new __ml__::__surfacepoint__::SurfacePoint(emitter_ref, emitter_position)))->get_emission(surface_point->position, (emit_direction->__neg__()), True)):(__ml__::__raytracer__::ZERO));
        return surface_point->get_reflection(emit_direction, (emission_in)->__mul__((this->scene_ref)->emitters_count()), (ray_direction->__neg__()));
    }
    else {
        return __ml__::__raytracer__::ZERO;
    }
    return 0;
}

void __init() {
    __name__ = new str("raytracer");

    ZERO = __ml__::__vector3f__::ZERO;
    default_0 = NULL;
    cl_RayTracer = new class_("RayTracer");
}

} // module namespace
} // module namespace

