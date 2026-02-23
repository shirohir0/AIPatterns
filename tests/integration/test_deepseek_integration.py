import os
import pytest

from agentic_lc import get_llm
from agentic_lc.patterns import prompt_chaining


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("DEEPSEEK_API_KEY"), reason="DEEPSEEK_API_KEY is not set")
def test_prompt_chaining_real_api():
    llm = get_llm()
    result = prompt_chaining(llm, "Скажи одно предложение про агентов")
    assert "draft" in result and "refined" in result
    assert len(result["refined"]) > 0
