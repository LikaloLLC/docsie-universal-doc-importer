from django.db import models
from django.utils.translation import gettext_lazy as _


class ConnectorToken(models.Model):
    # Must contain provider id
    provider = models.CharField(
        verbose_name=_('provider'),
        max_length=30,
    )

    token = models.TextField(
        verbose_name=_('token'),
        help_text=_('"oauth_token" (OAuth1) or access token (OAuth2)'),
    )
    token_secret = models.TextField(
        blank=True,
        verbose_name=_('token secret'),
        help_text=_('"oauth_token_secret" (OAuth1) or refresh token (OAuth2)'),
    )
    expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_('expires at')
    )

    def __str__(self):
        return self.token
