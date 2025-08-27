"""
Custom middleware to bypass CSRF checks for API endpoints
"""

class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 完全禁用 CSRF 检查
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response 