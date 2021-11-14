# U100KIndexer

An Indexer that works out-of-the-box when you have less than 100K stored Documents. `U100K` means under 100K. At 100K stored Documents with 768-dim embeddings, you can expect 300ms for single query or 20~120QPS for batch queries. Results are **full Documents**.

`U100KIndexer` leverages `jina.DocumenetArrayMemmap` as the storage backend and `.match()` to conduct nearest neighbours search. It returns the full Documents as-is, hence no need to concatenate it with another key-value indexer to retrieve Documents.

The indexing and query performance on 768-dim embeddings is as follows (unit is second):

|Stored data| Indexing time | Query size=1 | Query size=8 | Query size=64|
|---|---|---|---|---|
|10000 | 0.256 | 0.019 | 0.029 | 0.086|
|50000 | 1.156 | 0.147 | 0.177 | 0.314|
|100000 | 2.329 | 0.297 | 0.332 | 0.536|
|200000 | 4.704 | 0.656 | 0.744 | 1.050|
|400000 | 11.105 | 1.289 | 1.536 | 2.793|

Benchmark script can be found in [`benchmark.py`](benchmark.py).

To change workspace, 

```python
U100KIndexer(metas={'workspace': './my'})
```

Or `.add(..., uses_metas={'workspace': './my'})` when you use it in a Flow.