.PHONY: all
all: locale

TRANS_TARGET=$(shell find -iname "messages.po")

.PHONY: trans
locale: $(patsubst %/messages.po,%/messages.mo,$(TRANS_TARGET))

src/grotten/locale/base.pot: src/grotten/*.py src/grotten/*/*.py
	pybabel extract --output src/grotten/locale/base.pot ./

%/messages.po: src/grotten/locale/base.pot
	pybabel update --input-file src/grotten/locale/base.pot --output-dir src/grotten/locale/

%/messages.mo: %/messages.po
	pybabel compile --directory src/grotten/locale/
