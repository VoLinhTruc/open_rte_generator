
#ifndef RTE_ASW2_H
#define RTE_ASW2_H

#include "Rte_Type.h"

#ifdef __cplusplus
extern "C" {
#endif

extern IDT_ASW1_uint32 Rte_DRead_ASW2_RP_ASW2_RP1_VDP_ASW1_Var1(void ); 
extern Std_ReturnType Rte_Write_ASW2_PP_ASW2_PP1_VDP_ASW2_Var1(IDT_ASW2_uint32 data); 

#ifdef __cplusplus
}
#endif

#define Rte_DRead_RP_ASW2_RP1_VDP_ASW1_Var1() Rte_DRead_ASW2_RP_ASW2_RP1_VDP_ASW1_Var1() 
#define Rte_Write_PP_ASW2_PP1_VDP_ASW2_Var1(data) Rte_Write_ASW2_PP_ASW2_PP1_VDP_ASW2_Var1(data) 

#endif // RTE_ASW2