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
    NodeBlockCard,
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
from atlas_doc_parser.tests.case import NodeCase, CaseEnum


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

    def test_code_mark_with_empty_string(self):
        """Test code mark with empty string."""
        data = {"type": "code"}
        mark = MarkCode.from_dict(data)
        assert mark.to_markdown("") == "``"

    def test_code_mark_preserves_whitespace_and_newlines(self):
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
    def test_link_mark_with_title_and_href(self):
        data = {
            "type": "link",
            "attrs": {"href": "http://atlassian.com", "title": "Atlassian"},
        }
        mark = MarkLink.from_dict(data)
        check_seder(mark)

        assert isinstance(mark.attrs, MarkLinkAttrs)
        assert mark.to_dict() == data
        assert mark.to_markdown("Atlassian") == "[Atlassian](http://atlassian.com)"

    def test_link_mark_without_title_uses_text(self):
        data = {"type": "link", "attrs": {"href": "http://example.com"}}
        mark = MarkLink.from_dict(data)
        check_seder(mark)
        # When no title is provided, it should use the text content
        assert mark.to_markdown("Click here") == "[Click here](http://example.com)"

    def test_link_mark_missing_required_attrs_raises(self):
        data = {"type": "link", "attrs": {}}
        with pytest.raises(ParamError):
            MarkLink.from_dict(data)

    def test_link_mark_with_special_chars_in_url(self):
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

    def test_strong_mark_with_empty_string(self):
        """Test strong mark with empty text."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        assert mark.to_markdown("") == "****"

    def test_strong_mark_preserves_whitespace(self):
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


class TestNodeBlockCard:
    def test_block_card_with_url_to_markdown(self):
        CaseEnum.block_card_with_url_to_markdown.test()


class TestNodeBlockQuote:
    def test(self):
        pass


class TestNodeBulletList:
    def test_bullet_list_with_single_plain_text_item(self):
        case = CaseEnum.bullet_list_with_single_plain_text_item.test()

        node = case.node
        node_list_item = node.content[0]
        assert isinstance(node_list_item, NodeListItem)
        node_paragraph = node_list_item.content[0]
        assert isinstance(node_paragraph, NodeParagraph)
        node_text = node_paragraph.content[0]
        assert isinstance(node_text, NodeText)

    def test_bullet_list_with_formatted_text_marks(self):
        CaseEnum.bullet_list_with_formatted_text_marks.test()

    def test_bullet_list_with_links_and_mixed_formatting(self):
        CaseEnum.bullet_list_with_links_and_mixed_formatting.test()

    def test_bullet_list_with_nested_structure(self):
        CaseEnum.bullet_list_with_nested_structure.test()


class TestNodeCodeBlock:
    def test_code_block_none(self):
        CaseEnum.code_block_none.test()

    def test_code_block_python(self):
        CaseEnum.code_block_python.test()

    def test_code_block_without_attributes(self):
        CaseEnum.code_block_without_attributes.test()


class TestNodeDate:
    def test_date_basic(self):
        CaseEnum.date_basic.test()

    def test_missing_timestamp(self):
        # Test error handling for missing timestamp.
        data = {"type": "date", "attrs": {}}
        with pytest.raises(ParamError):
            NodeDate.from_dict(data)

    def test_invalid_timestamp_format(self):
        # Test error handling for invalid timestamp format.
        data = {"type": "date", "attrs": {"timestamp": "not-a-timestamp"}}
        node = NodeDate.from_dict(data)
        with pytest.raises(ValueError):
            node.to_markdown()

    def test_timestamp_conversion(self):
        # Test various timestamp conversions.
        test_cases = [
            # (timestamp in ms, expected date string)
            ("0", "1970-01-01"),  # Unix epoch
            ("1704067200000", "2024-01-01"),  # 2024 New Year
            ("1735689600000", "2025-01-01"),  # 2025 New Year
        ]
        for timestamp, expected in test_cases:
            case = NodeCase(
                klass=NodeDate,
                data={"type": "date", "attrs": {"timestamp": timestamp}},
                md=expected,
            )
            case.test()

    def test_very_large_timestamp(self):
        # Test handling of very large timestamps.
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
class TestNodeInlineCard:
    def test_inline_card_url_to_markdown_link(self):
        CaseEnum.inline_card_url_to_markdown_link.test()


class TestNodeListItem:
    def test_list_item_with_simple_text(self):
        CaseEnum.list_item_with_simple_text.test()

    def test_list_item_with_multiple_text_formats(self):
        CaseEnum.list_item_with_multiple_text_formats.test()


class TestNodeMedia:
    def test_media_external_image_basic_markdown(self):
        CaseEnum.media_external_image_basic_markdown.test()

    def test_media_external_image_with_alt_text(self):
        CaseEnum.media_external_image_with_alt_text.test()

    def test_media_external_image_with_hyperlink(self):
        CaseEnum.media_external_image_with_hyperlink.test()

    def test_media_external_image_with_alt_and_link(self):
        CaseEnum.media_external_image_with_alt_and_link.test()


class TestNodeMediaGroup:
    def test_case_1(self):
        pass


class TestNodeMediaSingle:
    def test_media_single_with_one_image(self):
        CaseEnum.media_single_with_one_image.test()


class TestNodeMention:
    def test_mention_basic(self):
        CaseEnum.mention_basic.test()


class TestNodeNestedExpand:
    def test(self):
        pass


class TestNodeOrderedList:
    def test_ordered_list_with_single_item(self):
        CaseEnum.ordered_list_with_single_item.test()

    def test_ordered_list_with_formatted_text(self):
        CaseEnum.ordered_list_with_formatted_text.test()

    def test_ordered_list_with_nested_structure(self):
        CaseEnum.ordered_list_with_nested_structure.test()

    def test_ordered_list_custom_start_number(self):
        CaseEnum.ordered_list_custom_start_number.test()


class TestNodePanel:
    def test_panel_basic(self):
        CaseEnum.panel_basic.test()

    def test_panel_with_multiple_content_types(self):
        CaseEnum.panel_with_multiple_content_types.test()


class TestNodeParagraph:
    def test_paragraph_with_simple_text(self):
        data = {
            "type": "paragraph",
            "content": [{"type": "text", "text": "Hello world"}],
        }
        node = NodeParagraph.from_dict(data)
        assert node.to_dict() == data

        check_seder(node)
        expected = "Hello world"
        check_markdown(node, expected)

    def test_paragraph_without_content(self):
        data = {
            "type": "paragraph",
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        expected = ""
        check_markdown(node, expected)

    def test_paragraph_with_multiple_text_nodes(self):
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

    def test_paragraph_with_multiple_text_formats(self):
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

    def test_paragraph_with_local_id(self):
        data = {
            "type": "paragraph",
            "attrs": {"localId": "unique-id-123"},
            "content": [{"type": "text", "text": "Hello world"}],
        }
        node = NodeParagraph.from_dict(data)
        check_seder(node)
        assert node.to_markdown().strip() == "Hello world"
        assert node.attrs.localId == "unique-id-123"

    def test_paragraph_with_emoji_and_mention(self):
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

    def test_paragraph_with_hyperlink(self):
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


class TestNodeRule:
    def test_rule_basic(self):
        case = NodeCase(
            klass=NodeRule,
            data={"type": "rule"},
            md="---",
        )
        case.test()


# class TestNodeStatus:
#     def test(self):
#         pass
#
#
class TestNodeTable:
    def test_table_with_complex_nested_content(self):
        data = {
            "type": "table",
            "attrs": {
                "layout": "default",
                "width": 760.0,
                "localId": "662e4ab6-11fd-4afa-8c15-613b7bee54cb",
            },
            "content": [
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableHeader",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "text": "Col 1",
                                            "type": "text",
                                            "marks": [{"type": "strong"}],
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "type": "tableHeader",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "text": "Col 2",
                                            "type": "text",
                                            "marks": [{"type": "strong"}],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "key 1", "type": "text"}],
                                },
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "text": "special character | is not markdown friendly",
                                            "type": "text",
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "value 1", "type": "text"}],
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
                                                            "text": "this is ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "text": "Alice",
                                                            "type": "text",
                                                            "marks": [
                                                                {"type": "strong"}
                                                            ],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "Bob",
                                                            "type": "text",
                                                            "marks": [{"type": "em"}],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "Cathy",
                                                            "type": "text",
                                                            "marks": [
                                                                {"type": "underline"}
                                                            ],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "David",
                                                            "type": "text",
                                                            "marks": [
                                                                {"type": "strike"}
                                                            ],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "Edward",
                                                            "type": "text",
                                                            "marks": [{"type": "code"}],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "Frank",
                                                            "type": "text",
                                                            "marks": [
                                                                {
                                                                    "type": "subsup",
                                                                    "attrs": {
                                                                        "type": "sub"
                                                                    },
                                                                }
                                                            ],
                                                        },
                                                        {"text": ", ", "type": "text"},
                                                        {
                                                            "text": "George",
                                                            "type": "text",
                                                            "marks": [
                                                                {
                                                                    "type": "subsup",
                                                                    "attrs": {
                                                                        "type": "sup"
                                                                    },
                                                                }
                                                            ],
                                                        },
                                                        {"text": ".", "type": "text"},
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
                                                            "text": "This line has titled hyperlink ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "text": "Atlas Doc Format",
                                                            "type": "text",
                                                            "marks": [
                                                                {
                                                                    "type": "link",
                                                                    "attrs": {
                                                                        "href": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
                                                                    },
                                                                }
                                                            ],
                                                        },
                                                        {"text": ".", "type": "text"},
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
                                                            "text": "This line has url hyperlink ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "type": "inlineCard",
                                                            "attrs": {
                                                                "url": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
                                                            },
                                                        },
                                                        {
                                                            "text": "    ",
                                                            "type": "text",
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
                                                            "text": "This line has inline hyperlink ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "type": "inlineCard",
                                                            "attrs": {
                                                                "url": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
                                                            },
                                                        },
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
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "key 2", "type": "text"}],
                                },
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "text": "special character | is not markdown friendly",
                                            "type": "text",
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "value 2", "type": "text"}],
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
                                                            "text": "Alice",
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
                                                        {"text": "Bob", "type": "text"}
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
                                                            "text": "Cathy",
                                                            "type": "text",
                                                        }
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
                                                                            "text": "Cathy 1",
                                                                            "type": "text",
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "type": "orderedList",
                                                                    "attrs": {
                                                                        "order": 1
                                                                    },
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
                                                                        {
                                                                            "text": "Cathy 2",
                                                                            "type": "text",
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "type": "orderedList",
                                                                    "attrs": {
                                                                        "order": 1
                                                                    },
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
                                },
                            ],
                        },
                    ],
                },
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "key 3", "type": "text"}],
                                },
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "text": "special character | is not markdown friendly",
                                            "type": "text",
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 1, "rowspan": 1},
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "value 3", "type": "text"}],
                                },
                                {
                                    "type": "taskList",
                                    "attrs": {"localId": ""},
                                    "content": [
                                        {
                                            "type": "taskItem",
                                            "attrs": {"state": "DONE", "localId": "33"},
                                            "content": [
                                                {"text": "Do this", "type": "text"}
                                            ],
                                        },
                                        {
                                            "type": "taskItem",
                                            "attrs": {"state": "TODO", "localId": "34"},
                                            "content": [
                                                {"text": "And do ", "type": "text"},
                                                {
                                                    "text": "this",
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
                                                    "attrs": {
                                                        "state": "TODO",
                                                        "localId": "35",
                                                    },
                                                    "content": [
                                                        {
                                                            "text": "sub ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "text": "task",
                                                            "type": "text",
                                                            "marks": [{"type": "code"}],
                                                        },
                                                        {"text": " 1", "type": "text"},
                                                    ],
                                                },
                                                {
                                                    "type": "taskList",
                                                    "attrs": {"localId": ""},
                                                    "content": [
                                                        {
                                                            "type": "taskItem",
                                                            "attrs": {
                                                                "state": "DONE",
                                                                "localId": "36",
                                                            },
                                                            "content": [
                                                                {
                                                                    "text": "sub ",
                                                                    "type": "text",
                                                                },
                                                                {
                                                                    "text": "task",
                                                                    "type": "text",
                                                                    "marks": [
                                                                        {
                                                                            "type": "underline"
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "text": " 1.1",
                                                                    "type": "text",
                                                                },
                                                            ],
                                                        },
                                                        {
                                                            "type": "taskItem",
                                                            "attrs": {
                                                                "state": "TODO",
                                                                "localId": "37",
                                                            },
                                                            "content": [
                                                                {
                                                                    "text": "sub ",
                                                                    "type": "text",
                                                                },
                                                                {
                                                                    "text": "task",
                                                                    "type": "text",
                                                                    "marks": [
                                                                        {
                                                                            "type": "strike"
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "text": " 1.2",
                                                                    "type": "text",
                                                                },
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "type": "taskItem",
                                                    "attrs": {
                                                        "state": "TODO",
                                                        "localId": "38",
                                                    },
                                                    "content": [
                                                        {
                                                            "text": "sub ",
                                                            "type": "text",
                                                        },
                                                        {
                                                            "text": "task",
                                                            "type": "text",
                                                            "marks": [
                                                                {"type": "strong"}
                                                            ],
                                                        },
                                                        {"text": " 2", "type": "text"},
                                                    ],
                                                },
                                                {
                                                    "type": "taskList",
                                                    "attrs": {"localId": ""},
                                                    "content": [
                                                        {
                                                            "type": "taskItem",
                                                            "attrs": {
                                                                "state": "TODO",
                                                                "localId": "39",
                                                            },
                                                            "content": [
                                                                {
                                                                    "text": "sub ",
                                                                    "type": "text",
                                                                },
                                                                {
                                                                    "text": "task",
                                                                    "type": "text",
                                                                    "marks": [
                                                                        {
                                                                            "type": "textColor",
                                                                            "attrs": {
                                                                                "color": "#ff5630"
                                                                            },
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "text": " 2.1",
                                                                    "type": "text",
                                                                },
                                                            ],
                                                        },
                                                        {
                                                            "type": "taskItem",
                                                            "attrs": {
                                                                "state": "DONE",
                                                                "localId": "40",
                                                            },
                                                            "content": [
                                                                {
                                                                    "text": "sub ",
                                                                    "type": "text",
                                                                },
                                                                {
                                                                    "text": "task",
                                                                    "type": "text",
                                                                    "marks": [
                                                                        {
                                                                            "type": "backgroundColor",
                                                                            "attrs": {
                                                                                "color": "#c6edfb"
                                                                            },
                                                                        }
                                                                    ],
                                                                },
                                                                {
                                                                    "text": " 2.2",
                                                                    "type": "text",
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
                        },
                    ],
                },
            ],
        }
        node = NodeTable.from_dict(data)
        check_seder(node)
        expected = r"""
        | **Col 1**<br> | **Col 2**<br> |
        | --- | --- |
        | key 1<br>special character \| is not markdown friendly<br> | value 1<br>- this is **Alice**, *Bob*, Cathy, ~~David~~, `Edward`, Frank, George.<br>- This line has titled hyperlink [Atlas Doc Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).<br>- This line has url hyperlink [https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)<br>- This line has inline hyperlink [https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) |
        | key 2<br>special character \| is not markdown friendly<br> | value 2<br>1. Alice<br>2. Bob<br>3. Cathy<br>    1. Cathy 1<br>        1. Cathy 1.1<br>        2. Cathy 1.2<br>    2. Cathy 2<br>        1. Cathy 2.1<br>        2. Cathy 2.2 |
        | key 3<br>special character \| is not markdown friendly<br> | value 3<br>- [x] Do this<br>- [ ] And do **this**<br>    - [ ] sub `task` 1<br>        - [x] sub task 1.1<br>        - [ ] sub ~~task~~ 1.2<br>    - [ ] sub **task** 2<br>        - [ ] sub task 2.1<br>        - [x] sub task 2.2 |
        """
        check_markdown(node, expected)


class TestNodeTableCell:
    def test_table_cell_with_escaped_pipe_char(self):
        data = {
            "type": "tableCell",
            "attrs": {"colspan": 1, "rowspan": 1},
            "content": [
                {"type": "paragraph", "content": [{"text": "key 1", "type": "text"}]},
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "special character | is not markdown friendly",
                            "type": "text",
                        }
                    ],
                },
            ],
        }
        node = NodeTableCell.from_dict(data)
        check_seder(node)
        expected = r"key 1<br>special character \| is not markdown friendly<br>"
        check_markdown(node, expected)

    def test_table_cell_with_bullet_list(self):
        data = {
            "type": "tableCell",
            "attrs": {"colspan": 1, "rowspan": 1},
            "content": [
                {"type": "paragraph", "content": [{"text": "value 1", "type": "text"}]},
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "a", "type": "text"}],
                                }
                            ],
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"text": "b", "type": "text"}],
                                }
                            ],
                        },
                    ],
                },
            ],
        }
        node = NodeTableCell.from_dict(data)
        check_seder(node)
        expected = "value 1<br>- a<br>- b"
        check_markdown(node, expected)


class TestNodeTableHeader:
    def test_table_header_with_bold_text(self):
        data = {
            "type": "tableHeader",
            "attrs": {"colspan": 1, "rowspan": 1},
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"text": "Col 1", "type": "text", "marks": [{"type": "strong"}]}
                    ],
                }
            ],
        }
        node = NodeTableHeader.from_dict(data)
        check_seder(node)
        expected = "**Col 1**<br>"
        check_markdown(node, expected)


class TestNodeTableRow:
    def test_table_row_with_multiple_cells(self):
        data = {
            "type": "tableRow",
            "content": [
                {
                    "type": "tableCell",
                    "attrs": {"colspan": 1, "rowspan": 1},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "key 1", "type": "text"}],
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": "special character | is not markdown friendly",
                                    "type": "text",
                                }
                            ],
                        },
                    ],
                },
                {
                    "type": "tableCell",
                    "attrs": {"colspan": 1, "rowspan": 1},
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": "value 1", "type": "text"}],
                        },
                        {
                            "type": "bulletList",
                            "content": [
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [{"text": "a", "type": "text"}],
                                        }
                                    ],
                                },
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [{"text": "b", "type": "text"}],
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        node = NodeTableRow.from_dict(data)
        check_seder(node)
        expected = r"| key 1<br>special character \| is not markdown friendly<br> | value 1<br>- a<br>- b |"
        check_markdown(node, expected)


class TestNodeTaskItem:
    def test_task_item_done_and_todo_states(self):
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
    def test_task_list_with_multiple_states(self):
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

    def test_task_list_with_nested_structure(self):
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
    def test_text_node_plain_text(self):
        data = {"type": "text", "text": "Hello world"}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Plain text should remain unchanged
        assert node.to_markdown() == "Hello world"

    def test_text_node_missing_text_raises(self):
        data = {"type": "text"}
        with pytest.raises(ParamError):
            NodeText.from_dict(data)

    def test_text_node_with_strong_emphasis(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strong"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        expected = "**Hello world**"
        check_markdown(node, expected)

    def test_text_node_with_italic(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "em"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Emphasis should wrap text in asterisks
        expected = "*Hello world*"
        check_markdown(node, expected)

    def test_text_node_with_underline(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "underline"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # HTML underline doesn't have standard markdown equivalent, should return plain text
        expected = "Hello world"
        check_markdown(node, expected)

    def test_text_node_with_strikethrough(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strike"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "~~Hello world~~"

    def test_text_node_with_code_mark(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "code"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Code mark should wrap text in backticks
        expected = "`Hello world`"
        check_markdown(node, expected)

    def test_text_node_with_subscript(self):
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

    def test_text_node_with_text_color(self):
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

    def test_text_node_with_background_color(self):
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

    def test_text_node_with_titled_hyperlink(self):
        data = {
            "text": "Atlas Doc Format",
            "type": "text",
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
                    },
                }
            ],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        expected = "[Atlas Doc Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)"
        check_markdown(node, expected)

    def test_text_node_with_url_hyperlink(self):
        data = {
            "text": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/",
            "type": "text",
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
                    },
                }
            ],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        expected = "[https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)"
        check_markdown(node, expected)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.model", preview=False)
