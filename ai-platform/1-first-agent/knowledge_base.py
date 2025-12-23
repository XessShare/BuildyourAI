"""
Knowledge Base System - Vector Database Integration

Dieses System:
- Speichert Knowledge persistent in ChromaDB
- Ermöglicht semantic search über gespeichertes Wissen
- Verwaltet verschiedene Collections (Research, Facts, Insights)
- Tracked Metadaten (Source, Timestamp, Agent, Confidence)
- Unterstützt Knowledge-Sharing zwischen Agenten
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path
import logging
import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_PATH, COLLECTION_NAME


class KnowledgeBase:
    """
    Vector Database System für persistent Knowledge Storage

    Features:
    1. Knowledge storage with embeddings
    2. Semantic search and retrieval
    3. Multiple collections for different knowledge types
    4. Metadata tracking (source, agent, timestamp, confidence)
    5. Knowledge sharing across agents
    6. Statistics and analytics
    """

    def __init__(
        self,
        persist_directory: str = CHROMA_DB_PATH,
        collection_name: str = COLLECTION_NAME
    ):
        """
        Initialize Knowledge Base with ChromaDB

        Args:
            persist_directory: Path to persist ChromaDB data
            collection_name: Main collection name
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger("knowledge_base")
        self.logger.setLevel(logging.INFO)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Main collection
        self.collection_name = collection_name
        self.collection = self._get_or_create_collection(collection_name)

        # Collections for different knowledge types
        self.collections = {
            "research": self._get_or_create_collection("research"),
            "facts": self._get_or_create_collection("facts"),
            "insights": self._get_or_create_collection("insights"),
            "content": self._get_or_create_collection("content"),
            "general": self.collection
        }

        self.logger.info(f"Knowledge Base initialized at {persist_directory}")

    def _get_or_create_collection(self, name: str):
        """Get existing collection or create new one"""
        try:
            return self.client.get_collection(name=name)
        except Exception:
            return self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )

    def add_knowledge(
        self,
        content: str,
        knowledge_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
        knowledge_id: Optional[str] = None
    ) -> str:
        """
        Add knowledge to the database

        Args:
            content: The knowledge content/text
            knowledge_type: Type of knowledge (research, facts, insights, content, general)
            metadata: Additional metadata (source, agent, confidence, etc.)
            knowledge_id: Optional custom ID (auto-generated if not provided)

        Returns:
            The ID of the stored knowledge
        """
        # Prepare metadata
        meta = {
            "type": knowledge_type,
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content)
        }
        if metadata:
            # ChromaDB only accepts str, int, float, bool, None
            # Convert lists to comma-separated strings
            for key, value in metadata.items():
                if isinstance(value, list):
                    meta[key] = ", ".join(str(v) for v in value)
                else:
                    meta[key] = value

        # Generate ID if not provided
        if not knowledge_id:
            knowledge_id = f"{knowledge_type}_{datetime.now().timestamp()}_{hash(content) % 10000}"

        # Get appropriate collection
        collection = self.collections.get(knowledge_type, self.collection)

        # Add to collection
        collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[knowledge_id]
        )

        self.logger.info(f"Added knowledge: {knowledge_id} to {knowledge_type}")
        return knowledge_id

    def add_research(
        self,
        topic: str,
        findings: str,
        sources: Optional[List[str]] = None,
        agent: str = "researcher",
        confidence: float = 1.0
    ) -> str:
        """
        Add research findings to knowledge base

        Args:
            topic: Research topic
            findings: Research findings/results
            sources: List of sources/citations
            agent: Agent that created the research
            confidence: Confidence score (0-1)

        Returns:
            Knowledge ID
        """
        metadata = {
            "topic": topic,
            "agent": agent,
            "confidence": confidence,
            "sources": sources if sources else [],
            "source_count": len(sources) if sources else 0
        }

        content = f"Topic: {topic}\n\nFindings:\n{findings}"
        if sources:
            content += f"\n\nSources: {', '.join(sources)}"

        return self.add_knowledge(
            content=content,
            knowledge_type="research",
            metadata=metadata
        )

    def add_fact(
        self,
        fact: str,
        verified: bool = True,
        sources: Optional[List[str]] = None,
        confidence: float = 1.0,
        agent: str = "verifier"
    ) -> str:
        """
        Add verified fact to knowledge base

        Args:
            fact: The factual statement
            verified: Whether the fact has been verified
            sources: Supporting sources
            confidence: Verification confidence (0-1)
            agent: Agent that verified the fact

        Returns:
            Knowledge ID
        """
        metadata = {
            "verified": verified,
            "confidence": confidence,
            "agent": agent,
            "sources": sources if sources else [],
            "verification_status": "verified" if verified else "unverified"
        }

        return self.add_knowledge(
            content=fact,
            knowledge_type="facts",
            metadata=metadata
        )

    def add_insight(
        self,
        insight: str,
        category: str = "general",
        source_data: Optional[str] = None,
        agent: str = "analyst",
        actionable: bool = True
    ) -> str:
        """
        Add analytical insight to knowledge base

        Args:
            insight: The insight/finding
            category: Category of insight
            source_data: Description of source data
            agent: Agent that generated the insight
            actionable: Whether the insight is actionable

        Returns:
            Knowledge ID
        """
        metadata = {
            "category": category,
            "agent": agent,
            "actionable": actionable,
            "source_data": source_data if source_data else "unknown"
        }

        return self.add_knowledge(
            content=insight,
            knowledge_type="insights",
            metadata=metadata
        )

    def add_content(
        self,
        content: str,
        content_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add generated content to knowledge base

        Args:
            content: The content text
            content_type: Type of content (video_script, newsletter, blog, etc.)
            metadata: Additional metadata

        Returns:
            Knowledge ID
        """
        meta = {"content_type": content_type}
        if metadata:
            meta.update(metadata)

        return self.add_knowledge(
            content=content,
            knowledge_type="content",
            metadata=meta
        )

    def search(
        self,
        query: str,
        knowledge_type: Optional[str] = None,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Semantic search for relevant knowledge

        Args:
            query: Search query
            knowledge_type: Optional type filter (research, facts, insights, content)
            n_results: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            Dict with results, distances, and metadata
        """
        # Select collection
        collection = self.collections.get(knowledge_type, self.collection) if knowledge_type else self.collection

        # Perform search
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata if filter_metadata else None
        )

        # Format results
        if not results["documents"] or not results["documents"][0]:
            return {
                "query": query,
                "results": [],
                "count": 0
            }

        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "id": results["ids"][0][i],
                "distance": results["distances"][0][i] if results["distances"] else None
            })

        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        }

    def search_research(
        self,
        query: str,
        n_results: int = 5,
        min_confidence: Optional[float] = None
    ) -> Dict[str, Any]:
        """Search for research findings"""
        filter_meta = {}
        if min_confidence is not None:
            filter_meta["confidence"] = {"$gte": min_confidence}

        return self.search(
            query=query,
            knowledge_type="research",
            n_results=n_results,
            filter_metadata=filter_meta if filter_meta else None
        )

    def search_facts(
        self,
        query: str,
        verified_only: bool = True,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """Search for verified facts"""
        filter_meta = {"verified": True} if verified_only else None

        return self.search(
            query=query,
            knowledge_type="facts",
            n_results=n_results,
            filter_metadata=filter_meta
        )

    def search_insights(
        self,
        query: str,
        category: Optional[str] = None,
        actionable_only: bool = False,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """Search for analytical insights"""
        filter_meta = {}
        if category:
            filter_meta["category"] = category
        if actionable_only:
            filter_meta["actionable"] = True

        return self.search(
            query=query,
            knowledge_type="insights",
            n_results=n_results,
            filter_metadata=filter_meta if filter_meta else None
        )

    def get_by_id(
        self,
        knowledge_id: str,
        knowledge_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve knowledge by ID

        Args:
            knowledge_id: The knowledge ID
            knowledge_type: Optional type hint

        Returns:
            Knowledge data or None if not found
        """
        # Try specified collection first
        if knowledge_type:
            collection = self.collections.get(knowledge_type, self.collection)
            try:
                result = collection.get(ids=[knowledge_id])
                if result["documents"]:
                    return {
                        "id": knowledge_id,
                        "content": result["documents"][0],
                        "metadata": result["metadatas"][0] if result["metadatas"] else {}
                    }
            except Exception as e:
                self.logger.warning(f"ID not found in {knowledge_type}: {e}")

        # Try all collections
        for coll_name, collection in self.collections.items():
            try:
                result = collection.get(ids=[knowledge_id])
                if result["documents"]:
                    return {
                        "id": knowledge_id,
                        "content": result["documents"][0],
                        "metadata": result["metadatas"][0] if result["metadatas"] else {},
                        "collection": coll_name
                    }
            except Exception:
                continue

        return None

    def delete(
        self,
        knowledge_id: str,
        knowledge_type: Optional[str] = None
    ) -> bool:
        """
        Delete knowledge by ID

        Args:
            knowledge_id: The knowledge ID
            knowledge_type: Optional type hint

        Returns:
            True if deleted, False if not found
        """
        # Try specified collection first
        if knowledge_type:
            collection = self.collections.get(knowledge_type, self.collection)
            try:
                collection.delete(ids=[knowledge_id])
                self.logger.info(f"Deleted knowledge: {knowledge_id} from {knowledge_type}")
                return True
            except Exception as e:
                self.logger.warning(f"Failed to delete from {knowledge_type}: {e}")

        # Try all collections
        for coll_name, collection in self.collections.items():
            try:
                collection.delete(ids=[knowledge_id])
                self.logger.info(f"Deleted knowledge: {knowledge_id} from {coll_name}")
                return True
            except Exception:
                continue

        return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base

        Returns:
            Statistics for all collections
        """
        stats = {
            "total_knowledge": 0,
            "collections": {}
        }

        for name, collection in self.collections.items():
            count = collection.count()
            stats["collections"][name] = {
                "count": count,
                "name": name
            }
            stats["total_knowledge"] += count

        stats["created_at"] = datetime.now().isoformat()

        return stats

    def clear_collection(self, knowledge_type: str = "general") -> bool:
        """
        Clear all knowledge from a collection

        Args:
            knowledge_type: Collection to clear

        Returns:
            True if successful
        """
        try:
            collection = self.collections.get(knowledge_type)
            if collection:
                # Delete and recreate collection
                self.client.delete_collection(name=knowledge_type)
                self.collections[knowledge_type] = self._get_or_create_collection(knowledge_type)
                self.logger.info(f"Cleared collection: {knowledge_type}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to clear collection {knowledge_type}: {e}")
            return False

    def reset_all(self) -> bool:
        """
        Reset entire knowledge base (DESTRUCTIVE)

        Returns:
            True if successful
        """
        try:
            self.client.reset()
            # Recreate collections
            for name in self.collections.keys():
                self.collections[name] = self._get_or_create_collection(name)
            self.logger.warning("Knowledge Base has been reset!")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reset knowledge base: {e}")
            return False


# Quick test function
def test_knowledge_base():
    """Test the Knowledge Base system"""
    print("=" * 60)
    print("Testing Knowledge Base")
    print("=" * 60)

    kb = KnowledgeBase()

    # Test: Add research
    print("\n[TEST] Adding research finding...")
    research_id = kb.add_research(
        topic="AI Model Performance",
        findings="GPT-4o-mini shows strong performance with 128k context window and competitive pricing.",
        sources=["OpenAI Documentation", "Benchmarks"],
        confidence=0.95
    )
    print(f"✓ Added research: {research_id}")

    # Test: Add fact
    print("\n[TEST] Adding verified fact...")
    fact_id = kb.add_fact(
        fact="Claude 3.5 Sonnet was released by Anthropic in 2024",
        verified=True,
        confidence=1.0
    )
    print(f"✓ Added fact: {fact_id}")

    # Test: Add insight
    print("\n[TEST] Adding analytical insight...")
    insight_id = kb.add_insight(
        insight="Subscriber growth shows consistent upward trend with 150% target achievement",
        category="performance",
        actionable=True
    )
    print(f"✓ Added insight: {insight_id}")

    # Test: Search
    print("\n[TEST] Searching knowledge base...")
    results = kb.search("AI models performance")
    print(f"✓ Found {results['count']} results")
    if results['results']:
        print(f"  Top result: {results['results'][0]['content'][:100]}...")

    # Test: Get stats
    print("\n[TEST] Getting knowledge base statistics...")
    stats = kb.get_stats()
    print(f"✓ Total knowledge items: {stats['total_knowledge']}")
    print("  Collection breakdown:")
    for name, info in stats['collections'].items():
        print(f"    - {name}: {info['count']} items")

    print("\n" + "=" * 60)
    print("Knowledge Base tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_base()
