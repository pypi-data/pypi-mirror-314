import itertools
import warnings
from multiprocessing import Pool, cpu_count
from pathlib import Path

import arrow as ar
import pandas as pd
from tqdm import tqdm

warnings.filterwarnings("ignore")

from .cei import indices
from geoprepare import base


def remove_duplicates(lst):
    """

    :param lst:
    :return:
    """
    return list(set([i for i in lst]))


def get_admin_zone(country, dg_shp):
    admin_zone = "admin_1"
    country = country.title().replace(" ", "_")

    # Read in shapefile
    dg_country = dg_shp[dg_shp["ADMIN0"] == country]

    # Is the ADMIN2 column all None? If so, return admin_1 else return admin_2
    if dg_country.empty:
        admin_zone = "admin_1"
    elif not dg_country["ADMIN2"].isna().all():
        admin_zone = "admin_2"

    return admin_zone


class cei_runner(base.BaseGeo):
    def __init__(self, path_config_file):
        super().__init__(path_config_file)

        # Parse configuration files
        self.parse_config()

        self.dir_input = Path(self.parser.get("PATHS", "dir_input"))
        self.base_dir = Path(self.parser.get("PATHS", "dir_crop_inputs"))
        self.do_parallel = self.parser.getboolean("DEFAULT", "do_parallel")

    def collect_files(self):
        """
        1. Collect all the files which contain EO information
        2. Exclude files from the `processed` directory if it is already in
        processed_include_fall directory
        3. Create a dataframe that contains the following columns:
            - directory: name of directory where file is located
            - path: full path to file
            - filename: name of file
        :return: Return the dataframe created above
        """
        import geopandas as gp

        dg_shp = gp.read_file(
            self.dir_input
            / "Global_Datasets"
            / "Regions"
            / "Shps"
            / "adm_shapefile.shp",
            engine="pyogrio",
        )

        # Collect all the files which contain EO information
        df_files = pd.DataFrame(columns=["directory", "path", "filename", "admin_zone"])
        for filepath in self.base_dir.rglob("*.csv"):
            country = filepath.parents[0].name

            admin_zone = get_admin_zone(country, dg_shp)

            # If country is not in cc.COUNTRIES then skip
            # HACK: Skip korea for now, as it is giving errors
            if country == "republic_of_korea":
                continue

            # Get name of directory one level up
            process_type = filepath.parents[1].name

            # Get name of file
            filename = filepath.name

            # Add to dataframe
            df_files.loc[len(df_files)] = [process_type, filepath, filename, admin_zone]

        # Exclude those rows where directory is processed and file is already in
        # processed_include_fall directory
        no_fall = df_files["directory"] == "processed"
        include_fall = df_files[df_files["directory"] == "processed_include_fall"][
            "filename"
        ]

        df_files = df_files[~(no_fall & (df_files["filename"].isin(include_fall)))]

        return df_files

    def process_combinations(self, df, method):
        """
        Create a list of tuples of the following:
            - directory: name of directory where file is located
            - path: full path to file
            - filename: name of file
            - method: whether to compute indices for phenological stages or not
        This tuple will be used as input to the `process` function
        :param df:
        :param method:
        :return:
        """
        combinations = []

        for index, row in tqdm(df.iterrows()):
            combinations.extend(
                list(
                    itertools.product([row[0]], [row[1]], [row[2]], [row[3]], [method])
                )
            )

        combinations = remove_duplicates(combinations)

        return combinations

    def main(self, method):
        """

        :param method:
        :return:
        """
        # Create a dataframe of the files to be analyzed
        df_files = self.collect_files()

        combinations = self.process_combinations(df_files, method)

        # Add an element to the tuple to indicate the season
        # Last element is redo flag which is True if the analysis is to be redone
        # and False otherwise. Analysis is always redone for the current year
        # and last year whether file exists or not
        combinations = [
            (
                self.parser,
                status,
                path,
                filename,
                admin_zone,
                category,
                year,
                "gcvi",
                False,  # redo
            )
            for year in range(2001, ar.utcnow().year + 1)
            for status, path, filename, admin_zone, category in combinations
        ]

        # Only keep those entries in combinations where the third elemt is
        # mozambique, south_africa, angola or dem_people's_rep_of_korea
        # This is done to test the code for these countries
        combinations = [
            i
            for i in combinations
            if "ukraine_maize" in i[3]
            # or "lesotho_maize" in i[3] or
            # #   "namibia_" in i[2] or
            # "united_republic_of_tanzania_maize" in i[3]
            # or "zambia_maize" in i[3]
            # or "zimbabwe_maize" in i[3]
            # or "south_africa_maize" in i[3]
            # or "mozambique_maize" in i[3]
            # or "united_states_of_america" in i[3]
            # or "russian_federation" in i[3]
            # or "ukraine" in i[3]
        ]
        #                 "malawi" in i[2]]

        if False and self.do_parallel:
            num_cpu = int(cpu_count() * 0.6)
            with Pool(num_cpu) as p:
                for i, _ in enumerate(p.imap_unordered(indices.process, combinations)):
                    pass
        else:
            # Use the code below if you want to test without parallelization or
            # if you want to debug by using pdb
            pbar = tqdm(combinations)
            for i, val in enumerate(pbar):
                pbar.set_description(
                    f"Main loop {combinations[i][2]} {combinations[i][5]}"
                )
                indices.process(val)


def run(path_config_files=[]):
    """

    Args:
        path_config_files:

    Returns:

    """
    """ Check dictionary keys to have no spaces"""
    indices.validate_index_definitions()

    for method in [
        "monthly_r",  # "dekad_r"  # "dekad_r"
    ]:  # , "full_season", "phenological_stages", "fraction_season"]:
        obj = cei_runner(path_config_files)
        obj.main(method)


if __name__ == "__main__":
    run()
