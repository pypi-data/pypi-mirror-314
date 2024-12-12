#ifndef __ML_RAYTRACER_HPP
#define __ML_RAYTRACER_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __surfacepoint__ { /* XXX */
class SurfacePoint;
}
}
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
namespace __ml__ { /* XXX */
namespace __scene__ { /* XXX */
class Scene;
}
}
namespace __ml__ {
namespace __raytracer__ {

class RayTracer;


extern str *__name__;
extern __ml__::__vector3f__::Vector3f *ZERO;


extern class_ *cl_RayTracer;
class RayTracer : public pyobj {
public:
    __ml__::__scene__::Scene *scene_ref;

    RayTracer() {}
    RayTracer(__ml__::__scene__::Scene *scene) {
        this->__class__ = cl_RayTracer;
        __init__(scene);
    }
    void *__init__(__ml__::__scene__::Scene *scene);
    __ml__::__vector3f__::Vector3f *get_radiance(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit);
    __ml__::__vector3f__::Vector3f *sample_emitters(__ml__::__vector3f__::Vector3f *ray_direction, __ml__::__surfacepoint__::SurfacePoint *surface_point);
};

extern __ml__::__triangle__::Triangle * default_0;
void __init();

} // module namespace
} // module namespace
#endif
