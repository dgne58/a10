---
title: "API Docs — Flask-RESTful 0.3.10 documentation"
source: "https://flask-restful.readthedocs.io/en/latest/api.html"
author:
published:
created: 2026-04-13
description:
tags:
  - "clippings"
---
## API Docs

## Api

## ReqParse

## Fields

## Inputs

`inputs.``boolean` (*value*) [¶](#inputs.boolean "Permalink to this definition")

Parse the string `"true"` or `"false"` as a boolean (case insensitive). Also accepts `"1"` and `"0"` as `True` / `False` (respectively). If the input is from the request JSON body, the type is already a native python boolean, and will be passed through without further parsing.

`inputs.``date` (*value*) [¶](#inputs.date "Permalink to this definition")

Parse a valid looking date in the format YYYY-mm-dd

`inputs.``datetime_from_iso8601` (*datetime\_str*) [¶](#inputs.datetime_from_iso8601 "Permalink to this definition")

Turns an ISO8601 formatted datetime into a datetime object.

Example:

```
inputs.datetime_from_iso8601("2012-01-01T23:30:00+02:00")
```

| Parameters: | **datetime\_str** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The ISO8601-complying string to transform |
| --- | --- |
| Returns: | A datetime |

`inputs.``datetime_from_rfc822` (*datetime\_str*) [¶](#inputs.datetime_from_rfc822 "Permalink to this definition")

Turns an RFC822 formatted date into a datetime object.

Example:

```
inputs.datetime_from_rfc822("Wed, 02 Oct 2002 08:00:00 EST")
```

| Parameters: | **datetime\_str** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The RFC822-complying string to transform |
| --- | --- |
| Returns: | A datetime |

*class* `inputs.``int_range` (*low*, *high*, *argument='argument'*) [¶](#inputs.int_range "Permalink to this definition")

Restrict input to an integer in a range (inclusive)

`inputs.``iso8601interval` (*value*, *argument='argument'*) [¶](#inputs.iso8601interval "Permalink to this definition")

Parses ISO 8601-formatted datetime intervals into tuples of datetimes.

Accepts both a single date(time) or a full interval using either start/end or start/duration notation, with the following behavior:

- Intervals are defined as inclusive start, exclusive end
- Single datetimes are translated into the interval spanning the largest resolution not specified in the input value, up to the day.
- The smallest accepted resolution is 1 second.
- All timezones are accepted as values; returned datetimes are localized to UTC. Naive inputs and date inputs will are assumed UTC.

Examples:

```
"2013-01-01" -> datetime(2013, 1, 1), datetime(2013, 1, 2)
"2013-01-01T12" -> datetime(2013, 1, 1, 12), datetime(2013, 1, 1, 13)
"2013-01-01/2013-02-28" -> datetime(2013, 1, 1), datetime(2013, 2, 28)
"2013-01-01/P3D" -> datetime(2013, 1, 1), datetime(2013, 1, 4)
"2013-01-01T12:00/PT30M" -> datetime(2013, 1, 1, 12), datetime(2013, 1, 1, 12, 30)
"2013-01-01T06:00/2013-01-01T12:00" -> datetime(2013, 1, 1, 6), datetime(2013, 1, 1, 12)
```

| Parameters: | **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The ISO8601 date time as a string |
| --- | --- |
| Returns: | Two UTC datetimes, the start and the end of the specified interval |
| Return type: | A tuple (datetime, datetime) |
| Raises: | ValueError, if the interval is invalid. |

`inputs.``natural` (*value*, *argument='argument'*) [¶](#inputs.natural "Permalink to this definition")

Restrict input type to the natural numbers (0, 1, 2, 3…)

`inputs.``positive` (*value*, *argument='argument'*) [¶](#inputs.positive "Permalink to this definition")

Restrict input type to the positive integers (1, 2, 3…)

*class* `inputs.``regex` (*pattern*, *flags=0*) [¶](#inputs.regex "Permalink to this definition")

Validate a string based on a regular expression.

Example:

```
parser = reqparse.RequestParser()
parser.add_argument('example', type=inputs.regex('^[0-9]+$'))
```

Input to the `example` argument will be rejected if it contains anything but numbers.

| Parameters: | - **pattern** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.11)")) – The regular expression the input must match - **flags** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.11)")) – Flags to change expression behavior |
| --- | --- |

`inputs.``url` (*value*) [¶](#inputs.url "Permalink to this definition")

Validate a URL.

| Parameters: | **value** (*string*) – The URL to validate |
| --- | --- |
| Returns: | The URL if valid. |
| Raises: | ValueError |