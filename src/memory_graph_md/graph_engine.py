"""Graph engine for structured memory management."""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import networkx as nx


class NodeType(Enum):
    """Types of nodes in the memory graph."""
    ENTITY = "entity"
    CONCEPT = "concept"
    EVENT = "event"
    PERSON = "person"
    LOCATION = "location"
    ORGANIZATION = "organization"
    DATE = "date"
    GENERIC = "generic"


class RelationshipType(Enum):
    """Types of relationships between nodes."""
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    CAUSES = "causes"
    LEADS_TO = "leads_to"
    BELONGS_TO = "belongs_to"
    OCCURS_AT = "occurs_at"
    OCCURS_ON = "occurs_on"
    CREATED_BY = "created_by"
    KNOWS = "knows"
    WORKS_FOR = "works_for"
    LOCATED_AT = "located_at"
    UNKNOWN = "unknown"


@dataclass
class GraphNode:
    """Represents a node in the memory graph."""
    node_id: str
    label: str
    node_type: NodeType
    properties: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "node_id": self.node_id,
            "label": self.label,
            "node_type": self.node_type.value,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "confidence_score": self.confidence_score
        }


@dataclass
class GraphEdge:
    """Represents an edge (relationship) in the memory graph."""
    edge_id: str
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    properties: Dict[str, Any]
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "properties": self.properties,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class MemoryEntry:
    """Represents a memory entry in the graph."""
    entry_id: str
    content: str
    source: str
    metadata: Dict[str, Any]
    timestamp: datetime
    confidence_score: float
    entity_links: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entry_id": self.entry_id,
            "content": self.content,
            "source": self.source,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "confidence_score": self.confidence_score,
            "entity_links": self.entity_links
        }


