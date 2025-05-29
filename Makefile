# FILE = pseudo_adder.txt
FILE ?= pseudo_4x4_mult.txt

.PHONY: test_cf test_re test_sa

test_cf:
	clear && python3 dv/test_cf.py regularity/${FILE}

test_re:
	clear && python3 dv/test_re.py regularity/${FILE}

test_sa:
	clear && python3 dv/test_sa.py regularity/${FILE}

main:
	clear && python3 rtl/main.py regularity/${FILE}