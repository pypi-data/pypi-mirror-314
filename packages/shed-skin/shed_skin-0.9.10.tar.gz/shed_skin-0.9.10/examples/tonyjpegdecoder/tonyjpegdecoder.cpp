#include "builtin.hpp"
#include "tonyjpegdecoder.hpp"

/**
Based on C++ code by Dr. Tony Lin:
*****************************************************************************
*    Author:            Dr. Tony Lin                                        *
*    Email:            lintong@cis.pku.edu.cn                               *
*    Release Date:    Dec. 2002                                             *
*                                                                           *
*    Name:            TonyJpegLib, rewritten from IJG codes                 *
*    Source:            IJG v.6a JPEG LIB                                   *
*    Purpose:        Support real jpeg file, with readable code             *
*                                                                           *
*    Acknowlegement:    Thanks for great IJG, and Chris Losinger            *
*                                                                           *
*    Legal Issues:    (almost same as IJG with followings)                  *
*                                                                           *
*    1. We don't promise that this software works.                          *
*    2. You can use this software for whatever you want.                    *
*    You don't have to pay.                                                 *
*    3. You may not pretend that you wrote this software. If you use it     *
*    in a program, you must acknowledge somewhere. That is, please          *
*    metion IJG, and Me, Dr. Tony Lin.                                      *
*                                                                           *
*****************************************************************************
*/

namespace __tonyjpegdecoder__ {

bytes *const_0, *const_1, *const_17, *const_18, *const_19, *const_2;
str *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;


str *__name__;
__ss_int M_APP0, M_APP1, M_APP10, M_APP11, M_APP12, M_APP13, M_APP14, M_APP15, M_APP2, M_APP3, M_APP4, M_APP5, M_APP6, M_APP7, M_APP8, M_APP9, M_COM, M_DAC, M_DHP, M_DHT, M_DNL, M_DQT, M_DRI, M_EOI, M_ERROR, M_EXP, M_JPG, M_JPG0, M_JPG13, M_RST0, M_RST1, M_RST2, M_RST3, M_RST4, M_RST5, M_RST6, M_RST7, M_SOF0, M_SOF1, M_SOF10, M_SOF11, M_SOF13, M_SOF14, M_SOF15, M_SOF2, M_SOF3, M_SOF5, M_SOF6, M_SOF7, M_SOF9, M_SOI, M_SOS, M_TEM;
list<__ss_int> *jpeg_natural_order;


static inline list<__ss_int> *list_comp_0(list<__ss_int> *tblAan, __ss_int half, dict<__ss_int, __ss_int> *tblStd);
static inline list<__ss_int> *list_comp_1(TonyJpegDecoder *self);
static inline list<bytes *> *list_comp_2(bytes *bmpstr);
static inline list<bytes *> *list_comp_3(list<__ss_int> *bmpout);
static inline __ss_int __lambda0__(__ss_float x, __ss_int n);
static inline __ss_int __lambda1__(__ss_int var, __ss_int cons);
static inline __ss_int __lambda2__(__ss_int x, __ss_int n);

static inline list<__ss_int> *list_comp_0(list<__ss_int> *tblAan, __ss_int half, dict<__ss_int, __ss_int> *tblStd) {
    __ss_int __17, __18, i;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    FAST_FOR(i,0,__ss_int(64),1,17,18)
        __ss_result->append((((tblStd->__getitem__(i)*tblAan->__getfast__(i))+half)>>__ss_int(12)));
    END_FOR

    return __ss_result;
}

static inline list<__ss_int> *list_comp_1(TonyJpegDecoder *self) {
    __ss_int __56, __57, i;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    FAST_FOR(i,0,(self->BlocksInMcu-__ss_int(2)),1,56,57)
        __ss_result->append((i*__ss_int(64)));
    END_FOR

    return __ss_result;
}

static inline list<bytes *> *list_comp_2(bytes *bmpstr) {
    __ss_int __74, __75, i;

    list<bytes *> *__ss_result = new list<bytes *>();

    FAST_FOR(i,0,__floordiv(len(bmpstr),__ss_int(3)),1,74,75)
        __ss_result->append(__mod6(const_0, 3, bmpstr->__getitem__(((i*__ss_int(3))+__ss_int(2))), bmpstr->__getitem__(((i*__ss_int(3))+__ss_int(1))), bmpstr->__getitem__((i*__ss_int(3)))));
    END_FOR

    return __ss_result;
}

static inline list<bytes *> *list_comp_3(list<__ss_int> *bmpout) {
    __ss_int __78, x;
    list<__ss_int> *__76;
    __iter<__ss_int> *__77;
    list<__ss_int>::for_in_loop __79;

    list<bytes *> *__ss_result = new list<bytes *>();

    __ss_result->resize(len(bmpout));
    FOR_IN(x,bmpout,76,78,79)
        __ss_result->units[__78] = __mod6(const_1, 1, x);
    END_FOR

    return __ss_result;
}

static inline __ss_int __lambda0__(__ss_float x, __ss_int n) {
    return __int(((x*n)+__ss_float(0.5)));
}

static inline __ss_int __lambda1__(__ss_int var, __ss_int cons) {
    return (__int((var*cons))>>__ss_int(8));
}

static inline __ss_int __lambda2__(__ss_int x, __ss_int n) {
    return (x>>n);
}

/**
class jpeg_component_info
*/

class_ *cl_jpeg_component_info;

void jpeg_component_info::__static__() {
}

/**
class HUFFTABLE
*/

class_ *cl_HUFFTABLE;

void *HUFFTABLE::__init__() {
    this->mincode = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(17));
    this->maxcode = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(18));
    this->valptr = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(17));
    this->bits = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(17));
    this->huffval = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(256));
    this->look_nbits = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(256));
    this->look_sym = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(256));
    return NULL;
}

void *HUFFTABLE::ComputeHuffmanTable() {
    /**
    Compute the derived values for a Huffman table.
    */
    __ss_int HUFF_LOOKAHEAD, __0, __1, __11, __12, __13, __14, __2, __3, __4, __5, code, ctr, i, l, lookbits, p, si;
    list<__ss_int> *__10, *__15, *__16, *__6, *__7, *__8, *__9, *huffcode, *huffsize;

    p = __ss_int(0);
    huffsize = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(257));
    huffcode = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(257));

    FAST_FOR(l,__ss_int(1),__ss_int(17),1,0,1)

        FAST_FOR(i,__ss_int(1),((this->bits)->__getfast__(l)+__ss_int(1)),1,2,3)
            huffsize->__setitem__(p, l);
            p = (p+__ss_int(1));
        END_FOR

    END_FOR

    huffsize->__setitem__(p, __ss_int(0));
    code = __ss_int(0);
    si = huffsize->__getfast__(__ss_int(0));
    p = __ss_int(0);

    while (huffsize->__getfast__(p)) {

        while ((huffsize->__getfast__(p)==si)) {
            huffcode->__setitem__(p, code);
            code = (code+__ss_int(1));
            p = (p+__ss_int(1));
        }
        code = (code<<__ss_int(1));
        si = (si+__ss_int(1));
    }
    p = __ss_int(0);

    FAST_FOR(l,__ss_int(1),__ss_int(17),1,4,5)
        if ((this->bits)->__getfast__(l)) {
            this->valptr->__setitem__(l, p);
            this->mincode->__setitem__(l, huffcode->__getfast__(p));
            p = (p+(this->bits)->__getfast__(l));
            this->maxcode->__setitem__(l, huffcode->__getfast__((p-__ss_int(1))));
        }
        else {
            this->maxcode->__setitem__(l, (-__ss_int(1)));
        }
    END_FOR

    this->maxcode->__setitem__(__ss_int(17), __ss_int(1048575));
    this->look_nbits = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(256));
    HUFF_LOOKAHEAD = __ss_int(8);
    p = __ss_int(0);

    FAST_FOR(l,__ss_int(1),(HUFF_LOOKAHEAD+__ss_int(1)),1,11,12)

        FAST_FOR(i,__ss_int(1),((this->bits)->__getfast__(l)+__ss_int(1)),1,13,14)
            lookbits = (huffcode->__getfast__(p)<<(HUFF_LOOKAHEAD-l));
            ctr = (__ss_int(1)<<(HUFF_LOOKAHEAD-l));

            while ((ctr>__ss_int(0))) {
                this->look_nbits->__setitem__(lookbits, l);
                this->look_sym->__setitem__(lookbits, (this->huffval)->__getfast__(p));
                lookbits = (lookbits+__ss_int(1));
                ctr = (ctr-__ss_int(1));
            }
            p = (p+__ss_int(1));
        END_FOR

    END_FOR

    return NULL;
}

