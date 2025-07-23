import re
import logging
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from app.models.entities import ActionItem
from app.core.exceptions import NLPProcessingError

logger = logging.getLogger(__name__)


class NLPService:
    """Handles NLP processing for action item extraction"""
    
    def __init__(self):
        self._ner_pipeline = None
        self.action_keywords = [
            "need to", "should", "must", "will", "todo", "action item",
            "follow up", "reach out", "contact", "schedule", "deliver",
            "complete", "finish", "submit", "send", "prepare", "review",
            "update", "create", "develop", "implement", "investigate",
            "assign", "responsible", "deadline", "due", "by"
        ]
        
        self.date_patterns = [
            r'\b(?:by|before|until|due)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(?:by|before|until|due)\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}\b',
            r'\b(?:by|before|until|due)\s+\d{1,2}\/\d{1,2}(?:\/\d{2,4})?\b',
            r'\b(?:by|before|until|due)\s+(?:today|tomorrow|next week|this week|end of week|eod|end of day)\b',
            r'\bnext\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\bthis\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(?:in|within)\s+\d+\s+(?:days?|weeks?|months?)\b'
        ]
    
    @property
    def ner_pipeline(self):
        """Lazy load NER pipeline"""
        if self._ner_pipeline is None:
            logger.info("Loading NER model...")
            try:
                tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
                model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
                self._ner_pipeline = pipeline(
                    "ner",
                    model=model,
                    tokenizer=tokenizer,
                    aggregation_strategy="simple"
                )
                logger.info("NER model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load NER model: {e}")
                raise NLPProcessingError(f"Failed to load NER model: {str(e)}")
        return self._ner_pipeline
    
    def extract_sentences_with_keywords(self, text: str, custom_keywords: Optional[List[str]] = None) -> List[str]:
        """Extract sentences containing action-oriented keywords"""
        keywords = self.action_keywords.copy()
        if custom_keywords:
            keywords.extend(custom_keywords)
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        action_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # Filter very short sentences
                sentence_lower = sentence.lower()
                if any(keyword in sentence_lower for keyword in keywords):
                    action_sentences.append(sentence)
        
        return action_sentences
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text"""
        try:
            entities = self.ner_pipeline(text)
            return entities
        except Exception as e:
            logger.warning(f"Entity extraction failed for text: {text[:50]}... Error: {e}")
            return []
    
    def extract_deadlines(self, text: str) -> List[str]:
        """Extract potential deadlines from text"""
        deadlines = []
        text_lower = text.lower()
        
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                deadline = match.group().strip()
                if deadline not in deadlines:
                    deadlines.append(deadline)
        
        return deadlines
    
    def determine_priority(self, text: str) -> str:
        """Determine priority based on keywords in text"""
        text_lower = text.lower()
        
        high_priority_keywords = ["urgent", "asap", "immediately", "critical", "important", "high priority"]
        low_priority_keywords = ["when possible", "eventually", "sometime", "low priority", "nice to have"]
        
        if any(keyword in text_lower for keyword in high_priority_keywords):
            return "high"
        elif any(keyword in text_lower for keyword in low_priority_keywords):
            return "low"
        else:
            return "medium"
    
    def extract_action_items(self, transcript_text: str, custom_keywords: Optional[List[str]] = None) -> List[ActionItem]:
        """Extract action items from transcript text"""
        logger.info("Extracting action items from transcript...")
        
        try:
            # Get sentences with action keywords
            action_sentences = self.extract_sentences_with_keywords(transcript_text, custom_keywords)
            logger.info(f"Found {len(action_sentences)} potential action sentences")
            
            action_items = []
            
            for i, sentence in enumerate(action_sentences):
                # Extract entities from the sentence
                entities = self.extract_entities(sentence)
                
                # Extract potential assignees (persons)
                assignees = [ent['word'] for ent in entities if ent['entity_group'] == 'PER']
                
                # Extract potential deadlines
                deadlines = self.extract_deadlines(sentence)
                
                # Determine priority
                priority = self.determine_priority(sentence)
                
                # Calculate confidence score
                confidence = sum([ent['score'] for ent in entities]) / len(entities) if entities else 0.5
                
                action_item = ActionItem(
                    id=i + 1,
                    task=sentence.strip(),
                    assignees=assignees if assignees else ["unspecified"],
                    deadlines=deadlines if deadlines else ["not specified"],
                    priority=priority,
                    confidence=round(confidence, 2),
                    entities_found=entities
                )
                
                action_items.append(action_item)
            
            logger.info(f"Extracted {len(action_items)} action items")
            return action_items
            
        except Exception as e:
            logger.error(f"Action item extraction failed: {e}")
            raise NLPProcessingError(f"Action item extraction failed: {str(e)}")

