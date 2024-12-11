# -*- coding: utf-8 -*-

import mercurial_update_version as muv


def assert_equal(left, right):
    """Replacement for old nose function."""
    assert left == right


def _ver(*nums):
    return list(str(n) for n in nums)


def test_dotted():
    fmt = muv.TagFmtDotted()

    assert_equal(_ver(1, 0), fmt.extract_no("1.0"))
    assert_equal(_ver(1, 3), fmt.extract_no("1.3"))
    assert_equal(_ver(1, 3, 11), fmt.extract_no("1.3.11"))
    assert_equal(_ver(1, 3, 11, 8), fmt.extract_no("1.3.11.8"))
    assert_equal(_ver(1, 3, 11, 8, 15), fmt.extract_no("1.3.11.8.15"))

    assert_equal(_ver(1, 0, 3), fmt.extract_no("1.0.3"))
    assert_equal(_ver(0, 3, 11), fmt.extract_no("0.3.11"))
    assert_equal(_ver(1, 0, 0, 997), fmt.extract_no("1.0.0.997"))
    assert_equal(_ver(1, '00', '00', '0000', 15), fmt.extract_no("1.00.00.0000.15"))

    assert_equal(_ver(77777777, 88888888, 99999999, 11111111, 3333333), fmt.extract_no("77777777.88888888.99999999.11111111.3333333"))


def test_dotted_buggy():
    fmt = muv.TagFmtDotted()

    assert_equal(None, fmt.extract_no("iks"))
    assert_equal(None, fmt.extract_no("1,3"))
    assert_equal(None, fmt.extract_no("11-3"))
    assert_equal(None, fmt.extract_no("11"))
    assert_equal(None, fmt.extract_no(".1.11"))
    assert_equal(None, fmt.extract_no("11.a.3"))
    assert_equal(None, fmt.extract_no("11..3.0"))
    assert_equal(None, fmt.extract_no("ix_11.3.0"))
    assert_equal(None, fmt.extract_no("11.3.0b"))


def test_dashed():
    fmt = muv.TagFmtDashed()

    assert_equal(_ver(1, 0), fmt.extract_no("1-0"))
    assert_equal(_ver(1, 3), fmt.extract_no("1-3"))
    assert_equal(_ver(1, 3, 11), fmt.extract_no("1-3-11"))
    assert_equal(_ver(1, 3, 11, 8), fmt.extract_no("1-3-11-8"))
    assert_equal(_ver(1, 3, 11, 8, 15), fmt.extract_no("1-3-11-8-15"))

    assert_equal(_ver(1, 0, 3), fmt.extract_no("1-0-3"))
    assert_equal(_ver(0, 3, 11), fmt.extract_no("0-3-11"))
    assert_equal(_ver(1, 0, 0, 997), fmt.extract_no("1-0-0-997"))
    assert_equal(_ver(1, '00', '00', '0000', 15), fmt.extract_no("1-00-00-0000-15"))

    assert_equal(_ver(77777777, 88888888, 99999999, 11111111, 3333333), fmt.extract_no("77777777-88888888-99999999-11111111-3333333"))


def test_dashed_buggy():
    fmt = muv.TagFmtDashed()

    assert_equal(None, fmt.extract_no("iks"))
    assert_equal(None, fmt.extract_no("1,3"))
    assert_equal(None, fmt.extract_no("1.3.0"))
    assert_equal(None, fmt.extract_no("11.3"))
    assert_equal(None, fmt.extract_no("11-a-3"))
    assert_equal(None, fmt.extract_no("11--3-0"))
    assert_equal(None, fmt.extract_no("ix_11-3-0"))
    assert_equal(None, fmt.extract_no("11-3-0b"))


