CHANGELOG
=========

0.12.13 - 2024-12-11
--------------------

This is a maintenance release. There is no change in the code. Only a screenshot image has been added to the `README.md` file.

0.12.12 - 2024-12-11
--------------------

This is a maintenance release.

Bug fix: Set proper occurrence upper and lower bounds. In the previous situation, occurrence handles were getting inside the neighboring occurrences by one frame.

0.12.11 - 2024-11-05
--------------------

This is a maintenance release. 

Bug fix: Ensure that the tooltip argument is a string. This was preventing the correct loading of project files.

Small improvement in the `README.md` file.

0.12.10 - 2024-10-17
--------------------

Change the name of the application from ViCodePy to Felyx.

0.12.9 - 2024-10-17
-------------------

This is a maintenance release. A note has been added to the `README.me` file to inform about the imminent change in the name of the application, from ViCodePy to Felyx.

Bug fix: The occurrences are correctly initialized with the comments found in the data file.

0.12.8 - 2024-09-25
-------------------

This is a maintenance release.

Bug fix: Saving configuration files is working now.

Other visible change: When zooming the time pane, the event name of the occurrence is always centered on the visible part of the occurrence (issue #155).

0.12.7 - 2024-09-19
-------------------

This is a maintenance release.

Bugs fixed:

- The adjacency of occurrences was wrongly detected in the previous version, making it impossible to merge occurrences. This is a regression, that was introduce in commit 5091ce4a and appeared in
version 0.12.2.
- Timelines can now be deleted. This is a regression that  appeared in version 0.12.4.

Other changes visible to the user:

- The menu entry Video/Play no changes its icon and its text to “Pause” when video is playing and back to “Play”, when the video is paused.
- The cursor handle changes now its color to red when there is an occurrence under creation.

0.12.6 - 2024-09-19
-------------------

This is a maintenance release.

Bugs fixed:

- When finishing the creation of an occurrence, a dialog for choosing the associated event appears. In the previous version, if the user clicked on the “Cancel” button, the positioning of occurrence was resumed but it became impossible to finish the creation, because the menu entries and the keypresses for doing it were disabled. This is fixed now.
- When creating an occurrence by moving the cursor to the left of the initial position, the display of the associated rectangle was wrong. It displays correctly now.
- The zoom factor is internally stored as an integer number now, instead of a in floating point representation. This ensures that it will always come back to the initial zoom factor of 1.
- Fix the display of the handle at the left border of an occurrence. This is a regression, that appeared in version 0.12.3.

Other change visible to the user:

- The cursor is kept always visible now. If the cursor goes outside the visible due to movement initiated by the user (Left/Right keys of dragging with the mouse), or due to zooming or scrolling, then it will be brought back to the viewport or the time pane will be scrolled.

0.12.5 - 2024-09-18
-------------------

This is a maintenance release. In file `files.py`, we use now
`pathlib.Path.joinpath` instead of `os.path.join`. This was causing a bug
in Windows when trying to load the config.yaml file that is in the same
directory of the video file to be loaded. This regression was introduced in
commit 8ae9d4a and appeared in version 0.12.4.

0.12.4 - 2024-09-17
-------------------

This is a maintenance release.

Fixed bugs:

- In Linux, when loading a new project or video file, sometimes the application got frozen. This is fixed now.
- Show the timeline titles when loading a new video or project file.
- Update the color of occurrence handles when events are edited.
- On Windows, a regression was introduced in version 0.12.0, that made it impossible to save project files. It is fixed now.
- Ensure that event and timeline names in the data (CSV) files are read as strings. This was causing a loading problem for data files in which all the events in a timeline had integer numbers as names.
- The timelines are now saved in correct order in the configuration file.

Other change visible to the user:

- If a `config.yml` exists in the same directory from where a video file is loaded, then it will take preference over the configuration files in other locations.

0.12.3 - 2024-09-15
-------------------

This is a maintenance release. The code has received an extensive rewriting, in order to internally represent the time in frame units, instead of milliseconds. This improved and simplified the code, avoiding problems related to floating point precision.

Fixed bugs:

- Issue #151 is fully addressed, with the following bugs fixed:
    - When the cursor is positioned one frame after the right border of an occurrence, the borders of this latter are thickened. They should not.
    - When creating a new occurrence, its right border can go past the left border of the next occurrence. It should not.
    - Starting a new occurrence when the cursor is positioned at the frame after the right border of an occurrence is impossible. This should not be the case.

Other changes visible to the user:

- Add the date of publication of format v4 to the `FORMAT.md` file.
- When handles are active, the Enter key deselects the corresponding occurrence.

0.12.2 - 2024-09-15
-------------------

This is a maintenance release. Bug fixes:

- Several issues regarding the rendering of the borders of the occurrences and the occurrence handles are fixed. The remaining ones will be fixed in the next release (see issue #151).
- When moving the borders of an existing occurrence via the occurrence handles, it was possible to go past the other border. It was than possible to create occurrences with zero duration. This is fixed now (issue #150).
- The limits for creating occurrence borders are now respected. This is a regression, that appeared in version 0.11.6.
- When a file with an unsupported extension (neither a video nor a ZIP file) was required to be loaded, the application silently ignored it. A warning dialog is shown now.

0.12.1 - 2024-09-13
-------------------

This is a maintenance release. A critical bug is fixed, which was preventing to load project files with format version prior to 4.

0.12.0 - 2024-09-13
-------------------

This is a minor release. The format of the project file is upgraded to v4.

Changes visible to the user:

- The video file can now be absent from the project file. If this is the case, it will be loaded from the same directory of the project file.
- The format v4 mandates that the SHA-1 checksum and the size of the video file are reported in the project file. This information is used to check the integrity of the video file at loading time.
- In the `FORMAT.md` file, the ordering principle for timelines in the time pane is clarified and an example of the file `metadata.yml`.
- An entry for toggling video inclusion is included in the menu.
- The selected occurrence can now be changed via the keyboard (Alt-Left and Alt-Right key combinations).

Fixed bugs:

The dialogues for selecting and modifying the coders are now fixed. The “Cancel” buttons do now what is expected and abort the operation of saving the project file. The “Edit coder information” dialog is now centered on the main window.

0.11.6 - 2024-09-12
-------------------

This is a maintenance release. The code has been extensively changed. In particular, the internal representation of time is now a float number. This fixes several issues and improved the behavior of the application. This fixes problems for videos with a non-integer frame duration (in terms of milliseconds), for instance, a video with 30 fps,

Bug fixes:
- The positioning of the occurrences is now accurate. There is no visible gaps in the timeline between adjacent occurrences now.
- The begin and end times of the occurrences are now correctly reported in the CSV data file.
- When there is an occurrence under creation and the video is mode play, the right border of that occurrence stopped correctly at the left border of the next occurrence in the same timeline. However the video continued to play. This is fixed now.
- The player buttons have now the correct size on MacOS.

0.11.5 - 2024-09-10
-------------------

This is a maintenance release.

The size policy of the player buttons has been changed to “Fixed”. This should override the specific behavior of some platforms.

0.11.4 - 2024-09-10
-------------------

This is a maintenance release.

Bug fixes:
- Disable the menu entry “Edit” ⇒ “Occurrence” ⇒ “Delete Occurrence” during creation of an occurrence.
- Allow deletion of occurrence via Del/Backspace key press and via the associate menu entry.
- Allow abortion of occurrence creation via ESC key press and via the associated menu entry.
- Allow deletion of an empty timeline.

Changes visible to the user:
- Use more sensible menu entry text “Abort Current Occurrence” ⇒ “Abort Creation of Occurrence”.
- Show keybind for deletion action in Occurrence context menu
- Ensure that dialog for confirmation of occurrence deletion is centered on main application window.

0.11.3 - 2024-09-10
-------------------

This is a maintenance release.

User visible changes:
- It is possible now to export the configuration file `config.yaml` (or whichever name the user chooses), containing all the modifications made during a session (timelines and events properties, coders information, and CSV delimiter). A new entry “Export Configuration” is added to the File menu.
- Users can choose the configuration file to be used by using the option `--config`, when running the application from the command line.
- Users can directly select any occurrence with a mouse single click, even if it is in a deselected timeline.
- Set a minimum width for the volume slider. It should now be displayed correctly on all platforms.
- Ensure that the About window is centered on the main application window.

Bug fixes:
- When deleting a timeline, honor the button “No” of the dialog.
- Right-clicking on an occurrence in a deselected timeline was causing the selected timeline to be deselected. This is fixed now.
- Occurrence borders change according to the position of the cursor (thick borders when the cursor is inside the occurrence in the selected timeline). This was not working properly when selecting a new timeline and is fixed now.

Several minor enhancements in the code are made, improving readability and performance.

0.11.2 - 2024-09-08
-------------------

This is a maintenance release.

User visible changes:
- It is possible now to cancel the coders dialog without selecting one of the coders in the list. If this is the case, then the saving of the project file is aborted.
- Files `config.yml` and `metadata.yml` are now always encoded in UTF-8. The file `FORMAT.md` has been modified, accordingly. However, there is no need to bump the format version, since the conversion is done transparently by PyYAML.
- The context menus for the `Occurence` and `Timeline` objects, usually access via the left-click of the mouse, are now accessed via the Menu key. Pressing this key will act on the selected item.
- It is possible now to remove events form the event collection of a timeline.

Bug fixes:
- The occurrence dialog is working again. This a regression introduced in commit 4bd2302b that appeared in version 0.10.5.

Code enhancements:
-  The `Timeline.occurrences` attribute has been transformed into a method. This avoids the need for maintaining the list of occurrences as an attribute and make code more robust.

0.11.1 - 2024-09-08
-------------------

This is a maintenance release.

Changes visible to the user:

- It is now possible to show a table with summary statistics of the events in a specific timeline (count and total time of each event).

- It is now possible to set the CSV delimiter. The valid values are comma, semicolon, and tab. There is now a check for valid values when reading the configuration file `config.yml`.

- Occurrence begin and end times are now saved in microsecond precision in the data (CSV) file. This is necessary for video files with a frame duration with non-integer amount of milliseconds (for instance, a video with 30 frames per second).

- The bottom-right button in the event choosing dialog has now different labels, depending on the context. It is “Cancel”, when finalizing the creation of an occurrence or when changing the event associated with an occurrence. Otherwise, it is “Finish” when editing the events of a timeline.

- We have confirmation that the application installs and run on MacOS. The `README.md` file is updated, accordingly.

Bug fix:

- The dialog of confirmation of deletion of an occurrence was not working and is fixed now.

Improvements in the code are made, notably the transformation of the attributes `Files.csv_delimiter` and `Timeline.name` into `@property`s. This increases the robustness of the code.

0.11.0 - 2024-09-07
-------------------

This is a minor release. A certain number of new features have been added to the application, and some changes in the behavior of the interfaces have been done.

New features:

- It is now possible to fully delete a timeline, making it disappear from the time pane.

- When creating a new timeline, a field for entering the text for the timeline description appear in the dialog.

- It is now possible to insert timeline at different places:
    - at the top of the time pane
    - above the selected timeline
    - below the selected timeline
    - at the bottom of the time pane

Changes visible to the user:

- The visual indication of timeline selection has changed. Now, all the non-selected timelines are grayed out.

- It is not possible to set the video position with a mouse double click, as before. For doing this, please click on the time scale (at the desired time position) or drag the cursor.

- Occurrences are now selected with a mouse single-click (left button). In order to invoke the  occurrence popup menu (with a mouse right click), there is no need to previously select the occurrence.

- New entries “Edit Events” and “Edit Properties” are added to the Edit⇒Timeline menu.

Bug fixes:

- In the previous version, it was possible to give the same name to different timelines. This caused bugs when saving the project file.

0.10.5 - 2024-09-04
-------------------

This is a maintenance release.

Bug fix: a regression introduced in version 0.10.2 prevented the change in the appearance of the occurrence under the cursor.

The changes visible to the user:

- All the dialogues now appear in the front and centered on the application window.
- The video position slider and the timestamp for the total duration of the video are removed from the interface. The position slider was redundant with the time pane cursor and showing the total duration was not very useful. The timestamp for the current image appears now in the same line as the player buttons and the audio volume slider.
- Tool tips have been added to the player buttons, indicating the associated key bindings.
- The tool tip of the volume slider shows now the percentage of volume.

Code improvements: In this version, a huge step has been made towards a better hierarchy of graphics scene objects (issue #116). Several other minor improvements in the code are made.

0.10.4 - 2024-09-01
-------------------

This is a maintenance release.

Bug fixes:

- The active border of occurrence under creation is now correctly handled when there is a mouse double click on the time pane.
- All open file dialogues are now in the foreground.
- The Play menu items for navigating the video work correctly now.
- Really remove occurrence from graphics scene. This bug is a regression, introduced in commit ba88ee3b and appeared in version 0.10.2.

Other improvements visible to the user:

- The ordering of items in Play menu is now made more logical.
- ViCodePy depends now on NumPy==1.26.3. This is necessary, in order to avoid incompatibilities with the shiboken6 module (version 6.6.2)

Documentation:

- A note regarding a warning due to the absence of package libav-dev (on Linux) is added to the file README.md. This fixes the warning `qt.multimedia.ffmpeg.libsymbolsresolver: Couldn't load VAAPI library`.

Code improvements:

Several code improvements are integrated in this version, including changes in the nomenclature. More notably the method Occurrence.can_be_initiated is replaced by Timeline.can_create_occurrence.

0.10.3 - 2024-08-25
-------------------

This is a maintenance release.

User visible enhancements:
- The behavior of the horizontal scroll bar of the time pane has been improved. It is now always visible. This avoids the problem in the previous version, when the vertical scroll bar unnecessarily appeared when the horizontal scroll bar appeared.
- The logic around the need to save the project file is improved. In the present situation, the saving of the project file is only proposed when it is strictly necessary.
- In the context menu for the occurrence, the entry “Change occurrence label” is changed to “Change occurrence event.”

Bug fixes:
- The value of `csv_delimiter` is honored. This regression bug has been introduced in version 0.9.1.
- Always initialize the event collection in every timeline. This prevents a bug when creating an occurrence in a timeline without defined events.
- Fix position of timeline title.

Code enhancements:
- The positioning of the timeline title has made more robust.
- All constants, which were scattered through the source files, are grouped in the new file `constants.py`.

0.10.2 - 2024-08-22
-------------------

This is a maintenance release. Only code improvements have been made. No visible user changes.

0.10.1 - 2024-08-22
-------------------

This is a maintenance release. The changes visible to the user are:

- Use a neutral (gray) color for the occurrence being created.
- When clicking or double-clicking on an occurrence, the associated timeline is also selected.
- When selecting a timeline, ensure that all other timelines are deselected.

Several changes are made in the code, improving its maintainability and its readability. An important change is the concept of "Annotation” that is transformed into “Occurrence” (in the sense of “occurrence of an event”). This is part of the ongoing change of the nomenclature in the code.

0.10.0 - 2024-08-17
-------------------

This version contains version 3 of the FORMAT file. The main changes in the format are:

- The format of the `timeline` field in the configuration has been completely changed. Both collections of timelines and events are now associative arrays, instead of lists.
- The `duration` column has been dropped from the data file.
- The column `label` is renamed to `event`, in the data file.
- The ordering of the timelines in the time pane is determined by the `order` field and the key names.

This version also introduces an important change in the way events are treated in the code. The representation of timelines and events is now more robust than in the previous releases. In particular, it is impossible now to have two events of two timelines with the same name.

The dialogues for editing events and timelines are improved. It is now possible to edit the descriptions of events and timelines. Tool tips are added to provide an instant information on events and timelines.

The data file (in CSV format) is now manipulated using the Pandas module. This adds a new dependency to ViCodePy.

0.9.1 - 2024-08-15
------------------

This is a maintenance release.

Enhancements in the user interface:

- Several dialogues are now centered on main window (Coders, Timeline label, Comment Annotation, and File format warning). This also ensures that the components of the dialog window will follow the QSS style specifications.
- Changes in menu entries:
    - “Add Timeline line” ⇒ “Add Timeline”
    - “Export CSV” ⇒ “Export Data”
- Add icon for “Toggle Fullscreen” menu action.
- Add icons to modal dialog buttons (in method Timeline.edit_label).
- The styles of QLineEdit and QTextEdit widgets are improved.

Bug fixes:

- The variables `project_file_path` and `coders` are moved from the class `MainWindow` into the class `Files`. This was preventing the proper saving of the project file.
- The access to the data file and the metadata file was mangled. This is fixed in the present release.

Several code improvements, invisible to the user, have been made. Most notably, we are now using pandas, instead of the standard csv module, for loading/saving the data file.

0.9.0 - 2024-08-06
------------------

The user interface is improved in this release. In the three situation where the user can choose/change events names and colors (i.e., [1] when creating a new annotation, [2] when changing the event associated with an existing annotation, and [3] when editing the events on a timeline), the same dialog is used (the class ChangeEvent). This closes issue #103.

Furthermore:

Bug fix: The events dialog is always centered on the main application window.

Enhancement: One of the timelines is always selected at start time.

0.8.2 - 2024-08-05
------------------

This is a maintenance release. Some improvements have been made to the user interface:

- Events are now sorted using the lower-case version of their names.
- In the change event dialog window, add text "Name:" before the field for the label and the “Cancel” button is renamed to “Finish”. Furthermore, the “New” button is now show in the bottom row and the buttons can be selected by using the arrow keys (the default one is show with thicker borders).
- The change event dialog is now centered on the main window.
- The jagging of the video slide, when the video time is updated, is fixed.

Several minor bug fixes and code improvements are also done in this release.

0.8.1 - 2024-08-03
------------------

Enhancements:

- When the mouse hover over an annotation, the comment associated with it is shown in the tooltip. When the annotation has no comment, the tooltip shows `(no comment)`.
- The term `CSV` has been change to `data`, were it is appropriate.
- The cursor handle is made taller (the whole height of the `TimePaneScale` widget) and is now transparent.

Bug fixes:

Most of these bugs were caused by the code reorganization in the previous release. They were causing wrong behavior of the application.

- Add the lacking icon file with the plus (+) sign
- Fix name of method `Annotation.calculateBounds` to `.get_bounds`
- Ensure that first argument of `QMessageBox` is a widget
- Give sensible widget as argument of `QFileDialog.getSaveFileName`
- Use method `TimePane.has_annotations`
- Ensure that the variable `temp_dir` of class `Files` is initialized
- Correctly disable the menu item
- Fix call to `ConfirmMessageBox`
- Really cleanup the temporary directory at exit

Several improvements have been made to the code, mainly related to coherence and style. These changes are not visible to the user.

0.8.0 - 2024-08-02
------------------

It is now possible to specify the size of the window from the command line, by using either the `--size` option or the `--fullscreen` option.

The code has been completely reorganized and rationalized. The code in files video.py and widgets.py is now scattered into logical chunks into separated files.

0.7.4 - 2024-07-21
------------------

This is a maintenance release. The terminology in the code has been improved. User visible changes:

- The application menu has been reorganized. There are now submenus for manipulating timelines and annotations. There are now entries for accessing the GitLab repository and the project page at PyPI.

- The About window has been improved. It contains now information about the copyright notices and the license terms, as well as the upstream links.

0.7.3 - 2024-07-20
------------------

This is a maintenance release. User visible changes:

- The Escape key now aborts the creation of an annotation.

- The selected annotation can now be deleted by using the Backspace or the Delete keys.

- The selected timeline can be changed by using the Up and Down keys.

0.7.2 - 2024-07-18
------------------

This is a maintenance release.

Enhancements in the interface:

- When an annotation has just been created, it will appear with thick borders, indicating that it is under the cursor.

- The Enter key can now be used as a shortcut to select the annotation under the cursor. Furthermore, when an annotation is selected, pressing the Enter key will deselect it.

- The active annotation handle appears now with thick borders.

Bug fix:

- In the previous version, when moving an annotation handle by keeping the Right key pressed, it could go past the beginning borer of the subsequent annotation in the timeline. This has been fixed.

0.7.1 - 2024-07-17
------------------

This is a maintenance release. The distributed config.yml file has been changed. The event "ag" (attention getter) has been added and the colors of the events in the "gaze" timeline have been changed.

0.7.0 - 2024-07-16
------------------

New features:

- The format of the project file is upgraded to 2. This introduces a backward-incompatibility which may affect users. Indeed, previous versions of ViCodePy will refuse to load a project file with version 1 and the user will be invited to upgrade the application.

- The identity of the person doing the code (name and email address), as well as the date and time of last modification are now stored into the configuration file (in the `coders` field). The identity information is asked when the project file is saved for the first time and is persistent for the duration of the session.

- A new context menu is now added when right-clicking on a timeline. It allows to:
  * Add a new timeline.
  * Delete the timeline. This is not yet fully operational, since the timeline is not actually removed. For now, the timeline is only emptied from its annotations.
  * Edit the timeline label.
  * Edit the events defined for the timeline. it is possible to change the label and the background color of each event already defined for the current timeline.

Bug fix:

The base name of the CSV file saved in the project file is now exactly the same as the base name of the video file. In the previous version, it was wrongly set to the name of the ZIP file.

0.6.4 - 2024-07-13
------------------

This is a maintenance release, which fixes the reading of the CSV file.

0.6.3 - 2024-07-12
------------------

This is a maintenance release, with some code improvements. The only user visible change is the fixing of a bug causing the label of the annotation not changed when the event was changed.

0.6.2 - 2024-07-11
------------------

This is a bug-fixing, maintenance release. User visible changes:

- The format version of the project file is set to 1. In the previous release, it was wrongly set to 2.
- The Help/About window shows now the format version of the project file.

0.6.1 - 2024-07-11
------------------

This is a bug-fixing, maintenance release. User visible changes:

- When moving the borders of the selected annotation, they cannot go past the borders of adjacent annotations.
- Better logic for finding the current version of ViCodePy.

0.6.0 - 2024-07-08
------------------

New features:

- All the work done during a session can now be saved in a “project file”. This file is in ZIP format and contains the video file, the configuration file (which defines the timelines and the style of the events), and the CSV file (which contains the annotations). This file can also be loaded into ViCodePy, in order to resume of visualize previous sessions. The format of the project file is described in the `FORMAT.md` file. Provisions will be made for assuring backward and forward compatibility regarding the format of the project file.

- It is now possible to do further manipulations on a annotation, once it is created, by right-clicking on it:
  - Change the label (and the associated color) of the annotation.
  - Add comments to the annotation.
  - Merge with an adjacent annotation, if there is no gap between both of them and if they both indicate the same event.

- The configuration system is improved:
  - The loading of the configuration file `config.yml` is now incremental. Files named `config.yml` are read from the package, the system, the user, and the local directories, in this order. Latter settings override the former.
  - It is now possible to specify the separator for the CSV files (typically `,` or `;`), in the `config.yml` file.

- In the CSV file, time is now coded in milliseconds, instead of seconds. This avoids errors related to floating point precision.

- There is now an “About” entry in the “Help” for showing the version of ViCodePy.

- It is possible to horizontally scroll the timelines with Shift + mouse wheel.

- The annotation under the cursor is now highlighted. This is useful for creating contiguous annotations.

- Clicking on a timeline selects it. Double-clicking selects the timeline and move the cursor to the mouse pointer position.

Bugs fixed:

- Fixed several visualization problems, related to the zooming of the timeline and the location of annotation borders and the cursor, which are now precisely placed at the instant of time corresponding the each image in the video.

- The responses to the key presses are improved. In particular, if the Right key is kept pressed, the movie is played continuously.

- Several minor bugs in the interface have been fixed.

0.5.2 - 2024-06-21
------------------

Maintenance release: Integrate the changes for indicating the active timeline via the title bar (forgotten in last version).

0.5.1 - 2024-06-21
------------------

Enhancements:

- The handle for the video player / timeline editor splitter changes now its color when hovered by the mouse
- The title bars of the timelines change color to indicate which one is selected

User-invisible change:

- Code files reorganization

0.5.0 - 2024-06-20
------------------

New features:

- It is now possible to add annotations in multiple timelines
- When clicking on the timeline, the cursor is moved to the mouse position
- It is possible to go forward and backward in time in steps of 5 and 10 frames, either with keystrokes or with buttons in the video player
- Durations of the annotations are now saved in the CSV file
- New system for loading the configuration files (local-, user- and system-wide)
- The program does not exit before proposing to save the created annotations

User-visible fixed bugs:

- During the creation of a new annotation, the other existing annotation can not be made active
- The choice of color for a new label is persistent
- The menu entry for the creation of an annotation is more informative
- The existence of the video file is checked before loading it

0.4.5 - 2024-06-11
------------------

This is a maintenance release. The user visible changes are:

* Require version 6.6.2 of PySide6
* The zooming of the timeline is now centered on the mouse position
* The CSV file is now exported to the same directory where the video file is located
* The annotations appear in chronological order in the exported CSV file
* Improvements in the display of the tick labels in the timescale
* Fix bug when selecting annotations created by pressing the Left key
* At startup, if no video is loaded, a message is shown inviting the user to load a file

0.4.4 - 2024-06-02
------------------

* Annotations do not overlap anymore

0.4.3 - 2024-06-02
------------------

* Use better names for columns in the exported CSV file
* Improved documentation

0.4.2 - 2024-06-01
------------------

* The program accepts now command line arguments
* Annotation labels can be chosen directly using the keyboard, once the annotation dialog is displayed

0.4.1 - 2024-05-31
------------------

* All supported video file formats can now be loaded
* Annotation handles can now be clicked/dragged with the mouse
* Improved color contrast of annotation labels

0.4.0 - 2024-05-30
------------------

* First release to PyPI
* The code has been ported from PQt6 to PySide6
* Bugs fixed / Added features
  - The timeline can be zoomed/dezoomed
  - Annotation creation can be aborted
  - Annotation data can be saved in a CSV file
  - The configuration is now in YAML format and can store several annotation label definitions

0.3.7 - 2024-05-28
------------------

Depend on PySide6

0.3.6 - 2024-05-28
------------------

Add dependency on PyQt6-Qt6

0.3.5 - 2024-05-28
------------------

Force dependency on PyQt6 == 6.4

0.3.4 - 2024-05-23
------------------

Use GitLab CI and AutoPub for automatic publication of the package

0.3.3 - 2024-05-23
------------------

* First release to test.pypi.org
* The timeline is now implemented with QGraphics* objects
* Annotations are now clickable

0.2 - 2024-04-30
----------------

* Fix video playing issues
* The timeline is now functional and it is possible to add annotations

0.1 - 2024-03-25
----------------

Initial release, containing a very simple interface that allows loading a video file and playing it. A timeline is show but is not yet functional.
