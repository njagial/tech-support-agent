# Vector Store - Qdrant Integration
from qdrant_client import QdrantClient
from qdrant_client.models import Record, VectorParams, Distance
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self, url: str = "http://localhost:6333", collection_name: str = "tech_support_kb"):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=768,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.warning(f"Collection check error (may be single-node): {e}")

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """Add a document to the vector store"""
        from langchain_community.embeddings import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings()
        vector = embeddings.embed_documents([content])[0]

        self.client.upsert(
            collection_name=self.collection_name,
            points=[Record(id=doc_id, vector=vector, payload=metadata)]
        )
        logger.info(f"Added document {doc_id} to vector store")

    def search(self, query_text: str, limit: int = 5) -> List[Any]:
        """Search the vector store for similar documents"""
        from langchain_community.embeddings import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings()
        query_vector = embeddings.embed_query(query_text)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        return results

    def search_by_filter(self, query_text: str, filters: Dict[str, Any], limit: int = 5) -> List[Any]:
        """Search with filters (e.g., by OS)"""
        results = self.search(query_text, limit)

        # Apply client-side filtering
        filtered_results = []
        for result in results:
            payload = result.payload
            match = True
            for key, value in filters.items():
                if payload.get(key) != value:
                    match = False
                    break
            if match:
                filtered_results.append(result)

        return filtered_results

    def delete_document(self, doc_id: str):
        """Delete a document from the vector store"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[doc_id]
        )
