import unittest
from datetime import datetime, timedelta
from src.project_sorter import (
    calculate_priority,
    get_recurrence_score,
    ACCOUNTABILITY_SCORES,
    STATUS_SCORES,
    TIME_DISTORTION_SCORES,
    EFFORT_SCORES,
    INTEREST_SCORES,
    URGENCY_SCORES
)


class TestProjectSorter(unittest.TestCase):
    """Test suite for the project sorting functionality."""

    def test_score_mappings_exist(self):
        """Test that all score mapping dictionaries are properly defined."""
        self.assertTrue(isinstance(ACCOUNTABILITY_SCORES, dict))
        self.assertTrue(isinstance(STATUS_SCORES, dict))
        self.assertTrue(isinstance(TIME_DISTORTION_SCORES, dict))
        self.assertTrue(isinstance(EFFORT_SCORES, dict))
        self.assertTrue(isinstance(INTEREST_SCORES, dict))
        self.assertTrue(isinstance(URGENCY_SCORES, dict))

    def test_basic_priority_calculation(self):
        """Test priority calculation with minimal frontmatter."""
        frontmatter = {
            'ACCOUNTABILITY': 'imminent',
            'STATUS': 'active',
            'TIME_DISTORTION': 'linear',
            'EFFORT': 'push',
            'INTEREST': 'sparking',
            'URGENCY': 'soon'
        }
        score = calculate_priority(frontmatter)
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)

    def test_missing_frontmatter_fields(self):
        """Test that missing fields default to lowest priority."""
        frontmatter = {'STATUS': 'active'} # Only one field
        score = calculate_priority(frontmatter)
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)

    def test_recurrence_score_calculation(self):
        """Test calculation of recurrence scores."""
        now = datetime.now()
        interval = 7 # days

        # Test overdue case
        last_completed = now - timedelta(days=8)
        score = get_recurrence_score(last_completed, interval)
        self.assertEqual(score, 3) # Overdue

        # Test due soon case
        last_completed = now - timedelta(days=6)
        score = get_recurrence_score(last_completed, interval)
        self.assertEqual(score, 2) # Due soon

        # Test recently completed case
        last_completed = now - timedelta(days=2)
        score = get_recurrence_score(last_completed, interval)
        self.assertEqual(score, 0) # Recently completed

    def test_priority_boost_conditions(self):
        """Test that certain combinations of factors receive priority boost."""
        # Test stuck + imminent accountability boost
        frontmatter_stuck = {
            'ACCOUNTABILITY': 'imminent',
            'STATUS': 'stuck',
            'TIME_DISTORTION': 'linear',
            'EFFORT': 'push',
            'INTEREST': 'sparking',
            'URGENCY': 'soon'
        }
        score_stuck = calculate_priority(frontmatter_stuck)

        # Test same frontmatter without stuck status
        frontmatter_active = frontmatter_stuck.copy()
        frontmatter_active['STATUS'] = 'active'
        score_active = calculate_priority(frontmatter_active)

        self.assertGreater(score_stuck, score_active)

    def test_quick_win_boost(self):
        """Test that quick, hard tasks get appropriate priority boost."""
        # Test quick + hard + avoiding combination
        frontmatter_quick_hard = {
            'ACCOUNTABILITY': 'distant',
            'STATUS': 'active',
            'TIME_DISTORTION': 'blink',
            'EFFORT': 'resist',
            'INTEREST': 'avoiding',
            'URGENCY': 'later'
        }
        score_quick_hard = calculate_priority(frontmatter_quick_hard)

        # Test same frontmatter without the quick win combination
        frontmatter_normal = frontmatter_quick_hard.copy()
        frontmatter_normal['TIME_DISTORTION'] = 'linear'
        score_normal = calculate_priority(frontmatter_normal)

        self.assertGreater(score_quick_hard, score_normal)

    def test_done_status_handling(self):
        """Test that 'done' status results in zero priority."""
        frontmatter = {
            'ACCOUNTABILITY': 'imminent',
            'STATUS': 'done',
            'TIME_DISTORTION': 'blink',
            'EFFORT': 'resist',
            'INTEREST': 'avoiding',
            'URGENCY': 'now',
        }
        score = calculate_priority(frontmatter)
        self.assertEqual(score, 0)


if __name__ == '__main__':
    unittest.main()
