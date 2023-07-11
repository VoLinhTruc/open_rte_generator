#include "freertos/FreeRTOS.h"
#include "freertos/FreeRTOS.h"

extern void OS_1Q1_1000ms_Task();

void esc_stack_EventList_OS_1000ms_Task( void * pvParameters )
{
	TickType_t xLastWakeTime;
	const TickType_t xFrequency = 1;

	for(;;)
	{
		(void) OS_1Q1_1000ms_Task();

		vTaskDelayUntil( &xLastWakeTime, xFrequency );
	}
}

xTaskCreate(esc_stack_EventList_OS_1000ms_Task, "esc_stack_EventList_OS_1000ms_Task");

