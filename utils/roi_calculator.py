def calculate_roi(panel_count: int):
    """
    Calculates:
    - Total installation cost (₹)
    - Annual energy generation (kWh)
    - Annual savings (₹)
    - Payback period (years)

    Assumptions:
    • 1 panel = 400 W
    • Installation cost = ₹60 per W
    • Avg sunlight = 4 hours/day
    • Electricity rate = ₹7 per kWh
    """

    panel_power_watts = 400
    cost_per_watt = 60
    electricity_rate_per_kwh = 7
    avg_sunlight_hours_per_day = 4

    # Total system capacity in watts & kilowatts
    total_power_watts = panel_count * panel_power_watts
    total_power_kw = total_power_watts / 1000

    # Installation cost (₹)
    installation_cost = total_power_watts * cost_per_watt

    # Annual generation (kWh) = kW * sunlight hrs/day * 365
    annual_generation = total_power_kw * avg_sunlight_hours_per_day * 365

    # Annual savings (₹)
    annual_savings = annual_generation * electricity_rate_per_kwh

    # Payback period (years)
    if annual_savings > 0:
        payback_years = round(installation_cost / annual_savings, 1)
    else:
        payback_years = float('inf')

    return {
        "installation_cost": int(installation_cost),
        "annual_generation": int(annual_generation),
        "annual_savings": int(annual_savings),
        "payback_years": payback_years
    }
