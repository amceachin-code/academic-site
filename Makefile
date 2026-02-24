.PHONY: build preview clean validate install

# Path to add node_modules/.bin to PATH for tailwindcss
export PATH := $(shell pwd)/site/node_modules/.bin:$(PATH)

validate:
	python scripts/build_all.py --validate

build:
	python scripts/build_all.py
	cd site && hugo --minify

preview: build
	cd site && hugo server

clean:
	rm -f cv/output/McEachin_CV.tex cv/output/*.aux cv/output/*.log cv/output/*.out
	rm -f cv/output/*.fls cv/output/*.fdb_latexmk cv/output/*.synctex.gz

install:
	pip install -r scripts/requirements.txt
	cd site && npm install
