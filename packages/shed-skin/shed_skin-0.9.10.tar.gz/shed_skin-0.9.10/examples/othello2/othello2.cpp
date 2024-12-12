#include "builtin.hpp"
#include "time.hpp"
#include "sys.hpp"
#include "othello2.hpp"

namespace __othello2__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_40, *const_41, *const_42, *const_43, *const_44, *const_45, *const_46, *const_47, *const_48, *const_49, *const_5, *const_50, *const_51, *const_52, *const_53, *const_54, *const_55, *const_56, *const_57, *const_6, *const_7, *const_8, *const_9;


str *__name__, *arg, *mode;
__ss_int ALPHA_MIN, BETA_MAX, BLACK, CORNER_MASK, NODES, WHITE, WIN_BONUS, __49, i, max_depth;
list<__ss_int> *MASKS, *SHIFTS;
tuple2<__ss_int, str *> *__46;
__iter<tuple2<__ss_int, str *> *> *__47, *__48;
list<str *> *__50;
__iter<tuple2<__ss_int, str *> *>::for_in_loop __51;


__ss_int  default_0;
__ss_int  default_1;

__ss_int shift(__ss_int disks, __ss_int direction, __ss_int S, __ss_int M) {
    if ((direction<__ss_int(4LL))) {
        return (((disks>>S))&(M));
    }
    else {
        return (((disks<<S))&(M));
    }
    return 0;
}

__ss_int possible_moves(list<__ss_int> *state, __ss_int color) {
    __ss_int M, S, __3, __4, direction, empties, moves, my_disks, opp_disks, x;

    moves = __ss_int(0LL);
    my_disks = state->__getfast__(color);
    opp_disks = state->__getfast__(((color)^(__ss_int(1LL))));
    empties = ~((my_disks)|(opp_disks));

    FAST_FOR(direction,0,__ss_int(8LL),1,3,4)
        S = __othello2__::SHIFTS->__getfast__(direction);
        M = __othello2__::MASKS->__getfast__(direction);
        x = ((shift(my_disks, direction, S, M))&(opp_disks));
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        moves = ((moves)|(((shift(x, direction, S, M))&(empties))));
    END_FOR

    return moves;
}

void *do_move(list<__ss_int> *state, __ss_int color, __ss_int move) {
    __ss_int M, S, __10, __12, __6, __7, __8, bounding_disk, captured_disks, direction, disk, my_disks, opp_disks, x;
    list<__ss_int> *__11, *__5, *__9;

    disk = (__ss_int(1LL)<<move);
    __5 = state;
    __6 = color;
    __5->__setitem__(__6, ((__5->__getfast__(__6))|(disk)));
    my_disks = state->__getfast__(color);
    opp_disks = state->__getfast__(((color)^(__ss_int(1LL))));
    captured_disks = __ss_int(0LL);

    FAST_FOR(direction,0,__ss_int(8LL),1,7,8)
        S = __othello2__::SHIFTS->__getfast__(direction);
        M = __othello2__::MASKS->__getfast__(direction);
        x = ((shift(disk, direction, S, M))&(opp_disks));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        x = ((x)|(((shift(x, direction, S, M))&(opp_disks))));
        if ((x==__ss_int(0LL))) {
            continue;
        }
        bounding_disk = ((shift(x, direction, S, M))&(my_disks));
        if (bounding_disk) {
            captured_disks = ((captured_disks)|(x));
        }
    END_FOR

    __9 = state;
    __10 = color;
    __9->__setitem__(__10, ((__9->__getfast__(__10))^(captured_disks)));
    __11 = state;
    __12 = ((color)^(__ss_int(1LL)));
    __11->__setitem__(__12, ((__11->__getfast__(__12))^(captured_disks)));
    return NULL;
}

