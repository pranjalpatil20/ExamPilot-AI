from services.dashboard_service import dashboard_stats

def get_stats():
    data = dashboard_stats()
    return data