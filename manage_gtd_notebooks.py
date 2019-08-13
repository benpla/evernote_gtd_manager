# This file is part of the evernote_gtd_manager distribution (https://github.com/benpla/evernote_gtd_manager.git).
#
# Copyright © 2017 - 2019 by Benny Platte
# Licensed under the EUPL 1.2 (European Union Public Licence 1.2)
# Licence text is available in different languages under https://joinup.ec.europa.eu/collection/eupl/eupl-text-11-12
#
# The Licensor Benny Platte hereby grants a worldwide, royalty-free, non-exclusive, sublicensable licence to
#   — use the Work in any circumstance and for all usage, reproduce the Work,
#   — modify the Work, and make Derivative Works based upon the Work,
#   — communicate to the public, including the right to make available or display the Work to the public
#   — distribute the Work or copies thereof,
#
# Obligations of the Licensee:
#   - The Licensee shall keep intact all copyright, patent or trademarks notices
#   - The Licensee must include a copy of such notices and a copy of the Licence with every copy of the Work
#
# Liability:
#   The Licensor will in no event be liable for any direct or indirect, material or moral, damages of any kind, arising out of the Licence or of the use of the Work, including without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any commercial damage


from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as EnTypes
import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.edam.error.ttypes import EDAMUserException
from evernote.edam.error.ttypes import EDAMSystemException
from evernote.edam.error.ttypes import EDAMErrorCode
import datetime
import sys
import re
import evernoteApiKeys


class myEvernote(object):

    def __init__(self, kontoname):
        if kontoname == "loipe":
            self._connect_to_evernote(evernoteApiKeys.dev_tokenLoipe, istSandbox=False)
        else:
            self._connect_to_evernote(evernoteApiKeys.dev_tokenSandbox, istSandbox = True)


    def _connect_to_evernote(self, dev_token, istSandbox=True):
        user = None
        try:
            self.client = EvernoteClient(token=dev_token, sandbox=istSandbox)
            self.user_store = self.client.get_user_store()
            self.notestore = self.client.get_note_store()
            user = self.user_store.getUser()
        except EDAMUserException as e:
            err = e.errorCode
            print("Error attempting to authenticate to Evernote: %s - %s" % (
            EDAMErrorCode._VALUES_TO_NAMES[err], e.parameter))
            return False
        except EDAMSystemException as e:
            err = e.errorCode
            print("Error attempting to authenticate to Evernote: %s - %s" % (
            EDAMErrorCode._VALUES_TO_NAMES[err], e.message))
            sys.exit(-1)

        if user:
            print("Authenticated to evernote as user %s" % user.username)
            return True
        else:
            return False



def GetFirstDayInWeek(datum):
    # previous Monday
    dateOfFirstDayInWeek = datum + datetime.timedelta(days=-datum.weekday(), weeks=0)
    return dateOfFirstDayInWeek


def GetFirstDaysOfWeeksBetween(start_date, end_date):
    dateOfFirstDayInWeek = GetFirstDayInWeek(start_date)
    current_date =dateOfFirstDayInWeek  # start_date + datetime.timedelta(days=7-subtract_days)
    weeks_between = []
    while current_date <= end_date:
        weeks_between.append(current_date)
        # weeks_between.append(
        #     '{}{:02d}'.format(*current_date.isocalendar()[:2])
        # )
        current_date += datetime.timedelta(days=7)
    return weeks_between


