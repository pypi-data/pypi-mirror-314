#include <Python.h>

static PyObject *
hello(PyObject *self, PyObject *args) {
    printf("hello world\n");  // Simple print statement
    Py_RETURN_NONE;
}

static PyMethodDef hello_methods[] = {
    {"hello", hello, METH_VARARGS, "Say hello"},
};

static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT, "conda_build_test", "", -1, hello_methods
};

PyMODINIT_FUNC PyInit_hello(void) {
    return PyModule_Create(&hellomodule);
}
