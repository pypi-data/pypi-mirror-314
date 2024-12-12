#ifndef __SOKOBAN_HPP
#define __SOKOBAN_HPP

using namespace __shedskin__;
namespace __sokoban__ {

extern bytes *const_0, *const_10, *const_2, *const_4, *const_7, *const_9;
extern str *const_1, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_3, *const_5, *const_6, *const_8;

class Direction;
class Open;
class Board;


extern str *__name__, *level;
extern Board *b;


extern class_ *cl_Direction;
class Direction : public pyobj {
public:
    str *letter;
    __ss_int dx;
    __ss_int dy;

    Direction() {}
    Direction(__ss_int dx, __ss_int dy, str *letter) {
        this->__class__ = cl_Direction;
        __init__(dx, dy, letter);
    }
    void *__init__(__ss_int dx, __ss_int dy, str *letter);
};

extern class_ *cl_Open;
class Open : public pyobj {
public:
    __ss_int x;
    __ss_int y;
    str *csol;
    bytes *cur;

    Open() {}
    Open(bytes *cur, str *csol, __ss_int x, __ss_int y) {
        this->__class__ = cl_Open;
        __init__(cur, csol, x, y);
    }
    void *__init__(bytes *cur, str *csol, __ss_int x, __ss_int y);
};

extern class_ *cl_Board;
class Board : public pyobj {
public:
    bytes *sdata;
    bytes *ddata;
    __ss_int py;
    __ss_int px;
    __ss_int nrows;

    Board() {}
    Board(str *board) {
        this->__class__ = cl_Board;
        __init__(board);
    }
    void *__init__(str *board);
    bytes *move(__ss_int x, __ss_int y, __ss_int dx, __ss_int dy, bytes *data);
    bytes *push(__ss_int x, __ss_int y, __ss_int dx, __ss_int dy, bytes *data);
    __ss_bool is_solved(bytes *data);
    str *solve();
};


} // module namespace
#endif
