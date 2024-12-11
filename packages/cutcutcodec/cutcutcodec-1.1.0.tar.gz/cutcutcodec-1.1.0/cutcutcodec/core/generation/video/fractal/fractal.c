/* Fast generation of fractal. */

#define PY_SSIZE_T_CLEAN
#include <numpy/arrayobject.h>
#include <omp.h>
#include <Python.h>


void mandelbrot_longdouble(float *iters, long double *cst_reals, long double *cst_imags, const npy_intp dim, const long int iter_max) {
  npy_intp i, j;
  const float iter_max_float=(float)iter_max;
  #pragma omp parallel for schedule(dynamic)
  for ( i = 0; i < dim; ++i ) {
    long double real, imag, cst_real, cst_imag, real_square, imag_square;
    cst_real = cst_reals[i], cst_imag = cst_imags[i];
    real = cst_real, imag = cst_imag;
    real_square = real*real, imag_square = imag*imag;
    for ( j = 0; j < iter_max && real_square + imag_square <= 4.0L; ++j ) {
      imag = 2.0L*real*imag + cst_imag;
      real = real_square - imag_square + cst_real;
      real_square = real*real, imag_square = imag*imag;
    }
    iters[i] = (float)j / iter_max_float;
  }
}


void mandelbrot_double(float *iters, double *cst_reals, double *cst_imags, const npy_intp dim, const long int iter_max) {
  npy_intp i, j;
  const float iter_max_float=(float)iter_max;
  #pragma omp parallel for schedule(dynamic)
  for ( i = 0; i < dim; ++i ) {
    double real, imag, cst_real, cst_imag, real_square, imag_square;
    { // simd
      cst_real = cst_reals[i], cst_imag = cst_imags[i];
      real = cst_real, imag = cst_imag;
      real_square = real*real, imag_square = imag*imag;
    };
    for ( j = 0; j < iter_max && real_square + imag_square <= 4.0; ++j ) {
      imag = 2.0*real*imag + cst_imag;
      real = real_square - imag_square + cst_real;
      real_square = real*real, imag_square = imag*imag; // simd
    }
    iters[i] = (float)j / iter_max_float;
  }
}


static PyObject *py_mandelbrot(PyObject *self, PyObject *args) {
  PyArrayObject *iters, *reals, *imags;
  long int iter_max;
  npy_intp dim;

  // parse arguments alloc new array
  if ( !PyArg_ParseTuple(args, "O!O!l", &PyArray_Type, &reals, &PyArray_Type, &imags, &iter_max) ) {
    return NULL;
  }
  dim = PyArray_DIM(reals, 0);
  iters = (PyArrayObject *)PyArray_SimpleNew(1, &dim, NPY_FLOAT32);
  if ( NULL == iters ) {
    PyErr_SetString(PyExc_RuntimeError, "failed to create a new array");
    return NULL;
  }

  // call c func
  switch(PyArray_TYPE(reals)) {
  case NPY_DOUBLE:
    Py_BEGIN_ALLOW_THREADS
    mandelbrot_double(
      (float *)PyArray_DATA(iters),
      (double *)PyArray_DATA(reals),
      (double *)PyArray_DATA(imags),
      dim,
      iter_max
    );
    Py_END_ALLOW_THREADS
    return (PyObject *)iters;
  case NPY_LONGDOUBLE:
    Py_BEGIN_ALLOW_THREADS
    mandelbrot_longdouble(
      (float *)PyArray_DATA(iters),
      (long double *)PyArray_DATA(reals),
      (long double *)PyArray_DATA(imags),
      dim,
      iter_max
    );
    Py_END_ALLOW_THREADS
    return (PyObject *)iters;
  default:
    PyErr_SetString(PyExc_TypeError, "only the types double and long double are accepted");
    Py_DECREF(iters);
    return NULL;
  }
}


static PyMethodDef fractalMethods[] = {
  {"mandelbrot", py_mandelbrot, METH_VARARGS, "Function for calculating mandelbrot in C."},
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef fractal = {
  PyModuleDef_HEAD_INIT,
  "fractal",
  "Fast C fractal module.",
  -1,
  fractalMethods
};


PyMODINIT_FUNC PyInit_fractal(void)
{
  import_array();
  return PyModule_Create(&fractal);
}
