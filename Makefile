.PHONY: all clean

all:
	python3 generate.py

clean:
	rm -rf site
