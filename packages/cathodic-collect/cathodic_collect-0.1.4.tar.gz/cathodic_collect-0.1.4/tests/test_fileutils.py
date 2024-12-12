import pathlib as p

from cathodic_collect import fileutils


def file_list():
    folder = "./src/resources/2024-12-11-test"
    filenum = 2

    filelist = []
    for i in range(1, filenum + 1):
        # ac dc 在阶段2 是一样的
        filelist.append("result_%s_%d_2.csv" % ("dc", i))

    return [p.Path(folder) / file for file in filelist]


def test_merge_stage_2_files():
    df_list = fileutils.read_file_list(file_list())
    folder = p.Path("./tmp/20241211")
    folder.mkdir(parents=True, exist_ok=True)
    fileutils.merge_stage_2_files(df_list, folder / "output_2.csv")
