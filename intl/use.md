# 国际化

全部的流程化过程见 `.github/workflows/deploy.yml`。

## 本地化部署

创建并激活环境：

```sh
conda create -n py39 python=3.9
conda activate py39
pip install sphinx-intl
```

克隆不同分支的 Nuitka 源码：

```sh
git clone https://github.com/Nuitka/Nuitka.git -b main Nuitka-main
git clone https://github.com/Nuitka/Nuitka.git -b develop Nuitka-develop
git clone https://github.com/Nuitka/Nuitka.git -b factory Nuitka-factory

mkdir docs/doc/ docs/doc/images/
cp -rf doc/doc/images/  docs/images
cp doc/pages/images/gitter-badge.svg  docs/images/gitter-badge.svg
cp Nuitka-develop/doc/images/Nuitka-Logo-Symbol.png docs/doc/images/Nuitka-Logo-Symbol.png
```

构建多语言：

```sh
cd docs
make gettext
sphinx-intl update -p ../output/gettext -l zh_CN,en
```

构建英文原文：

```sh
cp -rf doc/posts docs/posts/
cd docs
make html
rm -rf posts/
```

构建其他语言：

```sh
cd docs
sphinx-build -D language=zh_CN -b html ./ ../output/html/zh_CN
```

最终的输出的主版本为 `html/`，中文版本在 `html/zh_CN/`。

当然，可以输出更多的其他语言版本。
