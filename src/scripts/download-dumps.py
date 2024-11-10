import os
import sys
import requests
import hashlib
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_ATTEMPTS = 10

dumps_folder = "../../dumps"

"""
    download_file
"""
def download_file(url, folder, file_name, expected_checksum):
    part_file = os.path.join(folder, f"{file_name}.part")
    dest_file = os.path.join(folder, file_name)

    for attempt in range(MAX_ATTEMPTS):
        try:
            # - Getting the part file size
            part_file_size = 0
            if os.path.exists(part_file):
                part_file_size = os.path.getsize(part_file)

            # - Requesting the download
            headers = { "Range": f"bytes={part_file_size}-" }
            response = requests.get(url, headers, stream=True)

            # - Checking whether the file has already been downloaded

            if os.path.exists(dest_file):
                print(f"[LOG] Already downloaded: {file_name}")
                return

            if response.status_code == 416:
                print(f"[LOG] Already downloaded: {file_name}")
                os.rename(part_file, dest_file)
                return

            elif response.status_code in (200, 206):
                total_size = int(response.headers.get("Content-Length", 0))

                progress = tqdm(
                    total=part_file_size + total_size,
                    initial=part_file_size,
                    unit="B",
                    unit_scale=True,
                    desc=f"{file_name} (attempt {attempt + 1})"
                )

                with open(part_file, "ab") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            progress.update(len(chunk))

                progress.close()

                with open(part_file, "rb") as file:
                    checksum = hashlib.md5(file.read()).hexdigest()

                    if checksum != expected_checksum:
                        print(f"[LOG] Checksums do not match for {file_name}. Deleting it.")
                        os.remove(part_file)

                    else:
                        os.rename(part_file, dest_file)
                        return
            else:
                print(f"Error {response.status_code}: {file_name}")
        except Exception as e:
            print(f"Error during download of {file_name}: {e}")

"""
    download_files
"""
def download_files(folder, files, max_workers=3):
    os.makedirs(folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers) as executor:
        for file_name, checksum, url in files:
            executor.submit(
                download_file,
                url,
                folder,
                file_name,
                checksum,
            )