list<__ss_int> *ScaleQuantTable(dict<__ss_int, __ss_int> *tblStd, list<__ss_int> *tblAan) {
    __ss_int half;

    half = (__ss_int(1)<<__ss_int(11));
    return list_comp_0(tblAan, half, tblStd);
}

/**
class TonyJpegDecoder
*/

class_ *cl_TonyJpegDecoder;

void *TonyJpegDecoder::__init__() {
    /**
    set up the decoder
    */
    this->Quality = __ss_int(0);
    this->Scale = __ss_int(0);
    this->tblRange = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(((__ss_int(5)*__ss_int(256))+__ss_int(128)));
    this->CrToR = (new dict<__ss_int, __ss_int>());
    this->CrToG = (new dict<__ss_int, __ss_int>());
    this->CbToB = (new dict<__ss_int, __ss_int>());
    this->CbToG = (new dict<__ss_int, __ss_int>());
    this->qtblY_dict = (new dict<__ss_int, __ss_int>());
    this->qtblCbCr_dict = (new dict<__ss_int, __ss_int>());
    this->htblYDC = (new HUFFTABLE(1));
    this->htblYAC = (new HUFFTABLE(1));
    this->htblCbCrDC = (new HUFFTABLE(1));
    this->htblCbCrAC = (new HUFFTABLE(1));
    this->Width = __ss_int(0);
    this->Height = __ss_int(0);
    this->McuSize = __ss_int(0);
    this->BlocksInMcu = __ss_int(0);
    this->dcY = __ss_int(0);
    this->dcCb = __ss_int(0);
    this->dcCr = __ss_int(0);
    this->GetBits = __ss_int(0);
    this->GetBuff = __ss_int(0);
    this->DataBytesLeft = __ss_int(0);
    this->Data = const_2;
    this->DataPos = __ss_int(0);
    this->Precision = __ss_int(0);
    this->Component = __ss_int(0);
    this->restart_interval = __ss_int(0);
    this->restarts_to_go = __ss_int(0);
    this->unread_marker = __ss_int(0);
    this->next_restart_num = __ss_int(0);
    this->comp_info = (new list<jpeg_component_info *>(3,(new jpeg_component_info()),(new jpeg_component_info()),(new jpeg_component_info())));
    return NULL;
}

void *TonyJpegDecoder::ReadJpgHeader(bytes *jpegsrc) {
    /**
    reads Width, Height, headsize
    */
    __ss_bool __19, __20;

    this->read_markers(jpegsrc);
    if (((this->Width<=__ss_int(0)) or (this->Height<=__ss_int(0)))) {
        throw ((new ValueError(const_3)));
    }
    print(__mod6(const_4, 2, this->Width, this->Height));
    this->DataBytesLeft = (len(jpegsrc)-this->DataPos);
    this->InitDecoder();
    return NULL;
}

__ss_int TonyJpegDecoder::ReadByte() {
    __ss_int byte;

    byte = (this->Data)->__getitem__(this->DataPos);
    this->DataPos = (this->DataPos+__ss_int(1));
    return byte;
}

__ss_int TonyJpegDecoder::ReadWord() {
    __ss_int byte1, byte2;
    bytes *__21;

    __21 = (this->Data)->__slice__(__ss_int(3), this->DataPos, (this->DataPos+__ss_int(2)), __ss_int(0));
    __unpack_check(__21, 2);
    byte1 = __21->__getitem__(0);
    byte2 = __21->__getitem__(1);
    this->DataPos = (this->DataPos+__ss_int(2));
    return ((byte1<<__ss_int(8))+byte2);
}

__ss_int TonyJpegDecoder::ReadOneMarker() {
    /**
    read exact marker, two bytes, no stuffing allowed
    */
    if ((this->ReadByte()!=__ss_int(255))) {
        throw ((new ValueError(const_5)));
    }
    return this->ReadByte();
}

void *TonyJpegDecoder::SkipMarker() {
    /**
    Skip over an unknown or uninteresting variable-length marker
    */
    __ss_int length;

    length = this->ReadWord();
    print(const_6, length);
    this->DataPos = (this->DataPos+(length-__ss_int(2)));
    return NULL;
}

void *TonyJpegDecoder::GetDqt() {
    __ss_int __22, __23, i, length, n, prec;
    dict<__ss_int, __ss_int> *qtb;

    length = (this->ReadWord()-__ss_int(2));

    while ((length>__ss_int(0))) {
        n = this->ReadByte();
        length = (length-__ss_int(1));
        prec = (n>>__ss_int(4));
        n = ((n)&(__ss_int(15)));
        if ((n==__ss_int(0))) {
            qtb = this->qtblY_dict;
        }
        else {
            qtb = this->qtblCbCr_dict;
        }

        FAST_FOR(i,0,__ss_int(64),1,22,23)
            qtb->__setitem__(__tonyjpegdecoder__::jpeg_natural_order->__getfast__(i), this->ReadByte());
        END_FOR

        length = (length-__ss_int(64));
    }
    return NULL;
}

void *TonyJpegDecoder::get_sof(__ss_bool is_prog, __ss_bool is_arith) {
    /**
    get Width and Height, and component info
    */
    __ss_int __24, __25, c, ci, length;
    jpeg_component_info *comp;
    __ss_bool __26, __27, __29, __30;
    list<jpeg_component_info *> *__28;

    length = this->ReadWord();
    this->Precision = this->ReadByte();
    this->Height = this->ReadWord();
    this->Width = this->ReadWord();
    this->Component = this->ReadByte();
    length = (length-__ss_int(8));

    FAST_FOR(ci,0,this->Component,1,24,25)
        comp = (new jpeg_component_info());
        comp->component_index = ci;
        comp->component_id = this->ReadByte();
        c = this->ReadByte();
        comp->h_samp_factor = (((c>>__ss_int(4)))&(__ss_int(15)));
        comp->v_samp_factor = ((c)&(__ss_int(15)));
        if (((ci==__ss_int(0)) and (c!=__ss_int(34)))) {
            print(__mod6(const_7, 1, c));
        }
        comp->quant_tbl_no = this->ReadByte();
        this->comp_info->__setitem__(ci, comp);
    END_FOR

    if (((((this->comp_info)->__getfast__(__ss_int(0)))->h_samp_factor==__ss_int(1)) and (((this->comp_info)->__getfast__(__ss_int(0)))->v_samp_factor==__ss_int(1)))) {
        this->McuSize = __ss_int(8);
        this->BlocksInMcu = __ss_int(3);
    }
    else {
        this->McuSize = __ss_int(16);
        this->BlocksInMcu = __ss_int(6);
    }
    return NULL;
}

void *TonyJpegDecoder::get_dht() {
    __ss_int __32, __33, __35, __36, count, i, index, length;
    HUFFTABLE *htbl;
    list<__ss_int> *__31, *__34, *__37;

    length = (this->ReadWord()-__ss_int(2));

    while ((length>__ss_int(0))) {
        index = this->ReadByte();
        htbl = (new HUFFTABLE(1));
        count = __ss_int(0);
        htbl->bits->__setitem__(__ss_int(0), __ss_int(0));

        FAST_FOR(i,__ss_int(1),__ss_int(17),1,32,33)
            htbl->bits->__setitem__(i, this->ReadByte());
            count = (count+(htbl->bits)->__getfast__(i));
        END_FOR


        FAST_FOR(i,0,count,1,35,36)
            htbl->huffval->__setitem__(i, this->ReadByte());
        END_FOR

        length = (length-(count+__ss_int(17)));
        if ((index==__ss_int(0))) {
            this->htblYDC = htbl;
        }
        else if ((index==__ss_int(16))) {
            this->htblYAC = htbl;
        }
        else if ((index==__ss_int(1))) {
            this->htblCbCrDC = htbl;
        }
        else if ((index==__ss_int(17))) {
            this->htblCbCrAC = htbl;
        }
    }
    return NULL;
}

