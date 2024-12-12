#ifndef __ML_SCENE_HPP
#define __ML_SCENE_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __triangle__ { /* XXX */
class Triangle;
}
}
namespace __ml__ { /* XXX */
namespace __spatialindex__ { /* XXX */
class SpatialIndex;
}
}
namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ {
namespace __scene__ {

extern str *const_0;

class Scene;


extern str *__name__;
extern __re__::re_object *SEARCH;
extern __ss_int MAX_TRIANGLES;
extern __ml__::__vector3f__::Vector3f *MAX, *ONE, *ZERO;


extern class_ *cl_Scene;
class Scene : public pyobj {
public:
    list<__ml__::__triangle__::Triangle *> *triangles;
    list<__ml__::__triangle__::Triangle *> *emitters;
    __ml__::__spatialindex__::SpatialIndex *index;
    __ml__::__vector3f__::Vector3f *ground_reflection;
    __ml__::__vector3f__::Vector3f *sky_emission;

    Scene() {}
    Scene(file *in_stream, __ml__::__vector3f__::Vector3f *eye_position) {
        this->__class__ = cl_Scene;
        __init__(in_stream, eye_position);
    }
    void *__init__(file *in_stream, __ml__::__vector3f__::Vector3f *eye_position);
    tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit);
    tuple2<__ml__::__vector3f__::Vector3f *, __ml__::__triangle__::Triangle *> *get_emitter();
    __ss_int emitters_count();
    __ml__::__vector3f__::Vector3f *get_default_emission(__ml__::__vector3f__::Vector3f *back_direction);
};

void __init();

} // module namespace
} // module namespace
#endif