void *print_board(list<__ss_int> *state) {
    __ss_int __13, __14, mask, move;


    FAST_FOR(move,0,__ss_int(64LL),1,13,14)
        mask = (__ss_int(1LL)<<move);
        if (((state->__getfast__(__othello2__::BLACK))&(mask))) {
            print_(1, False, NULL, const_0, NULL, const_1);
        }
        else if (((state->__getfast__(__othello2__::WHITE))&(mask))) {
            print_(1, False, NULL, const_0, NULL, const_2);
        }
        else {
            print_(1, False, NULL, const_0, NULL, const_3);
        }
        if ((__mods(move, __ss_int(8LL))==__ss_int(7LL))) {
            print();
        }
    END_FOR

    print(__add_strs(4, __str(const_4), __str(__int___::bit_count(state->__getfast__(__ss_int(0LL)))), __str(const_5), __str(__int___::bit_count(state->__getfast__(__ss_int(1LL))))));
    return NULL;
}

list<__ss_int> *parse_state(str *board) {
    list<__ss_int> *__17, *__19, *state;
    __ss_int __15, __16, __18, __20, mask, move;

    state = (new list<__ss_int>(2,__ss_int(0LL),__ss_int(0LL)));

    FAST_FOR(move,0,__ss_int(64LL),1,15,16)
        mask = (__ss_int(1LL)<<move);
        if (__eq(board->__getfast__(move), const_1)) {
            __17 = state;
            __18 = __ss_int(0LL);
            __17->__setitem__(__18, ((__17->__getfast__(__18))|(mask)));
        }
        else if (__eq(board->__getfast__(move), const_2)) {
            __19 = state;
            __20 = __ss_int(1LL);
            __19->__setitem__(__20, ((__19->__getfast__(__20))|(mask)));
        }
    END_FOR

    return state;
}

str *human_move(__ss_int move) {
    __ss_int col, row;

    col = ((move)&(__ss_int(7LL)));
    row = (((move>>__ss_int(3LL)))&(__ss_int(7LL)));
    return ((const_6)->__getfast__(col))->__add__(__str((row+__ss_int(1LL))));
}

__ss_int parse_move(str *s) {
    return ((const_6)->index(s->__getfast__(__ss_int(0LL)))+(__ss_int(8LL)*(__int(s->__getfast__(__ss_int(1LL)))-__ss_int(1LL))));
}

__ss_int evaluate(list<__ss_int> *state, __ss_int color, __ss_bool is_max_player, __ss_int my_moves, __ss_int opp_moves) {
    __ss_int my_corners, my_disks, opp_corners, opp_disks, value;

    value = __ss_int(0LL);
    if ((((my_moves)|(opp_moves))==__ss_int(0LL))) {
        value = (__int___::bit_count(state->__getfast__(color))-__int___::bit_count(state->__getfast__(((color)^(__ss_int(1LL))))));
        value = (value*__othello2__::WIN_BONUS);
    }
    else {
        my_disks = state->__getfast__(color);
        opp_disks = state->__getfast__(((color)^(__ss_int(1LL))));
        my_corners = ((my_disks)&(__othello2__::CORNER_MASK));
        opp_corners = ((opp_disks)&(__othello2__::CORNER_MASK));
        value = (value+((__int___::bit_count(my_corners)-__int___::bit_count(opp_corners))*__ss_int(16LL)));
        value = (value+((__int___::bit_count(my_moves)-__int___::bit_count(opp_moves))*__ss_int(2LL)));
    }
    if (is_max_player) {
        return value;
    }
    else {
        return (-value);
    }
    return 0;
}

