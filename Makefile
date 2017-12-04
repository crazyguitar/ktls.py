.PHONY: all test clean

all: test

test:
	python3 ktls.py

clean:
	rm -rf $(CERT) $(KEY)
