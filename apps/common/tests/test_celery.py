from unittest.mock import patch

from django.test import TestCase, override_settings


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_RESULT_BACKEND="cache+memory://",
)
class DebugTaskTest(TestCase):
    def test_debug_task_runs_eagerly(self):
        """debug_task should log its request context and complete with SUCCESS."""
        from core.celery import app, debug_task

        # Use in-memory backend so no Redis connection is required in tests.
        app.conf.result_backend = "cache+memory://"

        with patch("core.celery.logger") as mock_logger:
            result = debug_task.apply()

        self.assertEqual(result.state, "SUCCESS")
        self.assertIsNone(result.result)
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0]
        self.assertIn("Request", call_args[0])
