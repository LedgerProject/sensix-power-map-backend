from project.settings.config import cfg

if cfg.get('SENTRY_IO_ENABLED', False):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from pathlib import Path

    release = ''
    release_file_path = 'assets/release.txt'

    if Path(release_file_path).is_file():
        with open(release_file_path) as release_file:
            release = release_file.readline().strip()

    sentry_sdk.init(
        dsn=cfg.get('SENTRY_IO_DSN'),
        release=release,
        environment=cfg.get('ENV_ID'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1
    )
