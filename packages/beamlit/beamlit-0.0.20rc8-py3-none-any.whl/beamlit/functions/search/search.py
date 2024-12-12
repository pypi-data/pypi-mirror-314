from langchain_community.tools.tavily_search.tool import TavilySearchResults

from beamlit.common.secrets import Secret


def search(query: str):
    """
    A search engine optimized for comprehensive, accurate, and trusted results.
    Useful for when you need to answer questions about current events.
    Input should be a search query.
    """
    api_key = Secret.get("TAVILY_API_KEY")
    tavily = TavilySearchResults(api_key=api_key, max_results=2)
    result = tavily.invoke(input=query)
    return result
