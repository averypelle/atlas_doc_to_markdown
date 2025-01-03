Atlassian Document Format Parser (ADF Parser)
==============================================================================


What is Atlassian Document Format (ADF)?
------------------------------------------------------------------------------
`Atlassian Document Format <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ is the rich text storage format used across Atlassian products:

- Confluence page content
- Jira issue descriptions and comments
- Jira custom field content (rich text fields)

ADF represents formatted content as a structured JSON document with a specific schema defined by Atlassian. This library makes it easy to work with ADF content programmatically.


Features
------------------------------------------------------------------------------
- Complete implementation of the ADF specification
- Parse ADF JSON from Confluence pages and Jira fields into Python objects
- Convert ADF content to multiple formats:
    - Back to ADF JSON
    - Markdown
    - reStructuredText
    - HTML
- Support for all ADF node types:
    - Block nodes (paragraph, heading, codeBlock, etc.)
    - Inline nodes (text, mention, emoji, etc.)
    - Marks (strong, em, link, etc.)
- Programmatically create and modify ADF content
- Type hints for better development experience


Common Use Cases
------------------------------------------------------------------------------
- Extract and process content from Confluence pages
- Parse and analyze Jira issue descriptions and comments
- Convert Confluence/Jira content to other documentation formats
- Create formatted content for Confluence pages or Jira issues
- Build automation tools for Confluence and Jira content
- Migrate content between different documentation systems
