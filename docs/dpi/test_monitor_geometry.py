from monitor_geometry import GetGeometry


gg = GetGeometry() #GetTkGeometry.GetTkGeometry()
# padding specified 10 % of screen dimensions
gg.get_tkinter_geometry(10.0, 10, 10)
geometry = gg.geometry
print(f"\ngeometry - 10% of monitor size 10 pixel x and y padding:\n{geometry}")

# padding not specified 60 % of screen dimensions
gg.get_tkinter_geometry(60.0)
geometry = gg.geometry
print(f"\ngeometry - 60% of monitor size centered (no pading specified):\n{geometry}")