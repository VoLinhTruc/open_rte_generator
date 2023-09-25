/*<RBHead>
*************************************************************************
* *
* ROBERT BOSCH GMBH *
* STUTTGART *
* *
* Alle Rechte vorbehalten - All rights reserved *
* *
*************************************************************************
*
*   __   __   ___  ___
*  /_ / /  / /__  /    /__/
* /__/ /__/ __ / /__  /  /
*
*
*************************************************************************
* Administrative Information (automatically filled in by eASEE) *
*************************************************************************
*
* $Filename__:$
*
* $Author____:$
*
* $Function__:$
*
*************************************************************************
* $Domain____:$
* $User______:$
* $Date______:$
* $Class_____:$
* $Name______:$
* $Variant___:$
* $Revision__:$
* $Type______:$
* $State_____:$
*
*************************************************************************
* List Of Changes
*
* $History___:
*
*
* $
*
*
***************************************************************************************************
</RBHead>*/

#include "Arduino.h"
#include "SRF05.h"
#include "ASW3.h"

#define SRF05_TRIGGER_PIN 2
#define SRF05_ECHO_PIN 39
SRF05 SRF(SRF05_TRIGGER_PIN, SRF05_ECHO_PIN);

void ASW3_10ms()
{
    static uint8 first_cycle_run_done = ASW3_FIRST_CYCLE_RUN_NOT_DONE;

    if (first_cycle_run_done == ASW3_FIRST_CYCLE_RUN_NOT_DONE)
    {
        // Implementation for the first cycle
        SRF.setCorrectionFactor(1.035);
        SRF.setModeAverage(10);

        first_cycle_run_done = ASW3_FIRST_CYCLE_RUN_DONE;
    }
    else
    {
        // Cyclelic implementation
        static uint8 counter_for_1_second = 0;
        counter_for_1_second = ++counter_for_1_second % 10;
        if (counter_for_1_second == 0)
        {
            static uint32 asw3_counter = 0;
            asw3_counter++;
            Rte_Write_PP_ASW3_PP1_VDP_ASW3_Var1(asw3_counter*3);
            
            uint32 distance;
            distance = SRF.getMillimeter();
            Rte_Write_PP_ASW3_PP2_VDP_ASW3_Var2(distance);
            
            Serial.println("ASW3_PP2_VDP_ASW3_Var2: " + String(distance));

            // Serial.print("ASW3 receive from ASW1");
            // Serial.print(" ");
            // Serial.print(Rte_DRead_RP_ASW3_RP1_VDP_ASW1_Var2());
            // Serial.println();
        }
    }
}
