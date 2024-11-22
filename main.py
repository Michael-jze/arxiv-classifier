from url_tools.arxiv_fetcher import ArxivFetcher
from bytedance_ai_tools.bytedance_classifier import BytedanceClassifier
from bytedance_ai_tools.bytedance_translator import BytedanceTranslator

def main():
    # 获取论文
    fetcher = ArxivFetcher()
    papers = fetcher.get_recent_papers()
    
    # 初始化翻译器和分类器
    translator = BytedanceTranslator(
        use_ai=True,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model_id="ep-20241122223516-96dll"
    )
    
    # 分类论文
    classifier = BytedanceClassifier(
        use_ai=True,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model_id="ep-20241122223516-96dll",
        classify_types=["model architecture", 
                        "multimodal fusion", 
                        "modality encoders",    
                        "pre-training strategies",
                        "model compression",
                        "distributed training",
                        "evaluation metrics",
                        "correctness verification",
                        "adversarial attacks",
                        "audio features",
                        "audio-text alignment",
                        "audio generation",
                        "cross-domain applications",
                        "transfer learning",
                        "zero-shot and few-shot learning"]
    )
    categories = {}
    
    try:
        for paper in papers:
            # 翻译标题和摘要
            translated_paper = {
                'title': translator.translate(paper['title']),
                'abstract': translator.translate(paper['abstract']),
                'url': paper['url']  # URL保持不变
            }
            
            categories_list = classifier.classify_paper(paper['title'], paper['abstract'])
            for category in categories_list:
                if category not in categories:
                    categories[category] = []
                categories[category].append(translated_paper)
    except Exception as e:
        print(f"Error during processing: {e}")
        return ""
        
    # Build markdown string instead of printing
    markdown_output = []
    for category, papers in categories.items():
        markdown_output.append(f"\n## {category}")
        for paper in papers:
            markdown_output.append(f"- [{paper['title']}]({paper['url']})")
            markdown_output.append(f"  > {paper['abstract']}\n")
    
    return "\n".join(markdown_output)

if __name__ == "__main__":
    markdown = main()
    print(markdown)
    with open("output.md", "w", encoding="utf-8") as file:
        file.write(markdown)