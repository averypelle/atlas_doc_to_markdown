# -*- coding: utf-8 -*-

import typing as T
import enum
import textwrap
import dataclasses
from datetime import datetime

from .arg import REQ, NA, rm_na
from .type_enum import TypeEnum
from .base import Base, T_DATA, T_DATA_LIKE


@dataclasses.dataclass
class BaseMark(Base):
    type: str = dataclasses.field(default_factory=REQ)

    def to_markdown(self, text: str) -> str:
        return text


T_MARK = T.TypeVar("T_MARK", bound=BaseMark)


@dataclasses.dataclass
class MarkBackGroundColorAttrs(Base):
    color: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkBackGroundColor(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.backgroundColor.value)
    attrs: MarkBackGroundColorAttrs = MarkBackGroundColorAttrs.nested_field(
        default_factory=NA
    )


@dataclasses.dataclass
class MarkCode(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.code.value)

    def to_markdown(self, text: str) -> str:
        return f"`{text}`"


@dataclasses.dataclass
class MarkEm(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.em.value)

    def to_markdown(self, text: str) -> str:
        return f"*{text}*"


@dataclasses.dataclass
class MarkLinkAttrs(Base):
    href: str = dataclasses.field(default_factory=REQ)
    title: str = dataclasses.field(default_factory=NA)
    id: str = dataclasses.field(default_factory=NA)
    collection: str = dataclasses.field(default_factory=NA)
    occurrenceKey: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkLink(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.link.value)
    attrs: MarkLinkAttrs = MarkLinkAttrs.nested_field(default_factory=REQ)

    def to_markdown(self, text: str) -> str:
        if isinstance(self.attrs.title, str):
            title = self.attrs.title
        else:
            title = text
        return f"[{title}]({self.attrs.href})"


@dataclasses.dataclass
class MarkStrike(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.strike.value)

    def to_markdown(self, text: str) -> str:
        return f"~~{text}~~"


@dataclasses.dataclass
class MarkStrong(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.strong.value)

    def to_markdown(self, text: str) -> str:
        return f"**{text}**"


@dataclasses.dataclass
class MarkSubSupAttrs(Base):
    type: str = dataclasses.field(default=TypeEnum.sub.value)


@dataclasses.dataclass
class MarkSubSup(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.subsup.value)
    attrs: MarkSubSupAttrs = MarkSubSupAttrs.nested_field(default_factory=NA)


@dataclasses.dataclass
class MarkTextColorAttrs(Base):
    color: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkTextColor(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.textColor.value)
    attrs: MarkTextColorAttrs = MarkTextColorAttrs.nested_field(default_factory=NA)


@dataclasses.dataclass
class MarkUnderLine(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.underline.value)


_mark_type_to_class_mapping = {
    TypeEnum.backgroundColor.value: MarkBackGroundColor,
    TypeEnum.code.value: MarkCode,
    TypeEnum.em.value: MarkEm,
    TypeEnum.link.value: MarkLink,
    TypeEnum.strike.value: MarkStrike,
    TypeEnum.strong.value: MarkStrong,
    TypeEnum.subsup.value: MarkSubSup,
    TypeEnum.textColor.value: MarkTextColor,
    TypeEnum.underline.value: MarkUnderLine,
}


def parse_mark(dct: T_DATA) -> "T_MARK":
    type_ = dct["type"]
    return _mark_type_to_class_mapping[type_].from_dict(dct)


@dataclasses.dataclass
class BaseNode(Base):
    type: str = dataclasses.field(default_factory=REQ)

    @classmethod
    def from_dict(
        cls,
        dct_or_obj: T_DATA_LIKE,
    ) -> T.Optional["Base"]:
        if "content" in dct_or_obj:
            if isinstance(dct_or_obj["content"], list):
                # print(f"{dct_or_obj = }")  # for debug only
                new_content = list()
                for d in dct_or_obj["content"]:
                    print(f"{d = }")  # for debug only
                    content = parse_node(d)
                    new_content.append(content)
                dct_or_obj["content"] = new_content
        if "marks" in dct_or_obj:
            if isinstance(dct_or_obj["marks"], list):
                # print(f"{dct_or_obj = }")  # for debug only
                new_marks = list()
                for d in dct_or_obj["marks"]:
                    # print(f"{d = }")  # for debug only
                    mark = parse_mark(d)
                    new_marks.append(mark)
                dct_or_obj["marks"] = new_marks
        print(f"{dct_or_obj = }")  # for debug only
        return super().from_dict(dct_or_obj)

    def to_markdown(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__} has not implemented the ``def to_markdown(self):`` method"
        )


