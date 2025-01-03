# -*- coding: utf-8 -*-

from atlas_doc_parser import api


def test():
    _ = api


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.api", preview=False)