void *TonyJpegDecoder::get_sos() {
    __ss_int Ah, Al, Se, Ss, __38, __39, c, cc, ci, i, length, n;

    length = this->ReadWord();
    n = this->ReadByte();
    cc = __ss_int(0);
    c = __ss_int(0);
    ci = __ss_int(0);

    FAST_FOR(i,0,n,1,38,39)
        cc = this->ReadByte();
        c = this->ReadByte();
    END_FOR

    Ss = this->ReadByte();
    Se = this->ReadByte();
    c = this->ReadByte();
    Ah = (((c>>__ss_int(4)))&(__ss_int(15)));
    Al = ((c)&(__ss_int(15)));
    this->next_restart_num = __ss_int(0);
    return NULL;
}

void *TonyJpegDecoder::get_dri() {
    this->length = this->ReadWord();
    this->restart_interval = this->ReadWord();
    this->restarts_to_go = this->restart_interval;
    print(__mod6(const_8, 1, this->restart_interval));
    return NULL;
}

void *TonyJpegDecoder::read_markers(bytes *inbuf) {
    /**
    raises an error or returns if successfull
    */
    __ss_int __40, __41, marker, retval;

    this->Data = inbuf;

    while (True) {
        marker = this->ReadOneMarker();
        print(__mod6(const_9, 1, marker));
        if ((marker==__tonyjpegdecoder__::M_SOI)) {
        }
        else if (((new tuple<__ss_int>(16,__tonyjpegdecoder__::M_APP0,__tonyjpegdecoder__::M_APP1,__tonyjpegdecoder__::M_APP2,__tonyjpegdecoder__::M_APP3,__tonyjpegdecoder__::M_APP4,__tonyjpegdecoder__::M_APP5,__tonyjpegdecoder__::M_APP6,__tonyjpegdecoder__::M_APP7,__tonyjpegdecoder__::M_APP8,__tonyjpegdecoder__::M_APP9,__tonyjpegdecoder__::M_APP10,__tonyjpegdecoder__::M_APP11,__tonyjpegdecoder__::M_APP12,__tonyjpegdecoder__::M_APP13,__tonyjpegdecoder__::M_APP14,__tonyjpegdecoder__::M_APP15)))->__contains__(marker)) {
            this->SkipMarker();
        }
        else if ((marker==__tonyjpegdecoder__::M_DQT)) {
            this->GetDqt();
        }
        else if (((new tuple<__ss_int>(2,__tonyjpegdecoder__::M_SOF0,__tonyjpegdecoder__::M_SOF1)))->__contains__(marker)) {
            this->get_sof(False, False);
        }
        else if ((marker==__tonyjpegdecoder__::M_SOF2)) {
            throw ((new ValueError(const_10)));
        }
        else if ((marker==__tonyjpegdecoder__::M_SOF9)) {
            throw ((new ValueError(const_11)));
        }
        else if ((marker==__tonyjpegdecoder__::M_SOF10)) {
            throw ((new ValueError(const_12)));
        }
        else if ((marker==__tonyjpegdecoder__::M_DHT)) {
            this->get_dht();
        }
        else if ((marker==__tonyjpegdecoder__::M_SOS)) {
            this->get_sos();
            retval = __ss_int(0);
            return NULL;
        }
        else if ((marker==__tonyjpegdecoder__::M_COM)) {
            this->SkipMarker();
        }
        else if ((marker==__tonyjpegdecoder__::M_DRI)) {
            this->get_dri();
        }
        else {
            throw ((new ValueError(__mod6(const_13, 1, marker))));
        }
        this->unread_marker = __ss_int(0);
    }
    return 0;
}

void *TonyJpegDecoder::read_restart_marker() {
    if ((this->unread_marker==__ss_int(0))) {
        this->unread_marker = this->ReadOneMarker();
    }
    if ((this->unread_marker==(__tonyjpegdecoder__::M_RST0+this->next_restart_num))) {
        this->unread_marker = __ss_int(0);
    }
    else {
    }
    this->next_restart_num = (((this->next_restart_num+__ss_int(1)))&(__ss_int(7)));
    return NULL;
}

void *TonyJpegDecoder::InitDecoder() {
    /**
    Prepare for all the tables needed, 
    eg. quantization tables, huff tables, color convert tables
    1 <= nQuality <= 100, is used for quantization scaling
    Computing once, and reuse them again and again !!!!!!!
    */
    this->GetBits = __ss_int(0);
    this->GetBuff = __ss_int(0);
    this->dcY = __ss_int(0);
    this->dcCb = __ss_int(0);
    this->dcCr = __ss_int(0);
    this->SetRangeTable();
    this->InitColorTable();
    this->InitQuantTable();
    this->InitHuffmanTable();
    return NULL;
}

