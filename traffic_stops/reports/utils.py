"""
reusable functions
for running reports
"""

def get_rate(num,den):
    if den:
        return round(float(num)/den,2)
