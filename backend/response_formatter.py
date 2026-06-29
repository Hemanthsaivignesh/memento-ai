"""
Response Formatter Module
Handles ChatGPT-style response formatting with Markdown, tables, code blocks, etc.
"""

from typing import Dict, List, Optional
import re


class ResponseFormatter:
    """
    Formats AI responses with ChatGPT-style markdown and structure.
    """
    
    @staticmethod
    def format_markdown(text: str) -> str:
        """
        Ensure proper Markdown formatting in the response.
        """
        # Ensure code blocks have language specification
        text = re.sub(r'```(?!\w)', '```text', text)
        
        # Ensure proper heading spacing
        text = re.sub(r'([^\n])#', r'\1\n#', text)
        
        # Ensure list items are properly formatted
        text = re.sub(r'(?<!\n)-', '\n-', text)
        
        # Ensure numbered lists have proper spacing
        text = re.sub(r'(?<!\n)\d+\.', '\n\\0', text)
        
        return text
    
    @staticmethod
    def add_structure(text: str, intent: str) -> str:
        """
        Add structural elements based on intent.
        """
        if intent == 'coding':
            return ResponseFormatter._add_coding_structure(text)
        elif intent == 'summarization':
            return ResponseFormatter._add_summary_structure(text)
        elif intent == 'comparison':
            return ResponseFormatter._add_comparison_structure(text)
        
        return text
    
    @staticmethod
    def _add_coding_structure(text: str) -> str:
        """Add structure for coding responses."""
        # Check if response already has structure
        if any(marker in text for marker in ['## Explanation', '## Approach', '## Code']):
            return text
        
        # Try to add structure if not present
        lines = text.split('\n')
        structured = []
        current_section = None
        
        for line in lines:
            # Detect code blocks
            if '```' in line:
                if current_section != 'code':
                    structured.append('## Code')
                    current_section = 'code'
                structured.append(line)
            elif line.strip().startswith(('def ', 'class ', 'import ', 'from ')):
                if current_section != 'code':
                    structured.append('## Code')
                    current_section = 'code'
                structured.append(line)
            elif any(word in line.lower() for word in ['explain', 'approach', 'algorithm', 'method']):
                if current_section != 'explanation':
                    structured.append('## Explanation')
                    current_section = 'explanation'
                structured.append(line)
            else:
                structured.append(line)
        
        return '\n'.join(structured)
    
    @staticmethod
    def _add_summary_structure(text: str) -> str:
        """Add structure for summary responses."""
        if '##' in text:
            return text  # Already has structure
        
        lines = text.split('\n')
        structured = ['## Summary']
        
        for line in lines:
            if line.strip().startswith(('-', '*', '•')):
                if '## Key Points' not in '\n'.join(structured):
                    structured.append('## Key Points')
                structured.append(line)
            else:
                structured.append(line)
        
        return '\n'.join(structured)
    
    @staticmethod
    def _add_comparison_structure(text: str) -> str:
        """Add structure for comparison responses."""
        if '|' in text and '##' not in text:
            # Has table but no heading
            return f"## Comparison\n\n{text}"
        return text
    
    @staticmethod
    def add_source_attribution(text: str, sources: List[Dict]) -> str:
        """
        Add source attribution for document-based answers.
        """
        if not sources:
            return text
        
        attribution = "\n\n---\n\n**Sources:**\n"
        for i, source in enumerate(sources, 1):
            doc_name = source.get('document', 'Unknown')
            memory_name = source.get('memory', 'Unknown')
            attribution += f"{i}. {doc_name} - {memory_name}\n"
        
        return text + attribution
    
    @staticmethod
    def add_followup_suggestions(text: str, suggestions: List[str]) -> str:
        """
        Add follow-up question suggestions.
        """
        if not suggestions:
            return text
        
        followup = "\n\n---\n\n**You might also ask:**\n"
        for i, suggestion in enumerate(suggestions, 1):
            followup += f"{i}. {suggestion}\n"
        
        return text + followup
    
    @staticmethod
    def ensure_readability(text: str) -> str:
        """
        Ensure the response is readable and well-formatted.
        """
        # Break up very long paragraphs
        paragraphs = text.split('\n\n')
        formatted = []
        
        for para in paragraphs:
            if len(para) > 500 and '\n' not in para:
                # Break long paragraph
                sentences = re.split(r'(?<=[.!?])\s+', para)
                chunks = []
                current_chunk = []
                current_length = 0
                
                for sentence in sentences:
                    if current_length + len(sentence) > 300:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = [sentence]
                        current_length = len(sentence)
                    else:
                        current_chunk.append(sentence)
                        current_length += len(sentence)
                
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                
                formatted.extend(chunks)
            else:
                formatted.append(para)
        
        return '\n\n'.join(formatted)
    
    @staticmethod
    def add_key_takeaways(text: str) -> str:
        """
        Add key takeaways section if appropriate.
        """
        # Check if response is informational
        if len(text) > 500 and '##' not in text:
            # Add key takeaways for longer responses
            return text + "\n\n**Key Takeaways:**\n- [Response summary points would be added here by the LLM]"
        
        return text


class FollowupGenerator:
    """
    Generates intelligent follow-up questions based on context.
    """
    
    @staticmethod
    def generate_followups(
        user_message: str,
        assistant_response: str,
        intent: str,
        has_documents: bool
    ) -> List[str]:
        """
        Generate relevant follow-up questions.
        """
        followups = []
        
        # Intent-specific follow-ups
        if intent == 'coding':
            followups.extend([
                "Explain this code in more detail",
                "What are the time and space complexity?",
                "Can you optimize this code further?",
                "Add error handling to this code"
            ])
        elif intent == 'document_query':
            followups.extend([
                "Summarize this document",
                "Find important skills mentioned",
                "Compare with other documents",
                "Extract key insights"
            ])
        elif intent == 'memory_query':
            followups.extend([
                "What did I learn recently?",
                "Show my top memories",
                "What are my key achievements?",
                "What projects have I worked on?"
            ])
        elif intent == 'summarization':
            followups.extend([
                "What are the main points?",
                "Create a bullet-point summary",
                "What are the key takeaways?",
                "Explain this in simpler terms"
            ])
        
        # Context-aware follow-ups
        if has_documents:
            followups.extend([
                "Search for related information",
                "Find more details in my documents",
                "What else do my documents say about this?"
            ])
        
        # Generic follow-ups
        followups.extend([
            "Tell me more about this",
            "Give me an example",
            "How does this work?"
        ])
        
        # Return top 3-4 most relevant
        return followups[:4]
    
    @staticmethod
    def generate_contextual_followups(
        conversation_history: List[Dict],
        current_topic: str
    ) -> List[str]:
        """
        Generate follow-ups based on conversation context.
        """
        followups = []
        
        # Analyze recent conversation for themes
        recent_topics = []
        for conv in conversation_history[-3:]:
            recent_topics.append(conv['question'].lower())
        
        # Generate follow-ups based on detected themes
        if any('code' in topic for topic in recent_topics):
            followups.append("Show me more code examples")
        
        if any('document' in topic or 'file' in topic for topic in recent_topics):
            followups.append("What other information is in my documents?")
        
        if any('skill' in topic or 'experience' in topic for topic in recent_topics):
            followups.append("What are my strongest skills?")
        
        return followups[:3]
