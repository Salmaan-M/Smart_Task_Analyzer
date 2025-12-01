from django.test import TestCase
from datetime import datetime, timedelta
from .utils import calculate_priority

class TestPriorityScoring(TestCase):

    def test_overdue_task_is_higher_priority(self):
        now = datetime.now()
        overdue = calculate_priority(
            due_date=now - timedelta(days=1),
            estimated_hours=2,
            importance=5,
            dependencies=[]
        )["score"]

        future = calculate_priority(
            due_date=now + timedelta(days=5),
            estimated_hours=2,
            importance=5,
            dependencies=[]
        )["score"]

        self.assertGreater(overdue, future)

    def test_high_importance_beats_low_importance(self):
        now = datetime.now()
        low = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=3,
            dependencies=[]
        )["score"]

        high = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=9,
            dependencies=[]
        )["score"]

        self.assertGreater(high, low)

    def test_short_tasks_get_effort_bonus(self):
        now = datetime.now()
        long_task = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=8,
            importance=5,
            dependencies=[]
        )["score"]

        short_task = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=1,
            importance=5,
            dependencies=[]
        )["score"]

        self.assertGreater(short_task, long_task)

    def test_dependency_penalty_reduces_score(self):
        now = datetime.now()
        independent = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=5,
            dependencies=[]
        )["score"]

        blocked = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=5,
            dependencies=[1,2]
        )["score"]

        self.assertGreater(independent, blocked)

    def test_circular_dependency_penalized_more(self):
        now = datetime.now()
        normal = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=5,
            dependencies=[2],
            self_id=1,
        )["score"]

        circular = calculate_priority(
            due_date=now + timedelta(days=2),
            estimated_hours=2,
            importance=5,
            dependencies=[1],
            self_id=1,
        )["score"]

        self.assertGreater(normal, circular)
