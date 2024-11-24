import argparse
import yaml
from url_tools.arxiv_fetcher import ArxivFetcher
from bytedance_ai_tools.bytedance_classifier import BytedanceClassifier
from bytedance_ai_tools.bytedance_translator import BytedanceTranslator
import pdb
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
import time
from url_tools.arxiv_latest import ArxivWebScraper

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def parse_args():
    parser = argparse.ArgumentParser(description='ArXiv Paper Fetcher and Classifier')
    parser.add_argument('--config', type=str, default='config.yaml',
                      help='Path to configuration file (default: config.yaml)')
    return parser.parse_args()

def process_paper(paper: dict, translator: BytedanceTranslator, classifier: BytedanceClassifier) -> tuple:
    """
    处理单篇论文：翻译和分类
    
    Args:
        paper: 论文信息字典
        translator: 翻译器实例
        classifier: 分类器实例
    
    Returns:
        tuple: (translated_paper, categories_list)
    """
    try:
        # If AI translation is enabled, translate; otherwise use original content
        if translator.ai_client.use_ai:
            translated_paper = {
                'title': translator.translate(paper['title']),
                'abstract': translator.translate(paper['abstract']),
                'url': paper['url']
            }
        else:
            translated_paper = {
                'title': paper['title'],
                'abstract': paper['abstract'],
                'url': paper['url']
            }
        
        # 分类论文
        # categories_list = classifier.classify_paper(paper['title'], paper['abstract'])
        categories_list = ["others"]
        return translated_paper, categories_list
    except Exception as e:
        print(f"Error processing paper {paper['title']}: {e}")
        return None, None

def main():
    start_time = time.time()
    args = parse_args()
    config = load_config(args.config)
    
    # 初始化论文获取器
    scraper = ArxivWebScraper()
    print(f"Fetching papers... Time elapsed: {time.time() - start_time:.2f}s")
    
    # 从配置中获取要查询的分类
    categories_to_fetch = config['arxiv']['categories']
    papers = []
    
    # 获取每个分类的论文
    for category in categories_to_fetch:
        category_papers = scraper.get_latest_papers(
            category=category,
            max_results=config['arxiv']['max_papers']
        )
        papers.extend(category_papers)
        print(f"Fetched {len(category_papers)} papers from {category}")
    
    print(f"Found {len(papers)} papers in total. Time elapsed: {time.time() - start_time:.2f}s")
    
    # 转换论文格式以适配后续处理
    formatted_papers = [{
        'title': paper['title'],
        'abstract': paper.get('abstract', ''),
        'url': paper['arxiv_url']
    } for paper in papers]

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
    
    print(f"Processing papers with translation and classification...")
    try:
        # 使用线程池并发处理论文
        with ThreadPoolExecutor(max_workers=16) as executor:
            results = list(executor.map(lambda paper: process_paper(paper, translator, classifier), formatted_papers))
        
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
    markdown_output.append(f"Date range: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}\n")
    
    for category, papers in categories.items():
        markdown_output.append(f"\n## {category}")
        for paper in papers:
            markdown_output.append(f"- [{paper['title']}]({paper['url']})")
            # Split abstract into lines and format each line with quote prefix
            abstract_lines = paper['abstract'].split('\n')
            for line in abstract_lines:
                if len(line) > 200:  # Handle long lines by wrapping at 200 chars
                    words = line.split()
                    current_line = []
                    current_length = 0
                    for word in words:
                        if current_length + len(word) + 1 <= 200:
                            current_line.append(word)
                            current_length += len(word) + 1
                        else:
                            markdown_output.append(f"  > {''.join(current_line)}")
                            current_line = [word]
                            current_length = len(word)
                    if current_line:
                        markdown_output.append(f"  > {''.join(current_line)}")
                else:
                    markdown_output.append(f"  > {line}")
            markdown_output.append("")  # Add blank line after abstract
    
    markdown = "\n".join(markdown_output)

    print(f"Writing output file... Time elapsed: {time.time() - start_time:.2f}s")
    with open(config['output']['file_path'], "w", encoding="utf-8") as file:
        file.write(markdown)
    print(f"All done! Total time elapsed: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
   