_default:
	@echo "make"
sources:
	@echo "make sources"
srpm: sources
	rpmbuild -bs --define '_sourcedir .' --define '_srcrpmdir .' fermilab-conf_ocsinventory.spec
