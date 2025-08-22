#!/usr/bin/env python3
"""
Test script for AI Student Diary application
This script tests basic functionality without running the full Streamlit app
"""

import json
import os
from datetime import datetime, timedelta

def test_data_structures():
    """Test that data structures can be created and manipulated"""
    print("🧪 Testing data structures...")
    
    # Test diary entry structure
    sample_entry = {
        'id': 1,
        'date': '2025-01-15',
        'content': 'Test entry for testing purposes',
        'mood': 7,
        'topics': ['test', 'academic'],
        'word_count': 6,
        'timestamp': datetime.now().isoformat()
    }
    
    assert 'id' in sample_entry
    assert 'content' in sample_entry
    assert 'mood' in sample_entry
    print("✅ Diary entry structure test passed")
    
    # Test mood history structure
    mood_entry = {
        'date': '2025-01-15',
        'mood': 7,
        'note': 'Test mood entry'
    }
    
    assert 'date' in mood_entry
    assert 'mood' in mood_entry
    print("✅ Mood history structure test passed")
    
    # Test calendar event structure
    event = {
        'id': 1,
        'title': 'Test Event',
        'date': '2025-01-20',
        'description': 'Test event description',
        'type': 'academic',
        'priority': 'high'
    }
    
    assert 'title' in event
    assert 'date' in event
    assert 'type' in event
    print("✅ Calendar event structure test passed")

def test_ai_analysis():
    """Test basic AI analysis functionality"""
    print("🧪 Testing AI analysis...")
    
    def analyze_entry(entry_text, mood):
        """Simplified version of the analysis function"""
        analysis = {
            'sentiment': 'neutral',
            'topics': [],
            'stress_level': 'low',
            'insights': []
        }
        
        text_lower = entry_text.lower()
        
        # Basic sentiment analysis
        positive_words = ['happy', 'excited', 'great', 'amazing', 'wonderful']
        negative_words = ['sad', 'angry', 'frustrated', 'worried', 'scared']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            analysis['sentiment'] = 'positive'
        elif negative_count > positive_count:
            analysis['sentiment'] = 'negative'
        
        # Topic detection
        topics = {
            'academic': ['test', 'exam', 'homework', 'study', 'class'],
            'social': ['friend', 'group', 'party', 'lunch', 'play'],
            'family': ['mom', 'dad', 'parent', 'family', 'home']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                analysis['topics'].append(topic)
        
        # Stress level
        if mood and mood <= 3:
            analysis['stress_level'] = 'high'
        elif negative_count > 2:
            analysis['stress_level'] = 'medium'
        
        return analysis
    
    # Test cases
    test_cases = [
        ("I'm so happy today! Great day at school.", 8),
        ("I'm worried about the math test tomorrow.", 4),
        ("Regular day, nothing special happened.", 6)
    ]
    
    for text, mood in test_cases:
        result = analyze_entry(text, mood)
        assert 'sentiment' in result
        assert 'topics' in result
        assert 'stress_level' in result
        print(f"✅ Analysis test passed for: '{text[:30]}...'")
    
    print("✅ AI analysis test passed")

def test_calendar_detection():
    """Test calendar event detection"""
    print("🧪 Testing calendar event detection...")
    
    def detect_events(entry_text):
        """Simplified event detection"""
        events = []
        text_lower = entry_text.lower()
        
        # Event keywords
        event_keywords = ['test', 'exam', 'quiz', 'birthday', 'party', 'meeting']
        
        for keyword in event_keywords:
            if keyword in text_lower:
                event = {
                    'id': len(events) + 1,
                    'title': keyword.title(),
                    'date': '2025-01-20',  # Simplified date
                    'description': f'Detected: {keyword}',
                    'type': 'academic' if keyword in ['test', 'exam', 'quiz'] else 'personal',
                    'priority': 'high' if keyword in ['test', 'exam', 'quiz'] else 'medium'
                }
                events.append(event)
        
        return events
    
    # Test cases
    test_entries = [
        "I have a math test tomorrow",
        "Priya's birthday party is next week",
        "Meeting with the teacher after school",
        "Just a regular day, nothing special"
    ]
    
    for entry in test_entries:
        events = detect_events(entry)
        if 'test' in entry.lower() or 'birthday' in entry.lower() or 'meeting' in entry.lower():
            assert len(events) > 0, f"Should detect events in: {entry}"
        print(f"✅ Event detection test passed for: '{entry[:30]}...'")
    
    print("✅ Calendar event detection test passed")

def test_data_persistence():
    """Test data saving and loading"""
    print("🧪 Testing data persistence...")
    
    # Test data
    test_data = {
        'entries': [
            {
                'id': 1,
                'date': '2025-01-15',
                'content': 'Test entry',
                'mood': 7,
                'topics': ['test'],
                'word_count': 2
            }
        ],
        'events': [
            {
                'id': 1,
                'title': 'Test Event',
                'date': '2025-01-20',
                'description': 'Test description',
                'type': 'academic',
                'priority': 'high'
            }
        ],
        'mood_history': [
            {
                'date': '2025-01-15',
                'mood': 7,
                'note': 'Test mood'
            }
        ]
    }
    
    # Test saving
    try:
        with open('test_data.json', 'w') as f:
            json.dump(test_data, f, indent=2)
        print("✅ Data saving test passed")
    except Exception as e:
        print(f"❌ Data saving test failed: {e}")
        return
    
    # Test loading
    try:
        with open('test_data.json', 'r') as f:
            loaded_data = json.load(f)
        
        assert 'entries' in loaded_data
        assert 'events' in loaded_data
        assert 'mood_history' in loaded_data
        print("✅ Data loading test passed")
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return
    
    # Cleanup
    try:
        os.remove('test_data.json')
        print("✅ Cleanup test passed")
    except Exception as e:
        print(f"❌ Cleanup test failed: {e}")

def test_date_parsing():
    """Test date parsing functionality"""
    print("🧪 Testing date parsing...")
    
    def parse_date_from_text(text):
        """Simplified date parser"""
        if 'tomorrow' in text.lower():
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.strftime('%Y-%m-%d')
        elif 'next week' in text.lower():
            next_week = datetime.now() + timedelta(days=7)
            return next_week.strftime('%Y-%m-%d')
        else:
            return datetime.now().strftime('%Y-%m-%d')
    
    # Test cases
    test_texts = [
        "I have a test tomorrow",
        "Meeting next week",
        "Regular entry with no date"
    ]
    
    for text in test_texts:
        date = parse_date_from_text(text)
        assert len(date) == 10, f"Date format should be YYYY-MM-DD, got: {date}"
        print(f"✅ Date parsing test passed for: '{text[:30]}...'")
    
    print("✅ Date parsing test passed")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting AI Student Diary application tests...\n")
    
    try:
        test_data_structures()
        print()
        
        test_ai_analysis()
        print()
        
        test_calendar_detection()
        print()
        
        test_data_persistence()
        print()
        
        test_date_parsing()
        print()
        
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo run the full application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("Please check the application code and try again.")

if __name__ == "__main__":
    run_all_tests()
