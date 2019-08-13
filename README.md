# evernote_gtd_manager
It manages (create/update) notebooks and notes in Evernote according to GTD workflow

The program creates notebooks in a stack, one for each calendar week. It creates notebooks for future weeks. The name of the notebooks is defined in the function 'GetWeekString'. 
When starting the program, a date range must be specified in which a notebook is created for each calendar week in it.
Then all notebooks are read in and compared with the generated week names. If the week name or the week name is different (e.g. because the function 'GetWeekString' was changed), all affected notebooks will be renamed. 
In this way, different naming conventions for the weekly notebooks can be tested. 

Afterwards, all notes with unfinished reminders are read and sorted into the corresponding weekly notebook. Past unfinished reminders are sorted into the notebook "_overdue".

This script can run daily as a cron job. Thus the notes in the background are sorted automatically correctly and overdue ones are marked. Only the deletion of past notebook weeks has to be done manually. This functionality is not available in the API.

## Deutsch
Das Programm erzeugt Notizbücher in einem Stapel, eines für jede Kalenderwoche. Dabei werden Notizbücher für zukünftige Wochen erzeugt. Der Name bzw. die Bezeichnung der Notizbücher ist festgelegt in der Funktion 'GetWeekString'. 
Beim Start des Programms ist ein Datumsbereich anzugeben, in welchem für jede darin befindliche Kalenderwoche ein Notizbuch angelegt wird:

Anschließend werden alle Notizbücher eingelesen und mit den erzeugten Wochennamen verglichen. Sollte der Wochenname bzw. die Wochenbezeichnung anders lauten (weil z.B. die Funktion 'GetWeekString' geändert wurde), dann werden alle betroffenen Notizbücher umbenannt. 
Auf diese Weise können verschiedene Namenskonventionen für die Wochen-Notizbücher getestet werden. 

Im Anschluss daran werden alle Notizen mit unerledigten Erinnerungen gelesen und in das entsprechende Wochennotizbuch einsortiert. Vergangene unerledigte Erinnerungen werden in das Notizbuch "_overdue" einsortiert.

Dieses Skript kann als cron-Job täglich laufen. Damit werden die Notizen im Hintergrund automatisch korrekt einsortiert und überfällige gekennzeichnet. Nur das Löschen vergangener Notizbuch-Wochen muss manuell erfolgen. Diese Funktionalität ist in der API nicht vorhanden.