__ss_int minimax_ab(list<__ss_int> *state, __ss_int color, __ss_int depth, __ss_int max_depth, __ss_bool is_max_player, __ss_int alpha, __ss_int beta) {
    __ss_int __21, __22, best_move, best_val, move, moves, opp_moves, orig_black, orig_white, val;

    NODES = (__othello2__::NODES+__ss_int(1LL));
    moves = possible_moves(state, color);
    opp_moves = possible_moves(state, ((color)^(__ss_int(1LL))));
    if ((depth==max_depth)) {
        return evaluate(state, color, is_max_player, moves, opp_moves);
    }
    if ((moves==__ss_int(0LL))) {
        if ((opp_moves==__ss_int(0LL))) {
            return evaluate(state, color, is_max_player, moves, opp_moves);
        }
        color = ((color)^(__ss_int(1LL)));
        is_max_player = __NOT(is_max_player);
        moves = opp_moves;
    }
    orig_black = state->__getfast__(__ss_int(0LL));
    orig_white = state->__getfast__(__ss_int(1LL));
    if (is_max_player) {
        best_val = __othello2__::ALPHA_MIN;
    }
    else {
        best_val = __othello2__::BETA_MAX;
    }

    FAST_FOR(move,0,__ss_int(64LL),1,21,22)
        if (((moves)&((__ss_int(1LL)<<move)))) {
            do_move(state, color, move);
            val = minimax_ab(state, ((color)^(__ss_int(1LL))), (depth+__ss_int(1LL)), max_depth, __NOT(is_max_player), alpha, beta);
            state->__setitem__(__ss_int(0LL), orig_black);
            state->__setitem__(__ss_int(1LL), orig_white);
            if (is_max_player) {
                if ((val>best_val)) {
                    best_move = move;
                    best_val = val;
                }
                alpha = ___max(2, __ss_int(0LL), alpha, best_val);
            }
            else {
                if ((val<best_val)) {
                    best_move = move;
                    best_val = val;
                }
                beta = ___min(2, __ss_int(0LL), beta, best_val);
            }
            if ((beta<=alpha)) {
                break;
            }
        }
    END_FOR

    if ((depth>__ss_int(0LL))) {
        return best_val;
    }
    else {
        return best_move;
    }
    return 0;
}

str *empty_board() {
    return const_7;
}

void *vs_cpu_cli(__ss_int max_depth) {
    str *board;
    list<__ss_int> *state;
    __ss_int color, move, moves, passing;
    __ss_float t0, t1;

    board = empty_board();
    state = parse_state(board);
    color = __othello2__::BLACK;
    print_board(state);

    while (True) {
        NODES = __ss_int(0LL);
        passing = __ss_int(0LL);
        moves = possible_moves(state, color);
        if ((moves==__ss_int(0LL))) {
            print(const_8);
            passing = (passing+__ss_int(1LL));
        }
        else {
            print(const_9);
            t0 = __time__::time();
            move = minimax_ab(state, color, __ss_int(0LL), max_depth, True, default_0, default_1);
            t1 = (__time__::time()-t0);
            print(__mod6(const_10, 3, __othello2__::NODES, t1, (__othello2__::NODES/t1)));
            print(__add_strs(2, __str(const_11), __str(human_move(move))));
            do_move(state, color, move);
            print_board(state);
        }
        color = ((color)^(__ss_int(1LL)));
        moves = possible_moves(state, color);
        if ((moves==__ss_int(0LL))) {
            print(const_12);
            passing = (passing+__ss_int(1LL));
            if ((passing==__ss_int(2LL))) {
                print_board(state);
                break;
            }
        }
        else {

            while (True) {
                move = parse_move(input(const_13));
                if (((moves)&((__ss_int(1LL)<<move)))) {
                    break;
                }
            }
            do_move(state, color, move);
            print_board(state);
        }
        color = ((color)^(__ss_int(1LL)));
    }
    return NULL;
}

