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

class Case:
    pass