from wallaroo.explainability import *


def test_truncate():
    v = ["fooobar"]
    s = truncate(v, num_char=50)
    assert len(s) == len(str(v))

    v = v * 100
    s = truncate(v, num_char=50)
    assert len(s) == 50


def test_explainabilty_config():
    exc = ExplainabilityConfig(None, 1, None, "", None)
    assert exc

    html = exc._repr_html_()
    assert html.startswith("<table>")
    assert html.endswith("</table>")


def test_explainabilty_config_list():
    excl = ExplainabilityConfigList([ExplainabilityConfig(None, 1, None, "", None)])

    html = excl._repr_html_()
    assert html.startswith("<table>")
    assert html.endswith("</table>")


def test_explainabilty_request():
    exc = ExplainabilityRequest(None, 1, True, False, None, None, None, None)
    assert exc

    html = exc._repr_html_()
    assert html.startswith("<table>")
    assert html.endswith("</table>")


def test_explainabilty_request_list():
    exrl = ExplainabilityRequestList(
        [ExplainabilityRequest(None, 1, True, False, None, None, None, None)]
    )

    html = exrl._repr_html_()
    assert html.startswith("<table>")
    assert html.endswith("</table>")
