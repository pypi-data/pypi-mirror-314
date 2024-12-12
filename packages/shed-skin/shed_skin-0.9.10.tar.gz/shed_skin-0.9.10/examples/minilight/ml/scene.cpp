#include "builtin.hpp"
#include "time.hpp"
#include "re.hpp"
#include "math.hpp"
#include "random.hpp"
#include "ml/triangle.hpp"
#include "ml/spatialindex.hpp"
#include "ml/vector3f.hpp"
#include "ml/scene.hpp"

namespace __ml__ {
namespace __scene__ {

str *const_0;

using __random__::choice;
using __ml__::__spatialindex__::SpatialIndex;
using __ml__::__triangle__::Triangle;
using __ml__::__vector3f__::Vector3f_str;

str *__name__;
__re__::re_object *SEARCH;
__ss_int MAX_TRIANGLES;
__ml__::__vector3f__::Vector3f *MAX, *ONE, *ZERO;


static inline list<__ml__::__triangle__::Triangle *> *list_comp_0(Scene *self);

static inline list<__ml__::__triangle__::Triangle *> *list_comp_0(Scene *self) {
    __ml__::__triangle__::Triangle *triangle;
    list<__ml__::__triangle__::Triangle *> *__109;
    __iter<__ml__::__triangle__::Triangle *> *__110;
    __ss_int __111;
    list<__ml__::__triangle__::Triangle *>::for_in_loop __112;
    __ss_bool __113, __114;

    list<__ml__::__triangle__::Triangle *> *__ss_result = new list<__ml__::__triangle__::Triangle *>();

    __109 = self->triangles;
    FOR_IN(triangle,__109,109,111,112)
        if ((__NOT((triangle->emitivity)->is_zero()) and (triangle->area>__ss_float(0.0)))) {
            __ss_result->append(triangle);
        }
    END_FOR

    return __ss_result;
}

/**
class Scene
*/

class_ *cl_Scene;

void *Scene::__init__(file *in_stream, __ml__::__vector3f__::Vector3f *eye_position) {
    str *g, *line, *s;
    __ss_int __103, __106, __107, i;
    file *__101;
    __iter<str *> *__102;
    file::for_in_loop __104;
    tuple<str *> *__105;


    FOR_IN(line,in_stream,101,103,104)
        if (__NOT(line->isspace())) {
            __105 = (__ml__::__scene__::SEARCH->search(line, __ss_int(0), (-__ss_int(1))))->groups(NULL);
            __unpack_check(__105, 2);
            s = __105->__getfast__(0);
            g = __105->__getfast__(1);
            this->sky_emission = (Vector3f_str(s))->clamped(__ml__::__scene__::ZERO, __ml__::__scene__::MAX);
            this->ground_reflection = (Vector3f_str(g))->clamped(__ml__::__scene__::ZERO, __ml__::__scene__::ONE);
            this->triangles = (new list<__ml__::__triangle__::Triangle *>());
            try {

                FAST_FOR(i,0,__ml__::__scene__::MAX_TRIANGLES,1,106,107)
                    (this->triangles)->append((new __ml__::__triangle__::Triangle(in_stream)));
                END_FOR

            } catch (StopIteration *) {
            }
            this->emitters = list_comp_0(this);
            this->index = (new __ml__::__spatialindex__::SpatialIndex(eye_position, NULL, this->triangles, __ss_int(0)));
            break;
        }
    END_FOR

    return NULL;
}

tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *Scene::get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit) {
    return (this->index)->get_intersection(ray_origin, ray_direction, last_hit, NULL);
}

tuple2<__ml__::__vector3f__::Vector3f *, __ml__::__triangle__::Triangle *> *Scene::get_emitter() {
    __ml__::__triangle__::Triangle *emitter;

    emitter = (((len(this->emitters)==__ss_int(0)))?(NULL):(choice(this->emitters)));
    return (new tuple2<__ml__::__vector3f__::Vector3f *, __ml__::__triangle__::Triangle *>(2,((___bool(emitter))?(emitter->get_sample_point()):(__ml__::__scene__::ZERO)),emitter));
}

__ss_int Scene::emitters_count() {
    return len(this->emitters);
}

__ml__::__vector3f__::Vector3f *Scene::get_default_emission(__ml__::__vector3f__::Vector3f *back_direction) {
    return (((back_direction->y<__ss_float(0.0)))?(this->sky_emission):((this->sky_emission)->mul(this->ground_reflection)));
}

void __init() {
    const_0 = new str("(\\(.+\\))\\s*(\\(.+\\))");

    __name__ = new str("scene");

    ZERO = __ml__::__vector3f__::ZERO;
    ONE = __ml__::__vector3f__::ONE;
    MAX = __ml__::__vector3f__::MAX;
    SEARCH = __re__::compile(const_0, __ss_int(0));
    MAX_TRIANGLES = __ss_int(1048576);
    cl_Scene = new class_("Scene");
}

} // module namespace
} // module namespace

