from API.Search.Search import search_by_category, search_by_location, extended_search, search_offers
from API.setup_database import SessionLocal


def test_search_functions():
    db = SessionLocal()

    # Test 1: testing search_by_category
    conditions = search_by_category(db, category_id=28)
    assert conditions is not None, "No conditions were created for category search"

    # Test 2: testing search_by_location
    conditions = search_by_location(db, location="Hamburg")
    assert conditions is not None, "No conditions were created for location search"

    # Test 3: testing extended_search
    conditions = extended_search(db, min_price=1.00, max_price=100.0)
    assert conditions is not None, "No conditions were created for extended search"

    # Test 4: testing search_offers
    results = search_offers(db, query="Au", category_id=28, location="Hamburg", min_price=1.00, max_price=100.0)
    assert results is not None, "No results for offer search"
    assert len(results) > 0, "No offers found"

    db.close()

    print("All search function tests passed!")
