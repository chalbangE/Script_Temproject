#include "python.h" 

static PyObject *

average(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    if (!PyArg_ParseTuple(args, "O", &listObj))
        return NULL;

    if (!PyList_Check(listObj)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list");
        return NULL;
    }

    int listSize = PyList_Size(listObj);
    if (listSize == 0) {
        PyErr_SetString(PyExc_ValueError, "list is empty");
        return NULL;
    }

    int sum = 0;
    for (int i = 0; i < listSize; i++) {
        PyObject* item = PyList_GetItem(listObj, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "list items must be integers");
            return NULL;
        }
        sum += PyLong_AsLong(item);
    }

    int average = sum / listSize;
    return Py_BuildValue("i", average);
}

static PyMethodDef AverageMethods[] = {
    {"average", average, METH_VARARGS, "Calculate the average of a list of integers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef averagemodule = {
    PyModuleDef_HEAD_INIT,
    "average",
    "It is test module.",
    -1,
    AverageMethods
};

PyMODINIT_FUNC
PyInit_average(void)
{
    return PyModule_Create(&averagemodule);
}
