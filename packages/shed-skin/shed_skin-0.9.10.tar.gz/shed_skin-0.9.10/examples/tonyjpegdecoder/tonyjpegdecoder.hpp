#ifndef __TONYJPEGDECODER_HPP
#define __TONYJPEGDECODER_HPP

using namespace __shedskin__;
namespace __tonyjpegdecoder__ {

extern bytes *const_0, *const_1, *const_17, *const_18, *const_19, *const_2;
extern str *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

class jpeg_component_info;
class HUFFTABLE;
class TonyJpegDecoder;
class BMPFile;

typedef __ss_int (*lambda0)(__ss_float, __ss_int);
typedef __ss_int (*lambda1)(__ss_int, __ss_int);
typedef __ss_int (*lambda2)(__ss_int, __ss_int);

extern str *__name__;
extern __ss_int M_APP0, M_APP1, M_APP10, M_APP11, M_APP12, M_APP13, M_APP14, M_APP15, M_APP2, M_APP3, M_APP4, M_APP5, M_APP6, M_APP7, M_APP8, M_APP9, M_COM, M_DAC, M_DHP, M_DHT, M_DNL, M_DQT, M_DRI, M_EOI, M_ERROR, M_EXP, M_JPG, M_JPG0, M_JPG13, M_RST0, M_RST1, M_RST2, M_RST3, M_RST4, M_RST5, M_RST6, M_RST7, M_SOF0, M_SOF1, M_SOF10, M_SOF11, M_SOF13, M_SOF14, M_SOF15, M_SOF2, M_SOF3, M_SOF5, M_SOF6, M_SOF7, M_SOF9, M_SOI, M_SOS, M_TEM;
extern list<__ss_int> *jpeg_natural_order;


extern class_ *cl_jpeg_component_info;
class jpeg_component_info : public pyobj {
public:
    __ss_int h_samp_factor;
    __ss_int v_samp_factor;
    __ss_int component_index;
    __ss_int quant_tbl_no;
    __ss_int component_id;

    jpeg_component_info() { this->__class__ = cl_jpeg_component_info; }
    static void __static__();
};

extern class_ *cl_HUFFTABLE;
class HUFFTABLE : public pyobj {
public:
    list<__ss_int> *bits;
    list<__ss_int> *huffval;
    list<__ss_int> *mincode;
    list<__ss_int> *maxcode;
    list<__ss_int> *valptr;
    list<__ss_int> *look_nbits;
    list<__ss_int> *look_sym;

    HUFFTABLE() {}
    HUFFTABLE(int __ss_init) {
        this->__class__ = cl_HUFFTABLE;
        __init__();
    }
    void *__init__();
    void *ComputeHuffmanTable();
};

extern class_ *cl_TonyJpegDecoder;
class TonyJpegDecoder : public pyobj {
public:
    __ss_int Width;
    __ss_int Height;
    __ss_int next_restart_num;
    __ss_int Component;
    __ss_int Scale;
    __ss_int restarts_to_go;
    __ss_int BlocksInMcu;
    __ss_int DataBytesLeft;
    __ss_int dcCb;
    __ss_int Quality;
    __ss_int Precision;
    __ss_int McuSize;
    __ss_int GetBits;
    __ss_int restart_interval;
    __ss_int GetBuff;
    __ss_int DataPos;
    __ss_int unread_marker;
    __ss_int dcY;
    __ss_int dcCr;
    bytes *Data;
    list<__ss_int> *tblRange;
    dict<__ss_int, __ss_int> *CrToR;
    dict<__ss_int, __ss_int> *CrToG;
    dict<__ss_int, __ss_int> *CbToB;
    dict<__ss_int, __ss_int> *CbToG;
    dict<__ss_int, __ss_int> *qtblY_dict;
    dict<__ss_int, __ss_int> *qtblCbCr_dict;
    HUFFTABLE *htblYDC;
    HUFFTABLE *htblYAC;
    HUFFTABLE *htblCbCrDC;
    HUFFTABLE *htblCbCrAC;
    list<jpeg_component_info *> *comp_info;
    __ss_int length;
    list<__ss_int> *qtblCbCr;
    list<__ss_int> *qtblY;

    TonyJpegDecoder() {}
    TonyJpegDecoder(int __ss_init) {
        this->__class__ = cl_TonyJpegDecoder;
        __init__();
    }
    void *__init__();
    void *ReadJpgHeader(bytes *jpegsrc);
    __ss_int ReadByte();
    __ss_int ReadWord();
    __ss_int ReadOneMarker();
    void *SkipMarker();
    void *GetDqt();
    void *get_sof(__ss_bool is_prog, __ss_bool is_arith);
    void *get_dht();
    void *get_sos();
    void *get_dri();
    void *read_markers(bytes *inbuf);
    void *read_restart_marker();
    void *InitDecoder();
    void *SetRangeTable();
    void *InitColorTable();
    void *InitQuantTable();
    void *InitHuffmanTable();
    list<__ss_int> *DecompressImage(bytes *inbuf);
    list<__ss_int> *DecompressOneTile();
    list<__ss_int> *YCbCrToBGREx(list<__ss_int> *pYCbCr);
    list<__ss_int> *InverseDct(list<__ss_int> *coeff, __ss_int nBlock);
    list<__ss_int> *HuffmanDecode(__ss_int iBlock);
    __ss_int GetCategory(HUFFTABLE *htbl);
    void *FillBitBuffer();
    __ss_int DoGetBits(__ss_int nbits);
    __ss_int SpecialDecode(HUFFTABLE *htbl, __ss_int nMinBits);
    __ss_int ValueFromCategory(__ss_int nCate, __ss_int nOffset);
};

extern class_ *cl_BMPFile;
class BMPFile : public pyobj {
public:
    bytes *data;
    __ss_int width;
    __ss_int height;

    BMPFile() {}
    BMPFile(__ss_int width, __ss_int height, bytes *rgbstr) {
        this->__class__ = cl_BMPFile;
        __init__(width, height, rgbstr);
    }
    void *__init__(__ss_int width, __ss_int height, bytes *rgbstr);
    bytes *__bytes__();
    bytes *getheader();
    __ss_int filesize();
    __ss_int dataoffset();
    __ss_int imagesize();
    bytes *getinfoheader();
    bytes *getcolortable();
};

list<__ss_int> *ScaleQuantTable(dict<__ss_int, __ss_int> *tblStd, list<__ss_int> *tblAan);
bytes *dw2c(__ss_int word);
bytes *w2c(__ss_int word);
bytes *bgr2rgb(bytes *bmpstr);
void *__ss_main();

} // module namespace
#endif
