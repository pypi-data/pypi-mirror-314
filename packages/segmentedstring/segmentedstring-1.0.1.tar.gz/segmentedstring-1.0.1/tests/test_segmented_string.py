from unittest import TestCase

from segmentedstring import SegmentedString


class TestSegmentedString(TestCase):

    def setUp(self):
        self.segmented_string = SegmentedString((
            "hello",
            "world",
            "this",
            "is",
            "a",
            "test",
        ))
        self.segmented_string_with_labels = SegmentedString([
            "hello",
            "world",
            "this",
            "is",
            "a",
            "test",
        ], [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ])
        self.segmented_string_only_one_segment = SegmentedString(" ")
        self.segmented_string_only_one_segment_with_labels = SegmentedString((" ",), ("delimiter",))

    def test_getitem(self):
        self.assertEqual("h", self.segmented_string[0])
        self.assertEqual("h", self.segmented_string_with_labels[0])
        self.assertEqual(" ", self.segmented_string_only_one_segment[0])

        self.assertEqual("w", self.segmented_string[5])

        self.assertEqual("t", self.segmented_string[-1])
        self.assertEqual("t", self.segmented_string_with_labels[-1])
        self.assertEqual(" ", self.segmented_string_only_one_segment[-1])

        self.assertEqual("he", self.segmented_string[0:2])
        self.assertEqual("he", self.segmented_string_with_labels[0:2])

    def test_len(self):
        self.assertEqual(21, len(self.segmented_string))
        self.assertEqual(21, len(self.segmented_string_with_labels))
        self.assertEqual(1, len(self.segmented_string_only_one_segment))

    def test_segments(self):
        self.assertEqual(("hello", "world", "this", "is", "a", "test"), self.segmented_string.segments)
        self.assertEqual(("hello", "world", "this", "is", "a", "test"), self.segmented_string_with_labels.segments)
        self.assertEqual((" ",), self.segmented_string_only_one_segment.segments)

    def test_labels(self):
        self.assertEqual(None, self.segmented_string.labels)
        self.assertEqual(("1", "2", "3", "4", "5", "6"), self.segmented_string_with_labels.labels)

    def test_add_string(self):
        res = self.segmented_string + "!"
        self.assertEqual("helloworldthisisatest!", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!"), res.segments)
        self.assertEqual(None, res.labels)

        res = self.segmented_string_with_labels + "!"
        self.assertEqual("helloworldthisisatest!", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6", None), res.labels)

    def test_add_segmented_string(self):
        res = self.segmented_string + SegmentedString("!")
        self.assertEqual("helloworldthisisatest!", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!"), res.segments)
        self.assertEqual(None, res.labels)

        res = self.segmented_string_with_labels + SegmentedString("!")
        self.assertEqual("helloworldthisisatest!", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6", None), res.labels)

    def test_add_segmented_string_with_labels(self):
        res = self.segmented_string + SegmentedString(("!", "?"), ("exclamation", "question"))
        self.assertEqual("helloworldthisisatest!?", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!", "?"), res.segments)
        self.assertEqual((None, None, None, None, None, None, "exclamation", "question"), res.labels)

        res = self.segmented_string_with_labels + SegmentedString(("!", "?"), ("exclamation", "question"))
        self.assertEqual("helloworldthisisatest!?", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "!", "?"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6", "exclamation", "question"), res.labels)

    def test_mull(self):
        res = self.segmented_string * 2
        self.assertEqual("helloworldthisisatesthelloworldthisisatest", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "hello", "world", "this", "is", "a", "test"), res.segments)
        self.assertIsNone(res.labels)

        res = self.segmented_string_with_labels * 2
        self.assertEqual("helloworldthisisatesthelloworldthisisatest", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test", "hello", "world", "this", "is", "a", "test"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6", "1", "2", "3", "4", "5", "6"), res.labels)

        res = self.segmented_string * 0
        self.assertEqual("", res)
        self.assertEqual((), res.segments)
        self.assertEqual(None, res.labels)

        res = self.segmented_string_with_labels * 0
        self.assertEqual("", res)
        self.assertEqual((), res.segments)
        self.assertIsNone(res.labels)

    def test_join_strings_only(self):
        res = self.segmented_string_only_one_segment.join(["hello", "world", "this", "is", "a", "test"])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertIsNone(res.labels)

        res = self.segmented_string_only_one_segment_with_labels.join(["hello", "world", "this", "is", "a", "test"])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual((None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None), res.labels)

    def test_join_segmented_strings_only(self):
        res = self.segmented_string_only_one_segment.join(
            [SegmentedString("hello"), SegmentedString("world"), SegmentedString("this"), SegmentedString("is"),
             SegmentedString("a"), SegmentedString("test")])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertIsNone(res.labels)

        res = self.segmented_string_only_one_segment_with_labels.join(
            [SegmentedString("hello"), SegmentedString("world"), SegmentedString("this"), SegmentedString("is"),
             SegmentedString("a"), SegmentedString("test")])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual((None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None), res.labels)

    def test_join_segmented_strings_with_labels(self):
        res = self.segmented_string_only_one_segment.join(
            [SegmentedString(("hello",), ("1",), ), SegmentedString(("world",), ("2",), ),
             SegmentedString(("this",), ("3",), ), SegmentedString(("is",), ("4",), ),
             SegmentedString(("a",), ("5",), ), SegmentedString(("test",), ("6",), )])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual(("1", None, "2", None, "3", None, "4", None, "5", None, "6"), res.labels)

        res = self.segmented_string_only_one_segment_with_labels.join(
            [SegmentedString(("hello",), ("1",), ), SegmentedString(("world",), ("2",), ),
             SegmentedString(("this",), ("3",), ), SegmentedString(("is",), ("4",), ),
             SegmentedString(("a",), ("5",), ), SegmentedString(("test",), ("6",), )])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual(("1", "delimiter", "2", "delimiter", "3", "delimiter", "4", "delimiter", "5", "delimiter", "6"), res.labels)

    def test_join_mixed_type_strings(self):
        res = self.segmented_string_only_one_segment.join(
            ["hello", SegmentedString("world"), "this", SegmentedString("is"), "a", SegmentedString("test")])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertIsNone(res.labels)

        res = self.segmented_string_only_one_segment_with_labels.join(
            ["hello", SegmentedString("world"), "this", SegmentedString("is"), "a", SegmentedString("test")])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual((None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None, "delimiter", None), res.labels)

    def test_join_mixed_type_strings_with_labels(self):
        res = self.segmented_string_only_one_segment.join(
            [SegmentedString(("hello",), ("1",), ), "world", SegmentedString(("this",), ("3",), ), "is",
             SegmentedString(("a",), ("5",), ), "test"])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual(("1", None, None, None, "3", None, None, None, "5", None, None), res.labels)

        res = self.segmented_string_only_one_segment_with_labels.join(
            [SegmentedString(("hello",), ("1",), ), "world", SegmentedString(("this",), ("3",), ), "is",
             SegmentedString(("a",), ("5",), ), "test"])
        self.assertEqual("hello world this is a test", res)
        self.assertEqual(("hello", " ", "world", " ", "this", " ", "is", " ", "a", " ", "test"), res.segments)
        self.assertEqual(("1", "delimiter", None, "delimiter", "3", "delimiter", None, "delimiter", "5", "delimiter", None), res.labels)

    def test_getitem(self):
        res = self.segmented_string_with_labels[0]
        self.assertEqual("h", res)
        self.assertEqual(("h",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[3]
        self.assertEqual("l", res)
        self.assertEqual(("l",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[-1]
        self.assertEqual("t", res)
        self.assertEqual(("t",), res.segments)
        self.assertEqual(('6',), res.labels)

        res = self.segmented_string_with_labels[20]
        self.assertEqual("t", res)
        self.assertEqual(("t",), res.segments)
        self.assertEqual(('6',), res.labels)

        with self.assertRaises(Exception):
            self.segmented_string_with_labels[99]

    def test_getitem_slice(self):
        res = self.segmented_string_with_labels[0:1]
        self.assertEqual("h", res)
        self.assertEqual(("h",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[2:4]
        self.assertEqual("ll", res)
        self.assertEqual(("ll",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[0:5]
        self.assertEqual("hello", res)
        self.assertEqual(("hello",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[4:6]
        self.assertEqual("ow", res)
        self.assertEqual(("o", "w"), res.segments)
        self.assertEqual(('1', '2'), res.labels)

        res = self.segmented_string_with_labels[:1]
        self.assertEqual("h", res)
        self.assertEqual(("h",), res.segments)
        self.assertEqual(('1',), res.labels)

        res = self.segmented_string_with_labels[19:]
        self.assertEqual("st", res)
        self.assertEqual(("st",), res.segments)
        self.assertEqual(('6',), res.labels)

        res = self.segmented_string_with_labels[19:25]
        self.assertEqual("st", res)
        self.assertEqual(("st",), res.segments)
        self.assertEqual(('6',), res.labels)

        res = self.segmented_string_with_labels[-2:]
        self.assertEqual("st", res)
        self.assertEqual(("st",), res.segments)
        self.assertEqual(('6',), res.labels)

        res = self.segmented_string_with_labels[-2:-1]
        self.assertEqual("s", res)
        self.assertEqual(("s",), res.segments)
        self.assertEqual(('6',), res.labels)

        res = self.segmented_string_with_labels[:]
        self.assertEqual("helloworldthisisatest", res)
        self.assertEqual(("hello", "world", "this", "is", "a", "test"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6"), res.labels)

    def test_getitem_slice_step(self):
        res = self.segmented_string_with_labels[::2]
        self.assertEqual("hlooltiiaet", res)
        self.assertEqual(("hlo", "ol", "ti", "i", "a", "et"), res.segments)
        self.assertEqual(("1", "2", "3", "4", "5", "6"), res.labels)

        res = self.segmented_string_with_labels[::-2]
        self.assertEqual("teaiitloolh", res)
        self.assertEqual(('te', 'a', 'i', 'it', 'lo', 'olh'), res.segments)
        self.assertEqual(('6', '5', '4', '3', '2', '1'), res.labels)