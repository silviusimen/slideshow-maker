import subprocess


def melt(commandline: str) -> str:
    output = subprocess.check_output(f"melt {commandline} 2>/dev/null", shell=True)
    return output


def melt_get_xml_info_for_video_file(filename: str) -> tuple:
    cmd = f"{filename} -consumer xml"
    output = melt(cmd)
    return output
