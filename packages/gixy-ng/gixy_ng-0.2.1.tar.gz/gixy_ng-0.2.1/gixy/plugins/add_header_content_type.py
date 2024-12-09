import gixy
from gixy.plugins.plugin import Plugin


class add_header_content_type(Plugin):
    """
    Bad example: add_header Content-Type text/plain;
    Good example: default_type text/plain;
    """
    summary = 'Found add_header usage for setting Content-Type.'
    severity = gixy.severity.LOW
    description = 'Target Content-Type in NGINX should not be set via "add_header"'
    help_url = 'https://github.com/dvershinin/gixy/blob/master/docs/en/plugins/add_header_content_type.md'
    directives = ['add_header']

    def audit(self, directive):
        header_values = get_header_values(directive)
        if directive.header == 'content-type':
            reason = 'You probably want "default_type {default_type};" instead of "add_header" or "more_set_headers"'.format(default_type=header_values[0])
            self.add_issue(
                directive=directive,
                reason=reason
            )


def get_header_values(directive):
    if directive.name == 'add_header':
        return [directive.args[1]]

    # See headers more documentation: https://github.com/openresty/headers-more-nginx-module#description
    result = []
    skip_next = False
    for arg in directive.args:
        if arg in ['-s', '-t']:
            # Skip next value, because it's not a header
            skip_next = True
        elif arg.startswith('-'):
            # Skip any options
            pass
        elif skip_next:
            skip_next = False
        elif not skip_next:
            result.append(arg)
    return result
