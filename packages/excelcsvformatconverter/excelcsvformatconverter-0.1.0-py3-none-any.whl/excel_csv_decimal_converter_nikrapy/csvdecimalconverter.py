import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parsed_args = parser.parse_args()

    source: Path = parsed_args.source
    dst: Path = parsed_args.destination
    if source.is_dir() and dst.is_dir():
        convert_files_in_dir(source, dst)
    else:
        convert_csv_format(source, dst)


def convert_files_in_dir(source: Path, dst: Path):
    for src_file in source.iterdir():
        basename = Path(src_file).name
        dst_file = dst.joinpath(basename)
        convert_csv_format(src_file, dst_file)


def convert_csv_format(src_path: Path, dst_path: Path):
    with  open(src_path) as source_file:
        with open(dst_path, 'w') as outfile:
            for line in source_file:
                line = line.replace(",", ";")
                line = line.replace(".", ",")
                outfile.write(line)


if __name__ == "__main__":
    main()
