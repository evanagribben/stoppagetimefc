# Stoppage Time

The website for Evan Gribben's weekly soccer newsletters: https://stoppagetimefc.com

- `build.py` and `theme.py` build every page, in the same design as The Newsstand.
- `tools/mirror.py` copies editions from the public Newsstand repository
  (evanagribben/evanagribben.github.io), which pulls them from Google Drive.
- `.github/workflows/sync.yml` runs that copy and a rebuild every hour at :45.
