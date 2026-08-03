from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

FIVE_MINUTES = 5 * 60  # 300 seconds


class LoginUserThrottle(UserRateThrottle):
    scope = 'login_user'
    rate = "5/min"  # num_requests parsed; duration overridden below

    def parse_rate(self, rate):
        return (5, FIVE_MINUTES)


class LoginAnonThrottle(AnonRateThrottle):
    scope = 'login_anon'

    def parse_rate(self, rate):
        return (5, FIVE_MINUTES)


class SignupUserThrottle(UserRateThrottle):
    scope = 'signup_user'

    def parse_rate(self, rate):
        return (5, FIVE_MINUTES)


class SignupAnonThrottle(AnonRateThrottle):
    scope = 'signup_anon'

    def parse_rate(self, rate):
        return (5, FIVE_MINUTES)
        
# OTP throttle - 10 attempts per hour
class OTPThrottle(AnonRateThrottle):
    scope = 'otp'
    rate = "10/hour"

# Password reset throttle - 5 attempts per hour
class PasswordResetThrottle(AnonRateThrottle):
    scope = 'password_reset'
    rate = "10/hour"

# Social auth throttle - 10 attempts per hour
class SocialAuthThrottle(AnonRateThrottle):
    scope = 'social_auth'
    rate = "5/min"
