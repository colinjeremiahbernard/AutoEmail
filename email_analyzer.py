"""
Advanced email analysis module for categorization, priority scoring, and sentiment analysis.
Enhances AutoEmail with intelligent email processing capabilities.
"""

import re
from typing import Dict, Tuple, Any
from groq import Groq
from config import get_groq_api_key


class EmailAnalyzer:
    """Analyzes emails for category, priority, and sentiment."""
    
    # Email categories
    CATEGORIES = {
        'WORK': ['meeting', 'project', 'deadline', 'report', 'presentation', 'task', 'client'],
        'PERSONAL': ['family', 'friend', 'birthday', 'party', 'vacation', 'weekend'],
        'FINANCIAL': ['invoice', 'payment', 'bill', 'receipt', 'transaction', 'account', 'bank'],
        'MARKETING': ['offer', 'sale', 'discount', 'promotion', 'subscribe', 'unsubscribe', 'newsletter'],
        'URGENT': ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'important'],
        'SOCIAL': ['linkedin', 'facebook', 'twitter', 'instagram', 'notification', 'connection']
    }
    
    # Priority keywords with weights
    PRIORITY_KEYWORDS = {
        'urgent': 10,
        'asap': 10,
        'critical': 9,
        'important': 8,
        'deadline': 7,
        'emergency': 10,
        'immediately': 9,
        'priority': 7,
        'time-sensitive': 8,
        'action required': 8
    }
    
    def __init__(self):
        """Initialize the email analyzer with Groq client."""
        self.client = Groq(api_key=get_groq_api_key())
    
    def categorize_email(self, email_text: str) -> str:
        """
        Categorize email based on content analysis.
        
        Args:
            email_text: The email content to analyze
            
        Returns:
            str: The primary category (WORK, PERSONAL, FINANCIAL, etc.)
        """
        email_lower = email_text.lower()
        category_scores = {}
        
        for category, keywords in self.CATEGORIES.items():
            score = sum(1 for keyword in keywords if keyword in email_lower)
            category_scores[category] = score
        
        # Return category with highest score, default to WORK if no matches
        if max(category_scores.values()) == 0:
            return 'GENERAL'
        
        return max(category_scores, key=category_scores.get)
    
    def calculate_priority_score(self, email_text: str, subject: str = "") -> Tuple[int, str]:
        """
        Calculate priority score (0-100) based on content analysis.
        
        Args:
            email_text: The email content
            subject: The email subject line (optional)
            
        Returns:
            Tuple[int, str]: Priority score and priority level (LOW/MEDIUM/HIGH/CRITICAL)
        """
        combined_text = (subject + " " + email_text).lower()
        score = 0
        
        # Check for priority keywords
        for keyword, weight in self.PRIORITY_KEYWORDS.items():
            if keyword in combined_text:
                score += weight
        
        # Check for question marks (questions often need responses)
        question_count = combined_text.count('?')
        score += min(question_count * 3, 15)
        
        # Check for exclamation marks (urgency indicators)
        exclamation_count = combined_text.count('!')
        score += min(exclamation_count * 2, 10)
        
        # Check for deadline mentions
        if re.search(r'\b(today|tomorrow|this week|by \w+day)\b', combined_text):
            score += 15
        
        # Cap score at 100
        score = min(score, 100)
        
        # Determine priority level
        if score >= 70:
            level = 'CRITICAL'
        elif score >= 50:
            level = 'HIGH'
        elif score >= 25:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        
        return score, level
    
    def analyze_sentiment(self, email_text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of an email using AI.
        
        Args:
            email_text: The email content to analyze
            
        Returns:
            Dict containing sentiment (POSITIVE/NEGATIVE/NEUTRAL) and confidence
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the sentiment of this email. Respond with only one word: POSITIVE, NEGATIVE, or NEUTRAL."
                    },
                    {
                        "role": "user",
                        "content": email_text[:1000]  # Limit to first 1000 chars for efficiency
                    }
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            content = response.choices[0].message.content
            sentiment = content.strip().upper() if content else 'NEUTRAL'
            
            # Validate sentiment
            if sentiment not in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                sentiment = 'NEUTRAL'
            
            return {
                'sentiment': sentiment,
                'confidence': 'HIGH'  # Simplified for now
            }
            
        except Exception as e:
            # Fallback to basic sentiment analysis
            return self._basic_sentiment_analysis(email_text)
    
    def _basic_sentiment_analysis(self, email_text: str) -> Dict[str, Any]:
        """
        Fallback basic sentiment analysis using keyword matching.
        
        Args:
            email_text: The email content
            
        Returns:
            Dict containing sentiment and confidence
        """
        positive_words = ['thank', 'great', 'excellent', 'happy', 'pleased', 'wonderful', 
                         'appreciate', 'good', 'best', 'congratulations', 'success']
        negative_words = ['sorry', 'unfortunately', 'problem', 'issue', 'concern', 'disappointed',
                         'error', 'mistake', 'failed', 'urgent', 'complaint']
        
        email_lower = email_text.lower()
        
        positive_count = sum(1 for word in positive_words if word in email_lower)
        negative_count = sum(1 for word in negative_words if word in email_lower)
        
        if positive_count > negative_count:
            sentiment = 'POSITIVE'
        elif negative_count > positive_count:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'
        
        return {
            'sentiment': sentiment,
            'confidence': 'MEDIUM'
        }
    
    def get_comprehensive_analysis(self, email_text: str, subject: str = "") -> Dict[str, Any]:
        """
        Perform comprehensive email analysis.
        
        Args:
            email_text: The email content
            subject: The email subject line (optional)
            
        Returns:
            Dict containing category, priority, sentiment, and recommendations
        """
        category = self.categorize_email(email_text)
        priority_score, priority_level = self.calculate_priority_score(email_text, subject)
        sentiment_data = self.analyze_sentiment(email_text)
        
        # Generate recommendations
        recommendations = []
        if priority_level in ['CRITICAL', 'HIGH']:
            recommendations.append("⚡ Respond promptly")
        if sentiment_data['sentiment'] == 'NEGATIVE':
            recommendations.append("⚠️ Handle with care - negative sentiment detected")
        if category == 'FINANCIAL':
            recommendations.append("💰 Review financial details carefully")
        
        return {
            'category': category,
            'priority': {
                'score': priority_score,
                'level': priority_level
            },
            'sentiment': sentiment_data,
            'recommendations': recommendations,
            'requires_action': priority_level in ['CRITICAL', 'HIGH']
        }


def analyze_email(email_text: str, subject: str = "") -> Dict[str, Any]:
    """
    Convenience function to analyze an email.
    
    Args:
        email_text: The email content
        subject: The email subject line (optional)
        
    Returns:
        Dict containing comprehensive analysis results
    """
    analyzer = EmailAnalyzer()
    return analyzer.get_comprehensive_analysis(email_text, subject)

# Made with Bob
