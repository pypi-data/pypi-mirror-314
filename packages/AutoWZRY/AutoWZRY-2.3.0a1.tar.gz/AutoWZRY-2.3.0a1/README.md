# AutoWZRY

* 此项目用于将 [WZRY](https://github.com/cndaqiang/WZRY) 子模块发布到 [AutoWZRY@PyPI](https://pypi.org/project/AutoWZRY/)。

* 用于在无法访问github的情况下获取[WZRY](https://github.com/cndaqiang/WZRY)代码. 即 `pip download AutoWZRY --no-deps`

* 当然也可以直接运行`autowzry.exe config.win.yaml`, 更多见[进阶教程](https://wzry-doc.pages.dev/guide/autowzry/)

## 构建发布过程
### 初始化仓库
[添加 WZRY 子模块](how_to_use_submodule.md)


### clone仓库
```
git clone --recurse-submodules  git@github.com:cndaqiang/AutoWZRY.git
```

### 更新代码
```
bash pull.sub.sh
```
### 发布
```
./build.ps1
```