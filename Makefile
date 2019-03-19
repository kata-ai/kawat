build_dir := build
syntax_dir := $(build_dir)/syntax
semantic_dir := $(build_dir)/semantic

# File names must match those in `syntax` directory
syntax_files := $(syntax_dir)/nouns.txt $(syntax_dir)/verbs.txt
syntax_files += $(syntax_dir)/plurals.txt $(syntax_dir)/reduplications.txt

# File names must match those in `semantic` directory
semantic_files := $(semantic_dir)/antonyms.txt $(semantic_dir)/country-capitals.txt
semantic_files += $(semantic_dir)/country-currencies.txt $(semantic_dir)/gender-specific-words.txt
semantic_files += $(semantic_dir)/measure-words.txt $(semantic_dir)/province-capitals.txt

.PHONY: clean help

$(build_dir)/all.txt: $(build_dir)/semantic.txt $(build_dir)/syntax.txt
	cat $^ > $@

$(build_dir)/semantic.txt: $(semantic_files)
	cat $^ > $@

$(build_dir)/syntax.txt: $(syntax_files)
	cat $^ > $@

$(syntax_dir)/%.txt: syntax/%.txt
	mkdir -p $(syntax_dir)
	./make_pairs.py $< > $@

$(semantic_dir)/%.txt: semantic/%.txt
	mkdir -p $(semantic_dir)
	./make_pairs.py $< > $@

clean:
	rm -rf $(build_dir)/*.txt $(syntax_dir) $(semantic_dir)

help:
	@echo "make - build all KaWAT dataset"
	@echo "make clean - clean build files"
	@echo "make help  - print this help"
