# -*- coding: utf-8 -*-

"""
为了方便测试, 我们在 Confluence Cloud 上维护着这样一篇 Confluence Page
https://example.atlassian.net/wiki/spaces/JWBMT/pages/294223873/Atlassian+Document+Format+Parser+Test
里面包含了基本上所有主要文档元素和格式, 以及一些特殊情况, 用于测试解析器的正确性.

我们有一个 `脚本 <https://github.com/MacHu-GWU/atlas_doc_parser-project/tree/dev/scripts/get_examples>`_
可以将这个 Confluence Page 对应的 JSON 数据下载到本地, 以便于测试.

在 `test_model.py <https://github.com/MacHu-GWU/atlas_doc_parser-project/blob/dev/tests/test_model.py>`_
这个单元测试中, 我们需要使用很多 JSON 来进行测试. 有些 JSON 的体积太大了, 不适合直接放在代码中,
所以我们将这些 JSON 放在了这个模块中, 以便于让单元测试的代码更好维护, 并且方便需要的时候一键
点击跳转查看原始 JSON.
"""

import typing as T
import dataclasses

from .helper import check_seder, check_markdown

from ..model import T_DATA, T_NODE
from .. import model


@dataclasses.dataclass
class NodeCase:
    klass: T.Type[T_NODE] = dataclasses.field()
    data: T_DATA = dataclasses.field()
    md: str = dataclasses.field()
    node: T_NODE = dataclasses.field(init=False)

    def __post_init__(self):
        self.node = self.klass.from_dict(self.data)

    def test(self):
        check_seder(self.node)
        check_markdown(self.node, self.md)
        return self


