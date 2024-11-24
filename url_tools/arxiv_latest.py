import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import re

class ArxivWebScraper:
    def __init__(self):
        self.base_url = "https://arxiv.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_latest_papers(self, category: str, max_results: int = None) -> List[Dict]:
        """
        从arXiv网页直接获取最新论文
        
        Args:
            category: arXiv分类代码，如 'cs.AI', 'cs.CL'等
            max_results: 最大返回结果数量
        
        Returns:
            包含论文信息的字典列表
        """
        # 构建URL
        url = f"{self.base_url}/list/{category}/recent?skip=0&show=2000"
        
        try:
            # 获取网页内容
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 找到论文列表区域
            dlpage = soup.find('div', {'id': 'dlpage'})
            if not dlpage:
                print("Cannot find paper list section")
                return []
            
            papers = []
            # 查找所有论文条目
            for dt, dd in zip(dlpage.find_all('dt'), dlpage.find_all('dd')):
                if max_results and len(papers) >= max_results:
                    break
                    
                try:
                    # 获取论文ID和链接
                    paper_link = dt.find('a', {'title': 'Abstract'})
                    if not paper_link:
                        continue
                    paper_id = paper_link.text.strip().replace('arXiv:', '')
                    
                    # 获取PDF链接
                    pdf_link = dt.find('a', {'title': 'Download PDF'})
                    pdf_url = f"{self.base_url}{pdf_link['href']}" if pdf_link else None
                    
                    # 解析论文元数据
                    meta = dd.find('div', {'class': 'meta'})
                    if not meta:
                        continue
                    
                    # 获取标题
                    title_div = meta.find('div', {'class': 'list-title'})
                    title = title_div.text.replace('Title:', '').strip() if title_div else 'N/A'
                    
                    # 获取作者列表
                    authors_div = meta.find('div', {'class': 'list-authors'})
                    author_list = []
                    if authors_div:
                        author_links = authors_div.find_all('a')
                        author_list = [a.text.strip() for a in author_links]
                    
                    # 获取摘要
                    abstract = dd.find('p', {'class': 'mathjax'})
                    abstract = abstract.text.strip() if abstract else 'N/A'
                    
                    # 获取主题分类
                    subjects_div = meta.find('div', {'class': 'list-subjects'})
                    if subjects_div:
                        primary_subject = subjects_div.find('span', {'class': 'primary-subject'})
                        primary_subject = primary_subject.text.strip() if primary_subject else 'N/A'
                        # 获取所有主题（包括交叉列表）
                        subjects = subjects_div.text.replace('Subjects:', '').strip()
                    else:
                        primary_subject = 'N/A'
                        subjects = 'N/A'
                    
                    papers.append({
                        'id': paper_id,
                        'title': title,
                        'authors': author_list,
                        'abstract': abstract,
                        'primary_subject': primary_subject,
                        'subjects': subjects,
                        'pdf_url': pdf_url,
                        'arxiv_url': f"{self.base_url}/abs/{paper_id}",
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                    
                except Exception as e:
                    print(f"Error parsing paper: {e}")
                    continue
            
            return papers
            
        except requests.RequestException as e:
            print(f"Error fetching papers: {e}")
            return []

# 使用示例
if __name__ == "__main__":
    scraper = ArxivWebScraper()
    
    # 获取AI领域最新的5篇论文
    papers = scraper.get_latest_papers('cs.AI', max_results=5)
    # 打印结果
    for paper in papers:
        print(f"\nTitle: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Primary Subject: {paper['primary_subject']}")
        print(f"All Subjects: {paper['subjects']}")
        print(f"PDF: {paper['pdf_url']}")
        print(f"arXiv: {paper['arxiv_url']}")
        print("-" * 80)
