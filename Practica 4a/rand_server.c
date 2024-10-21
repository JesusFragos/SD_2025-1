#include "calculadora.h"
#include <stdio.h>

//  función suma
int *suma_1_svc(intpair *argp, struct svc_req *rqstp) {
    static int result;
    result = argp->a + argp->b;
    printf("Suma: %d + %d = %d\n", argp->a, argp->b, result);
    return &result;
}

//función resta
int *resta_1_svc(intpair *argp, struct svc_req *rqstp) {
    static int result;
    result = argp->a - argp->b;
    printf("Resta: %d - %d = %d\n", argp->a, argp->b, result);
    return &result;
}

// función multiplicacion
int *multiplicacion_1_svc(intpair *argp, struct svc_req *rqstp) {
    static int result;
    result = argp->a * argp->b;
    printf("Multiplicacion: %d * %d = %d\n", argp->a, argp->b, result);
    return &result;
}

// función division
float *division_1_svc(intpair *argp, struct svc_req *rqstp) {
    static float result;
    if (argp->b == 0) {
        printf("Error: División entre 0\n");
        result = 0.0;
    } else {
        result = (float)argp->a / (float)argp->b;
        printf("Division: %d / %d = %.2f\n", argp->a, argp->b, result);
    }
    return &result;
}

