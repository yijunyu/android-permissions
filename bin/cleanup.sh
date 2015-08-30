function pscout_mapping() {
 case $1 in
2.2.3)
    echo 8
	;;
2.3.6)
    echo 10
	;;
3.2.2)
    echo 13
	;;
4.0.1)
    echo 14
	;;
4.1.1)
    echo 16
	;;
 esac
}

function pscout_remove() {
  pscout_releases="2.2.3 2.3.6 3.2.2 4.0.1 4.1.1"
  for p in $pscout_releases; do
	v=$(pscout_mapping $p)
	if [ "$v" -lt "$1" -o "$v" -gt "$2" ]; then
		echo $p
	fi
  done
}

function main() {
cat ~/result/min-sdk-version.txt | while read f; do
  minver=$(echo $f | awk '{ print $3}' | sed -e "s/'//g" )
  folder=$(echo $f | awk '{ split($1, a, /\//); print a[2]}')
  maxver=$(grep targetSdkVersion ~/result/$folder/$folder/apktool.yml | awk '{ print $2}' | sed -e "s/'//g" )
  if [ "$maxver" == "" ]; then
	maxver=22
  fi
  echo $folder $minver $maxver
  release=$(pscout_remove $minver $maxver)
  if [ ! -d $folder ]; then
	echo cp -r ~/result/$folder .
	cp -r ~/result/$folder .
  fi
  rm -rf $folder/$folder
  if [ "$release" != "" ]; then
	  for r in $release; do
		echo rm -f $folder/comparison_$r.xml
		rm -f $folder/comparison_$r.xml
		echo rm -f $folder/code_permissions_$r.xml
		rm -f $folder/code_permissions_$r.xml
	  done
  fi
done
}
main
