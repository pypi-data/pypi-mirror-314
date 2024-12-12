from typing import Union, Iterable, Optional, Any, Tuple, List


class SegmentedString(str):
    """
    A class that acts like string, but it also provides a way to work with it in segments.

    The eq, lt, and gt methods are the same as the ones for ordinary strings.
    Therefore, there is no consideration of the segments.

    Example usage:
    >>> s = SegmentedString(("abc", "def", "ghi"), labels=("first", "second", "third"))
    >>> s
    'abcdefghi'
    >>> s.segments
    ('abc', 'def', 'ghi')
    >>> s.labels
    ('first', 'second', 'third')

    """

    def __new__(cls, value: Union[str, Iterable[str]], labels: Optional[Iterable[Any]] = None) -> "SegmentedString":
        if isinstance(value, str):
            if labels is not None:
                raise ValueError("Labels can only be provided when value is a sequence of strings")

            segments = tuple([value])
        else:
            segments = tuple(value)
            value = "".join(value)

        instance = super().__new__(cls, value)
        instance._segments = segments if len(value) > 0 else ()
        instance._labels = tuple(labels) if labels is not None else None

        return instance

    def num_of_segments(self) -> int:
        """
        Get the number of segments in the string.
        """
        return len(self._segments)

    @property
    def segments(self) -> Tuple[str, ...]:
        return self._segments

    @property
    def labels(self) -> Optional[Tuple[Any, ...]]:
        return self._labels

    def __add__(self, other):
        if isinstance(other, SegmentedString):
            # as the labels are voluntary, we need to check if they are present, there can be four cases

            labels = None
            if self._labels is not None and other._labels is not None:
                labels = self._labels + other._labels
            elif self._labels is not None:
                labels = self._labels + (None,) * other.num_of_segments()
            elif other._labels is not None:
                labels = (None,) * self.num_of_segments() + other._labels

            return SegmentedString(self._segments + other._segments, labels)
        else:
            labels = self._labels
            if labels is not None:
                labels = labels + (None,)
            return SegmentedString(self._segments + (other,), labels)

    def __mul__(self, other):
        if isinstance(other, int):
            if other < 0:
                raise ValueError("Can only multiply SegmentedString by a non-negative integer")
            if other == 0:
                return SegmentedString("")

            return SegmentedString(self._segments * other, self._labels * other if self._labels is not None else None)
        else:
            raise ValueError("Can only multiply SegmentedString by an integer")

    def __getitem__(self, item):
        if isinstance(item, slice):
            indices = range(len(self))[item]
            indices_2_segment_indices = []

            for i, s in enumerate(self._segments):
                indices_2_segment_indices.extend([i] * len(s))

            segments = [[]]

            previous_segment_index = indices_2_segment_indices[indices[0]]
            labels = [self._labels[previous_segment_index]] if self._labels is not None else None

            for i in indices:
                segment_index = indices_2_segment_indices[i]
                if segment_index != previous_segment_index:
                    segments.append([])
                    previous_segment_index = segment_index
                    if labels is not None:
                        labels.append(self._labels[segment_index])
                segments[-1].append(super().__getitem__(i))

            segments = ["".join(s) for s in segments]

            return SegmentedString(segments, labels)
        else:
            return SegmentedString(
                (super().__getitem__(item),),
                (self._labels[self.char_2_segment_index(range(len(self))[item])],) if self._labels is not None else None
            )

    def char_2_segment_index(self, char_index: int) -> int:
        """
        Get the index of the segment that contains the character at the given index.

        Args:
            char_index: The index of the character.

        Returns:
            The index of the segment.
        """
        if char_index < 0:
            raise ValueError("The character index must be non-negative")
        if char_index >= len(self):
            raise ValueError("The character index is out of range")

        for i, segment in enumerate(self._segments):
            if char_index < len(segment):
                return i
            char_index -= len(segment)

    @staticmethod
    def _add_item(item: Union["SegmentedString", str], segments: List[str], labels: Optional[List[Any]]) -> Optional[
        List[Any]]:
        """
        Helper method for join method, that helps to assemble segments and labels.

        Args:
        - item: The item to be added.
        - segments: The list of segments, is modified in place.
        - labels: The list of labels, is modified in place if not None. If None, it is created and returned.

        Returns:
            labels
        """
        if isinstance(item, SegmentedString):
            if labels is None:
                if item._labels is not None:
                    labels = [None] * len(segments)
                    labels.extend(item._labels)
            else:
                if item._labels is not None:
                    labels.extend(item._labels)
                else:
                    labels.extend([None] * item.num_of_segments())
            segments.extend(
                item._segments)  # need to be after labels, as labels are edited according to previous length of segments
        else:
            segments.append(item)
            if labels is not None:
                labels.append(None)

        return labels

    def join(self, __iterable: Iterable[Union["SegmentedString", str]]) -> "SegmentedString":
        segments = []

        __iterable = iter(__iterable)
        try:
            labels = self._add_item(next(__iterable), segments, None)
        except StopIteration:
            return SegmentedString("")

        for item in __iterable:
            labels = self._add_item(self, segments, labels)
            labels = self._add_item(item, segments, labels)

        return SegmentedString(segments, labels)
