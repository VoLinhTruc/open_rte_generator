#include "Rte.h"
#include "Rte_Type.h"

#ifdef __cplusplus
extern "C" {
#endif

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

