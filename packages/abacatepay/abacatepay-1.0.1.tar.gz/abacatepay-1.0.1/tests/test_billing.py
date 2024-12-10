from abacatepay import AbacatePay

def test_list_billings(list_billings_response):
    client = AbacatePay("dummy-token")
    billings = client.list_bills()
    assert len(billings) == 1

def test_list_more_than_one_billing(list_more_than_one_billing_response):
    client = AbacatePay("dummy-token")
    billings = client.list_bills()
    assert len(billings) == 2
