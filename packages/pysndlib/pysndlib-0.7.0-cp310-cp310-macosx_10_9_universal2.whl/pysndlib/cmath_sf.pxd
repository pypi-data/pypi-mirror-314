#cython libc.math does not contain special functions
cdef extern from "<math.h>" nogil:
    double j0(double x)
    double j1(double x)
    double jn(int n, double x)
    double y0(double x)
    double y1(double x)
    double yn(int n, double x)



