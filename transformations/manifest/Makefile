sourceDtd = manifest.dtd
tartgetDtd = permissions.dtd
update = transformation.upd
sourceXML = manifest.xml
targetXML = permissions.xml

all: u

u: u.hs
	ghc u.hs

u.hs: $(sourceDtd) $(tartgetDtd) $(update)
	BiFluX --sdtd=$(sourceDtd) --vdtd=$(tartgetDtd) --bx=$(update)  --bxhs=u.hs

forward: u $(sourceXML) $(targetXML)
	cp $(targetXML) target.xml.backup
	./u -f -s $(sourceXML) -t $(targetXML) -o $(targetXML) -d

backward: u $(sourceXML) $(targetXML)
	cp $(sourceXML) source.xml.backup
	./u -b -s $(sourceXML) -t $(targetXML) -o $(sourceXML)


recs:
	mv source.xml.backup $(sourceXML)

recv:
	mv target.xml.backup $(targetXML)

rec:
	mv source.xml.backup $(sourceXML)
	mv target.xml.backup $(targetXML)

shows:
	cat $(sourceXML)

showt:
	cat $(targetXML)

clean:
	rm -r *.hs *.hi *.o  u
