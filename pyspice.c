/**
 * PySPICE implementation file
 *
 * This file contains some helper functions for going between C and Python
 *
 * Author: Roberto Aguilar, roberto.c.aguilar@jpl.nasa.gov
 *
 * Released under the BSD license, see LICENSE for details
 *
 * $Id$
 */
#include "pyspice.h"

void make_buildvalue_tuple(char *buf, const char *type, const int count)
{
    int i = 0;

    strcat(buf, "(");

    for(i = 0; i < count; ++ i) {
        strcat(buf, type);
    }

    strcat(buf, ")");
}

static PyObject * get_double_list(double *array, const int count)
{
    int i = 0;
    /* set the center */
    PyObject *list = PyList_New(count);

    if(list) {
        for(i = 0; i < count; ++ i) {
            PyObject *d = PyFloat_FromDouble(array[i]);
            PyList_SET_ITEM(list, i, d);
        }
    }

    return list;
}

PyObject * get_py_boolean(SpiceBoolean* spicebool)
{
    return Py_BuildValue( "O", *spicebool ? Py_True : Py_False);
}

/**
 * Create a Python Ellipse object from a SpiceEllipse object
 */
PyObject * get_py_ellipse(SpiceEllipse *spice_obj)
{
    PyObject *py_obj = NULL;
    PyObject *module = PyImport_ImportModule("spice");

    if(module) {
        PyObject *py_cls = PyObject_GetAttrString(module, "Ellipse");

        if(py_cls) {
            py_obj = PyObject_CallObject(py_cls, NULL);

            if(py_obj) {
                PyObject_SetAttrString(py_obj, "center", get_double_list(spice_obj->center, 3));
                PyObject_SetAttrString(py_obj, "semi_major", get_double_list(spice_obj->semiMajor, 3));
                PyObject_SetAttrString(py_obj, "semi_minor", get_double_list(spice_obj->semiMinor, 3));
            }
        }
    }

    return py_obj;
}

#define XCLEAN(PYO) if ( PYO ) { Py_DECREF(PYO); PYO = NULL; }

#define ALLCLEAN \
  XCLEAN( pymodule ) \
  XCLEAN( py_cls ) \
  XCLEAN( pytooplArgs ) \
  XCLEAN( pydiktKw ) \
  XCLEAN( pybase ) \
  XCLEAN( pydata ) \
  XCLEAN( pyitem ) \
  if ( cell && dofree) PyMem_Free( cell )

#define RTNNULL \
  { XCLEAN( py_obj ) \
    ALLCLEAN; \
    return NULL; \
  }

