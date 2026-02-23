from agentic_lc.patterns.tool_use import tool_use_agent


class DummyResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class DummyModel:  # pylint: disable=too-few-public-methods
    def __init__(self, responses):
        self._responses = list(responses)

    def invoke(self, _messages):
        return self._responses.pop(0)


class DummyLLM:  # pylint: disable=too-few-public-methods
    def bind_tools(self, _tools):
        # Подделываем выбор инструмента calc.
        tool_call = {
            "id": "1",
            "name": "calc",
            "args": {"expression": "2+2"},
        }

        return DummyModel(
            [
                DummyResponse("", tool_calls=[tool_call]),
                DummyResponse("Итог: 4"),
            ]
        )


def test_tool_use_agent_calc():
    llm = DummyLLM()
    result = tool_use_agent(llm, "Сколько будет 2+2?")
    assert "4" in result
