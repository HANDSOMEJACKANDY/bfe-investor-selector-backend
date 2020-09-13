from backend.investors_database.database import InvestorsDB

if __name__ == "__main__":
    sectors_dir = "./data/sectors.txt"
    regions_dir = "./data/regions.txt"
    db_dir = "./data/investor.db"

    idb = InvestorsDB(db_dir, sectors_dir, regions_dir)

    try:
        idb.add_investor(investor_name="investor1", investor_regions=[],
                             investor_sectors=["agriculture", "training", "transportation and logistics"], investor_websites=["www.investor1.com"],
                             investor_crawled_texts=[" "])
    except Exception as e:
        print(e)

    try:
        idb.add_investor(investor_name="investor2", investor_regions=["Africa"],
                             investor_sectors=["agriculture", "training", "transportation and logistics"], investor_websites=["www.investor2.com"],
                             investor_crawled_texts=[" "])
    except Exception as e:
        print(e)

    try:
        idb.update_investor(investor_name="investor1", col_name="regions", args=["kenya"])
    except Exception as e:
        print(e)

    s = idb.acquire_element("investor1", "sectors")
    r = idb.acquire_element("investor1", "regions")

    search_result1 = idb.search("regions", ["kenya"])
    search_result2 = idb.search("regions", ["Africa"])

    idb = idb