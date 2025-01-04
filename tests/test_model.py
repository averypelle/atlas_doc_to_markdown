# -*- coding: utf-8 -*-

import textwrap

import pytest

from atlas_doc_parser.exc import ParamError
from atlas_doc_parser.model import (
    MarkBackGroundColor,
    MarkCode,
    MarkEm,
    MarkLinkAttrs,
    MarkLink,
    MarkStrike,
    MarkStrong,
    MarkSubSup,
    MarkTextColor,
    MarkUnderLine,
    NodeBlockQuote,
    NodeBulletList,
    NodeCodeBlock,
    NodeDate,
    NodeDoc,
    NodeEmoji,
    NodeExpand,
    NodeHardBreak,
    NodeHeading,
    NodeInlineCard,
    NodeListItem,
    NodeMedia,
    NodeMediaGroup,
    NodeMediaSingle,
    NodeMention,
    NodeNestedExpand,
    NodeOrderedList,
    NodePanel,
    NodeParagraph,
    NodeRule,
    NodeStatus,
    NodeTable,
    NodeTableCell,
    NodeTableHeader,
    NodeTableRow,
    NodeTaskItem,
    NodeTaskList,
    NodeText,
    parse_node,
)
from atlas_doc_parser.tests import check_seder, check_markdown


class TestMarkBackGroundColor:
    def test_case_1(self):
        pass


class TestMarkCode:
    def test_basic_code_mark(self):
        """Test basic code mark creation and serialization."""
        data = {"type": "code"}
        mark = MarkCode.from_dict(data)
        check_seder(mark)

        # Verify the mark properties
        assert mark.type == "code"
        assert mark.to_dict() == data

        # Test markdown conversion
        assert mark.to_markdown("print('hello')") == "`print('hello')`"

    def test_code_mark_with_special_chars(self):
        """Test code mark with text containing special characters."""
        data = {"type": "code"}
        mark = MarkCode.from_dict(data)

        # Test with backticks in code
        text_with_backticks = "var x = `template string`"
        assert mark.to_markdown(text_with_backticks) == "`var x = `template string``"

        # Test with multiple lines
        multiline_code = "def func():\n    return True"
        assert mark.to_markdown(multiline_code) == "`def func():\n    return True`"

    def test_empty_code(self):
        """Test code mark with empty string."""
        data = {"type": "code"}
        mark = MarkCode.from_dict(data)
        assert mark.to_markdown("") == "``"

    def test_code_mark_whitespace(self):
        """Test code mark with various whitespace scenarios."""
        data = {"type": "code"}
        mark = MarkCode.from_dict(data)

        # Test with leading/trailing whitespace
        assert mark.to_markdown("  code  ") == "`  code  `"

        # Test with tabs
        assert mark.to_markdown("\tcode\t") == "`\tcode\t`"

        # Test with newlines
        assert mark.to_markdown("code\nmore code") == "`code\nmore code`"


class TestMarkEm:
    def test_case_1(self):
        pass


class TestMarkLink:
    def test_case_1(self):
        """Test basic link creation with title."""
        data = {
            "type": "link",
            "attrs": {"href": "http://atlassian.com", "title": "Atlassian"},
        }
        mark = MarkLink.from_dict(data)
        check_seder(mark)

        assert isinstance(mark.attrs, MarkLinkAttrs)
        assert mark.to_dict() == data
        assert mark.to_markdown("Atlassian") == "[Atlassian](http://atlassian.com)"

    def test_case_2(self):
        """Test link without title."""
        data = {"type": "link", "attrs": {"href": "http://example.com"}}
        mark = MarkLink.from_dict(data)
        check_seder(mark)
        # When no title is provided, it should use the text content
        assert mark.to_markdown("Click here") == "[Click here](http://example.com)"

    def test_case_4(self):
        """Test error handling for missing required attributes."""
        data = {"type": "link", "attrs": {}}
        with pytest.raises(ParamError):
            MarkLink.from_dict(data)

    def test_case_5(self):
        """Test link with special characters in URL."""
        data = {
            "type": "link",
            "attrs": {
                "href": "http://example.com/path?param=value&other=123",
                "title": "Complex URL",
            },
        }
        mark = MarkLink.from_dict(data)
        check_seder(mark)

        assert (
            mark.to_markdown("Special Link")
            == "[Complex URL](http://example.com/path?param=value&other=123)"
        )


