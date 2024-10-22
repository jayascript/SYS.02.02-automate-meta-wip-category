import unittest
from datetime import datetime, timedelta
from meta_wip_automation.project_sorter import (
    calculate_priority,
    get_recurrence_score,
    sort_projects,
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


    def test_recurrence_conditions(self):
        """Test all combinations of recurrence parameters."""
        from datetime import datetime, timedelta

        frontmatter = {
            'STATUS': 'active',
            'ACCOUNTABILITY': 'looming',
            'TIME_DISTORTION': 'linear',
            'EFFORT': 'push',
            'INTEREST': 'sparking',
            'URGENCY': 'soon'
        }

        now = datetime.now()

        # Test all combinations:
        # 1. Both None
        score1 = calculate_priority(frontmatter, None, None)

        # 2. Only last_completed provided
        score2 = calculate_priority(frontmatter, now - timedelta(days=5), None)

        # 3. Only interval provided
        score3 = calculate_priority(frontmatter, None, 30)

        # 4. Both provided - use overdue scenario to ensure different score
        score4 = calculate_priority(
            frontmatter,
            now - timedelta(days=31), # More than 30 days ago
            30 # 30 day interval
            )

        # All scores should be valid
        assert score1 >= 0
        assert score2 >= 0
        assert score3 >= 0
        assert score4 >= 0

        # Score4 should be different because it's the only one that
        # should trigger the recurrence calculation
        # Score4 should be higher because it includes recurrence score for overdue
        assert score4 != score1


    def test_avoiding_high_accountability_boost(self):
        """Test the priority boost for avoided tasks with high accountability."""
        frontmatter = {
            'STATUS': 'active',
            'ACCOUNTABILITY': 'imminent', # High accountability (score >=2)
            'TIME_DISTORTION': 'linear',
            'EFFORT': 'push',
            'INTEREST': 'avoiding', # Avoiding (score == 3)
            'URGENCY': 'soon'
        }
        # Trigger avoiding + high accountability boost
        score1 = calculate_priority(frontmatter)

        # Compare with same frontmatter but lower accountability
        frontmatter['ACCOUNTABILITY'] = 'distant'
        score2 = calculate_priority(frontmatter)

        assert score1 > score2 + 3 # Should be higher by at least the boost amount


    def test_sort_projects_basic(self):
        """Test basic project sorting functionality."""
        # project1 score: (5 x 'imminent') + (4 x 'stuck') + (1 x 'now')
        # project1 score: (5 x 3) + (4 x 3) + (1 x 3) = 15 + 12 + 3 = 30
        project1 = ({
            'STATUS': 'stuck',
            'ACCOUNTABILITY': 'imminent',
            'URGENCY': 'now'
        }, None, None)

        # project2 score: (5 x 'distant') + (4 x 'active') + (1 x 'later')
        # project2 score: (5 x 1) + (4 x 1) + (1 x 1) = 5 + 4 + 1 = 10
        project2 = ({
            'STATUS': 'active',
            'ACCOUNTABILITY': 'distant',
            'URGENCY': 'later'
        }, None, None)

        projects = [project2, project1] # Intentionally out of order
        sorted_projects = sort_projects(projects)

        assert sorted_projects[0] == project1 # Higher priority should be first
        assert sorted_projects[1] == project2


if __name__ == '__main__':
    unittest.main()
