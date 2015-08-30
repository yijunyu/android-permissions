function main() {
cat ~/result/min-sdk-version.txt | while read f; do
  folder=$(echo $f | awk '{ split($1, a, /\//); print a[2]}')
  for f in $folder/comparison_*.xml; do
 	md5sum $f >> md5.txt
  done
done
}
main
