/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _CALCULADORA_H_RPCGEN
#define _CALCULADORA_H_RPCGEN

#include <rpc/rpc.h>


#ifdef __cplusplus
extern "C" {
#endif


struct intpair {
	int a;
	int b;
};
typedef struct intpair intpair;

#define CALCULADORA_PROG 0x23451111
#define CALCULADORA_VERS 1

#if defined(__STDC__) || defined(__cplusplus)
#define suma 1
extern  int * suma_1(intpair *, CLIENT *);
extern  int * suma_1_svc(intpair *, struct svc_req *);
#define resta 2
extern  int * resta_1(intpair *, CLIENT *);
extern  int * resta_1_svc(intpair *, struct svc_req *);
#define multiplicacion 3
extern  int * multiplicacion_1(intpair *, CLIENT *);
extern  int * multiplicacion_1_svc(intpair *, struct svc_req *);
#define division 4
extern  float * division_1(intpair *, CLIENT *);
extern  float * division_1_svc(intpair *, struct svc_req *);
extern int calculadora_prog_1_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define suma 1
extern  int * suma_1();
extern  int * suma_1_svc();
#define resta 2
extern  int * resta_1();
extern  int * resta_1_svc();
#define multiplicacion 3
extern  int * multiplicacion_1();
extern  int * multiplicacion_1_svc();
#define division 4
extern  float * division_1();
extern  float * division_1_svc();
extern int calculadora_prog_1_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_intpair (XDR *, intpair*);

#else /* K&R C */
extern bool_t xdr_intpair ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_CALCULADORA_H_RPCGEN */