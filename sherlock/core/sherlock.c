#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyObject *get_pyobject(PyObject *frame) {
    PyThreadState *tstate = PyThreadState_GET();
}