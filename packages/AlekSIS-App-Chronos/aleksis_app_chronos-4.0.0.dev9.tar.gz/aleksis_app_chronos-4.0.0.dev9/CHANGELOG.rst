Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`4.0.0.dev9`_ - 2024-12-08
--------------------------

Added
~~~~~

* Substitution planning interface based on teacher absences.

`4.0.0.dev8`_ - 2024-10-17
--------------------------

Upgrade notice
~~~~~~~~~~~~~~

If you're updating from 3.x, there is a migration path to use.
Therefore, please install ``AlekSIS-App-Lesrooster`` which now
includes parts of the legacy Chronos and the migration path.

Added
~~~~~

* New timetable interface based on calendar system.
* Dialog for fast changing lessons and creating substitutions in the calendar. 
* [Dev] LessonEvent and SupervisionEvent basing on calendar system.

Changed
~~~~~~~

* Substitution table was updated to new frontend.
* Substitution PDF was updated to new timetable interface and 
  therefore has a slightly different look.

Removed
~~~~~~~

* Legacy timetable frontend.

`3.0.2`_ - 2023-09-10
---------------------

Fixed
~~~~~

* Remove lessons replaced by events from "My timetable"

`3.0.1`_ - 2023-07-20
---------------------

Fixed
~~~~~

* [Dev] Sample data were broken due to using old room model.

`3.0`_ - 2023-05-14
-------------------

Changed
~~~~~~~

* Translations were updated.

`3.0b0`_ - 2023-02-16
---------------------

This version requires AlekSIS-Core 3.0. It is incompatible with any previous
version.

Removed
~~~~~~~

* `Room` model is now available in AlekSIS-Core 3.0
* Legacy menu integration for AlekSIS-Core pre-3.0

Added
~~~~~

* Support for SPA in AlekSIS-Core 3.0

Changed
~~~~~~~

* Improve rendering of substituted or cancelled items on daily lessons/supervisions pages.

Fixed
~~~~~

* The daily lessons page did not work correctly due to faulty pre-filtering of lessons.
* Substitution form teacher selections also included students in some cases
* Getting the max and min periods for events failed due to using always the current school term.
  Typically, that caused problems when the schedule changed (more or less periods on a day). 

`2.5`_ - 2022-11-12
-------------------

Added
~~~~~

* Add overview page of all daily supervisions.
* Add form to add substitutions to supervisions.
* Add filter to daily lessons page.
* Display initial lesson data with substituted lessons in daily lessons table.

`2.4.2`_ - 2022-11-02
---------------------

Fixed
~~~~~

* The date picker did not work with some date formats.
* Send notifications for changes done via daily lessons page.
* Lessons with same subject and groups but different teachers were not considered equal.
* Lessons without any groups were displayed as cancelled if there was an event in the same time period.

`2.4.1`_ - 2022-08-31
---------------------

Fixed
~~~~~

* The week and lesson period fields in the edit substitution form could be changed
  and the comment field was missing.

`2.4`_ - 2022-06-23
-------------------

Added
~~~~~

* Add Ukrainian locale (contributed by Sergiy Gorichenko from Fre(i)e Software GmbH).

Changed
~~~~~~~

* Change the icon set to iconify.
* Remove the update() method in AutomaticPlan (it is inherited from LiveDocument in Resint).

Fixed
~~~~~

* Optimize exam model and add reference to exams at extra lessons.
* Lessons weren't shown as cancelled on teacher or room timetables
  if events had replaced them.
* The teacher dropdown in the substitution edit form did not contain suggestions.
* The URLs containing the term "substitution" were missspelled.

`2.3`_ - 2022-03-21
-------------------

Added
~~~~~

* Add support for notifications about current changes to the users' timetables.

Fixed
~~~~~

* *All timetables* showed teachers and rooms from all school terms and not only the current.

`2.2.1`_ - 2022-02-13
---------------------

Fixed
~~~~~

* Substitution table was not usable on mobile devices.

`2.2`_ - 2022-01-12
-------------------

Changed
~~~~~~~

* Ignore lesson background colour if it is the same as the foreground colour.
* Added link to class register week view for users of the Alsijil class register.

`2.1`_ - 2022-01-04
-------------------

Added
~~~~~

* Add support for automatically generating PDF files of substitutions plans on data changes.
* Display warning if no timetable exists in one category.

Changed
~~~~~~~

* The subject linked to a group can now be edited in the normal group edit form.
* Names of subjects no longer have to be unique (short names still have to be).
* Update German translations.

Fixed
~~~~~

* Events replace normal lesson periods in all views.
* Announcements weren't shown on substitutions printout.
* Do registration of additional fields in `form_extensions` module.
* Automatic plan update failed if objects were deleted.

`2.0`_ - 2021-10-30
-------------------

Changed
~~~~~~~

* Improve the formatting of the print version of the substitution plan
  * Reduce the page margin.
  * Reduce the space between the header and the heading.
  * Display block of absences as a table.

Fixed
~~~~~

* Do not show substitutions on regular timetables.

`2.0rc3`_ - 2021-09-24
----------------------