class MemoryGraph:
    """Graph-based memory storage system."""
    
    def __init__(self, name: str = "default"):
        """
        Initialize memory graph.
        
        Args:
            name: Graph name
        """
        self._name = name
        self._graph = nx.DiGraph()
        self._node_map: Dict[str, GraphNode] = {}
        self._edge_map: Dict[str, GraphEdge] = {}
        self._memory_entries: Dict[str, MemoryEntry] = {}
        self._entry_counter = 0
    
    def add_entity(
        self,
        label: str,
        entity_type: NodeType,
        properties: Optional[Dict[str, Any]] = None,
        confidence: float = 0.9
    ) -> GraphNode:
        """
        Add an entity node to the graph.
        
        Args:
            label: Entity label/name
            entity_type: Type of entity
            properties: Entity properties
            confidence: Confidence score
            
        Returns:
            Created GraphNode
        """
        # Generate unique ID
        node_id = f"node_{datetime.now().timestamp():.0f}_{hash(label)}"
        
        # Check if entity already exists
        existing_id = self._find_similar_entity(label, entity_type)
        if existing_id:
            # Update existing node
            node = self._node_map[existing_id]
            node.properties.update(properties or {})
            node.updated_at = datetime.now()
            node.confidence_score = max(node.confidence_score, confidence)
            return node
        
        # Create new node
        node = GraphNode(
            node_id=node_id,
            label=label,
            node_type=entity_type,
            properties=properties or {},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            confidence_score=confidence
        )
        
        # Add to graph
        self._graph.add_node(node_id, 
                           label=label,
                           node_type=entity_type.value,
                           properties=properties or {},
                           confidence=confidence)
        
        self._node_map[node_id] = node
        return node
    
    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType,
        properties: Optional[Dict[str, Any]] = None
    ) -> Optional[GraphEdge]:
        """
        Add a relationship edge between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Type of relationship
            properties: Edge properties
            
        Returns:
            Created GraphEdge or None if nodes don't exist
        """
        # Check if nodes exist
        if source_id not in self._node_map or target_id not in self._node_map:
            return None
        
        # Generate unique ID
        edge_id = f"edge_{datetime.now().timestamp():.0f}_{hash(source_id) + hash(target_id)}"
        
        # Create edge
        edge = GraphEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {},
            created_at=datetime.now()
        )
        
        # Add to graph
        self._graph.add_edge(
            source_id,
            target_id,
            edge_id=edge_id,
            relationship_type=relationship_type.value,
            properties=properties or {}
        )
        
        self._edge_map[edge_id] = edge
        return edge
    
    def add_memory_entry(
        self,
        content: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
        confidence: float = 0.85
    ) -> MemoryEntry:
        """
        Add a memory entry and extract entities.
        
        Args:
            content: Memory content
            source: Source of memory
            metadata: Additional metadata
            confidence: Confidence score
            
        Returns:
            Created MemoryEntry
        """
        self._entry_counter += 1
        entry_id = f"mem_{self._entry_counter}_{datetime.now().timestamp():.0f}"
        
        # Extract entities from content (simplified for demo)
        entity_links = self._extract_entities(content)
        
        entry = MemoryEntry(
            entry_id=entry_id,
            content=content,
            source=source,
            metadata=metadata or {},
            timestamp=datetime.now(),
            confidence_score=confidence,
            entity_links=entity_links
        )
        
        self._memory_entries[entry_id] = entry
        
        # Link entry to graph nodes
        for entity_id in entity_links:
            if entity_id in self._node_map:
                self._graph.add_node(
                    entry_id,
                    label=f"Memory:{entry_id[:8]}",
                    node_type=NodeType.EVENT,
                    properties={"content": content[:100]},
                    confidence=confidence
                )
                self._node_map[entry_id] = GraphNode(
                    node_id=entry_id,
                    label=f"Memory:{entry_id[:8]}",
                    node_type=NodeType.EVENT,
                    properties={"content": content[:100]},
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    confidence_score=confidence
                )
                self.add_relationship(entry_id, entity_id, RelationshipType.BELONGS_TO)
        
        return entry
    
    def _extract_entities(self, content: str) -> List[str]:
        """
        Extract entities from content and link to graph.
        
        Args:
            content: Content to analyze
            
        Returns:
            List of entity IDs
        """
        entity_ids = []
        
        # Simplified entity extraction for demo
        # In production, would use NLP to extract entities
        words = content.lower().split()
        
        # Extract potential entities (simplified)
        for word in words:
            if len(word) > 4 and word.isalpha():
                # Check if entity exists
                existing = self._find_similar_entity(word, NodeType.GENERIC)
                if not existing:
                    # Create entity node
                    entity = self.add_entity(
                        label=word.capitalize(),
                        entity_type=NodeType.GENERIC,
                        properties={"extracted_from": content[:50]},
                        confidence=0.5
                    )
                    entity_ids.append(entity.node_id)
        
        return entity_ids
    
    def _find_similar_entity(self, label: str, entity_type: NodeType) -> Optional[str]:
        """
        Find a similar existing entity.
        
        Args:
            label: Entity label
            entity_type: Entity type
            
        Returns:
            Existing node ID or None
        """
        # Simple case-insensitive match
        label_lower = label.lower()
        
        for node_id, node in self._node_map.items():
            if (node.label.lower() == label_lower and 
                node.node_type == entity_type):
                return node_id
        
        return None
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """
        Get a node by ID.
        
        Args:
            node_id: Node identifier
            
        Returns:
            GraphNode or None
        """
        return self._node_map.get(node_id)
    
    def get_neighbors(
        self,
        node_id: str,
        max_depth: int = 2,
        relationship_types: Optional[List[RelationshipType]] = None
    ) -> List[Tuple[str, str, str]]:
        """
        Get neighboring nodes within max_depth.
        
        Args:
            node_id: Starting node ID
            max_depth: Maximum traversal depth
            relationship_types: Optional filter by relationship types
            
        Returns:
            List of (neighbor_id, relationship_type, distance) tuples
        """
        neighbors = []
        
        if node_id not in self._node_map:
            return neighbors
        
        # BFS traversal
        visited = {node_id}
        queue = [(node_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            # Get neighbors
            for neighbor_id in self._graph.successors(current_id):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    edge_data = self._graph.edges[current_id, neighbor_id]
                    
                    rel_type = RelationshipType(edge_data.get('relationship_type', 'unknown'))
                    
                    if relationship_types is None or rel_type in relationship_types:
                        neighbors.append((neighbor_id, rel_type.value, depth + 1))
                        queue.append((neighbor_id, depth + 1))
            
            for neighbor_id in self._graph.predecessors(current_id):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    edge_data = self._graph.edges[neighbor_id, current_id]
                    
                    rel_type = RelationshipType(edge_data.get('relationship_type', 'unknown'))
                    
                    if relationship_types is None or rel_type in relationship_types:
                        neighbors.append((neighbor_id, rel_type.value, depth + 1))
                        queue.append((neighbor_id, depth + 1))
        
        return neighbors
    
    def get_recent_entries(
        self,
        limit: int = 10,
        entity_filter: Optional[str] = None
    ) -> List[MemoryEntry]:
        """
        Get recent memory entries.
        
        Args:
            limit: Maximum entries to return
            entity_filter: Optional entity filter
            
        Returns:
            List of MemoryEntries
        """
        entries = sorted(
            self._memory_entries.values(),
            key=lambda e: e.timestamp,
            reverse=True
        )[:limit]
        
        if entity_filter:
            entries = [
                e for e in entries
                if any(
                    e_id in self._node_map and 
                    self._node_map[e_id].label.lower() == entity_filter.lower()
                    for e_id in e.entity_links
                )
            ]
        
        return entries
    
    def search_entities(
        self,
        query: str,
        entity_type: Optional[NodeType] = None,
        min_confidence: float = 0.0
    ) -> List[GraphNode]:
        """
        Search for entities matching query.
        
        Args:
            query: Search query
            entity_type: Optional entity type filter
            min_confidence: Minimum confidence score
            
        Returns:
            List of matching GraphNodes
        """
        results = []
        
        query_lower = query.lower()
        
        for node in self._node_map.values():
            if entity_type and node.node_type != entity_type:
                continue
            
            if node.confidence_score < min_confidence:
                continue
            
            # Search in label and properties
            searchable = f"{node.label} {json.dumps(node.properties)}".lower()
            
            if query_lower in searchable:
                results.append(node)
        
        return sorted(results, key=lambda n: n.confidence_score, reverse=True)
    
    def get_subgraph(self, seed_nodes: List[str], max_depth: int = 2) -> nx.DiGraph:
        """
        Get a subgraph centered on seed nodes.
        
        Args:
            seed_nodes: Seed node IDs
            max_depth: Maximum traversal depth
            
        Returns:
            NetworkX subgraph
        """
        subgraph = self._graph.copy()
        
        # Filter to only relevant nodes
        relevant_nodes = set(seed_nodes)
        
        for seed in seed_nodes:
            if seed in self._node_map:
                neighbors = self.get_neighbors(seed, max_depth)
                for neighbor_id, _, _ in neighbors:
                    relevant_nodes.add(neighbor_id)
        
        # Remove nodes not in relevant set
        for node in list(subgraph.nodes()):
            if node not in relevant_nodes:
                subgraph.remove_node(node)
        
        return subgraph
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get graph statistics.
        
        Returns:
            Dictionary of statistics
        """
        total_nodes = len(self._node_map)
        total_edges = len(self._edge_map)
        total_entries = len(self._memory_entries)
        
        entity_types = {}
        for node in self._node_map.values():
            type_name = node.node_type.value
            entity_types[type_name] = entity_types.get(type_name, 0) + 1
        
        relationship_types = {}
        for edge in self._edge_map.values():
            type_name = edge.relationship_type.value
            relationship_types[type_name] = relationship_types.get(type_name, 0) + 1
        
        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "total_entries": total_entries,
            "entity_types": entity_types,
            "relationship_types": relationship_types,
            "graph_name": self._name
        }
