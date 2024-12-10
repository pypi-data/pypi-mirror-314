if (Test-Path dist) {
    rm -r dist
}

py -m build
py -m twine upload dist/* # 上传，需要 token