void *vs_cpu_nboard(__ss_int max_depth) {
    str *__32, *a, *b, *board, *l, *line;
    list<__ss_int> *state;
    __ss_int __25, __29, color, move, moves;
    file *__23;
    __iter<str *> *__24, *__28;
    file::for_in_loop __26;
    list<str *> *__27, *__33;
    list<str *>::for_in_loop __30;
    void *__31;

    board = empty_board();
    state = parse_state(board);
    color = __othello2__::BLACK;
    (__sys__::__ss_stdout)->write(const_14);

    FOR_IN(line,__sys__::__ss_stdin,23,25,26)
        line = line->strip();
        if (__eq(line, const_15)) {
            moves = possible_moves(state, color);
            if ((moves==__ss_int(0LL))) {
                (__sys__::__ss_stdout)->write(const_16);
                color = ((color)^(__ss_int(1LL)));
            }
            else {
                move = minimax_ab(state, color, __ss_int(0LL), max_depth, True, default_0, default_1);
                (__sys__::__ss_stdout)->write(__mod6(const_17, 1, (human_move(move))->upper()));
            }
        }
        else if (line->startswith(const_18)) {
            (__sys__::__ss_stdout)->write(__add_strs(3, const_19, line->__slice__(__ss_int(1LL), __ss_int(5LL), __ss_int(0LL), __ss_int(0LL)), const_20));
        }
        else if (line->startswith(const_21)) {
            b = (line->__slice__(__ss_int(3LL), __ss_int(5LL), __ss_int(7LL), __ss_int(0LL)))->lower();
            if (__ne(b, const_22)) {
                do_move(state, color, parse_move(b));
            }
            color = ((color)^(__ss_int(1LL)));
        }
        else if (line->startswith(const_23)) {
            board = empty_board();
            state = parse_state(board);
            color = __othello2__::BLACK;

            FOR_IN(l,line->split(const_24),27,29,30)
                if ((l)->__contains__(const_25)) {
                    __33 = l->split(const_25);
                    __unpack_check(__33, 2);
                    a = __33->__getfast__(0);
                    b = __33->__getfast__(1);
                    b = (b->lower())->__slice__(__ss_int(2LL), __ss_int(0LL), __ss_int(2LL), __ss_int(0LL));
                    if (__eq(a, const_26)) {
                        if (__ne(b, const_22)) {
                            do_move(state, __othello2__::BLACK, parse_move(b));
                        }
                        color = __othello2__::WHITE;
                    }
                    else if (__eq(a, const_27)) {
                        if (__ne(b, const_22)) {
                            do_move(state, __othello2__::WHITE, parse_move(b));
                        }
                        color = __othello2__::BLACK;
                    }
                }
            END_FOR

        }
        else if (line->startswith(const_28)) {
            max_depth = __int((line->split())->__getfast__(__ss_int(2LL)));
        }
        (__sys__::__ss_stdout)->flush();
    END_FOR

    return NULL;
}