void *TonyJpegDecoder::SetRangeTable() {
    /**
    prepare_range_limit_table(): Set self.tblRange[5*256+128 = 1408]
    range table is used for range limiting of idct results
    On most machines, particularly CPUs with pipelines or instruction prefetch,
    a (subscript-check-less) C table lookup
          x = sample_range_limit[x]
    is faster than explicit tests
            if (x < 0)  x = 0
            else if (x > MAXJSAMPLE)  x = MAXJSAMPLE
    */
    this->tblRange = ((((((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(256)))->__add__((new list<__ss_int>(range(__ss_int(256))))))->__add__(((new list<__ss_int>(1,__ss_int(255))))->__mul__((__ss_int(512)-__ss_int(128)))))->__add__(((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(384))))->__add__((new list<__ss_int>(range(__ss_int(128)))));
    return NULL;
}

void *TonyJpegDecoder::InitColorTable() {
    __ss_int __42, __43, i, nHalf, nScale, x;
    lambda0 FIX;
    dict<__ss_int, __ss_int> *__44, *__45, *__46, *__47;

    nScale = (__ss_int(1)<<__ss_int(16));
    nHalf = (nScale>>__ss_int(1));
    FIX = __lambda0__;

    FAST_FOR(i,0,__ss_int(256),1,42,43)
        x = (i-__ss_int(128));
        this->CrToR->__setitem__(i, (__int(((FIX(__ss_float(1.402), nScale)*x)+nHalf))>>__ss_int(16)));
        this->CbToB->__setitem__(i, (__int(((FIX(__ss_float(1.772), nScale)*x)+nHalf))>>__ss_int(16)));
        this->CrToG->__setitem__(i, __int(((-FIX(__ss_float(0.71414), nScale))*x)));
        this->CbToG->__setitem__(i, __int((((-FIX(__ss_float(0.34414), nScale))*x)+nHalf)));
    END_FOR

    return NULL;
}

void *TonyJpegDecoder::InitQuantTable() {
    /**
    InitQuantTable will produce customized quantization table into: self.tblYQuant[0..63] and self.tblCbCrQuant[0..63]
    */
    list<__ss_int> *aanscales, *std_chrominance_quant_tbl, *std_luminance_quant_tbl;

    std_luminance_quant_tbl = (new list<__ss_int>(64,__ss_int(16),__ss_int(11),__ss_int(10),__ss_int(16),__ss_int(24),__ss_int(40),__ss_int(51),__ss_int(61),__ss_int(12),__ss_int(12),__ss_int(14),__ss_int(19),__ss_int(26),__ss_int(58),__ss_int(60),__ss_int(55),__ss_int(14),__ss_int(13),__ss_int(16),__ss_int(24),__ss_int(40),__ss_int(57),__ss_int(69),__ss_int(56),__ss_int(14),__ss_int(17),__ss_int(22),__ss_int(29),__ss_int(51),__ss_int(87),__ss_int(80),__ss_int(62),__ss_int(18),__ss_int(22),__ss_int(37),__ss_int(56),__ss_int(68),__ss_int(109),__ss_int(103),__ss_int(77),__ss_int(24),__ss_int(35),__ss_int(55),__ss_int(64),__ss_int(81),__ss_int(104),__ss_int(113),__ss_int(92),__ss_int(49),__ss_int(64),__ss_int(78),__ss_int(87),__ss_int(103),__ss_int(121),__ss_int(120),__ss_int(101),__ss_int(72),__ss_int(92),__ss_int(95),__ss_int(98),__ss_int(112),__ss_int(100),__ss_int(103),__ss_int(99)));
    std_chrominance_quant_tbl = (new list<__ss_int>(64,__ss_int(17),__ss_int(18),__ss_int(24),__ss_int(47),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(18),__ss_int(21),__ss_int(26),__ss_int(66),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(24),__ss_int(26),__ss_int(56),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(47),__ss_int(66),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99),__ss_int(99)));
    aanscales = (new list<__ss_int>(64,__ss_int(16384),__ss_int(22725),__ss_int(21407),__ss_int(19266),__ss_int(16384),__ss_int(12873),__ss_int(8867),__ss_int(4520),__ss_int(22725),__ss_int(31521),__ss_int(29692),__ss_int(26722),__ss_int(22725),__ss_int(17855),__ss_int(12299),__ss_int(6270),__ss_int(21407),__ss_int(29692),__ss_int(27969),__ss_int(25172),__ss_int(21407),__ss_int(16819),__ss_int(11585),__ss_int(5906),__ss_int(19266),__ss_int(26722),__ss_int(25172),__ss_int(22654),__ss_int(19266),__ss_int(15137),__ss_int(10426),__ss_int(5315),__ss_int(16384),__ss_int(22725),__ss_int(21407),__ss_int(19266),__ss_int(16384),__ss_int(12873),__ss_int(8867),__ss_int(4520),__ss_int(12873),__ss_int(17855),__ss_int(16819),__ss_int(15137),__ss_int(12873),__ss_int(10114),__ss_int(6967),__ss_int(3552),__ss_int(8867),__ss_int(12299),__ss_int(11585),__ss_int(10426),__ss_int(8867),__ss_int(6967),__ss_int(4799),__ss_int(2446),__ss_int(4520),__ss_int(6270),__ss_int(5906),__ss_int(5315),__ss_int(4520),__ss_int(3552),__ss_int(2446),__ss_int(1247)));
    this->qtblY = ScaleQuantTable(this->qtblY_dict, aanscales);
    this->qtblCbCr = ScaleQuantTable(this->qtblCbCr_dict, aanscales);
    return NULL;
}

void *TonyJpegDecoder::InitHuffmanTable() {
    /**
    Prepare four Huffman tables:
    HUFFMAN_TABLE self.htblYDC, self.htblYAC, self.htblCbCrDC, self.htblCbCrAC
    */
    list<__ss_int> *bitsCbCrAC, *bitsCbCrDC, *bitsYAC, *bitsYDC, *valCbCrAC, *valCbCrDC, *valYAC, *valYDC;

    bitsYDC = (new list<__ss_int>(17,__ss_int(0),__ss_int(0),__ss_int(1),__ss_int(5),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0)));
    valYDC = (new list<__ss_int>(12,__ss_int(0),__ss_int(1),__ss_int(2),__ss_int(3),__ss_int(4),__ss_int(5),__ss_int(6),__ss_int(7),__ss_int(8),__ss_int(9),__ss_int(10),__ss_int(11)));
    bitsCbCrDC = (new list<__ss_int>(17,__ss_int(0),__ss_int(0),__ss_int(3),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(1),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0)));
    valCbCrDC = (new list<__ss_int>(12,__ss_int(0),__ss_int(1),__ss_int(2),__ss_int(3),__ss_int(4),__ss_int(5),__ss_int(6),__ss_int(7),__ss_int(8),__ss_int(9),__ss_int(10),__ss_int(11)));
    bitsYAC = (new list<__ss_int>(17,__ss_int(0),__ss_int(0),__ss_int(2),__ss_int(1),__ss_int(3),__ss_int(3),__ss_int(2),__ss_int(4),__ss_int(3),__ss_int(5),__ss_int(5),__ss_int(4),__ss_int(4),__ss_int(0),__ss_int(0),__ss_int(1),__ss_int(125)));
    valYAC = (new list<__ss_int>(162,__ss_int(1),__ss_int(2),__ss_int(3),__ss_int(0),__ss_int(4),__ss_int(17),__ss_int(5),__ss_int(18),__ss_int(33),__ss_int(49),__ss_int(65),__ss_int(6),__ss_int(19),__ss_int(81),__ss_int(97),__ss_int(7),__ss_int(34),__ss_int(113),__ss_int(20),__ss_int(50),__ss_int(129),__ss_int(145),__ss_int(161),__ss_int(8),__ss_int(35),__ss_int(66),__ss_int(177),__ss_int(193),__ss_int(21),__ss_int(82),__ss_int(209),__ss_int(240),__ss_int(36),__ss_int(51),__ss_int(98),__ss_int(114),__ss_int(130),__ss_int(9),__ss_int(10),__ss_int(22),__ss_int(23),__ss_int(24),__ss_int(25),__ss_int(26),__ss_int(37),__ss_int(38),__ss_int(39),__ss_int(40),__ss_int(41),__ss_int(42),__ss_int(52),__ss_int(53),__ss_int(54),__ss_int(55),__ss_int(56),__ss_int(57),__ss_int(58),__ss_int(67),__ss_int(68),__ss_int(69),__ss_int(70),__ss_int(71),__ss_int(72),__ss_int(73),__ss_int(74),__ss_int(83),__ss_int(84),__ss_int(85),__ss_int(86),__ss_int(87),__ss_int(88),__ss_int(89),__ss_int(90),__ss_int(99),__ss_int(100),__ss_int(101),__ss_int(102),__ss_int(103),__ss_int(104),__ss_int(105),__ss_int(106),__ss_int(115),__ss_int(116),__ss_int(117),__ss_int(118),__ss_int(119),__ss_int(120),__ss_int(121),__ss_int(122),__ss_int(131),__ss_int(132),__ss_int(133),__ss_int(134),__ss_int(135),__ss_int(136),__ss_int(137),__ss_int(138),__ss_int(146),__ss_int(147),__ss_int(148),__ss_int(149),__ss_int(150),__ss_int(151),__ss_int(152),__ss_int(153),__ss_int(154),__ss_int(162),__ss_int(163),__ss_int(164),__ss_int(165),__ss_int(166),__ss_int(167),__ss_int(168),__ss_int(169),__ss_int(170),__ss_int(178),__ss_int(179),__ss_int(180),__ss_int(181),__ss_int(182),__ss_int(183),__ss_int(184),__ss_int(185),__ss_int(186),__ss_int(194),__ss_int(195),__ss_int(196),__ss_int(197),__ss_int(198),__ss_int(199),__ss_int(200),__ss_int(201),__ss_int(202),__ss_int(210),__ss_int(211),__ss_int(212),__ss_int(213),__ss_int(214),__ss_int(215),__ss_int(216),__ss_int(217),__ss_int(218),__ss_int(225),__ss_int(226),__ss_int(227),__ss_int(228),__ss_int(229),__ss_int(230),__ss_int(231),__ss_int(232),__ss_int(233),__ss_int(234),__ss_int(241),__ss_int(242),__ss_int(243),__ss_int(244),__ss_int(245),__ss_int(246),__ss_int(247),__ss_int(248),__ss_int(249),__ss_int(250)));
    bitsCbCrAC = (new list<__ss_int>(17,__ss_int(0),__ss_int(0),__ss_int(2),__ss_int(1),__ss_int(2),__ss_int(4),__ss_int(4),__ss_int(3),__ss_int(4),__ss_int(7),__ss_int(5),__ss_int(4),__ss_int(4),__ss_int(0),__ss_int(1),__ss_int(2),__ss_int(119)));
    valCbCrAC = (new list<__ss_int>(162,__ss_int(0),__ss_int(1),__ss_int(2),__ss_int(3),__ss_int(17),__ss_int(4),__ss_int(5),__ss_int(33),__ss_int(49),__ss_int(6),__ss_int(18),__ss_int(65),__ss_int(81),__ss_int(7),__ss_int(97),__ss_int(113),__ss_int(19),__ss_int(34),__ss_int(50),__ss_int(129),__ss_int(8),__ss_int(20),__ss_int(66),__ss_int(145),__ss_int(161),__ss_int(177),__ss_int(193),__ss_int(9),__ss_int(35),__ss_int(51),__ss_int(82),__ss_int(240),__ss_int(21),__ss_int(98),__ss_int(114),__ss_int(209),__ss_int(10),__ss_int(22),__ss_int(36),__ss_int(52),__ss_int(225),__ss_int(37),__ss_int(241),__ss_int(23),__ss_int(24),__ss_int(25),__ss_int(26),__ss_int(38),__ss_int(39),__ss_int(40),__ss_int(41),__ss_int(42),__ss_int(53),__ss_int(54),__ss_int(55),__ss_int(56),__ss_int(57),__ss_int(58),__ss_int(67),__ss_int(68),__ss_int(69),__ss_int(70),__ss_int(71),__ss_int(72),__ss_int(73),__ss_int(74),__ss_int(83),__ss_int(84),__ss_int(85),__ss_int(86),__ss_int(87),__ss_int(88),__ss_int(89),__ss_int(90),__ss_int(99),__ss_int(100),__ss_int(101),__ss_int(102),__ss_int(103),__ss_int(104),__ss_int(105),__ss_int(106),__ss_int(115),__ss_int(116),__ss_int(117),__ss_int(118),__ss_int(119),__ss_int(120),__ss_int(121),__ss_int(122),__ss_int(130),__ss_int(131),__ss_int(132),__ss_int(133),__ss_int(134),__ss_int(135),__ss_int(136),__ss_int(137),__ss_int(138),__ss_int(146),__ss_int(147),__ss_int(148),__ss_int(149),__ss_int(150),__ss_int(151),__ss_int(152),__ss_int(153),__ss_int(154),__ss_int(162),__ss_int(163),__ss_int(164),__ss_int(165),__ss_int(166),__ss_int(167),__ss_int(168),__ss_int(169),__ss_int(170),__ss_int(178),__ss_int(179),__ss_int(180),__ss_int(181),__ss_int(182),__ss_int(183),__ss_int(184),__ss_int(185),__ss_int(186),__ss_int(194),__ss_int(195),__ss_int(196),__ss_int(197),__ss_int(198),__ss_int(199),__ss_int(200),__ss_int(201),__ss_int(202),__ss_int(210),__ss_int(211),__ss_int(212),__ss_int(213),__ss_int(214),__ss_int(215),__ss_int(216),__ss_int(217),__ss_int(218),__ss_int(226),__ss_int(227),__ss_int(228),__ss_int(229),__ss_int(230),__ss_int(231),__ss_int(232),__ss_int(233),__ss_int(234),__ss_int(242),__ss_int(243),__ss_int(244),__ss_int(245),__ss_int(246),__ss_int(247),__ss_int(248),__ss_int(249),__ss_int(250)));
    (this->htblYDC)->ComputeHuffmanTable();
    (this->htblYAC)->ComputeHuffmanTable();
    (this->htblCbCrDC)->ComputeHuffmanTable();
    (this->htblCbCrAC)->ComputeHuffmanTable();
    return NULL;
}

