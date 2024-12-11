## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${integration_name} config
"""


def auto_upload_product_exports(config):
    """
    Returns boolean indicating whether product exports should be
    automatically uploaded to the ${integration_name} FTP server, when
    they are generated.
    """
    # if main flag is not set, we can safely say no uploads
    if not config.getbool('${pkg_name}', 'product_exports.auto_upload'):
        return False

    # if main flag is set, and we're in production, uploads are good
    if config.production():
        return True

    # but if *not* in production, we require one more flag to enable uploads
    return config.getbool('${pkg_name}', 'product_exports.auto_upload.force',
                          default=False)
