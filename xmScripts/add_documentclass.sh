for f in */*.tex; do
  tmpfile=$(mktemp)
  echo "Doing $f (via $tmpfile)"
  cat header.txt "$f" > "$tmpfile"
  echo -e "\n\n\\\\end{document}" >> "$tmpfile"
  mv "$tmpfile" "$f"
done





##  sed -i "s?\\\\input{Ex?%% SKIPPED %% \\\\input{Ex?" */*.tex
##  sed -i "s/PNG/png/" */*.tex

## for f in */Exe*.tex; do sed -i "6i\\\\\\mfpicnumber{1} \\\\opengraphsfile{$(basename $f .tex)} % mfpic settings added " $f; done 


## for f in *; do [[ -f $f/$f.tex ]] && mv $f/$f.tex $f/$f.txt; done 

## sed -i "s?\\\\begin{defn}?\\\\^Cgin{definition}?" */*.tex     # etcetera ...

## sed -i  's?^\\colorbox{ResultColor}{\\bbm?%% \\colorbox{ResultColor}{\\bbm?' */*.tex
## sed -i  "s?\\\\ebm}?%% \\\\ebm}?" */*.tex