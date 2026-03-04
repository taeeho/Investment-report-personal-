def route_experts(company, has_financials=True, has_news=True):
    experts = ["summary"]
    if has_news:
        experts.append("sentiment")
    if has_financials:
        experts.append("fundamental")
    experts.append("risk")
    return experts
