#include "calculadora.h"
#include <stdio.h>
#include <stdlib.h>

void calculadora_prog_1(char *host, int a, int b) {
    CLIENT *clnt;
    intpair params;
    int *result_1;
    float *result_2;

    clnt = clnt_create(host, CALCULADORA_PROG, CALCULADORA_VERS, "udp");
    if (clnt == NULL) {
        clnt_pcreateerror(host);
        exit(1);
    }

    params.a = a;
    params.b = b;

    //suma
    result_1 = suma_1(&params, clnt);
    if (result_1 == NULL) {
        clnt_perror(clnt, "call failed");
    } else {
        printf("Suma: %d + %d = %d\n", a, b, *result_1);
    }

    //resta
    result_1 = resta_1(&params, clnt);
    if (result_1 == NULL) {
        clnt_perror(clnt, "call failed");
    } else {
        printf("Resta: %d - %d = %d\n", a, b, *result_1);
    }

    //multiplicación
    result_1 = multiplicacion_1(&params, clnt);
    if (result_1 == NULL) {
        clnt_perror(clnt, "call failed");
    } else {
        printf("Multiplicación: %d * %d = %d\n", a, b, *result_1);
    }

    //división
    result_2 = division_1(&params, clnt);
    if (result_2 == NULL) {
        clnt_perror(clnt, "call failed");
    } else {
        printf("División: %d / %d = %.2f\n", a, b, *result_2);
    }

    clnt_destroy(clnt);
}

int main(int argc, char *argv[]) {
    char *host;
    int a, b;

    if (argc < 4) {
        printf("usage: %s server_host num1 num2\n", argv[0]);
        exit(1);
    }

    host = argv[1];
    a = atoi(argv[2]);
    b = atoi(argv[3]);

    calculadora_prog_1(host, a, b);
}

