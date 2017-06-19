test:
	nose2-3 -s tests --with-cov

test-coverage-missing
	nose2-3 -s tests --with-cov --coverage-report html
