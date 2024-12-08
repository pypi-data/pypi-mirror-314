Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

Unreleased
----------

Upgrade notice
~~~~~~~~~~~~~~

If you're upgrading from 3.x, there is now a migration path to use.
Therefore, please install ``AlekSIS-App-Lesrooster`` which now
includes parts of the legacy Chronos and the migration path.

`4.0.0.dev9`_ - 2024-12-07
--------------------------

Added
~~~~~

* Configurable PDF export of the coursebook for one or more groups.

`4.0.0.dev8`_ - 2024-11-15
--------------------------

Added
~~~~~

* Widgets on person and group pages with detailed coursebook statistics
  and including all participations/personal notes.

`4.0.0.dev3`_ - 2024-07-10
--------------------------

Added
~~~~~

* Support for entering personal notes for students in the new coursebook interface.
* Support for entering tardiness for students in the new coursebook interface.

`4.0.0.dev2`_ - 2024-07-13
--------------------------

Fixed version of 4.0.0.dev1

`4.0.0.dev1`_ - 2024-06-13
--------------------------

Added
~~~~~

* Support for entering absences for students in the new coursebook interface.

`4.0.0.dev0`_ - 2024-04-23
--------------------------

Notable, breaking changes
~~~~~~~~~~~~~~~~~~~~~~~~~

Starting from the class register core functionality, Alsijil is getting a entire rewrite
of both its frontend and backend. The models formerly used for lesson documentation, notably
`LessonDocumentation` and `PersonalNote` are replaced by new ones based on the calendar framework
provided by `AlekSIS-Core` and the absense framework provided by `AlekSIS-App-Kolego`. The legacy
views providing management functionality for those legacy models are not available anymore.

Changed
~~~~~~~

* Modern rewrite of class register/coursebook, both in the frontend and the backend
  * Several legacy class register views were consolidated in a modern frontend (coursebook).
  * [Dev] The `LessonDocumentation` model is replaced with the `Documentation` model, based on the calendar framework.
  * [Dev] The `PersonalNote` model is replaced with the `NewPersonalNote` model.
  * [Dev] Participation status documentation is taken over by the new `Participation` model.

Fixed
~~~~~

* Migrating failed due to an incorrect field reference.

`3.0.1`_ - 2023-09-02
-------------------

Fixed
~~~~~

* Migrations failed on empty database

`3.0`_ - 2023-05-15
-------------------

Fixed
~~~~~
* In some cases, pages showing the count of extra marks and lessons with custom excuse types of
  persons threw an error.
* The redirection to generated class register PDF printouts did not work.
* Some columns in the table showing statistics for the members of a group were labled wrongly.
* Absences with custom excuse types were not counted correctly.
* Tabs on the week overview page were not displayed.

`3.0b0`_ - 2023-02-28
---------------------

This version requires AlekSIS-Core 3.0. It is incompatible with any previous
version.

Removed
~~~~~~~

* Legacy menu integration for AlekSIS-Core pre-3.0

Added
~~~~~

* Add SPA support for AlekSIS-Core 3.0

Changed
~~~~~~~

* [Dev] Rename the "late" field in the PersonalNote model to "tardiness".
* Use new icon set inside of models and templates
* Run full register printout generation in background 

Fixed
~~~~~

* Extra marks and excused absences were counted multiple times in some class register views.
* Substitution teachers couldn't see any persons in the person list of a substituted lesson.
* Events were shown for days not being inside the timetable schema in full register printout.

`2.1.1`_ - 2022-09-01
---------------------

Fixed
~~~~~

* Register absence form wasn't accessible without direct access to class register.
* Printing the full group register failed when a person had no personal notes.
* Data checks reported all Lesson Documentations as being during Holidays if there was no Holiday object.
* Students were displayed multiple times in class register views.
* Absences were counted multiple times in some class register views.
* Group owners couldn't create new seating plans.

`2.1`_ - 2022-06-25
-------------------

Added
~~~~~

* Owners of one of the parent groups of a object can now have the same rights on it
as a group owner (can be toggled with a preference).
* Integrate seating plans in lesson overview
* Add option to set LessonDocumentation data for all lessons in one week at once.
* Excuse types can now be marked as `Count as absent`, which they are per default. If not, they aren't counted in the overviews.
* Add Ukrainian locale (contributed by Sergiy Gorichenko from Fre(i)e Software GmbH).

Fixed
~~~~~

* The week overview page was not refreshed when a new week was selected in the dropdown.
* Make generation of full register printout faster.
* Updating a lesson documentation caused an error when the preference for carrying over lesson documentations to the whole week was deactivated.

`2.0.1`_ - 2022-02-12
---------------------

Fixed
~~~~~

* Status icon in single-lesson view showed 'Missing data' although the data were complete.
* The personal note tab of a lesson was not well usable on mobile devices.

`2.0`_ - 2022-02-06
------------------

Changed
~~~~~~~

* Use start date of current SchoolTerm as default value for PersonalNote filter in overview.

Fixed
~~~~~

* Events without groups caused an error when not accessed through the week view.

`2.0rc7`_ - 2021-12-25
---------------------

Changed
~~~~~~~

* Optimize view for one register object ("lesson view") for mobile and tablet devices.
* Optimize view for lessons of a week ("week view") for mobile and tablet devices.
* German translations were updated.
* Link to personal notes in the personal overview.

Fixed
~~~~~

