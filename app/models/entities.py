from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class ActionItem:
    """Action item entity"""
    id: int
    task: str
    assignees: List[str]
    deadlines: List[str]
    priority: str
    confidence: float
    entities_found: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'task': self.task,
            'assignees': self.assignees,
            'deadlines': self.deadlines,
            'priority': self.priority,
            'confidence': self.confidence,
            'entities_found': self.entities_found
        }


@dataclass
class TranscriptionSegment:
    """Transcription segment entity"""
    id: int
    start: float
    end: float
    text: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'text': self.text
        }


@dataclass
class MeetingAnalysis:
    """Complete meeting analysis result"""
    metadata: Dict[str, Any]
    transcript: Dict[str, Any]
    action_items: List[ActionItem]
    summary: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'metadata': self.metadata,
            'transcript': self.transcript,
            'action_items': [item.to_dict() for item in self.action_items],
            'summary': self.summary
        }