PyObject * get_py_cell_freeopt(SpiceCell *cell, int dofree)
{
    PyObject *py_obj = NULL;
    PyObject *pymodule = NULL;
    PyObject *py_cls = NULL;
    PyObject *pytooplArgs = NULL;
    PyObject *pydiktKw = NULL;
    PyObject *pybase = NULL;
    PyObject *pydata = NULL;
    PyObject *pyitem = NULL;

    Py_ssize_t i;
    int itemLen;

    switch (cell->dtype) {
    case SPICE_CHR: itemLen = cell->length * sizeof(SpiceChar); break;
    case SPICE_INT: itemLen = sizeof(SpiceInt); break;
    case SPICE_DP: itemLen = sizeof(SpiceDouble); break;

    case SPICE_TIME: //itemLen = sizeof(SpiceDouble); break;
    case SPICE_BOOL: //itemLen = sizeof(SpiceBoolean); break;
    default: RTNNULL
    }

    if ( !(pymodule = PyImport_ImportModule("spice")) ) RTNNULL
    if ( !(py_cls = PyObject_GetAttrString(pymodule, "Cell")) ) RTNNULL
    if ( !(pytooplArgs = Py_BuildValue( "(ii)", (int)cell->dtype, (int)cell->size)) ) RTNNULL
    if ( !(pydiktKw = Py_BuildValue( "{s:i}", "lenArg", cell->length)) ) RTNNULL
    if ( !(py_obj = PyObject_Call(py_cls, pytooplArgs, pydiktKw)) ) RTNNULL
    if ( !(pybase = PyObject_GetAttrString( py_obj, "base")) ) RTNNULL
    if ( !(pydata = PyObject_GetAttrString( py_obj, "data")) ) RTNNULL

#   define XI(ATTR) PyObject_SetAttrString(py_obj, #ATTR, PyInt_FromLong((long)cell->ATTR));
#   define XB(ATTR) PyObject_SetAttrString(py_obj, #ATTR, get_py_boolean(&cell->ATTR) );
    XI(dtype)
    XI(length)
    XI(size)
    XI(card)
    XB(isSet)
    XB(adjust)
    XB(init)
    //printf( " after:" );
    //printf( "Cell.card=%ld",   PyInt_AsLong( PyObject_GetAttrString(py_obj, "card") ) );
    //printf( "; Cell.init=%s",   PyObject_GetAttrString(py_obj,"init")==Py_True?" True":"False" );
    //printf( "; cell->card=%ld",   (long)cell->card);
    //printf( "; cell->init=%s",   cell->init?"True ":"False");
    //printf( "; err=%s\n",   PyErr_Occurred() ? "Yes" : "No " );
#   undef XI
#   undef XB

    switch( cell->dtype ) {

    case SPICE_CHR:

      for ( i=0; i<(SPICE_CELL_CTRLSZ+cell->size); ++i ) {
        if ( !(pyitem = PyString_FromStringAndSize( cell->base+(i*itemLen), (Py_ssize_t)cell->length)) ) RTNNULL
        if ( -1==PyList_SetItem( i<SPICE_CELL_CTRLSZ ? pybase : pydata, i - (i<SPICE_CELL_CTRLSZ?0:SPICE_CELL_CTRLSZ), pyitem ) ) RTNNULL
        pyitem = NULL;
      }
      break;

    case SPICE_INT:

      for ( i=0; i<(SPICE_CELL_CTRLSZ+cell->size); ++i ) {
        if ( !(pyitem = PyInt_FromLong( (long) ((SpiceInt*)cell->base)[i] ) ) ) RTNNULL
        if ( -1==PyList_SetItem( i<SPICE_CELL_CTRLSZ ? pybase : pydata, i - (i<SPICE_CELL_CTRLSZ?0:SPICE_CELL_CTRLSZ), pyitem ) ) RTNNULL
        pyitem = NULL;
      }
      break;

    case SPICE_DP:

      for ( i=0; i<(SPICE_CELL_CTRLSZ+cell->size); ++i ) {
        if ( !(pyitem = PyFloat_FromDouble( (double) ((SpiceDouble*)cell->base)[i] )) ) RTNNULL
        if ( -1==PyList_SetItem( i<SPICE_CELL_CTRLSZ ? pybase : pydata, i - (i<SPICE_CELL_CTRLSZ?0:SPICE_CELL_CTRLSZ), pyitem ) ) RTNNULL
        pyitem = NULL;
      }

      break;

    case SPICE_TIME:
    case SPICE_BOOL:
    default:
      RTNNULL
    }

    ALLCLEAN;

    return py_obj;
}
#undef XCLEAN
#undef RTNNULL
#undef ALLCLEAN

PyObject * get_py_cell(SpiceCell *cell) {
  return get_py_cell_freeopt( cell, 1 );
}

PyObject * get_py_ekattdsc(SpiceEKAttDsc *spice_obj)
{
    PyObject *py_obj = NULL;
    return py_obj;
}

PyObject * get_py_eksegsum(SpiceEKSegSum *spice_obj)
{
    PyObject *py_obj = NULL;
    return py_obj;
}

