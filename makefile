FILES :=                              \
		.gitignore												\
		makefile													\
		apiary.apib												\
    models.html                       \
			app/tests.py                    \
			app/models.py                   \
		IDB1.log													\
    IDB2.log

ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage
    PYLINT   := pylint
endif

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

IDB1.html: app/models.py
	pydoc3 -w app.models
	mv app.models.html models.html

IDB1.log:
	git log > IDB1.log

IDB2.log:
	git log > IDB2.log

clean:
	rm -f  .pylintrc
	rm -f  models.html
	rm -f  IDB1.log
	rm -f  IDB2.log
	rm -rf __pycache__

config:
	git config -l

format:
	autopep8 -i app/tests.py
	autopep8 -i app/models.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: IDB2.log
	-$(PYLINT) app/tests.py