list<__ss_int> *TonyJpegDecoder::DecompressImage(bytes *inbuf) {
    /**
    DecompressImage(), the main function in this class !!
    inbuf is source data in jpg format
    return is bmp bgr format, bottom_up
    */
    list<__ss_int> *byTile, *outbuf, *tilerow;
    __ss_int __48, __49, __50, __51, __52, __53, cxTile, cyTile, nRowBytes, nTrueCols, nTrueRows, offset, outbufpos, xPixel, xTile, y, yPixel, yTile;

    this->ReadJpgHeader(inbuf);
    outbuf = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(((this->Width*this->Height)*__ss_int(3)));
    cxTile = __floordiv(((this->Width+this->McuSize)-__ss_int(1)),this->McuSize);
    cyTile = __floordiv(((this->Height+this->McuSize)-__ss_int(1)),this->McuSize);
    nRowBytes = (__floordiv(((this->Width*__ss_int(3))+__ss_int(3)),__ss_int(4))*__ss_int(4));

    FAST_FOR(yTile,0,cyTile,1,48,49)

        FAST_FOR(xTile,0,cxTile,1,50,51)
            byTile = this->DecompressOneTile();
            xPixel = (xTile*this->McuSize);
            yPixel = (yTile*this->McuSize);
            nTrueRows = this->McuSize;
            nTrueCols = this->McuSize;
            if (((yPixel+nTrueRows)>this->Height)) {
                nTrueRows = (this->Height-yPixel);
            }
            if (((xPixel+nTrueCols)>this->Width)) {
                nTrueCols = (this->Width-xPixel);
            }
            outbufpos = ((((this->Height-__ss_int(1))-yPixel)*nRowBytes)+(xPixel*__ss_int(3)));

            FAST_FOR(y,0,nTrueRows,1,52,53)
                offset = ((y*this->McuSize)*__ss_int(3));
                tilerow = byTile->__slice__(__ss_int(3), offset, (offset+(nTrueCols*__ss_int(3))), __ss_int(0));
                (outbuf)->__setslice__(__ss_int(3),outbufpos,(outbufpos+(nTrueCols*__ss_int(3))),__ss_int(0),tilerow);
                outbufpos = (outbufpos-nRowBytes);
            END_FOR

        END_FOR

    END_FOR

    return outbuf;
}

list<__ss_int> *TonyJpegDecoder::DecompressOneTile() {
    /**
    decompress one 16*16 pixel tile. returns output in BGR format, 16*16*3
    */
    list<__ss_int> *coeff, *pYCbCr, *tileoutput;
    __ss_int __54, __55, i;

    if (this->restart_interval) {
        if ((this->restarts_to_go==__ss_int(0))) {
            this->GetBits = __ss_int(0);
            this->read_restart_marker();
            this->dcY = __ss_int(0);
            this->dcCb = __ss_int(0);
            this->dcCr = __ss_int(0);
            this->restarts_to_go = this->restart_interval;
        }
    }
    pYCbCr = (new list<__ss_int>());

    FAST_FOR(i,0,this->BlocksInMcu,1,54,55)
        coeff = this->HuffmanDecode(i);
        pYCbCr = (pYCbCr)->__iadd__(this->InverseDct(coeff, i));
    END_FOR

    tileoutput = this->YCbCrToBGREx(pYCbCr);
    this->restarts_to_go = (this->restarts_to_go-__ss_int(1));
    return tileoutput;
}

list<__ss_int> *TonyJpegDecoder::YCbCrToBGREx(list<__ss_int> *pYCbCr) {
    /**
    Color conversion and up-sampling
    in, Y: 256 or 64 bytes; Cb: 64 bytes; Cr: 64 bytes
    out, BGR format, 16*16*3 = 768 bytes; or 8*8*3=192 bytes
    */
    list<__ss_int> *__62, *pByte, *pyoffset, *range_limit;
    __ss_int __58, __59, __60, __61, __63, blocknum, blue, cb, cr, green, i, j, pcboffset, pcroffset, pyindex, red, y;

    pyoffset = list_comp_1(this);
    pcboffset = ((this->BlocksInMcu-__ss_int(2))*__ss_int(64));
    pcroffset = (pcboffset+__ss_int(64));
    range_limit = ((this->tblRange)->__slice__(__ss_int(1), __ss_int(256), __ss_int(0), __ss_int(0)))->__add__((this->tblRange)->__slice__(__ss_int(2), __ss_int(0), __ss_int(256), __ss_int(0)));
    pByte = (new list<__ss_int>());

    FAST_FOR(j,0,this->McuSize,1,58,59)

        FAST_FOR(i,0,this->McuSize,1,60,61)
            blocknum = ((__floordiv(j,__ss_int(2))*__ss_int(8))+__floordiv(i,__ss_int(2)));
            pyindex = (((j>>__ss_int(3))*__ss_int(2))+(i>>__ss_int(3)));
            y = pYCbCr->__getfast__(pyoffset->__getfast__(pyindex));
            __62 = pyoffset;
            __63 = pyindex;
            __62->__setitem__(__63, (__62->__getfast__(__63)+__ss_int(1)));
            cb = pYCbCr->__getfast__((pcboffset+blocknum));
            cr = pYCbCr->__getfast__((pcroffset+blocknum));
            blue = range_limit->__getfast__((y+(this->CbToB)->__getitem__(cb)));
            green = range_limit->__getfast__((y+(((this->CbToG)->__getitem__(cb)+(this->CrToG)->__getitem__(cr))>>__ss_int(16))));
            red = range_limit->__getfast__((y+(this->CrToR)->__getitem__(cr)));
            pByte = (pByte)->__iadd__((new list<__ss_int>(3,blue,green,red)));
        END_FOR

    END_FOR

    return pByte;
}

