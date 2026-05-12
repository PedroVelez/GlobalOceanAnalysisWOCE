'''This function is used to calculate the surface of a given level for a given dataset. It is used in the Heat flux calculations'''

def surface(ds, press_level):
    surf_valid = ds.surface.where(ds.batimetry <= -press_level)
    area = surf_valid.sum().values
    return area