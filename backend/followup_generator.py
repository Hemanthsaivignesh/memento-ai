"""
Follow-up Question Generator
Generates intelligent, context-aware follow-up questions.
"""

from typing import List, Dict, Optional
from conversation_intelligence import ConversationIntelligence


class FollowupGenerator:
    """
    Generates relevant follow-up questions based on conversation context.
    """
    
    INTENT_FOLLOWUPS = {
        'coding': [
            "Explain this code in more detail",
            "What are the time and space complexity?",
            "Can you optimize this code further?",
            "Add error handling to this code",
            "Show me a different approach",
            "What are the edge cases?"
        ],
        'document_query': [
            "Summarize this document",
            "Find important skills mentioned",
            "Compare with other documents",
            "Extract key insights",
            "What are the main points?",
            "Search for related information"
        ],
        'memory_query': [
            "What did I learn recently?",
            "Show my top memories",
            "What are my key achievements?",
            "What projects have I worked on?",
            "What skills do I have?",
            "What's my experience with X?"
        ],
        'summarization': [
            "What are the main points?",
            "Create a bullet-point summary",
            "What are the key takeaways?",
            "Explain this in simpler terms",
            "What did I miss?",
            "Summarize in one sentence"
        ],
        'comparison': [
            "What are the key differences?",
            "Which one is better for my use case?",
            "Compare them in a table",
            "What are the pros and cons?",
            "When should I use each?"
        ],
        'general': [
            "Tell me more about this",
            "Give me an example",
            "How does this work?",
            "Why is this important?",
            "What should I do next?"
        ]
    }
    
    def __init__(self, conversation_intelligence: ConversationIntelligence):
        self.ci = conversation_intelligence
    
    def generate_followups(
        self,
        user_message: str,
        assistant_response: str,
        intent: str,
        has_documents: bool = False,
        conversation_history: Optional[List[Dict]] = None
    ) -> List[str]:
        """
        Generate relevant follow-up questions.
        
        Args:
            user_message: The user's original message
            assistant_response: The assistant's response
            intent: Detected intent
            has_documents: Whether user has documents
            conversation_history: Recent conversation history
        
        Returns:
            List of follow-up questions
        """
        followups = []
        
        # Get intent-specific follow-ups
        intent_followups = self.INTENT_FOLLOWUPS.get(intent, self.INTENT_FOLLOWUPS['general'])
        followups.extend(intent_followups[:3])
        
        # Add context-aware follow-ups
        if conversation_history:
            contextual = self._generate_contextual_followups(conversation_history, intent)
            followups.extend(contextual[:2])
        
        # Add document-aware follow-ups
        if has_documents:
            doc_followups = [
                "Search for related information in my documents",
                "What else do my documents say about this?",
                "Find more details in my uploaded files"
            ]
            followups.extend(doc_followups[:2])
        
        # Add response-specific follow-ups
        response_followups = self._generate_response_followups(assistant_response)
        followups.extend(response_followups[:2])
        
        # Deduplicate and limit
        unique_followups = list(dict.fromkeys(followups))  # Preserve order, remove duplicates
        return unique_followups[:4]
    
    def _generate_contextual_followups(
        self,
        conversation_history: List[Dict],
        intent: str
    ) -> List[str]:
        """Generate follow-ups based on conversation context."""
        followups = []
        
        # Analyze recent conversation for themes
        recent_topics = []
        for conv in conversation_history[-3:]:
            recent_topics.append(conv['question'].lower())
        
        # Generate based on detected themes
        if any('code' in topic for topic in recent_topics):
            followups.append("Show me more code examples")
        
        if any('document' in topic or 'file' in topic for topic in recent_topics):
            followups.append("What other information is in my documents?")
        
        if any('skill' in topic or 'experience' in topic for topic in recent_topics):
            followups.append("What are my strongest skills?")
        
        if any('project' in topic for topic in recent_topics):
            followups.append("Tell me about another project")
        
        return followups
    
    def _generate_response_followups(self, response: str) -> List[str]:
        """Generate follow-ups based on the response content."""
        followups = []
        response_lower = response.lower()
        
        # Check for code in response
        if '```' in response or 'code' in response_lower:
            followups.append("Explain this code")
        
        # Check for lists/points
        if '-' in response or '*' in response or '•' in response:
            followups.append("Elaborate on these points")
        
        # Check for comparisons
        if 'vs' in response_lower or 'versus' in response_lower or 'compare' in response_lower:
            followups.append("Which one should I choose?")
        
        # Check for explanations
        if 'explain' in response_lower or 'how' in response_lower:
            followups.append("Show me an example")
        
        return followups
    
    def generate_coding_followups(self, code_language: Optional[str] = None) -> List[str]:
        """Generate follow-ups specific to coding questions."""
        base_followups = [
            "Explain this code in detail",
            "What are the time and space complexity?",
            "Can you optimize this further?",
            "Add error handling",
            "Write unit tests for this"
        ]
        
        if code_language:
            language_specific = {
                'python': [
                    "Use list comprehension instead",
                    "Make it more Pythonic",
                    "Add type hints"
                ],
                'javascript': [
                    "Convert to modern ES6+",
                    "Use async/await",
                    "Add error handling with try/catch"
                ],
                'java': [
                    "Use streams instead of loops",
                    "Add proper exception handling",
                    "Use generics"
                ]
            }
            base_followups.extend(language_specific.get(code_language, []))
        
        return base_followups[:4]
    
    def generate_document_followups(self, document_type: Optional[str] = None) -> List[str]:
        """Generate follow-ups specific to document queries."""
        base_followups = [
            "Summarize the key points",
            "Extract important information",
            "Find related sections",
            "What are the main conclusions?"
        ]
        
        if document_type:
            type_specific = {
                'resume': [
                    "What are my key skills?",
                    "Summarize my experience",
                    "What are my achievements?"
                ],
                'research': [
                    "What are the key findings?",
                    "Summarize the methodology",
                    "What are the limitations?"
                ],
                'report': [
                    "What are the recommendations?",
                    "Summarize the executive summary",
                    "What are the action items?"
                ]
            }
            base_followups.extend(type_specific.get(document_type, []))
        
        return base_followups[:4]
