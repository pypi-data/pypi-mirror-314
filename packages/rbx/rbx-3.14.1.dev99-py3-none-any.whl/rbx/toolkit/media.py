from typing import Optional

import sh


def convert(
    infile: str,
    outfile: str,
    delay: Optional[str] = None,
    duration: Optional[int] = None,
    opts: Optional[list] = None,
):
    """Convert `infile` to `outfile`.

    For WebM to MP4 conversion, see
        https://blog.addpipe.com/converting-webm-to-mp4-with-ffmpeg/

    """
    args = ["-y"]
    if delay:
        args.extend(["-ss", delay])
    if duration:
        args.extend(["-t", duration])
    args.extend(["-i", infile])
    if opts:
        args.extend(opts)
    args.append(outfile)
    ffmpg(args)


def merge(infiles: [str], outfile: str) -> None:
    args = ["-y"]
    for file in infiles:
        args.extend(["-i", file])
    args.extend(["-c", "copy", outfile])
    ffmpg(args)


def ffmpg(args):
    try:
        sh.ffmpeg(*args)
    except sh.ErrorReturnCode as e:
        raise RuntimeError(
            f"Command {e.full_cmd} exited with {e.exit_code}\n\n{e.stderr.decode()}"
        )
