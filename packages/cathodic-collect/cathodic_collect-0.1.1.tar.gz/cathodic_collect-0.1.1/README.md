# cathodic-collect

This package is used to collect files.

这个库可以将生成的文件进行解析，来生成报告。

## Install

`pip install cathodic-report`

## Usage

本库的使用方法如下。

### 如何使用`collect`?

参考文件[test_collect](./tests/test_collect.py).

### 如何使用 `GraphReader`?

参考文件[test_graph](./tests/reader/test_graph.py).

## Depends on

```txt
web -> collect -> report
    -> cp-core
```
