import geopandas as gpd

def geocode(address, provider="nominatim"):
    all_addresses = ['2224 Shattuck Avenue Berkeley CA',
       '1799 Solano Avenue Berkeley CA',
       '1444 Shattuck Place Berkeley CA',
       '3001 Telegraph Avenue Berkeley CA',
       '2128 Oxford Street Berkeley CA']
    
    print(address)
    print(provider)
    print("address in addresses?", (address in all_addresses))
    my_index = all_addresses.index(address)
    print(my_index)
    gdf = gpd.read_file("../../notebooks/geospatial/ex4_files/add_{}.shp".format(my_index))
    print(gdf.head())
    return gdf