from dynamic_preferences.registries import global_preferences_registry


def get_monthly_nnm_target(*args, **kwargs):
    global_preferences = global_preferences_registry.manager()
    return global_preferences["wbportfolio__monthly_nnm_target"]
