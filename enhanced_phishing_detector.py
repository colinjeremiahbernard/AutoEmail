"""
Enhanced phishing detection with ML-based scoring and detailed threat analysis.
Provides more sophisticated phishing detection than the basic version.
"""

import re
from typing import Dict, List, Tuple, Any
import tldextract


class EnhancedPhishingDetector:
    """Advanced phishing detection with threat scoring and detailed analysis."""
    
    # Weighted suspicious keywords (keyword: threat_score)
    THREAT_KEYWORDS = {
        'urgent': 8,
        'verify your account': 10,
        'suspended': 9,
        'confirm your identity': 9,
        'update your information': 8,
        'click here immediately': 10,
        'account will be closed': 9,
        'unusual activity': 8,
        'security alert': 7,
        'verify now': 9,
        'act now': 8,
        'limited time': 6,
        'congratulations': 5,
        'you have won': 7,
        'claim your prize': 7,
        'reset your password': 6,
        'confirm payment': 7,
        'refund': 6,
        'tax refund': 8,
        'irs': 7,
        'social security': 8,
        'wire transfer': 7,
        'bitcoin': 6,
        'cryptocurrency': 6
    }
    
    # Trusted domains (whitelist)
    TRUSTED_DOMAINS = [
        'google', 'microsoft', 'amazon', 'apple', 'facebook', 'twitter',
        'linkedin', 'github', 'stackoverflow', 'reddit', 'wikipedia',
        'youtube', 'gmail', 'outlook', 'yahoo', 'dropbox', 'slack'
    ]
    
    # Suspicious TLDs
    SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']
    
    def __init__(self):
        """Initialize the enhanced phishing detector."""
        self.detection_stats = {
            'total_analyzed': 0,
            'phishing_detected': 0,
            'safe_emails': 0
        }
    
    def analyze_urls(self, text: str) -> Tuple[int, List[str]]:
        """
        Analyze URLs in the email for suspicious patterns.
        
        Args:
            text: Email content to analyze
            
        Returns:
            Tuple of (threat_score, list of suspicious URLs)
        """
        urls = re.findall(r'https?://\S+', text)
        threat_score = 0
        suspicious_urls = []
        
        for url in urls:
            url_score = 0
            extracted = tldextract.extract(url)
            domain = extracted.domain
            suffix = extracted.suffix
            
            # Check if domain is trusted
            if domain.lower() not in self.TRUSTED_DOMAINS:
                url_score += 5
                
                # Check for suspicious TLD
                if f'.{suffix}' in self.SUSPICIOUS_TLDS:
                    url_score += 8
                
                # Check for IP address in URL
                if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                    url_score += 10
                
                # Check for excessive subdomains
                subdomain_count = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
                if subdomain_count > 2:
                    url_score += 5
                
                # Check for URL shorteners (often used in phishing)
                shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
                if any(shortener in url.lower() for shortener in shorteners):
                    url_score += 6
                
                if url_score > 5:
                    suspicious_urls.append(url)
                    threat_score += url_score
        
        return threat_score, suspicious_urls
    
    def analyze_content(self, text: str) -> Tuple[int, List[str]]:
        """
        Analyze email content for phishing indicators.
        
        Args:
            text: Email content to analyze
            
        Returns:
            Tuple of (threat_score, list of detected threats)
        """
        text_lower = text.lower()
        threat_score = 0
        detected_threats = []
        
        # Check for threat keywords
        for keyword, score in self.THREAT_KEYWORDS.items():
            if keyword in text_lower:
                threat_score += score
                detected_threats.append(f"Suspicious keyword: '{keyword}'")
        
        # Check for excessive urgency markers
        urgency_markers = text_lower.count('!') + text_lower.count('urgent') * 2
        if urgency_markers > 5:
            threat_score += 10
            detected_threats.append("Excessive urgency indicators")
        
        # Check for requests for personal information
        personal_info_requests = [
            'social security', 'ssn', 'credit card', 'bank account',
            'password', 'pin', 'date of birth', 'mother\'s maiden name'
        ]
        for info_type in personal_info_requests:
            if info_type in text_lower:
                threat_score += 12
                detected_threats.append(f"Requests sensitive info: {info_type}")
        
        # Check for poor grammar/spelling (common in phishing)
        if self._has_poor_grammar(text):
            threat_score += 5
            detected_threats.append("Poor grammar detected")
        
        return threat_score, detected_threats
    
    def _has_poor_grammar(self, text: str) -> bool:
        """
        Basic check for poor grammar indicators.
        
        Args:
            text: Text to analyze
            
        Returns:
            bool: True if poor grammar detected
        """
        # Check for multiple consecutive spaces
        if '  ' in text:
            return True
        
        # Check for missing spaces after punctuation
        if re.search(r'[.!?][a-zA-Z]', text):
            return True
        
        # Check for all caps (common in phishing)
        words = text.split()
        if len(words) > 10:
            caps_ratio = sum(1 for word in words if word.isupper() and len(word) > 2) / len(words)
            if caps_ratio > 0.3:
                return True
        
        return False
    
    def calculate_threat_level(self, threat_score: int) -> str:
        """
        Convert threat score to threat level.
        
        Args:
            threat_score: Numerical threat score
            
        Returns:
            str: Threat level (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
        """
        if threat_score >= 50:
            return 'CRITICAL'
        elif threat_score >= 35:
            return 'HIGH'
        elif threat_score >= 20:
            return 'MEDIUM'
        elif threat_score >= 10:
            return 'LOW'
        else:
            return 'SAFE'
    
    def detect_phishing(self, email_text: str) -> Dict[str, Any]:
        """
        Perform comprehensive phishing detection analysis.
        
        Args:
            email_text: Email content to analyze
            
        Returns:
            Dict containing detailed analysis results
        """
        self.detection_stats['total_analyzed'] += 1
        
        # Analyze URLs
        url_score, suspicious_urls = self.analyze_urls(email_text)
        
        # Analyze content
        content_score, detected_threats = self.analyze_content(email_text)
        
        # Calculate total threat score
        total_score = url_score + content_score
        threat_level = self.calculate_threat_level(total_score)
        
        # Determine if phishing
        is_phishing = threat_level in ['HIGH', 'CRITICAL']
        
        if is_phishing:
            self.detection_stats['phishing_detected'] += 1
        else:
            self.detection_stats['safe_emails'] += 1
        
        return {
            'is_phishing': is_phishing,
            'threat_score': total_score,
            'threat_level': threat_level,
            'url_threat_score': url_score,
            'content_threat_score': content_score,
            'suspicious_urls': suspicious_urls,
            'detected_threats': detected_threats,
            'recommendation': self._get_recommendation(threat_level)
        }
    
    def _get_recommendation(self, threat_level: str) -> str:
        """
        Get recommendation based on threat level.
        
        Args:
            threat_level: The assessed threat level
            
        Returns:
            str: Recommendation for handling the email
        """
        recommendations = {
            'CRITICAL': '🚨 DO NOT INTERACT - Delete immediately and report as phishing',
            'HIGH': '⚠️ LIKELY PHISHING - Do not click links or provide information',
            'MEDIUM': '⚡ SUSPICIOUS - Verify sender authenticity before responding',
            'LOW': '⚠️ CAUTION - Review carefully before taking action',
            'SAFE': '✅ APPEARS SAFE - Standard email processing'
        }
        return recommendations.get(threat_level, 'Review manually')
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get detection statistics.
        
        Returns:
            Dict containing detection statistics
        """
        total = self.detection_stats['total_analyzed']
        if total == 0:
            detection_rate = 0
        else:
            detection_rate = (self.detection_stats['phishing_detected'] / total) * 100
        
        return {
            'total_analyzed': total,
            'phishing_detected': self.detection_stats['phishing_detected'],
            'safe_emails': self.detection_stats['safe_emails'],
            'detection_rate': f"{detection_rate:.1f}%"
        }


# Convenience function
def detect_phishing_enhanced(email_text: str) -> Dict[str, Any]:
    """
    Convenience function for enhanced phishing detection.
    
    Args:
        email_text: Email content to analyze
        
    Returns:
        Dict containing detailed phishing analysis
    """
    detector = EnhancedPhishingDetector()
    return detector.detect_phishing(email_text)

# Made with Bob
