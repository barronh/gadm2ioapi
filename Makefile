all: \
  original/gadm36_shp.zip original/gadm36.shp \
  projected/updated defn/updated \
  ioapi/updated ioapi_frac/updated

original/gadm36_shp.zip:
	wget -O $@ https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_shp.zip

original/gadm36.shp: original/gadm36_shp.zip
	cd original; unzip ../$<

projected/updated: original/gadm36.shp
ioapi/updated: projected/updated defn/updated
ioapi_frac/updated: ioapi/updated

%/updated: scripts/make_%.sh
	./$< &> $@
