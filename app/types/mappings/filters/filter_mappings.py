# PROFILE ACCESSORIES FILTER MAPPINGS
PROFILE_ACCESSORIES_FILTER_MAPPINGS = {
            'name': {'field': 'accessory_name', 'type': 'like'},
            'description': {'field': 'accessory_description', 'type': 'like'},
            'type': {'field': 'profile_accessory_type', 'type': 'exact'},
            'profile_type': {'field': 'profile_type', 'type': 'exact'},
            'bits': {'field': 'bits', 'type': 'number'},
            'ownership': {'field': 'ownership_type', 'type': 'exact'},
            'available': {'field': 'available', 'type': 'exact'},
            'default': {'field': 'default_accessory', 'type': 'exact'},
            'owner_count': {'field': 'owner_count', 'type': 'number'},
            'created_at': {'field': 'created_at', 'type': 'date'}
        }

BLOCKED_USERS_FILTER_MAPPINGS = {
    'username': {
        'field': 'blocked.username',
        'type': 'like'
    },
    'blocked_at': {
        'field': 'blocked_at',
        'type': 'date'
    }
}