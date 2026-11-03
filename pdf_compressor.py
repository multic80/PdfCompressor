#!/usr/bin/env python3
"""Ghostscript로 PDF 내부 이미지의 DPI와 JPEG 품질을 낮춰 용량을 줄이는 도구."""
import argparse
import os
import shutil
import subprocess
import sys


def find_ghostscript():
    for name in ("gs", "gswin64c", "gswin32c"):
        path = shutil.which(name)
        if path:
            return path
    return None


def build_command(gs, src, dst, dpi=150, quality=50):
    if dpi < 1:
        raise ValueError("dpi must be >= 1")
    if not 1 <= quality <= 100:
        raise ValueError("quality must be between 1 and 100")
    # Ghostscript QFactor: 낮을수록 고품질. quality(1-100)를 0.1~2.4 범위로 변환
    qfactor = round(0.1 + (100 - quality) / 100 * 2.3, 2)
    cmd = [
        gs, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        "-dNOPAUSE", "-dBATCH", "-dQUIET", "-dSAFER",
        "-dDownsampleColorImages=true", "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        f"-dColorImageResolution={dpi}", f"-dGrayImageResolution={dpi}",
        f"-dMonoImageResolution={dpi}",
        "-dAutoFilterColorImages=false", "-dAutoFilterGrayImages=false",
        "-dColorImageFilter=/DCTEncode", "-dGrayImageFilter=/DCTEncode",
        "-c", f"<< /ColorACSImageDict << /QFactor {qfactor} /Blend 1 "
        "/HSamples [2 1 1 2] /VSamples [2 1 1 2] >> "
        f"/GrayACSImageDict << /QFactor {qfactor} /Blend 1 "
        "/HSamples [1 1 1 1] /VSamples [1 1 1 1] >> >> setdistillerparams",
        "-f",
    ]
    cmd.insert(-3, f"-sOutputFile={dst}")
    cmd.append(src)
    return cmd


def compress(src, dst, dpi=150, quality=50):
    gs = find_ghostscript()
    if not gs:
        raise RuntimeError("Ghostscript(gs)를 찾을 수 없습니다.")
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    subprocess.run(build_command(gs, src, dst, dpi, quality), check=True)
    return os.path.getsize(src), os.path.getsize(dst)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--dpi", type=int, default=150, help="이미지 목표 DPI")
    p.add_argument("--quality", type=int, default=50,
                   help="JPEG 품질 1-100 (낮을수록 용량 감소)")
    a = p.parse_args(argv)
    try:
        before, after = compress(a.input, a.output, a.dpi, a.quality)
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1
    print(f"{before:,} -> {after:,} bytes ({after / before:.0%})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
