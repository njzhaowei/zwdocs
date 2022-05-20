def test_func(arg1, arg2=None):
    """desc
    `Sphinx reStructuretext docs <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html>`_

    :param str arg1: AAA
    :param arg2: BBB
    :type arg2: dict{str, int}
    :return: None
    :rtype: None or str
    :raise ValueError: raises ValueError exception.

    .. code-block:: Python

        test_docs(111, 222)
    """