import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key, password, and the current timestamp.
        """
        # Include a timestamp in the hash.
        return f"{user.pk}{user.password}{timestamp}"

    def make_token(self, user):
        """
        Generate a token with a timestamp.
        """
        # The timestamp is the number of seconds since the epoch.
        return self._make_token_with_timestamp(user, int(time.time()), self.secret)

    def check_token(self, user, token):
        """
        Check that the token is valid and has not expired.
        """
        if not (user and token):
            return False

        # Parse the token
        try:
            ts_b36, _ = token.split("-")
            ts = int(ts_b36, 36)
        except ValueError:
            return False

        # Check that the timestamp is within the allowed timeframe (e.g., 10 minutes).
        if (int(time.time()) - ts) > 600:  # 10 minutes in seconds
            return False

        # Check the hash against the user's current state.
        if not super().check_token(user, token):
            return False

        return True


password_reset_token_generator = CustomPasswordResetTokenGenerator()
