
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView
from django.shortcuts import render
import os
import shutil
import re


def get_system_metrics():
    cpu_count = os.cpu_count() or 1
    load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
    total, used, free = shutil.disk_usage("/")
    # Try to read memory and cpu percent using psutil if available
    mem_total_gb = None
    mem_used_gb = None
    mem_used_pct = None
    cpu_usage_pct = None
    try:
        import psutil
        vm = psutil.virtual_memory()
        mem_total_gb = round(vm.total / (1024 ** 3), 2)
        mem_used_gb = round((vm.total - vm.available) / (1024 ** 3), 2)
        mem_used_pct = round(vm.percent, 1)
        cpu_usage_pct = round(psutil.cpu_percent(interval=0.1), 1)
    except Exception:
        # Fallback: estimate memory from /proc/meminfo (linux) and cpu from load
        try:
            with open('/proc/meminfo') as f:
                info = f.read()
            def parse_val(key):
                for line in info.splitlines():
                    if line.startswith(key):
                        parts = line.split()
                        return int(parts[1])
                return None
            mem_total_kb = parse_val('MemTotal:')
            mem_available_kb = parse_val('MemAvailable:') or parse_val('MemFree:')
            if mem_total_kb and mem_available_kb is not None:
                mem_total_gb = round(mem_total_kb / 1024.0 / 1024.0, 2)
                mem_used_gb = round((mem_total_kb - mem_available_kb) / 1024.0 / 1024.0, 2)
                mem_used_pct = round(((mem_total_kb - mem_available_kb) / mem_total_kb) * 100, 1)
        except Exception:
            pass
        try:
            # approximate cpu percent from 1m load per core
            load_per_cpu = (load_avg[0] / cpu_count) if cpu_count else 0.0
            cpu_usage_pct = round(min(100.0, load_per_cpu * 100.0), 1)
        except Exception:
            cpu_usage_pct = None
    return {
        "cpu_count": cpu_count,
        "load_average": {
            "1m": round(load_avg[0], 2),
            "5m": round(load_avg[1], 2),
            "15m": round(load_avg[2], 2),
        },
        "load_1m": round(load_avg[0], 2),
        "load_5m": round(load_avg[1], 2),
        "load_15m": round(load_avg[2], 2),
        "disk_total_gb": round(total / (1024 ** 3), 2),
        "disk_used_gb": round(used / (1024 ** 3), 2),
        "disk_free_gb": round(free / (1024 ** 3), 2),
        "memory_total_gb": mem_total_gb,
        "memory_used_gb": mem_used_gb,
        "memory_used_pct": mem_used_pct,
        "cpu_usage_percent": cpu_usage_pct,
    }


def health_view(request):
    system = get_system_metrics()
    # Compute simple health classification from load and disk usage
    try:
        load_1m = float(system["load_average"]["1m"])
    except Exception:
        load_1m = 0.0
    cpu_count = int(system.get("cpu_count") or 1)
    load_per_cpu = load_1m / cpu_count if cpu_count else load_1m

    # disk usage percent
    try:
        used = float(system.get("disk_used_gb", 0.0))
        total = float(system.get("disk_total_gb", 1.0))
        disk_used_pct = (used / total) * 100 if total else 0.0
    except Exception:
        disk_used_pct = 0.0

    # thresholds (tunable)
    # We'll consider cpu_usage_pct and memory_used_pct as well as load and disk
    cpu_pct = None
    mem_pct = None
    try:
        cpu_pct = float(system.get('cpu_usage_percent'))
    except Exception:
        cpu_pct = None
    try:
        mem_pct = float(system.get('memory_used_pct'))
    except Exception:
        mem_pct = None

    # Determine level using multiple signals: cpu_pct, load_per_cpu, mem_pct, disk_used_pct
    level = "Normal"
    # Helper to set to Risk if any critical metric exceeds risk threshold
    def is_risk():
        if cpu_pct is not None and cpu_pct > 90: return True
        if mem_pct is not None and mem_pct > 90: return True
        if load_per_cpu > 1.5: return True
        if disk_used_pct > 90: return True
        return False
    def is_abnormal():
        if cpu_pct is not None and cpu_pct > 70: return True
        if mem_pct is not None and mem_pct > 70: return True
        if load_per_cpu > 0.7: return True
        if disk_used_pct > 70: return True
        return False

    if is_risk():
        level = "Risk"
    elif is_abnormal():
        level = "Abnormal"

    message = "🚀 Server is up and running!"
    if level == "Abnormal":
        message = "⚠️ Server showing elevated resource usage"
    elif level == "Risk":
        message = "🔥 Server under high resource pressure — immediate attention recommended"
    context = {
        "project_name": getattr(settings, "PROJECT_NAME", "unknown"),
        "status": "ok",
        "server_health": level,
        "message": message,
        # plain message without emojis for cleaner display
        "message_plain": re.sub(r"[\U00010000-\U0010ffff]|[\u2600-\u27ff]", "", message).strip(),
        "system": system,
    }
    return render(request, "health.html", context)

schema_view = get_schema_view(
    openapi.Info(
        title="LifeChoice API",
        default_version='v1',
        description="API documentation for LifeChoice Backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', health_view, name='health-check'),
    path('certificates/verify/<str:certificate_number>/', RedirectView.as_view(
        url='/progress/user/certificates/verify/%(certificate_number)s/', permanent=False
    ), name='certificate-verify-redirect'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    
    path('settings/', include('configuration.urls')),   
    
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)