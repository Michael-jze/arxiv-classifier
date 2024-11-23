import argparse
import yaml
from url_tools.arxiv_fetcher import ArxivFetcher
from bytedance_ai_tools.bytedance_classifier import BytedanceClassifier
from bytedance_ai_tools.bytedance_translator import BytedanceTranslator
import pdb
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
import time

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def parse_args():
    parser = argparse.ArgumentParser(description='ArXiv Paper Fetcher and Classifier')
    parser.add_argument('--config', type=str, default='config.yaml',
                      help='Path to configuration file (default: config.yaml)')
    return parser.parse_args()

def main():
    start_time = time.time()
    args = parse_args()
    config = load_config(args.config)
    
    # 获取论文
    fetcher = ArxivFetcher(
        max_results=config['arxiv']['max_papers'],
        search_query=config['arxiv']['search_query'],
        sort_by=config['arxiv']['sort_by']
    )
    print(f"Fetching papers... Time elapsed: {time.time() - start_time:.2f}s")
    papers = fetcher.get_recent_papers(days=config['arxiv']['days'])
    print(f"Found {len(papers)} papers. Time elapsed: {time.time() - start_time:.2f}s")
    
    # 初始化翻译器和分类器
    translator = BytedanceTranslator(
        use_ai=config['api']['use_ai'],
        base_url=config['api']['base_url'],
        model_id=config['api']['model_id']
    )
    
    classifier = BytedanceClassifier(
        use_ai=config['api']['use_ai'],
        base_url=config['api']['base_url'],
        model_id=config['api']['model_id'],
        classify_types=config['categories']
    )
    categories = {}
    
    def process_paper(paper):
        try:
            # 翻译标题和摘要
            translated_paper = {
                'title': translator.translate(paper['title']),
                'abstract': translator.translate(paper['abstract']),
                'url': paper['url']
            }
            
            categories_list = classifier.classify_paper(paper['title'], paper['abstract'])
            return translated_paper, categories_list
        except Exception as e:
            print(f"Error processing paper {paper['title']}: {e}")
            return None, None

    print(f"Processing papers with translation and classification...")
    try:
        # 使用线程池并发处理论文
        with ThreadPoolExecutor(max_workers=16) as executor:
            results = list(executor.map(process_paper, papers))
        
        print(f"Processing completed. Time elapsed: {time.time() - start_time:.2f}s")
        # 处理结果
        for translated_paper, categories_list in results:
            if translated_paper and categories_list:
                for category in categories_list:
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(translated_paper)
    except Exception as e:
        print(f"Error during processing: {e}")
        exit(1)
        
    # Build markdown string instead of printing
    markdown_output = []
    
    # Add title with search range and time info
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=config['arxiv']['days'])
    markdown_output.append(f"# ArXiv Papers")
    markdown_output.append(f"Search query: `{config['arxiv']['search_query']}`")
    markdown_output.append(f"Date range: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}\n")
    
    for category, papers in categories.items():
        markdown_output.append(f"\n## {category}")
        for paper in papers:
            markdown_output.append(f"- [{paper['title']}]({paper['url']})")
            markdown_output.append(f"  > {paper['abstract']}\n")
    
    markdown = "\n".join(markdown_output)

    print(f"Writing output file... Time elapsed: {time.time() - start_time:.2f}s")
    with open(config['output']['file_path'], "w", encoding="utf-8") as file:
        file.write(markdown)
    print(f"All done! Total time elapsed: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
   