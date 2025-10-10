# Week 2 学习总结

## 目录
1. [学习目标](#学习目标)
2. [Shell 脚本自动化](#Shell-脚本自动化)
3. [LaTeX 科学写作](#LaTeX-科学写作)
4. [Git 版本控制](#Git-版本控制)
5. [综合收获与反思](#综合收获与反思)

---

## 学习目标

本周主题：**Shell 脚本自动化**、**LaTeX 科学写作**、**Git 版本控制**。

- **技术技能层面**
  - 掌握 Shell 脚本语法与自动化思维
  - 熟悉 LaTeX 文档编写与编译流程
  - 理解 Git 基本命令与协作机制
- **科研工作流层面**
  - 建立系统化、可复现的科研流程
  - 形成标准目录结构与规范记录
- **科研素养层面**
  - 培养工程化、可维护性与协作意识

---

## Shell 脚本自动化

### 核心知识点
- 批量处理文件、运行程序、提取数据
- 优势：可重复、易修改、与其他语言协作

### 脚本结构与语法
```bash
#!/bin/bash
# Author: Your Name
# Description: Example shell script
# Date: Oct 2025

echo "This is a shell script!"
```
- `#!/bin/bash`：指定解释器
- `#`：注释
- `echo`：输出命令
- `chmod +x script.sh`：赋予可执行权限
- `./script.sh`：运行脚本

### 变量与输入输出
```bash
#!/bin/bash
echo "Script name: $0"
echo "First argument: $1"
read NAME
echo "Hello, $NAME"
```
- 系统变量：`$PATH`, `$USER`
- 位置参数：`$0`, `$1`, `$#`
- 自定义变量：`MY_VAR="some string"`
- 命令替换：`VAR=$(command)`

### 实践案例
- `boilerplate.sh`：模板脚本
- `variables.sh`：变量与输入
- `tabtocsv.sh`：制表符转逗号
  ```bash
  cat $1 | tr -s "\t" "," > $1.csv
  ```
- `CountLines.sh`：统计行数
  ```bash
  wc -l < file
  ```
- `tiff2png.sh`：图片批量转换

### 编程规范
- 使用相对路径
- 输入检查：
  ```bash
  if [ "$#" -ne 1 ]; then
    echo "Usage: bash script.sh <filename>"
    exit 1
  fi
  ```
- 结果输出清晰
- 组织结构：`Code/`, `Data/`, `Sandbox/`, `Results/`
- 每目录配 README.md

### 学习收获
Shell scripting 提升科研自动化效率，理解 Bash 环境变量与命令替换，为后续整合 Python/R 打基础。

---

## LaTeX 科学写作

### 优势
- 版面统一、公式与引用支持好、自动生成目录与参考文献
- 内容与样式分离，利于版本控制

### 文档结构
```latex
\documentclass[12pt]{article}
\usepackage{graphicx,amsmath}
\title{A Simple Document}
\author{Your Name}
\date{}
\begin{document}
\maketitle
\section{Introduction}
This is the introduction section.
\end{document}
```
- `\documentclass[]{} `：文档类型
- `\usepackage{}`：功能包
- `\section{}`：章节
- `\begin{document} ~ \end{document}`：主内容

### 数学公式与环境
- 行内公式：`$E=mc^2$`
- 独立公式：
  ```latex
  \begin{equation}
  \int_0^1 p^x (1-p)^y dp
  \end{equation}
  ```
- 常见环境：itemize, enumerate, figure, table

### 参考文献与 BibTeX
- `.bib` 文件管理文献
  ```bibtex
  @article{verhulst1838notice,
    title={Notice sur la loi que la population suit dans son accroissement},
    author={Verhulst, Pierre-Fran{\c{c}}ois},
    journal={Corresp. Math. Phys.},
    year={1838}
  }
  ```
- 主文档引用：
  ```latex
  It was first proposed by Verhulst in 1838 \cite{verhulst1838notice}.
  \bibliographystyle{plain}
  \bibliography{FirstBiblio}
  ```

### 自动化编译脚本
```bash
#!/bin/bash
pdflatex $1.tex
bibtex $1
pdflatex $1.tex
pdflatex $1.tex
evince $1.pdf &
```
- 运行：`bash CompileLaTeX.sh FirstExample`

### 学习体会
独立编译带公式、参考文献与图表的 PDF，理解编译顺序与文件依赖。

---

## Git 版本控制

### 基础原理
- 分布式版本控制，追踪文件修改与协作
- 提升科研可复现性

### 基本命令与流程
| 操作         | 命令                        | 说明           |
| ------------ | -------------------------- | -------------- |
| 初始化仓库   | `git init`                 | 创建本地仓库   |
| 查看状态     | `git status`               | 显示修改状态   |
| 暂存文件     | `git add <file>`           | 添加至暂存区   |
| 提交修改     | `git commit -m "message"` | 保存版本快照   |
| 查看历史     | `git log`                  | 浏览提交历史   |
| 创建分支     | `git branch <name>`        | 新功能开发     |
| 切换分支     | `git checkout <name>`      | 移动分支       |
| 合并分支     | `git merge <name>`         | 合并更改       |
| 推送远程     | `git push origin main`     | 同步 GitHub    |

### .gitignore 使用
- 忽略临时文件和大数据：
  ```gitignore
  *.tmp
  *.csv
  *.log
  *.pdf
  Data/large_files/
  ```

### 团队协作与分支管理
- 独立分支开发，测试后合并 main
- 避免 `git push --force`
- 保持“commit often, comment always”习惯

### 实践成果
- 创建 CMEECourseWork 仓库
- 管理多脚本项目，使用 SSH 连接 GitHub
- 理解分支与冲突解决流程
- 规范 .gitignore 与 README.md

### 学习反思
Git 是科研协作核心工具，commit 粒度与信息清晰度对项目管理至关重要。

---

## 综合收获与反思

- **技能融合与流程改进**
  - Shell 实现批量数据转换与日志生成
  - LaTeX 结构化组织章节、公式和图表
  - Git 记录科研历程与分支实验思路
- **科研规范性与可复现性意识**
  - Git + LaTeX 可重现论文撰写与数据生成
  - Shell scripting 使分析流程模块化、透明化
- **困难与突破**
  - LaTeX 编译报错与 Git 冲突，通过调试与查阅文档逐步解决
- **科研方法论启发**
  - 科研编程是思维训练，强化系统工程观念
- **展望与提升方向**
  - 期待整合 Shell + Git + Python，实现一体化脚本化工作流
  - 学习 GitHub Actions、Makefile 等持续集成工具，实现“一键复现”
  - 目标：可执行分析脚本 + 自动生成报告 + 完整版本记录

---

> Shell 提供执行力，LaTeX 提供表达力，Git 提供可追溯性 —— 科研信息化与自动化的三脚架。