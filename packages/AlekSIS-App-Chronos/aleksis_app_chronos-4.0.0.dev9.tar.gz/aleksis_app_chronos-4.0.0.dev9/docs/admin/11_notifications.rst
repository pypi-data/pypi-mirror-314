Setup notifications about current changes
=========================================

Users can get notifications about current changes to their personal timetables.
To activate this behavior, the system administrator has to ensure multiple things:

* The data come from a compatible source, for example, AlekSIS-App-Untis.
* The notifications have been activated in the preferences (see below).
* There is at least one notification channel available to your users (cf. :ref:`core-admin-notifications`).

Preferences
-----------

You can customize the way how and when notifications are sent at the configuration page at **Admin → Configuration → Timetables**:

* **Send notifications for current timetable changes:** With this checkbox, the whole feature can be activated or deactivated.
* **How many days in advance users should be notified about timetable changes?** Here the number of days can be configured notifications will be sent 
  before the actual affected day. A common value is one or two days.
* **Time for sending notifications about timetable changes:** At this time, the notifications for the next days will be sent. 
  This is only used if the changes are created before the period configured with the above mentioned option. If they affect a day in this period,
  the notification will be sent immediately.
