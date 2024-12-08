#!/usr/bin/python3

import argparse
import wget
from datetime import datetime, timedelta
from ppgnss import gnss_time  # 导入 ppnss 库中的时间转换模块
import os


def parse_year_and_doy(value):
    try:
        year, doy = map(int, value.split(','))
        return year, doy
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid year,doy format. Example: --from 2023,100")


def download_brdc_data(year, doy, out_dir="."):
    base_url = "ftp://igs.gnsswhu.cn/pub/gps/data/daily"
    yr = str(year)[2:]
    doy_str = f"{doy:03d}"  # 使用 zfill 将 doy 格式化为三位数字
    url = f"{base_url}/{year}/{doy_str}/{yr}p/BRDM00DLR_S_{year}{doy_str}0000_01D_MN.rnx.gz"
    filename = os.path.join(out_dir, f"BRDM00DLR_S_{year}{doy_str}0000_01D_MN.rnx.gz")

    try:
        wget.download(url, out=filename)
        print(f"\nDownloaded BRDC data for {year}-{doy_str} to {filename}")
    except Exception as e:
        print(f"Failed to download BRDC data for {year}-{doy_str}. Error: {e}")


def download_gim_data(year, doy, out_dir="."):
    base_url = "http://ftp.aiub.unibe.ch/CODE"
    yr = str(year)[2:]
    doy_str = f"{doy:03d}"  # 使用 zfill 将 doy 格式化为三位数字

    # 判断时间，选择不同的 URL
    if datetime(year, 1, 1) + timedelta(days=doy - 1) <= datetime(2022, 11, 26):  # 2022年330天或之前
        url = f"{base_url}/{year}/CODG{doy_str}0.{yr}I.Z"
    else:
        url = f"{base_url}/{year}/COD0OPSFIN_{year}{doy_str}0000_01D_01H_GIM.INX.gz"

    # 本地文件名与远程文件名保持一致
    filename = os.path.join(out_dir, url.split("/")[-1])

    try:
        wget.download(url, out=filename)
        print(f"\nDownloaded GIM data for {year}-{doy_str} to {filename}")
    except Exception as e:
        print(f"Failed to download GIM data for {year}-{doy_str}. Error: {e}")


def download_snx_data(year, doy, ac="COD", freq="daily", out_dir="."):
    """
    freq: "daily", or "weekly"
    ac: "COD", or "GFZ", or "MIT", or "NGS", or "IGS"
    
    ftp://igs.gnsswhu.cn/pub/gps/products/2246/IGS0OPSSNX_20230240000_01D_01D_SOL.SNX.gz #
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/SIO0OPSFIN_20223340000_01D_01D_SOL.SNX.gz
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/COD0OPSFIN_20223310000_01D_01D_SOL.SNX.gz
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/GFZ0OPSFIN_20223370000_01D_01D_SOL.SNX.gz
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/MIT0OPSFIN_20223310000_01D_01D_SOL.SNX.gz
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/NGS0OPSFIN_20223360000_01D_01D_SOL.SNX.gz
    ftp://igs.gnsswhu.cn/pub/gps/products/2238/SIO0OPSFIN_20223320000_01D_01D_SOL.SNX.gz
                                               IGS0OPSSNX_yyyyddd0000_07D_07D_SOL.SNX.gz
    
    """
    gpsw, gpsd = gnss_time.doy2gpsw(year, doy)
    base_url = "ftp://igs.gnsswhu.cn/pub/gps/products"
    doy_str = f"{doy:03d}"
    
    if gpsw >= 2238:
        url = 1
    else:
        url = f"{base_url}/{gpsw:04d}/{ac}{gpsw:04d}{int(gpsd):01d}.snx.Z"
    

def download_sp3_data(year, doy, out_dir="."):
    gpsw, gpsd = gnss_time.doy2gpsw(year, doy)
    base_url = "ftp://igs.gnsswhu.cn/pub/gps/products"
    doy_str = f"{doy:03d}"

    if datetime(year, 1, 1) + timedelta(days=doy - 1) <= datetime(2022, 11, 26):  # 2022年330天或之前
        url = f"{base_url}/{gpsw:04d}/igs{gpsw:04d}{int(gpsd):01d}.sp3.Z"
    else:
        url = f"{base_url}/{gpsw}/IGS0OPSFIN_{year}{doy_str}0000_01D_15M_ORB.SP3.gz"

    filename = os.path.join(out_dir, f"IGS0OPSFIN_{year}{doy_str}0000_01D_15M_ORB.SP3.gz")
    print(url)
    try:
        wget.download(url, out=filename)
        print(f"\nDownloaded SP3 data for {year}-{doy_str} to {filename}")
    except Exception as e:
        print(f"Failed to download SP3 data for {year}-{doy_str}. Error: {e}")