T_NODE = T.TypeVar("T_NODE", bound=BaseNode)


def _content_to_markdown(content: T.Union[T.List["T_NODE"], NA]) -> str:
    if isinstance(content, NA):
        return ""
    else:
        lst = list()
        for node in content:
            print("----- Work on a new node -----")
            md = node.to_markdown()
            print(f"{node = }")
            print(f"{md = }")
            lst.append(md)
        return "".join(lst)


@dataclasses.dataclass
class NodeBlockQuote(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.blockquote.value)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=NA)

    def to_markdown(self) -> str:
        return textwrap.indent(
            _content_to_markdown(self.content),
            prefix=" " * 4,
        )


@dataclasses.dataclass
class NodeBulletList(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.bulletList.value)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        return f"- {_content_to_markdown(self.content)}"


@dataclasses.dataclass
class NodeCodeBlockAttrs(Base):
    language: str = dataclasses.field(default_factory=NA)


_atlassian_lang_to_markdown_lang_mapping = {}


@dataclasses.dataclass
class NodeCodeBlock(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.codeBlock.value)
    attrs: NodeCodeBlockAttrs = NodeCodeBlockAttrs.nested_field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default=NA)

    def to_markdown(self) -> str:
        code = _content_to_markdown(self.content)
        lang = ""
        if isinstance(self.attrs, NodeCodeBlockAttrs):
            if isinstance(self.attrs.language, str):
                lang = _atlassian_lang_to_markdown_lang_mapping.get(
                    self.attrs.language,
                    self.attrs.language,
                )
        return f"```{lang}\n{code}\n```"


@dataclasses.dataclass
class NodeDateAttrs(Base):
    timestamp: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodeDate(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.date.value)
    attrs: NodeDateAttrs = NodeDateAttrs.nested_field(default_factory=REQ)

    def to_markdown(self) -> str:
        return str(datetime.utcfromtimestamp(int(self.attrs.timestamp) / 1000).date())


@dataclasses.dataclass
class NodeDoc(BaseNode):
    version: int = dataclasses.field(default=1)
    type: str = dataclasses.field(default=TypeEnum.doc.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeEmojiAttrs(Base):
    shortName: str = dataclasses.field(default_factory=REQ)
    id: str = dataclasses.field(default_factory=NA)
    text: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeEmoji(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.emoji.value)
    attrs: NodeEmojiAttrs = NodeEmojiAttrs.nested_field(default_factory=REQ)

    def to_markdown(self) -> str:
        if isinstance(self.attrs.text, str):
            return self.attrs.text
        else:
            raise NotImplementedError


@dataclasses.dataclass
class NodeExpandAttrs(Base):
    title: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeExpand(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.expand.value)
    attrs: NodeExpandAttrs = NodeExpandAttrs.nested_field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default=NA)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeHardBreak(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.hardBreak.value)


@dataclasses.dataclass
class NodeHeadingAttrs(Base):
    level: int = dataclasses.field(default_factory=REQ)
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeHeading(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.heading.value)
    attrs: NodeHeadingAttrs = NodeHeadingAttrs.nested_field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return "#" * self.attrs.level + " " + _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeInlineCardAttrs(Base):
    url: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodeInlineCard(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.inlineCard.value)
    attrs: NodeInlineCardAttrs = NodeInlineCardAttrs.nested_field(default_factory=REQ)


@dataclasses.dataclass
class NodeListItem(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.listItem.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return f"- {_content_to_markdown(self.content)}"


@dataclasses.dataclass
class NodeMediaAttrs(Base):
    id: str = dataclasses.field(default_factory=NA)
    type: str = dataclasses.field(default_factory=REQ)
    collection: str = dataclasses.field(default_factory=NA)
    width: int = dataclasses.field(default_factory=NA)
    height: int = dataclasses.field(default_factory=NA)
    occurrenceKey: int = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMedia(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.media.value)
    attrs: NodeMediaAttrs = NodeMediaAttrs.nested_field(default_factory=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default=NA)


@dataclasses.dataclass
class NodeMediaGroup(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mediaGroup.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)


@dataclasses.dataclass
class NodeMediaSingleAttrs(Base):
    layout: str = dataclasses.field(default_factory=REQ)
    width: int = dataclasses.field(default_factory=NA)
    widthType: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMediaSingle(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mediaSingle.value)
    attrs: NodeMediaSingleAttrs = NodeMediaSingleAttrs.nested_field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeMentionAttrs(Base):
    id: str = dataclasses.field(default_factory=REQ)
    text: str = dataclasses.field(default_factory=NA)
    userType: str = dataclasses.field(default_factory=NA)
    accessLevel: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMention(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mention.value)
    attrs: NodeMentionAttrs = NodeMentionAttrs.nested_field(default_factory=REQ)


@dataclasses.dataclass
class NodeNestedExpandAttrs(Base):
    title: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeNestedExpand(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.nestedExpand.value)
    attrs: NodeNestedExpandAttrs = NodeNestedExpandAttrs.nested_field(
        default_factory=NA
    )
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)


