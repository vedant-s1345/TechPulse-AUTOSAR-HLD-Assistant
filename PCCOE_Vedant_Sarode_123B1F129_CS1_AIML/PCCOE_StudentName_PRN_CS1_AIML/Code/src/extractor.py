"""
AUTOSAR Architectural Entity Extractor module.
Extracts Software Components (SWCs), ports, interfaces, ASIL levels, and functional flows.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass, field
from src.chunking import TextChunk

@dataclass
class ArchitectureEntity:
    """Represents an extracted AUTOSAR architectural entity."""
    entity_type: str  # SWC, Interface, Port, FunctionalFlow, SafetyConstraint
    name: str
    doc_name: str
    page_num: int
    details: str

class ArchitectureExtractor:
    """Rule-based and pattern-based extractor for AUTOSAR HLD elements."""

    def __init__(self, chunks: List[TextChunk]):
        self.chunks = chunks

    def extract_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extracts complete architecture catalog across all chunks."""
        components = []
        interfaces = []
        flows = []
        safety_items = []

        seen_names = set()

        for chunk in self.chunks:
            text = chunk.text

            # 1. Extract Software Components (SWC)
            # Matches "Component Name: X", "BmsCellSupervisor_SWC", etc.
            swc_matches = re.findall(r'(?:Component Name:\s*([A-Za-z0-9_]+))|([A-Za-z0-9_]+_SWC)', text)
            for m in swc_matches:
                swc_name = m[0] or m[1]
                if swc_name and swc_name not in seen_names:
                    seen_names.add(swc_name)
                    components.append({
                        "name": swc_name,
                        "type": "Software Component (SWC)",
                        "document": chunk.doc_name,
                        "page": chunk.page_num,
                        "context_snippet": text[:150].replace('\n', ' ')
                    })

            # 2. Extract Interfaces & Ports
            # Matches "If_...", "RPort_...", "PPort_..."
            if_matches = re.findall(r'\b(If_[A-Za-z0-9_]+|RPort_[A-Za-z0-9_]+|PPort_[A-Za-z0-9_]+)\b', text)
            for item in if_matches:
                if item not in seen_names:
                    seen_names.add(item)
                    kind = "Port" if item.startswith(("RPort", "PPort")) else "Interface"
                    interfaces.append({
                        "name": item,
                        "category": kind,
                        "document": chunk.doc_name,
                        "page": chunk.page_num
                    })

            # 3. Extract Functional Flows
            # Matches "Sequence FF-..." or "Flow: ..."
            flow_matches = re.findall(r'(Sequence\s+FF-[A-Za-z0-9\-]+:[^\n]+)', text)
            for flow in flow_matches:
                if flow not in seen_names:
                    seen_names.add(flow)
                    flows.append({
                        "flow_id": flow.split(':')[0].strip(),
                        "description": flow.strip(),
                        "document": chunk.doc_name,
                        "page": chunk.page_num
                    })

            # 4. Extract Safety Constraints (ASIL)
            asil_matches = re.findall(r'\b(ASIL\s+[A-D]|Safety Goal\s+[A-Za-z0-9\-]+:[^\n]+)', text, re.IGNORECASE)
            for asil in asil_matches:
                if asil not in seen_names:
                    seen_names.add(asil)
                    safety_items.append({
                        "safety_requirement": asil.strip(),
                        "document": chunk.doc_name,
                        "page": chunk.page_num
                    })

        return {
            "components": components,
            "interfaces": interfaces,
            "functional_flows": flows,
            "safety_constraints": safety_items
        }
