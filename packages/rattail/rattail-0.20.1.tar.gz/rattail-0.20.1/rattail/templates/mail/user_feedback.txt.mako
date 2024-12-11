## -*- coding: utf-8; -*-

# User feedback from website

**User Name**

% if user:
    ${user}
% else:
    ${user_name}
% endif

**Referring URL**

${referrer}

**Client IP**

${client_ip}
% if please_reply_to:

**PLEASE REPLY TO**

${please_reply_to}
% endif

**Message**

${message}
