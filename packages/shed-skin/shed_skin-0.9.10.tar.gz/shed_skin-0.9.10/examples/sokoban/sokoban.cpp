#include "builtin.hpp"
#include "collections.hpp"
#include "sokoban.hpp"

namespace __sokoban__ {

bytes *const_0, *const_10, *const_2, *const_4, *const_7, *const_9;
str *const_1, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_3, *const_5, *const_6, *const_8;

using __collections__::deque;

str *__name__, *level;
Board *b;


class list_comp_0 : public __iter<__ss_int> {
public:
    str *r;
    list<str *> *__7;
    __iter<str *> *__8;
    __ss_int __9;
    list<str *>::for_in_loop __10;

    list<str *> *data;
    int __last_yield;

    list_comp_0(list<str *> *data);
    __ss_int __get_next();
};


list_comp_0::list_comp_0(list<str *> *data) {
    this->data = data;
    __last_yield = -1;
}

__ss_int list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FOR_IN(r,data,7,9,10)
        __result = len(r);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

/**
class Direction
*/

class_ *cl_Direction;

void *Direction::__init__(__ss_int dx, __ss_int dy, str *letter) {
    __ss_int __0, __1;
    str *__2;

    __0 = dx;
    __1 = dy;
    __2 = letter;
    this->dx = __0;
    this->dy = __1;
    this->letter = __2;
    return NULL;
}

/**
class Open
*/

class_ *cl_Open;

void *Open::__init__(bytes *cur, str *csol, __ss_int x, __ss_int y) {
    bytes *__3;
    str *__4;
    __ss_int __5, __6;

    __3 = cur;
    __4 = csol;
    __5 = x;
    __6 = y;
    this->cur = __3;
    this->csol = __4;
    this->x = __5;
    this->y = __6;
    return NULL;
}

/**
class Board
*/

class_ *cl_Board;

void *Board::__init__(str *board) {
    list<str *> *__15, *data;
    __ss_int __14, __20, c, r;
    dict<str *, bytes *> *mapd, *maps;
    str *__21, *ch, *row;
    tuple2<__ss_int, str *> *__11, *__17;
    __iter<tuple2<__ss_int, str *> *> *__12, *__13, *__18, *__19;
    __iter<tuple2<__ss_int, str *> *>::for_in_loop __16, __22;

    data = (new list<str *>(filter(NULL, board->splitlines())));
    this->nrows = ___max(1, __ss_int(0), new list_comp_0(data));
    this->sdata = const_0;
    this->ddata = const_0;
    maps = (new dict<str *, bytes *>(5, (new tuple2<str *, bytes *>(2,const_1,const_2)),(new tuple2<str *, bytes *>(2,const_3,const_4)),(new tuple2<str *, bytes *>(2,const_5,const_2)),(new tuple2<str *, bytes *>(2,const_6,const_7)),(new tuple2<str *, bytes *>(2,const_8,const_2))));
    mapd = (new dict<str *, bytes *>(5, (new tuple2<str *, bytes *>(2,const_1,const_2)),(new tuple2<str *, bytes *>(2,const_3,const_2)),(new tuple2<str *, bytes *>(2,const_5,const_9)),(new tuple2<str *, bytes *>(2,const_6,const_2)),(new tuple2<str *, bytes *>(2,const_8,const_10))));

    FOR_IN_ENUMERATE(row,data,15,14)
        r = __14;

        FOR_IN_ENUMERATE_STR(ch,row,21,20)
            c = __20;
            this->sdata = (this->sdata)->__iadd__(maps->__getitem__(ch));
            this->ddata = (this->ddata)->__iadd__(mapd->__getitem__(ch));
            if (__eq(ch, const_5)) {
                this->px = c;
                this->py = r;
            }
        END_FOR

    END_FOR

    return NULL;
}

bytes *Board::move(__ss_int x, __ss_int y, __ss_int dx, __ss_int dy, bytes *data) {
    bytes *data2;
    __ss_bool __23, __24;

    if ((((this->sdata)->__getitem__(((((y+dy)*this->nrows)+x)+dx))==ord(const_6)) or (data->__getitem__(((((y+dy)*this->nrows)+x)+dx))!=ord(const_1)))) {
        return NULL;
    }
    data2 = __bytearray(data);
    data2->__setitem__(((y*this->nrows)+x), ord(const_1));
    data2->__setitem__(((((y+dy)*this->nrows)+x)+dx), ord(const_5));
    return __bytes(data2);
}

bytes *Board::push(__ss_int x, __ss_int y, __ss_int dx, __ss_int dy, bytes *data) {
    bytes *data2;
    __ss_bool __25, __26;

    if ((((this->sdata)->__getitem__(((((y+(__ss_int(2)*dy))*this->nrows)+x)+(__ss_int(2)*dx)))==ord(const_6)) or (data->__getitem__(((((y+(__ss_int(2)*dy))*this->nrows)+x)+(__ss_int(2)*dx)))!=ord(const_1)))) {
        return NULL;
    }
    data2 = __bytearray(data);
    data2->__setitem__(((y*this->nrows)+x), ord(const_1));
    data2->__setitem__(((((y+dy)*this->nrows)+x)+dx), ord(const_5));
    data2->__setitem__(((((y+(__ss_int(2)*dy))*this->nrows)+x)+(__ss_int(2)*dx)), ord(const_11));
    return __bytes(data2);
}

__ss_bool Board::is_solved(bytes *data) {
    __ss_int __27, __28, i;


    FAST_FOR(i,0,len(data),1,27,28)
        if ((___bool(((this->sdata)->__getitem__(i)==ord(const_3)))!=___bool((data->__getitem__(i)==ord(const_11))))) {
            return False;
        }
    END_FOR

    return True;
}

str *Board::solve() {
    __collections__::deque<Open *> *todo;
    set<bytes *> *visited;
    tuple<Direction *> *dirs;
    Open *o;
    bytes *__29, *cur, *temp;
    str *__30, *csol;
    __ss_int __31, __32, __33, __34, __35, __36, dx, dy, i, x, y;
    Direction *dir;
    pyobj *__37, *__38, *__39, *__40;

    todo = (new __collections__::deque<Open *>());
    todo->append((new Open(this->ddata, const_12, this->px, this->py)));
    visited = (new set<bytes *>());
    visited->add(this->ddata);
    dirs = (new tuple<Direction *>(4,(new Direction(__ss_int(0), (-__ss_int(1)), const_13)),(new Direction(__ss_int(1), __ss_int(0), const_14)),(new Direction(__ss_int(0), __ss_int(1), const_15)),(new Direction((-__ss_int(1)), __ss_int(0), const_16))));

    while (___bool(todo)) {
        o = todo->popleft();
        __29 = o->cur;
        __30 = o->csol;
        __31 = o->x;
        __32 = o->y;
        cur = __29;
        csol = __30;
        x = __31;
        y = __32;

        FAST_FOR(i,0,__ss_int(4),1,33,34)
            temp = cur;
            dir = dirs->__getfast__(i);
            __35 = dir->dx;
            __36 = dir->dy;
            dx = __35;
            dy = __36;
            if ((temp->__getitem__(((((y+dy)*this->nrows)+x)+dx))==ord(const_11))) {
                temp = this->push(x, y, dx, dy, temp);
                if ((___bool(temp) and (!(visited)->__contains__(temp)))) {
                    if (this->is_solved(temp)) {
                        return (csol)->__add__((dir->letter)->upper());
                    }
                    todo->append((new Open(temp, (csol)->__add__((dir->letter)->upper()), (x+dx), (y+dy))));
                    visited->add(temp);
                }
            }
            else {
                temp = this->move(x, y, dx, dy, temp);
                if ((___bool(temp) and (!(visited)->__contains__(temp)))) {
                    if (this->is_solved(temp)) {
                        return (csol)->__add__(dir->letter);
                    }
                    todo->append((new Open(temp, (csol)->__add__(dir->letter), (x+dx), (y+dy))));
                    visited->add(temp);
                }
            }
        END_FOR

    }
    return const_17;
}

void __init() {
    const_0 = new bytes("");
    const_1 = __char_cache[32];
    const_2 = __byte_cache[32];
    const_3 = __char_cache[46];
    const_4 = __byte_cache[46];
    const_5 = __char_cache[64];
    const_6 = __char_cache[35];
    const_7 = __byte_cache[35];
    const_8 = __char_cache[36];
    const_9 = __byte_cache[64];
    const_10 = __byte_cache[42];
    const_11 = __char_cache[42];
    const_12 = new str("");
    const_13 = __char_cache[117];
    const_14 = __char_cache[114];
    const_15 = __char_cache[100];
    const_16 = __char_cache[108];
    const_17 = new str("No solution");
    const_18 = new str("#######\n#     #\n#     #\n#. #  #\n#. $$ #\n#.$$  #\n#.#  @#\n#######");

    __name__ = new str("__main__");

    cl_Direction = new class_("Direction");
    cl_Open = new class_("Open");
    cl_Board = new class_("Board");
    level = const_18;
    print(__sokoban__::level);
    print();
    b = (new Board(__sokoban__::level));
    print(__sokoban__::b->solve());
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __collections__::__init();
    __shedskin__::__start(__sokoban__::__init);
}
