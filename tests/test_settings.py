from django import get_version


def test_django_version():
    min_ver = '3.2.16'
    used_ver = get_version()
    assert used_ver >= min_ver, (
        f'В проекте должна быть установлена версия Django '
        f'не менее {min_ver}. У вас Django версии {used_ver}')


def test_static_dir(settings_app_name, project_dirname):
    settings_app = __import__(f'{settings_app_name}', globals(), locals())
    try:
        staticfiles_dirs = settings_app.settings.STATICFILES_DIRS
    except Exception as e:
        raise AssertionError(
            'Убедитесь, что в файле settings.py установлена переменная '
            '`STATICFILES_DIRS`.'
        ) from e
    assert isinstance(staticfiles_dirs, list), (
        'Убедитесь, что значение переменной `STATICFILES_DIRS` в файле '
        'settings.py - список.'
    )


def test_apps_registered(settings_app_name, project_dirname):
    register_apps_old_style = ['blog', 'pages']
    register_apps_new_style = [
        'blog.apps.BlogConfig', 'pages.apps.PagesConfig']
    settings_app = __import__(f'{settings_app_name}')
    installed_apps = settings_app.settings.INSTALLED_APPS
    registered = set(installed_apps)
    app_names = ' и '.join(f'`{n}`' for n in register_apps_old_style)
    assert set(register_apps_new_style).issubset(registered) or (
        set(register_apps_old_style).issubset(registered)
    ), (
        f'Убедитесь, что приложения {app_names} зарегистрированы в файле '
        'settings.py'
    )
