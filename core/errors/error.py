class AppInvokeQuotaExceededError(ValueError):
    """
    Custom exception raised when the quota for an app has been exceeded.
    """

    description = "App Invoke Quota Exceeded"
    