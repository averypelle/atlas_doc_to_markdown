为了方便我们利用 AI 协助开发, 我们需要将 `Atlassian Document Format 的官方文档 <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ 抓取下来喂给 AI 的知识库. 但是这个原文档有很多个页面, 需要一个个手动下载下来, 万一以后官方有更新, 重新手动下载也很麻烦. 而且下载下来的是 HTML 格式, 放在 AI 知识库里会以 HTML 的形式保存, 太占空间, 而如果我们去掉所有 HTMl 标签, 那么文档的结构就丢失了. 为了解决这一问题, 我们这个目录下的一些脚本可以帮助我们将官方文档提取为一个单个 Markdown 文件.

**Step 1**

运行 `step1_crawl_document.py <https://github.com/MacHu-GWU/atlas_doc_parser-project/blob/dev/scripts/crawl_document/crawl_document.py>`_, 把所有文档的 HTML 页面下载下来, 保存到 tmp 目录下.

**Step 2**

Use AI to convert HTML document to Markdown for reduced size. 每次粘贴这个 Prompt 并上传 tmp 目录下的一个 HTML 文件, AI 会帮你转换成 Markdown 文件. 然后把结果拷贝到 `Atlassian-Document-Format-Reference.md <https://github.com/MacHu-GWU/atlas_doc_parser-project/blob/dev/scripts/crawl_document/Atlassian-Document-Format-Reference.md>`_ 文件中.

.. dropdown:: Prompt

    I have documents extracted from the [Atlassian Document Format official documentation](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/). The content still contains excessive HTML formatting, including styles and scripts that are unnecessary for my needs. I aim to convert this HTML to a clean Markdown format. The conversion should include:

    - Converting bullet points in HTML to Markdown bullets.
    - Transforming HTML code blocks into Markdown code blocks.
    - Converting HTML tables to Markdown tables.

    Please strip out any inline CSS, JavaScript, or non-essential style-related tags during the conversion. Process the content accurately while retaining the structural integrity of the original information in Markdown format.

    I will provide them one by one. Here's the first one, please help me convert it. Please generate the Markdown using Claude Artifacts, Just include the artifact in your response, no need to explain how you did it for me.
