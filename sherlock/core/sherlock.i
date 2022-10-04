/* File : example.i */
%module example
%{
PyObject *get_pyobject(PyObject *list);
%}
PyObject *get_pyobject(PyObject *list);