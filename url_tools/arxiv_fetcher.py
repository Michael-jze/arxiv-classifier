import arxiv
from datetime import datetime, timedelta, timezone
from arxiv import SortCriterion, SortOrder

class ArxivFetcher:
    def __init__(self, max_results=100, search_query="", sort_by="lastUpdatedDate"):
        # Remove sort handling from client initialization
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,
            num_retries=3
        )
        
        # Convert string to proper SortCriterion enum
        if sort_by in ["lastUpdatedDate", "last"]:
            self.sort_by = arxiv.SortCriterion.LastUpdatedDate
        elif sort_by in ["submittedDate", "submitted"]:
            self.sort_by = arxiv.SortCriterion.SubmittedDate
        elif sort_by in ["relevance", "relevant"]:
            self.sort_by = arxiv.SortCriterion.Relevance
        else:
            self.sort_by = arxiv.SortCriterion.LastUpdatedDate  # default fallback
            
        self.max_results = max_results
        self.search_query = search_query
        assert self.search_query != "", "search_query must be a non-empty string"

    def get_recent_papers(self, days=7):
        # 计算日期范围 - 使用 UTC 时区
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # 构建查询 - 使用实例变量
        search = arxiv.Search(
            query=self.search_query,  # 使用传入的搜索查询
            max_results=self.max_results,
            sort_by=self.sort_by  # 使用传入的排序方式
        )

        papers = []
        for result in self.client.results(search):
            published_date = result.published.replace(tzinfo=timezone.utc)  # 确保发布时间使用 UTC
            if published_date < start_date:  # 如果发布日期早于开始日期，直接跳出循环
                break
            if published_date <= end_date:  # 如果在时间范围内，添加到结果中
                paper = {
                    'title': result.title,
                    'abstract': result.summary,
                    'authors': [author.name for author in result.authors],
                    'published': published_date,  # 存储 UTC 时间
                    'url': result.entry_id
                }
                papers.append(paper)
                
        return papers 