import funkyheatmappy as fhm
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib

def mtcars():
    mtcars = pd.read_csv("./test/data/mtcars.csv")
    mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
    column_info = pd.DataFrame(
        {
            "id": mtcars.columns,
            "group": [
                pd.NA,
                "overall",
                "overall",
                "group1",
                "group1",
                "group1",
                "group1",
                "group2",
                "group2",
                "group2",
                "group2",
                "group2",
            ],
            "name": [
                "",
                "Miles / gallon",
                "Number of cylinders",
                "Displacement (cu.in.)",
                "Gross horsepower",
                "Rear axle ratio",
                "Weight (1000 lbs)",
                "1/4 mile time",
                "Engine",
                "Transmission",
                "# Forward gears",
                "# Carburetors",
            ],
            "geom": [
                "text",
                "bar",
                "bar",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "circle",
                "circle",
                "circle",
                "circle",
                "circle",
            ],
            "options": [
                {"ha": 0, "width": 6},
                {"width": 4, "legend": False},
                {"width": 4, "legend": False},
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
            ],
            "palette": [
                np.nan,
                "palette1",
                "palette2",
                "palette1",
                "palette1",
                "palette1",
                "palette1",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
            ],
        }
    )
    column_info.index = column_info["id"]
    column_groups = pd.DataFrame(
        {
            "Category": ["Overall", "Group1", "Group2"],
            "group": ["overall", "group1", "group2"],
            "palette": ["ocerall", "palette1", "palette2"],
        }
    )
    row_info = pd.DataFrame({"id": mtcars["id"], "group": "test"}, index=mtcars["id"])
    row_groups = pd.DataFrame({"Group": ["Test"], "group": ["test"]})
    norm = matplotlib.colors.Normalize(vmin=0, vmax=101, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap="Greys")
    colors = [mapper.to_rgba(i) for i in range(0, 101)]
    palettes = pd.DataFrame(
        {
            "palettes": ["palette1", "palette1", "palette2"],
            "colours": ["Greys", "Blues", "Reds"],
        }
    )
    return {
        "data": mtcars,
        "column_info": column_info,
        "column_groups": column_groups,
        "row_info": row_info,
        "row_groups": row_groups,
        "palettes": palettes,
    }

mtcars = mtcars()

mtcars["data"]["type"] = np.concatenate(
    (np.repeat("ice", 10), np.repeat("electric", 22))
)
mtcars["column_info"] = pd.concat(
    [
        mtcars["column_info"],
        pd.DataFrame(
            {
                "id": ["type"],
                "group": ["group2"],
                "name": ["columnname"],
                "geom": ["image"],
                "options": [{"path": "./test/data/", "filetype": "png"}],
                "palette": [np.nan],
            },
            index=["type"],
        ),
    ]
)
res = fhm.funky_heatmap(
    data=mtcars["data"],
    column_info=mtcars["column_info"],
    column_groups=mtcars["column_groups"],
    row_info=mtcars["row_info"],
    row_groups=mtcars["row_groups"],
    palettes=mtcars["palettes"]
)

res.savefig("mtcars_test.png")