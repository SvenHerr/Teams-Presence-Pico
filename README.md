# Teams-Presence-Pico
Python script to show Teams presence status on led.  The reciverer script runs on raspbery pi (pico) and the sender runs on windows.

Teams stores the log of status and a lot more locally in a Txt file.
The script looks for the last status in the log file and sends it to the receiver. Here we can display the status with lights or LEDs 
