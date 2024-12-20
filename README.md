# ArXiv Paper Classifier

这是一个用于获取、翻译和分类 ArXiv 论文的工具。它可以自动获取最新的论文，将其翻译成中文，并根据预定义的类别进行分类，最终生成一个格式化的 Markdown 文档。

## 主要功能

1. 论文获取：通过 ArxivFetcher 自动获取最新的 ArXiv 论文
2. 中英翻译：使用 BytedanceTranslator 将论文标题和摘要翻译成中文
3. 论文分类：使用 BytedanceClassifier 将论文按主题自动分类
4. Markdown 输出：生成格式化的 Markdown 文档，包含分类、论文链接和摘要

## 使用方法
### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

参考字节跳动官方示例配置环境变量：
```bash
export ARK_API_KEY="YOUR_API_KEY" # linux / macos
$env:ARK_API_KEY = "YOUR_API_KEY" # windows powershell
set ARK_API_KEY=YOUR_API_KEY # windows cmd
```

### 3. 运行程序

```bash
python codes/main.py
```
程序会生成一个 `output.md` 文件，包含分类后的论文列表。

## 项目结构
- `main.py`: 主程序入口
- `arxiv_fetcher.py`: 负责从 ArXiv 获取论文
- `bytedance_translator.py`: 处理英文到中文的翻译
- `bytedance_classifier.py`: 处理论文分类
- `bytedance_ai_client.py`: AI API 客户端

## 注意事项

- 需要有效的 API 密钥和访问权限
- 翻译和分类功能依赖于 AI 服务的可用性
- 建议添加错误处理和重试机制
- 可以根据需要调整分类类别
- 输出文件使用 UTF-8 编码，确保正确显示中文

## 可能的扩展

- 添加缓存机制减少 API 调用
- 添加更多的论文源
- 支持自定义分类规则
- 添加定时任务自动更新
- 添加 Web 界面

## 许可协议

本项目采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 协议。这意味着您可以：

### 允许
- 复制、分发和传播本作品
- 修改、转换或以本作品为基础进行创作

### 惟须遵守下列条件
- **署名**：您必须按照作者或者许可人指定的方式对作品进行署名
- **非商业性使用**：您不得将本作品用于商业目的
- **相同方式共享**：如果您改变、转换本作品或者以本作品为基础进行创作，您只能采用与本协议相同的许可协议发布基于本作品的演绎作品

### 声明
- 您不必因为公共领域的作品要素而遵守许可协议，或者您的使用被可适用的例外或限制所允许
- 不提供担保。许可协议可能不会给与您意图使用的所必须的所有许可。例如，其他权利比如形象权、隐私权或人格权可能限制您如何使用作品