def surface(ds, press_level):
    surf_valid = ds.surface.where(ds.batimetry <= -press_level)
    area = surf_valid.sum().values
    return area