class TestMarkStrike:
    def test_case_1(self):
        pass


class TestMarkStrong:
    def test_basic_strong_mark(self):
        """Test basic strong mark creation and markdown conversion."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        assert mark.to_markdown("Hello world") == "**Hello world**"

    def test_strong_mark_with_special_chars(self):
        """Test strong mark with text containing special characters."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        special_text = "Hello * World ** !"
        assert mark.to_markdown(special_text) == f"**{special_text}**"

    def test_strong_mark_empty_text(self):
        """Test strong mark with empty text."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        assert mark.to_markdown("") == "****"

    def test_strong_mark_with_whitespace(self):
        """Test strong mark with text containing various whitespace."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        text_with_spaces = "  Hello  World  "
        assert mark.to_markdown(text_with_spaces) == f"**{text_with_spaces}**"


class TestMarkSubSup:
    def test_case_1(self):
        pass


class TestMarkTextColor:
    def test_case_1(self):
        pass


class TestMarkUnderLine:
    def test_case_1(self):
        pass


# class TestNodeBlockQuote:
#     def test(self):
#         pass
#
#
class TestNodeBulletList:
    def test_case_1(self):
        # Simple bullet list with plain text
        data = {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Hello world"}],
                        }
                    ],
                }
            ],
        }
        node: NodeBulletList = NodeBulletList.from_dict(data)
        node_list_item = node.content[0]
        assert isinstance(node_list_item, NodeListItem)
        node_paragraph = node_list_item.content[0]
        assert isinstance(node_paragraph, NodeParagraph)
        node_text = node_paragraph.content[0]
        assert isinstance(node_text, NodeText)

        check_seder(node)
        expected = "- Hello world"
        check_markdown(node, expected)

    def test_case_2(self):
        # Test case 2: Bullet list with formatted text (bold, italic, code)
        data = {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Bold",
                                    "marks": [{"type": "strong"}],
                                },
                                {"type": "text", "text": " and "},
                                {
                                    "type": "text",
                                    "text": "italic",
                                    "marks": [{"type": "em"}],
                                },
                                {"type": "text", "text": " and "},
                                {
                                    "type": "text",
                                    "text": "code",
                                    "marks": [{"type": "code"}],
                                },
                            ],
                        }
                    ],
                }
            ],
        }
        node = NodeBulletList.from_dict(data)
        check_seder(node)
        expected = "- **Bold** and *italic* and `code`"
        check_markdown(node, expected)

    def test_case_3(self):
        # Test case 3: Multiple bullet points with links and mixed formatting
        data = {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Visit ",
                                },
                                {
                                    "type": "text",
                                    "text": "Atlassian",
                                    "marks": [
                                        {
                                            "type": "link",
                                            "attrs": {
                                                "href": "http://atlassian.com",
                                                "title": "Atlassian",
                                            },
                                        }
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "This is ",
                                },
                                {
                                    "type": "text",
                                    "text": "strikethrough",
                                    "marks": [{"type": "strike"}],
                                },
                            ],
                        }
                    ],
                },
            ],
        }
        node = NodeBulletList.from_dict(data)
        check_seder(node)
        expected = """
        - Visit [Atlassian](http://atlassian.com)
        - This is ~~strikethrough~~
        """
        check_markdown(node, expected)

    def test_case_4(self):
        data = {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "item 1", "type": "text"}],
                        }
                    ],
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "item 2", "type": "text"}],
                        },
                        {
                            "type": "bulletList",
                            "content": [
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"text": "item 2.1", "type": "text"}
                                            ],
                                        },
                                        {
                                            "type": "bulletList",
                                            "content": [
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "item 2.1.1",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "item 2.1.2",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"text": "item 2.2", "type": "text"}
                                            ],
                                        },
                                        {
                                            "type": "bulletList",
                                            "content": [
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "item 2.2.1",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "item 2.2.2",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        node = NodeBulletList.from_dict(data)
        check_seder(node)
        expected = """
        - item 1
        - item 2
            - item 2.1
                - item 2.1.1
                - item 2.1.2
            - item 2.2
                - item 2.2.1
                - item 2.2.2
        """
        check_markdown(node, expected)


class TestNodeCodeBlock:
    def test_case_1(self):
        data = {
            "type": "codeBlock",
            "attrs": {"language": "python"},
            "content": [
                {"text": "def add_two(a, b):\n    return a + b", "type": "text"}
            ],
        }
        check_seder(NodeCodeBlock.from_dict(data))

    def test_case_2(self):
        data = {
            "type": "codeBlock",
        }
        check_seder(NodeCodeBlock.from_dict(data))


class TestNodeDate:
    def test_basic_date_node(self):
        """Test basic date node creation and conversion."""
        # Unix timestamp for 2024-01-01 00:00:00 UTC
        data = {
            "type": "date",
            "attrs": {"timestamp": "1704067200000"},  # Note: ADF uses milliseconds
        }
        node = NodeDate.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "2024-01-01"

    def test_missing_timestamp(self):
        """Test error handling for missing timestamp."""
        data = {"type": "date", "attrs": {}}
        with pytest.raises(ParamError):
            NodeDate.from_dict(data)

    def test_invalid_timestamp_format(self):
        """Test error handling for invalid timestamp format."""
        data = {"type": "date", "attrs": {"timestamp": "not-a-timestamp"}}
        node = NodeDate.from_dict(data)
        with pytest.raises(ValueError):
            node.to_markdown()

    def test_timestamp_conversion(self):
        """Test various timestamp conversions."""
        test_cases = [
            # (timestamp in ms, expected date string)
            ("0", "1970-01-01"),  # Unix epoch
            ("1704067200000", "2024-01-01"),  # 2024 New Year
            ("1735689600000", "2025-01-01"),  # 2025 New Year
        ]

        for timestamp, expected in test_cases:
            data = {"type": "date", "attrs": {"timestamp": timestamp}}
            node = NodeDate.from_dict(data)
            check_seder(node)
            assert node.to_markdown() == expected

    def test_very_large_timestamp(self):
        """Test handling of very large timestamps."""
        # Year 2100 timestamp
        data = {"type": "date", "attrs": {"timestamp": "4102444800000"}}
        node = NodeDate.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "2100-01-01"


# class TestNodeDoc:
#     def test(self):
#         pass
#
#
# class TestNodeEmoji:
#     def test(self):
#         pass
#
#
# class TestNodeExpand:
#     def test(self):
#         pass
#
#
# class TestNodeHardBreak:
#     def test(self):
#         pass
#
#
# class TestNodeHeading:
#     def test(self):
#         pass
#
#
# class TestNodeInlineCard:
#     def test(self):
#         pass
#
#
# class TestNodeListItem:
#     def test(self):
#         pass
#
#
# class TestNodeMedia:
#     def test(self):
#         pass
#
#
# class TestNodeMediaGroup:
#     def test(self):
#         pass
#
#
# class TestNodeMediaSingle:
#     def test(self):
#         pass
#
#
# class TestNodeMention:
#     def test(self):
#         pass
#
#
# class TestNodeNestedExpand:
#     def test(self):
#         pass
#
#
class TestNodeOrderedList:
    def test_case_1(self):
        """Test basic ordered list with simple text"""
        data = {
            "type": "orderedList",
            "attrs": {"order": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "Hello world", "type": "text"}],
                        }
                    ],
                }
            ],
        }
        node = NodeOrderedList.from_dict(data)
        check_seder(node)
        expected = "1. Hello world"
        check_markdown(node, expected)

    def test_case_2(self):
        """Test ordered list with formatted text (bold, italic, code)"""
        data = {
            "type": "orderedList",
            "attrs": {"order": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Bold",
                                    "marks": [{"type": "strong"}],
                                },
                                {"type": "text", "text": " and "},
                                {
                                    "type": "text",
                                    "text": "italic",
                                    "marks": [{"type": "em"}],
                                },
                                {"type": "text", "text": " and "},
                                {
                                    "type": "text",
                                    "text": "code",
                                    "marks": [{"type": "code"}],
                                },
                            ],
                        }
                    ],
                }
            ],
        }
        node = NodeOrderedList.from_dict(data)
        check_seder(node)
        expected = "1. **Bold** and *italic* and `code`"
        check_markdown(node, expected)

    def test_case_3(self):
        """Test nested ordered list with multiple levels"""
        data = {
            "type": "orderedList",
            "attrs": {"order": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "Alice", "type": "text"}],
                        }
                    ],
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "Bob", "type": "text"}],
                        }
                    ],
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "Cathy", "type": "text"}],
                        },
                        {
                            "type": "orderedList",
                            "attrs": {"order": 1},
                            "content": [
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"text": "Cathy 1", "type": "text"}
                                            ],
                                        },
                                        {
                                            "type": "orderedList",
                                            "attrs": {"order": 1},
                                            "content": [
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "Cathy 1.1",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "Cathy 1.2",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"text": "Cathy 2", "type": "text"}
                                            ],
                                        },
                                        {
                                            "type": "orderedList",
                                            "attrs": {"order": 1},
                                            "content": [
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "Cathy 2.1",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                                {
                                                    "type": "listItem",
                                                    "content": [
                                                        {
                                                            "type": "paragraph",
                                                            "content": [
                                                                {
                                                                    "text": "Cathy 2.2",
                                                                    "type": "text",
                                                                }
                                                            ],
                                                        }
                                                    ],
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        node = NodeOrderedList.from_dict(data)
        check_seder(node)
        expected = """
        1. Alice
        2. Bob
        3. Cathy
            1. Cathy 1
                1. Cathy 1.1
                2. Cathy 1.2
            2. Cathy 2
                1. Cathy 2.1
                2. Cathy 2.2
        """
        check_markdown(node, expected)

    def test_case_4(self):
        """Test ordered list with custom starting number"""
        data = {
            "type": "orderedList",
            "attrs": {"order": 5},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "Starting at 5", "type": "text"}],
                        }
                    ],
                }
            ],
        }
        node = NodeOrderedList.from_dict(data)
        check_seder(node)
        assert node.to_markdown().strip() == "5. Starting at 5"


