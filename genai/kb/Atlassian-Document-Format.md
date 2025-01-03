# Atlassian Document Format

## Purpose

The Atlassian Document Format (ADF) represents rich text stored in Atlassian products. For example, in Jira Cloud platform, the text in issue comments and in `textarea` custom fields is stored as ADF.

## JSON schema

An Atlassian Document Format document is a JSON object. A JSON schema is available to validate documents. This JSON schema is found at [http://go.atlassian.com/adf-json-schema](http://go.atlassian.com/adf-json-schema).

> **Note**: Marks and nodes included in the JSON schema may not be valid in this implementation. Refer to this documentation for details of supported marks and nodes.

## JSON structure

An ADF document is composed of a hierarchy of *nodes*. There are two categories of nodes: block and inline. Block nodes define the structural elements of the document such as headings, paragraphs, lists, and alike. Inline nodes contain the document content such as text and images. Some of these nodes can take *marks* that define text formatting or embellishment such as centered, bold, italics, and alike.

To center text: add a mark of the type alignment with an attribute `align` and the value `center`.

A document is *ordered*, that is, there's a single sequential path through it: traversing a document in sequence and concatenating the nodes yields content in the correct order.

For example:

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello "
        },
        {
          "type": "text",
          "text": "world",
          "marks": [
            {
              "type": "strong"
            }
          ]
        }
      ]
    }
  ]
}
```

Result in the text "Hello **world**".

## Nodes

Nodes have the following common properties:

| Property | Required | Description |
|----------|----------|-------------|
| type | ✓ | Defines the type of block node such as `paragraph`, `table`, and alike. |
| content | ✓ in block nodes, not applicable in inline nodes | An array contaning inline and block nodes that define the content of a section of the document. |
| version | ✓ in the root, otherwise not applicable | Defines the version of ADF used in this representation. |
| marks | | Defines text decoration or formatting. |
| attrs | | Further information defining attributes of the block such as the language represented in a block of code. |

### Block nodes

Block nodes can be subdivided into:

* the root (`doc`) node.
* top level nodes, nodes that can be placed directly below the root node.
* child nodes, nodes that have to be the child of a higher-level mode.

Some top-level nodes can be used as child nodes. For example, the `paragraph` node can be used at the top level or embedded within a list or table.

#### Root block node

Every document starts with a root `doc` node. This node contains the `version` and `content` properties. The simplest document in ADF is this root node with no content:

```json
{
  "version": 1,
  "type": "doc",
  "content": []
}
```

### Top-level block nodes

The top-level block nodes include:

* `blockquote`
* `bulletList`
* `codeBlock`
* `expand`
* `heading`
* `mediaGroup`
* `mediaSingle`
* `orderedList`
* `panel`
* `paragraph`
* `rule`
* `table`
* `multiBodiedExtension`

### Child block nodes

The child block nodes include:

* `listItem`
* `media`
* `nestedExpand`
* `tableCell`
* `tableHeader`
* `tableRow`
* `extensionFrame`

## Inline nodes

The inline nodes include:

* `date`
* `emoji`
* `hardBreak`
* `inlineCard`
* `mention`
* `status`
* `text`
* `mediaInline`

## Marks

Mark have the following properties:

| Property | Required | Description |
|----------|----------|-------------|
| type | ✓ | Defines the type of mark such as `code`, `link`, and alike. |
| attrs | | Further information defining attributes of the mask such as the URL in a link. |

The marks include:

* `border`
* `code`
* `em`
* `link`
* `strike`
* `strong`
* `subsup`
* `textColor`
* `underline`

# Node - blockquote

## Purpose
The `blockquote` node is a container for quotes.

## Type
`blockquote` is a top-level block node.

## Example
```json
{
  "type": "blockquote",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "blockquote" |
| content | ✓ | array | An array of nodes |

## Content
`content` must contain array of one or more of the following nodes:

* `paragraph` with no marks
* `bulletList`
* `orderedList`
* `codeBlock`
* `mediaGroup`
* `mediaSingle`

# Node - bulletList

## Purpose
The `bulletList` node is a container for list items.

## Type
`bulletList` is a top-level block node.

## Example
```json
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
              "type": "text",
              "text": "Hello world"
            }
          ]
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "bulletList" |
| content | ✓ | array | An array of nodes |

## Content
`content` can contain one or more `listItem` nodes.

# Node - codeBlock

## Purpose

The `codeBlock` node is a container for lines of code.

## Type

`codeBlock` is a top-level block node.

## Example

```json
{
  "type": "codeBlock",
  "attrs": {
    "language": "javascript"
  },
  "content": [
    {
      "type": "text",
      "text": "var foo = {};\nvar bar = [];"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "codeBlock" |
| content | | array | An array of nodes |
| attrs | | object | |
| attrs.language | | string | Language of the code lines |

## Content

`content` takes an array of one or more `text` nodes without marks.

## Attributes

* `language` for syntax highlighting, a code language supported by [Prism](https://prismjs.com/). See [available languages imports](https://github.com/conorhastings/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD) for a list of the languages supported in Prism. If set to `text` or an unsupported value, code is rendered as plain, monospaced text.

# Node - date

## Purpose
The `date` node displays a date in the user's locale.

## Type
`date` is an inline node.

## Example
```json
{
  "type": "date",
  "attrs": {
    "timestamp": "1582152559"
  }
}
```

## Marks
`date` does not support any marks.

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "date" |
| attrs | ✓ | object | |
| attrs.timestamp | ✓ | string | "*unix timestamp in milliseconds*" |

# Node - doc

## Purpose
The `doc` node is the root container node representing a document.

## Example
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "doc" |
| content | ✓ | array | An array of zero or more nodes |
| version | ✓ | integer | 1 |

## Content
`content` takes zero or more top-level block nodes.

## Version
`version` represents the version of the ADF specification used in the document.

# Node - emoji

## Purpose
The `emoji` node is an inline node that represents an emoji.

There are three kinds of emoji:
* Standard – Unicode emoji
* Atlassian – Non-standard emoji introduced by Atlassian  
* Site – Non-standard customer defined emoji

## Type
`emoji` is an inline node.

## Examples

### Unicode emoji
```json
{
  "type": "emoji",
  "attrs": {
    "shortName": ":grinning:",
    "text": "😀"
  }
}
```

### Non-standard Atlassian emoji
```json
{
  "type": "emoji",
  "attrs": {
    "shortName": ":awthanks:",
    "id": "atlassian-awthanks",
    "text": ":awthanks:"
  }
}
```

### Non-standard customer emoji
```json
{
  "type": "emoji",
  "attrs": {
    "shortName": ":thumbsup::skin-tone-2:",
    "id": "1f44d",
    "text": "👍🏽"
  }
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "emoji" |
| attrs | ✓ | object | |
| attrs.id | | string | Emoji service ID of the emoji |
| attrs.shortName | ✓ | string | |
| attrs.text | | string | |

## Attributes

* `id` is the Emoji service ID of the emoji. The value varies based on the kind, for example, standard emoji ID "1f3f3-1f308", Atlassian emoji ID "atlassian-<shortName>", and site emoji ID "13d29267-ff9e-4892-a484-1a1eef3b5ca3". The value is not intended to have any user facing meaning.
* `shortName` represent a name for the emoji, such as ":grinning:"
* `text` represents the text version of the emoji, `shortName` is rendered instead if omitted.

# Node - expand

## Purpose

The `expand` node is a container that enables content to be hidden or shown, similar to an accordion or disclosure widget.

Note: To add an expand to a table (`tableCell` or `tableHeader`) use `nestedExpand` instead.

## Type

`expand` is a top-level block node.

## Example

```json
{
  "type": "expand",
  "attrs": {
    "title": "Hello world"
  },
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "expand" |
| content | ✓ | array | Array of one or more nodes |
| attrs | ✓ | object | |
| attrs.title | | string | A title for the expand |
| marks | | array | An optional mark |

## Content

`expand` takes an array of one or more of the following nodes:

* `bulletList`
* `blockquote`
* `codeblock`
* `heading`
* `mediaGroup`
* `mediaSingle`
* `orderedList`
* `panel`
* `paragraph`
* `rule`
* `table`
* `multiBodiedExtension`
* `extensionFrame`
* `nestedExpand`

# Node - hardBreak

## Purpose

The `hardBreak` node inserts a new line in a text string. It's the equivalent to a <br/> in HTML.

## Type

`hardBreak` is an [inline](cloud/jira/platform/apis/document/structure#inline-nodes) node.

## Example

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello"
        },
        {
          "type": "hardBreak"
        },
        {
          "type": "text",
          "text": "world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "hardBreak" |
| attrs | | object | |
| attrs.text | | string | "\n" |

I've:
1. Preserved all headings with appropriate Markdown levels (#)
2. Maintained code blocks using triple backticks with language specification
3. Converted the HTML table to Markdown table format
4. Kept all inline code formatting using backticks
5. Removed all styling-related HTML and CSS
6. Preserved links but simplified their format
7. Maintained the document structure while making it more readable

# Node - heading

## Purpose

The `heading` node represents a heading.

## Content

`heading` is a [top-level block](https://your-docs-link/structure#top-level-block-nodes) node.

## Example

```json
{
  "type": "heading",
  "attrs": {
    "level": 1
  },
  "content": [
    {
      "type": "text",
      "text": "Heading 1"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "heading" |
| content | | array | Array of zero or more inline nodes |
| attrs | ✓ | object | |
| attrs.level | ✓ | integer | 1-6 |
| attrs.localId | | string | An ID to uniquely identify this node within the document. |

## Content

`content` takes any [inline](https://your-docs-link/structure#inline-nodes) node.

## Attributes

* `level` represents the depth of the heading following the same convention as HTML: when level is set to 1 it's the equivalent of `<h1>`.

# Node - inlineCard

## Purpose

The `inlineCard` node is an Atlassian link card with a type icon and content description derived from the link.

## Type

`inlineCard` is an [inline node](https://your-docs-link/structure#inline-nodes).

## Example

```json
{
  "type": "inlineCard",
  "attrs": {
    "url": "https://atlassian.com"
  }
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "inlineCard" |
| attrs | ✓ | object | |
| attrs.data | | object | [JSONLD](https://json-ld.org/) representation of the link |
| attrs.url | | object | A URI |

## Attributes

Either `data` or `url` must be provided, but not both.

# Node - listItem

## Purpose

The `listItem` node represents an item in a list.

## Type

`listItem` is a [child block node](https://your-docs-link/structure#child-block-nodes) of:

* [`bulletList`](https://your-docs-link/nodes/bulletList)
* [`orderedList`](https://your-docs-link/nodes/orderedList)

## Example

```json
{
  "type": "listItem",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "listItem" |
| content | ✓ | array | An array of one or more nodes. |

## Content

`content` must contain at least one of the following nodes:

* [`bulletList`](https://your-docs-link/nodes/bulletList)
* [`codeBlock`](https://your-docs-link/nodes/codeBlock) with no marks
* [`mediaSingle`](https://your-docs-link/nodes/mediaSingle)
* [`orderedList`](https://your-docs-link/nodes/orderedList)
* [`paragraph`](https://your-docs-link/nodes/paragraph) with no marks

# Node - media

## Purpose

The `media` node represents a single file or link stored in media services.

## Type

`media` is a [child block node](/cloud/jira/platform/apis/document/structure#child-block-nodes) of:

* [`mediaGroup`](/cloud/jira/platform/apis/document/nodes/mediaGroup)
* [`mediaSingle`](/cloud/jira/platform/apis/document/nodes/mediaSingle)

## Example

```json
{
  "type": "media",
  "attrs": {
    "id": "4478e39c-cf9b-41d1-ba92-68589487cd75",
    "type": "file", 
    "collection": "MediaServicesSample",
    "alt": "moon.jpeg",
    "width": 225,
    "height": 225
  },
  "marks": [
    {
      "type": "link",
      "attrs": {
        "href": "https://developer.atlassian.com/platform/atlassian-document-format/concepts/document-structure/nodes/media/#media"
      }
    },
    {
      "type": "border",
      "attrs": {
        "color": "#091e4224",
        "size": 2
      }
    },
    {
      "type": "annotation",
      "attrs": {
        "id": "c4cbe18e-9902-4734-bf9b-1426a81ef785",
        "annotationType": "inlineComment"
      }
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|--------|
| type | ✓ | string | "media" |
| attrs | ✓ | object | |
| attrs.width | | integer | A positive integer |
| attrs.height | | integer | A positive integer |
| attrs.id | ✓ | string | Media Services ID |
| attrs.type | ✓ | string | "file", "link" |
| attrs.collection | ✓ | string | Media Services Collection name |
| attrs.occurrenceKey | | string | Non‐empty string |

## Attributes

* `width` defines the display width of the media item in pixels. Must be provided within `mediaSingle` or the media isn't displayed.
* `height` defines the display height of the media item in pixels. Must be provided within `mediaSingle` or the media isn't displayed.
* `id` is the Media Services ID and is used for querying the media services API to retrieve metadata, such as, filename. Consumers of the document should always fetch fresh metadata using the Media API.
* `type` whether the media is a file or a link.
* `collection` the Media Services Collection name for the media.
* `occurrenceKey` needs to be present in order to enable deletion of files from a collection.

## Marks

The following marks can be applied:

* [`border`](/cloud/jira/platform/apis/document/marks/border)
* [`link`](/cloud/jira/platform/apis/document/marks/link)

# Node - mediaGroup

## Purpose

The `mediaGroup` node is a container for several media items. Compare to `mediaSingle`, which is intended for the display of a single media item in full.

## Type

`mediaGroup` is a top-level block node.

## Example

```json
{
  "type": "mediaGroup",
  "content": [
    {
      "type": "media",
      "attrs": {
        "type": "file",
        "id": "6e7c7f2c-dd7a-499c-bceb-6f32bfbf30b5",
        "collection": "ae730abd-a389-46a7-90eb-c03e75a45bf6"
      }
    },
    {
      "type": "media",
      "attrs": {
        "type": "file",
        "id": "6e7c7f2c-dd7a-499c-bceb-6f32bfbf30b5",
        "collection": "ae730abd-a389-46a7-90eb-c03e75a45bf6"
      }
    }
  ]
}
```

## Fields

| Name    | Required | Type   | Value              |
|---------|----------|--------|-------------------|
| type    | ✓        | string | "mediaGroup"      |
| content | ✓        | array  | An array of nodes |

## Content

`content` must contain one or more `media` nodes.

# Node - mediaSingle

## Purpose

The `mediaSingle` node is a container for *one* media item. This node enables the display of the content in full, in contrast to a `mediaGroup` that is intended for a list of attachments. A common use case is to display an image, but it can also be used for videos, or other types of content usually renderable by a `@atlaskit/media` card component.

## Type

`mediaSingle` is a top-level block node.

## Example

```json
{
  "type": "mediaSingle",
  "attrs": {
    "layout": "center"
  },
  "content": [
    {
      "type": "media",
      "attrs": {
        "id": "4478e39c-cf9b-41d1-ba92-68589487cd75",
        "type": "file",
        "collection": "MediaServicesSample",
        "alt": "moon.jpeg",
        "width": 225,
        "height": 225
      }
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|--------|
| type | ✓ | string | "mediaSingle" |
| content | ✓ | array | An array of nodes |
| attrs | ✓ | object | |
| attrs.layout | ✓ | string | "wrap-left", "center", "wrap-right", "wide", "full-width", "align-start", "align-end" |
| attrs.width | | number | Floating point number between 0 and 100 |
| attrs.widthType | | enum | pixel or percentage |

## Content

`content` must be a `media` node.

## Attributes

* `layout` determines the placement of the node on the page. `wrap-left` and `wrap-right` provide an image floated to the left or right of the page respectively, with text wrapped around it. `center` center aligns the image as a block, while `wide` does the same but bleeds into the margins. `full-width` makes the image stretch from edge to edge of the page.
* `width` determines the width of the image as a percentage of the width of the text content area. Has no effect if layout mode is `wide` or `full-width`.
* `widthType` [optional] determines what the "unit" of the width attribute is presenting. Possible values are `pixel` and `percentage`. If the widthType attribute is undefined, it fallbacks to percentage.

# Node - mention

## Purpose

The `mention` node represents a user mention.

## Type

`mention` is an inline node.

## Examples

```json
{
  "type": "mention",
  "attrs": {
    "id": "ABCDE-ABCDE-ABCDE-ABCDE",
    "text": "@Bradley Ayers",
    "userType": "APP"
  }
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|--------|
| type | ✓ | string | "mention" |
| attrs | ✓ | object | |
| attrs.accessLevel | | string | "NONE", "SITE", "APPLICATION", "CONTAINER" |
| attrs.id | ✓ | string | Atlassian Account ID or collection name |
| attrs.text | | string | |
| attrs.userType | | string | "DEFAULT", "SPECIAL", "APP" |

## Attributes

* `accessLevel`
* `id` the Atlassian account ID or collection name of the person or collection being mentioned.
* `text` the textual representation of the mention, including a leading @.
* `userType`

# Node - nestedExpand

## Purpose

The `nestedExpand` node is a container that allows content to be hidden or shown, similar to an accordion or disclosure widget.

`nestedExpand` is available to avoid infinite nesting, therefore it can **only** be placed within a TableCell or TableHeader, where an Expand can only be placed at the top-level or inside a .

## Example

```json
{
  "type": "nestedExpand",
  "attrs": {
    "title": "Hello world"
  },
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Content

`nestedExpand` can contain an array of one-or-more:

* Paragraph
* Heading
* MediaGroup
* MediaSingle

## Fields

| Name | Required | Type | Value | Notes |
|------|----------|------|-------|-------|
| content | ✓ | Array of one-or-more above mentioned nodes. | | |
| type | ✓ | string | "nestedExpand" | |
| attrs | ✓ | object | | |
| attrs.title | | string | | |

# Node - orderedList

## Purpose

The `orderedList` node is a container for a numbered list of items. It's the ordered equivalent of `bulletList`.

## Type

`orderedList` is a top-level block node.

## Example

```json
{
  "type": "orderedList",
  "attrs": {
    "order": 3
  },
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Hello world"
            }
          ]
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "orderedList" |
| content | ✓ | array | An array of nodes |
| attrs | | object | |
| attrs.order | | integer | A positive integer greater than or equal to 0 |

## Content

`content` can contain one or more `listItem` nodes.

## Attributes

`order` defines the number of the first item in the list. For example, `3` would mean the list starts at number three. When not specified, the list starts from 1.

# Node - panel

## Purpose

The `panel` node is a container that highlights content.

## Type

`panel` is a [top-level block node](/cloud/jira/platform/apis/document/structure#top-level-block-nodes).

## Example

```json
{
  "type": "panel",
  "attrs": {
    "panelType": "info"
  },
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "panel" |
| content | ✓ | array | An array of one or more nodes |
| attrs | ✓ | object | |
| attrs.panelType | ✓ | string | "info", "note", "warning", "success", "error" |

## Content

`content` must contain array of one or more of the following nodes:

* [`bulletList`](/cloud/jira/platform/apis/document/nodes/bulletList)
* [`heading`](/cloud/jira/platform/apis/document/nodes/heading) with no marks.
* [`orderedList`](/cloud/jira/platform/apis/document/nodes/orderedList)
* [`paragraph`](/cloud/jira/platform/apis/document/nodes/paragraph) with no marks.

# Node - paragraph

## Purpose

The `paragraph` node is a container for a block of formatted text delineated by a carriage return.
It's the equivalent of the HTML <p> tag.

## Type

`paragraph` is a [top-level block node](/cloud/jira/platform/apis/document/structure#top-level-block-nodes).

## Example

```json
{
  "type": "paragraph",
  "content": [
    {
      "type": "text",
      "text": "Hello world"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "paragraph" |
| content | | array | Array of zero or more nodes. |
| attrs | | object | |
| attrs.localId | | string | An ID to uniquely identify this node within the document. |

## Content

`content` can take any [inline mode](/cloud/jira/platform/apis/document/structure#inline-nodes).

# Node - rule

## Purpose

The `rule` node represents a divider, it is equivalent to the HTML <hr/> tag.

## Type

`rule` is a [top-level block node](/cloud/jira/platform/apis/document/structure#top-level-block-nodes).

## Example

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    },
    {
      "type": "rule"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "rule" |

# Node - status

## Purpose

The `status` node is a mutable **inline** node that represents the state of work.

## Examples

```json
{
  "type": "status",
  "attrs": {
    "localId": "abcdef12-abcd-abcd-abcd-abcdef123456",
    "text": "In Progress",
    "color": "yellow"
  }
}
```

## Content

`status` is an inline node in the [inlines](/cloud/jira/platform/apis/document/structure#inline-nodes) group.

## Marks

`status` does not support any marks.

## Fields

| Name | Required | Type | Value | Notes |
|------|----------|------|-------|-------|
| type | ✓ | string | "status" | |
| attrs | ✓ | object | | |
| attrs.localId | | string | | unique identifier, auto-generated |
| attrs.text | ✓ | string | | The textual representation of the status |
| attrs.color | ✓ | string | "neutral" \| "purple" \| "blue"\| "red"\| "yellow"\| "green" | neutral is the default and represents the grey color |

# Node - table

## Purpose

The `table` node provides a container for the nodes that define a table.

> **Note**: only supported on **web** and **desktop**. **Mobile** rendering support for tables is not available.

## Type

`table` is a top-level block node.

## Example

```json
{
  "type": "table",
  "attrs": {
    "isNumberColumnEnabled": false,
    "layout": "center", 
    "width": 900,
    "displayMode": "default"
  },
  "content": [
    {
      "type": "tableRow",
      "content": [
        {
          "type": "tableCell",
          "attrs": {},
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": " Row one, cell one"
                }
              ]
            }
          ]
        },
        {
          "type": "tableCell",
          "attrs": {},
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Row one, cell two"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| `type` | ✓ | string | "table" |
| `content` | ✓ | array | Array of one or more nodes |
| `attrs` | | object | |
| `attrs.isNumberColumnEnabled` | | boolean | 'true','false' |
| `attrs.width` | | number | A positive integer |
| `attrs.layout` | | string | 'center', 'align-start' |
| `attrs.displayMode` | | string | 'default', 'fixed' |

## Content

`content` takes an array of one or more `tableRow` nodes.

## Attributes

When `isNumberColumnEnabled` is set to 'true' the first table column provides numbering for the table rows.

`width` sets the length (in pixels) of the table on the page. This value is independent of the table's column width, this allows control of the table's overflow. It supersedes the existing `layout` attribute and will be used instead of it at runtime. If `width` is not provided the editor will convert `layout` to pixels (`default=760`, `wide=960` and `full-width=1800`). Although no minimum and maximum width is enforced it is recommended to follow these guidelines:

Minimum width

* 1 column table = 48px
* 2 column table = 96px 
* 3 column table = 144px
* > 3 column table = 144px

Maximum width

* 1800

`layout` determines the alignment of a table in the full page editor, relevant to the line length. Currently only center and left alignment options are supported.

The layout values are mapped as follows:

* `center` will align the table to the *center* of page, its width can be larger than the line length
* `align-start` will align the table *left* of the line length, its width cannot be larger than the line length

The layout attribute was previously reserved for width options ('default', 'wide' and 'full-width') however this was deprecated when the width attribute was released and should be used instead. The editor continues to convert these values to widths, but if you wish to apply an alignment value please use width and layout for *table alignment*.

> These settings do not apply in Jira where tables are automatically displayed across the full width of the text container.

`displayMode` attribute controls how tables adapt to narrow screens:

* When displayMode is set to 'default' or left unset, the table's columns will automatically scale down to accommodate narrow screens, with a maximum reduction of up to 40%.
* When displayMode is set to 'fixed', the table's columns will maintain their original width, regardless of screen size.

# Node - tableCell

## Purpose

The `tableCell` node defines a cell within a table row.

> Note: only supported on **web** and **desktop**. **Mobile** rendering support for tables is not available.

## Type

`tableCell` is a child block node of the `tableRow` node.

## Example

```json
{
  "type": "tableCell",
  "attrs": {},
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "tableCell" |
| content | ✓ | array | An array of one or more nodes |
| attrs | | object | |
| attrs.background | | string | Short or long hex color code or HTML color name |
| attrs.colspan | | integer | Positive integer, defaults to 1 |
| attrs.colwidth | | array | Array of positive integers |
| attrs.rowspan | | integer | Positive integer, defaults to 1 |

## Content

`content` takes an array of one or more of these nodes:

* `blockquote`
* `bulletList`
* `codeBlock`
* `heading`
* `mediaGroup`
* `nestedExpand`
* `orderedList`
* `panel`
* `paragraph`
* `rule`

## Attributes

* `background` defines the color of the cell background.
* `colspan` defines the number of columns the cell spans.
* `colwidth` defines the width of the column or, where the cell spans columns, the width of the columns it spans in pixels. The length of the array should be equal to the number of spanned columns. 0 is permitted as an *array value* if the column size is not fixed, for example, a cell merged across 3 columns where one unfixed column is surrounded by two fixed might be represented as `[120, 0, 120]`.
* `rowspan` defines the number of rows a cell spans.

# Node - tableHeader

## Purpose

The `tableHeader` node defines a cell within a table heading row.

> Note: only supported on **web** and **desktop**. **Mobile** rendering support for tables is not available.

## Type

`tableHeader` is a child block node of the `tableRow` node.

## Example

```json
{
  "type": "tableHeader",
  "attrs": {},
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Hello world header"
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "tableHeader" |
| content | ✓ | array | An array of one or more nodes |
| attrs | | object | |
| attrs.background | | string | Short or long hex color code or HTML color name |
| attrs.colspan | | integer | Positive integer, defaults to 1 |
| attrs.colwidth | | array | Array of positive integers |
| attrs.rowspan | | integer | Positive integer, defaults to 1 |

## Content

`content` takes an array of one or more of these nodes:

* `blockquote`
* `bulletList`
* `codeBlock`
* `heading`
* `mediaGroup`
* `nestedExpand`
* `orderedList`
* `panel`
* `paragraph`
* `rule`

## Attributes

* `background` defines the color of the cell background.
* `colspan` defines the number of columns the cell spans.
* `colwidth` defines the width of the column or, where the cell spans columns, the width of the columns it spans in pixels. The length of the array should be equal to the number of spanned columns. 0 is permitted as an *array value* if the column size is not fixed, for example, a cell merged across 3 columns where one unfixed column is surrounded by two fixed might be represented as `[120, 0, 120]`.
* `rowspan` defines the number of rows a cell spans.

# Node - tableRow

## Purpose

The `tableRow` node defines rows within a table and is a container for table heading and table cell nodes. 

> Note: only supported on **web** and **desktop**. **Mobile** rendering support for tables is not available.

## Type

`tableRow` is a [child block node](/cloud/jira/platform/apis/document/structure#child-block-nodes) of the [`table`](/cloud/jira/platform/apis/document/nodes/table) node.

## Example

```json
{
  "type": "tableRow",
  "content": [
    {
      "type": "tableHeader",
      "attrs": {},
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Heading one",
              "marks": [
                {
                  "type": "strong"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "tableRow" |
| content | ✓ | array | An array of nodes |

## Content

`content` takes an array of one or more [`tableHeader`](/cloud/jira/platform/apis/document/nodes/table_header) or [`tableCell`](/cloud/jira/platform/apis/document/nodes/table_cell) nodes.

# Node - text

## Purpose

The `text` node holds document text.

## Type

`text` is an [inline node](/cloud/jira/platform/apis/document/structure#inline-node).

## Example

```json
{
  "type": "text",
  "text": "Hello world"
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| `type` | ✓ | string | "text" |
| `text` | ✓ | string | Non-empty text string |
| `marks` |  | array | Array of marks |

## Text

`text` **must not** be empty.

## Marks

The following marks can be applied:

* [`code`](/cloud/jira/platform/apis/document/marks/code)
* [`em`](/cloud/jira/platform/apis/document/marks/em)
* [`link`](/cloud/jira/platform/apis/document/marks/link)
* [`strike`](/cloud/jira/platform/apis/document/marks/strike)
* [`strong`](/cloud/jira/platform/apis/document/marks/strong)
* [`subsup`](/cloud/jira/platform/apis/document/marks/subsup)
* [`textColor`](/cloud/jira/platform/apis/document/marks/textColor)
* [`underline`](/cloud/jira/platform/apis/document/marks/underline)

# Mark - backgroundColor

## Purpose

The `backgroundColor` mark sets background color styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "backgroundColor",
      "attrs": {
        "color": "#fedec8"
      }
    }
  ]
}
```

## Combinations with other marks

The `backgroundColor` **cannot** be combined with the following marks:

* code

## Rendering colors with theme support

Colors are stored in a hexadecimal format - but need to be displayed differently depending on the current product theme, such as light and dark mode. Support for this is provided via a mapping from each hexadecimal color to a design token from the Atlassian Design System.

Currently, such theming is only supported on **web**.

This mapping is provided by the `@atlaskit/editor-palette` package. Documentation for this package is found at https://atlaskit.atlassian.com/packages/editor/editor-palette.

Documentation for Atlassian Design System tokens is found at https://atlassian.design/components/tokens.

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "backgroundColor" |
| attrs | ✓ | object | |
| attrs.color | ✓ | string | A color defined in HTML hexadecimal format, for example #daa520. To display this color with correct contrast in different product themes, such as light and dark mode, use colors defined in the background color palette of `@atlaskit/editor-palette`. |

# Mark - code

## Purpose

The `code` mark sets code styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "code"
    }
  ]
}
```

## Combinations with other marks

`code` can **ONLY** be combined with the following marks:

* `link`

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "code" |

# Mark - em

## Purpose

The `em` mark sets *italic* styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "em"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "em" |

# Mark - link

## Purpose

The `link` mark sets a hyperlink. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "link",
      "attrs": {
        "href": "http://atlassian.com",
        "title": "Atlassian"
      }
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "link" |
| attrs | ✓ | object | |
| attrs.collection | | string | |
| attrs.href | ✓ | string | A URI |
| attrs.id | | string | |
| attrs.occurrenceKey | | string | |
| attrs.title | | string | Title for the URI |

## Attributes

* `collection`
* `href` defines the URL for the hyperlink and is the equivalent of the `href` value for a HTML <a> element.
* `id`
* `occurrenceKey`
* `title` defines the title for the hyperlink and is the equivalent of the `title` value for a HTML <a> element.

# Mark - strike

## Purpose

The `strike` mark sets ~~strike-through~~ styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "strike"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "strike" |

# Mark - strong

## Purpose

The `strong` mark sets **strong** styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "strong"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | â | string | "strong" |

# Mark - subsup

## Purpose

The `subsup` mark sets ^superscript^ or ~subscript~ styling. This mark applies to [`text`](/cloud/jira/platform/apis/document/nodes/text) nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "subsup",
      "attrs": {
        "type": "sub"
      }
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "subsup" |
| attrs | ✓ | object | |
| attrs.type | ✓ | string | "sup" or "sub" |

# Mark - textColor

## Purpose

The `textColor` mark sets *color* styling. This mark applies to `text` nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "textColor",
      "attrs": {
        "color": "#97a0af"
      }
    }
  ]
}
```

## Combinations with other marks

The `textColor` **cannot** be combined with the following marks:

* code
* link

## Rendering colors with theme support

Colors are stored in a hexadecimal format - but need to be displayed differently depending on the current product theme, such as light and dark mode. Support for this is provided via a mapping from each hexadecimal color to a design token from the Atlassian Design System.

Currently, such theming is only supported on **web**.

This mapping is provided by the `@atlaskit/editor-palette` package. Documentation for this package is found at https://atlaskit.atlassian.com/packages/editor/editor-palette.

Documentation for Atlassian Design System tokens is found at https://atlassian.design/components/tokens.

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "textColor" |
| attrs | ✓ | object | |
| attrs.color | ✓ | string | A color defined in HTML hexadecimal format, for example #daa520. To display this color with correct contrast in different product themes, such as light and dark mode, use `@atlaskit/editor-palette` to map this color to a design token from the Atlassian Design System. |

# Mark - underline

## Purpose

The `underline` mark sets **underline** styling. This mark applies to [`text`](/cloud/jira/platform/apis/document/nodes/text) nodes.

## Example

```json
{
  "type": "text",
  "text": "Hello world",
  "marks": [
    {
      "type": "underline"
    }
  ]
}
```

## Fields

| Name | Required | Type | Value |
|------|----------|------|-------|
| type | ✓ | string | "underline" |
