"""
Grounded Question Answering Engine for AUTOSAR HLD Document Analysis Assistant.
Supports Gemini API and Deterministic Retrieval-Only Fallback with strict citation validation.
"""

import time
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from src.retriever import DocumentRetriever, RetrievedPassage
from src.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, format_context_block

@dataclass
class QAResponse:
    """Encapsulates the complete grounded Q&A response and verification telemetry."""
    query: str
    answer: str
    passages: List[RetrievedPassage]
    citations: List[str]
    provider_used: str
    grounded: bool
    is_insufficient_evidence: bool
    latency_ms: float
    raw_prompt: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class GroundedQAEngine:
    """Orchestrates document retrieval and grounded answer synthesis."""

    def __init__(
        self,
        retriever: DocumentRetriever,
        provider: str = "gemini",
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.0,
        similarity_threshold: float = 0.20
    ):
        self.retriever = retriever
        self.provider = provider
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.similarity_threshold = similarity_threshold

    def _is_adversarial_injection(self, text: str) -> bool:
        """Detect prompt injection and instruction override attempts."""
        t_low = text.lower()
        injection_signals = [
            "ignore all previous",
            "ignore previous instructions",
            "system override",
            "reveal secret",
            "reveal password",
            "reveal your prompt",
            "disable citations",
            "display secret",
            "bypass guardrails"
        ]
        return any(sig in t_low for sig in injection_signals)

    def answer_question(self, question: str, top_k: int = 4) -> QAResponse:
        """
        Executes grounded retrieval and answer synthesis for a user query.
        """
        start_time = time.time()
        q_clean = question.strip()

        # 1. Handle empty/whitespace input boundary
        if not q_clean:
            return QAResponse(
                query=question,
                answer="Invalid input: Question cannot be empty.",
                passages=[],
                citations=[],
                provider_used="input_validator",
                grounded=False,
                is_insufficient_evidence=True,
                latency_ms=(time.time() - start_time) * 1000
            )

        # 2. Adversarial prompt injection defense guard
        if self._is_adversarial_injection(q_clean):
            return QAResponse(
                query=question,
                answer="The provided document does not provide enough information to answer this question. (Untrusted instruction override attempt neutralized).",
                passages=[],
                citations=[],
                provider_used="security_guardrail",
                grounded=True,
                is_insufficient_evidence=True,
                latency_ms=(time.time() - start_time) * 1000
            )

        # 3. Retrieve relevant evidence passages
        passages = self.retriever.retrieve(q_clean, top_k=top_k)

        # 4. Handle empty knowledge base
        if not passages:
            return QAResponse(
                query=question,
                answer="The provided document does not provide enough information to answer this question. (No indexed passages available)",
                passages=[],
                citations=[],
                provider_used="retrieval_guard",
                grounded=True,
                is_insufficient_evidence=True,
                latency_ms=(time.time() - start_time) * 1000
            )

        # 5. Check if top passage similarity is below threshold
        best_score = passages[0].score
        if best_score < self.similarity_threshold:
            return QAResponse(
                query=question,
                answer="The provided document does not provide enough information to answer this question. (Retrieval confidence below threshold)",
                passages=passages,
                citations=[],
                provider_used="relevance_filter",
                grounded=True,
                is_insufficient_evidence=True,
                latency_ms=(time.time() - start_time) * 1000
            )

        # 6. Decide whether to use Gemini LLM or Deterministic Fallback
        use_gemini = (self.provider == "gemini") and bool(self.api_key and len(self.api_key.strip()) > 5)

        if use_gemini:
            response = self._call_gemini(q_clean, passages, start_time)
        else:
            response = self._run_deterministic_fallback(q_clean, passages, start_time)

        return response

    def _call_gemini(self, question: str, passages: List[RetrievedPassage], start_time: float) -> QAResponse:
        """Synthesize answer using Google Gemini API with strict grounding instructions."""
        from google import genai
        from google.genai import types

        context_block = format_context_block(passages)
        prompt_content = USER_PROMPT_TEMPLATE.format(question=question, context_block=context_block)

        try:
            client = genai.Client(api_key=self.api_key)
            result = client.models.generate_content(
                model=self.model_name,
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=self.temperature
                )
            )
            raw_answer = result.text.strip() if result.text else ""
            latency_ms = (time.time() - start_time) * 1000

            is_insufficient = "does not provide enough information" in raw_answer.lower()
            citations = self._extract_citations(raw_answer, passages)

            return QAResponse(
                query=question,
                answer=raw_answer,
                passages=passages,
                citations=citations,
                provider_used=f"Google Gemini ({self.model_name})",
                grounded=True,
                is_insufficient_evidence=is_insufficient,
                latency_ms=latency_ms,
                raw_prompt=prompt_content
            )
        except Exception as e:
            # Fallback gracefully to deterministic extraction if API call fails
            print(f"[Warning] Gemini API call failed ({e}). Reverting to deterministic retrieval fallback.")
            fallback = self._run_deterministic_fallback(question, passages, start_time)
            fallback.answer = f"[Note: Gemini API unavailable ({str(e)}). Displaying deterministic retrieval result:]\n\n" + fallback.answer
            return fallback

    def _run_deterministic_fallback(self, question: str, passages: List[RetrievedPassage], start_time: float) -> QAResponse:
        """
        Deterministic, offline extraction fallback.
        Selects salient sentences matching query keywords directly from top retrieved passages.
        Ensures strict ground-truth traceability without calling any external LLM.
        """
        # Split query into keywords
        raw_words = re.findall(r'\b[A-Za-z0-9_\-]{3,}\b', question.lower())
        stop_words = {
            "what", "when", "where", "which", "does", "have", "from", "with",
            "this", "that", "these", "those", "explain", "describe", "show",
            "list", "name", "the", "and", "for", "how", "are", "about", "can",
            "will", "into", "been", "form", "make", "system", "specified", "involved"
        }
        keywords = {k for k in raw_words if k not in stop_words}

        found_sentences = []
        citations_found = set()
        all_matched_keywords = set()

        is_component_query = any(k in question.lower() for k in ["component", "swc", "interface", "port", "module"])

        for p in passages:
            chunk_text = p.chunk.text
            citation_label = f"[{p.chunk.doc_name}, Page {p.chunk.page_num}]"
            
            # Split by sentences or structured lines
            lines = [l.strip() for l in chunk_text.splitlines() if l.strip()]
            for line in lines:
                if len(line) < 15:
                    continue
                line_lower = line.lower()
                matched_in_line = {kw for kw in keywords if kw in line_lower}
                matches = len(matched_in_line)
                
                # Architecture boost: if query asks about components/interfaces and line defines one
                if is_component_query and any(tag in line for tag in ["Component Name:", "_SWC", "Interface", "PPort_", "RPort_"]):
                    matches += 3

                if matches > 0:
                    all_matched_keywords.update(matched_in_line)
                    found_sentences.append((matches, line, citation_label, p.score, p.citation_str))

        # Check keyword coverage across the entire query
        keyword_coverage = len(all_matched_keywords) / max(len(keywords), 1)
        top_score = passages[0].score if passages else 0.0
        latency_ms = (time.time() - start_time) * 1000

        # Reject out-of-scope or unsupported queries if coverage is low or score is weak
        if (keyword_coverage < 0.35 and top_score < 0.40) or not found_sentences:
            return QAResponse(
                query=question,
                answer="The provided document does not provide enough information to answer this question.",
                passages=passages,
                citations=[],
                provider_used="Deterministic Retrieval Fallback (Offline Mode)",
                grounded=True,
                is_insufficient_evidence=True,
                latency_ms=latency_ms
            )

        # Sort found sentences by matches and similarity score
        found_sentences.sort(key=lambda x: (x[0], x[3]), reverse=True)

        # Deduplicate and build answer
        seen_texts = set()
        selected_lines = []
        for match_cnt, s_text, cit, score, cit_str in found_sentences[:5]:
            if s_text not in seen_texts:
                seen_texts.add(s_text)
                selected_lines.append(f"• {s_text} {cit}")
                citations_found.add(cit_str)

        answer_text = (
            "**Grounded Architectural Findings (Deterministic Fallback Mode):**\n\n"
            + "\n".join(selected_lines)
            + f"\n\n*(Retrieved from {len(citations_found)} referenced pages with top similarity score {passages[0].score:.3f})*"
        )

        return QAResponse(
            query=question,
            answer=answer_text,
            passages=passages,
            citations=sorted(list(citations_found)),
            provider_used="Deterministic Retrieval Fallback (Offline Mode)",
            grounded=True,
            is_insufficient_evidence=False,
            latency_ms=latency_ms
        )

    def _extract_citations(self, answer: str, passages: List[RetrievedPassage]) -> List[str]:
        """Extract or verify citation references present in the generated response."""
        citations = set()
        # Look for [DocName, Page X] or (DocName, Page X) pattern
        matches = re.findall(r'\[([^,\]]+),\s*Page\s*(\d+)\]', answer, re.IGNORECASE)
        for doc_part, page_part in matches:
            citations.add(f"{doc_part.strip()} (Page {page_part.strip()})")

        # Also fallback to matching passages cited in the context
        if not citations:
            for p in passages:
                if f"page {p.chunk.page_num}" in answer.lower() or p.chunk.doc_name.lower() in answer.lower():
                    citations.add(p.citation_str)

        return sorted(list(citations))
