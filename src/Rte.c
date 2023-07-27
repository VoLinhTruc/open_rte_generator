#include "Rte.h"
#include "Rte_Type.h"

#ifdef __cplusplus
extern "C" {
#endif

Std_ReturnType Rte_Write_ASW1_PP_ASW1_PP1_VDP_ASW1_Var1(IDT_ASW1_uint32 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            ASW1_PP_ASW1_PP1_VDP_ASW1_Var1 = data;

            ASW2_RP_ASW2_RP1_VDP_ASW1_Var1 = ASW1_PP_ASW1_PP1_VDP_ASW1_Var1;

            return rtn;
        }
                
Std_ReturnType Rte_Write_ASW1_PP_ASW1_PP2_VDP_ASW1_Var2(IDT_ASW1_uint32 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            ASW1_PP_ASW1_PP2_VDP_ASW1_Var2 = data;

            ASW3_RP_ASW3_RP1_VDP_ASW1_Var2 = ASW1_PP_ASW1_PP2_VDP_ASW1_Var2;

            return rtn;
        }
                
Std_ReturnType Rte_Write_ASW2_PP_ASW2_PP1_VDP_ASW2_Var1(IDT_ASW2_uint32 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            ASW2_PP_ASW2_PP1_VDP_ASW2_Var1 = data;

            ASW1_RP_ASW1_RP1_VDP_ASW2_Var1 = ASW2_PP_ASW2_PP1_VDP_ASW2_Var1;

            return rtn;
        }
                
Std_ReturnType Rte_Write_ASW3_PP_ASW3_PP1_VDP_ASW3_Var1(IDT_ASW3_uint32 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            ASW3_PP_ASW3_PP1_VDP_ASW3_Var1 = data;

            ASW1_RP_ASW1_RP2_VDP_ASW3_Var1 = ASW3_PP_ASW3_PP1_VDP_ASW3_Var1;

            return rtn;
        }
                
Std_ReturnType Rte_Write_DcmSample_Provider_PP_DcmSample_Provider_PP1_VDP_DcmSample_Provider_Var1(IDT_DcmSample_Provider_uint8 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            DcmSample_Provider_PP_DcmSample_Provider_PP1_VDP_DcmSample_Provider_Var1 = data;

            DcmSample_Requester_RP_DcmSample_Requester_RP1_VDP_DcmSample_Provider_Var1 = DcmSample_Provider_PP_DcmSample_Provider_PP1_VDP_DcmSample_Provider_Var1;

            return rtn;
        }
                
Std_ReturnType Rte_Write_DcmSample_Requester_PP_DcmSample_Requester_PP1_VDP_DcmSample_Requester_Var1(IDT_DcmSample_Requester_uint8 data)
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            DcmSample_Requester_PP_DcmSample_Requester_PP1_VDP_DcmSample_Requester_Var1 = data;

            DcmSample_Provider_RP_DcmSample_Provider_RP1_VDP_DcmSample_Requester_Var1 = DcmSample_Requester_PP_DcmSample_Requester_PP1_VDP_DcmSample_Requester_Var1;

            return rtn;
        }
                
IDT_ASW2_uint32 Rte_DRead_ASW1_RP_ASW1_RP1_VDP_ASW2_Var1(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = ASW1_RP_ASW1_RP1_VDP_ASW2_Var1;

            return rtn;
        }
                
IDT_ASW3_uint32 Rte_DRead_ASW1_RP_ASW1_RP2_VDP_ASW3_Var1(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = ASW1_RP_ASW1_RP2_VDP_ASW3_Var1;

            return rtn;
        }
                
IDT_ASW1_uint32 Rte_DRead_ASW2_RP_ASW2_RP1_VDP_ASW1_Var1(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = ASW2_RP_ASW2_RP1_VDP_ASW1_Var1;

            return rtn;
        }
                
IDT_ASW1_uint32 Rte_DRead_ASW3_RP_ASW3_RP1_VDP_ASW1_Var2(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = ASW3_RP_ASW3_RP1_VDP_ASW1_Var2;

            return rtn;
        }
                
IDT_DcmSample_Requester_uint8 Rte_DRead_DcmSample_Provider_RP_DcmSample_Provider_RP1_VDP_DcmSample_Requester_Var1(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = DcmSample_Provider_RP_DcmSample_Provider_RP1_VDP_DcmSample_Requester_Var1;

            return rtn;
        }
                
IDT_DcmSample_Provider_uint8 Rte_DRead_DcmSample_Requester_RP_DcmSample_Requester_RP1_VDP_DcmSample_Provider_Var1(void )
        {
            IDT_DcmSample_Provider_uint8 rtn;

            rtn = DcmSample_Requester_RP_DcmSample_Requester_RP1_VDP_DcmSample_Provider_Var1;

            return rtn;
        }
                

#ifdef __cplusplus
}
#endif

