from agentic_lc.patterns.routing import route_query


def test_route_query_math():
    llm = lambda _input: "math"
    route, response = route_query(llm, "2+2")
    assert route == "math"
    assert "Результат" in response
