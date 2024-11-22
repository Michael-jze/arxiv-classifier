from arxiv_fetcher import ArxivFetcher
from bytedance_classifier import BytedanceClassifier
from collections import Counter

def main():
    # 获取论文
    fetcher = ArxivFetcher()
    papers = fetcher.get_recent_papers()
    
    # 分类论文
    classifier = BytedanceClassifier(
        use_ai=True,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model_id="ep-20241122223516-96dll"
    )
    categories = {}
    
    for paper in papers:
        categories_list = classifier.classify_paper(paper['title'], paper['abstract'])
        for category in categories_list:
            if category not in categories:
                categories[category] = []
        categories[category].append(paper["title"])
    print(categories)

if __name__ == "__main__":
    main() 