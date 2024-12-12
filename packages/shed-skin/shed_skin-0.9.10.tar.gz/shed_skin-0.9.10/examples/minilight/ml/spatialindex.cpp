#include "builtin.hpp"
#include "time.hpp"
#include "re.hpp"
#include "math.hpp"
#include "random.hpp"
#include "ml/triangle.hpp"
#include "ml/spatialindex.hpp"
#include "ml/vector3f.hpp"

namespace __ml__ {
namespace __spatialindex__ {

using __ml__::__vector3f__::Vector3f_seq;
using __ml__::__vector3f__::Vector3f_scalar;

str *__name__;
__ss_int MAX_ITEMS, MAX_LEVELS;
__ss_float TOLERANCE;
__ml__::__vector3f__::Vector3f *MAX;


__ml__::__vector3f__::Vector3f * default_0;

/**
class SpatialIndex
*/

class_ *cl_SpatialIndex;

void *SpatialIndex::__init__(__ml__::__vector3f__::Vector3f *vect, list<__ss_float> *bound, list<__ml__::__triangle__::Triangle *> *items, __ss_int level) {
    __ml__::__triangle__::Triangle *item;
    __ss_int __58, __62, __64, __65, __68, __69, __70, __71, __74, j, m, q1, s;
    __ss_float size;
    list<__ss_float> *sub_bound;
    list<__ml__::__triangle__::Triangle *> *__56, *__60, *__72, *sub_items;
    __ss_bool __66, __67, __76, __77, __78, __79, __80, __81, __82, __83, q2;
    __iter<__ml__::__triangle__::Triangle *> *__57, *__61, *__73;
    list<__ml__::__triangle__::Triangle *>::for_in_loop __59, __63, __75;
    list<SpatialIndex *> *__84;

    if (___bool(vect)) {

        FOR_IN(item,items,56,58,59)
            item->bound = item->get_bound();
        END_FOR

        bound = (vect->as_list())->__mul__(__ss_int(2));

        FOR_IN(item,items,60,62,63)

            FAST_FOR(j,0,__ss_int(6),1,64,65)
                if (((___bool((bound->__getfast__(j)>(item->bound)->__getfast__(j))))^(___bool((j>__ss_int(2)))))) {
                    bound->__setitem__(j, (item->bound)->__getfast__(j));
                }
            END_FOR

        END_FOR

        size = ___max(1, __ss_int(0), ((Vector3f_seq(bound->__slice__(__ss_int(3), __ss_int(3), __ss_int(6), __ss_int(0))))->__sub__(Vector3f_seq(bound->__slice__(__ss_int(3), __ss_int(0), __ss_int(3), __ss_int(0)))))->as_list());
        this->bound = (bound->__slice__(__ss_int(3), __ss_int(0), __ss_int(3), __ss_int(0)))->__add__(((Vector3f_seq(bound->__slice__(__ss_int(3), __ss_int(3), __ss_int(6), __ss_int(0))))->clamped((Vector3f_seq(bound->__slice__(__ss_int(3), __ss_int(0), __ss_int(3), __ss_int(0))))->__add__(Vector3f_scalar(size)), __ml__::__spatialindex__::MAX))->as_list());
    }
    else {
        this->bound = bound;
    }
    this->is_branch = __AND(___bool((len(items)>__ml__::__spatialindex__::MAX_ITEMS)), ___bool((level<(__ml__::__spatialindex__::MAX_LEVELS-__ss_int(1)))), 66);
    if (this->is_branch) {
        q1 = __ss_int(0);
        this->vector = ((new list<SpatialIndex *>(1,NULL)))->__mul__(__ss_int(8));

        FAST_FOR(s,0,__ss_int(8),1,68,69)
            sub_bound = (new list<__ss_float>());

            FAST_FOR(j,0,__ss_int(6),1,70,71)
                m = __mods(j, __ss_int(3));
                if (((___bool(((((s>>m))&(__ss_int(1)))!=__ss_int(0))))^(___bool((j>__ss_int(2)))))) {
                    sub_bound->append((((this->bound)->__getfast__(m)+(this->bound)->__getfast__((m+__ss_int(3))))*__ss_float(0.5)));
                }
                else {
                    sub_bound->append((this->bound)->__getfast__(j));
                }
            END_FOR

            sub_items = (new list<__ml__::__triangle__::Triangle *>());

            FOR_IN(item,items,72,74,75)
                if ((((item->bound)->__getfast__(__ss_int(3))>=sub_bound->__getfast__(__ss_int(0))) and ((item->bound)->__getfast__(__ss_int(0))<sub_bound->__getfast__(__ss_int(3))) and ((item->bound)->__getfast__(__ss_int(4))>=sub_bound->__getfast__(__ss_int(1))) and ((item->bound)->__getfast__(__ss_int(1))<sub_bound->__getfast__(__ss_int(4))) and ((item->bound)->__getfast__(__ss_int(5))>=sub_bound->__getfast__(__ss_int(2))) and ((item->bound)->__getfast__(__ss_int(2))<sub_bound->__getfast__(__ss_int(5))))) {
                    sub_items->append(item);
                }
            END_FOR

            q1 = (q1+(((len(sub_items)==len(items)))?(__ss_int(1)):(__ss_int(0))));
            q2 = ___bool(((sub_bound->__getfast__(__ss_int(3))-sub_bound->__getfast__(__ss_int(0)))<(__ml__::__spatialindex__::TOLERANCE*__ss_float(4.0))));
            if ((len(sub_items)>__ss_int(0))) {
                this->vector->__setitem__(s, (new SpatialIndex(NULL, sub_bound, sub_items, ((__OR(___bool((q1>__ss_int(1))), q2, 82))?(__ml__::__spatialindex__::MAX_LEVELS):((level+__ss_int(1)))))));
            }
        END_FOR

    }
    else {
        this->items = items;
    }
    return NULL;
}

tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *SpatialIndex::get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction, __ml__::__triangle__::Triangle *last_hit, __ml__::__vector3f__::Vector3f *start) {
    __ml__::__triangle__::Triangle *hit_object, *item;
    __ml__::__vector3f__::Vector3f *cell_position, *hit, *hit_position;
    __ss_float b0, b1, b2, b3, b4, b5, distance, face, nearest_distance, step;
    __ss_int __87, __88, __93, axis, high, i, sub_cell;
    list<__ss_float> *__85;
    tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *> *__86;
    __ss_bool __100, __89, __90, __95, __96, __97, __98, __99;
    list<__ml__::__triangle__::Triangle *> *__91;
    __iter<__ml__::__triangle__::Triangle *> *__92;
    list<__ml__::__triangle__::Triangle *>::for_in_loop __94;

    start = ((___bool(start))?(start):(ray_origin));
    hit_object = NULL;
    hit_position = NULL;
    __85 = this->bound;
    __unpack_check(__85, 6);
    b0 = __85->__getfast__(0);
    b1 = __85->__getfast__(1);
    b2 = __85->__getfast__(2);
    b3 = __85->__getfast__(3);
    b4 = __85->__getfast__(4);
    b5 = __85->__getfast__(5);
    if (this->is_branch) {
        sub_cell = (((start->x>=((b0+b3)*__ss_float(0.5))))?(__ss_int(1)):(__ss_int(0)));
        if ((start->y>=((b1+b4)*__ss_float(0.5)))) {
            sub_cell = ((sub_cell)|(__ss_int(2)));
        }
        if ((start->z>=((b2+b5)*__ss_float(0.5)))) {
            sub_cell = ((sub_cell)|(__ss_int(4)));
        }
        cell_position = start;

        while (True) {
            if (((this->vector)->__getfast__(sub_cell)!=NULL)) {
                __86 = ((this->vector)->__getfast__(sub_cell))->get_intersection(ray_origin, ray_direction, last_hit, cell_position);
                __unpack_check(__86, 2);
                hit_object = __86->__getfirst__();
                hit_position = __86->__getsecond__();
                if ((hit_object!=NULL)) {
                    break;
                }
            }
            step = __ss_float(1.797e+308);
            axis = __ss_int(0);

            FAST_FOR(i,0,__ss_int(3),1,87,88)
                high = (((sub_cell>>i))&(__ss_int(1)));
                face = ((((___bool((ray_direction->__getitem__(i)<__ss_float(0.0))))^(___bool((__ss_int(0)!=high)))))?((this->bound)->__getfast__((i+(high*__ss_int(3))))):((((this->bound)->__getfast__(i)+(this->bound)->__getfast__((i+__ss_int(3))))*__ss_float(0.5))));
                ASSERT(__AND(True, True, 89), 0);
                try {
                    distance = ((face-ray_origin->__getitem__(i))/ray_direction->__getitem__(i));
                } catch (Exception *) {
                    distance = __ss_float(INFINITY);
                }
                if ((distance<=step)) {
                    step = distance;
                    axis = i;
                }
            END_FOR

            if (((___bool(((((sub_cell>>axis))&(__ss_int(1)))==__ss_int(1))))^(___bool((ray_direction->__getitem__(axis)<__ss_float(0.0)))))) {
                break;
            }
            cell_position = (ray_origin)->__add__((ray_direction)->__mul__(step));
            sub_cell = ((sub_cell)^((__ss_int(1)<<axis)));
        }
    }
    else {
        nearest_distance = __ss_float(1.797e+308);

        FOR_IN(item,this->items,91,93,94)
            if (__ne(item, last_hit)) {
                distance = item->get_intersection(ray_origin, ray_direction);
                if ((__ss_float(0.0)<=distance)&&(distance<nearest_distance)) {
                    hit = (ray_origin)->__add__((ray_direction)->__mul__(distance));
                    if ((((b0-hit->x)<=__ml__::__spatialindex__::TOLERANCE) and ((hit->x-b3)<=__ml__::__spatialindex__::TOLERANCE) and ((b1-hit->y)<=__ml__::__spatialindex__::TOLERANCE) and ((hit->y-b4)<=__ml__::__spatialindex__::TOLERANCE) and ((b2-hit->z)<=__ml__::__spatialindex__::TOLERANCE) and ((hit->z-b5)<=__ml__::__spatialindex__::TOLERANCE))) {
                        hit_object = item;
                        hit_position = hit;
                        nearest_distance = distance;
                    }
                }
            }
        END_FOR

    }
    return (new tuple2<__ml__::__triangle__::Triangle *, __ml__::__vector3f__::Vector3f *>(2,hit_object,hit_position));
}

void __init() {
    __name__ = new str("spatialindex");

    TOLERANCE = __ml__::__triangle__::TOLERANCE;
    MAX = __ml__::__vector3f__::MAX;
    MAX_LEVELS = __ss_int(44);
    MAX_ITEMS = __ss_int(8);
    default_0 = NULL;
    cl_SpatialIndex = new class_("SpatialIndex");
}

} // module namespace
} // module namespace

