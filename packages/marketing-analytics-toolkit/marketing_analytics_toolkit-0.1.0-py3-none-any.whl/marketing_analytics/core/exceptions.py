class MarketingAnalyticsError(Exception):
    """Temel hata sınıfı"""
    def __init__(self, message: str = None, code: str = None):
        self.message = message or "An error occurred in Marketing Analytics"
        self.code = code
        super().__init__(self.message)
        
class ModelNotFittedError(MarketingAnalyticsError):
    """Model eğitilmemiş hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Model must be fitted before making predictions",
            code="MODEL_NOT_FITTED"
        )
        
class ValidationError(MarketingAnalyticsError):
    """Doğrulama hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Validation failed",
            code="VALIDATION_ERROR"
        )
        
class ConfigurationError(MarketingAnalyticsError):
    """Konfigürasyon hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Invalid configuration",
            code="CONFIG_ERROR"
        )
        
class DataQualityError(MarketingAnalyticsError):
    """Veri kalitesi hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Data quality check failed",
            code="DATA_QUALITY_ERROR"
        )
        
class PerformanceError(MarketingAnalyticsError):
    """Performans hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Performance threshold not met",
            code="PERFORMANCE_ERROR"
        )
        
class ResourceError(MarketingAnalyticsError):
    """Kaynak hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Resource limit exceeded",
            code="RESOURCE_ERROR"
        )
        
class TimeoutError(MarketingAnalyticsError):
    """Zaman aşımı hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Operation timed out",
            code="TIMEOUT_ERROR"
        )
        
class InputError(MarketingAnalyticsError):
    """Girdi hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Invalid input",
            code="INPUT_ERROR"
        )
        
class OutputError(MarketingAnalyticsError):
    """Çıktı hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Invalid output",
            code="OUTPUT_ERROR"
        )
        
class DependencyError(MarketingAnalyticsError):
    """Bağımlılık hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Missing or incompatible dependency",
            code="DEPENDENCY_ERROR"
        )
        
class StateError(MarketingAnalyticsError):
    """Durum hatası"""
    def __init__(self, message: str = None):
        super().__init__(
            message or "Invalid state",
            code="STATE_ERROR"
        ) 