@dataclasses.dataclass
class NodeOrderedListAttrs(Base):
    order: int = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeOrderedList(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.orderedList.value)
    attrs: NodeOrderedListAttrs = NodeOrderedListAttrs.nested_field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        if isinstance(self.attrs.order, int):
            order = self.attrs.order + 1
        else:
            raise ValueError
        return f"{order}. {_content_to_markdown(self.content)}"


@dataclasses.dataclass
class NodePanelAttrs(Base):
    panelType: int = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodePanel(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.panel.value)
    attrs: NodePanelAttrs = NodePanelAttrs.nested_field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return textwrap.indent(
            "\n".join(
                [
                    f"**{self.attrs.panelType}**",
                    "",
                    _content_to_markdown(self.content),
                ]
            ),
            prefix=" " * 4,
        )


@dataclasses.dataclass
class NodeParagraphAttrs(Base):
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeParagraph(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.paragraph.value)
    attrs: NodeParagraphAttrs = NodeParagraphAttrs.nested_field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default=NA)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeRule(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.rule.value)

    def to_markdown(self) -> str:
        return "---"


@dataclasses.dataclass
class NodeStatusAttrs(Base):
    text: str = dataclasses.field(default_factory=REQ)
    color: str = dataclasses.field(default="neutral")
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeStatus(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.status.value)
    attrs: NodeStatusAttrs = NodeStatusAttrs.nested_field(default_factory=REQ)

    def to_markdown(self) -> str:
        return f"`{self.attrs.text}`"


@dataclasses.dataclass
class NodeTable(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.table.value)


@dataclasses.dataclass
class NodeTableCell(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableCell.value)


@dataclasses.dataclass
class NodeTableHeader(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableHeader.value)


@dataclasses.dataclass
class NodeTableRow(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableRow.value)


@dataclasses.dataclass
class NodeText(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.text.value)
    text: str = dataclasses.field(default_factory=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default_factory=NA)

    def to_markdown(self):
        md = self.text
        if isinstance(self.marks, list):
            for mark in self.marks:
                md = mark.to_markdown(md)
        return md


_node_type_to_class_mapping = {
    TypeEnum.blockquote.value: NodeBlockQuote,
    TypeEnum.bulletList.value: NodeBulletList,
    TypeEnum.codeBlock.value: NodeCodeBlock,
    TypeEnum.date.value: NodeDate,
    TypeEnum.doc.value: NodeDoc,
    TypeEnum.emoji.value: NodeEmoji,
    TypeEnum.expand.value: NodeExpand,
    TypeEnum.hardBreak.value: NodeHardBreak,
    TypeEnum.heading.value: NodeHeading,
    TypeEnum.inlineCard.value: NodeInlineCard,
    TypeEnum.listItem.value: NodeListItem,
    TypeEnum.media.value: NodeMedia,
    TypeEnum.mediaGroup.value: NodeMediaGroup,
    TypeEnum.mediaSingle.value: NodeMediaSingle,
    TypeEnum.mention.value: NodeMention,
    TypeEnum.nestedExpand.value: NodeNestedExpand,
    TypeEnum.orderedList.value: NodeOrderedList,
    TypeEnum.panel.value: NodePanel,
    TypeEnum.paragraph.value: NodeParagraph,
    TypeEnum.rule.value: NodeRule,
    TypeEnum.status.value: NodeStatus,
    TypeEnum.table.value: NodeTable,
    TypeEnum.tableCell.value: NodeTableCell,
    TypeEnum.tableHeader.value: NodeTableHeader,
    TypeEnum.tableRow.value: NodeTableRow,
    TypeEnum.text.value: NodeText,
}


def parse_node(dct_or_obj: T_DATA_LIKE) -> "T_NODE":
    if isinstance(dct_or_obj, dict) is False:
        return dct_or_obj
    # print(f"{dct_or_obj = }")  # for debug only
    type_ = dct_or_obj["type"]
    klass = _node_type_to_class_mapping[type_]
    # print(f"{klass = }")  # for debug only
    return klass.from_dict(dct_or_obj)