PyObject * get_py_plane(SpicePlane *spice_obj)
{
    PyObject *py_obj = NULL;
    PyObject *module = PyImport_ImportModule("spice");

    if(module) {
        PyObject *py_cls = PyObject_GetAttrString(module, "Plane");

        if(py_cls) {
            py_obj = PyObject_CallObject(py_cls, NULL);

            if(py_obj) {
                PyObject_SetAttrString(py_obj, "constant", PyFloat_FromDouble(spice_obj->constant));
                PyObject_SetAttrString(py_obj, "normal", get_double_list(spice_obj->normal, 3));
            }
        }
    }

    return py_obj;
}


static inline int gat( PyObject* pyo, char* attr, SpiceCellDataType* ptr) {
PyObject* pySubo;
    pySubo = PyObject_GetAttrString( pyo, attr );
    if ( !pySubo ) return 0;
    Py_DECREF( pySubo );
    if ( PyInt_Check(pySubo) ) { *ptr = (SpiceCellDataType) PyInt_AsLong(pySubo); return 1; }
    if ( PyLong_Check(pySubo) ) { *ptr = (SpiceCellDataType) PyLong_AsDouble(pySubo); return 1; }
    return 0;
}

static inline int gai( PyObject* pyo, char* attr, SpiceInt* ptr) {
PyObject* pySubo;
    pySubo = PyObject_GetAttrString( pyo, attr );
    if ( !pySubo ) return 0;
    Py_DECREF( pySubo );
    if ( PyFloat_Check(pySubo) ) { *ptr = (SpiceDouble) PyFloat_AsDouble(pySubo); return 1; }
    if ( PyInt_Check(pySubo) ) { *ptr = (SpiceDouble) PyInt_AsLong(pySubo); return 1; }
    if ( PyLong_Check(pySubo) ) { *ptr = (SpiceDouble) PyLong_AsDouble(pySubo); return 1; }
    return 0;
}

static inline int gad( PyObject* pyo, char* attr, SpiceInt* ptr) {
PyObject* pySubo;
    pySubo = PyObject_GetAttrString( pyo, attr );
    if ( !pySubo ) return 0;
    Py_DECREF( pySubo );
    if ( PyInt_Check(pySubo) ) { *ptr = (SpiceInt) PyInt_AsLong(pySubo); return 1; }
    if ( PyLong_Check(pySubo) ) { *ptr = (SpiceInt) PyLong_AsLong(pySubo); return 1; }
    if ( PyFloat_Check(pySubo) ) { *ptr = (SpiceInt) PyFloat_AsDouble(pySubo); return 1; }
    return 0;
}

static inline int gab( PyObject* pyo, char* attr, SpiceBoolean* ptr) {
PyObject* pySubo;
    pySubo = PyObject_GetAttrString( pyo, attr );
    if ( !pySubo ) return 0;
    Py_DECREF( pySubo );
    if ( pySubo == Py_True ) { *ptr = SPICETRUE; return 1; }
    if ( pySubo == Py_False ) { *ptr = SPICEFALSE; return 1; }
    return 0;
}

#define GAANY(FUNC,ATTR) if ( ! FUNC(py_obj, #ATTR, &placeholder.ATTR) ) return NULL
#define GAT(ATTR) GAANY(gat,ATTR)
#define GAI(ATTR) GAANY(gai,ATTR)
#define GAD(ATTR) GAANY(gad,ATTR)
#define GAB(ATTR) GAANY(gab,ATTR)

