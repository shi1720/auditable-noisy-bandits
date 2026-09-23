#!/usr/bin/env python3
"""Build both paper variants with Tectonic; reject broken references/overflow."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
engine = shutil.which('tectonic')
if engine is None:
    raise SystemExit('Install Tectonic, then rerun this builder.')
out = ROOT / 'output' / 'pdf'
out.mkdir(parents=True, exist_ok=True)
for variant, name in [('anonymous', 'when-rankings-are-not-enough-anonymous'),
                      ('author', 'when-rankings-are-not-enough')]:
    subprocess.run([engine, '-X', 'compile', str(ROOT/'paper'/f'{variant}.tex'),
                    '--outdir', str(out), '--keep-logs'], check=True, cwd=ROOT)
    log = (out / f'{variant}.log').read_text(errors='replace')
    failures = [line for line in log.splitlines()
                if 'Overfull \\hbox' in line or 'undefined' in line.lower()
                or 'Missing character' in line]
    if failures:
        raise SystemExit('PDF needs correction:\n' + '\n'.join(failures))
    (out/f'{variant}.pdf').replace(out/f'{name}.pdf')
    for suffix in ['aux', 'bbl', 'blg', 'out', 'log']:
        (out / f'{variant}.{suffix}').unlink(missing_ok=True)
    print(f'Built {name}.pdf')
