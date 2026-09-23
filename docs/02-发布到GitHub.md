# 发布到 GitHub

本仓库已经是可直接发布的形态：纯静态、无需构建、`.gitignore` 已配置好。
下面是从零到上线 GitHub Pages 的完整步骤（Windows 环境）。

---

## 0. 前置检查

本机目前**未安装 Git**（`git` 不在 PATH 中）。先装 Git：

```powershell
winget install --id Git.Git -e
```

装完后**新开一个终端**（让 PATH 生效），确认：

```powershell
git --version
```

再设置提交身份（只需一次，会写进全局配置）：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

> 邮箱建议与 GitHub 账号一致，这样提交才会正确归到你名下。

---

## 1. 在 GitHub 上创建空仓库

1. 打开 <https://github.com/new>；
2. **Repository name** 填仓库名（例如 `lblb-math-library`）；
3. 可见性按需选择 **Public**（公开）或 **Private**（私有）；
4. **不要**勾选 "Add a README file"、".gitignore"、"license" —— 仓库里已经有了，勾了会冲突；
5. 点 **Create repository**。

创建完成后页面会显示仓库地址，形如 `https://github.com/<用户名>/<仓库名>.git`。

---

## 2. 初始化本地仓库并推送

在仓库目录（本文件所在的上级目录）打开 PowerShell：

```powershell
cd D:\LBLB-github

git init
git add .
git commit -m "chore: 初始化 LBLB 数学爱好者宝库"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

推送时会弹出浏览器登录 GitHub（或要求输入 Personal Access Token），按提示完成即可。

### 推送前建议先确认一次

提交前检查仓库里**没有**混进题库数据。执行：

```powershell
git status --short
```

输出里不应出现 `13-应试训练/123/` 下的题库 JS（`真题卷.js`、`题库-汇总.js`、
`文本整卷-新增.js` 等）或任何 `.pdf`。`.gitignore` 已默认排除这些文件；
若它们确实出现在待提交列表里，说明本地文件名与忽略规则不匹配，需要先修正再提交。

也可以先看一眼将要提交的文件总数与体积：

```powershell
git add .
git status --short | Measure-Object -Line
```

---

## 3. 开启 GitHub Pages（在线浏览）

1. 进入仓库 **Settings** → 左侧 **Pages**；
2. **Source** 选 `Deploy from a branch`；
3. **Branch** 选 `main`，目录选 `/ (root)`，点 **Save**；
4. 等待 1–2 分钟，页面顶部会显示访问地址：

   ```
   https://<用户名>.github.io/<仓库名>/
   ```

仓库根目录已包含 `.nojekyll`，GitHub Pages 不会对文件做 Jekyll 处理，
中文文件名与含下划线的路径都能正常访问。

> 项目页面的公式渲染依赖 `assets/` 目录，仓库已包含，无需额外配置。

---

## 4. 后续更新

```powershell
cd D:\LBLB-github
git add .
git commit -m "docs: 更新 xx 讲义"
git push
```

GitHub Pages 会在推送后自动重新部署。

---

## 备选方案：不装 Git

### 用 GitHub Desktop

1. 安装 <https://desktop.github.com/>；
2. **File → Add local repository**，选择 `D:\LBLB-github`；
3. 如果提示不是 Git 仓库，选择 **create a repository** 在此目录初始化；
4. 在界面上填写提交信息并 **Commit to main**，再点 **Publish repository**。

### 用网页上传

适合一次性发布，但仓库有 300 多个文件，网页拖拽上传较慢且后续维护不便，
仅建议用于小规模修补。路径：仓库页面 **Add file → Upload files**。

---

## 常见问题

**推送被拒（`rejected` / `non-fast-forward`）**
远程仓库比本地新，通常是创建仓库时勾选了 README。先拉取合并：

```powershell
git pull --rebase origin main
git push
```

**中文文件名在网页上显示为乱码**
在仓库根目录设置 `git config core.quotepath false`，让 `git status` 直接显示中文：

```powershell
git config core.quotepath false
```

这只影响本地终端的显示，不影响仓库内容。

**想收紧或放宽授权**
改 `LICENSE`、`LICENSE-MIT` 与 `README.md` 中的「授权与第三方」一节即可。
若换成单一许可，记得同步删除另一份许可文件，避免歧义。

**GitHub 提示仓库体积偏大**
当前约 14 MB（287 个文件），其中约 3.5 MB 是随仓库分发的 MathJax（保证离线可用）。
如果不需要离线渲染、希望仓库更小，可以改为从 CDN 加载 MathJax，
并把 `assets/` 从仓库中移除——但这样就破坏了「完全离线」这一特性，
需要在 `README.md` 中同步修改说明。
（注意：`assets/mathjax/es5/` 必须整份保留，其中的 `input/tex/extensions/` 是按需加载的模块，
删掉会让用到 `\boldsymbol` 等命令的页面整页公式都不渲染。详见 `README.md` 技术说明。）
