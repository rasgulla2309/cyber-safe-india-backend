def calculate_risk(report_count: int) -> str:
    if report_count == 0:
        return "Safe"
    elif report_count <= 5:
        return "Low Risk"
    elif report_count <= 10:
        return "Medium Risk"
    else:
        return "High Risk"
