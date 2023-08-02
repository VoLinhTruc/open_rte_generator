
#ifndef RTE_ASW1_H
#define RTE_ASW1_H

#include "Rte_Type.h"

extern IDT_ASW2_uint32 Rte_DRead_ASW1_RP_ASW1_RP1_VDP_ASW2_Var1(void ); 
extern IDT_ASW3_uint32 Rte_DRead_ASW1_RP_ASW1_RP2_VDP_ASW3_Var1(void ); 
extern Std_ReturnType Rte_Write_ASW1_PP_ASW1_PP1_VDP_ASW1_Var1(IDT_ASW1_uint32 data); 
extern Std_ReturnType Rte_Write_ASW1_PP_ASW1_PP2_VDP_ASW1_Var2(IDT_ASW1_uint32 data); 
#define Rte_DRead_RP_ASW1_RP1_VDP_ASW2_Var1() Rte_DRead_ASW1_RP_ASW1_RP1_VDP_ASW2_Var1() 
#define Rte_DRead_RP_ASW1_RP2_VDP_ASW3_Var1() Rte_DRead_ASW1_RP_ASW1_RP2_VDP_ASW3_Var1() 
#define Rte_Write_PP_ASW1_PP1_VDP_ASW1_Var1(data) Rte_Write_ASW1_PP_ASW1_PP1_VDP_ASW1_Var1(data) 
#define Rte_Write_PP_ASW1_PP2_VDP_ASW1_Var2(data) Rte_Write_ASW1_PP_ASW1_PP2_VDP_ASW1_Var2(data) 

#endif // RTE_ASW1