void *vs_cpu_ugi(__ss_int max_depth) {
    str *__38, *board, *c, *hmove, *line;
    list<__ss_int> *state;
    __ss_int __36, __40, __44, blacks, color, move, moves, opp_moves, s, whites;
    list<str *> *__42, *segs;
    file *__34;
    __iter<str *> *__35, *__39, *__43;
    file::for_in_loop __37;
    str::for_in_loop __41;
    list<str *>::for_in_loop __45;

    NODES = __ss_int(0LL);

    FOR_IN(line,__sys__::__ss_stdin,34,36,37)
        line = line->strip();
        if (__eq(line, const_29)) {
            (__sys__::__ss_stdout)->write(const_30);
        }
        else if (__eq(line, const_31)) {
            (__sys__::__ss_stdout)->write(const_32);
        }
        else if (__eq(line, const_33)) {
            board = empty_board();
            state = parse_state(board);
            color = __othello2__::BLACK;
        }
        else if (__eq(line, const_34)) {
            if ((color==__othello2__::BLACK)) {
                (__sys__::__ss_stdout)->write(const_35);
            }
            else {
                (__sys__::__ss_stdout)->write(const_36);
            }
        }
        else if (__eq(line, const_37)) {
            blacks = __int___::bit_count(state->__getfast__(__ss_int(0LL)));
            whites = __int___::bit_count(state->__getfast__(__ss_int(1LL)));
            if ((blacks>whites)) {
                (__sys__::__ss_stdout)->write(const_38);
            }
            else if ((whites>blacks)) {
                (__sys__::__ss_stdout)->write(const_39);
            }
            else {
                (__sys__::__ss_stdout)->write(const_40);
            }
        }
        else if (__eq(line, const_41)) {
            moves = possible_moves(state, color);
            opp_moves = possible_moves(state, ((color)^(__ss_int(1LL))));
            if ((((moves)|(opp_moves))==__ss_int(0LL))) {
                (__sys__::__ss_stdout)->write(const_35);
            }
            else {
                (__sys__::__ss_stdout)->write(const_36);
            }
        }
        else if (line->startswith(const_42)) {
            move = minimax_ab(state, color, __ss_int(0LL), max_depth, True, default_0, default_1);
            (__sys__::__ss_stdout)->write(__mod6(const_43, 1, human_move(move)));
        }
        else if (line->startswith(const_44)) {
            segs = line->split();
            s = __ss_int(1LL);

            while ((s<len(segs))) {
                if (__eq(segs->__getfast__(s), const_45)) {
                    s = (s+__ss_int(1LL));
                    board = const_0;

                    FOR_IN(c,segs->__getfast__(s),38,40,41)
                        if (c->isdigit()) {
                            board = (board)->__iadd__(__mul2(__int(c), const_3));
                        }
                        else if ((const_46)->__contains__(c->lower())) {
                            board = (board)->__iadd__(c->upper());
                        }
                    END_FOR

                    ASSERT(___bool((len(board)==__ss_int(64LL))), 0);
                    state = parse_state(board);
                    s = (s+__ss_int(1LL));
                    color = ((__eq((segs->__getfast__(s))->lower(), const_47))?(__othello2__::BLACK):(__othello2__::WHITE));
                }
                else if (__eq(segs->__getfast__(s), const_48)) {
                    board = empty_board();
                    state = parse_state(board);
                    color = __othello2__::BLACK;
                }
                else if (__eq(segs->__getfast__(s), const_49)) {

                    FOR_IN(hmove,segs->__slice__(__ss_int(1LL), (s+__ss_int(1LL)), __ss_int(0LL), __ss_int(0LL)),42,44,45)
                        if (__ne(hmove, const_49)) {
                            do_move(state, color, parse_move(hmove->lower()));
                            if ((possible_moves(state, ((color)^(__ss_int(1LL))))!=__ss_int(0LL))) {
                                color = ((color)^(__ss_int(1LL)));
                            }
                        }
                    END_FOR

                    break;
                }
                s = (s+__ss_int(1LL));
            }
        }
        (__sys__::__ss_stdout)->flush();
    END_FOR

    return NULL;
}

void *speed_test(__ss_int max_depth) {
    str *board;
    list<__ss_int> *state;
    __ss_int color, move;
    __ss_float t0, t1;

    NODES = __ss_int(0LL);
    board = empty_board();
    state = parse_state(board);
    color = __othello2__::BLACK;
    t0 = __time__::time();
    move = minimax_ab(state, color, __ss_int(0LL), max_depth, True, default_0, default_1);
    t1 = (__time__::time()-t0);
    print(__mod6(const_50, 3, __othello2__::NODES, t1, (__othello2__::NODES/t1)));
    return NULL;
}

