'''

Config values such as tinder_color or page_load_wait_time.

'''

# Default Tinder color for CLI coloration.
TINDER_COLOR = 'red'

# Wait times for pages to load before Selenium interacts with loaded elemets.

# Used in SAP interactions where load times are shorter.
SHORT_PAGE_LOAD_WAIT_TIME = 2

# Used when load times are longer such as initial login.
LONG_PAGE_LOAD_WAIT_TIME = 6

# Used when swiping
SWIPE_LOAD_TIME = 1
