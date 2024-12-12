/* Copyright (c) 2009 Jérémie Roquet <arkanosis@gmail.com>; License Expat (See LICENSE) */

#ifndef ITERTOOLS_HPP
#define ITERTOOLS_HPP

#include "builtin.hpp"
#include <cassert>

#define __SS_ALLOC_TUPLES 25

using namespace __shedskin__;

namespace __itertools__ {

/* Local helpers */

template<class T> static bool _identity(T value) {
    return value;
}

/* Infinite Iterators */

// count

template<class T> class countiter : public __iter<T> {
public:
    T counter;
    T step;

    countiter();
    countiter(T start, T step);

    T __next__();
};

template<class T> inline countiter<T>::countiter() {}
template<class T> inline countiter<T>::countiter(T start, T step_) {
    counter = start - step_;
    step = step_;
}

template<class T> inline T countiter<T>::__next__() {
    return this->counter += this->step;
}

template<class T> inline countiter<T> *count(T start, T step) {
    return new countiter<T>(start, step);
}
inline countiter<int> *count(int start = 0) {
    return new countiter<int>(start, 1);
}
inline countiter<__ss_float> *count(__ss_float start, __ss_float step = 1.) {
    return new countiter<__ss_float>(start, step);
}

// accumulate

template<class T> class accumulateiter : public __iter<T> {
    __iter<T> *iter;
    int position;
    T prev;

public:
    T (*func)(T, T);
    bool has_func;
    T initial;
    bool has_initial;

    accumulateiter(pyiter<T> *iterable);

    T __next__();
};

template<class T> inline accumulateiter<T>::accumulateiter(pyiter<T> *iterable) {
    position = 0;
    has_func = false;
    has_initial = false;
    iter = iterable->__iter__();
}

template<class T> T accumulateiter<T>::__next__() {
    if(position++ == 0) {
        if(has_initial)
            prev = initial;
        else
            prev = this->iter->__next__();
        return prev;
    }

    T t = this->iter->__next__();

    if(has_func)
        prev = func(prev, t);
    else
        prev = __add(prev, t);

    return prev;
}

/* no beauty prize for now */

template<class T> inline accumulateiter<T> *accumulate(pyiter<T> *iterable, T(*func)(T, T), T initial) {
    auto acciter = new accumulateiter<T>(iterable);
    acciter->func = func;
    acciter->has_func = True;
    acciter->initial = initial;
    acciter->has_initial = true;
    return acciter;
}
template<class T> inline accumulateiter<T> *accumulate(pyiter<T> *iterable, void *, T initial) {
    auto acciter = new accumulateiter<T>(iterable);
    acciter->initial = initial;
    acciter->has_initial = true;
    return acciter;
}

template<class T> inline accumulateiter<T> *accumulate(pyiter<T> *iterable, T(*func)(T, T), void *v) {
    auto acciter = new accumulateiter<T>(iterable);
    acciter->func = func;
    acciter->has_func = true;
    return acciter;
}
template<class T> inline accumulateiter<T> *accumulate(pyiter<T> *iterable, void *, void *v) {
    return new accumulateiter<T>(iterable);
}

// pairwise

template<class T> class pairwiseiter : public __iter<tuple<T> *> {
    int position;
    __iter<T> *iter;
    T prev;

public:
    pairwiseiter(pyiter<T> *iterable);

    tuple<T> *__next__();
};

template<class T> inline pairwiseiter<T>::pairwiseiter(pyiter<T> *iterable) {
    this->position = 0;
    this->iter = iterable->__iter__();
}

template<class T> tuple<T> *pairwiseiter<T>::__next__() {
    if(position++ == 0)
        prev = this->iter->__next__();
    T t = this->iter->__next__();

    tuple<T> *result = new tuple<T>(0, prev, t);
    prev = t;
    return result;
}

template<class T> inline pairwiseiter<T> *pairwise(pyiter<T> *iterable) {
    return new pairwiseiter<T>(iterable);
}

// cycle

template<class T> class cycleiter : public __iter<T> {
public:
    bool exhausted;
    int position;
    __iter<T> *iter;
    __GC_VECTOR(T) cache;

    cycleiter();
    cycleiter(pyiter<T> *iterable);

    T __next__();
};

template<class T> inline cycleiter<T>::cycleiter() {}
template<class T> inline cycleiter<T>::cycleiter(pyiter<T> *iterable) {
    this->exhausted = false;
    this->position = 0;
    this->iter = iterable->__iter__();
}

template<class T> T cycleiter<T>::__next__() {
    if (!this->exhausted) {
        try  {
            this->cache.push_back(this->iter->__next__());
            return this->cache.back();
        } catch (StopIteration *) {
            if (this->cache.empty())
                throw new StopIteration();
            this->exhausted = true;
        }
    }
    assert(this->cache.size());
    const T& value = this->cache[position];
    this->position = (this->position + 1) % this->cache.size();
    return value;
}

template<class T> inline cycleiter<T> *cycle(pyiter<T> *iterable) {
    return new cycleiter<T>(iterable);
}

// batched

template<class T> class batchediter : public __iter<tuple<T> *> {
public:
    int n;
    int count;
    bool exhausted;
    __ss_bool strict;
    __iter<T> *iter;

    batchediter(pyiter<T> *iterable, __ss_int n, __ss_bool strict);

    tuple<T> *__next__();
};

template<class T> inline batchediter<T>::batchediter(pyiter<T> *iterable, __ss_int n, __ss_bool strict) {
    this->count = 0;
    this->exhausted = false;
    this->n = n;
    this->iter = iterable->__iter__();
    this->strict = strict;
}

template<class T> tuple<T> *batchediter<T>::__next__() {
    if (this->exhausted)
        throw new StopIteration();
    tuple<T> *t = new tuple<T>();
    for(count = 0; count < this->n; count++) {
        try {
            t->units.push_back(iter->__next__());
        } catch (StopIteration *) {
            exhausted = true;
            if(count == 0)
                throw new StopIteration();
            if (this->strict)
                throw new ValueError(new str("batched(): incomplete batch"));
            return t;
        }
    }
    return t;
}

template<class T> inline batchediter<T> *batched(pyiter<T> *iterable, __ss_int n, __ss_bool strict) {
    return new batchediter<T>(iterable, n, strict);
}

// repeat

template<class T> class repeatiter : public __iter<T> {
public:
    T object;
    int times;

    repeatiter();
    repeatiter(T object, int times);

    T __next__();
};

template<class T> inline repeatiter<T>::repeatiter() {}
template<class T> inline repeatiter<T>::repeatiter(T object_, int times_) {
    object = object_;
    times = times_ ? times_ : -1;
}

template<class T> T repeatiter<T>::__next__() {
  if (!times)
    throw new StopIteration();

  if (times > 0)
    --times;

  return object;
}

template<class T> inline repeatiter<T> *repeat(T object, int times = 0) {
    return new repeatiter<T>(object, times);
}

/* Iterators terminating on the shortest input sequence */

// chain

template<class T> class chainiter : public __iter<T> {
public:
    unsigned int iterable;
    __GC_VECTOR(__iter<T> *) iters;

    chainiter();
    chainiter(pyiter<T> *iterable_);

    void push_iter(pyiter<T> *iterable_);

    T __next__();
};

template<class T> inline chainiter<T>::chainiter() {}
template<class T> inline chainiter<T>::chainiter(pyiter<T> *iterable_) {
    iterable = 0;
    push_iter(iterable_);
}
template<class T> void chainiter<T>::push_iter(pyiter<T> *iterable_) {
    iters.push_back(iterable_->__iter__());
}

template<class T> T chainiter<T>::__next__() {
    for (; ; ) {
        try  {
            return this->iters[iterable]->__next__();
        } catch (StopIteration *) {
            if (this->iterable == this->iters.size() - 1)
                throw new StopIteration();
            ++this->iterable;
        }
    }
}

template<class T, class ... Args> inline chainiter<T> *chain(int iterable_count, pyiter<T> *iterable, Args ... args) {
    chainiter<T> *iter = new chainiter<T>(iterable);

    (iter->push_iter(reinterpret_cast<pyiter<T> *>(args)), ...);

    return iter;
}

// compress

template<class T, class B> class compressiter : public __iter<T> {
public:
    __iter<T> *data_iter;
    __iter<B> *selectors_iter;

    compressiter();
    compressiter(pyiter<T> *data, pyiter<B> *selectors);

    T __next__();
};

template<class T, class B> inline compressiter<T, B>::compressiter() {}
template<class T, class B> inline compressiter<T, B>::compressiter(pyiter<T> *data, pyiter<B> *selectors) {
    this->data_iter = data->__iter__();
    this->selectors_iter = selectors->__iter__();
}

template<class T, class B> T compressiter<T, B>::__next__() {
    while (!this->selectors_iter->__next__()) {
        this->data_iter->__next__();
    }
    return this->data_iter->__next__();
}

template<class T, class B> inline compressiter<T, B> *compress(pyiter<T> *data, pyiter<B> *selectors) {
    return new compressiter<T, B>(data, selectors);
}

// dropwhile

template<class T, class B> class dropwhileiter : public __iter<T> {
public:
    bool drop;
    B (*predicate)(T);
    __iter<T> *iter;

    dropwhileiter();
    dropwhileiter(B (*predicate)(T), pyiter<T> *iterable);

    T __next__();
};

template<class T, class B> inline dropwhileiter<T, B>::dropwhileiter() {}
template<class T, class B> inline dropwhileiter<T, B>::dropwhileiter(B (*predicate_)(T), pyiter<T> *iterable) {
    drop = true;
    predicate = predicate_;
    iter = iterable->__iter__();
}

template<class T, class B> T dropwhileiter<T, B>::__next__() {
    if (drop) {
        for (; ; ) {
            const T& value = this->iter->__next__();
            if (!this->predicate(value)) {
                this->drop = false;
                return value;
            }
        }
    }
    return this->iter->__next__();
}

template<class T, class B> inline dropwhileiter<T, B> *dropwhile(B (*predicate)(T), pyiter<T> *iterable) {
    return new dropwhileiter<T, B>(predicate, iterable);
}

// groupby

template<class T, class K> class groupiter;

template<class T, class K> class groupbyiter : public __iter<tuple2<K, __iter<T> *> *> {
public:
    bool first;
    bool skip;
    T current_value;
    K current_key;
    K (*key)(T);
    __iter<T> *iter;

    groupbyiter();
    groupbyiter(pyiter<T> *iterable, K (*key)(T));

    tuple2<K, __iter<T> *> *__next__();

};

template<class T, class K> class groupiter : public __iter<T> {
public:
    bool first;
    groupbyiter<T, K>* iter;

    groupiter();
    groupiter(groupbyiter<T, K>* iter);

    T __next__();
};

template<class T, class K> inline groupiter<T, K>::groupiter() {}
template<class T, class K> inline groupiter<T, K>::groupiter(groupbyiter<T, K>* iter_) {
    first = true;
    iter = iter_;
}

template<class T, class K> T groupiter<T, K>::__next__() {
    if (this->first) {
        this->first = false;
        return this->iter->current_value;
    }

    this->iter->current_value = this->iter->iter->__next__();;
    const K& new_key = this->iter->key(this->iter->current_value);

    if (new_key != this->iter->current_key) {
        this->iter->current_key = new_key;
        this->iter->skip = false;
        throw new StopIteration();
    }

    return this->iter->current_value;
}

template<class T, class K> inline groupbyiter<T, K>::groupbyiter() {}
template<class T, class K> inline groupbyiter<T, K>::groupbyiter(pyiter<T> *iterable, K (*key_)(T)) {
    first = true;
    skip = false;
    key = key_;
    iter = iterable->__iter__();
}

template<class T, class K> tuple2<K, __iter<T> *> *groupbyiter<T, K>::__next__() {
    if (!this->skip) {
        if (this->first) {
            this->current_value = this->iter->__next__();;
            this->current_key = this->key(this->current_value);
            this->first = false;
        }

        this->skip = true;
        return new tuple2<K, __iter<T> *>(2, this->current_key, new groupiter<T, K>(this));
    }

    for (; ; ) {
        this->current_value = this->iter->__next__();
        const K& new_key = this->key(this->current_value);
        if (new_key != this->current_key) {
            this->current_key = new_key;
            return new tuple2<K, __iter<T> *>(2, this->current_key, new groupiter<T, K>(this));
        }
    }
}

template<class T, class K> inline groupbyiter<T, K> *groupby(pyiter<T> *iterable, K (*key)(T)) {
    return new groupbyiter<T, K>(iterable, key);
}

// filterfalse

template<class T, class B> class filterfalseiter : public __iter<T> {
public:
    B (*predicate)(T);
    __iter<T> *iter;

    filterfalseiter();
    filterfalseiter(B (*predicate)(T), pyiter<T> *iterable);

    T __next__();
};

template<class T, class B> inline filterfalseiter<T, B>::filterfalseiter() {}
template<class T, class B> inline filterfalseiter<T, B>::filterfalseiter(B (*predicate_)(T), pyiter<T> *iterable) {
    predicate = predicate_;
    iter = iterable->__iter__();
}

template<class T, class B> T filterfalseiter<T, B>::__next__() {
    for (; ; ) {
        const T& value = this->iter->__next__();
        if (!this->predicate(value)) {
            return value;
        }
    }

    assert(false && "unreachable");
}

template<class T, class B> inline filterfalseiter<T, B> *filterfalse(B (*predicate)(T), pyiter<T> *iterable) {
    return new filterfalseiter<T, B>(predicate, iterable);
}
template<class T> inline filterfalseiter<T, bool> *filterfalse(void * /* null */, pyiter<T> *iterable) {
    return new filterfalseiter<T, bool>(_identity, iterable);
}

// islice

template<class T> class isliceiter : public __iter<T> {
public:
    int current_position;
    int next_position;
    int stop;
    int step;
    __iter<T> *iter;

    isliceiter();
    isliceiter(pyiter<T> *iterable, int start, int stop, int step);

    T __next__();
};

template<class T> inline isliceiter<T>::isliceiter() {}
template<class T> inline isliceiter<T>::isliceiter(pyiter<T> *iterable, int start_, int stop_, int step_) {
    current_position = 0;
    next_position = start_;
    stop = stop_;
    step = step_;
    iter = iterable->__iter__();
}

template<class T> T isliceiter<T>::__next__() {
    if (this->next_position >= this->stop && this->stop != -1)
        throw new StopIteration();

    for (; this->current_position < this->next_position; ++this->current_position) {
        this->iter->__next__();
    }

    ++this->current_position;
    this->next_position += this->step;

    return this->iter->__next__();
}

inline int _start(int start) {
    return start;
}
inline int _start(void*) {
    return 0;
}
inline int _stop(int stop) {
    return stop;
}
inline int _stop(void*) {
    return -1;
}
inline int _step(int step) {
    if (step > 0) {
        return step;
    } else {
        return 1;
    }
}
inline int _step(void*) {
    return 1;
}
template<class T> inline bool _onearg(T /* stop */) {
    return false;
}
template<> inline bool _onearg(__ss_int stop) {
    return stop == -1;
}

template<class T, class U, class V, class W> inline isliceiter<T> *islice(pyiter<T> *iterable, U start, V stop, W step) {
  if (_onearg(stop)) {
      return new isliceiter<T>(iterable, 0, _stop(start), _step(step));
  } else {
      return new isliceiter<T>(iterable, _start(start), _stop(stop), _step(step));
  }
}

// starmap

// TODO

// tee

template<class T> class teecache {
public:
    typedef std::pair<T, int> item;

    int begin;
    int end;
    int clients;
    __GC_DEQUE(item) cache;

    teecache(int clients);

    void add(const T& value);
    T get(int position);
};

template<class T> inline teecache<T>::teecache(int clients_) {
    begin = 0;
    end = 0;
    clients = clients_;
}

template<class T> void teecache<T>::add(const T& value) {
    ++this->end;
    this->cache.push_back(std::make_pair(value, clients));
}

template<class T> T teecache<T>::get(int position) {
    assert(!this->cache.empty());

    while (!this->cache.front().second) {
        ++this->begin;
        this->cache.pop_front();
    }

    --this->cache[position - this->begin].second;
    return this->cache[position - this->begin].first;
}

template<class T> class teeiter : public __iter<T> {
public:
    int position;
    __iter<T> *iter;
    teecache<T> *cache;

    teeiter();
    teeiter(pyiter<T> *iterable, teecache<T> *cache);

    T __next__();
};

template<class T> inline teeiter<T>::teeiter() {}
template<class T> inline teeiter<T>::teeiter(pyiter<T> *iterable, teecache<T> *cache_) {
    position = 0;
    iter = iterable->__iter__();
    cache = cache_;
}

template<class T> T teeiter<T>::__next__() {
    if (this->position == this->cache->end) {
        this->cache->add(this->iter->__next__());
    }

    return this->cache->get(position++);
}

template<class T> inline tuple2<__iter<T> *, __iter<T> *> *tee(pyiter<T> *iterable, int n = 2) {
    teecache<T> *cache = new teecache<T>(n);

    if (n == 2) {
        return new tuple2<__iter<T> *, __iter<T> *>(n, new teeiter<T>(iterable, cache), new teeiter<T>(iterable, cache));
    }

    tuple2<__iter<T> *, __iter<T> *>* tuple = new tuple2<__iter<T> *, __iter<T> *>(1, new teeiter<T>(iterable, cache));

    for (int i = 1; i < n; ++i) {
        tuple->units.push_back(new teeiter<T>(iterable, cache));
    }

    return tuple;
}

// takewhile

template<class T, class B> class takewhileiter : public __iter<T> {
public:
    bool take;
    B (*predicate)(T);
    __iter<T> *iter;

    takewhileiter();
    takewhileiter(B (*predicate)(T), pyiter<T> *iterable);

    T __next__();
};

template<class T, class B> inline takewhileiter<T, B>::takewhileiter() {}
template<class T, class B> inline takewhileiter<T, B>::takewhileiter(B (*predicate_)(T), pyiter<T> *iterable) {
    take = true;
    predicate = predicate_;
    iter = iterable->__iter__();
}

template<class T, class B> T takewhileiter<T, B>::__next__() {
    if (take) {
        const T& value = this->iter->__next__();
        if (this->predicate(value)) {
            return value;
        }
        this->take = false;
    }

    throw new StopIteration();
}

template<class T, class B> inline takewhileiter<T, B> *takewhile(B (*predicate)(T), pyiter<T> *iterable) {
    return new takewhileiter<T, B>(predicate, iterable);
}

// zip_longest

template<class T, class U> class zip_longestiter : public __iter<tuple2<T, U> *> {
public:
    bool exhausted;
    bool first_exhausted;
    bool second_exhausted;
    __iter<T> *first;
    __iter<U> *second;
    T fillvalue;

    zip_longestiter();
    zip_longestiter(T fillvalue, pyiter<T> *iterable1, pyiter<U>* iterable2);

    tuple2<T, U> *__next__();
};

template<class T, class U> inline zip_longestiter<T, U>::zip_longestiter() {
    this->exhausted = true;
}
template<class T, class U> inline zip_longestiter<T, U>::zip_longestiter(T fillvalue_, pyiter<T> *iterable1, pyiter<U> *iterable2) {
    exhausted = false;
    first_exhausted = false;
    second_exhausted = false;
    first = iterable1->__iter__();
    second = iterable2->__iter__();
    fillvalue = fillvalue_;
}

template<class T, class U> tuple2<T, U> *zip_longestiter<T, U>::__next__() {
    if (this->exhausted) {
        throw new StopIteration();
    }

    tuple2<T, U> *tuple = new tuple2<T, U>;

    if (this->first_exhausted) {
        tuple->first = this->fillvalue;
    } else {
        try {
            tuple->first = this->first->__next__();
        } catch (StopIteration *) {
            if (this->second_exhausted) {
                this->exhausted = true;
                throw;
            }
            this->first_exhausted = true;
            tuple->first = this->fillvalue;
        }

        if (this->second_exhausted) {
            tuple->second = (U)this->fillvalue;
            return tuple;
        }
    }

    try {
        tuple->second = this->second->__next__();
    } catch (StopIteration *) {
        if (this->first_exhausted) {
            this->exhausted = true;
            throw;
        }
        this->second_exhausted = true;
        tuple->second = (U)this->fillvalue;
    }

    return tuple;
}

template<class T> class zip_longestiter<T, T> : public __iter<tuple2<T, T> *> {
public:
    unsigned int exhausted;
    std::vector<char> exhausted_iter; // never use std::vector<bool> because this is *slow*
    __GC_VECTOR(__iter<T> *) iters;
    T fillvalue;

    zip_longestiter();
    zip_longestiter(T fillvalue, pyiter<T> *iterable);
    zip_longestiter(T fillvalue, pyiter<T> *iterable, pyiter<T> *iterable2);

    void push_iter(pyiter<T> *iterable);

    tuple2<T, T> *__next__();

};

template<class T> inline zip_longestiter<T, T>::zip_longestiter() {
    this->exhausted = 0;
}
template<class T> inline zip_longestiter<T, T>::zip_longestiter(T fillvalue_, pyiter<T> *iterable) {
    exhausted = 0;
    push_iter(iterable);
    fillvalue = fillvalue_;
}
template<class T> inline zip_longestiter<T, T>::zip_longestiter(T fillvalue_, pyiter<T> *iterable, pyiter<T> *iterable2) {
    exhausted = 0;
    push_iter(iterable);
    push_iter(iterable2);
    fillvalue = fillvalue;
}

template<class T> void zip_longestiter<T, T>::push_iter(pyiter<T> *iterable) {
    iters.push_back(iterable->__iter__());
    exhausted_iter.push_back(0);
}

template<class T> tuple2<T, T> *zip_longestiter<T, T>::__next__() {
    if (this->exhausted == this->iters.size()) {
        throw new StopIteration();
    }

    tuple2<T, T> *tuple = new tuple2<T, T>;
    for (unsigned int i = 0; i < this->iters.size(); ++i) {
        if (!this->exhausted_iter[i]) {
            try  {
                tuple->units.push_back(this->iters[i]->__next__());
                continue;
            } catch (StopIteration *) {
                ++this->exhausted;
                if (this->exhausted == this->iters.size()) {
                    throw;
                }
                this->exhausted_iter[i] = 1;
            }
        }
        tuple->units.push_back(this->fillvalue);
    }

    return tuple;
}

template<class T> inline zip_longestiter<void*, void*> *zip_longest(int /* iterable_count */, T /* fillvalue */) {
    return new zip_longestiter<void*, void*>();
}

template<class T, class F> inline zip_longestiter<T, T> *zip_longest(int iterable_count, F fillvalue, pyiter<T> *iterable) {
    T fv;
    if constexpr (std::is_same_v<F, void *>)
        fv = (T)0;
    else
        fv = (T)fillvalue;
    zip_longestiter<T, T> *iter = new zip_longestiter<T, T>(fv, iterable);
    return iter;
}

template<class T, class U, class F> inline zip_longestiter<T, U> *zip_longest(int iterable_count, F fillvalue, pyiter<T> *iterable1, pyiter<U> *iterable2) {
    T fv;
    if constexpr (std::is_same_v<F, void *>)
        fv = (T)0;
    else
        fv = (T)fillvalue;
  return new zip_longestiter<T, U>(fv, iterable1, iterable2);
}

template<class T, class F, class ... Args> inline zip_longestiter<T, T> *zip_longest(int iterable_count, F fillvalue, pyiter<T> *iterable, pyiter<T> *iterable2, pyiter<T> *iterable3, Args ... args) {
    T fv;
    if constexpr (std::is_same_v<F, void *>)
        fv = (T)0;
    else
        fv = (T)fillvalue;
    zip_longestiter<T, T> *iter = new zip_longestiter<T, T>(fv, iterable);

    iter->push_iter(reinterpret_cast<pyiter<T> *>(iterable2));
    iter->push_iter(reinterpret_cast<pyiter<T> *>(iterable3));
    (iter->push_iter(reinterpret_cast<pyiter<T> *>(args)), ...);

    return iter;
}

/* Combinatoric generators */

// product

template<class T, class U> class productiter : public __iter<tuple2<T, U> *> {
public:
    bool exhausted;
    std::vector<T> values1;
    std::vector<U> values2;
    unsigned int indice1;
    unsigned int indice2;

    tuple2<T, U> *__tuple_cache;
    int __tuple_count; 

    productiter();
    productiter(pyiter<T> *iterable1, pyiter<U> *iterable2);

    tuple2<T, U> *__next__();
};

template<class T, class U> inline productiter<T, U>::productiter() {
    this->__tuple_cache = new tuple2<T,T>[__SS_ALLOC_TUPLES];
    this->__tuple_count = 0; 
}
template<class T, class U> inline productiter<T, U>::productiter(pyiter<T> *iterable1, pyiter<U> *iterable2) {
    this->exhausted = false;
    this->indice1 = 0;
    this->indice2 = 0;

    // TODO this is not optimal at all for pyseq
    // (could be improved with static polymorphism and partial specialization on templates templates)

    #define CACHE_VALUES(TYPE, ID)                            \
        __iter<TYPE> *iter##ID = iterable##ID->__iter__();    \
        for (; ; ) {                                          \
            try {                                             \
                this->values##ID.push_back(iter##ID->__next__()); \
            } catch (StopIteration *) {                       \
                break;                                        \
            }                                                 \
        }                                                     \
        if (this->values##ID.empty()) {                       \
            this->exhausted = true;                           \
            return;                                           \
        }

    CACHE_VALUES(T, 1)
    CACHE_VALUES(U, 2)

    #undef CACHE_VALUES

    this->__tuple_cache = new tuple2<T,U>[__SS_ALLOC_TUPLES];
    this->__tuple_count = 0; 
}

template<class T, class U> tuple2<T, U> *productiter<T, U>::__next__() {
    if (this->exhausted) {
        throw new StopIteration();
    }

    tuple2<T, U> *tuple = &(this->__tuple_cache[this->__tuple_count++]);
    if(this->__tuple_count == __SS_ALLOC_TUPLES) { /* XXX make this more generic? */
        this->__tuple_count = 0;
        this->__tuple_cache = new tuple2<T,U>[__SS_ALLOC_TUPLES];
    }

    tuple->first = this->values1[this->indice1];
    tuple->second = this->values2[this->indice2];

    ++this->indice2;
    if (this->indice2 == this->values2.size()) {
        this->indice2 = 0;

        ++this->indice1;
        if (this->indice1 == this->values1.size()) {
            this->exhausted = true;
        }
    }

    return tuple;
}

template<class T> class productiter<T, T> : public __iter<tuple2<T, T> *> {
public:
    bool exhausted;
    unsigned int highest_exhausted;
    std::vector<std::vector<T> > values;
    std::vector<unsigned int> iter;
    std::vector<unsigned int> indices;

    tuple2<T, T> *__tuple_cache;
    int __tuple_count; 

    productiter();

    void push_iter(pyiter<T> *iterable);
    void repeat(int times);

    tuple2<T, T> *__next__();

};

template<class T> inline productiter<T, T>::productiter() {
    this->exhausted = false;
    this->highest_exhausted = 0;

    this->__tuple_cache = new tuple2<T,T>[__SS_ALLOC_TUPLES];
    this->__tuple_count = 0; 
}

template<class T> void productiter<T, T>::push_iter(pyiter<T> *iterable) {
    this->values.push_back(std::vector<T>());
    this->indices.push_back(0);

    // TODO this is not optimal at all for pyseq
    // (could be improved with static polymorphism and partial specialization on templates templates)
    __iter<T> *iter_ = iterable->__iter__();
    for (; ; ) {
        try {
            this->values.back().push_back(iter_->__next__());
        } catch (StopIteration *) {
            break;
        }
    }

    if (!this->values.back().size()) {
        this->exhausted = true;
    } else if (this->values.back().size() == 1 && this->highest_exhausted == this->values.size() - 1) {
        ++this->highest_exhausted;
    }
}

template<class T> inline void productiter<T, T>::repeat(int times) {
    if (this->highest_exhausted == this->values.size()) {
      this->highest_exhausted *= times;
    }

    for (int time = 0; time < times; ++time) {
        for (unsigned int iter_ = 0; iter_ < this->values.size(); ++iter_) {
            this->iter.push_back(iter_);
            this->indices.push_back(0);
        }
    }
}

template<class T> tuple2<T, T> *productiter<T, T>::__next__() {
    if (this->exhausted) {
        throw new StopIteration();
    }

    tuple2<T, T> *tuple = &(this->__tuple_cache[this->__tuple_count++]);
    if(this->__tuple_count == __SS_ALLOC_TUPLES) { /* XXX make this more generic? */
        this->__tuple_count = 0;
        this->__tuple_cache = new tuple2<T,T>[__SS_ALLOC_TUPLES];
    } 

    if (this->iter.size()) {
        size_t iter_size = this->iter.size();
        tuple->units.resize(iter_size);
        for (size_t i = 0; i < iter_size; ++i) {
            size_t j = (size_t)(this->iter[i]);
            tuple->units[i] = this->values[j][this->indices[i]];
        }
        for (size_t i = this->iter.size() - 1; i != std::string::npos; --i) {
            size_t j = (size_t)(this->iter[i]);
            ++this->indices[i];
            if (i <= (size_t)this->highest_exhausted) {
                if (this->indices[i] >= this->values[j].size() - 1) {
                    ++this->highest_exhausted;
                    if (this->highest_exhausted > this->iter.size()) {
                        this->exhausted = true;
                    }
                    break;
                }
            }
            if (this->indices[i] == this->values[j].size()) {
                this->indices[i] = 0;
            } else {
                break;
            }
        }
    } else {
        this->exhausted = true;
    }

    return tuple;
}

inline productiter<void*, void*> *product(int /* iterable_count */, int /* repeat */) {
    return new productiter<void*, void*>();
}

template<class T> inline productiter<T, T> *product(int /* iterable_count */, int repeat, pyiter<T> *iterable) {
    productiter<T, T> *iter = new productiter<T, T>();
    iter->push_iter(iterable);
    iter->repeat(repeat);
    return iter;
}


template<class T> inline productiter<T, T> *product(int /* iterable_count */, int repeat, pyiter<T> *iterable1, pyiter<T> *iterable2) {
    productiter<T, T> *iter = new productiter<T, T>();

    iter->push_iter(iterable1);
    iter->push_iter(iterable2);

    iter->repeat(repeat);

    return iter;
}
template<class T, class U> inline productiter<T, U> *product(int /* iterable_count */, int /* repeat */, pyiter<T> *iterable1, pyiter<U> *iterable2) {
    return new productiter<T, U>(iterable1, iterable2);
}
template<class T, class ... Args> inline productiter<T, T> *product(
    int iterable_count, int repeat, pyiter<T> *iterable, pyiter<T> *iterable2, pyiter<T> *iterable3, Args ... args
) {
    productiter<T, T> *iter = new productiter<T, T>();

    iter->push_iter(iterable);
    iter->push_iter(iterable2);
    iter->push_iter(iterable3);
    (iter->push_iter(reinterpret_cast<pyiter<T> *>(args)), ...);

    iter->repeat(repeat);

    return iter;
}

// permutations

template<class T> class permutationsiter : public __iter<tuple2<T, T> *> {
public:
    int r;
    int len;
    int current;
    unsigned int* indices;
    unsigned int* cycles;
    std::vector<T> cache;

    permutationsiter();
    permutationsiter(pyiter<T> *iterable, __ss_int r);

    ~permutationsiter();

    tuple2<T, T> *__next__();

private: // We might want to implement this, but we certainly don't want the default ones
    permutationsiter(const permutationsiter& other);
    permutationsiter<T>& operator=(const permutationsiter& other);
};

template<class T> inline permutationsiter<T>::permutationsiter() {
    this->indices = 0;
    this->cycles = 0;
}
template<class T> inline permutationsiter<T>::permutationsiter(pyiter<T> *iterable, __ss_int r_) {
    this->r = r_;
    this->len = 0;

    // TODO this is not optimal at all for pyseq
    // (could be improved with static polymorphism and partial specialization on templates templates)
    __iter<T> *iter = iterable->__iter__();
    for (; ; ) {
        try  {
            this->cache.push_back(iter->__next__());
        } catch (StopIteration *) {
            break;
        }
    }
    this->len = this->cache.size();

    if (r_ > this->len) {
        this->current = -1;
        this->indices = 0;
        this->cycles = 0;
    } else {
        this->current = this->r;
        this->indices = new unsigned int[this->len];
        this->cycles = new unsigned int[this->r];

        for (int i = 0; i < this->len; ++i) {
            this->indices[i] = i;
        }
        for (int i = 0; i < this->r; ++i) {
            this->cycles[i] = this->len - i;
        }
    }
}

template<class T> inline permutationsiter<T>::~permutationsiter() {
    delete[] this->indices;
    delete[] this->cycles;
}

template<class T> tuple2<T, T> *permutationsiter<T>::__next__() {
    if (this->current == this->r) {
        tuple2<T, T> *tuple = new tuple2<T, T>;
        for (int i = 0; i < this->r; ++i) {
            tuple->units.push_back(this->cache[i]);
        }
        --this->current;
        return tuple;
    }

    for (; ; ) {
        if (this->current == -1) {
            throw new StopIteration();
        }

        int cycle = --this->cycles[this->current];
        if (cycle) {
            assert(this->current < this->len);
            std::swap(this->indices[this->current], this->indices[cycle ? this->len - cycle : 0]);
            tuple2<T, T> *tuple = new tuple2<T, T>;
            for (int i = 0; i < this->r; ++i) {
                tuple->units.push_back(this->cache[this->indices[i]]);
            }
            this->current = this->r - 1;
            return tuple;
        } else {
            int last = this->indices[this->current];
            for (int i = this->current; i < this->len - 1; ++i) {
                this->indices[i] = this->indices[i + 1];
            }
            this->indices[this->len - 1] = last;
            this->cycles[this->current] = this->len - this->current;
            --this->current;
        }
    }
}

template<class T> inline permutationsiter<T> *permutations(pyiter<T> *iterable, void* /* r */) {
    return new permutationsiter<T>(iterable, iterable->__len__());
}
template<class T> inline permutationsiter<T> *permutations(pyiter<T> *iterable, __ss_int r) {
    return new permutationsiter<T>(iterable, r);
}

// combinations

template<class T> class combinationsiter : public __iter<tuple2<T, T> *> {
public:
    int r;
    int len;
    int current;
    int* indices;
    __GC_VECTOR(T) cache;

    combinationsiter();
    combinationsiter(pyiter<T> *iterable, int r);

    ~combinationsiter();

    tuple2<T, T> *__next__();

private: // We might want to implement this, but we certainly don't want the default ones
    combinationsiter(const combinationsiter& other);
    combinationsiter<T>& operator=(const combinationsiter& other);
};

template<class T> inline combinationsiter<T>::combinationsiter() {
    this->indices = 0;
}
template<class T> inline combinationsiter<T>::combinationsiter(pyiter<T> *iterable, int r_) {
    this->r = r_;
    this->len = 0;

    // TODO this is not optimal at all for pyseq
    // (could be improved with static polymorphism and partial specialization on templates templates)
    __iter<T> *iter_ = iterable->__iter__();
    for (; ; ) {
        try  {
            this->cache.push_back(iter_->__next__());
        } catch (StopIteration *) {
            break;
        }
    }
    this->len = this->cache.size();

    if (r_ > this->len) {
        this->current = -1;
        this->indices = 0;
    } else {
        this->current = r_;
        this->indices = new int[r_];

        for (int i = 0; i < this->r; ++i) {
            this->indices[i] = i;
        }
    }
}

template<class T> inline combinationsiter<T>::~combinationsiter() {
    delete[] this->indices;
}

template<class T> tuple2<T, T> *combinationsiter<T>::__next__() {
    if (this->current == this->r) {
        tuple2<T, T> *tuple = new tuple2<T, T>;
        for (int i = 0; i < this->r; ++i) {
            tuple->units.push_back(this->cache[i]);
        }
        --this->current;
        return tuple;
    }

    for (; ; ) {
        if (this->current == -1) {
            throw new StopIteration();
        }

        while (this->indices[this->current] == this->current + this->len - this->r) {
            --this->current;

            if (this->current == -1) {
                throw new StopIteration();
            }
        }


        ++this->indices[this->current];
        for (int i = this->current + 1; i < this->r; ++i) {
            this->indices[i] = this->indices[i - 1] + 1;
        }

        tuple2<T, T> *tuple = new tuple2<T, T>;
        for (int i = 0; i < this->r; ++i) {
            tuple->units.push_back(this->cache[this->indices[i]]);
        }

        this->current = this->r - 1;

        return tuple;
    }
}

template<class T> inline combinationsiter<T> *combinations(pyiter<T> *iterable, int r) {
    return new combinationsiter<T>(iterable, r);
}

// combinations_with_replacement

template<class T> class combinations_with_replacementiter : public __iter<tuple2<T, T> *> {
public:
    int r;
    int len;
    int current;
    int* indices;
    __GC_VECTOR(T) cache;

    combinations_with_replacementiter();
    combinations_with_replacementiter(pyiter<T> *iterable, int r);

    ~combinations_with_replacementiter();

    tuple2<T, T> *__next__();

private: // We might want to implement this, but we certainly don't want the default ones
    combinations_with_replacementiter(const combinations_with_replacementiter& other);
    combinations_with_replacementiter<T>& operator=(const combinations_with_replacementiter& other);
};

template<class T> inline combinations_with_replacementiter<T>::combinations_with_replacementiter() {
    this->indices = 0;
}
template<class T> inline combinations_with_replacementiter<T>::combinations_with_replacementiter(pyiter<T> *iterable, int r_) {
    this->r = r_;
    this->len = 0;

    // TODO this is not optimal at all for pyseq
    // (could be improved with static polymorphism and partial specialization on templates templates)
    __iter<T> *iter = iterable->__iter__();
    for (; ; ) {
        try  {
            this->cache.push_back(iter->__next__());
        } catch (StopIteration *) {
            break;
        }
    }
    this->len = this->cache.size();

    if (!this->len && r_) {
        this->current = -1;
        this->indices = 0;
    } else {
        this->current = r_;
        this->indices = new int[r_];

        for (int i = 0; i < this->r; ++i) {
            this->indices[i] = 0;
        }
    }
}

template<class T> inline combinations_with_replacementiter<T>::~combinations_with_replacementiter() {
    delete[] this->indices;
}

template<class T> tuple2<T, T> *combinations_with_replacementiter<T>::__next__() {
    if (this->current == this->r) {
        tuple2<T, T> *tuple = new tuple2<T, T>;
        for (int i = 0; i < this->r; ++i) {
            tuple->units.push_back(this->cache[0]);
        }
        --this->current;
        return tuple;
    }

    for (; ; ) {
        if (this->current == -1) {
            throw new StopIteration();
        }

        while (this->indices[this->current] == this->len - 1) {
            --this->current;

            if (this->current == -1) {
                throw new StopIteration();
            }
        }

        ++this->indices[this->current];
        for (int i = this->current + 1; i < this->r; ++i) {
            this->indices[i] = this->indices[this->current];
        }

        tuple2<T, T> *tuple = new tuple2<T, T>;
        for (int i = 0; i < this->r; ++i) {
            tuple->units.push_back(this->cache[this->indices[i]]);
        }

        this->current = this->r - 1;

        return tuple;
    }
}

template<class T> inline combinations_with_replacementiter<T> *combinations_with_replacement(pyiter<T> *iterable, int r) {
    return new combinations_with_replacementiter<T>(iterable, r);
}

void __init();

} // module namespace
#endif