def download_clk_data(year, doy, out_dir="."):
    gpsw, gpsd = gnss_time.doy2gpsw(year, doy)
    base_url = "ftp://igs.gnsswhu.cn/pub/gps/products"
    doy_str = f"{doy:03d}"  # 使用 zfill 将 doy 格式化为三位数字

    if datetime(year, 1, 1) + timedelta(days=doy - 1) <= datetime(2022, 11, 26):  # 2022年330天或之前
        url = f"{base_url}/{gpsw:04d}/igs{gpsw:04d}{int(gpsd):01d}.clk.Z"
    else:
        url = f"{base_url}/{gpsw:04d}/IGS0OPSFIN_{year}{doy_str}0000_01D_05M_CLK.CLK.gz"

    filename = os.path.join(out_dir, f"IGS0OPSFIN_{year}{doy_str}0000_01D_05M_CLK.CLK.gz")

    try:
        wget.download(url, out=filename)
        print(f"\nDownloaded CLK data for {year}-{doy_str} to {filename}")
    except Exception as e:
        print(f"Failed to download CLK data for {year}-{doy_str}. Error: {e}")


def download_rnx2_data(year, doy, site, out_dir="."):
    yr = year-2000
    url=f"ftp://igs.gnsswhu.cn/pub/gps/data/daily/{year:04d}/{doy:03d}/{yr:02d}d/{site}{doy:03d}0.{yr:02d}d.Z"

    filename = os.path.join(out_dir, f"wuhn{doy:03d}0.{yr:02d}d.Z")
    print(f"\ntrying to download {url}")
    try:
        wget.download(url, out=filename)
    except Exception as e:
        print(f"Failed to download rnx data for {year}-{doy}. Error: {e}")



def download_rnx3_data(year, doy, site, out_dir="."):
    yr = year-2000
    # url=f"ftp://igs.gnsswhu.cn/pub/gps/data/daily/{year:04d}/{doy:03d}/{yr:02d}d/{site}{doy:03d}0.{yr:02d}d.Z"
    url=f"ftp://igs.gnsswhu.cn/pub/gps/data/daily/{year:04d}/{doy:03d}/{yr:02d}d/{site}_R_{year:04d}{doy:03d}0000_01D_30S_MO.crx.gz"

    filename = os.path.join(out_dir, f"wuhn{doy:03d}0.{yr:02d}d.Z")
    print(f"\ntrying to download {url}")
    try:
        wget.download(url, out=filename)
    except Exception as e:
        print(f"Failed to download rnx data for {year}-{doy}. Error: {e}")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Download data for ppget script.")

    # 添加--data参数，允许的值为brdc, gim, sp3, clk
    parser.add_argument('--data', choices=['brdc', 'gim', 'sp3', 'clk', 'rnx2', 'rnx3'], help='Specify the type of data to download.')

    parser.add_argument("--site", dest="site", type=str, help="site name")
    # 添加--from参数，用于指定开始时间的年份和年积日
    parser.add_argument('--from', dest='start_date', type=parse_year_and_doy,
                        help='Specify the start date for data download. Format: year,doy')

    # 添加--to参数，用于指定结束时间的年份和年积日
    parser.add_argument('--to', dest='end_date', type=parse_year_and_doy,
                        help='Specify the end date for data download. Format: year,doy')

    # 添加--outdir参数，用于指定下载目录，默认为当前目录
    parser.add_argument('--outdir', default=".", help='Specify the local directory for downloaded files.')

    # 添加--help参数，显示脚本用法
    args = parser.parse_args()

    # 检查输出目录是否存在
    if not os.path.exists(args.outdir):
        print(f"Error: Directory '{args.outdir}' does not exist.")
        return

    if args.start_date and args.end_date:
        start_year, start_doy = args.start_date
        end_year, end_doy = args.end_date
        if args.data == "rnx2" or args.data == "rnx3":
            site = args.site
        start_date = datetime(start_year, 1, 1) + timedelta(days=start_doy - 1)
        end_date = datetime(end_year, 1, 1) + timedelta(days=end_doy - 1)

        current_date = start_date
        while current_date <= end_date:
            year, doy = current_date.year, current_date.timetuple().tm_yday

            if args.data == 'brdc':
                download_brdc_data(year, doy, out_dir=args.outdir)
            elif args.data == 'gim':
                download_gim_data(year, doy, out_dir=args.outdir)
            elif args.data == 'sp3':
                download_sp3_data(year, doy, out_dir=args.outdir)
            elif args.data == 'clk':
                download_clk_data(year, doy, out_dir=args.outdir)
            elif args.data=="rnx2":
                download_rnx2_data(year, doy, site, out_dir=args.outdir)
            elif args.data=="rnx3":
                download_rnx3_data(year, doy, site, out_dir=args.outdir)
            else:
                print(f"Error: Unsupported data type '{args.data}'")
                break

            current_date += timedelta(days=1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
