# BG4h

bee gees for Humans Table Definitions

## ChangeLog

### v1.0.10 10.12.2024

- added defs for stockminmaxalmacen

### v1.0.9 01.12.2024

- fixed wrong defs on Inmovilizados
- added defs for OtrosCostes and ValoresOtrosCostes

### v1.0.8 01.12.2024

- added new fields to `bg_soc.py`
- fixed typos in `bg_main.py`
- added missing field definitions in various tables

### v1.0.7 25.11.2024

- added missing index field tarticulosavisos

### v1.0.6 27.09.2024

- added missing fields in ttareasavisos

### v1.0.5 17.09.2024

- added missing worker 1-3 fields -> tavisosreparacionesclientes

### v1.0.4 02.08.2024

- added missing fields
- fix misspeling table ttrabajosavisos -> trabajosavisos

### v1.0.3 13.03.2024

- fixed spelling in vars of Personal table in BgMain

### v1.0.2 - 27.01.2024

- added missing fields from table vacaciones

### v1.0.1 - 10.01.2024

- added long description to setup.py
- fixed ttarea6 -> to TTAREAS6

### v1.0.0 - 18.12.2023

- ts/net lib converted to python
- spellfix
- added todos for unknown / unclear values

# Publish

Hacer Build:
python setup.py sdist

Publicar:
twine upload dist/*   
