from .models import SpendingRules, EndUser
import time

def ValidateSpendingRule(enduser, amount):
    spending_rule = SpendingRules.objects.get(user = enduser)
    if spending_rule.enable_next_txn:
        return True

    if (time.time() - spending_rule.start_time) > spending_rule.reset_period:
        spending_rule.total_txn_amt = 0
        spending_rule.txn_no = 0
        spending_rule.start_time  = time.time()
        spending_rule.save()

    if (spending_rule.txn_no == spending_rule.txn_no_limit) or (spending_rule.total_txn_amt + amount > spending_rule.total_txn_amt_limit) or (amount > spending_rule.per_txn_amt_limit):
        return False
    else:
        spending_rule.txn_no = spending_rule.txn_no + 1
        spending_rule.total_txn_amt = spending_rule.total_txn_amt + amount
        spending_rule.save()
        return True        