void __init() {
    const_0 = new str("");
    const_1 = __char_cache[88];
    const_2 = __char_cache[79];
    const_3 = __char_cache[46];
    const_4 = new str("black: ");
    const_5 = new str(", white: ");
    const_6 = new str("abcdefgh");
    const_7 = new str("...........................OX......XO...........................");
    const_8 = new str("I pass");
    const_9 = new str("(thinking)");
    const_10 = new str("%d nodes in %.2fs seconds (%.2f/second)");
    const_11 = new str("I move here: ");
    const_12 = new str("you pass");
    const_13 = new str("your move? ");
    const_14 = new str("set myname Poppy\n");
    const_15 = new str("go");
    const_16 = new str("=== PASS\n");
    const_17 = new str("=== %s\n");
    const_18 = new str("ping ");
    const_19 = new str("pong ");
    const_20 = __char_cache[10];
    const_21 = new str("move ");
    const_22 = new str("pa");
    const_23 = new str("set game ");
    const_24 = __char_cache[93];
    const_25 = __char_cache[91];
    const_26 = __char_cache[66];
    const_27 = __char_cache[87];
    const_28 = new str("set depth ");
    const_29 = new str("ugi");
    const_30 = new str("ugiok\n");
    const_31 = new str("isready");
    const_32 = new str("readyok\n");
    const_33 = new str("uginewgame");
    const_34 = new str("query p1turn");
    const_35 = new str("response true\n");
    const_36 = new str("response false\n");
    const_37 = new str("query result");
    const_38 = new str("response p1win\n");
    const_39 = new str("response p2win\n");
    const_40 = new str("response draw\n");
    const_41 = new str("query gameover");
    const_42 = new str("go ");
    const_43 = new str("bestmove %s\n");
    const_44 = new str("position");
    const_45 = new str("fen");
    const_46 = new str("ox");
    const_47 = __char_cache[120];
    const_48 = new str("startpos");
    const_49 = new str("moves");
    const_50 = new str("%d nodes in %.2f seconds (%.2f/second)");
    const_51 = new str("__main__");
    const_52 = new str("--depth");
    const_53 = new str("--nboard");
    const_54 = new str("nboard");
    const_55 = new str("--ugi");
    const_56 = new str("--cli");
    const_57 = new str("cli");

    __name__ = new str("__main__");

    BLACK = __ss_int(0LL);
    WHITE = __ss_int(1LL);
    MASKS = (new list<__ss_int>(8,__ss_int(9187201950435737471LL),__ss_int(35887507618889599LL),__ss_int(72057594037927935LL),__ss_int(71775015237779198LL),__ss_int(18374403900871474942LL),__ss_int(18374403900871474688LL),__ss_int(18446744073709551615LL),__ss_int(9187201950435737344LL)));
    CORNER_MASK = __ss_int(9295429630892703873LL);
    WIN_BONUS = (__ss_int(1LL)<<__ss_int(20LL));
    ALPHA_MIN = ((-__ss_int(65LL))*__othello2__::WIN_BONUS);
    BETA_MAX = (__ss_int(65LL)*__othello2__::WIN_BONUS);
    SHIFTS = (new list<__ss_int>(8,__ss_int(1LL),__ss_int(9LL),__ss_int(8LL),__ss_int(7LL),__ss_int(1LL),__ss_int(9LL),__ss_int(8LL),__ss_int(7LL)));
    default_0 = __othello2__::ALPHA_MIN;
    default_1 = __othello2__::BETA_MAX;
    if (__eq(__othello2__::__name__, const_51)) {
        max_depth = __ss_int(10LL);
        mode = NULL;

        FOR_IN_ENUMERATE(arg,(__sys__::argv)->__slice__(__ss_int(1LL), __ss_int(1LL), __ss_int(0LL), __ss_int(0LL)),50,49)
            i = __49;
            if (__eq(__othello2__::arg, const_52)) {
                max_depth = __int((__sys__::argv)->__getfast__((__othello2__::i+__ss_int(2LL))));
            }
            else if (__eq(__othello2__::arg, const_53)) {
                mode = const_54;
            }
            else if (__eq(__othello2__::arg, const_55)) {
                mode = const_29;
            }
            else if (__eq(__othello2__::arg, const_56)) {
                mode = const_57;
            }
        END_FOR

        if (__eq(__othello2__::mode, const_54)) {
            vs_cpu_nboard(__othello2__::max_depth);
        }
        else if (__eq(__othello2__::mode, const_29)) {
            vs_cpu_ugi(__othello2__::max_depth);
        }
        else if (__eq(__othello2__::mode, const_57)) {
            vs_cpu_cli(__othello2__::max_depth);
        }
        else {
            speed_test(__othello2__::max_depth);
        }
    }
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __time__::__init();
    __shedskin__::__start(__othello2__::__init);
}
