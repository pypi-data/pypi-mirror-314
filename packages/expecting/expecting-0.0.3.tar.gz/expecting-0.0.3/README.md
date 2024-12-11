# expecting

Elegant assertions library.

This is currently a work in progress.


## Installation options

```bash
pip install expecting
```
```bash
poetry add expecting --group dev
```

## Usage

Expecting consists of a set of assertion objects that can be used with `assert` statements in a clear, readable way.
Most common assertion will be covered under a structured set of modules, following an intuitive naming schema:

```python
import expecting

assert '2023-10-11' == expecting.string.datetime.iso8601_day()
```

Here, the `expcting.string.datetime` module introduces a handful of factory methods for asserting that the value is a
string representing a date and time format.

It's specially useful with [pytest](https://docs.pytest.org/)  and its amazing error messages, where an assertion
failure message would look something like:

```text
string/test_datetime.py:7 (test_iso8601_full_matches[2023/10/11 13:01:10])
'2023/10/11 13:01:10' != ~= <datetime as "%Y-%m-%dT%H:%M:%S.%f%z">

Expected :~= <datetime as "%Y-%m-%dT%H:%M:%S.%f%z">
Actual   :'2023/10/11 13:01:10'
<Click to see difference>

datetime_str = '2023/10/11 13:01:10'

    @pytest.mark.parametrize(
        'datetime_str',
        (
            '2023/10/11 13:01:10',
        )
    )
    def test_iso8601_full_matches(datetime_str: str):
>       assert datetime_str == expecting.string.datetime.iso8601_full()
E       assert '2023/10/11 13:01:10' == ~= <datetime as "%Y-%m-%dT%H:%M:%S.%f%z">
...
```

The `~=` symbol prefixing the expected value is used denote this value is an "expecting object".

## Contributing

Feel free to create issues or merge requests with any improvement or fix you might find useful.
