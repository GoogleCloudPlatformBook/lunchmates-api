# Configuration

import os

if os.getenv('SERVER_SOFTWARE', '!Dev').startswith('Dev'):
    subdomain = 'localhost'
else:
    subdomain = 'lunch--mates\.appspot\.com'