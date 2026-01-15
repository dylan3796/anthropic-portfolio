"""
Sample data for portfolio visualizations.
Demonstrates attribution model concepts from the Attribution MVP project.
"""

import pandas as pd

# Sample partner attribution data
PARTNER_DATA = pd.DataFrame({
    'partner_name': ['Acme Consulting', 'DataTech SI', 'Cloud Partners', 'Integration Pro', 'Analytics Corp'],
    'attributed_amount': [245000, 189000, 156000, 98000, 72000],
    'deals_influenced': [12, 8, 10, 5, 4],
    'avg_deal_size': [20417, 23625, 15600, 19600, 18000]
})

# Sample deal for attribution model comparison
SAMPLE_DEAL = {
    'deal_name': 'Enterprise Analytics Platform',
    'deal_value': 150000,
    'touchpoints': [
        {'partner': 'Acme Consulting', 'type': 'Referral', 'days_before_close': 90},
        {'partner': 'DataTech SI', 'type': 'Implementation', 'days_before_close': 45},
        {'partner': 'Cloud Partners', 'type': 'Influence', 'days_before_close': 30},
        {'partner': 'Integration Pro', 'type': 'Technical Demo', 'days_before_close': 14},
    ]
}

# Attribution model results for the sample deal
ATTRIBUTION_MODELS = {
    'Equal Split': {
        'description': 'Each partner receives equal credit regardless of contribution type or timing.',
        'results': {
            'Acme Consulting': 37500,
            'DataTech SI': 37500,
            'Cloud Partners': 37500,
            'Integration Pro': 37500
        }
    },
    'Role-Weighted': {
        'description': 'Partners weighted by their role type. Implementation partners get higher attribution.',
        'results': {
            'Acme Consulting': 22500,  # Referral: 15%
            'DataTech SI': 60000,      # Implementation: 40%
            'Cloud Partners': 22500,   # Influence: 15%
            'Integration Pro': 45000   # Technical: 30%
        }
    },
    'Time Decay': {
        'description': 'Recent touchpoints weighted more heavily. Activities closer to close get more credit.',
        'results': {
            'Acme Consulting': 15000,  # 90 days out: 10%
            'DataTech SI': 37500,      # 45 days out: 25%
            'Cloud Partners': 45000,   # 30 days out: 30%
            'Integration Pro': 52500   # 14 days out: 35%
        }
    },
    'First Touch': {
        'description': '100% credit to the partner who initiated the relationship.',
        'results': {
            'Acme Consulting': 150000,
            'DataTech SI': 0,
            'Cloud Partners': 0,
            'Integration Pro': 0
        }
    },
    'Last Touch': {
        'description': '100% credit to the most recent partner interaction before close.',
        'results': {
            'Acme Consulting': 0,
            'DataTech SI': 0,
            'Cloud Partners': 0,
            'Integration Pro': 150000
        }
    },
    'U-Shaped': {
        'description': 'Heavy weight on first and last touch (40% each), remaining 20% distributed to middle.',
        'results': {
            'Acme Consulting': 60000,  # First: 40%
            'DataTech SI': 15000,      # Middle: 10%
            'Cloud Partners': 15000,   # Middle: 10%
            'Integration Pro': 60000   # Last: 40%
        }
    }
}

# Revenue over time (monthly aggregated)
REVENUE_TIMELINE = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'partner_attributed': [125000, 145000, 168000, 192000, 215000, 248000, 276000, 312000, 358000, 402000, 445000, 498000],
    'direct': [89000, 102000, 118000, 135000, 152000, 174000, 195000, 220000, 252000, 283000, 312000, 350000]
})

# Project metrics for portfolio display
PROJECT_METRICS = {
    'lines_of_code': 18500,
    'attribution_models': 8,
    'customer_segments': 3,
    'database_tables': 15,
    'test_modules': 6,
    'integrations': ['Salesforce', 'PostgreSQL', 'OpenAI']
}