list<__ss_int> *TonyJpegDecoder::InverseDct(list<__ss_int> *coeff, __ss_int nBlock) {
    /**
    AA&N DCT algorithm implemention
    coeff             # in, dct coefficients, length = 64
    data             # out, 64 bytes        
    nBlock           # block index: 0~3:Y; 4:Cb; 5:Cr
    */
    __ss_int DCTSIZE, FIX_1_082392200, FIX_1_414213562, FIX_1_847759065, FIX_2_613125930, PASS1_BITS, RANGE_MASK, __64, __65, __66, __67, __68, __69, __72, basis, ctr, dcval, inptr, n, outptr, quantptr, tmp0, tmp1, tmp10, tmp11, tmp12, tmp13, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, uuhu, wsptr, z10, z11, z12, z13, z5;
    lambda1 MULTIPLY;
    list<__ss_int> *__70, *outbuf, *quant, *range_limit, *workspace;
    lambda2 IDESCALE;
    __iter<__ss_int> *__71;
    list<__ss_int>::for_in_loop __73;

    FIX_1_082392200 = __ss_int(277);
    FIX_1_414213562 = __ss_int(362);
    FIX_1_847759065 = __ss_int(473);
    FIX_2_613125930 = __ss_int(669);
    MULTIPLY = __lambda1__;
    workspace = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(64));
    inptr = __ss_int(0);
    wsptr = __ss_int(0);
    outbuf = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(64));
    outptr = __ss_int(0);
    range_limit = (this->tblRange)->__slice__(__ss_int(1), (__ss_int(256)+__ss_int(128)), __ss_int(0), __ss_int(0));
    dcval = __ss_int(0);
    DCTSIZE = __ss_int(8);
    if ((nBlock<__ss_int(4))) {
        quant = this->qtblY;
    }
    else {
        quant = this->qtblCbCr;
    }
    quantptr = __ss_int(0);

    FAST_FOR(ctr,__ss_int(8),__ss_int(0),(-__ss_int(1)),64,65)
        basis = __ss_int(0);

        FAST_FOR(n,__ss_int(1),__ss_int(8),1,66,67)
            basis = ((basis)|(coeff->__getfast__((inptr+(DCTSIZE*n)))));
        END_FOR

        if ((basis==__ss_int(0))) {
            dcval = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(0))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(0)))));
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(0))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(1))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(2))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(3))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(4))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(5))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(6))), dcval);
            workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(7))), dcval);
            inptr = (inptr+__ss_int(1));
            quantptr = (quantptr+__ss_int(1));
            wsptr = (wsptr+__ss_int(1));
            continue;
        }
        tmp0 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(0))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(0)))));
        tmp1 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(2))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(2)))));
        tmp2 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(4))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(4)))));
        tmp3 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(6))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(6)))));
        tmp10 = (tmp0+tmp2);
        tmp11 = (tmp0-tmp2);
        tmp13 = (tmp1+tmp3);
        tmp12 = (MULTIPLY((tmp1-tmp3), FIX_1_414213562)-tmp13);
        tmp0 = (tmp10+tmp13);
        tmp3 = (tmp10-tmp13);
        tmp1 = (tmp11+tmp12);
        tmp2 = (tmp11-tmp12);
        tmp4 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(1))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(1)))));
        tmp5 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(3))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(3)))));
        tmp6 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(5))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(5)))));
        tmp7 = (coeff->__getfast__((inptr+(DCTSIZE*__ss_int(7))))*quant->__getfast__((quantptr+(DCTSIZE*__ss_int(7)))));
        z13 = (tmp6+tmp5);
        z10 = (tmp6-tmp5);
        z11 = (tmp4+tmp7);
        z12 = (tmp4-tmp7);
        tmp7 = (z11+z13);
        tmp11 = MULTIPLY((z11-z13), FIX_1_414213562);
        z5 = MULTIPLY((z10+z12), FIX_1_847759065);
        tmp10 = (MULTIPLY(z12, FIX_1_082392200)-z5);
        tmp12 = (MULTIPLY(z10, (-FIX_2_613125930))+z5);
        tmp6 = (tmp12-tmp7);
        tmp5 = (tmp11-tmp6);
        tmp4 = (tmp10+tmp5);
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(0))), __int((tmp0+tmp7)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(7))), __int((tmp0-tmp7)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(1))), __int((tmp1+tmp6)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(6))), __int((tmp1-tmp6)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(2))), __int((tmp2+tmp5)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(5))), __int((tmp2-tmp5)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(4))), __int((tmp3+tmp4)));
        workspace->__setitem__((wsptr+(DCTSIZE*__ss_int(3))), __int((tmp3-tmp4)));
        inptr = (inptr+__ss_int(1));
        quantptr = (quantptr+__ss_int(1));
        wsptr = (wsptr+__ss_int(1));
    END_FOR

    RANGE_MASK = __ss_int(1023);
    PASS1_BITS = __ss_int(2);
    IDESCALE = __lambda2__;
    wsptr = __ss_int(0);

    FAST_FOR(ctr,0,DCTSIZE,1,68,69)
        outptr = (ctr*__ss_int(8));
        basis = __ss_int(0);

        FOR_IN(uuhu,workspace->__slice__(__ss_int(3), (wsptr+__ss_int(1)), (wsptr+__ss_int(8)), __ss_int(0)),70,72,73)
            basis = ((basis)|(uuhu));
        END_FOR

        if ((basis==__ss_int(0))) {
            dcval = range_limit->__getfast__((((workspace->__getfast__(wsptr)>>__ss_int(5)))&(RANGE_MASK)));
            outbuf->__setitem__((outptr+__ss_int(0)), dcval);
            outbuf->__setitem__((outptr+__ss_int(1)), dcval);
            outbuf->__setitem__((outptr+__ss_int(2)), dcval);
            outbuf->__setitem__((outptr+__ss_int(3)), dcval);
            outbuf->__setitem__((outptr+__ss_int(4)), dcval);
            outbuf->__setitem__((outptr+__ss_int(5)), dcval);
            outbuf->__setitem__((outptr+__ss_int(6)), dcval);
            outbuf->__setitem__((outptr+__ss_int(7)), dcval);
            wsptr = (wsptr+DCTSIZE);
            continue;
        }
        tmp10 = (workspace->__getfast__((wsptr+__ss_int(0)))+workspace->__getfast__((wsptr+__ss_int(4))));
        tmp11 = (workspace->__getfast__((wsptr+__ss_int(0)))-workspace->__getfast__((wsptr+__ss_int(4))));
        tmp13 = (workspace->__getfast__((wsptr+__ss_int(2)))+workspace->__getfast__((wsptr+__ss_int(6))));
        tmp12 = (MULTIPLY((workspace->__getfast__((wsptr+__ss_int(2)))-workspace->__getfast__((wsptr+__ss_int(6)))), FIX_1_414213562)-tmp13);
        tmp0 = (tmp10+tmp13);
        tmp3 = (tmp10-tmp13);
        tmp1 = (tmp11+tmp12);
        tmp2 = (tmp11-tmp12);
        z13 = (workspace->__getfast__((wsptr+__ss_int(5)))+workspace->__getfast__((wsptr+__ss_int(3))));
        z10 = (workspace->__getfast__((wsptr+__ss_int(5)))-workspace->__getfast__((wsptr+__ss_int(3))));
        z11 = (workspace->__getfast__((wsptr+__ss_int(1)))+workspace->__getfast__((wsptr+__ss_int(7))));
        z12 = (workspace->__getfast__((wsptr+__ss_int(1)))-workspace->__getfast__((wsptr+__ss_int(7))));
        tmp7 = (z11+z13);
        tmp11 = MULTIPLY((z11-z13), FIX_1_414213562);
        z5 = MULTIPLY((z10+z12), FIX_1_847759065);
        tmp10 = (MULTIPLY(z12, FIX_1_082392200)-z5);
        tmp12 = (MULTIPLY(z10, (-FIX_2_613125930))+z5);
        tmp6 = (tmp12-tmp7);
        tmp5 = (tmp11-tmp6);
        tmp4 = (tmp10+tmp5);
        outbuf->__setitem__((outptr+__ss_int(0)), range_limit->__getfast__(((IDESCALE((tmp0+tmp7), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(7)), range_limit->__getfast__(((IDESCALE((tmp0-tmp7), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(1)), range_limit->__getfast__(((IDESCALE((tmp1+tmp6), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(6)), range_limit->__getfast__(((IDESCALE((tmp1-tmp6), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(2)), range_limit->__getfast__(((IDESCALE((tmp2+tmp5), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(5)), range_limit->__getfast__(((IDESCALE((tmp2-tmp5), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(4)), range_limit->__getfast__(((IDESCALE((tmp3+tmp4), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        outbuf->__setitem__((outptr+__ss_int(3)), range_limit->__getfast__(((IDESCALE((tmp3-tmp4), (PASS1_BITS+__ss_int(3))))&(RANGE_MASK))));
        wsptr = (wsptr+DCTSIZE);
    END_FOR

    return outbuf;
}

list<__ss_int> *TonyJpegDecoder::HuffmanDecode(__ss_int iBlock) {
    /**
    source is self.Data
    out DCT coefficients
    iBlock  0,1,2,3:Y; 4:Cb; 5:Cr; or 0:Y;1:Cb;2:Cr
    */
    HUFFTABLE *actbl, *dctbl;
    str *LastDC;
    list<__ss_int> *coeff;
    __ss_int k, r, s;

    if ((iBlock<(this->BlocksInMcu-__ss_int(2)))) {
        dctbl = this->htblYDC;
        actbl = this->htblYAC;
        LastDC = const_14;
    }
    else {
        dctbl = this->htblCbCrDC;
        actbl = this->htblCbCrAC;
        if ((iBlock==(this->BlocksInMcu-__ss_int(2)))) {
            LastDC = const_15;
        }
        else {
            LastDC = const_16;
        }
    }
    coeff = ((new list<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(64));
    s = this->GetCategory(dctbl);
    if (s) {
        r = this->DoGetBits(s);
        s = this->ValueFromCategory(s, r);
    }
    if (__eq(LastDC, const_14)) {
        s = (s+this->dcY);
        this->dcY = s;
    }
    else if (__eq(LastDC, const_15)) {
        s = (s+this->dcCb);
        this->dcCb = s;
    }
    else if (__eq(LastDC, const_16)) {
        s = (s+this->dcCr);
        this->dcCr = s;
    }
    coeff->__setitem__(__ss_int(0), s);
    k = __ss_int(1);

    while ((k<__ss_int(64))) {
        s = this->GetCategory(actbl);
        r = (s>>__ss_int(4));
        s = ((s)&(__ss_int(15)));
        if (s) {
            k = (k+r);
            r = this->DoGetBits(s);
            s = this->ValueFromCategory(s, r);
            coeff->__setitem__(__tonyjpegdecoder__::jpeg_natural_order->__getfast__(k), s);
        }
        else {
            if ((r!=__ss_int(15))) {
                break;
            }
            k = (k+__ss_int(15));
        }
        k = (k+__ss_int(1));
    }
    return coeff;
}

__ss_int TonyJpegDecoder::GetCategory(HUFFTABLE *htbl) {
    /**
    get category number for dc, or (0 run length, ac category) for ac
    */
    __ss_int look, nb;

    if ((this->GetBits<__ss_int(8))) {
        this->FillBitBuffer();
    }
    if ((this->GetBits<__ss_int(8))) {
        return this->SpecialDecode(htbl, __ss_int(1));
    }
    look = (((this->GetBuff>>(this->GetBits-__ss_int(8))))&(__ss_int(255)));
    nb = (htbl->look_nbits)->__getfast__(look);
    if (nb) {
        this->GetBits = (this->GetBits-nb);
        return (htbl->look_sym)->__getfast__(look);
    }
    else {
        return this->SpecialDecode(htbl, __ss_int(9));
    }
    return 0;
}

void *TonyJpegDecoder::FillBitBuffer() {
    __ss_int uc;


    while ((this->GetBits<__ss_int(25))) {
        if ((this->DataBytesLeft>__ss_int(0))) {
            if ((this->unread_marker!=__ss_int(0))) {
                if ((this->GetBits>=__ss_int(0))) {
                    break;
                }
            }
            uc = (this->Data)->__getitem__(this->DataPos);
            this->DataPos = (this->DataPos+__ss_int(1));
            this->DataBytesLeft = (this->DataBytesLeft-__ss_int(1));
            if ((uc==__ss_int(255))) {

                while ((uc==__ss_int(255))) {
                    uc = (this->Data)->__getitem__(this->DataPos);
                    this->DataPos = (this->DataPos+__ss_int(1));
                    this->DataBytesLeft = (this->DataBytesLeft-__ss_int(1));
                }
                if ((uc==__ss_int(0))) {
                    uc = __ss_int(255);
                }
                else {
                    this->unread_marker = uc;
                    if ((this->GetBits>=__ss_int(0))) {
                        break;
                    }
                }
            }
            this->GetBuff = ((__int((this->GetBuff<<__ss_int(8))))|(uc));
            this->GetBits = (this->GetBits+__ss_int(8));
        }
        else {
            break;
        }
    }
    return NULL;
}

__ss_int TonyJpegDecoder::DoGetBits(__ss_int nbits) {
    if ((this->GetBits<nbits)) {
        this->FillBitBuffer();
    }
    this->GetBits = (this->GetBits-nbits);
    return (((this->GetBuff>>this->GetBits))&(((__ss_int(1)<<nbits)-__ss_int(1))));
}

__ss_int TonyJpegDecoder::SpecialDecode(HUFFTABLE *htbl, __ss_int nMinBits) {
    /**
    Special Huffman decode:
    (1) For codes with length > 8
    (2) For codes with length < 8 while data is finished
    */
    __ss_int code, l;

    l = nMinBits;
    code = this->DoGetBits(l);

    while ((code>(htbl->maxcode)->__getfast__(l))) {
        code = (code<<__ss_int(1));
        code = ((code)|(this->DoGetBits(__ss_int(1))));
        l = (l+__ss_int(1));
    }
    if ((l>__ss_int(16))) {
        return __ss_int(0);
    }
    return (htbl->huffval)->__getfast__(((htbl->valptr)->__getfast__(l)+(code-(htbl->mincode)->__getfast__(l))));
}

__ss_int TonyJpegDecoder::ValueFromCategory(__ss_int nCate, __ss_int nOffset) {
    /**
    To find dc or ac value according to category and category offset
    */
    list<__ss_int> *half, *start;

    half = (new list<__ss_int>(16,__ss_int(0),__ss_int(1),__ss_int(2),__ss_int(4),__ss_int(8),__ss_int(16),__ss_int(32),__ss_int(64),__ss_int(128),__ss_int(256),__ss_int(512),__ss_int(1024),__ss_int(2048),__ss_int(4096),__ss_int(8192),__ss_int(16384)));
    start = (new list<__ss_int>(16,__ss_int(0),(((-__ss_int(1))<<__ss_int(1))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(2))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(3))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(4))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(5))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(6))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(7))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(8))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(9))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(10))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(11))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(12))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(13))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(14))+__ss_int(1)),(((-__ss_int(1))<<__ss_int(15))+__ss_int(1))));
    if ((nOffset<half->__getfast__(nCate))) {
        return (nOffset+start->__getfast__(nCate));
    }
    else {
        return nOffset;
    }
    return 0;
}

bytes *dw2c(__ss_int word) {
    return __mod6(const_17, 4, ((word)&(__ss_int(255))), (((word>>__ss_int(8)))&(__ss_int(255))), (((word>>__ss_int(16)))&(__ss_int(255))), (((word>>__ss_int(24)))&(__ss_int(255))));
}

bytes *w2c(__ss_int word) {
    return __mod6(const_18, 2, ((word)&(__ss_int(255))), (((word>>__ss_int(8)))&(__ss_int(255))));
}

/**
class BMPFile
*/

class_ *cl_BMPFile;

void *BMPFile::__init__(__ss_int width, __ss_int height, bytes *rgbstr) {
    this->data = rgbstr;
    this->width = width;
    this->height = height;
    return NULL;
}

bytes *BMPFile::__bytes__() {
    return (((this->getheader())->__add__(this->getinfoheader()))->__add__(this->getcolortable()))->__add__(this->data);
}

bytes *BMPFile::getheader() {
    return (((const_19)->__add__(dw2c(this->filesize())))->__add__(dw2c(__ss_int(0))))->__add__(dw2c(this->dataoffset()));
}

__ss_int BMPFile::filesize() {
    return (this->dataoffset()+this->imagesize());
}

__ss_int BMPFile::dataoffset() {
    __ss_int colortablelen, headerlen, infoheaderlen;

    headerlen = __ss_int(14);
    infoheaderlen = __ss_int(40);
    colortablelen = __ss_int(0);
    return ((headerlen+infoheaderlen)+colortablelen);
}

__ss_int BMPFile::imagesize() {
    /**
    compressed size of image
    */
    return len(this->data);
}

bytes *BMPFile::getinfoheader() {
    __ss_int bitcount, colorsimportant, colorsused, compression, planes, xpixelsperm, ypixelsperm;

    planes = __ss_int(1);
    bitcount = __ss_int(24);
    compression = __ss_int(0);
    xpixelsperm = __ss_int(1);
    ypixelsperm = __ss_int(1);
    colorsused = __ss_int(0);
    colorsimportant = __ss_int(0);
    return ((((((((((dw2c(__ss_int(40)))->__add__(dw2c(this->width)))->__add__(dw2c(this->height)))->__add__(w2c(planes)))->__add__(w2c(bitcount)))->__add__(dw2c(compression)))->__add__(dw2c(this->imagesize())))->__add__(dw2c(xpixelsperm)))->__add__(dw2c(ypixelsperm)))->__add__(dw2c(colorsused)))->__add__(dw2c(colorsimportant));
}

bytes *BMPFile::getcolortable() {
    return const_2;
}

bytes *bgr2rgb(bytes *bmpstr) {
    return (const_2)->join(list_comp_2(bmpstr));
}

void *__ss_main() {
    file_binary *inputfile;
    bytes *bmpstr, *bmpstr2, *jpgsrc;
    TonyJpegDecoder *decoder;
    list<__ss_int> *bmpout;
    BMPFile *bmp;
    str *bmpfile;

    inputfile = open_binary(const_20, const_21);
    jpgsrc = inputfile->read();
    inputfile->close();
    decoder = (new TonyJpegDecoder(1));
    bmpout = decoder->DecompressImage(jpgsrc);
    bmpstr = (const_2)->join(list_comp_3(bmpout));
    bmpstr2 = bgr2rgb(bmpstr);
    bmp = (new BMPFile(decoder->Width, decoder->Height, bmpstr));
    bmpfile = const_22;
    (open_binary(bmpfile, const_23))->write(__bytes(bmp));
    print(__mod6(const_24, 2, inputfile, bmpfile));
    return NULL;
}

void __init() {
    const_0 = new bytes("%c%c%c");
    const_1 = new bytes("%c");
    const_2 = new bytes("");
    const_3 = new str("Error reading the file header");
    const_4 = new str("jpeg header read, %d x %d");
    const_5 = new str("error reading one marker");
    const_6 = new str("skipping marker, length");
    const_7 = new str("comp 0 samp_factor = %d");
    const_8 = new str("restart_interval=%d");
    const_9 = new str("marker %02x");
    const_10 = new str("Prog + Huff is not supported");
    const_11 = new str("Sequential + Arith is not supported");
    const_12 = new str("Prog + Arith is not supported");
    const_13 = new str("Unknown marker: 0x%x");
    const_14 = new str("dcY");
    const_15 = new str("dcCb");
    const_16 = new str("dcCr");
    const_17 = new bytes("%c%c%c%c");
    const_18 = new bytes("%c%c");
    const_19 = new bytes("BM");
    const_20 = new str("tiger1.jpg");
    const_21 = new str("rb");
    const_22 = new str("tiger1.bmp");
    const_23 = new str("wb");
    const_24 = new str("converted %s to %s");
    const_25 = new str("__main__");

    __name__ = new str("__main__");

    M_SOF0 = __ss_int(192);
    M_SOF1 = __ss_int(193);
    M_SOF2 = __ss_int(194);
    M_SOF3 = __ss_int(195);
    M_SOF5 = __ss_int(197);
    M_SOF6 = __ss_int(198);
    M_SOF7 = __ss_int(199);
    M_JPG = __ss_int(200);
    M_SOF9 = __ss_int(201);
    M_SOF10 = __ss_int(202);
    M_SOF11 = __ss_int(203);
    M_SOF13 = __ss_int(205);
    M_SOF14 = __ss_int(206);
    M_SOF15 = __ss_int(207);
    M_DHT = __ss_int(196);
    M_DAC = __ss_int(204);
    M_RST0 = __ss_int(208);
    M_RST1 = __ss_int(209);
    M_RST2 = __ss_int(210);
    M_RST3 = __ss_int(211);
    M_RST4 = __ss_int(212);
    M_RST5 = __ss_int(213);
    M_RST6 = __ss_int(214);
    M_RST7 = __ss_int(215);
    M_SOI = __ss_int(216);
    M_EOI = __ss_int(217);
    M_SOS = __ss_int(218);
    M_DQT = __ss_int(219);
    M_DNL = __ss_int(220);
    M_DRI = __ss_int(221);
    M_DHP = __ss_int(222);
    M_EXP = __ss_int(223);
    M_APP0 = __ss_int(224);
    M_APP1 = __ss_int(225);
    M_APP2 = __ss_int(226);
    M_APP3 = __ss_int(227);
    M_APP4 = __ss_int(228);
    M_APP5 = __ss_int(229);
    M_APP6 = __ss_int(230);
    M_APP7 = __ss_int(231);
    M_APP8 = __ss_int(232);
    M_APP9 = __ss_int(233);
    M_APP10 = __ss_int(234);
    M_APP11 = __ss_int(235);
    M_APP12 = __ss_int(236);
    M_APP13 = __ss_int(237);
    M_APP14 = __ss_int(238);
    M_APP15 = __ss_int(239);
    M_JPG0 = __ss_int(240);
    M_JPG13 = __ss_int(253);
    M_COM = __ss_int(254);
    M_TEM = __ss_int(1);
    M_ERROR = __ss_int(256);
    jpeg_natural_order = (new list<__ss_int>(80,__ss_int(0),__ss_int(1),__ss_int(8),__ss_int(16),__ss_int(9),__ss_int(2),__ss_int(3),__ss_int(10),__ss_int(17),__ss_int(24),__ss_int(32),__ss_int(25),__ss_int(18),__ss_int(11),__ss_int(4),__ss_int(5),__ss_int(12),__ss_int(19),__ss_int(26),__ss_int(33),__ss_int(40),__ss_int(48),__ss_int(41),__ss_int(34),__ss_int(27),__ss_int(20),__ss_int(13),__ss_int(6),__ss_int(7),__ss_int(14),__ss_int(21),__ss_int(28),__ss_int(35),__ss_int(42),__ss_int(49),__ss_int(56),__ss_int(57),__ss_int(50),__ss_int(43),__ss_int(36),__ss_int(29),__ss_int(22),__ss_int(15),__ss_int(23),__ss_int(30),__ss_int(37),__ss_int(44),__ss_int(51),__ss_int(58),__ss_int(59),__ss_int(52),__ss_int(45),__ss_int(38),__ss_int(31),__ss_int(39),__ss_int(46),__ss_int(53),__ss_int(60),__ss_int(61),__ss_int(54),__ss_int(47),__ss_int(55),__ss_int(62),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63),__ss_int(63)));
    cl_jpeg_component_info = new class_("jpeg_component_info");
    jpeg_component_info::__static__();
    cl_HUFFTABLE = new class_("HUFFTABLE");
    cl_TonyJpegDecoder = new class_("TonyJpegDecoder");
    cl_BMPFile = new class_("BMPFile");
    if (__eq(__tonyjpegdecoder__::__name__, const_25)) {
        __ss_main();
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __shedskin__::__start(__tonyjpegdecoder__::__init);
}
