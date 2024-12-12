#include "builtin.hpp"
#include "collections.hpp"
#include "itertools.hpp"
#include "life.hpp"

/**
Implementation of: http://en.wikipedia.org/wiki/Conway's_Game_of_Life 
Tested on Python 2.6.4 and Python 3.1.1 
*/

namespace __life__ {

str *const_0;

using __collections__::defaultdict;
using __itertools__::product;

str *__name__;
__ss_int columns, count, rows;


static inline list<tuple<__ss_int> *> *list_comp_0(__ss_int columns, __ss_int rows);
static inline __ss_int __lambda0__();
static inline __ss_int __lambda1__();

static inline list<tuple<__ss_int> *> *list_comp_0(__ss_int columns, __ss_int rows) {
    __ss_int __10, __11, __12, __13, column, row;

    list<tuple<__ss_int> *> *__ss_result = new list<tuple<__ss_int> *>();

    FAST_FOR(row,0,rows,1,10,11)
        FAST_FOR(column,0,columns,1,12,13)
            __ss_result->append((new tuple<__ss_int>(2,row,column)));
        END_FOR

    END_FOR

    return __ss_result;
}

static inline __ss_int __lambda0__() {
    return __int();
}

static inline __ss_int __lambda1__() {
    return __int();
}

__ss_int add(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board, tuple<__ss_int> *pos) {
    /**
    Adds eight cells near current cell 
    */
    __ss_int column, row;
    tuple<__ss_int> *__0;

    __0 = pos;
    __unpack_check(__0, 2);
    row = __0->__getfirst__();
    column = __0->__getsecond__();
    return (((((((board->__getitem__((new tuple<__ss_int>(2,(row-__ss_int(1)),(column-__ss_int(1)))))+board->__getitem__((new tuple<__ss_int>(2,(row-__ss_int(1)),column))))+board->__getitem__((new tuple<__ss_int>(2,(row-__ss_int(1)),(column+__ss_int(1))))))+board->__getitem__((new tuple<__ss_int>(2,row,(column-__ss_int(1))))))+board->__getitem__((new tuple<__ss_int>(2,row,(column+__ss_int(1))))))+board->__getitem__((new tuple<__ss_int>(2,(row+__ss_int(1)),(column-__ss_int(1))))))+board->__getitem__((new tuple<__ss_int>(2,(row+__ss_int(1)),column))))+board->__getitem__((new tuple<__ss_int>(2,(row+__ss_int(1)),(column+__ss_int(1))))));
}

__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *snext(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board) {
    /**
    Calculates the next stage 
    */
    __collections__::defaultdict<tuple<__ss_int> *, __ss_int> *__ss_new;
    tuple<__ss_int> *pos;
    __ss_int __3, __5, item, near;
    list<tuple<__ss_int> *> *__1;
    __iter<tuple<__ss_int> *> *__2;
    list<tuple<__ss_int> *>::for_in_loop __4;
    pyobj *__6, *__7;
    __ss_bool __8, __9;

    __ss_new = (new __collections__::defaultdict<tuple<__ss_int> *, __ss_int>(__lambda0__, board));

    FOR_IN(pos,(new list<tuple<__ss_int> *>(board->keys())),1,3,4)
        near = add(board, pos);
        item = board->__getitem__(pos);
        if (((!__eq(__5=near,__ss_int(2)) && !__eq(__5,__ss_int(3))) and item)) {
            __ss_new->__setitem__(pos, __ss_int(0));
        }
        else if (((near==__ss_int(3)) and __NOT(item))) {
            __ss_new->__setitem__(pos, __ss_int(1));
        }
    END_FOR

    return __ss_new;
}

__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *process(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board) {
    /**
    Finds if this board repeats itself 
    */
    list<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *> *history;

    history = (new list<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *>(1,(new __collections__::defaultdict<tuple<__ss_int> *, __ss_int>(NULL, board))));

    while (__ss_int(1)) {
        board = snext(board);
        if ((history)->__contains__(board)) {
            if (__eq(board, history->__getfast__(__ss_int(0)))) {
                return board;
            }
            return NULL;
        }
        history->append((new __collections__::defaultdict<tuple<__ss_int> *, __ss_int>(NULL, board)));
    }
    return 0;
}

class __gen_generator : public __iter<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *> {
public:
    list<tuple<__ss_int> *> *__22, *ppos;
    __iter<tuple<__ss_int> *> *__14, *__15, *possibilities;
    tuple<__ss_int> *__23, *__ss_case, *pos;
    __collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board;
    __ss_int __16, __21, __24, columns, rows, value;
    __iter<tuple<__ss_int> *>::for_in_loop __17;
    tuple2<tuple<__ss_int> *, __ss_int> *__18;
    __iter<tuple2<tuple<__ss_int> *, __ss_int> *> *__19, *__20;
    __iter<tuple2<tuple<__ss_int> *, __ss_int> *>::for_in_loop __25;

    int __last_yield;

    __gen_generator(__ss_int rows,__ss_int columns) {
        this->rows = rows;
        this->columns = columns;
        __last_yield = -1;
    }

    __collections__::defaultdict<tuple<__ss_int> *, __ss_int> * __get_next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }
        ppos = list_comp_0(columns, rows);
        possibilities = product(1, (rows*columns), (new tuple<__ss_int>(2,__ss_int(0),__ss_int(1))));

        FOR_IN(__ss_case,possibilities,14,16,17)
            board = (new __collections__::defaultdict<tuple<__ss_int> *, __ss_int>(__lambda1__));

            FOR_IN_ZIP(pos,value,ppos,__ss_case,22,23,21,24)
                board->__setitem__(pos, value);
            END_FOR

            __last_yield = 0;
            __result = board;
            return __result;
            __after_yield_0:;
        END_FOR

        __stop_iteration = true;
        return __zero<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *>();
    }

};

__iter<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *> *generator(__ss_int rows, __ss_int columns) {
    /**
    Generates a board 
    */
    return new __gen_generator(rows,columns);

}

void *bruteforce(__ss_int rows, __ss_int columns) {
    __collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board;
    __iter<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *> *__26, *__27;
    __ss_int __28;
    __iter<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *>::for_in_loop __29;

    count = __ss_int(0);

    FOR_IN(board,map(1, process, generator(rows, columns)),26,28,29)
        if ((board!=NULL)) {
            count = (__life__::count+__ss_int(1));
        }
    END_FOR

    return NULL;
}

void __init() {
    const_0 = new str("__main__");

    __name__ = new str("__main__");

    if (__eq(__life__::__name__, const_0)) {
        rows = __ss_int(4);
        columns = __ss_int(3);
        bruteforce(__life__::rows, __life__::columns);
        print(__life__::count);
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __collections__::__init();
    __itertools__::__init();
    __shedskin__::__start(__life__::__init);
}