"""
    main
"""
if __name__ == "__main__":
    files = [
        ("dump-1.7z", "cf24006a4e1533806ac920314f90e74c", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p1p4078.7z"),
        ("dump-2.7z", "342f78c1597612580a8437bb4bfbfc6e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p4079p12174.7z"),
        ("dump-3.7z", "94ba3471fa311c20e8ff41d1abb4c45c", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p12175p20116.7z"),
        ("dump-4.7z", "fc1d2ceda63ed4312359fc386a46b014", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p20117p32067.7z"),
        ("dump-5.7z", "ea0d9e818c20b482c5279c08371cf9f2", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p32068p40961.7z"),
        ("dump-6.7z", "e791cd1798bcd5f7fff02908995036ee", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p40962p59405.7z"),
        ("dump-7.7z", "52129aa54f2318cb8c604e17da8be4f7", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p59406p76823.7z"),
        ("dump-8.7z", "72f7905781d21904f176c7357877e534", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p76824p93817.7z"),
        ("dump-9.7z", "970d4c413e78395dc914c326ad5d504c", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p93818p110029.7z"),
        ("dump-10.7z", "9fdb8b1e76719d13d6f5f91f08430fb8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p110030p128402.7z"),
        ("dump-11.7z", "238ebed06968a59b748b013a6a2cfac4", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p128403p153167.7z"),
        ("dump-12.7z", "1779c18def7ce2d7464cc8254911abc6", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p153168p182903.7z"),
        ("dump-13.7z", "c0425346c561f4ba38aba9d26871210e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p182904p214362.7z"),
        ("dump-14.7z", "e8840c6049ae6064fa788f47539cdc2a", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p214363p244836.7z"),
        ("dump-15.7z", "ac79fb9bcfdc221f89e88cf3d64d379f", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p244837p277300.7z"),
        ("dump-16.7z", "de6b8e7d55735c87f2814cd01f908033", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p277301p313000.7z"),
        ("dump-17.7z", "9b24b0b54686a073b239b8da4dbd8a04", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history1.xml-p313001p316052.7z"),
        ("dump-18.7z", "d036784ccd286d818ff8f469c63ba1aa", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p316053p365164.7z"),
        ("dump-19.7z", "0b6afb744231a4ba29d4875611da28da", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p365165p422094.7z"),
        ("dump-20.7z", "dddde4b2b592f11a8f6b1d173730bbf6", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p422095p475113.7z"),
        ("dump-21.7z", "3898038b777074bd0cb9a35e41a39413", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p475114p511258.7z"),
        ("dump-22.7z", "042129b9727d5beeb680ba02984c65f5", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p511259p552580.7z"),
        ("dump-23.7z", "406dd71da32ae00bc30abb6bb64842c8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p552581p599078.7z"),
        ("dump-24.7z", "752f8d6accc4a753bedb727ae9356c2a", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p599079p649824.7z"),
        ("dump-25.7z", "1c4b443757cfc7643b6a99d9c5e71220", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p649825p697308.7z"),
        ("dump-26.7z", "0cc372022409e0520d71caaf57d5559d", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p697309p743724.7z"),
        ("dump-27.7z", "c54dc9d71f07af6e67243d037b09a056", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p743725p801601.7z"),
        ("dump-28.7z", "b0a8ed21051a4758f66ea964f1ceb638", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p801602p862155.7z"),
        ("dump-29.7z", "4a7e1f1dfb8bf8fce7ac0be09f78ddbe", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p862156p986800.7z"),
        ("dump-30.7z", "65d2b483d9a610b44a614a2510bf5590", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p986801p1109100.7z"),
        ("dump-31.7z", "5d7773f3a4d04a9db0a91fc79995e2ad", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p1109101p1177946.7z"),
        ("dump-32.7z", "7064a3e30d56cedbdb4df37bb46007c5", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history2.xml-p1177947p1204973.7z"),
        ("dump-33.7z", "d44386dc6723c1bde4db19b0a6aecc11", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1204974p1264156.7z"),
        ("dump-34.7z", "4d773106c4ffcdb08a62964749210465", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1264157p1282619.7z"),
        ("dump-35.7z", "31f9936683316bc76e6f07c4ac82f76e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1282620p1293349.7z"),
        ("dump-36.7z", "bdef2fb917d891c8aee32ca12f96fc8b", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1293350p1351192.7z"),
        ("dump-37.7z", "25e8e5a0b2d593744ed7834c3d735377", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1351193p1418328.7z"),
        ("dump-38.7z", "277d4f336c28d2f604927bfcfc603ad9", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1418329p1487721.7z"),
        ("dump-39.7z", "89b0df17fd574dba67a1e81621ccf653", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1487722p1555595.7z"),
        ("dump-40.7z", "60d5845577c4ced90dd4c3f52a38dea9", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1555596p1621164.7z"),
        ("dump-41.7z", "fb6c786e503509ec0d3f514dc57fb160", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1621165p1696042.7z"),
        ("dump-42.7z", "9924d8eb885080d0f1958d78d9d29814", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1696043p1775688.7z"),
        ("dump-43.7z", "4f5dfe13fa46dbe5759798c9addb0b72", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1775689p1851256.7z"),
        ("dump-44.7z", "d82a2dc457f654c199da2adde4d37e14", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1851257p1924677.7z"),
        ("dump-45.7z", "18944b8154dec59761f3531d56621d81", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p1924678p2003706.7z"),
        ("dump-46.7z", "220d5829561f96997f3f43946179a5f8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p2003707p2085062.7z"),
        ("dump-47.7z", "36a1cb73d0a0462cdc92ecd9d361fc90", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p2085063p2162550.7z"),
        ("dump-48.7z", "9cdb159b7931a003ec2a62b563c3db83", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history3.xml-p2162551p2206774.7z"),
        ("dump-49.7z", "edb6f69e902077efe58ba273318424c8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2206775p2295446.7z"),
        ("dump-50.7z", "8cb3e517f3a0acfc13e0655d4b722f92", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2295447p2377605.7z"),
        ("dump-51.7z", "b005705b19527c86f744efa72dab6eb0", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2377606p2448763.7z"),
        ("dump-52.7z", "2d500e5fff99dd679197ceb5d9651546", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2448764p2540458.7z"),
        ("dump-53.7z", "9579efdc2fd5f2d67bd5e8d2390580d2", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2540459p2621251.7z"),
        ("dump-54.7z", "a4fdf374cb26983646a0409febac8a3c", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2621252p2701950.7z"),
        ("dump-55.7z", "89344211643dc6aa0bfffdac858d5a5e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2701951p2789396.7z"),
        ("dump-56.7z", "3d3a55283076cb7ca7fbe1d438189474", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2789397p2881682.7z"),
        ("dump-57.7z", "a8a5b761fc12fdf583fe42c9303694d1", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2881683p2978008.7z"),
        ("dump-58.7z", "4c51b0e031cf39f1f97cd69cf837f711", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p2978009p3083401.7z"),
        ("dump-59.7z", "d32d35230a43d225e74a15152fca743e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p3083402p3192398.7z"),
        ("dump-60.7z", "a9f33a81f501998bb261ba91bc7894af", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p3192399p3313119.7z"),
        ("dump-61.7z", "24f9e373067ccd013ccbd36d78e87ea3", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p3313120p3395173.7z"),
        ("dump-62.7z", "d51ffd5f9ec50dd0073579081a804f93", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p3395174p3519694.7z"),
        ("dump-63.7z", "cca1e12f10948c5425d56ecd6ee7cc17", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history4.xml-p3519695p3593336.7z"),
        ("dump-64.7z", "d5834b74f1c266429b1fe3d19dd65022", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p3593337p3708275.7z"),
        ("dump-65.7z", "7c8fb47d477798487f005828bc47ff82", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p3708276p3833994.7z"),
        ("dump-66.7z", "1769a39e23834e07158cb81b524e3970", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p3833995p3962697.7z"),
        ("dump-67.7z", "78bac6f0c78eafa92b652718f6bd8f6d", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p3962698p4100357.7z"),
        ("dump-68.7z", "f37229ac966a8c084db1537ff0561bb3", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4100358p4220619.7z"),
        ("dump-69.7z", "8b42d0a68b598894ba772d58616c81c9", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4220620p4361933.7z"),
        ("dump-70.7z", "983ec30f83dd1504904dd1af9c012645", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4361934p4508661.7z"),
        ("dump-71.7z", "6b436f3ee666fead1db65be0213f8c07", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4508662p4665070.7z"),
        ("dump-72.7z", "ef38bc27347b3bcd6d9bf162fabb0141", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4665071p4814799.7z"),
        ("dump-73.7z", "cfd899b849bf5c44fabee5e7711d6da8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4814800p4963445.7z"),
        ("dump-74.7z", "d6c9c8baab0fcee2b39a2056d6442bca", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p4963446p5131593.7z"),
        ("dump-75.7z", "7fe07907c057219f08afa1028ee1956a", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p5131594p5303152.7z"),
        ("dump-76.7z", "09a8bb4cc1bf6efe239c19fe1c0763c8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p5303153p5498805.7z"),
        ("dump-77.7z", "42c6746088a5dd162407e99dd369a86e", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p5498806p5703180.7z"),
        ("dump-78.7z", "5ed6c7ecf9ccd01fa67631995b36e780", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p5703181p5879474.7z"),
        ("dump-79.7z", "de4702ea45878d05535475a735fbca87", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history5.xml-p5879475p5915379.7z"),
        ("dump-80.7z", "edfe5cb5568158c067b9aa1c3572a4de", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p5915380p6103833.7z"),
        ("dump-81.7z", "dfaf83e4ec64e116de50e70ad43e5d46", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p6103834p6299734.7z"),
        ("dump-82.7z", "8f5af3a85137913722fd225e5117333d", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p6299735p6482058.7z"),
        ("dump-83.7z", "5cd884eb8f2f0ae89ec271258137c8ac", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p6482059p6733663.7z"),
        ("dump-84.7z", "bb70294c5d68eb485feea872a9d52e3d", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p6733664p7358356.7z"),
        ("dump-85.7z", "102952f83cf4ac84ceed3663b451e224", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p7358357p7652441.7z"),
        ("dump-86.7z", "64dd6d7ac043c93166544725d1416a18", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p7652442p7863371.7z"),
        ("dump-87.7z", "95a7a4f8e250f7458955b6f0cc2d778a", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p7863372p8104005.7z"),
        ("dump-88.7z", "8fc822d317105157be7ad728ad826ea8", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p8104006p8318295.7z"),
        ("dump-89.7z", "0108b9eff7eaa19de61b3a3c5ec0e055", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p8318296p8568857.7z"),
        ("dump-90.7z", "3412e045adb322aa7923fcd58623c443", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p8568858p8769007.7z"),
        ("dump-91.7z", "fbc76e8f25eb689e3329c8bf08f28b96", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p8769008p9027695.7z"),
        ("dump-92.7z", "1546f1ed377418711f8cc66d947fb7b1", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p9027696p9377365.7z"),
        ("dump-93.7z", "108253fd6f28fb6e516a73a25da47238", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p9377366p9706155.7z"),
        ("dump-94.7z", "a29f3b2e7be64e6c61e214c7cff17f34", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p9706156p10121637.7z"),
        ("dump-95.7z", "db0720106cceee33b57f4d465f0c6bf0", "https://dumps.wikimedia.org/itwiki/20241001/itwiki-20241001-pages-meta-history6.xml-p10121638p10252496.7z"),
    ]

    download_files(dumps_folder, files)
