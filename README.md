# Josh's Schedule Synchronizer

Here's the "problem:" I use a Google Sheets spreadsheet to maintain all my public appearances. 
I check the spreadsheet as often as possible to know where to be and when. I check every morning and every night, before bed.
But, sometimes I get tied into work and forget that I've got a meeting. This is where it would be useful to have a Google Calendar notification 
telling me I have an important meeting in 10 minutes or something like that. So, my solution is to read that data from the
spreadsheet and use it to populate calendar events that have as many nagging reminders as possible. 

Sometimes things change, so this action will _delete_ any calendar notifications that haven't been changed in any way 
if the start and stop time don't line up. Maybe it'll figure out which ones to delete by looking for a unique string in 
the calendar event. 

