# segmentedstring
Simple python class that acts like string, but it also provides a way to work with it in segments.


The eq, lt, and gt methods are the same as the ones for ordinary strings.
Therefore, there is no consideration of the segments.

Example usage:
```python
>>> s = SegmentedString(("abc", "def", "ghi"), labels=("first", "second", "third"))
>>> s
'abcdefghi'
>>> s.segments
('abc', 'def', 'ghi')
>>> s.labels
('first', 'second', 'third')
```