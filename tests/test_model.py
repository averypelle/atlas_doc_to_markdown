# -*- coding: utf-8 -*-

import pytest

from atlas_doc_parser.exc import ParamError
from atlas_doc_parser.model import (
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
    NodeText,
    parse_node,
)
from atlas_doc_parser.tests import check_seder


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
        node = NodeBulletList.from_dict(data)
        check_seder(node)
        # assert node.to_markdown() == "- Hello world"

        # # Test case 2: Bullet list with formatted text (bold, italic, code)
        # data = {
        #     "type": "bulletList",
        #     "content": [
        #         {
        #             "type": "listItem",
        #             "content": [
        #                 {
        #                     "type": "paragraph",
        #                     "content": [
        #                         {
        #                             "type": "text",
        #                             "text": "Bold",
        #                             "marks": [{"type": "strong"}]
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": " and "
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": "italic",
        #                             "marks": [{"type": "em"}]
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": " and "
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": "code",
        #                             "marks": [{"type": "code"}]
        #                         }
        #                     ]
        #                 }
        #             ]
        #         }
        #     ]
        # }
        # node = NodeBulletList.from_dict(data)
        # check_seder(node)
        # assert node.to_markdown() == "- **Bold** and *italic* and `code`"
        #
        # # Test case 3: Multiple bullet points with links and mixed formatting
        # data = {
        #     "type": "bulletList",
        #     "content": [
        #         {
        #             "type": "listItem",
        #             "content": [
        #                 {
        #                     "type": "paragraph",
        #                     "content": [
        #                         {
        #                             "type": "text",
        #                             "text": "Visit ",
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": "Atlassian",
        #                             "marks": [
        #                                 {
        #                                     "type": "link",
        #                                     "attrs": {
        #                                         "href": "http://atlassian.com",
        #                                         "title": "Atlassian"
        #                                     }
        #                                 }
        #                             ]
        #                         }
        #                     ]
        #                 }
        #             ]
        #         },
        #         {
        #             "type": "listItem",
        #             "content": [
        #                 {
        #                     "type": "paragraph",
        #                     "content": [
        #                         {
        #                             "type": "text",
        #                             "text": "This is ",
        #                         },
        #                         {
        #                             "type": "text",
        #                             "text": "strikethrough",
        #                             "marks": [{"type": "strike"}]
        #                         }
        #                     ]
        #                 }
        #             ]
        #         }
        #     ]
        # }
        # node = NodeBulletList.from_dict(data)
        # check_seder(node)
        # assert node.to_markdown() == "- Visit [Atlassian](http://atlassian.com)\n- This is ~~strikethrough~~"


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


# class TestNodeDate:
#     def test(self):
#         pass
#
#
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
# class TestNodeOrderedList:
#     def test(self):
#         pass
#
#
# class TestNodePanel:
#     def test(self):
#         pass
#
#
# class TestNodeParagraph:
#     def test(self):
#         pass
#
#
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
#
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
        assert node.to_markdown() == "Hello world"

    def test_case_4(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "code"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Code mark should wrap text in backticks
        assert node.to_markdown() == "`Hello world`"

    def test_case_5(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "em"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # Emphasis should wrap text in asterisks
        assert node.to_markdown() == "*Hello world*"

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
        assert node.to_markdown() == "[Atlassian](http://atlassian.com)"

    def test_case_7(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strike"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "~~Hello world~~"

    def test_case_8(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "strong"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        assert node.to_markdown() == "**Hello world**"

    def test_case_9(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [{"type": "subsup", "attrs": {"type": "sub"}}],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        # Subscript doesn't have standard markdown equivalent, should return plain text
        assert node.to_markdown() == "Hello world"

    def test_case_10(self):
        data = {
            "type": "text",
            "text": "Hello world",
            "marks": [{"type": "textColor", "attrs": {"color": "#97a0af"}}],
        }
        node = NodeText.from_dict(data)
        check_seder(node)
        # Text color doesn't have markdown equivalent, should return plain text
        assert node.to_markdown() == "Hello world"

    def test_case_11(self):
        data = {"type": "text", "text": "Hello world", "marks": [{"type": "underline"}]}
        node = NodeText.from_dict(data)
        check_seder(node)
        # HTML underline doesn't have standard markdown equivalent, should return plain text
        assert node.to_markdown() == "Hello world"


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.model", preview=False)