class TestNodePanel:
    def test_basic_panel(self):
        """Test basic panel with simple text content."""
        data = {
            "type": "panel",
            "attrs": {"panelType": "info"},
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Hello world"}],
                }
            ],
        }
        node = NodePanel.from_dict(data)
        check_seder(node)
        # Panel should format with indentation and panel type header
        expected = """
        > **INFO**
        > 
        > Hello world
        """
        check_markdown(node, expected)

    def test_panel_with_multiple_content_types(self):
        """Test panel with multiple allowed content types."""
        data = {
            "type": "panel",
            "attrs": {"panelType": "warning"},
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": "Warning Title"}],
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "List item 1"}
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
        }
        node = NodePanel.from_dict(data)
        check_seder(node)
        expected = """
        > **WARNING**
        > 
        > ## Warning Title
        > 
        > - List item 1
        """
        check_markdown(node, expected)


class TestNodeParagraph:
    def test_case_1(self):
        """Test basic paragraph with simple text"""
        data = {
            "type": "paragraph",
            "content": [{"type": "text", "text": "Hello world"}],
        }
        node = NodeParagraph.from_dict(data)
        assert node.to_dict() == data

        check_seder(node)
        expected = "Hello world"
        check_markdown(node, expected)

    def test_case_2(self):
        """Test paragraph with no content"""
        data = {
            "type": "paragraph",
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        expected = ""
        check_markdown(node, expected)

    def test_case_3(self):
        """Test paragraph with multiple text nodes"""
        data = {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Hello"},
                {"type": "text", "text": " "},
                {"type": "text", "text": "world"},
            ],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        expected = "Hello world"
        check_markdown(node, expected)

    def test_case_4(self):
        """Test paragraph with formatted text (multiple marks)"""
        data = {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Bold", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "italic", "marks": [{"type": "em"}]},
            ],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        expected = "**Bold** and *italic*"
        check_markdown(node, expected)

    def test_case_5(self):
        """Test paragraph with localId attribute"""
        data = {
            "type": "paragraph",
            "attrs": {"localId": "unique-id-123"},
            "content": [{"type": "text", "text": "Hello world"}],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        assert node.to_markdown().strip() == "Hello world"
        assert node.attrs.localId == "unique-id-123"

    def test_case_7(self):
        """Test paragraph with emoji and mention"""
        data = {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Hello "},
                {"type": "emoji", "attrs": {"shortName": ":smile:", "text": "😊"}},
                {"type": "text", "text": " "},
                {"type": "mention", "attrs": {"id": "123", "text": "@user"}},
            ],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        # The exact output will depend on how emoji and mention are implemented
        # in their respective to_markdown() methods
        expected = "Hello 😊 @user"
        check_markdown(node, expected)

    def test_case_8(self):
        """Test paragraph with link"""
        data = {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": "Visit us at ",
                },
                {
                    "type": "text",
                    "text": "HERE",
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {
                                "href": "https://example.com",
                            },
                        }
                    ],
                },
            ],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        expected = "Visit us at [HERE](https://example.com)"
        check_markdown(node, expected)