class CaseEnum:
    block_card_with_url_to_markdown = NodeCase(
        klass=model.NodeBlockCard,
        data={
            "type": "blockCard",
            "attrs": {
                "url": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
            },
        },
        md="[https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)",
    )
    bullet_list_with_single_plain_text_item = NodeCase(
        klass=model.NodeBulletList,
        data={
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
        },
        md="- Hello world",
    )
    bullet_list_with_formatted_text_marks = NodeCase(
        klass=model.NodeBulletList,
        data={
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
        },
        md="- **Bold** and *italic* and `code`",
    )
    bullet_list_with_links_and_mixed_formatting = NodeCase(
        klass=model.NodeBulletList,
        data={
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
        },
        md="""
        - Visit [Atlassian](http://atlassian.com)
        - This is ~~strikethrough~~
        """,
    )
    bullet_list_with_nested_structure = NodeCase(
        klass=model.NodeBulletList,
        data={
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
        },
        md="""
        - item 1
        - item 2
            - item 2.1
                - item 2.1.1
                - item 2.1.2
            - item 2.2
                - item 2.2.1
                - item 2.2.2
        """,
    )
    code_block_none = NodeCase(
        klass=model.NodeCodeBlock,
        data={
            "type": "codeBlock",
            "attrs": {"language": "none"},
            "content": [{"text": "> Hello world", "type": "text"}],
        },
        md="""
        ```
        > Hello world
        ```
        """,
    )
    code_block_python = NodeCase(
        klass=model.NodeCodeBlock,
        data={
            "type": "codeBlock",
            "attrs": {"language": "python"},
            "content": [
                {"text": "def add_two(a, b):\n    return a + b", "type": "text"}
            ],
        },
        md="""
        ```python
        def add_two(a, b):
            return a + b
        ```
        """,
    )
    code_block_without_attributes = NodeCase(
        klass=model.NodeCodeBlock,
        data={
            "type": "codeBlock",
        },
        md="""
        ```
        
        ```
        """,
    )
    date_basic = NodeCase(
        klass=model.NodeDate,
        data={
            "type": "date",
            # Unix timestamp for 2024-01-01 00:00:00 UTC
            "attrs": {"timestamp": "1704067200000"},  # Note: ADF uses milliseconds
        },
        md="2024-01-01",
    )
    inline_card_url_to_markdown_link = NodeCase(
        klass=model.NodeInlineCard,
        data={
            "type": "inlineCard",
            "attrs": {
                "url": "https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/"
            },
        },
        md="[https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)",
    )
    list_item_with_simple_text = NodeCase(
        klass=model.NodeListItem,
        data={
            "type": "listItem",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Hello world"}],
                }
            ],
        },
        md="Hello world",
    )
    list_item_with_multiple_text_formats = NodeCase(
        klass=model.NodeListItem,
        data={
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
        },
        md="**Bold** and *italic* and `code`",
    )
    ordered_list_with_single_item = NodeCase(
        klass=model.NodeOrderedList,
        data={
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
        },
        md="1. Hello world",
    )
    ordered_list_with_formatted_text = NodeCase(
        klass=model.NodeOrderedList,
        data={
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
        },
        md="1. **Bold** and *italic* and `code`",
    )
    ordered_list_with_nested_structure = NodeCase(
        klass=model.NodeOrderedList,
        data={
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
        },
        md="""
        1. Alice
        2. Bob
        3. Cathy
            1. Cathy 1
                1. Cathy 1.1
                2. Cathy 1.2
            2. Cathy 2
                1. Cathy 2.1
                2. Cathy 2.2
        """,
    )
    ordered_list_custom_start_number = NodeCase(
        klass=model.NodeOrderedList,
        data={
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
        },
        md="5. Starting at 5",
    )
    media_external_image_basic_markdown = NodeCase(
        klass=model.NodeMedia,
        data={
            "type": "media",
            "attrs": {
                "width": 580,
                "type": "external",
                "url": "https://www.python.org/static/img/python-logo.png",
                "height": 164,
            },
        },
        md="![](https://www.python.org/static/img/python-logo.png)",
    )
    media_external_image_with_alt_text = NodeCase(
        klass=model.NodeMedia,
        data={
            "type": "media",
            "attrs": {
                "width": 580,
                "alt": "Python Logo",
                "type": "external",
                "url": "https://www.python.org/static/img/python-logo.png",
                "height": 164,
            },
        },
        md="![Python Logo](https://www.python.org/static/img/python-logo.png)",
    )
    media_external_image_with_hyperlink = NodeCase(
        klass=model.NodeMedia,
        data={
            "type": "media",
            "attrs": {
                "width": 580,
                "type": "external",
                "url": "https://www.python.org/static/img/python-logo.png",
                "height": 164,
            },
            "marks": [{"type": "link", "attrs": {"href": "https://www.python.org/"}}],
        },
        md="[![](https://www.python.org/static/img/python-logo.png)](https://www.python.org/)",
    )
    media_external_image_with_alt_and_link = NodeCase(
        klass=model.NodeMedia,
        data={
            "type": "media",
            "attrs": {
                "width": 580,
                "alt": "Python Logo",
                "type": "external",
                "url": "https://www.python.org/static/img/python-logo.png",
                "height": 164,
            },
            "marks": [{"type": "link", "attrs": {"href": "https://www.python.org/"}}],
        },
        md="[![Python Logo](https://www.python.org/static/img/python-logo.png)](https://www.python.org/)",
    )
    media_single_with_one_image = NodeCase(
        klass=model.NodeMediaSingle,
        data={
            "type": "mediaSingle",
            "attrs": {"layout": "center", "width": 250, "widthType": "pixel"},
            "content": [
                {
                    "type": "media",
                    "attrs": {
                        "width": 580,
                        "alt": "Python Logo",
                        "type": "external",
                        "url": "https://www.python.org/static/img/python-logo.png",
                        "height": 164,
                    },
                    "marks": [
                        {"type": "link", "attrs": {"href": "https://www.python.org/"}}
                    ],
                }
            ],
        },
        md="[![Python Logo](https://www.python.org/static/img/python-logo.png)](https://www.python.org/)",
    )
    mention_basic = NodeCase(
        klass=model.NodeMention,
        data={
            "type": "mention",
            "attrs": {
                "id": "70121:5e8e6032-7f3d-4cfa-a4f7-c1bce3f8f06a",
                "localId": "bed788de-f5fb-4cd2-9ee7-cdd775c66dc9",
                "text": "@alice",
            },
        },
        md="@alice",
    )
    panel_basic = NodeCase(
        klass=model.NodePanel,
        data={
            "type": "panel",
            "attrs": {"panelType": "info"},
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "Hello world"}],
                }
            ],
        },
        md="""
        > **INFO**
        > 
        > Hello world
        """,
    )
    panel_with_multiple_content_types = NodeCase(
        klass=model.NodePanel,
        data={
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
        },
        md="""
        > **WARNING**
        > 
        > ## Warning Title
        > 
        > - List item 1
        """,
    )