Changed
~~~~~~~

* Support dates for ``TimePeriod.get_datetime_start`` and ``TimePeriod.get_datetime_end``.
* Update translations.

Fixed
~~~~~

* ``Event.__str__`` returned a proxy type instead a string.

`2.0rc2`_ - 2021-08-01
----------

Fixed
~~~~~

* Drop usage of non-existing permission in permission rules for lesson substitutions.

`2.0rc1`_ - 2021-06-23
----------------------

Changed
~~~~~~~

* Use semantically correct html elements for headings and alerts.

`2.0b3`_ - 2021-06-16
----------

Changed
~~~~~~~

* Use a more speaking name for preference section ("Timetables" instead of "Chronos").

Fixed
~~~~~

* Preference section verbose names were displayed in server language and not
  user language (fixed by using gettext_lazy).
* Affected groups and persons in substitutions list were displayed multiple times.
* ``lessons_on_day`` didn't work as expected if a person has no lessons.
* End of validity ranges list wasn't detected correctly in ``next_lesson``.

`2.0b2` - 2021-06-02
--------------------

Fixed
~~~~~

* Migration path was ambigious
* Unique constraints for breaks and substitutions were too tight
* Absences in substitutions list were displayed multiple times.

`2.0b1`_ - 2021-05-22
---------------------

Fixed
~~~~~

* Fix migration names and dependencies

`2.0b0`_ - 2021-05-21
---------------------

Added
~~~~~

* Introduce validity range and link data to validity ranges.
* Add option to link subjects to groups
* Add search indices for rooms.
* Show week version of smart timetable on desktop devices.
* Add PDF export function for regular timetables.

Changed
~~~~~~~

* Link week-related models not only to weeks, but also to years.
* Optimise query count in timetable views.
* Go to next week if current day is out of range (weekly timetable view).
* Summarize double lessons in substitutions print view.
* Show only parent groups in "Affected groups".

Fixed
~~~~~

* Do not show dates in regular timetable.
* Show correct tooltip for rooms in substitution table.
* Show extra lessons in which a person is the new teacher in "My timetable".
* Show translations for weekdays.
* Show absent teachers in substitutions plan.
* Show supervisions in substitutions plan.
* Sort teacher short names alphabetically.
* Sort substitutions table by parent groups if displaying parent groups is activated.
* Make previous/next lesson API functions independent of the validity range.
* Show only regular elements in regular timetable, don't include information like holidays.

`2.0a2`_ - 2020-05-04
---------------------

Added
~~~~~

* Header box with absent and affected teachers and groups.
* Provide smart plan for current day as dashboard widget.
* Roles and permissions for timetable and lists.
* Show events in timetable.
* Show exams in timetable.
* Show holidays in timetable.
* Show supervision substitutions in timetable and list.

Changed
~~~~~~~

* Improve handling of different types (substitutions, timetables,…).
* Improve view for groups in timetable views.
* More intelligent personal timetable (checks if current person is teacher,…).
* Show announcements in timetable views.
* Devs: Move prev/next function to models.
* Devs: Rename field abbrev to short_name.

Fixed
~~~~~

* Force all lessons in timetable to same height.
* Render empty periods correctly.

`2.0a1`_ - 2020-02-01
---------------------

Added
~~~~~

* Migrate to MaterializeCSS

Changed
~~~~~~~

* Redesign filter ui for rooms, classes or teachers.
* Rename person timetabe for current day to "smart plan".

Fixed
~~~~~

* Catch error if no timetable data is available.


`1.0a3`_ - 2019-11-24
---------------------

Added
~~~~~

* Add list of all future substitutions.
* Devs: Add API to get date of a period.


`1.0a2`_ - 2019-11-11
---------------------

Added
~~~~~

* Devs: LessonPeriod now has a custom QuerySet and manager for advanced filtering.

Fixed
~~~~~

* Room plan includes substituted lessons now.


`1.0a1`_ - 2019-09-17
---------------------

Added
~~~~~

* Support lesson cancellation.
* Devs: Add fully pythonic API for calendar weeks.

Fixed
~~~~~

* Redirect to correct date after editing a substitution.
* Correctly display teachers for substituted lessons.
* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a1
.. _1.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a2
.. _1.0a3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/1.0a3
.. _2.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0a1
.. _2.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0a2
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b0
.. _2.0b1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b1
.. _2.0b2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b2
.. _2.0b3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0b3
.. _2.0rc1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0rc1
.. _2.0rc2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0rc2
.. _2.0rc3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0rc3
.. _2.0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.0
.. _2.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.1
.. _2.2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.2
.. _2.2.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.2.1
.. _2.3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.3
.. _2.4: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.4
.. _2.4.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.4.1
.. _2.4.2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.4.2
.. _2.5: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/2.5
.. _3.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/3.0b0
.. _3.0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/3.0
.. _3.0.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/3.0.1
.. _3.0.2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/3.0.2
.. _4.0.0.dev8: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/4.0.0.dev8
.. _4.0.0.dev9: https://edugit.org/AlekSIS/Official/AlekSIS-App-Chronos/-/tags/4.0.0.dev9
