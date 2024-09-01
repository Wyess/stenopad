all:
	asy waseda.asy
	mv ./waseda_asy.toml _waseda_asy.toml
	./load.py
	rm ./_waseda_asy.toml
