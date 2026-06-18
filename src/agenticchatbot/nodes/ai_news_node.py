import os
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINode:
    def __init__(self,llm):
        self.llm = llm
        self.tavily = TavilyClient()

    def fecth_news(self, state:dict) -> dict:
        frequency = state['messages'][0].content.lower()
        time_range_map = {'daily':'d', 'weekly':'w', 'monthly':'m', 'yearly':'y'}
        days_count_map = {'daily':1, 'weekly':7, 'monthly':30, 'yearly':366}

        response = self.tavily.search(
            query="Top Artificial Intelligence news across India, globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer='advanced',
            max_results=15,
            days=days_count_map[frequency]
        )

        return {"frequency": frequency, "news_data": response.get('results', [])}

    def summarize_news(self, state:dict) -> dict:
        news_data = state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
                ("system", """Summarize AI news articles into markdown format. For each item include:
                - Date in **YYYY-MM-DD** format in IST timezone
                - Concise sentences summary from latest news
                - Sort news by date wise (latest first)
                - Source URL as link
                Use format:
                ### [Date]
                - [Summary](URL)"""),
                ("user", "Articles:\n{articles}")
        ])
        articles_str = "\n\n".join([
        f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
        for item in news_data
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        return {"summary": response.content}

    def save_result(self, state):
        frequency = state['frequency']
        summary = state['summary']
        os.makedirs("./AINews", exist_ok=True)
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary \n\n")
            f.write(summary)
        return {"filename": filename}
    


