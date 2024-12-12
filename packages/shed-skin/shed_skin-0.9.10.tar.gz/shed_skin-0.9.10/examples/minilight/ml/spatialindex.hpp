#ifndef __ML_SPATIALINDEX_HPP
#define __ML_SPATIALINDEX_HPP

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
namespace __spatialindex__ {

class SpatialIndex;

typedef __ss_float (*lambda0)(void *, void *, void *, void *, void *);
typedef __ss_float (*lambda1)(void *, void *, void *, void *, void *);

extern str *__name__;
extern __ss_int MAX_ITEMS, MAX_LEVELS;
extern __ss_float TOLERANCE;
extern __ml__::__vector3f__::Vector3f *MAX;


extern class_ *cl_SpatialIndex;
class SpatialIndex : public pyobj {
public:
    list<__ml__::__triangle__::Triangle *> *items;
    list<__ss_float> *bound;
    __ss_bool is_branch;
    list<SpatialIndex *> *vector;

    SpatialIndex() {}
    SpatialIndex(__ml__::__vector3f__::Vector3f *vect, list<__ss_float> *bound, list<__ml__::__triangle__::Triangle *> *items, __ss_int level) {
        this->__class__ = cl_SpatialIndex;
        __init__(vect, bound, items, level);
    }
    void *__init__(__ml__::__vector3f__::Vector3f *vect, list<__ss_float> *bound, list<__ml__::__triangle__::Triangle *> *items, __ss_int level);
    tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit, __ml__::__vector3f__::Vector3f *start);
};

extern __ml__::__vector3f__::Vector3f * default_0;
void __init();

} // module namespace
} // module namespace
#endif
