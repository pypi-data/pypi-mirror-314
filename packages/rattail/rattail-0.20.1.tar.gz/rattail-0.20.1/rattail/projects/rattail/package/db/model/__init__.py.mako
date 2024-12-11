## -*- coding: utf-8; mode: python; -*-
# -*- coding: utf-8; -*-
"""
${name} data models
"""

# bring in all of Rattail
from rattail.db.model import *

% if integrates_catapult:
# also bring in Catapult integration models
from rattail_onager.db.model import *
% endif

# TODO: import other/custom models here...
