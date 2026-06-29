"""
Dynamic Prompt Builder
Constructs optimized prompts with context injection for the local LLM.
"""

from typing import Dict, List, Optional
from personality_engine import PersonalityEngine
from conversation_intelligence import ConversationIntelligence


class PromptBuilder:
    """
    Builds dynamic, context-rich prompts for the LLM.
    Injects relevant context, conversation history, and personality.
    """
    
    def __init__(self, personality_engine: PersonalityEngine):
        self.personality = personality_engine
    
    def build_prompt(
        self,
        user_message: str,
        intelligence: Dict,
        retrieved_memories: List[Dict],
        conversation_history: List[Dict],
        user_preferences: Optional[Dict] = None,
        language: str = 'en'
    ) -> str:
        """
        Build a comprehensive prompt with all relevant context.
        """
        prompt_parts = []
        
        # 1. System Prompt with Personality
        system_prompt = self.personality.get_system_prompt(
            language=language,
            context={
                'has_documents': len(retrieved_memories) > 0,
                'previous_conversations': len(conversation_history) > 0,
                'user_preferences': user_preferences or {}
            }
        )
        prompt_parts.append(system_prompt)
        
        # 2. Conversation Summary (if long history)
        if len(conversation_history) > 5:
            summary = self._summarize_conversation(conversation_history)
            prompt_parts.append(f"\n**Conversation Summary:**\n{summary}")
        
        # 3. Recent Conversation History
        if conversation_history:
            recent_history = conversation_history[-3:]  # Last 3 turns
            history_text = self._format_history(recent_history)
            prompt_parts.append(f"\n**Recent Conversation:**\n{history_text}")
        
        # 4. User Preferences & Memory
        if user_preferences:
            pref_text = self._format_preferences(user_preferences)
            prompt_parts.append(f"\n**User Preferences:**\n{pref_text}")
        
        # 5. Retrieved Memories & Documents
        if retrieved_memories:
            memories_text = self._format_memories(retrieved_memories)
            prompt_parts.append(f"\n**Relevant Information from Your Documents:**\n{memories_text}")
        
        # 6. Intent and Context
        intent_info = self._format_intent(intelligence)
        prompt_parts.append(f"\n**Context:**\n{intent_info}")
        
        # 7. Current User Message
        prompt_parts.append(f"\n**User's Question:**\n{intelligence['resolved_message']}")
        
        # 8. Response Instructions
        response_instructions = self._get_response_instructions(
            intelligence['intent'],
            language
        )
        prompt_parts.append(f"\n**Instructions:**\n{response_instructions}")
        
        # 9. Formatting Guidelines
        formatting_guide = self._get_formatting_guide(intelligence['intent'])
        prompt_parts.append(f"\n**Formatting Guidelines:**\n{formatting_guide}")
        
        # Combine all parts
        full_prompt = '\n'.join(prompt_parts)
        
        # Optimize for local model
        return self._optimize_prompt(full_prompt)
    
    def _summarize_conversation(self, history: List[Dict]) -> str:
        """Summarize longer conversation history."""
        if not history:
            return ""
        
        topics = []
        for conv in history[:5]:  # First 5 exchanges
            topics.append(conv['question'][:50] + "...")
        
        return f"Previous conversation covered {len(history)} exchanges about topics including: {', '.join(topics)}"
    
    def _format_history(self, history: List[Dict]) -> str:
        """Format conversation history for the prompt."""
        formatted = []
        for i, conv in enumerate(history, 1):
            formatted.append(f"{i}. User: {conv['question']}")
            formatted.append(f"   Assistant: {conv['answer'][:200]}{'...' if len(conv['answer']) > 200 else ''}")
        return '\n'.join(formatted)
    
    def _format_preferences(self, preferences: Dict) -> str:
        """Format user preferences."""
        items = []
        for key, value in preferences.items():
            items.append(f"- {key}: {value}")
        return '\n'.join(items) if items else "No specific preferences set."
    
    def _format_memories(self, memories: List[Dict]) -> str:
        """Format retrieved memories with source attribution."""
        formatted = []
        
        for i, memory in enumerate(memories, 1):
            source = memory.get('source_file', 'Unknown')
            title = memory.get('title', 'Untitled')
            content = memory.get('content', '')[:500]
            score = memory.get('relevance_score', 0)
            
            formatted.append(f"\n{i}. **{title}** (from {source}) [Relevance: {score:.2f}]")
            formatted.append(f"   {content}{'...' if len(content) >= 500 else ''}")
        
        return '\n'.join(formatted)
    
    def _format_intent(self, intelligence: Dict) -> str:
        """Format detected intent and context."""
        parts = []
        parts.append(f"- Intent: {intelligence['intent']}")
        parts.append(f"- Follow-up question: {'Yes' if intelligence['is_follow_up'] else 'No'}")
        
        if intelligence['entities']:
            parts.append(f"- Detected entities: {', '.join(intelligence['entities'].keys())}")
        
        return '\n'.join(parts)
    
    def _get_response_instructions(self, intent: str, language: str) -> str:
        """Get specific instructions based on intent."""
        base = f"Provide a helpful, accurate response in {language.upper()}."
        
        intent_instructions = {
            'coding': "Structure your response with: 1) Explanation, 2) Approach, 3) Code, 4) Code explanation, 5) Complexity analysis, 6) Best practices.",
            'summarization': "Provide a clear, structured summary with key points and takeaways.",
            'comparison': "Use a comparison table or structured list to highlight differences.",
            'document_query': "Cite the specific documents you're referencing. Be precise about what information comes from where.",
            'memory_query': "Retrieve and present relevant memories in a clear, organized manner.",
            'question': "Answer directly and thoroughly. If uncertain, acknowledge limitations.",
            'general': "Be helpful and conversational. Adapt your response style to the question."
        }
        
        specific = intent_instructions.get(intent, intent_instructions['general'])
        return f"{base}\n{specific}"
    
    def _get_formatting_guide(self, intent: str) -> str:
        """Get formatting guidelines based on intent."""
        guide = """Use Markdown formatting to enhance readability:
- Use headings (# ## ###) for structure
- Use bullet points and numbered lists for clarity
- Use code blocks with syntax highlighting for code
- Use tables for comparisons and structured data
- Use blockquotes (> ) for important notes
- Use bold (**text**) and emphasis (*text*) sparingly
- Keep paragraphs concise and focused"""
        
        if intent == 'coding':
            guide += """
For coding questions specifically:
- Always include a complete, runnable code example
- Add comments explaining key parts
- Mention time and space complexity
- Suggest potential improvements or edge cases"""
        
        return guide
    
    def _optimize_prompt(self, prompt: str) -> str:
        """Optimize prompt for local model inference."""
        # Remove excessive whitespace
        prompt = '\n'.join(line for line in prompt.split('\n') if line.strip())
        
        # Ensure prompt isn't too long for the model
        # Approximate token count (rough estimate: 4 chars per token)
        max_chars = 4000  # ~1000 tokens for context window
        if len(prompt) > max_chars:
            # Truncate less critical parts first
            lines = prompt.split('\n')
            critical_lines = []
            optional_lines = []
            
            in_optional = False
            for line in lines:
                if line.startswith('**Relevant Information'):
                    in_optional = True
                if line.startswith('**User\'s Question'):
                    in_optional = False
                    critical_lines.append(line)
                    continue
                
                if in_optional:
                    optional_lines.append(line)
                else:
                    critical_lines.append(line)
            
            # Trim optional section if needed
            if len('\n'.join(critical_lines)) > max_chars * 0.7:
                # Keep only most relevant memories
                critical_lines = critical_lines[:int(len(critical_lines) * 0.8)]
            
            prompt = '\n'.join(critical_lines)
        
        return prompt
    
    def build_coding_prompt(
        self,
        user_message: str,
        intelligence: Dict,
        conversation_history: List[Dict],
        language: str = 'en'
    ) -> str:
        """
        Build a specialized prompt for coding questions.
        """
        prompt_parts = []
        
        # System prompt for coding
        system_prompt = f"""You are an expert coding assistant. Help the user with programming questions by providing:

1. **Clear Explanation** - Explain the problem and solution approach
2. **Approach** - Describe the algorithm or method you'll use
3. **Complete Code** - Provide runnable, well-commented code
4. **Code Explanation** - Walk through key parts of the implementation
5. **Complexity Analysis** - Time and space complexity
6. **Best Practices** - Mention relevant patterns, edge cases, improvements

Respond in {language.upper()}. Use proper code blocks with syntax highlighting."""
        
        prompt_parts.append(system_prompt)
        
        # Add context if available
        if conversation_history:
            recent = conversation_history[-2:]
            history = self._format_history(recent)
            prompt_parts.append(f"\n**Recent Context:**\n{history}")
        
        # User's question
        prompt_parts.append(f"\n**Coding Question:**\n{intelligence['resolved_message']}")
        
        return '\n'.join(prompt_parts)
    
    def build_summarization_prompt(
        self,
        user_message: str,
        content_to_summarize: str,
        language: str = 'en'
    ) -> str:
        """
        Build a specialized prompt for summarization tasks.
        """
        return f"""You are a skilled summarizer. Create a clear, well-structured summary of the following content in {language.upper()}.

**Content to Summarize:**
{content_to_summarize}

**User's Specific Request:**
{user_message}

Provide:
1. A concise executive summary (2-3 sentences)
2. Key points (bullet list)
3. Important details or takeaways
4. Any notable patterns or insights

Use Markdown formatting with headings and lists for clarity."""
    
    def build_followup_prompt(
        self,
        user_message: str,
        previous_answer: str,
        intelligence: Dict,
        language: str = 'en'
    ) -> str:
        """
        Build a prompt for follow-up questions that maintains context.
        """
        return f"""This is a follow-up question in an ongoing conversation.

**Previous Answer:**
{previous_answer[:500]}...

**Follow-up Question:**
{intelligence['resolved_message']}

**Context:**
- Intent: {intelligence['intent']}
- This is a continuation of the previous topic

Provide a response that naturally builds on the previous answer while addressing the new question. Maintain consistency with what was said before. Respond in {language.upper()}."""


class ProgressivePromptBuilder:
    """
    Builds prompts progressively for streaming responses.
    Allows for context injection at different stages.
    """
    
    def __init__(self, base_builder: PromptBuilder):
        self.base_builder = base_builder
    
    def build_initial_prompt(
        self,
        user_message: str,
        intelligence: Dict,
        language: str = 'en'
    ) -> str:
        """Build the initial prompt without full context."""
        system_prompt = self.base_builder.personality.get_system_prompt(language=language)
        return f"""{system_prompt}

**User's Question:**
{intelligence['resolved_message']}

Begin your response naturally and conversationally."""
    
    def build_context_injection_prompt(
        self,
        context: str,
        sources: List[str]
    ) -> str:
        """Build a prompt for injecting additional context."""
        sources_text = '\n'.join(f"- {s}" for s in sources)
        return f"""**Additional Context Retrieved:**
{context}

**Sources:**
{sources_text}

Continue your response incorporating this information naturally."""