SpiceCell * get_spice_cell(PyObject *py_obj)
{
    SpiceCell *spice_obj = NULL;

    SpiceCell placeholder;
    int baseLen;
    int dataLen;
    int itemLen;
    int minLen;
    int i;
    int j;
    Py_ssize_t pysz;
    void* pVoid;
    char* pChr;
    SpiceDouble* psDbl;
    SpiceInt* psInt;
    SpiceChar* psChr;
    PyObject* pyobj;

    PyObject* pyBase = PyObject_GetAttrString( py_obj, "base");
    PyObject* pyData = PyObject_GetAttrString( py_obj, "data");

#   define ANYCLEANUP(F) F(pyBase); F(pyData); if (spice_obj) PyMem_Free(spice_obj)
#   define XCLEANUP ANYCLEANUP(Py_XDECREF)
#   define CLEANUP ANYCLEANUP(Py_DECREF)
#   define RTNNULL { XCLEANUP; return NULL; }

    if ( !pyBase || !pyData) RTNNULL

    if ( (baseLen=PyObject_Length(pyBase)) != SPICE_CELL_CTRLSZ) RTNNULL

    GAI(size);

    if ( (dataLen=PyObject_Length(pyData)) != placeholder.size) RTNNULL

    GAT(dtype); GAI(length); GAI(card);
    GAB(isSet); GAB(adjust); GAB(init);

    switch (placeholder.dtype) {
    case SPICE_CHR: itemLen = placeholder.length * sizeof(SpiceChar); break;
    case SPICE_INT: itemLen = sizeof(SpiceInt); break;
    case SPICE_DP: itemLen = sizeof(SpiceDouble); break;

    case SPICE_TIME: //itemLen = sizeof(SpiceDouble); break;
    case SPICE_BOOL: //itemLen = sizeof(SpiceBoolean); break;
    default: RTNNULL
    }
    
    spice_obj = (SpiceCell*) PyMem_Malloc( sizeof( SpiceCell ) + ((SPICE_CELL_CTRLSZ + placeholder.size) * itemLen) );

    placeholder.base = (void*) (spice_obj+1);
    placeholder.data = placeholder.base + (SPICE_CELL_CTRLSZ * itemLen);

    memset( placeholder.base, 0, (SPICE_CELL_CTRLSZ+placeholder.size)*itemLen );

#   define GETPYBASEORDATA \
    if ( i<SPICE_CELL_CTRLSZ ) pyobj = PyList_GetItem( pyBase, i); \
    else                       pyobj = PyList_GetItem( pyData, i-SPICE_CELL_CTRLSZ); \
    if ( !pyobj ) RTNNULL

    switch (placeholder.dtype) {

    case SPICE_CHR:
      for ( (pVoid=placeholder.base),i=0; i<(SPICE_CELL_CTRLSZ+placeholder.size); (pVoid+=itemLen),++i ) {
        GETPYBASEORDATA
        if ( -1==PyString_AsStringAndSize( pyobj, &pChr, &pysz) ) RTNNULL
        psChr = pVoid;
        minLen = ((int)pysz) < itemLen ? (int)pysz : itemLen;
        for (j=0; j<minLen; ++j) *(psChr++) = (SpiceChar) *(pChr++);
      }
      break;

    case SPICE_INT:
      for ( (pVoid=placeholder.base),i=0; i<(SPICE_CELL_CTRLSZ+placeholder.size); (pVoid+=itemLen),++i ) {
        GETPYBASEORDATA
        psInt = pVoid;
        if ( -1==(*psInt=(SpiceInt)PyInt_AsLong( pyobj )) ) if ( PyErr_Occurred() ) RTNNULL
      }
      break;

    case SPICE_DP:
      for ( (pVoid=placeholder.base),i=0; i<(SPICE_CELL_CTRLSZ+placeholder.size); (pVoid+=itemLen),++i ) {
        GETPYBASEORDATA
        psDbl = pVoid;
        if ( -1.0==(*psDbl=(SpiceDouble)PyInt_AsLong( pyobj )) ) if ( PyErr_Occurred() ) RTNNULL
      }
      break;

    case SPICE_TIME:  // TBD
    case SPICE_BOOL:
    default: RTNNULL
    }

    *spice_obj = placeholder;

    return spice_obj;
}
#undef RTNNULL
#undef ANYCLEANUP
#undef XCLEANUP
#undef CLEANUP

