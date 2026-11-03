#!/bin/bash
# Rebuilds the nikud dictionary in index.html after adding or changing questions.
# Needs: node + playwright (chromium), python3, network access to Dicta (nakdan.dicta.org.il).
set -e
cd "$(dirname "$0")"
node collect.js
python3 -c "import json,re;c=json.load(open('corpus.json'));json.dump(sorted(set(re.sub(r'\d+','7',x) for x in c)),open('uniq.json','w'),ensure_ascii=False)"
python3 dicta.py
python3 build.py > build.log
python3 final.py
rm -f corpus.json uniq.json dicta.json raw.json nik.json
echo "Done. Check build.log for words with more than one reading."
