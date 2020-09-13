from backend.investors_database.database import InvestorsDB

def test_adding_and_searching(idb):
    try:
        idb.add_investor(investor_name="investor1", investor_regions=["kenya"],
                             investor_sectors=["agriculture", "training", "transportation and logistics"], investor_website="www.investor1.com",
                             investor_description=" ")
    except Exception as e:
        try:
            idb.update_investor(investor_name="investor1", col_name="regions", args=["kenya"])
        except Exception as e:
            print(e)

    try:
        idb.add_investor(investor_name="investor2", investor_regions=["Africa"],
                             investor_sectors=["agriculture", "training", "transportation and logistics"], investor_website="www.investor2.com",
                             investor_description=" ")
    except Exception as e:
        try:
            idb.update_investor(investor_name="investor2", col_name="regions", args=["Africa"])
            idb.update_investor(investor_name="investor2", col_name="name", args="investor3")
        except Exception as e:
            print(e)

    s = idb.acquire_element("investor1", "sectors")
    r = idb.acquire_element("investor1", "regions")

    search_result1 = idb.search("regions", ["kenya"])
    search_result2 = idb.search("regions", ["Africa"])

    return

import pandas

if __name__ == "__main__":
    sectors_dir = "./data/sectors.txt"
    regions_dir = "./data/regions.txt"
    db_dir = "./data/investor.db"

    idb = InvestorsDB(db_dir, sectors_dir, regions_dir)

    csv_dir = "../data/invs2.csv"
    csv_file = pandas.read_csv(csv_dir)
    assert(set(idb.col_names) in set(csv_file.columns))

    test_adding_and_searching(idb)

    print("done")