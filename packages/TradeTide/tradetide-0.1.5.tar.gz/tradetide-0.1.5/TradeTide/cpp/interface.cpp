#include <Python.h>
#include <datetime.h>
#include <iostream>
#include "position.cpp"
#include <datetime.h>

// Define the Python object structure
typedef struct
{
    PyObject_HEAD
    Position* cpp_obj;
} PyPositionObject;



// Names of the keyword arguments
static int PyPosition_init(PyPositionObject* self, PyObject* args, PyObject* kwargs)
{
    // Ensure the Python DateTime API is initialized at the beginning of your function
    PyDateTime_IMPORT;

    PyObject* start_date = NULL;
    PyObject* market = NULL;

    static char* kwlist[] = {"start_date", "market", NULL};
    // Corrected use of PyDateTime_Type
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", kwlist, &start_date, &market))
    {
        PyErr_SetString(PyExc_TypeError, "Parameters must be a datetime object and a market object");
        return -1;
    }

    // Verifying 'market' is DataFrame-like
    if (!PyObject_HasAttrString(market, "dtypes"))
    {
        PyErr_SetString(PyExc_TypeError, "The market parameter must have a 'dtypes' attribute, like a pandas DataFrame");
        return -1;
    }

    self->cpp_obj = new Position(start_date, market);
    return 0;
}


// Deallocate memory
static void PyPosition_dealloc(PyPositionObject* self)
{
    delete self->cpp_obj;
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

// Function to create new Position objects
static PyObject* PyPosition_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyPositionObject *self;
    self = (PyPositionObject*)type->tp_alloc(type, 0);
    if (self != nullptr) {
        self->cpp_obj = nullptr; // Initialize the pointer to nullptr
    }
    return (PyObject*)self;
}


// Method definitions for the Position object------------------------------------------------
static PyMethodDef PyPosition_methods[] =
{
    {nullptr}  // Sentinel
};
// Method definitions for the Position object------------------------------------------------

// Getter and Setter for attributes-----------------------------------------------------------
static PyObject* PyPosition_get_start_date(PyPositionObject* self, void* closure) 
{
    return self->cpp_obj->start_date;
}

static PyObject* PyPosition_get_exit_price(PyPositionObject* self, void* closure)
{
    return PyFloat_FromDouble(self->cpp_obj->exit_price);
}

static PyGetSetDef PyPosition_getsetters[] = {
    {"start_date", (getter)PyPosition_get_start_date, NULL, "start_date", nullptr},
    {"exit_price", (getter)PyPosition_get_exit_price, NULL, "exit_price", nullptr},
    {nullptr}  // Sentinel
};
// Getter and Setter for attributes-----------------------------------------------------------


// Python type object for Position
static PyTypeObject PyPositionType =
{
    PyVarObject_HEAD_INIT(NULL, 0)
    "interface.Position",              /* tp_name */
    sizeof(PyPositionObject),            /* tp_basicsize */
    0,                                   /* tp_itemsize */
    (destructor)PyPosition_dealloc,      /* tp_dealloc */
    0,                                   /* tp_print */
    0,                                   /* tp_getattr */
    0,                                   /* tp_setattr */
    0,                                   /* tp_reserved */
    0,                                   /* tp_repr */
    0,                                   /* tp_as_number */
    0,                                   /* tp_as_sequence */
    0,                                   /* tp_as_mapping */
    0,                                   /* tp_hash  */
    0,                                   /* tp_call */
    0,                                   /* tp_str */
    0,                                   /* tp_getattro */
    0,                                   /* tp_setattro */
    0,                                   /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "Position objects",                  /* tp_doc */
    0,                                   /* tp_traverse */
    0,                                   /* tp_clear */
    0,                                   /* tp_richcompare */
    0,                                   /* tp_weaklistoffset */
    0,                                   /* tp_iter */
    0,                                   /* tp_iternext */
    PyPosition_methods,                  /* tp_methods */
    0,                                   /* tp_members */
    PyPosition_getsetters,               /* tp_getset */
    0,                                   /* tp_base */
    0,                                   /* tp_dict */
    0,                                   /* tp_descr_get */
    0,                                   /* tp_descr_set */
    0,                                   /* tp_dictoffset */
    (initproc)PyPosition_init,           /* tp_init */
    0,                                   /* tp_alloc */
    PyPosition_new,                      /* tp_new */
};

// Module initialization function
static PyModuleDef interfacemodule = {
    PyModuleDef_HEAD_INIT,
    "interface",   /* m_name */
    "Example module that creates an extension type.",  /* m_doc */
    -1,              /* m_size */
};

PyMODINIT_FUNC PyInit_interface(void) {
    PyObject* m;

    if (PyType_Ready(&PyPositionType) < 0)
        return nullptr;

    m = PyModule_Create(&interfacemodule);
    if (!m)
        return nullptr;

    Py_INCREF(&PyPositionType);
    if (PyModule_AddObject(m, "Position", reinterpret_cast<PyObject*>(&PyPositionType)) < 0) {
        Py_DECREF(&PyPositionType);
        Py_DECREF(m);
        return nullptr;
    }

    return m;
}