def test_pfx_dotted():
    fmt = muv.TagFmtPfxDotted()

    assert_equal(_ver(1, 0), fmt.extract_no("blah-1.0"))
    assert_equal(_ver(1, 3), fmt.extract_no("furr_1.3"))
    assert_equal(_ver(1, 3, 11), fmt.extract_no("bibi_1.3.11"))
    assert_equal(_ver(1, 3, 11, 8), fmt.extract_no("la1nd-a-1.3.11.8"))
    assert_equal(_ver(1, 3, 11, 8, 15), fmt.extract_no("IKZES_1.3.11.8.15"))

    assert_equal(_ver(1, 0, 3), fmt.extract_no("reand___1.0.3"))
    assert_equal(_ver(0, 3, 11), fmt.extract_no("raba--0.3.11"))
    assert_equal(_ver(1, 0, 0, 997), fmt.extract_no("furk-1.0.0.997"))
    assert_equal(_ver(1, 0, 0, 997), fmt.extract_no("furk20-1.0.0.997"))
    assert_equal(_ver(1, '00', '00', '0000', 15), fmt.extract_no("synk_1.00.00.0000.15"))

    assert_equal(_ver(77777777, 88888888, 99999999, 11111111, 3333333), fmt.extract_no("hiddd-77777777.88888888.99999999.11111111.3333333"))


def test_pfx_dotted_buggy():
    fmt = muv.TagFmtPfxDotted()

    assert_equal(None, fmt.extract_no("iks"))
    assert_equal(None, fmt.extract_no("iks-1,3"))
    assert_equal(None, fmt.extract_no("1.3"))
    assert_equal(None, fmt.extract_no(".1.3"))
    assert_equal(None, fmt.extract_no("iks-1-3"))
    assert_equal(None, fmt.extract_no("iks_11-3"))
    assert_equal(None, fmt.extract_no("isssam-11.a.3"))
    assert_equal(None, fmt.extract_no("treol-11..3.0"))
    assert_equal(None, fmt.extract_no("ix_11.3.0bed"))
    assert_equal(None, fmt.extract_no("11..0b"))


def test_pfx_dashed():
    fmt = muv.TagFmtPfxDashed()

    assert_equal(_ver(1, 0), fmt.extract_no("lead_1-0"))
    assert_equal(_ver(1, 3), fmt.extract_no("lead-1-3"))
    assert_equal(_ver(1, 3, 11), fmt.extract_no("lead__1-3-11"))
    assert_equal(_ver(1, 3, 11, 8), fmt.extract_no("lea1-dder_1-3-11-8"))
    assert_equal(_ver(1, 3, 11, 8, 15), fmt.extract_no("lippen-1-3-11-8-15"))

    assert_equal(_ver(1, 0, 3), fmt.extract_no("cos___1-0-3"))
    assert_equal(_ver(0, 3, 11), fmt.extract_no("COS-0-3-11"))
    assert_equal(_ver(1, 0, 0, 997), fmt.extract_no("GDZIE_KOL_WIEK_1-0-0-997"))
    assert_equal(_ver(1, '00', '00', '0000', 15), fmt.extract_no("tit-1-00-00-0000-15"))

    assert_equal(_ver(77777777, 88888888, 99999999, 11111111, 3333333), fmt.extract_no("ahh_77777777-88888888-99999999-11111111-3333333"))

    assert_equal(_ver(1, 0, 3), fmt.extract_no("blah20_1-0-3"))
    assert_equal(_ver(3, 0), fmt.extract_no("pfx_11--3-0"))


def test_pfx_dashed_buggy():
    fmt = muv.TagFmtPfxDashed()

    assert_equal(None, fmt.extract_no("iks"))
    assert_equal(None, fmt.extract_no("1,3"))
    assert_equal(None, fmt.extract_no("1-3-0"))
    assert_equal(None, fmt.extract_no("11-3"))
    assert_equal(None, fmt.extract_no("pfx-11-a-3"))
    assert_equal(None, fmt.extract_no("11-3-0"))
    assert_equal(None, fmt.extract_no("ix-11-3-0b"))
