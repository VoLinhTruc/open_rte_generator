#include "Arduino.h"
#include "freertos/FreeRTOS.h"


#ifdef __cplusplus
extern "C" {
#endif

extern void OS_1Q1_1000ms_Task();
extern void OS_1Q1_10ms_Task();


#ifdef __cplusplus
}
#endif

void esc_stack_EventList_OS_1000ms_Task( void * pvParameters )
{
	TickType_t xLastWakeTime;
	const TickType_t xFrequency = 1000;

	for(;;)
	{
		(void) OS_1Q1_1000ms_Task();

		vTaskDelayUntil( &xLastWakeTime, xFrequency );
	}
}
void esc_stack_EventList_OS_10ms_Task( void * pvParameters )
{
	TickType_t xLastWakeTime;
	const TickType_t xFrequency = 10;

	for(;;)
	{
		(void) OS_1Q1_10ms_Task();

		vTaskDelayUntil( &xLastWakeTime, xFrequency );
	}
}


 
void setup() {
  // put your setup code here, to run once:
  	xTaskCreate(esc_stack_EventList_OS_1000ms_Task, "esc_stack_EventList_OS_1000ms_Task", 2000, NULL, 4, NULL);
	xTaskCreate(esc_stack_EventList_OS_10ms_Task, "esc_stack_EventList_OS_10ms_Task", 2000, NULL, 20, NULL);

}

void loop() {
  // put your main code here, to run repeatedly:
}   
