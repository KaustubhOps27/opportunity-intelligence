def get_research_evidence(company):
    """
    Manual research input for the POC.

    In a production system, this could be replaced with
    APIs, search, scraping, or other data sources.
    """

    research_evidence = []

    print(f"\nEnter external research evidence for {company}")
    print("Press Enter without typing anything when you are done.\n")

    while True:
        evidence_type = input(
            "Evidence type (funding/hiring/launch/repositioning): "
        ).strip()

        if not evidence_type:
            break

        evidence = input("Evidence: ").strip()
        source_url = input("Source URL: ").strip()

        research_evidence.append({
            "type": evidence_type,
            "evidence": evidence,
            "source_url": source_url
        })

    return research_evidence