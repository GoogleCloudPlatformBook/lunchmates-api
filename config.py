# Configuration

import os

if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    subdomain = 'localhost'
else:
    subdomain = 'lunch--mates\.appspot\.com'