SpiceEKAttDsc * get_spice_ekattdsc(PyObject *py_obj)
{
    SpiceEKAttDsc *spice_obj = NULL;
    return spice_obj;
}

SpiceEKSegSum * get_spice_eksegsum(PyObject *py_obj)
{
    SpiceEKSegSum *spice_obj = NULL;
    return spice_obj;
}

SpicePlane * get_spice_plane(PyObject *py_obj)
{
    SpicePlane *spice_obj = PyMem_Malloc(sizeof(SpicePlane));

    PyObject *l = NULL, *f = NULL;

    /* set the constant variable in the spice_obj */
    f = PyObject_GetAttrString(py_obj, "constant");
    spice_obj->constant = PyFloat_AsDouble(f);

    /* now set each element in the normal array */
    l = PyObject_GetAttrString(py_obj, "normal");

    f = PyList_GetItem(l, 0);
    spice_obj->normal[0] = PyFloat_AsDouble(f);

    f = PyList_GetItem(l, 1);
    spice_obj->normal[1] = PyFloat_AsDouble(f);

    f = PyList_GetItem(l, 2);
    spice_obj->normal[2] = PyFloat_AsDouble(f);

    return spice_obj;
}

SpiceEllipse * get_spice_ellipse(PyObject *ellipse)
{
    char failed = 0, *sections[3] = {"center", "semi_major", "semi_minor"};
    int i, j;

    SpiceEllipse *spice_ellipse = PyMem_Malloc(sizeof(SpiceEllipse));

    double *ellipse_sections[3] = {spice_ellipse->center, spice_ellipse->semiMajor, spice_ellipse->semiMinor};

    for(i = 0; i < 3; ++ i) {
        PyObject *section = PyObject_GetAttrString(ellipse, sections[i]);

        if(section) {
            for(j = 0; j < 3; ++ j) {
                ellipse_sections[i][j] = PyFloat_AS_DOUBLE(PyList_GET_ITEM(section, j));
            }
        } else {
            failed = 1;
            break;
        }
    }

    if(failed) {
        PyMem_Free(spice_ellipse);
        spice_ellipse = NULL;
    }

    return spice_ellipse;
}

PyObject * spice_berto(PyObject *self, PyObject *args)
{
    PyObject *py_ellipse = NULL;

    PYSPICE_CHECK_RETURN_STATUS(PyArg_ParseTuple(args, "O", &py_ellipse));

    SpiceEllipse *spice_ellipse = get_spice_ellipse(py_ellipse);

    char *sections[3] = {"center", "semi_major", "semi_minor"};
    double *ellipse_sections[3] = {spice_ellipse->center, spice_ellipse->semiMajor, spice_ellipse->semiMinor};
    int i = 0, j = 0;

    for(i = 0; i < 3; ++ i) {
        for(j = 0; j < 3; ++ j) {
            printf ("%s[%d] = %f\n", sections[i], j, ellipse_sections[i][j]);
        }
    }

    spice_ellipse->center[0] = 1;
    spice_ellipse->center[1] = 2;
    spice_ellipse->center[2] = 3;
    spice_ellipse->semiMajor[0] = 4;
    spice_ellipse->semiMajor[1] = 5;
    spice_ellipse->semiMajor[2] = 6;
    spice_ellipse->semiMinor[0] = 7;
    spice_ellipse->semiMinor[1] = 8;
    spice_ellipse->semiMinor[2] = 9;

    py_ellipse = get_py_ellipse(spice_ellipse);

    PyMem_Free(spice_ellipse);

    return py_ellipse;
}

PyObject * spice_test(PyObject *self, PyObject *args)
{
    PyObject *py_obj = NULL;
    SpicePlane *plane = NULL;

    PYSPICE_CHECK_RETURN_STATUS(PyArg_ParseTuple(args, "O", &py_obj));

    plane = get_spice_plane(py_obj);

    PyObject *py_obj2 = get_py_plane(plane);
    PyMem_Free(plane);

    return py_obj2;
}
