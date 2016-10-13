# 使用CORS
如果有架設後端主機的需求，設定檔愛閣加上
```python3
INSTALLED_APPS = +(
    'corsheaders',
)

MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
```
若是愛客製化設定，請看[django-cors-header](https://github.com/ottoyiu/django-cors-headers#setup)
