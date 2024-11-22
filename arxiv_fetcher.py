import arxiv
from datetime import datetime, timedelta, timezone

class ArxivFetcher:
    def __init__(self):
        self.client = arxiv.Client()

    def get_recent_papers(self, days=7):
        # 计算日期范围 - 使用 UTC 时区
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        # 构建查询 - 添加 cs.CL 类别过滤
        search = arxiv.Search(
            query="cat:cs.CL",  # 添加 cs.CL 类别过滤
            max_results=10, # debug 
            sort_by=arxiv.SortCriterion.SubmittedDate
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