def GetWeekString(weekStartDay):
    monthShortGerman = ['Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
    weeknumber = weekStartDay.isocalendar()[1]
    weekEndDay = weekStartDay + datetime.timedelta(days=7)

    # if weekStartDay.month == weekEndDay.month:
    #     daypart = "{d1:02d}.{m1}-{d2:02d}".format(d1=weekStartDay.day, d2=weekEndDay.day,
    #                                                   m1=monthShortGerman[weekStartDay.month-1])
    # else:
    #     daypart = "{d1:02d}.{m1}-{d2:02d}.{m2}".format(d1=weekStartDay.day, d2=weekEndDay.day,
    #                                                            m1=monthShortGerman[weekStartDay.month-1],
    #                                                            m2=monthShortGerman[weekEndDay.month-1])
    if weekStartDay.month == weekEndDay.month:
        daypart = "{d1:02d}.{m1}".format(d1=weekStartDay.day, d2=weekEndDay.day,
                                                      m1=monthShortGerman[weekStartDay.month-1])
    else:
        daypart = "{d1:02d}.{m1}".format(d1=weekStartDay.day, d2=weekEndDay.day,
                                                               m1=monthShortGerman[weekStartDay.month-1],
                                                               m2=monthShortGerman[weekEndDay.month-1])

    s = "{y:02d}w{w:02d}   {d}".format(y=weekEndDay.year - 2000,
                                     w=weeknumber,
                                     d=daypart)  # strftime("%Y-%m")
    return s



def GetNotebookSameWeekIfExists(dateOfAnyDayInThisWeek, notebookList):
    dateOfFirstDayInWeek = dateOfAnyDayInThisWeek + datetime.timedelta(days=-dateOfAnyDayInThisWeek.weekday(), weeks=0)

    weeknumber = dateOfFirstDayInWeek.isocalendar()[1]
    weekLastDay = dateOfFirstDayInWeek + datetime.timedelta(days=6)

    for nb in notebookList:
        regex = re.search("(?P<jahr>\d\d)w(?P<wochennummer>\d\d)", nb.name)
        # nb = [n for n in nbooksWv if re.search("(?P<jahr>\d\d)w(?P<wochennummer>\d\d)",nb.name)]
        if regex <> None:
            nbYear = int(regex.group('jahr')) + 2000
            nbWeeknumber = int(regex.group('wochennummer'))

            if nbYear == weekLastDay.year and nbWeeknumber == weeknumber:
                # notebook with same week found
                return nb

    return None



# def deleteOverdueNotebooks(EvernoteObject, date):
#     isRemindertimeBeforeCurrentWeek = remindertime < GetFirstDayInWeek(datetime.datetime.today())
#     notebooks = EvernoteObject.notestore.listNotebooks()
#     # Notebooks in stack 'Wiedervorlage' heraussuchen
#     nbooksWv = [n for n in notebooks if n.stack == stackName]


def createOrUpdateNotebooksWeeks(EvernoteObject, startdate, enddate, stackName, dateOverdue=None):
    weeks = GetFirstDaysOfWeeksBetween(startdate, enddate)

    notebooks = EvernoteObject.notestore.listNotebooks()
    # search notebooks in stack
    nbooksWv = [n for n in notebooks if n.stack == stackName]

    # iterate all weeks
    for weekday in weeks:
        weeknumber = weekday.isocalendar()[1]
        weekString = GetWeekString(weekday)

        # notebook exists in this week?
        existingNotebookInThisWeek = GetNotebookSameWeekIfExists(weekday, nbooksWv)
        if existingNotebookInThisWeek == None:
            # create new notebook
            notebook = EnTypes.Notebook()
            notebook.name = weekString
            notebook.stack = stackName
            notebook = EvernoteObject.notestore.createNotebook(notebook)
            msg = "created new notebook '" + notebook.name + "'"
        else:
            if dateOverdue <> None and weekday.date() < dateOverdue.date():
                # Notebook is obsolete
                noteFilter = NoteStoreTypes.NoteFilter(notebookGuid=existingNotebookInThisWeek.guid)
                spec = NoteStoreTypes.NotesMetadataResultSpec()
                notelist = EvernoteObject.notestore.findNotesMetadata(noteFilter, 0, 10, spec)
                #if notelist.totalNotes > 0:
                    # it contains notes
                oldName = existingNotebookInThisWeek.name
                existingNotebookInThisWeek.name = weekString + ": overdue!"
                notebook = EvernoteObject.notestore.updateNotebook(existingNotebookInThisWeek)
                msg = "overdue notebook '{o}' contains {cnt:d} Notes, rename to '{new}'".format(
                    o=oldName, cnt=notelist.totalNotes, new=existingNotebookInThisWeek.name)
                # else:
                #     # it contains no notes: delete notebook
                #     EvernoteObject.notestore.deleteNotebook(existingNotebookInThisWeek)

            else:
                # Notebook belongs to current or future week
                if weekString == existingNotebookInThisWeek.name:
                    # new name the same as old, so don't update anything
                    msg = "existing notebook '" + existingNotebookInThisWeek.name + "' name is correct, no update required"
                else:
                    # Update existing notebook
                    oldName = existingNotebookInThisWeek.name
                    existingNotebookInThisWeek.name = weekString
                    notebook = EvernoteObject.notestore.updateNotebook(existingNotebookInThisWeek)
                    msg = "updated existing notebook '" + oldName + "' to '" + existingNotebookInThisWeek.name + "'"

        print "    {msg}".format(msg=msg)




def GetAllNotesWithFilter(EvernoteObject, filterText):
    nFilter = NoteStoreTypes.NoteFilter()
    nFilter.words = filterText # "reminderOrder:*"
    # filter.notebookGuid = "SomeNotebookGuidHere"
    # filter.tagGuids = ["tagGuid1", "tagGuid2"]

    rSpec = NoteStoreTypes.NotesMetadataResultSpec()
    rSpec.includeTitle = True
    rSpec.includeAttributes = True
    rSpec.includeNotebookGuid = True

    notesMetadataList = EN.notestore.findNotesMetadata(nFilter, 0, 50, rSpec)
    return notesMetadataList.notes



def moveNoteToMatchingReminderTimeNotebook(EvernoteObject, note, stackName):
    remindertime = datetime.datetime.fromtimestamp(note.attributes.reminderTime / 1000)

    isRemindertimeBeforeCurrentWeek = remindertime < GetFirstDayInWeek(datetime.datetime.today())
    if isRemindertimeBeforeCurrentWeek:
        # Reminder is BEFORE this week, so sort in overdue
        notebooks = EvernoteObject.notestore.listNotebooks()
        destinationNotebook = [nb for nb in notebooks if nb.name == "_overdue"][0]

    else:
        # Reminder is now or in the future: sort into the appropriate week notebook
        # if notebook of week of reminder date not available, create it
        createOrUpdateNotebooksWeeks(EN, remindertime, remindertime, stackName)

        # re-read notebooks if a notebook was changed or newly created by the previous command
        notebooks = EvernoteObject.notestore.listNotebooks()
        # get notebooks in stack
        nbooksWv = [n for n in notebooks if n.stack == stackName]

        # Notebook suitable for the desired week
        destinationNotebook = GetNotebookSameWeekIfExists(rem, nbooksWv)

    # search the notebook of this note
    currentNotebook = [nb for nb in notebooks if nb.guid == note.notebookGuid][0]

    if note.notebookGuid == destinationNotebook.guid:
        print (
            "    Notebook: '{nb}'  --> OK, Note sorted into correct notebook".format(nb=currentNotebook.name))
    else:
        print ("    Notebook: '{nb}'  --> wrong notebook, move to '{nbTo}'".format(
            nb=currentNotebook.name,
            nbTo=destinationNotebook.name))
        # move note
        note.notebookGuid = destinationNotebook.guid
        note = EvernoteObject.notestore.updateNote(note)




wiedervorlageStackName = "Aktionen WV"


if __name__ == '__main__':
    #EN = myEvernote("sandbox")
    EN = myEvernote("loipe")

    start = datetime.datetime.today()  # datetime.date(2019, 07, 01)
    #start = datetime.datetime(2019, 07, 01)
    end = datetime.datetime(2020, 07, 30)
    mondayOfTodaysWeek = GetFirstDayInWeek(datetime.datetime.today())
    createOrUpdateNotebooksWeeks(EN, start, end, wiedervorlageStackName, mondayOfTodaysWeek)
    exit(1)
    reminderNotes = GetAllNotesWithFilter(EN, "reminderTime:* -reminderDoneTime:*")  # )

    #reminderNotes = GetAllNotesWithFilter(EN, "")

    print "Found {n:d} notes".format(n = len(reminderNotes))

    for note in reminderNotes:
        if note.attributes.reminderOrder is None:
            continue

        remCreated = datetime.datetime.fromtimestamp(note.attributes.reminderOrder/1000)
        rem = datetime.datetime.fromtimestamp(note.attributes.reminderTime / 1000)
        if note.attributes.reminderDoneTime <> None:
            # Reminder ist erledigt
            remDone = datetime.datetime.fromtimestamp(note.attributes.reminderDoneTime / 1000)
            remDoneString = "\n    " + remDone.strftime('%Y-%m-%d %H:%M')
        else:
            # Reminder ist nicht erledigt
            remDone = None
            remDoneString = ""
            moveNoteToMatchingReminderTimeNotebook(EN, note, wiedervorlageStackName)

        print
        print "{t}\n    created {rc}\n    rem {r}{rd}".format(t = note.title,
            rc = remCreated.strftime('%Y-%m-%d %H:%M'),
            r = rem.strftime('%Y-%m-%d %H:%M'),
            rd = remDoneString
        )


