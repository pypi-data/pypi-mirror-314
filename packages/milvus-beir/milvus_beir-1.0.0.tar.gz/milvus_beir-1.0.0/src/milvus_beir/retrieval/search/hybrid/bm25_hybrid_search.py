import logging
import random
import time
from typing import Any, Dict, Optional

from milvus_model.base import BaseEmbeddingFunction
from milvus_model.dense import SentenceTransformerEmbeddingFunction
from pymilvus import (
    AnnSearchRequest,
    DataType,
    Function,
    FunctionType,
    RRFRanker,
)
from tqdm.autonotebook import tqdm

from milvus_beir.retrieval.search.milvus import MilvusBaseSearch
from milvus_beir.utils import measure_search_qps_decorator

logger = logging.getLogger(__name__)


def get_default_model() -> BaseEmbeddingFunction:
    return SentenceTransformerEmbeddingFunction()


def get_default_ranker():
    return RRFRanker()


class MilvusBM25DenseHybridSearch(MilvusBaseSearch):
    def __init__(
        self,
        uri: str,
        token: str | None,
        collection_name: str,
        nq: int = 100,
        nb: int = 1000,
        initialize: bool = True,
        clean_up: bool = True,
        model: BaseEmbeddingFunction = None,
        dense_vector_field: str = "dense_embedding",
        bm25_output_field: str = "sparse_embedding",
        dense_metric_type: str = "COSINE",
        bm25_metric_type: str = "BM25",
        dense_search_params: Optional[Dict] = None,
        bm25_search_params: Optional[Dict] = None,
        ranker: Any = None,
        sleep_time: int = 5,
    ):
        self.model = model if model is not None else get_default_model()
        self.dense_vector_field = dense_vector_field
        self.bm25_output_field = bm25_output_field
        self.dense_metric_type = dense_metric_type
        self.bm25_metric_type = bm25_metric_type
        self.dense_search_params = dense_search_params if dense_search_params is not None else {}
        self.bm25_search_params = bm25_search_params if bm25_search_params is not None else {}
        self.ranker = ranker if ranker is not None else get_default_ranker()
        self.sleep_time = sleep_time
        self.query_embeddings = []
        self.query_texts = []

        super().__init__(
            uri=uri,
            token=token,
            collection_name=collection_name,
            nq=nq,
            nb=nb,
            initialize=initialize,
            clean_up=clean_up,
        )

    def _initialize_collection(self):
        if self.milvus_client.has_collection(self.collection_name):
            self.milvus_client.drop_collection(self.collection_name)
        schema = self.milvus_client.create_schema()
        analyzer_params = {
            "type": "english",
        }
        schema.add_field("id", DataType.VARCHAR, max_length=1000, is_primary=True)
        schema.add_field(
            field_name="text",
            datatype=DataType.VARCHAR,
            max_length=65535,
            enable_analyzer=True,
            analyzer_params=analyzer_params,
        )
        schema.add_field(field_name=self.bm25_output_field, datatype=DataType.SPARSE_FLOAT_VECTOR)
        schema.add_field(self.dense_vector_field, DataType.FLOAT_VECTOR, dim=self.model.dim)
        bm25_function = Function(
            name="text_bm25_emb",  # Function name
            input_field_names=["text"],  # Name of the VARCHAR field containing raw text data
            output_field_names=[
                self.bm25_output_field
            ],  # Name of the SPARSE_FLOAT_VECTOR field reserved to store generated embeddings
            # Name of the SPARSE_FLOAT_VECTOR field reserved to store generated embeddings
            function_type=FunctionType.BM25,
        )
        schema.add_function(bm25_function)
        self.milvus_client.create_collection(collection_name=self.collection_name, schema=schema)

    def _index(self, corpus):
        logger.info("Sorting Corpus by document length (Longest first)...")
        corpus_ids = sorted(
            corpus,
            key=lambda k: len(corpus[k].get("title", "") + corpus[k].get("text", "")),
            reverse=True,
        )
        corpus = [corpus[cid] for cid in corpus_ids]
        logger.info("Encoding Corpus in batches... Warning: This might take a while!")
        for start in tqdm(range(0, len(corpus), self.nb)):
            end = min(start + self.nb, len(corpus))
            batch = corpus[start:end]
            texts = [doc.get("title", "") + " " + doc.get("text", "") for doc in batch]
            embeddings = self.model(texts)
            texts = [text[:60000] for text in texts]
            ids = corpus_ids[start:end]
            data = [
                {"id": id, "text": text, self.dense_vector_field: emb}
                for id, text, emb in zip(ids, texts, embeddings)
            ]
            self.milvus_client.insert(collection_name=self.collection_name, data=data)
        self.milvus_client.flush(self.collection_name)
        index_params = self.milvus_client.prepare_index_params()
        index_params.add_index(
            field_name=self.dense_vector_field, metric_type=self.dense_metric_type
        )

        self.milvus_client.create_index(
            collection_name=self.collection_name, index_params=index_params
        )
        index_params.add_index(field_name=self.bm25_output_field, metric_type=self.bm25_metric_type)
        self.milvus_client.create_index(
            collection_name=self.collection_name, index_params=index_params
        )

        self.milvus_client.load_collection(self.collection_name)
        self.index_completed = True
        logger.info("Indexing Completed!")

    def _single_search(self, args):
        query_text, top_k = args
        query_embeddings = self.model.encode_queries([query_text])
        query_texts = [query_text]

        try:
            dense_rqs = AnnSearchRequest(
                data=query_embeddings,
                anns_field="dense_embedding",
                param=self.dense_search_params,
                limit=top_k,
            )
            bm25_rqs = AnnSearchRequest(
                data=query_texts,
                anns_field=self.bm25_output_field,
                param=self.bm25_search_params,
                limit=top_k,
            )

            result = self.milvus_client.hybrid_search(
                collection_name=self.collection_name,
                reqs=[dense_rqs, bm25_rqs],
                ranker=self.ranker,
                limit=top_k,
                output_fields=["id"],
            )
            return result
        except Exception as e:
            logger.error(f"Search error: {e!s}")
            return None

    def search(
        self,
        corpus: Dict[str, Dict[str, str]],
        queries: Dict[str, str],
        top_k: int,
        *args,
        **kwargs,
    ) -> Dict[str, Dict[str, float]]:
        if self.initialize:
            self._initialize_collection()

        if not self.index_completed:
            self._index(corpus)

        query_ids = list(queries.keys())
        query_texts = [queries[qid] for qid in query_ids]
        query_embeddings = self.model.encode_queries(query_texts)

        batch_size = self.nq
        total_rows = len(queries)
        result_list = []
        for start in tqdm(range(0, total_rows, batch_size)):
            end = min(start + batch_size, total_rows)
            embeddings = query_embeddings[start:end]

            dense_rqs = AnnSearchRequest(
                data=embeddings,
                anns_field="dense_embedding",
                param=self.dense_search_params,
                limit=top_k,
            )
            bm25_rqs = AnnSearchRequest(
                data=query_texts[start:end],
                anns_field=self.bm25_output_field,
                param=self.bm25_search_params,
                limit=top_k,
            )

            result = self.milvus_client.hybrid_search(
                collection_name=self.collection_name,
                reqs=[dense_rqs, bm25_rqs],
                ranker=self.ranker,
                limit=top_k,
                output_fields=["id"],
            )
            result_list.extend(result)

        result_dict = {}
        for i in range(len(queries)):
            data = {}
            for hit in result_list[i]:
                data[hit["id"]] = hit["distance"]
            result_dict[query_ids[i]] = data

        return result_dict

    def measure_search_qps(
        self, corpus, queries, top_k=1000, concurrency_levels=None, test_duration=60
    ):
        if concurrency_levels is None:
            concurrency_levels = [1, 2, 4, 8, 16, 32]

        @measure_search_qps_decorator(
            concurrency_levels, test_duration=test_duration, max_threads=None
        )
        def _single_search(top_k):
            """ """
            random_id = random.randint(0, len(queries) - 1)
            text = self.query_texts[random_id]
            embedding = self.query_embeddings[random_id]

            try:
                client = self._get_thread_client()
                dense_rqs = AnnSearchRequest(
                    data=[embedding],
                    anns_field="dense_embedding",
                    param=self.dense_search_params,
                    limit=top_k,
                )
                bm25_rqs = AnnSearchRequest(
                    data=[text],
                    anns_field=self.bm25_output_field,
                    param=self.bm25_search_params,
                    limit=top_k,
                )

                result = client.hybrid_search(
                    collection_name=self.collection_name,
                    reqs=[dense_rqs, bm25_rqs],
                    ranker=self.ranker,
                    limit=top_k,
                    output_fields=["id"],
                )
                return result
            except Exception as e:
                logger.error(f"Search error: {e!s}")
                return None

        if not self.index_completed:
            self._index(corpus)
            time.sleep(self.sleep_time)
        query_ids = list(queries.keys())
        query_texts = [queries[qid] for qid in query_ids]
        query_embeddings = self.model.encode_queries(query_texts)
        self.query_embeddings = query_embeddings
        self.query_texts = query_texts
        res = _single_search(top_k)
        return res
