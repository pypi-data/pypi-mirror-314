# Format specification of the project file for Felyx

## Version 4 (published on 2024-09-13)

The project file is a [ZIP][] file and must have the file extension `.zip`.

[ZIP]: https://en.wikipedia.org/wiki/ZIP

It must contain no sub-directories. At the top-level directory of the ZIP file, a file `metadata.yml`, in [YAML][] format, must be present. This file, encoded in [UTF-8][], must contain a single associative array, with two fields:

[YAML]: https://en.wikipedia.org/wiki/YAML
[UTF-8]: https://en.wikipedia.org/wiki/UTF-8

- `format`, whose value must be an integer, greater or equal to 1. This value specify the format version of the project file.

- `video`, whose value must be an associative array, containing the fields `filename`, `size`, and `sha1sum`.

The `filename` field must be a string with the name of the video file. The associated file may exist at the top-level directory of the ZIP file. If it is absent, loading of a file with that name (located at the same directory where the project file is) will be attempted.

The video file must be in any of the formats currently accepted by Felyx, whose MIME names are:

- video/mp4
- video/ogg
- video/quicktime
- video/vnd.avi
- video/webm
- video/x-matroska
- video/x-ms-wmv

The `size` field must be an integer value with the size of the file, in bytes.

The `sha1sum` field must be a string of hexadecimal characters of length 40
containing the [SHA-1][] checksum of the file contents.

[SHA-1]: https://en.wikipedia.org/wiki/SHA-1

The `size` and the `sha1sum` fields are used to check the integrity of the loaded video file.

Here is an example of the `metadata.yml` file:
```
video:
  filename: experiment.mp4
  size: 13793243
  sha1sum: 7500b753ac304a7e150081db67ad672ccdabaf8b
```

Two other files may be present at the top-level directory of the project ZIP file:

1. A data file in [CSV][] format, containing information about the timelines and the event occurrences (event occurrences will be referred hereafter as simply “occurrences”). The name of this file must be the same as the video file, but with the `.csv` extension. This file is a text file, containing a data frame with comma-separated values. Each line corresponds to an occurrence. The headers of this file must be the following:

```
timeline,label,begin,end,comment
```

The types of the columns are the following:

- `timeline`: a string containing the name of the timeline, indicating where is the occurrence associated with the line
- `event`: a string containing the label of the occurrence
- `begin`: a float number, indicating the begin time of the occurrence (in milliseconds)
- `end`: a float number, indicating the end time of the occurrence (in milliseconds)
- `comment`: a string containing comments associated with the occurrence; the value can be multi-lined, in which case it must be delimited by double quote characters (`"`)

[CSV]: https://en.wikipedia.org/wiki/Comma-separated_values

2. A file named `config.yml`, in YAML format and encoded in UTF-8, containing the possible events that the occurrences will represent. This file must contain a associative array, with, at least, the key `timelines`. The value of the `timeline` field must be an associative array. Each entry will specify an individual timeline, whose name is given by its key (which must be  string). The value associated with the key is itself an associative array with three optional fields: `order` `description`, and `events`:
- The value of the `order` field must be an integer number. It specifies the position of the associated timeline in the interface's time pane (see below).
- The value of the `description` field is a string containing a textual description of the purpose of the associated timeline. It should be informative to the user.
- The value of the `events` field is an associative array containing the events that can appear in the associated timeline. Each element of this associative array correspond to a specific event. Its key, which must be a string, represent the name of the event and its value contains the properties, in the form of an associative array. This associative array may have two keys: `color` and `description`. Both must be strings. The value of the `color` field can be either a [SVG 1.0 color name][] or a [CSS 2 RGB specification][] and will be the color of the occurrences representing the associated event. The `description` field contains a textual description of the event. It should be informative to the user.

[CSS 2 RGB specification]: https://www.w3.org/TR/SVG11/types.html#ColorKeywords
[SVG 1.0 color name]: https://www.w3.org/TR/2008/REC-CSS2-20080411/syndata.html#color-units

Every timeline name and occurrence label appearing in the data file must also appear in the `config.yml` file.

Here is an example of the contents of a `config.yml` file (this is the current default content of the configuration file of Felyx):

```
timelines:
  phase:
    order: 1
    description: Phase of the experiment
    events:
      F:
        color: yellow
        description: Familiarization phase
      T:
        color: green
        description: Test phase
  gaze:
    order: 2
    description: Looking direction
    events:
      '0':
        color: '#4DAF4A'
        description: The participant looks at the center of the screen
      '1':
        color: '#377EB8'
        description: The participant looks at the left side of the screen
      '2':
        color: '#E41A1C'
        description: The participant looks at the right side of the screen
      A:
        color: '#984EA3'
        description: The participant looks at the attention getter
```

Note that key names that would be interpreted as numeric values (like `'0'`, `'1'`, and `'2'` above) must appear between simple quotes, in order to be considered as strings. Likewise, the colors in CSS 2 RGB format (like `'#4DAF4A'` above) must also be quoted, because the hash character (`#`) marks the beginning of a comment in the YAML format.

The value of the description field can be a multi-line string. In order to accomplish that, users must use the pipe (`|`) syntax of YAML, like in the example below (notice that the indentation at the beginning of the lines is mandatory and will be stripped off the final resulting string):


```
description: |
  The participant looks at the right side of the screen
  (extra line goes here)
```

The ordering of the timelines in the time pane is determined by both the `order` field (in numeric order) and the timeline name (in alphabetical order). All timelines containing the `order` field will appear on the bottom of the time pane, in increasing order of the values (i.e. the timeline with higher value of `order` will at the bottom). The remaining ones, with no `order` field, will appear above the others, in descending alphabetical order. For instance, the following specification:

```
timelines:
  alpha:
    order: 5
  beta:
  gamma:
    order: 2
  delta:
```

will result in this layout:

```
┌───────┐
│ beta  │
├───────┤
│ delta │
├───────┤
│ gamma │
├───────┤
│ alpha │
└───────┘
```

The following are other optional fields recognized in `config.yml`:

- `csv-delimiter`: A string representing the delimiter in the CSV file (default: `,`)

- `coders`: A list of coder information. Each element of this list contains the identity of the person who did the video coding (name and email address) and the date and time of the last modifications. Each element must be an associated array with fields `name` (a string, *mandatory*), `email` (a string, *optional*), and `last-time` (a string representing the date and the time, in `datetime.strftime` format `%Y-%m-%d %H:%M:%S`, *optional*).

## History of changes in the format specification

### From version 3 (published on 2024-08-17)

- The `video` field of the `metadata.yml` file, which was a string in version 3, is now associative array in version 4. The descriptions of its fields `filename`, `size`, and `sha1sum` is added to the specification.
- Drop the obligation of inclusion of the video file in the ZIP project file.

### From version 2 (published on 2024-07-16)

- The format of the `timeline` field in the configuration is completely changed. Both collections of timelines and events are now associative arrays, instead of lists. 
- Drop the `duration` column from the data file.
- Rename the column `label` to `event`, in the data file.
- The ordering of the timelines in the time pane is determined now by the `order` field and the key names.
- Fix minor wording issues in the text.

### From version 1 (published on 2024-07-08)

Add the `coders` field to the `config.yml` file.

<!--  LocalWords:  YAML Felyx RGB webm -ogg quicktime vnd avi matroska wmv
      LocalWords:  UTF
 -->