# class TestNodeRule:
#     def test(self):
#         pass
#
#
# class TestNodeStatus:
#     def test(self):
#         pass
#
#
# class TestNodeTable:
#     def test(self):
#         pass
#
#
# class TestNodeTableCell:
#     def test(self):
#         pass
#
#
# class TestNodeTableHeader:
#     def test(self):
#         pass
#
#
# class TestNodeTableRow:
#     def test(self):
#         pass
#


class TestNodeTaskItem:
    def test_basic_task_item(self):
        data = {
            "type": "taskItem",
            "attrs": {"state": "DONE", "localId": "25"},
            "content": [{"text": "Do this", "type": "text"}],
        }
        node = NodeTaskItem.from_dict(data)
        check_seder(node)
        expected = "[x] Do this"
        check_markdown(node, expected)

        data = {
            "type": "taskItem",
            "attrs": {"state": "TODO", "localId": "26"},
            "content": [{"text": "And do this", "type": "text"}],
        }
        node = NodeTaskItem.from_dict(data)
        check_seder(node)
        expected = "[ ] And do this"
        check_markdown(node, expected)


class TestNodeTaskList:
    def test_basic_task_list(self):
        """Test basic task list with completed and task items."""
        data = {
            "type": "taskList",
            "attrs": {"localId": ""},
            "content": [
                {
                    "type": "taskItem",
                    "attrs": {"state": "DONE", "localId": "25"},
                    "content": [{"text": "Do this", "type": "text"}],
                },
                {
                    "type": "taskItem",
                    "attrs": {"state": "TODO", "localId": "26"},
                    "content": [{"text": "And do this", "type": "text"}],
                },
            ],
        }
        node = NodeTaskList.from_dict(data)
        check_seder(node)
        expected = """
        - [x] Do this
        - [ ] And do this
        """
        check_markdown(node, expected)

    def test_nested_task_list(self):
        data = {
            "type": "taskList",
            "attrs": {"localId": ""},
            "content": [
                {
                    "type": "taskItem",
                    "attrs": {"state": "DONE", "localId": "25"},
                    "content": [{"text": "Do this", "type": "text"}],
                },
                {
                    "type": "taskItem",
                    "attrs": {"state": "TODO", "localId": "26"},
                    "content": [{"text": "And do this", "type": "text"}],
                },
                {
                    "type": "taskList",
                    "attrs": {"localId": ""},
                    "content": [
                        {
                            "type": "taskItem",
                            "attrs": {"state": "TODO", "localId": "27"},
                            "content": [
                                {"text": "sub ", "type": "text"},
                                {
                                    "text": "task 1",
                                    "type": "text",
                                    "marks": [{"type": "code"}],
                                },
                            ],
                        },
                        {
                            "type": "taskList",
                            "attrs": {"localId": ""},
                            "content": [
                                {
                                    "type": "taskItem",
                                    "attrs": {"state": "DONE", "localId": "28"},
                                    "content": [
                                        {"text": "sub task 1.1", "type": "text"}
                                    ],
                                },
                                {
                                    "type": "taskItem",
                                    "attrs": {"state": "TODO", "localId": "29"},
                                    "content": [
                                        {"text": "sub task 1.2", "type": "text"}
                                    ],
                                },
                            ],
                        },
                        {
                            "type": "taskItem",
                            "attrs": {"state": "TODO", "localId": "30"},
                            "content": [
                                {"text": "sub ", "type": "text"},
                                {
                                    "text": "task 2",
                                    "type": "text",
                                    "marks": [{"type": "strong"}],
                                },
                            ],
                        },
                        {
                            "type": "taskList",
                            "attrs": {"localId": ""},
                            "content": [
                                {
                                    "type": "taskItem",
                                    "attrs": {"state": "TODO", "localId": "31"},
                                    "content": [
                                        {"text": "sub task 2.1", "type": "text"}
                                    ],
                                },
                                {
                                    "type": "taskItem",
                                    "attrs": {"state": "DONE", "localId": "32"},
                                    "content": [
                                        {"text": "sub task 2.2", "type": "text"}
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        node = NodeTaskList.from_dict(data)
        check_seder(node)
        expected = textwrap.dedent(
            """
            - [x] Do this
            - [ ] And do this
                - [ ] sub `task 1`
                    - [x] sub task 1.1
                    - [ ] sub task 1.2
                - [ ] sub **task 2**
                    - [ ] sub task 2.1
                    - [x] sub task 2.2
            """
        )
        check_markdown(node, expected)


class TestNodeText:
    def test_case_1(self):
        data = {"type": "text", "text": "Hello world"}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Plain text should remain unchanged
        assert node.to_markdown() == "Hello world"

    def test_case_2(self):
        data = {"type": "text"}
        with pytest.raises(ParamError):
            NodeText.from_dict(data)

    def test_case_3(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [{"type": "backgroundColor", "attrs": {"color": "#fedec8"}}],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        # Background color doesn't have markdown equivalent, should return plain text
        expected = "Hello world"
        check_markdown(node, expected)

    def test_case_4(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "code"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Code mark should wrap text in backticks
        expected = "`Hello world`"
        check_markdown(node, expected)

    def test_case_5(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "em"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Emphasis should wrap text in asterisks
        expected = "*Hello world*"
        check_markdown(node, expected)

    def test_case_6(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [
                {
                    "type": "link",
                    "attrs": {"href": "http://atlassian.com", "title": "Atlassian"},
                }
            ],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        expected = "[Atlassian](http://atlassian.com)"
        check_markdown(node, expected)

    def test_case_7(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strike"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "~~Hello world~~"

    def test_case_8(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strong"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        expected = "**Hello world**"
        check_markdown(node, expected)

    def test_case_9(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [{"type": "subsup", "attrs": {"type": "sub"}}],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        # Subscript doesn't have standard markdown equivalent, should return plain text
        expected = "Hello world"
        check_markdown(node, expected)

    def test_case_10(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [{"type": "textColor", "attrs": {"color": "#97a0af"}}],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        # Text color doesn't have markdown equivalent, should return plain text
        expected = "Hello world"
        check_markdown(node, expected)

    def test_case_11(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "underline"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # HTML underline doesn't have standard markdown equivalent, should return plain text
        expected = "Hello world"
        check_markdown(node, expected)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.model", preview=False)
