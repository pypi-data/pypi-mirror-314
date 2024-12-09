set_publish = "PR"  # "DV", "PR"

if set_publish == "PR":
    API_PYTHON_EXECUTOR = "https://moa.midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.midasit.com/backend/wgsd/dbase/sections/"
elif set_publish == "DV":
    API_PYTHON_EXECUTOR = "https://moa.rpm.kr-dv-midasit.com/backend/python-executor/"
    API_SECTION_DATABASE = "https://moa.rpm.kr-dv-midasit.com/backend/wgsd/dbase/sections/"
else:
    raise ValueError(f"Invalid set_publish: {set_publish}")
