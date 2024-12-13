from ageqrp import QueryResultParser

# pytest -v tests/test_query_result_parser.py


def test_non_tuples_tuple():
    for value in [None, 1, 3.14, "hello", [], {}]:
        qrp = QueryResultParser()
        result = qrp.parse(value)
        assert result == None


def test_parse_count_tuple():
    qrp = QueryResultParser()
    result = qrp.parse((10761,))
    assert result == 10761


def test_parse_two_numeric_tuple():
    qrp = QueryResultParser()
    result = qrp.parse(
        (
            0,
            1,
            1,
            2,
            3,
            5,
            8,
            13,
            21,
            34,
        )
    )
    assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_parse_two_str_tuple():
    qrp = QueryResultParser()
    result = qrp.parse(
        (
            "Azure Cosmos DB",
            "Azure PostgreSQL",
        )
    )
    assert result == ["Azure Cosmos DB", "Azure PostgreSQL"]


def test_parse_mixed_tuple():
    qrp = QueryResultParser()
    loc = {"lat": 35.50988920032978, "lon": -80.83487017080188}
    result = qrp.parse((28036, "Davidson", "NC", loc))
    assert result == [28036, "Davidson", "NC", loc]


def test_parse_simple_str_one_tuple():
    qrp = QueryResultParser()
    result = qrp.parse(("Azure PostgreSQL",))
    assert result == "Azure PostgreSQL"


def test_parse_single_result_vertex():
    qrp = QueryResultParser()
    arg = (
        '{"id": 844424930131969, "label": "Developer", "properties": {"name": "info@2captcha.com"}}::vertex',
    )
    result = qrp.parse(arg)
    print("test result: {}".format(result))
    assert result["id"] == 844424930131969
    assert result["label"] == "Developer"
    assert result["properties"]["name"] == "info@2captcha.com"


def test_legal_case_vertex():
    qrp = QueryResultParser()
    arg = (
        '{"id": 844424930133136, "label": "Case", "properties": {"id": 594079, "url": "https://static.case.law/wash/79/cases/0643-01.json", "name": "Martindale Clothing Co. v. Spokane &amp; Eastern Trust Co.", "court": "Washington Supreme Court", "court_id": 9029, "decision_year": 1914, "citation_count": 5}}::vertex',
    )
    expected_url = "https://static.case.law/wash/79/cases/0643-01.json"
    expected_name = "Martindale Clothing Co. v. Spokane &amp; Eastern Trust Co."
    result = qrp.parse(arg)
    print("test result: {}".format(result))
    assert result["id"] == 844424930133136
    assert result["label"] == "Case"
    assert result["properties"]["id"] == 594079
    assert result["properties"]["url"] == expected_url
    assert result["properties"]["name"] == expected_name
    assert result["properties"]["decision_year"] == 1914


def test_legal_case_edge():
    qrp = QueryResultParser()
    arg = (
        '{"id": 1407374883553314, "label": "cites", "end_id": 844424930131969, "start_id": 844424930131976, "properties": {"case_id": "1005793", "case_name": "Traverso v. Pupo", "cited_case_id": "1002109", "cited_case_name": "Cline v. Department of Labor &amp; Industries", "cited_case_year": 1957}}::edge',
    )

    expected_name = "Traverso v. Pupo"
    result = qrp.parse(arg)
    print("test result: {}".format(result))
    assert result["id"] == 1407374883553314
    assert result["label"] == "cites"
    assert result["start_id"] == 844424930131976
    assert result["end_id"] == 844424930131969
    assert result["properties"]["case_id"] == "1005793"
    assert result["properties"]["case_name"] == expected_name
    assert result["properties"]["cited_case_year"] == 1957