* Translate table columns and filter button on person overview page.
* Show correct status icon for events.
* Subjects in full register printout were struck through although they
hadn't changed.
* Table with all register objects didn't work with extra lessons.
* Add missing definitions of some permissions so they can be assigned.

`2.0rc6`_ - 2021-08-25
----------------------

Fixed
~~~~~

* Fix problems with displaying dates for events in the week and lesson view.
* Unique constraint on lesson documentations and personal notes did not work and caused racey duplicates.

`2.0rc5`_ - 2021-08-12
----------------------

Fixed
~~~~~

* The _Delete personal note_ action didn't work due to wrong usage of ``bulk_update``.
* Groups and persons were shown multiple times in some forms due to filtering by permissions.

`2.0rc4`_ - 2021-08-01
----------------------

Fixed
~~~~~

* The lesson documentations tab was displayed on overviews for persons who are not teachers.
* Teachers weren't able to edit personal notes of their students in the person overview.
* The actions to mark absences as excused in the personal notes table also marked personal notes as excused which are not absences.
* The delete action in the personal notes table really deleted the items instead of just resetting them to default values.

`2.0rc3`_ - 2021-07-20
----------------------

Fixed
~~~~~

* Lesson view didn't work due to additional whitespaces in ``url`` tags.

`2.0rc2`_ - 2021-06-26
----------------------

Fixed
~~~~~

* "My overview" and "All lessons" didn't work if there was no current school term.

`2.0rc1`_ - 2021-06-23
----------------------

Changed
~~~~~~~
* Show 'Lesson documentations' tab on person overview only if the person is a teacher.
* Use semantically correct html elements for headings and alerts.

Fixed
~~~~~

* Preference section verbose names were displayed in server language and not
  user language (fixed by using gettext_lazy).

`2.0b0`_ - 2021-05-21
---------------------

Added
~~~~~
* Show a status icon for every lesson (running, data complete, data missing, etc.).
* Add buttons to go the the next/previous lesson (on the day/for the group).
* Add support for custom excuse types.
* Add group notes field.
* Add option to configure extra marks for personal notes.
* Add week select in week view.
* Carry over data between adjacent lessons if not already filled out.
* Student view with all personal notes and some statistics.
    * Mark personal notes as excused.
    * Reset personal notes.
    * Multiple selection/filter/sorting.
* Add overview of all groups a person is an owner of ("My groups").
* Implement intelligent permission rules.
* Add overview of all students with some statistics ("My students").
* Use django-reversion to keep an auditlog.
* Add page with affected lessons to register absence form.
* Check plausibility of class register data.
* Manage group roles (like class services).

Changed
~~~~~~~
* Redesign and optimise MaterializeCSS frontend.
    * Organise information in multiple tabs.
    * Show lesson topic, homework and group note in week view.
    * Improve mobile design.
* Improve error messages if there are no matching lesson periods.
* Filter personal notes in full register printout by school term.
* Allow teachers to open lessons on the same day before they actually start.
* Count and sum up tardiness.
* Do not allow entries in holidays (configurable).
* Support events and extra lessons as class register objects.

Fixed
~~~~~
* Show only group members in the week view.
* Make register absence form complete.
* Repair and finish support for substitutions.

`2.0a1`_ - 2020-02-01
---------------------

Changed
~~~~~~~

* Migrate to MaterializeCSS.
* Use one card per day in week view.

Removed
~~~~~~~
* Remove SchoolRelated and all related uses.


`1.0a3`_ - 2019-11-24
---------------------

Added
~~~~~

* Allow to register absences and excuses centrally.
* Statistical evaluation of text snippets in personal notes.
* Add overview per person to register printout.

Fixed
~~~~~

* Show lesson documentations in printout again.
* Allow pages overflowing in printout
* Show all relevant personal notes in week view.

`1.0a2`_ - 2019-11-11
--------

Added
~~~~~

* Display sum of absences and tardiness in printout.
* Auto-calculate absences for all following lessons when saving a lesson.

Changed
~~~~~~~

* Allow superusers to create lesson documentations in the future.

Fixed
~~~~~

* Fixed minor style issues in register printout.

`1.0a1`_ - 2019-09-17
--------

Added
~~~~~

* Display audit trail in lesson view.
* Add printout of register for archival purposes.

Fixed
~~~~~

* Fix off-by-one error in some date headers.
* Deduplicate lessons of child groups in group week view.
* Keep selected group in group week view when browsing weeks.
* Correctly display substitutions in group week view.
* Support underfull school weeks (at start and end of timetable effectiveness).
* Use bootstrap buttons everywhere.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _1.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/1.0a1
.. _1.0a2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/1.0a2
.. _1.0a3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/1.0a3
.. _2.0a1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0a1
.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0b0
.. _2.0rc1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc1
.. _2.0rc2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc2
.. _2.0rc3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc3
.. _2.0rc4: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc4
.. _2.0rc5: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc5
.. _2.0rc6: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc6
.. _2.0rc7: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0rc7
.. _2.0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0
.. _2.0.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.0.1
.. _2.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.1
.. _2.1.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/2.1.1
.. _3.0b0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/3.0b0
.. _3.0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/3.0
.. _3.0.1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/3.0.1
.. _4.0.0.dev0: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev0
.. _4.0.0.dev1: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev1
.. _4.0.0.dev2: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev2
.. _4.0.0.dev3: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev3
.. _4.0.0.dev8: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev8
.. _4.0.0.dev9: https://edugit.org/AlekSIS/Official/AlekSIS-App-Alsijil/-/tags/4.0.0.dev9
