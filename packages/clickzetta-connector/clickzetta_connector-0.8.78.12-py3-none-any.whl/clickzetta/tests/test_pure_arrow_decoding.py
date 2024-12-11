import pytest


@pytest.mark.skip("clickzetta-connector does not support set pure arrow decoding")
def test_pure_arrow_decoding(it_conn):
    it_conn._set_pure_arrow_decoding(True)
    cursor = it_conn.cursor()
    cursor.execute("select * from values (cast(1 as int), cast(NULL as int)) t(a, b)")
    result = cursor.fetchall()
    assert result == [(1, None)]


@pytest.mark.skip("clickzetta-connector does not support set pure arrow decoding")
def test_pure_arrow_decoding_negative(it_conn):
    # DeprecationWarning: Passing a BlockManager to DataFrame is deprecated and will raise in a future version. Use public APIs instead.
    it_conn._set_pure_arrow_decoding(False)
    cursor = it_conn.cursor()
    cursor.execute("select * from values (cast(1 as int))")
    result = cursor.fetchall()
    assert result[0][0] == 1
